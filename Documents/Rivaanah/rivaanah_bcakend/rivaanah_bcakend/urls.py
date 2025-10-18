from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shop.views import ProductViewSet, CartItemViewSet, OrderViewSet, Stastics
from accounts.views import RegisterView, VerifyEmailView, PasswordResetView, PasswordResetRequestView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Rivaanah API",
        default_version='v1',
        description="E-commerce API for Rivaanah",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'cart', CartItemViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'stastics', Stastics, basename='stastics')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('api/reset-password/', PasswordResetView.as_view(), name='password-reset'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/me/', UserProfileView.as_view(), name='user-profile'), # GET or PATCH /api/users/me/
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)