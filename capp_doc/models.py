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


class TaskTypeDict(models.Model):
    """
    数据类型枚举
    """
    # 字典 code
    # task_status 任务状态  distributing 下发中   distribute_ok  下发完成  task_done  任务完成  task_save  任务保存
    # 任务类型    单装备任务   single_task   工程任务   project_task
    code = models.CharField(max_length=255)
    # 字典 中文名称
    name = models.CharField(max_length=255)
    # 字典数据类型  task_type,  task_status
    code_type = models.CharField(max_length=255, default='task_type')
    comments = models.CharField(max_length=255)


class Task(models.Model):
    """
    任务表
    """
    # 任务名称
    task_name = models.CharField(max_length=255, default='test-任务名称')
    # 任务类型
    task_type = models.CharField(max_length=255, default='task_type')
    # 任务状态
    task_status = models.CharField(max_length=255, default='task_status')
    date_added = models.DateTimeField(auto_now_add=True)


class TaskTemplate(models.Model):
    """
    任务的模板
    """
    # 任务id
    task_id = models.IntegerField(default=1)
    # 模板id
    template_id = models.CharField(max_length=255, default='test-任务名称')
    # 选择模板得顺序, 用于合并显示排序得
    template_sequence = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)


class Template(models.Model):
    """
    模板表
    """
    template_name = models.CharField(max_length=255, default='template_name')
    file_name = models.CharField(max_length=255, default='file_name')
    file_file_path = models.CharField(max_length=255, default='file_file_path')
    # 模板原来得文件路径（或者名称什么的）
    template_from = models.CharField(max_length=255, default='file_file_path')
    date_added = models.DateTimeField(auto_now_add=True)
