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
router.register('tags', views.TagViewSet)
router.register('ingridients', views.IngridientViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]