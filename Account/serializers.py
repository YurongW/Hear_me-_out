from django.core.cache import cache
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException

from Account.models import Account
from HearMeOut.settings import TOKEN_EXIST_TIME


class CustomerDuplicateError(APIException):  # 用户重复错误
    status_code = 403
    default_detail = "CustomerDuplicate!"


class AccountRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="username")

    class Meta:
        model = Account
        fields = ["email", "password"]

    def create(self, validated_data):
        if Account.objects.filter(username=validated_data["username"]):
            raise CustomerDuplicateError
        user = Account.objects.create_user(**validated_data)  # **解包 将字典解包为key value的关键字参数
        Token.objects.create(user=user)
        token = Token.objects.get(user=user)
        token_cache = 'token_' + token.key
        cache.set(token_cache, token, TOKEN_EXIST_TIME)
        return {"token": token.key, "exist_time": TOKEN_EXIST_TIME}, user


class AccountAdminRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="username")

    class Meta:
        model = Account
        fields = ["email", "password"]

    def create(self, validated_data):
        if Account.objects.filter(username=validated_data["username"]):
            raise CustomerDuplicateError
        user = Account.objects.create_user(**validated_data)  # **解包 将字典解包为key value的关键字参数
        user.is_superuser = True
        user.save()
        Token.objects.create(user=user)
        token = Token.objects.get(user=user)
        token_cache = 'token_' + token.key
        cache.set(token_cache, token, TOKEN_EXIST_TIME)
        return {"token": token.key, "exist_time": TOKEN_EXIST_TIME}


class AccountLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="username")

    class Meta:
        model = Account
        fields = ["email", "password"]


class AccountInformationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="username")

    class Meta:
        model = Account
        fields = ["email", "avatar", "num_post", "num_like"]
