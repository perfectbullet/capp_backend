"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views

app_name = 'capp_doc'
urlpatterns = [
    path('entry_type', views.EntryTypeView.as_view(), name='get entry type'),
    path('entry_data', views.EntryView.as_view(), name='get entry'),
    path('get_template_data', views.TemplateView.as_view(), name='get template data'),
    path('entry_type_dict', views.EntryTypeDictView.as_view(), name='entry type dict')
]
