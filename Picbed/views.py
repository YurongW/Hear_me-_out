import hashlib

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from Account.auth import ExpiringTokenAuthentication
from Picbed.models import PIC


def readmd5(fileinstance):
    md5 = hashlib.md5(fileinstance.file.read()).hexdigest()
    return md5


class UploadImg(APIView):
    # authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request):
        md5 = readmd5(request.data.get('pic'))
        try:
            pic = PIC.objects.get(md5=md5)
            return Response({"code": 200, "msg": pic.pic.url})
        except:
            pic = PIC.objects.create(pic=request.data.get('pic'), md5=md5)
            return Response({"code": 200, "msg": pic.pic.url})
