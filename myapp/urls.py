from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_document, name='add_document'),
    path('list-questions/', views.list_questions, name='list_questions'),
    path('search/', views.search_documents, name='search_documents'),
    path('document/<int:document_id>/delete/', views.delete_document, name='delete_document'),
]
