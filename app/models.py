from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class BaseModel(models.Model):
    """Base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_active = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        abstract = True


class MainPage(BaseModel):
    """Main page content"""
    main_photo = models.ImageField(upload_to='main_page/', blank=True, null=True, verbose_name="Главное фото")
    about_title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок об академии")
    about_description = models.TextField(blank=True, verbose_name="Описание об академии")
    about_link = models.CharField(max_length=200, blank=True, verbose_name="Ссылка об академии")

    class Meta:
        verbose_name = "Главная страница"
        verbose_name_plural = "Главная страница"

    def __str__(self):
        return "Главная страница"


class News(BaseModel):
    """News model"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL-адрес")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name="Фото")
    is_pinned = models.BooleanField(default=False, verbose_name="Закреплено")
    is_event = models.BooleanField(default=False, verbose_name="Событие")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class NewsPhoto(BaseModel):
    """Additional photos for news"""
    news = models.ForeignKey(News, related_name='photos', on_delete=models.CASCADE, verbose_name="Новость")
    photo = models.ImageField(upload_to='news/photos/', verbose_name="Фото")

    class Meta:
        verbose_name = "Фото новости"
        verbose_name_plural = "Фото новостей"

    def __str__(self):
        return f"Фото для {self.news.title}"


class Announcement(BaseModel):
    """Announcements model"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    is_pinned = models.BooleanField(default=False, verbose_name="Закреплено")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-is_pinned', '-date']

    def __str__(self):
        return self.title


class EducationProgram(BaseModel):
    """Education programs model"""
    PROGRAM_TYPES = [
        ('bachelor', 'Бакалавриат'),
        ('master', 'Магистратура'),
        ('phd', 'Аспирантура'),
        ('doctorate', 'Докторантура'),
        ('cppk', 'ЦППК - Центр подготовки и повышения квалификации'),
        ('spo', 'СПО - Среднее профессиональное образование'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название")
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPES, verbose_name="Тип программы")
    description = models.TextField(verbose_name="Описание")
    link = models.URLField(blank=True, verbose_name="Ссылка")
    photo = models.ImageField(upload_to='education/', blank=True, null=True, verbose_name="Фото")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Образовательная программа"
        verbose_name_plural = "Образовательные программы"
        ordering = ['order', 'title']

    def __str__(self):
        return f"{self.get_program_type_display()} - {self.title}"


class EducationDirection(BaseModel):
    """Education directions model"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    link = models.URLField(blank=True, verbose_name="Ссылка")
    photo = models.ImageField(upload_to='education/directions/', blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Направление образования"
        verbose_name_plural = "Направления образования"

    def __str__(self):
        return self.title


class LibraryCategory(BaseModel):
    """Library categories"""
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="URL-адрес")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Категория библиотеки"
        verbose_name_plural = "Категории библиотеки"
        ordering = ['order', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class LibraryResource(BaseModel):
    """Electronic library resources"""
    category = models.ForeignKey(LibraryCategory, related_name='resources', on_delete=models.CASCADE, verbose_name="Категория библиотеки")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='library/', blank=True, null=True, verbose_name="Фото")
    link = models.URLField(blank=True, verbose_name="Ссылка")
    file = models.FileField(upload_to='library/files/', blank=True, null=True, verbose_name="Файл")

    class Meta:
        verbose_name = "Ресурс библиотеки"
        verbose_name_plural = "Ресурсы библиотеки"

    def __str__(self):
        return self.title


class Contact(BaseModel):
    """Contacts model"""
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='contacts/', blank=True, null=True, verbose_name="Фото")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=50, blank=True, verbose_name="Телефон")
    address = models.TextField(blank=True, verbose_name="Адрес")
    map_url = models.URLField(blank=True, verbose_name="Ссылка на карту")
    map_embed = models.TextField(blank=True, verbose_name="Код карты (embed)")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return self.title


class ContactDepartment(BaseModel):
    """Contact departments"""
    DEPARTMENT_TYPES = [
        ('reception', 'Приемная и отделы'),
        ('academic', 'Академические структуры'),
        ('programs', 'Программы'),
    ]
    contact = models.ForeignKey(Contact, related_name='departments', on_delete=models.CASCADE, verbose_name="Контакт")
    department_type = models.CharField(max_length=20, choices=DEPARTMENT_TYPES, verbose_name="Тип отдела")
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Отдел контактов"
        verbose_name_plural = "Отделы контактов"

    def __str__(self):
        return f"{self.get_department_type_display()} - {self.title}"


