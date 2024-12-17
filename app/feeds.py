from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import BlogPost

class BlogRSSFeed(Feed):
    title = "Blog RSS Feed"
    link = "/rss/"
    description = "Blog RSS Feed"

    def items(self):
        return BlogPost.objects.all()[:6]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return reverse('post-view', args=[item.id])

    def item_author_name(self, item):
        # 每篇文章的作者
        return item.author

    def item_pubdate(self, item):
        # 每篇文章的发布时间
        return item.posted