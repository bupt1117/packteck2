from django.urls import path

from . import views

app_name = 'api'
urlpatterns = [
    path('login', views.Login.as_view()),
    path('changepwd', views.Changepwd.as_view()),
    path('usermanage', views.Usermanage.as_view()),
    path('adduser', views.Adduser.as_view()),
    path('resetpwd', views.Resetpwd.as_view()),
    path('adaptersinfo', views.Adaptersinfo.as_view()),
    path('rulesinfo', views.Ruleinfo.as_view()),
    path('rulesnum', views.Rulenum.as_view()),
    path('addrule',views.Addrule.as_view()),
    path('changerule',views.ChangeRule.as_view()),
    path('addrulebycsv',views.Addrulebycsv.as_view()),
    path('exampledownload',views.Exampledownload.as_view()),
    path('shot',views.Shot.as_view()),
    path('shotlist',views.Shotlist.as_view()),
    path('dataclear',views.Dataclear.as_view()),

]