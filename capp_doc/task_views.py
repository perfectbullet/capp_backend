import json
import hashlib
from django.http import JsonResponse
from django.template import loader
from django.views import View

from capp_doc.models import Entry, EntryType, EntryTypeDict, TaskTypeDict, Task
from common import const


class TaskView(View):
    """
    任务视图
    """

    def get(self, request):
        query_data = request.GET.dict()
        response_data = {
            'code': const.STATUS200,
            'msg': 'ok',
            'data': []
        }
        task_name = query_data.get('task_name')
        objs = Task.objects.all()
        if task_name:
            objs = objs.filter(task_name__contains=task_name)

        for obj in objs:
            one_data = {
                    'id': obj.id,
                    'task_name': obj.task_name,
                    'task_type': obj.task_type,
                    'task_status': obj.task_status,
                    'date_added': obj.date_added,
                },
            response_data['data'].append(one_data)
        return JsonResponse(response_data)

    def post(self, request):
        """
        新增或者修改，
        提供 row_id 时修改
        :param request:
        :return:
        """
        post_data = json.loads(request.body)
        row_id = post_data.get('id')
        task_name = post_data.get('task_name')
        task_type = post_data.get('task_type')
        task_status = post_data.get('task_status')

        defaults = {
            'task_name': task_name,
            'task_type': task_type,
            'task_status': task_status,
        }
        obj, created = Task.objects.update_or_create(defaults=defaults, id=row_id)
        return JsonResponse({
            'code': const.STATUS200,
            'msg': 'ok',
            'created': created,
            'id': obj.id
        })


class TemplateView(View):
    """
    子文档模板表
    """
    md5 = hashlib.md5()

    def get(self, request):
        response_data = {
            'code': const.STATUS200,
            'msg': 'ok',
        }

        template_path = 'capp_doc/3.html'
        self.md5.update(template_path.encode('utf-8'))
        file_name_key = self.md5.hexdigest()
        ets = EntryType.objects.filter(file_name_key=file_name_key)
        context = {
            'file_name_key': file_name_key,
            # 这里时 输入框 key 的列表
            'render_value_111222333344': '段落',
            'render_code_111222333344': 'paragraph'
        }

        for ef in ets:
            etd = EntryTypeDict.objects.get(code=ef.field_type)
            context['render_value_' + ef.key] = etd.name
        print(context)
        template_content = loader.render_to_string(template_path, context)
        response_data['template_content'] = template_content
        response_data['file_name_key'] = file_name_key
        return JsonResponse(response_data)


class TaskTypeDictView(View):
    """
    任务类型，状态字典
    """

    def get(self, request):
        query_data = request.GET.dict()
        response_data = {
            'code': const.STATUS200,
            'msg': 'ok',
            'data': []
        }
        code_type = query_data.get('code_type')
        objs = TaskTypeDict.objects.all()
        if code_type:
            objs = objs.filter(key=code_type)
        if objs:
            for obj in objs:
                one_data = {
                    'id': obj.id,
                    'code': obj.code,
                    'name': obj.name,
                    'code_type': obj.code_type,
                    'comments': obj.comments,
                }
                response_data['data'].append(one_data)
        else:
            response_data['data'] = {}
        return JsonResponse(response_data)

    def post(self, request):
        post_data = json.loads(request.body)
        code = post_data.get('code')
        code_type = post_data.get('code_type')
        name = post_data.get('name')
        comments = post_data.get('comments')
        row_id = post_data.get('id')
        defaults = {
            'code': code,
            'name': name,
            'code_type': code_type,
            'comments': comments,
        }

        obj, created = TaskTypeDict.objects.update_or_create(defaults=defaults, id=row_id)
        return JsonResponse({
            'code': const.STATUS200,
            'msg': 'ok',
            'created': created,
            'id': obj.id
        })
