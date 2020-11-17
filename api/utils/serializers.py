from rest_framework import serializers
from ..models import Users,Adapter,Rule,Packages


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'user_name', ]


class AdapterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Adapter
        fields = "__all__"


class RuleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = "__all__"


class PackagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Packages
        fields = ['r_id','cap_date',]