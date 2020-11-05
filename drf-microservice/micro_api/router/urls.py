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
        'post': 'update',
        'delete': 'destroy',
     },
)

urlpatterns = [
    path('routers/', router_list, name='router-list'),
    path('router/<int:pk>/', router_detail, name='router-detail'),
]