from django.contrib import admin

from .models import Document, Term, TermDocument

admin.site.register(Document)
admin.site.register(Term)
admin.site.register(TermDocument)
