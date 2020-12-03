from django.urls import path, include
from rest_framework.routers import DefaultRouter

from achievement import views

router = DefaultRouter()
router.register('achievement', views.AchievementViewSet)

app_name = 'achievement'

urlpatterns = [
    path('achievement/<int:pk>/', views.GetAchievementByIdView.as_view(), name='achievement'),
    path('', include(router.urls)),
]