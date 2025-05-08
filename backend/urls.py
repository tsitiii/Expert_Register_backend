from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import( UserViewSet, ExpertViewSet, LoginView, 
                    PasswordResetConfirmView, PasswordResetViewSet,
                    CVBuilderAPIView)
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import views as auth_view


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'experts', ExpertViewSet, basename='expert')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', PasswordResetViewSet.as_view(), name='api_password_reset'),
    path('password_reset/confirm/', PasswordResetConfirmView.as_view(), name='api_password_reset_confirm'),
    
    # path('api/v1/experts/register/', ExpertViewSet.as_view({'post': 'create'}), name='expert-register'),
    path('api/v1/experts/<int:expert_id>/build-cv/', CVBuilderAPIView.as_view({'post': 'create', 'put': 'update', 'patch': 'partial_update'}), name='build-cv'),
]


