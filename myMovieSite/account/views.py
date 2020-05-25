# Create your views here.
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage,EmptyPage
from django.template.defaulttags import register#为了使用range
from haystack.views import SearchView
from .models import movies, EmailRecord
from django import forms
from django.shortcuts import render,reverse
import string
import random
from django.http import HttpResponseRedirect,HttpResponse
from django.utils.timezone import localtime
from haystack.views import SearchView
import myMovieSite.settings
from django.db import models
from .models import users,rate
from .models import collections
from .models import comments
from .forms import Commentforms, ForgetForm
from django.http import JsonResponse
from django.db.models import Count, Q, Avg
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

@register.filter
def get_range(value):
    return range(value)
'''
def BlogIndex(request):
    blog_list = BlogsPost.objects.order_by('-date')
    blognum = list(range(1,(BlogsPost.objects.count())//11+2))  #每10篇博客分一页
    return render(request,'blog/index.html',{'blog_list':blog_list,'blog_num':blognum})
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''
def register(request):
    while request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        em=users.objects.filter(user_email=email)
        if em:
            return HttpResponse("zhuceshibai")
        user = users.objects.create()
        user.user_name = username
        user.user_password = password
        user.user_email = email
        user.save()
        return HttpResponseRedirect(reverse('account:index'))


    return render(request, 'account/register.html')







def login(request):
    while request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        referer = request.META.get('HTTP_REFERER','account/index.html')
        if email and password:
            email=email.strip()
            # 获取表单用户密码
            # 获取的表单数据与数据库进行比较
            user = users.objects.filter(user_email=email, user_password=password).first()
            if user:
                response=redirect(request.GET.get('from','account:index'))
                response.set_cookie('username', max_age=7 * 24 * 3600)
                request.session['islogin'] = True
                request.session['user'] = user.user_name
                return response
            else:
                return HttpResponse('yonghubucunzai')
        else:
            return HttpResponse('email password feizhen')
    return render(request, 'account/login.html')



def index(request):
    movies_list=movies.objects.all().order_by("id")#按中文标题排序
    types= ['科幻','动作','剧情','喜剧','家庭','动画']
    objs=collections.objects.values('mov_id').annotate(usercount = Count('user_name'))
    avg_rate = rate.objects.values('mov_id').annotate(avg_rate=Avg('rate'))
    movs={}
    l=[]
    for obj in objs:
        l.append((obj['usercount'],obj['mov_id']))
    sors = dict(sorted(l)[:3])
    values= sors.values()
    val = list(values)
    #for value in values:
    #for i in range(2):
    fav_movies=movies.objects.filter(Q(id = val[0])|Q(id = val[1]))
    #fav_movies_list= index.objects.raw('SELECT COUNT(*),movie_id FROM collections GROUP BY movie_id')
    paginator = Paginator(movies_list,4)
    page = request.GET.get('page')
    try:
        mov = paginator.page(page)
        # todo: 注意捕获异常
    except PageNotAnInteger:
            # 如果请求的页数不是整数, 返回第一页。
        mov = paginator.page(1)
    except InvalidPage:
            # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')


    return render(request, 'account/index.html', {'movies_list': movies_list,'mov': mov,'fav_movies':fav_movies,'types':types,'avg_rate':avg_rate})


def type(request,type):
    movies_list = movies.objects.filter(type__contains = type)
    paginator = Paginator(movies_list, 4)
    page = request.GET.get('page')
    try:
        mov = paginator.page(page)
        # todo: 注意捕获异常
    except PageNotAnInteger:
        # 如果请求的页数不是整数, 返回第一页。
        mov = paginator.page(1)
    except InvalidPage:
        # 如果请求的页数不存在, 重定向页面
        return HttpResponse('找不到页面的内容')

    return render(request, 'account/index.html', {'movies_list': movies_list, 'mov': mov,})


def details(request,id):
    # 视图函数，返回文章详情页
    movie = movies.objects.filter(id=id).first()
    cmts = comments.objects.filter(movie_id = id)
    if request.session.has_key('islogin'):
        # 已经登录的用户，则放行
        context = {}
        context['user'] = request.session['user']
        context['curr_movie'] = movie
        context['id'] = id
        context['cmts'] = cmts
        # context['cookie'] = cookie

        context['comment_form'] = Commentforms(initial={'user': request.session['user'], 'movie_id': id})

        # user=users.object.filter()
        # comment= comments.objects.filter(mov_name=movie.ch_title,user_name=user)
        response = render(request, 'account/details.html', context)
        return response
    else:
        # 没有登录的用户，跳转到登录页面
        context = {}
        context['curr_movie'] = movie
        context['cmts'] = cmts
        response = render(request, 'account/details-un.html', context)
        return response
        # cookie = False

def rating(request):
    if request.method == "POST":
        mov_id = request.POST.get('mov_id')
        rat = request.POST.get('rate')
        if request.session.has_key('islogin'):
            user_name = request.session.get('user')
            object = rate.objects.filter(user_name=user_name,mov_id = mov_id)
            ra = float(rat)
            if object:

                if (ra <= 5):
                   object.rate = rat
                   return JsonResponse({'result': 'success', 'message': '评价成功'})
                else:
                    return JsonResponse({'result': 'fail', 'message': '评价失败'})
            else:
                if (ra <= 5):
                    obj = rate(mov_id=mov_id, rate=rat,user_name=user_name)
                    obj.save()
                    return JsonResponse({'result': 'success', 'message': '评价成功'})
                else:
                    return JsonResponse({'result': 'fail', 'message': '评价失败'})




def collect(request):
    #referer = request.META.post('HTTP_REFERER','account:index')
    if request.method == "POST":
        mov_id = request.POST.get('mov_id')
        if request.session.has_key('islogin'):
            user_name = request.session.get('user')
        # name_id = str(BlogUser.objects.get(name=name).id)
        # thisarticle = get_object_or_404(Articles, id=blog_id)
        # thisarticle.increase_views()
            #data = {}
            if collections.objects.filter(mov_id=mov_id).count() == 1:
            # 如果记录已经存在，则表示用户取消收藏
                exist_records=collections.objects.filter(mov_id=mov_id)
                exist_records.delete()
                return JsonResponse({'result':'fail', 'message':'取消收藏'})


            else:
                obj = collections(mov_id=mov_id, user_name=user_name)
                obj.save()
                return JsonResponse({'result': 'success', 'message':'收藏'})
        else:
           return render(request, 'account/login.html')



def update_comment(request):
    #referer = request.META.post('HTTP_REFERER','account:index')
    #movie_id = int(request.POST.get('object_id', ''))'
    comment_form = Commentforms(request.POST)
    data = {}
    if comment_form.is_valid():
        comment = comments()
        #comment.user_name = users.objects.filter(user_name=request.session['user'])[0]
        comment.user_name = comment_form.cleaned_data['user']
        comment.co_text = comment_form.cleaned_data['text']
        comment.movie_id = comment_form.cleaned_data['movie_id']
        #comment.content_type= comments.objects.filter(content_type = comment_form.cleaned_data['content_type'])[0]
        comment.save()


        data['status']='SUCCESS'
        data['user_name'] = comment.user_name
        data['co_time'] = localtime(comment.co_time.strftime('%d/%m/%Y %H:%M'))
        data['co_text'] = comment.co_text
        return JsonResponse(data)
    else:
        data['status'] = 'ERROR'
        return JsonResponse(data)



def center(request):
    if request.session.has_key('islogin'):
        user=request.session['user']
        col_mov = collections.objects.filter(user_name =user) # 按中文标题排序
        return render(request,"account/center.html",{"fav_movie":col_mov})
    else:
        return HttpResponseRedirect(reverse('account:login'))

def logout(request):
    del request.session['islogin']
    return HttpResponseRedirect(reverse('account:index'))


def email(request):
    form = ForgetForm(request.POST)
    if request.method == 'POST':
        email = form.cleaned_data['email']
        #user_email = users.objects.filter(user_email=email)
        #if user_email:
         #   send_mail(email, "forget")

    return render(request, 'account/email.html', locals())

def send_verification(request):
    email=request.GET.get('email')
    data={}
    if email !='':
        code = ''.join(random.sample(string.ascii_letters + string.digits,4))
        request.session['email_code'] = code
        send_mail(
                   '修改密码',
                   '验证码：%s' % code,
                   '3373319993@qq.com',
                   [email],
                   fail_silently=False,
                  )
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

##重置密码
def repsw(request):
    form = ForgetForm(request.POST)
    code = request.session['email_code']
    if form.is_valid():
        if request.method == 'POST':

            verif = form.cleaned_data['verification_code']
            newpwd = form.cleaned_data['newpwd']
            if verif == code:
                user = users.objects.filter(user_email=email)
                user.user_password = newpwd
                render(request, 'account/login.html')


    return render(request, 'account/repsw.html', locals())














    """
    def search(request):
    movie_name = request.GET.get('name')
    movie_id = movies.objects.filter(ch_title__contains = movie_name).id
    
    #result.object.ch_title
    #更新用户
    def update(request):
        # 获取客户端通过get请求发送过来的数据
        uid= request.POST.get('uid')
        password= request.POST.get('password')
        try:
            user = users.objects.filter(user_id=uid)

            users.objects.update(user_password=password)

            result = '更改成功'
        except:
            pass
        return render(request, 'account/register.html')
    #一个快捷函数： render() 「载入模板，填充上下文，再返回由它生成的 HttpResponse 对象」是一个非常常用的操作流程
    class AddFavView(request):
        def post(self,request):
            fav_id = request.POST.get('fav_id',0)
            fav_type = request.POST.get('fav_type',0)

            if not request.user.is_authenticated():
                # 判断用户是否登陆

                return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                #  如果记录已经存在，那么表示用户取消收藏
                exist_records.delete()

                if int(fav_type) == 1:
                    course = Courses.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    if course.fav_nums < 0:
                        course.fav_nums = 0
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums -= 1
                    if org.fav_nums < 0:
                        org.fav_nums = 0
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teaher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    if teacher.fav_nums < 0:
                        teacher.fav_nums = 0
                    teacher.save()


                return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()

                    if int(fav_type) == 1:
                        course = Courses.objects.get(id=int(fav_id))
                        course.fav_nums += 1
                        course.save()
                    elif int(fav_type) == 2:
                        org = CourseOrg.objects.get(id=int(fav_id))
                        org.fav_nums += 1
                        org.save()
                    elif int(fav_type) == 3:
                        teacher = Teaher.objects.get(id=int(fav_id))
                        teacher.fav_nums += 1
                        teacher.save()


                    return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
                else:

                    return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')




    curr_movie =0
    movies_list = movies.objects.all()
    for movie in movies_list:  # 循环判断每个文章，若文章的ID等于我输入的ID，那么跳出循环
        if movie.id == id:
            curr_movie=id


class MySearchIndex(SearchView):

    template = 'search.html'
    #我们通过重写extra_context 来定义我们自己的变量，
    #通过看源码，extra_context 默认返回的是空，然后再get_context方法里面，把extra_context
    #返回的内容加到我们self.context字典里
    def extra_context(self):
        context = super(MySearchIndex,self).extra_context()
        search_movies = movies.objects.select_related('account').all()[:3]
        context['search_movies']= search_movies
        return context

    def create_response(self):
        if not self.request.GET.get('q'):
            print(self.request.GET.get('q'))
            search_song = movies.objects.select_related('account').all()[:3]
            movies_info = movies.objects.all()
            paginator = Paginator(movies_info, myMovieSite.settings.HAYSTACK_SEARCH_RESULTS_PER_PAGE)
            try:
                page = paginator.page(int(self.request.GET.get('page',1)))
            except PageNotAnInteger:
                page = paginator.page(1)
            except EmptyPage:
                page = paginator.page(paginator.num_pages)
            print(page)
            return render(self.request, self.template, locals())
        else:
            qs = super(MySearchIndex, self).create_response()
            print(self.get_context())
            return qs


class MySeachView(SearchView):
    def extra_context(self):  # 重载extra_context来添加额外的context内容
        context = super(MySeachView, self).extra_context()
        side_list = account.objects.filter(kind='major').order_by('en_title')[:3]
        context['side_list'] = side_list
        return context


def BlogIndex(request):
    blog_list = BlogsPost.objects.order_by('-date')
    blognum = list(range(1,(BlogsPost.objects.count())//11+2))  #每10篇博客分一页
    return render(request,'blog/index.html',{'blog_list':blog_list,'blog_num':blognum})
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
"""