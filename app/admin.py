from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from .models import (
    MainPage, News, NewsPhoto, Announcement, EducationProgram, EducationDirection,
    LibraryCategory, LibraryResource, Contact, ContactDepartment, SocialLink,
    AboutAcademy, Partner, AcademyCharter, AcademyHistory, AcademyLogo,
    OrganizationalStructure, Department, AcademicCouncil, AcademicCouncilFile,
    TradeUnion, QualityManagement, QualityManagementFile, Bulletin, BulletinFile,
    BudgetProgram, HonoraryProfessor, InternationalCooperation, InternationalCooperationLink,
    AcademicHonesty, LegalDocument, Schedule, Survey, SiteSettings
)


# Inline Admin Classes
class NewsPhotoInline(admin.TabularInline):
    model = NewsPhoto
    extra = 1
    fields = ('photo', 'is_active')


class ContactDepartmentInline(TranslationTabularInline):
    model = ContactDepartment
    extra = 1
    fields = ('department_type', 'title', 'description', 'is_active')


class DepartmentInline(TranslationTabularInline):
    model = Department
    extra = 1
    fields = ('name', 'description', 'order', 'is_active')


class AcademicCouncilFileInline(TranslationTabularInline):
    model = AcademicCouncilFile
    extra = 1
    fields = ('title', 'file', 'is_active')


class QualityManagementFileInline(TranslationTabularInline):
    model = QualityManagementFile
    extra = 1
    fields = ('title', 'file', 'is_active')


class BulletinFileInline(TranslationTabularInline):
    model = BulletinFile
    extra = 1
    fields = ('title', 'file', 'is_active')


class InternationalCooperationLinkInline(TranslationTabularInline):
    model = InternationalCooperationLink
    extra = 1
    fields = ('title', 'url', 'is_active')


# Main Admin Classes
@admin.register(MainPage)
class MainPageAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'about_title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('about_title', 'about_description', 'about_title_ru', 'about_title_ky', 'about_title_en', 'about_description_ru', 'about_description_ky', 'about_description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('main_photo', 'is_active')
        }),
        ('Об Академии', {
            'fields': ('about_title', 'about_description', 'about_link')
        }),
    )


@admin.register(News)
class NewsAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_pinned', 'is_event', 'date', 'is_active', 'created_at')
    list_filter = ('is_pinned', 'is_event', 'is_active', 'date')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en')
    prepopulated_fields = {'slug': ('title_ru',)}  # Используем русский язык для slug
    readonly_fields = ('date',)
    inlines = [NewsPhotoInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'description', 'photo', 'is_active')
        }),
        ('Настройки', {
            'fields': ('is_pinned', 'is_event', 'date')
        }),
    )


@admin.register(NewsPhoto)
class NewsPhotoAdmin(admin.ModelAdmin):
    list_display = ('news', 'photo', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('news__title',)


@admin.register(Announcement)
class AnnouncementAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_pinned', 'date', 'is_active', 'created_at')
    list_filter = ('is_pinned', 'is_active', 'date')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    readonly_fields = ('date',)
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Настройки', {
            'fields': ('is_pinned', 'date')
        }),
    )


@admin.register(EducationProgram)
class EducationProgramAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'program_type', 'order', 'is_active', 'created_at')
    list_filter = ('program_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'program_type', 'description', 'photo', 'is_active')
        }),
        ('Дополнительно', {
            'fields': ('link', 'order')
        }),
    )


@admin.register(EducationDirection)
class EducationDirectionAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'photo', 'link', 'is_active')
        }),
    )


@admin.register(LibraryCategory)
class LibraryCategoryAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'slug', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'title_ru', 'title_ky', 'title_en')
    prepopulated_fields = {'slug': ('title_ru',)}  # Используем русский язык для slug
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'order', 'is_active')
        }),
    )


@admin.register(LibraryResource)
class LibraryResourceAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('category', 'title', 'description', 'photo', 'is_active')
        }),
        ('Файлы и ссылки', {
            'fields': ('link', 'file')
        }),
    )


@admin.register(Contact)
class ContactAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'email', 'phone', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'email', 'phone')
    inlines = [ContactDepartmentInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'photo', 'is_active')
        }),
        ('Контакты', {
            'fields': ('email', 'phone', 'address')
        }),
        ('Карта', {
            'fields': ('map_url', 'map_embed')
        }),
    )


@admin.register(ContactDepartment)
class ContactDepartmentAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'contact', 'department_type', 'is_active', 'created_at')
    list_filter = ('department_type', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')


@admin.register(SocialLink)
class SocialLinkAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'url', 'show_in_header', 'show_in_footer', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'show_in_header', 'show_in_footer', 'created_at')
    search_fields = ('name', 'url')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'url', 'icon', 'show_in_header', 'show_in_footer', 'order', 'is_active')
        }),
    )


