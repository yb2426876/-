from django.shortcuts import render,redirect,HttpResponse
from django.contrib import auth
from blog.models import Article,Category,Tag,UserInfo,ArticleUpDown
from django.db.models import Count,Sum



def query_date(username,artical_id):
    user = UserInfo.objects.filter(username=username).first()
    blog = user.blog
    cate_ret = Article.objects.filter(user_id=user.pk).values(
        "category_id").annotate(c=Count("category_id")).values_list(
        "category__title", "c")
    tag_list = Tag.objects.filter(blog=user.blog).annotate(
        c=Count("article__title")).values_list("title", "c")
    article_sum = Article.objects.filter(user_id=user.pk).values(
        "user_id").annotate(s=Count('nid')).values("s")
    article_list = Article.objects.filter(user__username=username)
    artical = Article.objects.filter(pk=artical_id).first()

    return {"user":user,"blog":blog,"cate_ret":cate_ret,"tag_list":tag_list,"article_sum":article_sum,
            "article_list":article_list,"artical":artical}


def login(request):
    if request.method == "POST":
        user = request.POST.get("username")
        pwd = request.POST.get("password")
        user = auth.authenticate(username=user,password=pwd)
        print(user)
        if user:
            auth.login(request,user)
            return redirect("/index/")
    return render(request,"login.html")


def index(request):
    article_list = Article.objects.all()

    return render(request,"index.html",{"article_list":article_list})

def logout(request):

    auth.logout(request)
    return redirect("/index/")


def homesite(request,username,**kwargs):
        user = UserInfo.objects.filter(username=username).first()
        if user:
            blog = user.blog
            # article_list = Article.objects.filter(user_id=user.pk)
            cate_ret = Article.objects.filter(user_id=user.pk).values("category_id").annotate(c=Count("category_id")).values_list("category__title","c")
            article_sum = Article.objects.filter(user_id=user.pk).values("user_id").annotate(s=Count('nid')).values("s")
            tag_list = Tag.objects.filter(blog=user.blog).annotate(c=Count("article__title")).values_list("title", "c")
            print(tag_list)
            # date_list = Article.objects.filter(user=user).extra(select={"y_m_date":"strftime('%%Y/%%m',create_time)"}).values("y_m_date").annotate(c=Count("title")).values("y_m_date","c")
        # tag =Article.objects.filter(user_id=user.pk).values
        #     print(date_list)
            if not kwargs:
                article_list = Article.objects.filter(user__username=username)
            else:
                condition = kwargs.get("condition")
                params = kwargs.get("params")
                if condition== "tag":
                    article_list = Article.objects.filter(user__username=username).filter(tags__title=params)
                    # tag_num = Tag.objects.filter(blog=user.blog).annotate(c=Count("artic"))
                    print((article_list))

                elif condition == "category":
                    article_list = Article.objects.filter(user__username=username).filter(category__title=params)



            return render(request,"homesite.html",locals())
        return redirect('/login/')
def register(request):


    return render(request,"register.html")

import json
def artical_detail(request,artical_id,username):
    content = query_date(username, artical_id)
    if request.method ==" POST":
        if request.is_ajax:
            user =  username
            artical = artical_id
            up_down = request.POST.get("is_up")
            result_obj = ArticleUpDown.objects.filter(user_id=content[user].pk,article_id=artical_id)
            print(22)
            if result_obj:
                ArticleUpDown.objects.create(is_up=up_down,artical_id=artical_id,user_id=content.get('user').pk)
                up_num = artical.up_count +1
                print({'diggnum':up_num,"result":"成功推荐"})
                return HttpResponse(json.dumps({'diggnum':up_num,"result":"成功推荐"}))


            else:
                up_num =artical.up_count
                print({'diggnum':up_num,"result":"您已经推荐过了"})
                return HttpResponse(json.dumps({'diggnum':up_num,"result":"您已经推荐过了"}))




    return render(request,"article-detail.html",content)


from blog.models import ArticleUpDown
def updown(request):
    is_up = request.POST.get("is_up")
    artical_id = request.POST.get("article_id")
    user_id = request.user.pk
    print(is_up,artical_id,user_id)




    return HttpResponse("OK")




