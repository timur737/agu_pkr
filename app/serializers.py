from rest_framework import serializers
from .models import (
    MainPage, News, NewsPhoto, Announcement, EducationProgram, EducationDirection,
    LibraryCategory, LibraryResource, Contact, ContactDepartment, SocialLink,
    AboutAcademy, Partner, AcademyCharter, AcademyHistory, AcademyLogo,
    OrganizationalStructure, Department, AcademicCouncil, AcademicCouncilFile,
    TradeUnion, QualityManagement, QualityManagementFile, Bulletin, BulletinFile,
    BudgetProgram, HonoraryProfessor, InternationalCooperation, InternationalCooperationLink,
    AcademicHonesty, LegalDocument, Schedule, Survey
)


class NewsPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPhoto
        fields = ['id', 'photo', 'created_at']


class NewsSerializer(serializers.ModelSerializer):
    photos = NewsPhotoSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = [
            'id', 'title', 'slug', 'description', 'photo', 'photo_url',
            'is_pinned', 'is_event', 'date', 'photos', 'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'description', 'is_pinned', 'date',
            'created_at', 'updated_at'
        ]


class EducationProgramSerializer(serializers.ModelSerializer):
    program_type_display = serializers.CharField(source='get_program_type_display', read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = EducationProgram
        fields = [
            'id', 'title', 'program_type', 'program_type_display',
            'description', 'link', 'photo', 'photo_url', 'order',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class EducationDirectionSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = EducationDirection
        fields = [
            'id', 'title', 'description', 'link', 'photo', 'photo_url',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class LibraryResourceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title', read_only=True)
    photo_url = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LibraryResource
        fields = [
            'id', 'category', 'category_name', 'title', 'description',
            'photo', 'photo_url', 'link', 'file', 'file_url',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class LibraryCategorySerializer(serializers.ModelSerializer):
    resources = LibraryResourceSerializer(many=True, read_only=True)

    class Meta:
        model = LibraryCategory
        fields = ['id', 'title', 'slug', 'order', 'resources', 'created_at', 'updated_at']


class ContactDepartmentSerializer(serializers.ModelSerializer):
    department_type_display = serializers.CharField(source='get_department_type_display', read_only=True)

    class Meta:
        model = ContactDepartment
        fields = [
            'id', 'department_type', 'department_type_display',
            'title', 'description', 'created_at', 'updated_at'
        ]


class ContactSerializer(serializers.ModelSerializer):
    departments = ContactDepartmentSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = [
            'id', 'title', 'description', 'photo', 'photo_url',
            'email', 'phone', 'address', 'map_url', 'map_embed',
            'departments', 'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['id', 'name', 'url', 'icon', 'order', 'created_at', 'updated_at']


class MainPageSerializer(serializers.ModelSerializer):
    main_photo_url = serializers.SerializerMethodField()
    news = serializers.SerializerMethodField()
    education_programs = serializers.SerializerMethodField()

    class Meta:
        model = MainPage
        fields = [
            'id', 'main_photo', 'main_photo_url', 'about_title',
            'about_description', 'about_link', 'news', 'education_programs',
            'created_at', 'updated_at'
        ]

    def get_main_photo_url(self, obj):
        if obj.main_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_photo.url)
            return obj.main_photo.url
        return None

    def get_news(self, obj):
        news = News.objects.filter(is_active=True, is_event=False)[:4]
        return NewsSerializer(news, many=True, context=self.context).data

    def get_education_programs(self, obj):
        programs = EducationProgram.objects.filter(is_active=True)[:5]
        return EducationProgramSerializer(programs, many=True, context=self.context).data


class PartnerSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Partner
        fields = [
            'id', 'name', 'photo', 'photo_url', 'url', 'order',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class AboutAcademySerializer(serializers.ModelSerializer):
    main_photo_url = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    partners = serializers.SerializerMethodField()

    class Meta:
        model = AboutAcademy
        fields = [
            'id', 'title', 'main_photo', 'main_photo_url', 'description',
            'photo', 'photo_url', 'additional_description',
            'block1_title', 'block1_description',
            'block2_title', 'block2_description',
            'mission_title', 'mission_description',
            'partners', 'created_at', 'updated_at'
        ]

    def get_main_photo_url(self, obj):
        if obj.main_photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.main_photo.url)
            return obj.main_photo.url
        return None

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

    def get_partners(self, obj):
        partners = Partner.objects.filter(is_active=True)
        return PartnerSerializer(partners, many=True, context=self.context).data


class AcademyCharterSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AcademyCharter
        fields = ['id', 'title', 'description', 'file', 'file_url', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class AcademyHistorySerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AcademyHistory
        fields = ['id', 'title', 'description', 'file', 'file_url', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class AcademyLogoSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()

    class Meta:
        model = AcademyLogo
        fields = ['id', 'title', 'description', 'logo', 'logo_url', 'created_at', 'updated_at']

    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'order', 'created_at', 'updated_at']


class OrganizationalStructureSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)
    scheme_url = serializers.SerializerMethodField()

    class Meta:
        model = OrganizationalStructure
        fields = [
            'id', 'title', 'scheme', 'scheme_url', 'description',
            'departments', 'created_at', 'updated_at'
        ]

    def get_scheme_url(self, obj):
        if obj.scheme:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.scheme.url)
            return obj.scheme.url
        return None


class AcademicCouncilFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AcademicCouncilFile
        fields = ['id', 'title', 'file', 'file_url', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class AcademicCouncilSerializer(serializers.ModelSerializer):
    files = AcademicCouncilFileSerializer(many=True, read_only=True)

    class Meta:
        model = AcademicCouncil
        fields = ['id', 'title', 'composition', 'files', 'created_at', 'updated_at']


class TradeUnionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeUnion
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']


class QualityManagementFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = QualityManagementFile
        fields = ['id', 'title', 'file', 'file_url', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class QualityManagementSerializer(serializers.ModelSerializer):
    files = QualityManagementFileSerializer(many=True, read_only=True)

    class Meta:
        model = QualityManagement
        fields = ['id', 'title', 'files', 'created_at', 'updated_at']


class BulletinFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = BulletinFile
        fields = ['id', 'title', 'file', 'file_url', 'created_at', 'updated_at']

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class BulletinSerializer(serializers.ModelSerializer):
    files = BulletinFileSerializer(many=True, read_only=True)

    class Meta:
        model = Bulletin
        fields = ['id', 'title', 'description', 'files', 'created_at', 'updated_at']


class BudgetProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetProgram
        fields = ['id', 'title', 'description', 'period', 'created_at', 'updated_at']


class HonoraryProfessorSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = HonoraryProfessor
        fields = [
            'id', 'name', 'photo', 'photo_url', 'description', 'order',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class InternationalCooperationLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalCooperationLink
        fields = ['id', 'title', 'url', 'created_at', 'updated_at']


class InternationalCooperationSerializer(serializers.ModelSerializer):
    links = InternationalCooperationLinkSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = InternationalCooperation
        fields = [
            'id', 'title', 'description', 'photo', 'photo_url', 'links',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class AcademicHonestySerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = AcademicHonesty
        fields = [
            'id', 'title', 'description', 'photo', 'photo_url',
            'created_at', 'updated_at'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class LegalDocumentSerializer(serializers.ModelSerializer):
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LegalDocument
        fields = [
            'id', 'title', 'document_type', 'document_type_display',
            'file', 'file_url', 'created_at', 'updated_at'
        ]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class ScheduleSerializer(serializers.ModelSerializer):
    schedule_type_display = serializers.CharField(source='get_schedule_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = [
            'id', 'title', 'schedule_type', 'schedule_type_display',
            'file', 'file_url', 'order', 'created_at', 'updated_at'
        ]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'link', 'created_at', 'updated_at']

