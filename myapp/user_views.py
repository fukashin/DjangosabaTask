from .serializers import  CustomUserSerializer,SignInSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)
# ユーザー登録のビュー関数
@api_view(['POST'])
def signup(request):
    logger.info(f"Request data: {request.data}")  # リクエストデータをログ出力

    serializer = CustomUserSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        logger.info(f"After creating user: user={user}")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    else:
        logger.info(f"Serializer errors: {serializer.errors}")  # エラーメッセージをログ出力
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ユーザーログインのビュー関数
@api_view(['POST'])
def signin(request):
    # リクエストデータをシリアライザーに渡す
    serializer = SignInSerializer(data=request.data)

    # シリアライザーが有効な場合
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # ユーザー名とパスワードを使ってユーザーを認証
        user = authenticate(request, username=username, password=password)

        # 認証に成功した場合
        if user is not None:
            # ユーザーに関連付けられたトークンを取得（存在しない場合は作成）
            token, _ = Token.objects.get_or_create(user=user)
            # トークンをレスポンスとして返す
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            # 認証に失敗した場合はエラーを返す
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    user_info = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }
    return Response(user_info)
