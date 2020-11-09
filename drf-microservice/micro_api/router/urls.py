from django.urls import path
from .views import RouterViewSet

router_list = RouterViewSet.as_view(
    {
        'get': 'list',
        'post': 'create',
     },
)

router_detail = RouterViewSet.as_view(
    {
        'get': 'retrieve',
     },
)

router_update = RouterViewSet.as_view(
    {
        'post': 'update',
     },
)

router_delete = RouterViewSet.as_view(
    {
        'post': 'destroy',
    }
)

urlpatterns = [
    path('routers/', router_list, name='router-list'),
    path('get_router/<int:pk>/', router_detail, name='router-detail'),
    path('update_router/', router_update, name='router-update'),
    path('remove_router/', router_delete, name='remove-router'),
]