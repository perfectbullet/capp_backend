"""Defines URL patterns for learning_logs."""

from django.urls import path

from . import views
from .task_views import TaskTypeDictView, TaskView, TaskTemplateView, CappFileManagmentView

app_name = 'capp_doc'
urlpatterns = [
    path('template_file_list', CappFileManagmentView.as_view(), name='template file list'),
    path('task', TaskView.as_view(), name='TaskTypeDictView'),
    path('task_template', TaskTemplateView.as_view(), name='task template view'),
    path('task_type_dict', TaskTypeDictView.as_view(), name='TaskTypeDictView'),
    path('entry_type', views.EntryTypeView.as_view(), name='get entry type'),
    path('entry_data', views.EntryView.as_view(), name='get entry'),
    path('get_template_data', views.TemplateView.as_view(), name='get template data'),
    path('entry_type_dict', views.EntryTypeDictView.as_view(), name='entry type dict')
]
