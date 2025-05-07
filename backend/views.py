from rest_framework import viewsets
from .models import User, Expert
from .serializers import (UserSerializer, ExpertSerializer,
                            CVBuilderSerializer, LoginSerializer,
                            PasswordResetSerializer, PasswordResetConfirmSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import create_jwt_pair_user
from rest_framework.generics import GenericAPIView
from django.core.mail import send_mail
from django.conf import settings

def send_password_reset_email(email, url):
        subject = "Password Reset Request"
        message = f"Please click the following link to reset your password: {url}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )


class PasswordResetViewSet(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer
    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return Response(
                {"Detail": "user with this email does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_RESET_URL}?uid={uid}&token={token}"
        send_password_reset_email(user.email, reset_url)
        
        return Response({"detail": "Password reset email has been sent."},
                    status=status.HTTP_200_OK)

class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, serializer.validated_data['token']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Password has been reset successfully."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid reset link."},
                            status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = create_jwt_pair_user(user)
            return Response({
                "message": "Login successful",
                "tokens": tokens
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class CVBuilderAPIView(viewsets.ModelViewSet):
    serializer_class = CVBuilderSerializer
    def post(self, request, expert_id):
        try:
            expert = Expert.objects.get(id=expert_id)
            serializer = CVBuilderSerializer(
                data=request.data,
                context={'expert': expert}
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "status": "success",
                    "expert_id": expert.id,
                    "sections_updated": list(request.data.keys())
                })
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Expert.DoesNotExist:
            return Response(
                {"error": "Expert not found"},
                status=status.HTTP_404_NOT_FOUND
            )
    # def put(self):
    #     pass