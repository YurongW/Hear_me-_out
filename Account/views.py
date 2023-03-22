from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Account.auth import ExpiringTokenAuthentication, CsrfExemptSessionAuthentication
from Account.models import Account
from Account.serializers import AccountRegisterSerializer, AccountLoginSerializer, AccountInformationSerializer, \
    AccountAdminRegisterSerializer
from HearMeOut.settings import TOKEN_EXIST_TIME


# Create your views here.

class Register(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny, ]

    def post(self, request):
        register = AccountRegisterSerializer(data=request.data)
        if register.is_valid():
            info, user = register.save()
            login(request, user)
            return Response({"status": "success", "token_information": info})
        else:
            return Response(register.errors)
        # print(customer_password, customer_name)


class Login(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [ExpiringTokenAuthentication]
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny, ]

    def post(self, request):
        log = AccountLoginSerializer(data=request.data)
        if log.is_valid():
            user = authenticate(**log.validated_data)
            if not user:
                return Response({"status": "error", "detail": "Wrong username or password"})
            else:
                try:
                    token = Token.objects.get(user=user)
                    cache.delete('token_' + token.key)
                    token.delete()
                except ObjectDoesNotExist:
                    pass
                login(request, user)
                Token.objects.create(user=user)
                token = Token.objects.get(user=user)
                token_cache = 'token_' + token.key
                cache.set(token_cache, token, TOKEN_EXIST_TIME)
                return Response(
                    {"status": "success", "token_information": {"token": token.key, "exist_time": TOKEN_EXIST_TIME},
                     "isAdmin": request.user.is_superuser})
        else:
            return Response({"status": "error", "detail": log.errors})


class Logout(APIView):

    def get(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        cache.delete('token_' + token.key)
        token.delete()
        logout(request)
        return Response({"status": "success", "details": "logout success"})


class DeleteCustomer(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token = Token.objects.get(user=user)
        cache.delete('token_' + token.key)
        token.delete()
        user.is_deleted = True
        user.is_active = False
        user.save()
        return Response({"status": "success", "details": "delete success"})


class CustomerInformation(APIView):

    def get(self, request):
        user = request.user
        return Response(AccountInformationSerializer(user).data)


class CreateAdmin(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        register = AccountAdminRegisterSerializer(data=request.data)
        if register.is_valid():
            info = register.save()
            return Response({"status": "success", "token_information": info})
        else:
            return Response(register.errors)


class HistoryPost(APIView):

    def get(self, request):
        user = request.user
        comment = Account.objects.get(id=user.id).customers_comment.all()
        res_lst = []
        for c in comment:
            res_lst.append({
                "topic_name": c.topic_id.name,
                "topic_uuid": c.topic_id.uuid,
                "comment_uuid": c.uuid,
                "num_like": c.num_like,
                "content": c.content
            })
        topic = Account.objects.get(id=user.id).customers.all()
        for t in topic:
            res_lst.append({
                "topic_name": t.name,
                "topic_uuid": t.uuid,
                "comment_uuid": t.uuid,
                "num_like": t.like,
                "content": t.content
            })
        return Response({"status": "success", "detail": res_lst})