@admin.register(AboutAcademy)
class AboutAcademyAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'main_photo', 'description', 'photo', 'is_active')
        }),
        ('Дополнительное описание', {
            'fields': ('additional_description',)
        }),
        ('Блоки', {
            'fields': (
                'block1_title', 'block1_description',
                'block2_title', 'block2_description'
            )
        }),
        ('Миссия', {
            'fields': ('mission_title', 'mission_description')
        }),
    )


@admin.register(Partner)
class PartnerAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'photo', 'url', 'order', 'is_active')
        }),
    )


@admin.register(AcademyCharter)
class AcademyCharterAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'file', 'is_active')
        }),
    )


@admin.register(AcademyHistory)
class AcademyHistoryAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'file', 'is_active')
        }),
    )


@admin.register(AcademyLogo)
class AcademyLogoAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'logo', 'is_active')
        }),
    )


@admin.register(OrganizationalStructure)
class OrganizationalStructureAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    inlines = [DepartmentInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'scheme', 'description', 'is_active')
        }),
    )


@admin.register(Department)
class DepartmentAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'structure', 'order', 'is_active', 'created_at')
    list_filter = ('structure', 'is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(AcademicCouncil)
class AcademicCouncilAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'composition')
    inlines = [AcademicCouncilFileInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'composition', 'is_active')
        }),
    )


@admin.register(AcademicCouncilFile)
class AcademicCouncilFileAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'council', 'is_active', 'created_at')
    list_filter = ('council', 'is_active', 'created_at')
    search_fields = ('title', 'title_ru', 'title_ky', 'title_en')


@admin.register(TradeUnion)
class TradeUnionAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'is_active')
        }),
    )


@admin.register(QualityManagement)
class QualityManagementAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    inlines = [QualityManagementFileInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'is_active')
        }),
    )


@admin.register(QualityManagementFile)
class QualityManagementFileAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'quality', 'is_active', 'created_at')
    list_filter = ('quality', 'is_active', 'created_at')
    search_fields = ('title', 'title_ru', 'title_ky', 'title_en')


@admin.register(Bulletin)
class BulletinAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    inlines = [BulletinFileInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'is_active')
        }),
    )


@admin.register(BulletinFile)
class BulletinFileAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'bulletin', 'is_active', 'created_at')
    list_filter = ('bulletin', 'is_active', 'created_at')
    search_fields = ('title', 'title_ru', 'title_ky', 'title_en')


@admin.register(BudgetProgram)
class BudgetProgramAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'period', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'period')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'period', 'is_active')
        }),
    )


@admin.register(HonoraryProfessor)
class HonoraryProfessorAdmin(TabbedTranslationAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    fieldsets = (
        ('Основное', {
            'fields': ('name', 'photo', 'description', 'order', 'is_active')
        }),
    )


@admin.register(InternationalCooperation)
class InternationalCooperationAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    inlines = [InternationalCooperationLinkInline]
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'photo', 'is_active')
        }),
    )


@admin.register(InternationalCooperationLink)
class InternationalCooperationLinkAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'cooperation', 'url', 'is_active', 'created_at')
    list_filter = ('cooperation', 'is_active', 'created_at')
    search_fields = ('title', 'title_ru', 'title_ky', 'title_en', 'url')


@admin.register(AcademicHonesty)
class AcademicHonestyAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'photo', 'is_active')
        }),
    )


@admin.register(LegalDocument)
class LegalDocumentAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'document_type', 'is_active', 'created_at')
    list_filter = ('document_type', 'is_active', 'created_at')
    search_fields = ('title',)
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'document_type', 'file', 'is_active')
        }),
    )


@admin.register(Schedule)
class ScheduleAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'schedule_type', 'order', 'is_active', 'created_at')
    list_filter = ('schedule_type', 'is_active', 'created_at')
    search_fields = ('title',)
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'schedule_type', 'file', 'order', 'is_active')
        }),
    )


@admin.register(Survey)
class SurveyAdmin(TabbedTranslationAdmin):
    list_display = ('title', 'link', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description', 'title_ru', 'title_ky', 'title_en', 'description_ru', 'description_ky', 'description_en')
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'description', 'link', 'is_active')
        }),
    )

@admin.register(SiteSettings)
class SiteSettingsAdmin(TabbedTranslationAdmin):
    list_display = ('__str__', 'news_title', 'announcements_title', 'library_title', 'is_active')
    
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
