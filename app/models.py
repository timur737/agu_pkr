from django.db import models


def normalize_link(value):
    if not value:
        return value
    value = value.strip()
    if not value or value.startswith(('/', '#')):
        return value
    first_part = value.split('/', 1)[0]
    if ':' in first_part and first_part.split(':', 1)[0].lower() in {'http', 'https', 'mailto', 'tel', 'ftp', 'ftps'}:
        return value
    return f"https://{value}"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        abstract = True


class AdminPage(BaseModel):
    """Editable site page shown in the admin panel in the requested structure."""

    GROUP_HOME = 'home'
    GROUP_ABOUT = 'about'
    GROUP_ABDRAKHMANOV = 'abdrakhmanov'
    GROUP_IDEOLOGY = 'ideology'
    GROUP_PROFESSIONAL_DEVELOPMENT = 'professional_development'
    GROUP_EDUCATION = 'education'
    GROUP_SCIENCE = 'science'
    GROUP_INTERNATIONAL = 'international'
    GROUP_CONTACTS = 'contacts'

    GROUP_CHOICES = [
        (GROUP_HOME, 'Главная страница'),
        (GROUP_ABOUT, 'О нас'),
        (GROUP_ABDRAKHMANOV, 'Жусуп Абдрахманов'),
        (GROUP_IDEOLOGY, 'Национальная Идеология'),
        (GROUP_PROFESSIONAL_DEVELOPMENT, 'Профессиональное развитие'),
        (GROUP_EDUCATION, 'Образование'),
        (GROUP_SCIENCE, 'Наука и инновации'),
        (GROUP_INTERNATIONAL, 'Международное сотрудничество'),
        (GROUP_CONTACTS, 'Контакты'),
    ]

    title = models.CharField(max_length=255, verbose_name="Название блока")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="Системный URL")
    group = models.CharField(max_length=40, choices=GROUP_CHOICES, verbose_name="Главная страница раздела")
    parent = models.ForeignKey('self', related_name='subpages', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Родительская страница")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    main_photo = models.ImageField(upload_to='pages/main/', blank=True, null=True, verbose_name="Главная фотография")
    description = models.TextField(blank=True, verbose_name="Описание", help_text="Можно вставлять ссылки через CKEditor. Для редиректа всей страницы используйте поле «Ссылка на редирект».")
    redirect_url = models.CharField(max_length=500, blank=True, verbose_name="Ссылка на редирект")
    pdf_file = models.FileField(upload_to='pages/pdfs/', blank=True, null=True, verbose_name="PDF файл")
    is_development = models.BooleanField(default=False, verbose_name="В разработке")

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "01. Страницы сайта"
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.redirect_url = normalize_link(self.redirect_url)
        super().save(*args, **kwargs)


class PageBlock(BaseModel):
    TYPE_TEXT = 'text'
    TYPE_PHOTO_TEXT = 'photo_text'
    TYPE_LINK = 'link'
    TYPE_PDF = 'pdf'
    TYPE_NUMBER = 'number'
    TYPE_SOCIAL = 'social'
    TYPE_SLIDER = 'slider'

    TYPE_CHOICES = [
        (TYPE_TEXT, 'Текст / description'),
        (TYPE_PHOTO_TEXT, 'Фото + description'),
        (TYPE_LINK, 'Ссылка под текстом'),
        (TYPE_PDF, 'PDF файл скрытый под текстом'),
        (TYPE_NUMBER, 'Текстовое поле с цифрой'),
        (TYPE_SOCIAL, 'Ссылка на социальную сеть'),
        (TYPE_SLIDER, 'Слайд карусели'),
    ]

    page = models.ForeignKey(AdminPage, related_name='blocks', on_delete=models.CASCADE, verbose_name="Страница")
    block_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_TEXT, verbose_name="Тип блока")
    title = models.CharField(max_length=255, blank=True, verbose_name="Название / текст ссылки")
    description = models.TextField(blank=True, verbose_name="Описание", help_text="Можно вставлять ссылки через CKEditor. Для блоков AVN/ЭОП и других редиректов используйте отдельное поле «Ссылка» ниже.")
    date = models.DateField(blank=True, null=True, verbose_name="Дата")
    photo = models.ImageField(upload_to='pages/blocks/photos/', blank=True, null=True, verbose_name="Фото")
    file = models.FileField(upload_to='pages/blocks/files/', blank=True, null=True, verbose_name="PDF файл")
    url = models.CharField(max_length=500, blank=True, verbose_name="Ссылка", help_text="Заполняйте для блоков типа «Ссылка», например AVN или ЭОП. Ссылка нормализуется автоматически.")
    value = models.CharField(max_length=120, blank=True, verbose_name="Значение / цифра")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Блок страницы"
        verbose_name_plural = "02. Блоки страниц"
        ordering = ['page__order', 'order', 'id']

    def __str__(self):
        return self.title or self.get_block_type_display()

    def save(self, *args, **kwargs):
        self.url = normalize_link(self.url)
        super().save(*args, **kwargs)
