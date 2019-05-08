from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,"index.html")

def about(request):
    return render(request,"about.html")

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(content__contains = keyword)
        return render(request,"articles.html",{"articles":articles})

    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles" : articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"<b>" + str(article) + "</b> isimli makale başarıyla oluşturuldu!",extra_tags="safe")
        return redirect("index")
    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    article = get_object_or_404(Article,id = id)
    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})

@login_required(login_url = "user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None,request.FILES or None,instance= article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"<b>" + str(article) + "</b> isimli makale başarıyla güncellendi!",extra_tags="safe")
        return redirect("index")

    return render(request,"update.html",{"form":form})

@login_required(login_url = "user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    deleted_article = str(article)
    article.delete()
    messages.info(request,"<b>" + deleted_article + "</b> isimli makale başarıyla silindi!",extra_tags="safe")
    return redirect("article:dashboard")

def addComment(request,id):
    article = get_object_or_404(Article,id = id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()

        messages.success(request,"Yorumunuz başarıyla iletildi, teşekkür ederiz! " + "<b>" + str(comment_author) + "</b>",extra_tags="safe")

    return redirect(reverse("article:detail",kwargs={"id":id}))