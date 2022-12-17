from Internet.models import UserInternetIession
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from datetime import date, datetime

from .serializers import *

# Create your views here.


class LoadData(APIView):

    def post(self, request):
        f = open("user.txt", 'r')
        for i in f.readlines():
            i = i.strip().split(',')
            try:
                UserInternetIession.objects.get_or_create(
                    username=i[0], MAC=i[1], start_time=i[2], usage_time=i[3], upload=i[4], download=i[5])
            except:
                pass
        return Response(status=status.HTTP_201_CREATED)

def add_two_time(d1, d2):
    d = [0, 0, d1[2]+d2[2]]
    d = [0, d1[1]+d2[1] + d[2]//60, d[2]%60]
    return [d1[0]+d2[0] + d[1]//60, d[1]%60, d[2]]

class AnalyticsAPIView(generics.ListAPIView):
    serializer_class = AnalyticsSerializer

    def dispatch(self, request, *args, **kwargs):
        self.date = request.GET.get("date")
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        try:
            start_time = date(
                int(self.date[-4:]), int(self.date[2:4]), int(self.date[:2]))
            allData = UserInternetIession.objects.all()
            filterData, username = [], []
            for data in allData:
                if not data.username in username:
                    userData = allData.filter(username=data.username)
                    lDU, l7Du, l30DU = [0, 0, 0], [0, 0, 0], [0, 0, 0]
                    for user in userData:
                        usage_time = [user.usage_time.hour, user.usage_time.minute, user.usage_time.second]
                        d = user.start_time.date() - start_time
                        if d.days >= 0 and d.days <= 1:
                            lDU = add_two_time(lDU, usage_time)
                        if d.days >= 0 and d.days <= 7:
                            l7Du = add_two_time(l7Du, usage_time)
                        if d.days >= 0 and d.days <= 30:
                            l30DU = add_two_time(l30DU, usage_time)
                    username.append(data.username)
                    filterData.append({
                        "username": data.username,
                        "lastDayUsage": str(lDU[0])+"h"+str(lDU[1])+"m",
                        "last7DayUsage": str(l7Du[0])+"h"+str(l7Du[1])+"m",
                        "last30DayUsage": str(l30DU[0])+"h"+str(l30DU[1])+"m"
                    })
                
            return filterData
        except:
            raise NotFound({"ok": False, "error": {"message": 'invalid data'}})

class UserSearchAPIView(generics.ListAPIView):
    serializer_class = UserSearchSerializer

    def dispatch(self, request, *args, **kwargs):
        self.username = request.GET.get("username")
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        userData = UserInternetIession.objects.filter(username=self.username)
        if userData:
            filterData , lHU, l6HU, l24HU = [], [0, 0, 0], [0, 0, 0], [0, 0, 0]
            dHU, uHU, d6HU, u6HU, d24HU, u24HU = 0, 0, 0, 0, 0, 0
            for user in userData:
                usage_time = [user.usage_time.hour, user.usage_time.minute, user.usage_time.second]
        
                h = int(str(user.start_time.time())[:2]) - int(str(datetime.now().time())[:2])
                if h >= 0 and h <= 1:
                    lHU = add_two_time(lHU, usage_time)
                    dHU += user.download
                    uHU += user.upload
                if h >= 0 and h <= 6:
                    l6HU = add_two_time(l6HU, usage_time)
                    d6HU += user.download
                    u6HU += user.upload

            filterData.append({
                "username": self.username,
                "lastHourUsage": {
                    "time":str(lHU[0])+"h"+str(lHU[1])+"m",
                    "upload": str(uHU/1000)+"GB",
                    "download": str(dHU/1000)+"GB",
                },
                "last6HourUsage": {
                    "time":str(l6HU[0])+"h"+str(l6HU[1])+"m",
                    "upload": str(u6HU/1000)+"GB",
                    "download": str(d6HU/1000)+"GB",
                },
                "last24HourUsage": {
                    "time":str(l24HU[0])+"h"+str(l24HU[1])+"m",
                    "upload": str(u24HU/1000)+"GB",
                    "download": str(d24HU/1000)+"GB",
                }
            })

            return filterData
        else:
            raise NotFound({"ok": False, "error": {"message": 'user not found'}})