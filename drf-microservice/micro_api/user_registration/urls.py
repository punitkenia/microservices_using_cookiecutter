from django.urls import path
from .views import UserViewSet, UserRegistrationViewSet, UserToken, UserEmailVerify

create_user = UserRegistrationViewSet.as_view(
    {
        'post' : 'create',
    }
)

list_users = UserViewSet.as_view(
    {
        'get': 'list',
    }
)

user_details = UserViewSet.as_view(
    {
        'get': 'retrieve',
    },
)

user_update = UserViewSet.as_view(
    {
        'post': 'update',
    }
)

user_delete = UserViewSet.as_view(
    {
        'post': 'destroy',
    }
)

user_token = UserToken.as_view(
    {
        'get' : 'retrieve',
        'post': 'update',
    }
)

update_role = UserViewSet.as_view(
    {
        'post': 'update_role',
    }
)

verify_email = UserEmailVerify.as_view(
    {
        'get': 'verify_email',
    }
)

urlpatterns = [
    path('create_user/', create_user, name='create-user'),
    path('list_users/', list_users, name='list-user'),
    path('details/<int:pk>/', user_details, name='user-details'),
    path('update_user/', user_update, name='user-update'),
    path('delete_user/', user_delete, name='user-delete'),
    path('get_token/<int:pk>/', user_token, name='get-token'),
    path('reset_token/', user_token, name='reset-token'),
    path('update_role/<int:pk>', update_role, name='update-user-role'),
    path('verify_email/<int:user_id>', verify_email, name='verify-email'),
]
