from rest_framework.serializers import ModelSerializer, CharField

from .models import UserInternetIession


class AnalyticsSerializer(ModelSerializer):
    lastDayUsage = CharField()
    last7DayUsage = CharField()
    last30DayUsage = CharField()

    class Meta:
        model = UserInternetIession
        fields = ['username', 'lastDayUsage', 'last7DayUsage', 'last30DayUsage']

class LastHourUsage(ModelSerializer):
    time = CharField()
    upload = CharField()
    download = CharField()

    class Meta:
        model = UserInternetIession
        fields = ['time', 'upload', 'download']

class UserSearchSerializer(ModelSerializer):
    lastHourUsage = LastHourUsage()
    last6HourUsage = LastHourUsage()
    last24HourUsage = LastHourUsage()

    class Meta:
        model = UserInternetIession
        fields = ['username', 'lastHourUsage', "last6HourUsage", "last24HourUsage"]
