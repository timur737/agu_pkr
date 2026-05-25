from modeltranslation.translator import register, TranslationOptions
from .models import (
    MainPage, MainPageSlider, News, Announcement, EducationProgram, EducationDirection,
    LibraryCategory, LibraryResource, Contact, ContactDepartment, SocialLink,
    AboutAcademy, Partner, AcademyCharter, AcademyCharterLink, AcademyHistory, AcademyLogo,
    OrganizationalStructure, Department, AcademicCouncil, AcademicCouncilFile,
    TradeUnion, TradeUnionLink, QualityManagement, QualityManagementFile, Bulletin, BulletinFile,
    BulletinLink, BudgetProgram, BudgetProgramLink, HonoraryProfessor, InternationalCooperation, InternationalCooperationLink,
    AcademicHonesty, LegalDocument, Schedule, Survey, SiteSettings
)


@register(MainPage)
class MainPageTranslationOptions(TranslationOptions):
    fields = ('about_title', 'about_description', 'about_link')


@register(MainPageSlider)
class MainPageSliderTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Announcement)
class AnnouncementTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(EducationProgram)
class EducationProgramTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(EducationDirection)
class EducationDirectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(LibraryCategory)
class LibraryCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(LibraryResource)
class LibraryResourceTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'address')


@register(ContactDepartment)
class ContactDepartmentTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(SocialLink)
class SocialLinkTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(AboutAcademy)
class AboutAcademyTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'additional_description',
        'block1_title', 'block1_description',
        'block2_title', 'block2_description',
        'mission_title', 'mission_description'
    )


@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(AcademyCharter)
class AcademyCharterTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(AcademyCharterLink)
class AcademyCharterLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(AcademyHistory)
class AcademyHistoryTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(AcademyLogo)
class AcademyLogoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(OrganizationalStructure)
class OrganizationalStructureTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(AcademicCouncil)
class AcademicCouncilTranslationOptions(TranslationOptions):
    fields = ('title', 'composition')


@register(AcademicCouncilFile)
class AcademicCouncilFileTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(TradeUnion)
class TradeUnionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(TradeUnionLink)
class TradeUnionLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(QualityManagement)
class QualityManagementTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(QualityManagementFile)
class QualityManagementFileTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Bulletin)
class BulletinTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(BulletinLink)
class BulletinLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(BulletinFile)
class BulletinFileTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(BudgetProgram)
class BudgetProgramTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'period')


@register(BudgetProgramLink)
class BudgetProgramLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(HonoraryProfessor)
class HonoraryProfessorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(InternationalCooperation)
class InternationalCooperationTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(InternationalCooperationLink)
class InternationalCooperationLinkTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(AcademicHonesty)
class AcademicHonestyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(LegalDocument)
class LegalDocumentTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Schedule)
class ScheduleTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('news_title', 'announcements_title', 'library_title')
