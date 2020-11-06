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

update_role = UserViewSet.as_view(
    {
        'post': 'update_role',
    }
)

profile_history = UserViewSet.as_view(
    {
        'get': 'profile_history',
    }
)

urlpatterns = [
    path('create_user/', create_user, name='create-user'),
    path('details/<int:pk>', user_details, name='user-details'),
    path('update_role/<int:pk>', update_role, name='update-user-role'),
    path('profile_history/<int:user_id>', profile_history, name='user-profile-history'),
]