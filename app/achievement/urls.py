from django.urls import path, include
from rest_framework.routers import DefaultRouter

from achievement import views

router = DefaultRouter()
router.register('achievements', views.AchievementViewSet)
router.register('studentachievements', views.StudentAchievementViewSet)

app_name = 'achievement'

urlpatterns = [
    path('', include(router.urls)),
    path('achievements/<int:pk>/', views.GetAchievementByIdView.as_view(), name='achievement'),
    path('studentachievements/<int:pk>/', views.GetStudentAchievementByIdView.as_view(), name='studentachievement')
]