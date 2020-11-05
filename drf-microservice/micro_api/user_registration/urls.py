from django.urls import path
from .views import UserViewSet, UserRegistrationViewSet

create_user = UserRegistrationViewSet.as_view(
    {
        'post' : 'create',
    }
)

user_details = UserViewSet.as_view(
    {
        'get': 'retrieve',
        'post': 'update',
        'delete': 'destroy',
    },
)

urlpatterns = [
    path('create_user/', create_user, name='create-user'),
    path('details/<int:pk>', user_details, name='user-details'),
]