"""
URL configuration for MyBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf.urls.static import static

from app.feeds import BlogRSSFeed
from app.views import UserPostListView, PostDeleteView, PostEditView, IndexView, CategoryView, PostSearchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view(), name='index'),
    path('', views.root_page),
    path('logout/', views.logout_view, name = 'logout'),
    path('login/', views.login_view , name = 'login'),
    path('contact/', views.contact_view, name = 'contact'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/', views.post_view, name='post-view'),
    path('register/', views.register_view, name='register'),
    path('upload/', views.upload_article, name='upload-article'),
    path('user_profile/<str:username>/', views.user_profile, name='user-profile'),
    path('edit_profile/', views.edit_profile, name='edit-profile'),
    path('posts/<str:name>', UserPostListView.as_view(), name='user-post-list'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post-edit'),  # 编辑文章
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # 删除文章
    path('category/<int:category_id>', CategoryView.as_view(), name='category-posts'),
    path('search_list/', PostSearchView.as_view(), name='search-list'),
    path("accounts/", include("allauth.urls")),

    path('rss/', BlogRSSFeed(), name='rss_feed'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)