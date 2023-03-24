from django.urls import path
from .views import IndexEditorView
urlpatterns = [
    path('make_index/<int:id>', IndexEditorView.as_view(), name='editor_external_view')
]