class SocialLink(BaseModel):
    """Social media links"""
    name = models.CharField(max_length=100, verbose_name="Название")
    url = models.URLField(verbose_name="Ссылка")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Иконка")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Социальная сеть"
        verbose_name_plural = "Социальные сети"
        ordering = ['order']

    def __str__(self):
        return self.name


class AboutAcademy(BaseModel):
    """About Academy main content"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    main_photo = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Главное фото")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='about/', blank=True, null=True, verbose_name="Фото")
    additional_description = models.TextField(blank=True, verbose_name="Дополнительное описание")
    block1_title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок блока 1")
    block1_description = models.TextField(blank=True, verbose_name="Описание блока 1")
    block2_title = models.CharField(max_length=200, blank=True, verbose_name="Заголовок блока 2")
    block2_description = models.TextField(blank=True, verbose_name="Описание блока 2")
    mission_title = models.CharField(max_length=200, default="Миссия академии", verbose_name="Заголовок миссии")
    mission_description = models.TextField(blank=True, verbose_name="Описание миссии")

    class Meta:
        verbose_name = "Об академии"
        verbose_name_plural = "Об академии"

    def __str__(self):
        return "Об академии"


class Partner(BaseModel):
    """Partners model"""
    name = models.CharField(max_length=200, verbose_name="Название")
    photo = models.ImageField(upload_to='partners/', verbose_name="Логотип")
    url = models.URLField(blank=True, verbose_name="Ссылка")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"
        ordering = ['order']

    def __str__(self):
        return self.name


class AcademyCharter(BaseModel):
    """Academy Charter"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    file = models.FileField(upload_to='documents/charter/', blank=True, null=True, verbose_name="Файл")

    class Meta:
        verbose_name = "Устав академии"
        verbose_name_plural = "Устав академии"

    def __str__(self):
        return self.title


class AcademyHistory(BaseModel):
    """Academy History"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    file = models.FileField(upload_to='documents/history/', blank=True, null=True, verbose_name="Файл")

    class Meta:
        verbose_name = "История академии"
        verbose_name_plural = "История академии"

    def __str__(self):
        return self.title


class AcademyLogo(BaseModel):
    """Academy Logo"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    logo = models.ImageField(upload_to='logo/', verbose_name="Логотип")

    class Meta:
        verbose_name = "Логотип академии"
        verbose_name_plural = "Логотип академии"

    def __str__(self):
        return self.title


class OrganizationalStructure(BaseModel):
    """Organizational Structure"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    scheme = models.ImageField(upload_to='structure/', blank=True, null=True, verbose_name="Схема")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Организационная структура"
        verbose_name_plural = "Организационная структура"

    def __str__(self):
        return self.title


class Department(BaseModel):
    """Departments in organizational structure"""
    structure = models.ForeignKey(OrganizationalStructure, related_name='departments', on_delete=models.CASCADE, verbose_name="Организационная структура")
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Департамент"
        verbose_name_plural = "Департаменты"
        ordering = ['order']

    def __str__(self):
        return self.name


class AcademicCouncil(BaseModel):
    """Academic Council"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    composition = models.TextField(verbose_name="Состав УС")

    class Meta:
        verbose_name = "Ученый совет"
        verbose_name_plural = "Ученый совет"

    def __str__(self):
        return self.title


class AcademicCouncilFile(BaseModel):
    """Academic Council Files"""
    council = models.ForeignKey(AcademicCouncil, related_name='files', on_delete=models.CASCADE, verbose_name="Ученый совет")
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to='documents/council/', verbose_name="Файл")

    class Meta:
        verbose_name = "Файл ученого совета"
        verbose_name_plural = "Файлы ученого совета"

    def __str__(self):
        return self.title


class TradeUnion(BaseModel):
    """Trade Union Committee"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Профсоюзный комитет"
        verbose_name_plural = "Профсоюзный комитет"

    def __str__(self):
        return self.title


class QualityManagement(BaseModel):
    """Quality Management System"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")

    class Meta:
        verbose_name = "Система менеджмента качества"
        verbose_name_plural = "Система менеджмента качества"

    def __str__(self):
        return self.title


