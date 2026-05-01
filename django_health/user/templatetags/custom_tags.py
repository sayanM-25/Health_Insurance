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


@register.simple_tag
def plan_image_for_category(category):
    images = {
        'individual': 'user/images/plan_pic/individual-plan.svg',
        'family': 'user/images/plan_pic/family-plan.svg',
        'senior': 'user/images/plan_pic/senior-plan.svg',
    }
    return images.get(category, 'user/images/plan_pic/default-plan.svg')

