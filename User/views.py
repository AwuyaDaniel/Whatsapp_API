from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from .serializers import *
from rest_framework import status
from .utils import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

User = get_user_model()


class UserInfoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    # serializer_class = SingleUserSerializer
    def get(self, request):
        try:
            authentication = request.headers.get('Authorization', '').split()
            token_obj = Token.objects.get(key=authentication[1])
            user = token_obj.user
            data = {
                'username': user.username,
                'email': user.email,
                'is_active': user.is_active,
                'first_name': user.first_name,
                'middle_name': user.middle_name,
                'last_name': user.last_name,
            }
            return Response(data)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'})


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        try:
            args = check_request_arguments(request, ['password_2'])

            if not request.data.get('password_2'):
                return Response({'error': 'password_2 field is required'},
                                status.HTTP_400_BAD_REQUEST)
            elif not check_password(request, "password", 'password_2'):
                return Response({'error': 'Password does not Match'},
                                status.HTTP_400_BAD_REQUEST)
            else:
                return self.create(request, *args, **kwargs)
        except Exception as E:
            response = {
                'status': 'success',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)


class PasswordUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        try:
            if not request.data.get('password_2'):
                return Response({'error': 'password_2 field is required'},
                                status.HTTP_400_BAD_REQUEST)
            serializer = PasswordUpdateSerializer(
                data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'detail': 'Password updated successfully'})
        except Exception as E:
            response = {
                'status': 'success',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = PasswordUpdateSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Check old password
                if not request.data.get('password_2'):
                    return Response({'error': 'password_2 field is required'},
                                    status.HTTP_400_BAD_REQUEST)
                if request.data.get('password_2') != request.data.get('new_password'):
                    return Response({'error': 'Passwords does not match'},
                                    status.HTTP_400_BAD_REQUEST)
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            response = {
                'status': 'success',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)


class UpdateUserDetails(generics.UpdateAPIView):
    """
    An endpoint for changing User Details.
    """
    serializer_class = UpdateUserSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    parser_classes = [MultiPartParser]

    def put(self, request):
        try:
            user = request.user
            serializer = UpdateUserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=400)
        except Exception as E:
            response = {
                'status': 'success',
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Error Processing Data',
            }

            return Response(response)
