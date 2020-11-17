from django.db import models
from django.conf import settings
import os

# Create your models here.
# 用户
class Users(models.Model):
    user_type_choices = (
                (1, 'user'),
                (2, 'admin'),
    )
    user_name = models.CharField(max_length=64)
    user_pwd = models.CharField(max_length=64)
    user_type = models.IntegerField(choices=user_type_choices,default=None)
    # user_token = models.CharField(max_length=64,null=True,blank=True)

    def __str__(self):
        return self.user_name


# 网卡
class Adapter(models.Model):
    name = models.CharField(max_length=64)
    flow_rate = models.FloatField()
    loss_rate = models.FloatField()
    state = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 规则
# 由于约束关系所以将开启全留存的包的规则设为0
class Rule(models.Model):
    r_type_choices = (
        (0,'default'),
        (1,'ip'),
        (2,'protocal'),
        (3,'feature'),
    )
    # 如果用户删除那么规则怎么处理，伪删除吗还是彻底删除？
    uid = models.ForeignKey(Users,on_delete=models.CASCADE) # on_delete=models.CASCADE,多对一关系
    r_ofadapter = models.ForeignKey(Adapter,on_delete=models.CASCADE)
    r_name = models.CharField(max_length=64)
    r_state = models.BooleanField(default=False)
    r_addtime = models.DateTimeField(auto_now_add=True)
    r_isdel = models.BooleanField(default=False)
    r_description = models.TextField(default=None, null=True ,blank=True)
    r_type = models.IntegerField(choices=r_type_choices, default=0)
    src_ip = models.CharField(max_length=64, default=None, null=True,blank=True)
    dst_ip = models.CharField(max_length=64, default=None, null=True,blank=True)
    min_src_port = models.CharField(max_length=64, default=None, null=True,blank=True)
    max_src_port = models.CharField(max_length=64, default=None, null=True,blank=True)
    min_dst_port = models.CharField(max_length=64, default=None, null=True,blank=True)
    max_dst_port = models.CharField(max_length=64, default=None, null=True,blank=True)
    package_type = models.IntegerField(default=0)
    feature = models.CharField(max_length=64, default=None, null=True,blank=True)

    def __str__(self):
        return self.r_name


# 包
def pack_path():
    return os.path.join(settings.PACKCAPTURE_DIR,'packages')


class Packages(models.Model):
    r_id = models.ForeignKey(Rule,on_delete=models.CASCADE)
    adapter = models.ForeignKey(Adapter,on_delete=models.CASCADE)
    cap_date = models.DateTimeField(auto_now_add=True)
    path = models.FilePathField(path=pack_path)
    src_ip = models.CharField(max_length=64)
    dst_ip = models.CharField(max_length=64)
    src_port = models.IntegerField()
    dst_port = models.IntegerField()
    package_type = models.IntegerField()
    session_id = models.IntegerField()





