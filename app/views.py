import re

import markdown
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.messages import success
from django.shortcuts import render, redirect

from app.forms import RegisterForm, LoginForm, PostForm, UserProfileForm
from app.models import BlogPost, MyUser, UserProfile
from django.contrib.auth import logout, authenticate, login, get_user_model


# Create your views here.

User = get_user_model()

def root_page(request):
    return redirect('index')

def index(request):
    posts = BlogPost.objects.all()[:10]
    return render(request, 'index.html', {'posts': posts})

def logout_view(request):
    logout(request)
    return redirect('/index')
def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index')
            else:
                messages.error(request, 'Email or password incorrect')
        else:
            messages.error(request, 'Invalid Email or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html',{'form': form})

def contact_view(request):
    return render(request, 'contact_view.html')

def post_view(request, post_id):
    post = BlogPost.objects.get(id=post_id)

    content_html = markdown.markdown(post.body, extensions=["mdx_math"],
                    extension_configs={
                        'mdx_math': {
                            'enable_dollar_delimiter': True,  # 是否启用单美元符号
                            'add_preview': True  # 在公式加载成功前是否启用预览
                        }
                    }) # https://juejin.cn/post/7081398280755773447
    return render(request, 'post_view.html', {'post': post, 'content_html': content_html})

# 用户注册页面
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 获取表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            hashed_password = make_password(password)
            # 创建新用户
            new_user = User.objects.create(
                username=username,
                email=email,
                password=hashed_password)

            messages.success(request, 'Account created successfully')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

def upload_article(request):
    if not request.user.is_authenticated:
        messages.error(request, '请先登录')
        return redirect('/index')
    if request.method == "POST":
        form = PostForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            blog_post = form.save(commit=False)

            blog_post.author = request.user
            print("success")
            blog_post.save()

            return redirect('/index')
    else:
        form = PostForm()
    return render(request, 'upload_article.html', {'form': form})

def about(request):
    return render(request, 'about.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    print(user)
    profile = UserProfile.objects.filter(user=user).first()
    posts = BlogPost.objects.filter(author=username)
    return render(request, 'user_profile.html', {'profile': profile, 'user': user, 'posts': posts})

def edit_profile(request):
    if not UserProfile.objects.filter(user=request.user).first():
        UserProfile.objects.create(user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(profile.get_absolute_url())
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form, 'profile': profile})
