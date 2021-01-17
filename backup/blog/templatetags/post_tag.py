from django import template
from blog.models import Category,Post


register = template.Library()
@register.inclusion_tag('blog/latest_posts.html')
def latest_posts():
    context = {
        'l_posts': Category.objects.all()[0:15],
    }
    return context
  
@register.inclusion_tag('blog/v_posts.html')
def latest_posts1():
    context = {
        'l_posts': Post.objects.order_by('-views')[0:5],
    }
    return context
 