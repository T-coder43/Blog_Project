import markdown
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# 导入数据模型ArticlePost
from .models import ArticlePost
# 引入redirect重定向模块
from django.shortcuts import render, redirect
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    # # 取出所有博客文章
    # if request.GET.get('order') == 'total_views':
    #     article_list = ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     article_list = ArticlePost.objects.all()
    #     order = 'normal'
    if search:
        if order == 'total_views':
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 每页显示 1 篇文章
    paginator = Paginator(article_list, 3)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)
    # 需要传递给模板（templates）的对象
    context = {'articles': articles, 'order': order}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)
    # article.body = markdown.markdown(article.body,
    #                                  extensions=[
    #                                      # 包含 缩写、表格等常用扩展
    #                                      'markdown.extensions.extra',
    #                                      # 语法高亮扩展
    #                                      'markdown.extensions.codehilite',
    #                                      # 目录扩展
    #                                      'markdown.extensions.toc',
    #                                  ])
    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 浏览量 +1
    article.total_views += 1
    article.save(update_fields=['total_views'])
    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc}
    # 载入模板 并返回context对象
    return render(request, 'article/detail.html', context)


def article_create(request):
    # 判断用户是否提交数据
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            # 指定目前登录的用户作为作者
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect("article:article-list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)


def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article-list")


# 安全删除文章
def article_safe_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("你没有权限删除这篇博客。")
    if request.method == 'POST':
        # article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article-list")
    else:
        return HttpResponse("仅允许post请求")


# 更新文章
# 提醒用户登录
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("你没有权限修改这篇博客。")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.body = request.POST['body']
            article.title = request.POST['title']
            article.save()
            return redirect("article:article-detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")

    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form, 'article': article}
        return render(request, 'article/update.html', context)
