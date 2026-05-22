from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MainPageViewSet, MainPageSliderViewSet, NewsViewSet, NewsPhotoViewSet,
    AnnouncementViewSet, EducationProgramViewSet, EducationDirectionViewSet,
    LibraryCategoryViewSet, LibraryResourceViewSet, ContactViewSet,
    ContactDepartmentViewSet, SocialLinkViewSet, AboutAcademyViewSet,
    PartnerViewSet, AcademyCharterViewSet, AcademyHistoryViewSet,
    AcademyLogoViewSet, OrganizationalStructureViewSet, DepartmentViewSet,
    AcademicCouncilViewSet, AcademicCouncilFileViewSet, TradeUnionViewSet,
    QualityManagementViewSet, QualityManagementFileViewSet, BulletinViewSet,
    BulletinFileViewSet, BudgetProgramViewSet, HonoraryProfessorViewSet,
    InternationalCooperationViewSet, InternationalCooperationLinkViewSet,
    AcademicHonestyViewSet, LegalDocumentViewSet, ScheduleViewSet, SurveyViewSet,
    SiteSettingsViewSet
)

router = DefaultRouter()
router.register(r'site-settings', SiteSettingsViewSet, basename='sitesettings')
router.register(r'main-page', MainPageViewSet, basename='mainpage')
router.register(r'mainpageslider', MainPageSliderViewSet, basename='mainpageslider')
router.register(r'news', NewsViewSet, basename='news')
router.register(r'news-photos', NewsPhotoViewSet, basename='newsphoto')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'education-programs', EducationProgramViewSet, basename='educationprogram')
router.register(r'education-directions', EducationDirectionViewSet, basename='educationdirection')
router.register(r'library-categories', LibraryCategoryViewSet, basename='librarycategory')
router.register(r'library-resources', LibraryResourceViewSet, basename='libraryresource')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'contact-departments', ContactDepartmentViewSet, basename='contactdepartment')
router.register(r'social-links', SocialLinkViewSet, basename='sociallink')
router.register(r'about-academy', AboutAcademyViewSet, basename='aboutacademy')
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'academy-charter', AcademyCharterViewSet, basename='academycharter')
router.register(r'academy-history', AcademyHistoryViewSet, basename='academyhistory')
router.register(r'academy-logo', AcademyLogoViewSet, basename='academylogo')
router.register(r'organizational-structure', OrganizationalStructureViewSet, basename='organizationalstructure')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'academic-council', AcademicCouncilViewSet, basename='academiccouncil')
router.register(r'academic-council-files', AcademicCouncilFileViewSet, basename='academiccouncilfile')
router.register(r'trade-union', TradeUnionViewSet, basename='tradeunion')
router.register(r'quality-management', QualityManagementViewSet, basename='qualitymanagement')
router.register(r'quality-management-files', QualityManagementFileViewSet, basename='qualitymanagementfile')
router.register(r'bulletin', BulletinViewSet, basename='bulletin')
router.register(r'bulletin-files', BulletinFileViewSet, basename='bulletinfile')
router.register(r'budget-programs', BudgetProgramViewSet, basename='budgetprogram')
router.register(r'honorary-professors', HonoraryProfessorViewSet, basename='honoraryprofessor')
router.register(r'international-cooperation', InternationalCooperationViewSet, basename='internationalcooperation')
router.register(r'international-cooperation-links', InternationalCooperationLinkViewSet, basename='internationalcooperationlink')
router.register(r'academic-honesty', AcademicHonestyViewSet, basename='academichonesty')
router.register(r'legal-documents', LegalDocumentViewSet, basename='legaldocument')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'surveys', SurveyViewSet, basename='survey')

urlpatterns = [
    path('', include(router.urls)),
]
