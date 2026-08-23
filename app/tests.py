from datetime import timedelta
from tempfile import TemporaryDirectory

from django.contrib import admin
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from .admin import AdminPageAdmin, NewsAdminForm, PageBlockInline
from .models import AdminPage, News, NewsPhoto, PageBlock


def test_image(name):
    return SimpleUploadedFile(
        name,
        b'GIF87a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04'
        b'\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;',
        content_type='image/gif',
    )


class NewsApiTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_directory = TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.media_directory.name)
        cls.media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.media_override.disable()
        cls.media_directory.cleanup()

    def setUp(self):
        self.client = APIClient()
        self.news = News.objects.create(
            title='Открытие нового корпуса',
            slug='new-building',
            photo=test_image('card.gif'),
            description='Краткое описание новости',
            detail_description='Полный текст новости',
            detail_photo_1=test_image('detail-1.gif'),
            detail_photo_2=test_image('detail-2.gif'),
            detail_photo_3=test_image('detail-3.gif'),
            published_at=timezone.now(),
        )

    def test_news_list_returns_card_fields_only(self):
        response = self.client.get('/api/news/')

        self.assertEqual(response.status_code, 200)
        item = response.json()['results'][0]
        self.assertEqual(item['title'], self.news.title)
        self.assertIn('photo_url', item)
        self.assertNotIn('detail_description', item)
        self.assertNotIn('detail_photo_1', item)

    def test_news_detail_returns_description_and_three_photos(self):
        response = self.client.get('/api/news/new-building/')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['detail_description'], 'Полный текст новости')
        for number in range(1, 4):
            self.assertTrue(data[f'detail_photo_{number}_url'].startswith('http://testserver/media/'))

    def test_inactive_news_is_not_public(self):
        self.news.is_active = False
        self.news.save()

        response = self.client.get('/api/news/new-building/')

        self.assertEqual(response.status_code, 404)

    def test_news_are_ordered_by_admin_order_then_publication_date(self):
        older = News.objects.create(
            title='Более старая новость', slug='older', photo=test_image('older.gif'),
            description='Кратко', detail_description='Подробно',
            detail_photo_1=test_image('older-1.gif'), detail_photo_2=test_image('older-2.gif'),
            detail_photo_3=test_image('older-3.gif'), published_at=timezone.now() - timedelta(days=1),
            order=1,
        )

        response = self.client.get('/api/news/')

        self.assertEqual([item['slug'] for item in response.json()['results']], ['new-building', older.slug])

    def test_home_news_returns_only_three_selected_items_in_home_order(self):
        self.news.show_on_home = True
        self.news.home_order = 2
        self.news.save()
        for position in (1, 3):
            News.objects.create(
                title=f'Главная {position}', slug=f'home-{position}', photo=test_image(f'home-{position}.gif'),
                description='Кратко', detail_description='Подробно', published_at=timezone.now(),
                show_on_home=True, home_order=position,
            )
        News.objects.create(
            title='Только общий список', slug='list-only', photo=test_image('list-only.gif'),
            description='Кратко', detail_description='Подробно', published_at=timezone.now(),
        )

        response = self.client.get('/api/news/?on_home=true')

        self.assertEqual(response.status_code, 200)
        self.assertEqual([item['home_order'] for item in response.json()['results']], [1, 2, 3])

    def test_detail_returns_addable_photos(self):
        NewsPhoto.objects.create(news=self.news, photo=test_image('additional.gif'), order=1)

        response = self.client.get('/api/news/new-building/')

        self.assertEqual(len(response.json()['detail_photos']), 1)
        self.assertTrue(response.json()['detail_photos'][0]['photo_url'].endswith('additional.gif'))


class NewsAdminTests(TestCase):
    def test_news_model_is_available_in_admin(self):
        self.assertIn(News, admin.site._registry)

    def test_home_position_must_be_between_one_and_three(self):
        form = NewsAdminForm(data={'show_on_home': True, 'home_order': 0})

        self.assertFalse(form.is_valid())
        self.assertIn('home_order', form.errors)