class QualityManagementFile(BaseModel):
    """Quality Management Files"""
    quality = models.ForeignKey(QualityManagement, related_name='files', on_delete=models.CASCADE, verbose_name="Система менеджмента качества")
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to='documents/quality/', verbose_name="Файл")

    class Meta:
        verbose_name = "Файл системы качества"
        verbose_name_plural = "Файлы системы качества"

    def __str__(self):
        return self.title


class Bulletin(BaseModel):
    """Bulletin АГУПКР"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Вестник АГУПКР"
        verbose_name_plural = "Вестник АГУПКР"

    def __str__(self):
        return self.title


class BulletinFile(BaseModel):
    """Bulletin Files"""
    bulletin = models.ForeignKey(Bulletin, related_name='files', on_delete=models.CASCADE, verbose_name="Вестник")
    title = models.CharField(max_length=200, verbose_name="Название")
    file = models.FileField(upload_to='documents/bulletin/', verbose_name="Файл")

    class Meta:
        verbose_name = "Файл вестника"
        verbose_name_plural = "Файлы вестника"

    def __str__(self):
        return self.title


class BudgetProgram(BaseModel):
    """Budget Programs Project"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    period = models.CharField(max_length=50, blank=True, verbose_name="Период")

    class Meta:
        verbose_name = "Проект бюджетных программ"
        verbose_name_plural = "Проект бюджетных программ"

    def __str__(self):
        return self.title


class HonoraryProfessor(BaseModel):
    """Honorary Professors"""
    name = models.CharField(max_length=200, verbose_name="Имя")
    photo = models.ImageField(upload_to='professors/', blank=True, null=True, verbose_name="Фото")
    description = models.TextField(verbose_name="Описание")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Почетный профессор"
        verbose_name_plural = "Почетные профессора"
        ordering = ['order']

    def __str__(self):
        return self.name


class InternationalCooperation(BaseModel):
    """International Cooperation"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    photo = models.ImageField(upload_to='cooperation/', blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Международное сотрудничество"
        verbose_name_plural = "Международное сотрудничество"

    def __str__(self):
        return self.title


class InternationalCooperationLink(BaseModel):
    """International Cooperation Links"""
    cooperation = models.ForeignKey(InternationalCooperation, related_name='links', on_delete=models.CASCADE, verbose_name="Международное сотрудничество")
    title = models.CharField(max_length=200, verbose_name="Название")
    url = models.URLField(verbose_name="Ссылка")

    class Meta:
        verbose_name = "Ссылка сотрудничества"
        verbose_name_plural = "Ссылки сотрудничества"

    def __str__(self):
        return self.title


class AcademicHonesty(BaseModel):
    """Academic Honesty"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='honesty/', blank=True, null=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Академическая честность"
        verbose_name_plural = "Академическая честность"

    def __str__(self):
        return self.title


class LegalDocument(BaseModel):
    """Legal Documents"""
    DOCUMENT_TYPES = [
        ('external', 'Внешние'),
        ('internal', 'Внутренние'),
    ]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name="Тип документа")
    file = models.FileField(upload_to='documents/legal/', verbose_name="Файл")

    class Meta:
        verbose_name = "Нормативно-правовой акт"
        verbose_name_plural = "Нормативно-правовые акты"

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.title}"


class Schedule(BaseModel):
    """Schedule model"""
    SCHEDULE_TYPES = [
        ('bachelor', 'Расписание бакалавра'),
        ('master', 'Расписание магистратуры'),
        ('spo', 'Среднее проф образование'),
        ('bells', 'Расписание звонков'),
        ('graph_pb', 'График учебного процесса ПБ на 2025-2026 учебный год'),
        ('graph_pm', 'График учебного процесса ПМ на 2026-2027 год'),
        ('graph_pm_fhz', 'График учебного процесса ПМ ФХЗ 2025-2027 учебные года'),
    ]
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPES, verbose_name="Тип расписания")
    file = models.FileField(upload_to='schedules/', verbose_name="Файл")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
        ordering = ['order']

    def __str__(self):
        return f"{self.get_schedule_type_display()} - {self.title}"


class Survey(BaseModel):
    """Survey/Questionnaire model"""
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(blank=True, verbose_name="Описание")
    link = models.URLField(verbose_name="Ссылка")

    class Meta:
        verbose_name = "Анкетирование"
        verbose_name_plural = "Анкетирование"

    def __str__(self):
        return self.title
