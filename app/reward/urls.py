from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reward import views

router = DefaultRouter()
router.register('rewards', views.RewardViewSet)

app_name = 'reward'

urlpatterns = [
    path('', include(router.urls)),
    path('rewards/<int:pk>/', views.GetRewardByIdView.as_view(), name='reward'),
]