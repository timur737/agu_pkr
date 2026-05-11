from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import LanguageMixin
from .models import (
    MainPage, News, NewsPhoto, Announcement, EducationProgram, EducationDirection,
    LibraryCategory, LibraryResource, Contact, ContactDepartment, SocialLink,
    AboutAcademy, Partner, AcademyCharter, AcademyHistory, AcademyLogo,
    OrganizationalStructure, Department, AcademicCouncil, AcademicCouncilFile,
    TradeUnion, QualityManagement, QualityManagementFile, Bulletin, BulletinFile,
    BudgetProgram, HonoraryProfessor, InternationalCooperation, InternationalCooperationLink,
    AcademicHonesty, LegalDocument, Schedule, Survey, SiteSettings
)
from .serializers import (
    MainPageSerializer, NewsSerializer, NewsPhotoSerializer, AnnouncementSerializer,
    EducationProgramSerializer, EducationDirectionSerializer,
    LibraryCategorySerializer, LibraryResourceSerializer, ContactSerializer,
    ContactDepartmentSerializer, SocialLinkSerializer, AboutAcademySerializer,
    PartnerSerializer, AcademyCharterSerializer, AcademyHistorySerializer,
    AcademyLogoSerializer, OrganizationalStructureSerializer, DepartmentSerializer,
    AcademicCouncilSerializer, AcademicCouncilFileSerializer, TradeUnionSerializer,
    QualityManagementSerializer, QualityManagementFileSerializer, BulletinSerializer,
    BulletinFileSerializer, BudgetProgramSerializer, HonoraryProfessorSerializer,
    InternationalCooperationSerializer, InternationalCooperationLinkSerializer,
    AcademicHonestySerializer, LegalDocumentSerializer, ScheduleSerializer, SurveySerializer,
    SiteSettingsSerializer
)


class MainPageViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = MainPage.objects.filter(is_active=True)
    serializer_class = MainPageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = []

    def get_queryset(self):
        return MainPage.objects.filter(is_active=True)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class NewsViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = News.objects.filter(is_active=True)
    serializer_class = NewsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_pinned', 'is_event']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'created_at']
    ordering = ['-date']

    def get_queryset(self):
        queryset = News.objects.filter(is_active=True)
        is_event = self.request.query_params.get('is_event', None)
        if is_event is not None:
            queryset = queryset.filter(is_event=is_event.lower() == 'true')
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=False, methods=['get'])
    def events(self, request):
        """Get all events"""
        events = self.get_queryset().filter(is_event=True)
        serializer = self.get_serializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Get pinned news"""
        pinned = self.get_queryset().filter(is_pinned=True)
        serializer = self.get_serializer(pinned, many=True)
        return Response(serializer.data)


class NewsPhotoViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = NewsPhoto.objects.filter(is_active=True)
    serializer_class = NewsPhotoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['news']


class AnnouncementViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_pinned']
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'created_at']
    ordering = ['-is_pinned', '-date']

    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """Get pinned announcements"""
        pinned = self.get_queryset().filter(is_pinned=True)
        serializer = self.get_serializer(pinned, many=True)
        return Response(serializer.data)


class EducationProgramViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = EducationProgram.objects.filter(is_active=True)
    serializer_class = EducationProgramSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['program_type']
    search_fields = ['title', 'description']
    ordering_fields = ['order', 'title']
    ordering = ['order', 'title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class EducationDirectionViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = EducationDirection.objects.filter(is_active=True)
    serializer_class = EducationDirectionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LibraryCategoryViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = LibraryCategory.objects.filter(is_active=True)
    serializer_class = LibraryCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['order', 'title']
    ordering = ['order', 'title']


class LibraryResourceViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = LibraryResource.objects.filter(is_active=True)
    serializer_class = LibraryResourceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ContactViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Contact.objects.filter(is_active=True)
    serializer_class = ContactSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ContactDepartmentViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = ContactDepartment.objects.filter(is_active=True)
    serializer_class = ContactDepartmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact', 'department_type']


class SocialLinkViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = SocialLink.objects.filter(is_active=True)
    serializer_class = SocialLinkSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']


class AboutAcademyViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AboutAcademy.objects.filter(is_active=True)
    serializer_class = AboutAcademySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PartnerViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AcademyCharterViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AcademyCharter.objects.filter(is_active=True)
    serializer_class = AcademyCharterSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AcademyHistoryViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AcademyHistory.objects.filter(is_active=True)
    serializer_class = AcademyHistorySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class AcademyLogoViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AcademyLogo.objects.filter(is_active=True)
    serializer_class = AcademyLogoSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class OrganizationalStructureViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = OrganizationalStructure.objects.filter(is_active=True)
    serializer_class = OrganizationalStructureSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class DepartmentViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Department.objects.filter(is_active=True)
    serializer_class = DepartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['structure']
    ordering_fields = ['order']
    ordering = ['order']


class AcademicCouncilViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AcademicCouncil.objects.filter(is_active=True)
    serializer_class = AcademicCouncilSerializer


class AcademicCouncilFileViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AcademicCouncilFile.objects.filter(is_active=True)
    serializer_class = AcademicCouncilFileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['council']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class TradeUnionViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = TradeUnion.objects.filter(is_active=True)
    serializer_class = TradeUnionSerializer


class QualityManagementViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = QualityManagement.objects.filter(is_active=True)
    serializer_class = QualityManagementSerializer


class QualityManagementFileViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = QualityManagementFile.objects.filter(is_active=True)
    serializer_class = QualityManagementFileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['quality']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class BulletinViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Bulletin.objects.filter(is_active=True)
    serializer_class = BulletinSerializer


class BulletinFileViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = BulletinFile.objects.filter(is_active=True)
    serializer_class = BulletinFileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bulletin']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class BudgetProgramViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = BudgetProgram.objects.filter(is_active=True)
    serializer_class = BudgetProgramSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description', 'period']


class HonoraryProfessorViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = HonoraryProfessor.objects.filter(is_active=True)
    serializer_class = HonoraryProfessorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['order']
    ordering = ['order']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class InternationalCooperationViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = InternationalCooperation.objects.filter(is_active=True)
    serializer_class = InternationalCooperationSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class InternationalCooperationLinkViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = InternationalCooperationLink.objects.filter(is_active=True)
    serializer_class = InternationalCooperationLinkSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cooperation']


class AcademicHonestyViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = AcademicHonesty.objects.filter(is_active=True)
    serializer_class = AcademicHonestySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LegalDocumentViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = LegalDocument.objects.filter(is_active=True)
    serializer_class = LegalDocumentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['document_type']
    search_fields = ['title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ScheduleViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Schedule.objects.filter(is_active=True)
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['schedule_type']
    ordering_fields = ['order']
    ordering = ['order']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class SurveyViewSet(LanguageMixin, viewsets.ModelViewSet):
    queryset = Survey.objects.filter(is_active=True)
    serializer_class = SurveySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']

class SiteSettingsViewSet(LanguageMixin, viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for SiteSettings. Provides only read access to the frontend.
    Returns a single object or empty list.
    """
    queryset = SiteSettings.objects.filter(is_active=True)
    serializer_class = SiteSettingsSerializer
