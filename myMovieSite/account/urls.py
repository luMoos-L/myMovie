from django.urls import path,re_path
from . import views
from django.urls import include

#你这个app 最好就做成这样，最多再添加一个修改密码的页面
#懂了没 懂啦 index拆分出去是啥
# 就是现在index归属在account这个app里面 但是实际上index和account没什
# 但是为了访问是 127.0.0.1/login这样来登陆 现在就只能写成这样
# 拆分后就是 127.0.0.1 是首页 127.0.0.1/account/login 这样是登陆
# 暂时就这样 还是比较好看的 127.0.0.1 首页 127.0.0.1/login 登陆 127.0.0.1/regist 注册
#懂了没 嗯嗯
# 你去下个模板 现在就可以开始套上了 前端吗 嗯 就有个网站叫模板之家 你去上面找个符合你主题的 比如搜电影 o'k'k
urlpatterns = [
    path('login',views.login,name='login'),
    path('register',views.register,name = 'register'),
    path('',views.index,name = 'index'),
    # path('details',views.details,name='details')
    # re_path(r'^details/(?P<id>[0-9]{4})/$',views.details,name = 'details'),
    re_path(r'^details/[(,)]*(?P<id>[0-9]{4})*/$',views.details,name = 'details'),
    path('update_comment', views.update_comment, name='update_comment'),
    #path(r'^search/', include('haystack.urls'))
    path('collect',views.collect,name = 'collect'),
    path('rating',views.rating,name = 'rating'),
    path('center',views.center,name = 'center'),
    path('logout',views.logout,name ='logout'),
   #re_path(r'^type/[\u4e00-\u9fa5]{2}/$',views.type,name = 'type')
    re_path(r'type/[(,)]*([\u4E00-\u9FA5]{2,4})*/$',views.type,name = 'type'),
   ##发送邮件
    path('email/',views.email,name='email'),
    path('send_verification/',views.send_verification,name='send_verification'),
    ##重置密码（接受邮件中url的参数）
    path('repsw/',views.repsw,name='repsw')

]
app_name = 'account'
