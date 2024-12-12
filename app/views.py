import markdown
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView

from app.forms import RegisterForm, LoginForm, PostForm, UserProfileForm, CommentForm
from app.models import BlogPost, UserProfile, Comment, CategoryPost
from django.contrib.auth import logout, authenticate, login, get_user_model

User = get_user_model()


def root_page(request):
    return redirect('index')


class IndexView(ListView):
    model = BlogPost
    template_name = 'index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return BlogPost.objects.all().order_by('-posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoryPost.objects.all()
        return context


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
    return render(request, 'user/login.html', {'form': form})


def contact_view(request):
    return render(request, 'contact_view.html')


def post_view(request, post_id):
    post = BlogPost.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        print(request.POST)
        print(form.is_valid())
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post_id = post
            comment.save()
            return redirect('post-view', post_id=post_id)

    user = User.objects.get(username=post.author)
    userprofile = UserProfile.objects.get(user=user)

    # https://juejin.cn/post/7081398280755773447
    content_html = markdown.markdown(post.body, extensions=[
        "mdx_math",
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc', ],
                                     extension_configs={
                                         'mdx_math': {
                                             'enable_dollar_delimiter': True,  # 是否启用单美元符号
                                             'add_preview': True  # 在公式加载成功前是否启用预览
                                         }
                                     })
    comments = Comment.objects.filter(post_id=post_id)

    return render(request, 'blog/post_view.html',
                  {'post': post,
                        'content_html': content_html,
                        'userprofile': userprofile,
                        'comments': comments})


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
            return render(request, 'user/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'user/register.html', {'form': form})


def upload_article(request):
    if not request.user.is_authenticated:
        messages.error(request, '请先登录')
        return redirect('/index')
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)

            blog_post.author = request.user
            blog_post.save()

            return redirect('/index')
    else:
        form = PostForm()
    return render(request, 'blog/upload_article.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def user_profile(request, username):
    user = User.objects.get(username=username)
    print(user)
    profile = UserProfile.objects.filter(user=user).first()
    posts = BlogPost.objects.filter(author=username)
    return render(request, 'user/user_profile.html', {'profile': profile, 'user_in_profile': user, 'posts': posts})


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
    return render(request, 'user/edit_profile.html', {'form': form, 'profile': profile})


class UserPostListView(ListView):
    model = BlogPost
    template_name = 'user/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        username = self.kwargs.get('name')
        return BlogPost.objects.filter(author=username).order_by('-posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.kwargs.get('name')
        return context


class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    fields = ['title', 'body', 'category']
    context_object_name = 'post'
    template_name = 'blog/post_edit.html'

    def get_success_url(self):
        return reverse_lazy('user-post-list', kwargs={'name': self.request.user.username})

    # UserPassesTestMixin：验证用户权限
    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user.username


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('user-post-list', kwargs={'name': self.request.user.username})

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user.username

class CategoryView(ListView):
    model = BlogPost
    template_name = 'blog/category.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(CategoryPost, id=category_id)
        return category.posts.order_by('-posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        context['category'] = get_object_or_404(CategoryPost, id=category_id)
        return context

class PostSearchView(ListView):
    model = BlogPost
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query is not None:
            return BlogPost.objects.filter(
                models.Q(title__icontains=query) |
                models.Q(body__icontains=query)
            ).order_by('-posted')
        return BlogPost.objects.all().order_by('-posted')