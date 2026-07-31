from django import template

register = template.Library()

@register.filter(name='hazard_path')
def hazard_path(node):
    path = []
    for parent in node.get_ancestors():
        path.append(parent.slug)
    path.append(node.slug)
    return '/'.join(path)