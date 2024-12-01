from django import template

register = template.Library()

@register.filter
def add_class(value, arg):
    # 用于给 HTML 元素添加类的自定义过滤器。
    return value.as_widget(attrs={'class': arg})