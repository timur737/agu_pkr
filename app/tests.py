from datetime import timedelta
from tempfile import TemporaryDirectory

from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient

from .models import News


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


class NewsAdminTests(TestCase):
    def test_news_model_is_available_in_admin(self):
        self.assertIn(News, admin.site._registry)
