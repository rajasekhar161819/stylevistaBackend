from rest_framework import generics, status, permissions
from .serializers import RegisterSerializer, PasswordResetRequestSerializer, PasswordResetSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class VerifyEmailView(generics.GenericAPIView):
    def get(self, request, token):
        try:
            user = User.objects.get(username=token)
            user.is_verified = True
            user.save()
            return Response({'detail': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)

      
class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            reset_link = f"http://localhost:8000/api/reset-password/?username={user.username}"
            send_mail(
                'Reset your password',
                f'Click to reset your password: {reset_link}',
                'noreply@rivaanah.com',
                [user.email]
            )
            return Response({'detail': 'Password reset email sent'}, status=200)
        except User.DoesNotExist:
            return Response({'detail': 'No user with this email'}, status=404)

class PasswordResetView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        new_password = serializer.validated_data['new_password']
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful'})
        except User.DoesNotExist:
            return Response({'detail': 'Invalid username'}, status=404)
        

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



