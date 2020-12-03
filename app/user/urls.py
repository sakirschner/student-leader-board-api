from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views


router = DefaultRouter()
router.register('user', views.UserViewSet)

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', views.GetUsersView.as_view(), name ='all'),
    path('<int:pk>/', views.GetUserByIdView.as_view(), name='user'),
    path('', include(router.urls)),
]