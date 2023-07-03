# myapp/templatetags/myapp_tags.py

from django import template

register = template.Library()

@register.filter
def is_member_of_group(user, group_name):
    return user.groups.filter(name=group_name).exists()
