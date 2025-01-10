from django import template
import re

register = template.Library()

@register.filter
def highlight(text, tokens):
    if not tokens:
        return text
    
    for token in tokens:
        regex = re.compile(r'\b{}\b'.format(re.escape(token)), re.IGNORECASE)
        text = regex.sub(f'<span class="highlight">{token}</span>', text)
    
    return text
