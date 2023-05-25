from django.db import models
from django.contrib.auth.models import User


class Entry(models.Model):
    """
    数据实体
    """
    # 数据类型的主键
    entry_type_key = models.IntegerField()
    value = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.value[:50]}..."


class EntryType(models.Model):
    """
    数据类型配置
    """
    # 表单单元格id
    key = models.CharField(max_length=255)
    # 表单单元格类型
    field_type = models.CharField(max_length=255)
    # html 类型
    html_type = models.CharField(max_length=255)
    # file_name_key
    file_name_key = models.CharField(max_length=255, default='')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.field_type}..."


class EntryTypeDict(models.Model):
    """
    数据类型枚举
    """
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    html_type = models.CharField(max_length=255)
    doc_value_type = models.CharField(max_length=255)
    comments = models.CharField(max_length=255)


class Task(models.Model):
    """
    任务表
    """
    task_name = models.CharField(max_length=255, default='test-任务名称')
    template_key = models.IntegerField(default=1)


class Template(models.Model):
    """
    模板表
    """
    template_name = models.CharField(max_length=255, default='test-任务名称')
    template_key = models.IntegerField(default=1)
    file_name = models.CharField(max_length=255, default='test-任务名称')
