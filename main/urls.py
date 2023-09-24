from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, SectionViewSet, CollaborationViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'collaborations', CollaborationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]