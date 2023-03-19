from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated


class CustomUserCreate(APIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CustomUserSerializer(user).data,
            "message": "User has been successfully registered"
        })


class CustomUserGet(APIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        return Response(CustomUserSerializer(request.user).data)


class BlacklistTokenUpdateView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "User has been successfully unauthorized"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f"There's error trying to logout: {str(e)}"},
                            status=status.HTTP_400_BAD_REQUEST)
