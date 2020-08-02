from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .cart import urls as cart_urls
from .order import urls as order_urls
from .users.views import UserViewSet, UserCreateViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="REST API",
        default_version='v1',
        description="E-commerce Sample",
        contact=openapi.Contact(email="suneet@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(router.urls)),
    path('api/v1/cart/', include(cart_urls)),
    path('api/v1/orders/', include(order_urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
