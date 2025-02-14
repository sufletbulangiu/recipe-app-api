"""
URL mappings for the receipe app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.ReceipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]