# from django import template

# register = template.Library()

# @register.simple_tag
# def is_admin(user):
#     return user.is_superuser
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def is_admin(context):
    user = context['user']
    return user.is_superuser

