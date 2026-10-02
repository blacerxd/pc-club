from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/bookings/', include('bookings.urls')),
    path('api/v1/catalog/', include('catalog.urls')),
    path('api/v1/clubs/', include('clubs.urls')),
    path('api/v1/core/', include('core.urls')),
    path('api/v1/loyalty/', include('loyalty.urls')),
    path('api/v1/menu/', include('menu.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/promotions/', include('promotions.urls')),
    path('api/v1/tournaments/', include('tournaments.urls')),
]
