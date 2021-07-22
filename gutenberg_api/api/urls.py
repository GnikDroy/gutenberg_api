from django.urls import path, include

from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('book', views.BookViewSet)
router.register('bookshelf', views.BookshelfViewSet)
router.register('agent_type', views.AgentTypeViewSet)
router.register('person', views.PersonViewSet)
router.register('resource', views.ResourceViewSet)
router.register('agent', views.AgentViewSet)
router.register('language', views.LanguageViewSet)
router.register('subject', views.SubjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
]