class StructuredContentAdminTests(TestCase):
    def setUp(self):
        self.root = AdminPage.objects.create(
            title='Главная страница', slug='admin-home', group=AdminPage.GROUP_HOME, order=1,
        )
        self.child = AdminPage.objects.create(
            title='Карусель фотографий', slug='admin-slider', group=AdminPage.GROUP_HOME,
            parent=self.root, order=2,
        )

    def test_inline_does_not_create_an_implicit_empty_block(self):
        inline = PageBlockInline(AdminPage, admin.site)

        self.assertEqual(inline.extra, 0)

    def test_upload_field_limit_supports_translated_page_inlines(self):
        self.assertGreaterEqual(settings.DATA_UPLOAD_MAX_NUMBER_FIELDS, 10000)

    def test_blocks_are_only_managed_inside_their_page(self):
        self.assertNotIn(PageBlock, admin.site._registry)
        self.assertIn(PageBlockInline, AdminPageAdmin.inlines)

    def test_subpage_is_visually_indented(self):
        model_admin = AdminPageAdmin(AdminPage, admin.site)

        rendered = str(model_admin.structured_title(self.child))

        self.assertIn('admin-page-depth-1', rendered)
        self.assertIn('↳', rendered)

    def test_admin_page_query_uses_structure_order(self):
        model_admin = AdminPageAdmin(AdminPage, admin.site)
        request = RequestFactory().get('/admin/app/adminpage/')

        pages = model_admin.get_queryset(request).filter(pk__in=(self.root.pk, self.child.pk))
        self.assertEqual(list(pages), [self.root, self.child])

    def test_home_page_has_direct_news_subsection_navigation(self):
        model_admin = AdminPageAdmin(AdminPage, admin.site)
        request = RequestFactory().get('/admin/app/adminpage/1/change/')

        fieldsets = model_admin.get_fieldsets(request, self.root)
        navigation = str(model_admin.news_management(self.root))

        self.assertEqual(fieldsets[-1][0], '1.5. Новости')
        self.assertIn('1.5.1. Новости на главной', navigation)
        self.assertIn('/admin/app/news/', navigation)

    def test_block_inline_loads_structure_javascript_and_compact_styles(self):
        inline = PageBlockInline(AdminPage, admin.site)

        self.assertIn('app/admin/page_blocks.js', inline.media._js)
        self.assertIn('app/admin/content_structure.css', inline.media._css['all'])

    def test_content_title_is_shown_in_page_content_section(self):
        model_admin = AdminPageAdmin(AdminPage, admin.site)
        request = RequestFactory().get('/admin/app/adminpage/1/change/')

        fieldsets = model_admin.get_fieldsets(request, self.root)

        for language in ('ru', 'ky', 'en'):
            self.assertIn(f'content_title_{language}', fieldsets[1][1]['fields'])


class PageContentApiTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.media_directory = TemporaryDirectory()
        cls.media_override = override_settings(MEDIA_ROOT=cls.media_directory.name)
        cls.media_override.enable()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.media_override.disable()
        cls.media_directory.cleanup()

    def setUp(self):
        self.client = APIClient()
        self.page = AdminPage.objects.create(
            title='Страница', content_title='Название контента', slug='content-page',
            group=AdminPage.GROUP_ABOUT,
        )

    def test_page_detail_returns_content_title(self):
        response = self.client.get('/api/pages/content-page/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['content_title'], 'Название контента')

    def test_any_block_type_returns_attached_file_for_frontend(self):
        block = PageBlock.objects.create(
            page=self.page, block_type=PageBlock.TYPE_TEXT, title='Текстовый блок',
            file=SimpleUploadedFile('document.txt', b'content', content_type='text/plain'),
        )

        response = self.client.get(f'/api/page-blocks/{block.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['page'], self.page.pk)
        self.assertTrue(response.json()['file_url'].startswith('http://testserver/media/'))
        self.assertTrue(response.json()['file_url'].endswith('document.txt'))
