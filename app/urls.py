from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import AdminPageViewSet, PageBlockViewSet

router = DefaultRouter()
router.register(r'pages', AdminPageViewSet, basename='adminpage')
router.register(r'page-blocks', PageBlockViewSet, basename='pageblock')

urlpatterns = [
    path('', include(router.urls)),
]
