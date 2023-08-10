from django import template

register = template.Library()

def index(sequence, position):
    return sequence[position]

register.filter('index', index)