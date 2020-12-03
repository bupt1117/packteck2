from django.shortcuts import render
from django.http import JsonResponse, HttpResponse,FileResponse
from django.contrib.auth import authenticate
from .models import Users,Packages,Rule,Adapter
from rest_framework.views import APIView
from rest_framework.response import Response

from .extensions.auth import JwtQueryParamsAuthentication,JwtAdminQueryParamsAuthentication
from .utils.jwt_auth import create_token
from .utils.jwt_auth import idmatch,token_encode
from .utils.serializers import UserSerializers,AdapterSerializers,RuleSerializers,PackagesSerializers
import string,random
import logging
import csv
import json
import datetime
from rest_framework.parsers import MultiPartParser

# Create your views here.

# 用户部分
# post:'username','password'
class Login(APIView):
    authentication_classes=[]
    def post(self,request,*args,**kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')
        user_object = Users.objects.filter(user_name=user,user_pwd=pwd).first()
        if not user_object:
            return Response({'code': 1000, 'error': '用户名或密码错误'})
        token = create_token({'user_id':user_object.id,'username':user_object.user_name})
        return Response({'code': 1001, 'token': token})


# post new 'password'
class Changepwd(APIView):

    def post(self,request,*args,**kwargs):
        pwd = request.data.get('password')
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        token_user = token_encode(token)
        uid = token_user["user_id"]
        user_object = Users.objects.get(id=uid)
        user_object.user_pwd = pwd
        user_object.save()
        return Response({'code': 1001})

# return Users
class Usermanage(APIView):

    def get(self,request,*args,**kwargs):
        authentication_classes = [JwtAdminQueryParamsAuthentication, ]   # 管理员身份认证
        user_list = Users.objects.filter(user_type=1)
        sertializer_user = UserSerializers(user_list, many=True)  # 序列化
        return Response(sertializer_user.data)


# post 'username'
# return 'pwd'
class Adduser(APIView):

    def post(self,request,*args,**kwargs):
        authentication_classes = [JwtAdminQueryParamsAuthentication,]
        username = request.data.get('username')
        default_pwd = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user = Users(user_name=username, user_pwd=default_pwd, user_type=1)
        user.save()
        return Response({'code': 1001,'pwd': default_pwd, })


# get 需要重置的'uid'
# return 'pwd'
class Resetpwd(APIView):

    def get(self, request, *args, **kwargs):
        authentication_classes = [JwtAdminQueryParamsAuthentication, ]
        uid = request.GET.get('uid')
        user_object = Users.objects.get(id=uid)
        new_pwd = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        user_object.user_pwd = new_pwd
        user_object.save()
        return Response({'code': 1001,'pwd': new_pwd, })


# 主页展示信息部分
# 获取网卡流量信息
# return Adapters
class Adaptersinfo(APIView):

    def get(self,request,*args,**kwargs):
        adapters_objects = Adapter.objects.all()
        adapters_info = AdapterSerializers(adapters_objects, many=True)
        return Response(adapters_info.data)


# 获取规则列表
class Ruleinfo(APIView):

    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        token_user = token_encode(token)
        uid = token_user["user_id"]
        user_object = Users.objects.get(id=uid)
        rules = user_object.rule_set.all()
        rules_info = RuleSerializers(rules, many=True)
        return Response(rules_info.data)


# 获取规则数目
class Rulenum(APIView):

    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        token_user = token_encode(token)
        uid = token_user["user_id"]
        user_object = Users.objects.get(id=uid)
        count = user_object.rule_set.count()
        return Response({'code':'1001','count':count})

# 添加规则
# post newrule（json）
class Addrule(APIView):
    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        token_user = token_encode(token)
        uid = token_user["user_id"]
        ruleinfo = request.data
        ruleinfo["uid"]=uid
        rule = RuleSerializers(data=ruleinfo)
        if rule.is_valid(raise_exception=True):
            rule.save()
        else:
            print(rule.errors['name'][0])
            return Response({'code': 1004, 'error': "添加错误"})
        return Response({'code': 1001})


# 修改规则
# get rule_id,rule修改部分的json
# 删除规则直接改is_del位即可
class ChangeRule(APIView):

    def post(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        token_user = token_encode(token)
        uid = token_user["user_id"]
        rule_id = request.GET.get('rule_id')
        ruleobject = Rule.objects.get(pk=rule_id)
        if ruleobject.uid.pk != uid:
            return Response({'code': 1003, 'error': "权限错误"})
        else:
            rerule = request.data
            # logging.debug(type(rerule))
            # 似乎外键不能直接updata，必须要手动继承一下
            rerule["uid"] = uid
            rerule["r_ofadapter"] = ruleobject.r_ofadapter.pk
            if('r_name' in rerule):
                pass
            else:
                rerule["r_name"]= ruleobject.r_name
            rule = RuleSerializers(ruleobject,data=rerule)
            if rule.is_valid(raise_exception=True):
                rule.save()
            else:
                print(rule.errors['name'][0])
                return Response({'code': 1004, 'error': "添加错误"})
        return Response({'code': 1001})


# 处理参考https://www.jianshu.com/p/82cb876bb426
# csv上传 files
class Addrulebycsv(APIView):
    parser_classes = [MultiPartParser, ]

    def post(self,request,format=None):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        token_user = token_encode(token)
        uid = token_user["user_id"]
        file_obj = request.FILES["file"]
        filename = "upload.csv"
        with open(filename, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        # 因为导入的csv中没有uid这一列所以要处理下
        with open(filename, 'r',encoding="utf-8") as csvfile:
            # 每一行都按照字典存储
            reader = csv.DictReader(csvfile)
            column = []
            for row in reader:
                row['uid']=uid
                rule = RuleSerializers(data=row)
                if rule.is_valid(raise_exception=True):
                    rule.save()
                else:
                    print(rule.errors['name'][0])
                    return Response({'code': 1004, 'error': "添加错误"})
                column.append(row)
        # logging.debug(column)

        return Response({'code': 1001})


# 下载批量上传规则模板
class Exampledownload(APIView):

    def get(self,request,*args,**kwargs):
        file = open('static/files/addrule.csv','rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="example.csv"'
        return response


# 总命中数和今日命中数
# get r_id
# return count_total,count_today
class Shot(APIView):

    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        rule_id = request.GET.get('r_id')
        ruleobject = Rule.objects.get(pk=rule_id)
        if(idmatch(token, rule_id)):
            count_total = ruleobject.packages_set.count()
            # 今日0点
            date_zero = datetime.datetime.now().replace(year=datetime.datetime.now().year,
                                                        month=datetime.datetime.now().month,
                                                        day=datetime.datetime.now().day,
                                                        hour=0, minute=0, second=0)
            count_today = Packages.objects.filter(r_id=rule_id, cap_date__gte=date_zero).count()
            return Response({'code': 1001, 'count_total': count_total,'count_today':count_today})
        else:
            return Response({'code': 1003, 'error': "权限错误"})


# 获取包信息
# get r_id,time,timetail,格式为%Y-%m-%d %H:%M:%S
class Packinfo(APIView):
    def get(self, request, *args, **kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        rule_id = request.GET.get('r_id')
        time = request.GET.get('time')
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        timetail = request.GET.get('timetail')
        timetail = datetime.datetime.strptime(timetail, "%Y-%m-%d %H:%M:%S")
        if (idmatch(token, rule_id)):
            packages = Packages.objects.filter(r_id=rule_id, cap_date__gte=time, cap_date__lte=timetail)
            # packages = Packages.objects.filter(r_id=rule_id)
            packages_info = PackagesSerializers(packages, many=True)
            return Response(packages_info.data)
        else:
            return Response({'code': 1003, 'error': "权限错误"})


# 数据下载
class Datadownload(APIView):
    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        rule_id = request.GET.get('r_id')
        if (idmatch(token, rule_id)):
            #
            # 这里放数据打包的实现
            #
            return Response({'code': 1001})
        else:
            return Response({'code': 1003, 'error': "权限错误"})


# 清理数据
# get r_id
class Dataclear(APIView):
    def get(self,request,*args,**kwargs):
        token = request.META.get('HTTP_TOKEN')
        #token = request.GET.get('token')
        rule_id = request.GET.get('r_id')
        if (idmatch(token, rule_id)):
            #
            # 这里放数据清理的实现
            #
            Packages.objects.filter(r_id=rule_id).delete()
            return Response({'code': 1001})
        else:
            return Response({'code': 1003, 'error': "权限错误"})