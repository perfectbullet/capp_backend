import hashlib
import json

from django.http import JsonResponse
from django.template import loader
from django.views import View

from capp_doc.models import EntryType, EntryTypeDict, TaskTypeDict, Task, TaskTemplate, CappFileManagment
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
            }
            response_data['data'].append(one_data)
        return JsonResponse(response_data)

    def post(self, request):
        """
        新增或者修改，
        提供 row_id 时修改
        :param request:
        :return:
        """
        response_data = {
            'code': const.STATUS200,
            'msg': 'ok',
            'result': {}
        }
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
        task_obj, created = Task.objects.update_or_create(defaults=defaults, id=row_id)
        task_result = {
            'code': const.STATUS200,
            'msg': 'ok',
            'created': created,
            'id': task_obj.id,
            'task_temp_result': []
        }
        response_data['result'] = task_result
        template_infos = post_data.get('template_infos')
        for temp_info in template_infos:
            template_id = temp_info.get('template_id')
            template_sequence = temp_info.get('template_sequence')
            row_id = temp_info.get('id')
            defaults = {
                'task_id': task_obj.id,
                'template_id': template_id,
                'template_sequence': template_sequence,
            }
            obj, created = TaskTemplate.objects.update_or_create(defaults=defaults, id=row_id)
            task_result['task_temp_result'].append({
                'created': created,
                'id': obj.id
            })
        return JsonResponse(response_data)


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


class TaskTemplateView(View):
    """
    任务-子文档

    任务下选择的模板
    """

    def get(self, request):
        """
        查询任务模板
        :param request:
        :return:
        """
        query_data = request.GET.dict()
        response_data = {
            'code': const.STATUS200,
            'msg': 'ok',
            'data': []
        }
        task_id = query_data.get('task_id')
        task_name = Task.objects.get(id=task_id).task_name
        objs = TaskTemplate.objects.all()
        if task_id:
            objs = objs.filter(task_id=task_id)
        for obj in objs:
            one_data = {
                'id': obj.id,
                'task_id': obj.task_id,
                'template_id': obj.template_id,
                'template_sequence': obj.template_sequence,
                'task_name': task_name,
            }
            response_data['data'].append(one_data)

        return JsonResponse(response_data)

    def post(self, request):
        """

        :param request:
        :return:
        """
        post_data = json.loads(request.body)
        task_id = post_data.get('task_id')
        template_infos = post_data.get('template_infos')
        result_info = []
        for temp_info in template_infos:
            template_id = temp_info.get('template_id')
            template_sequence = temp_info.get('template_sequence')
            row_id = temp_info.get('id')
            defaults = {
                'task_id': task_id,
                'template_id': template_id,
                'template_sequence': template_sequence,
            }
            obj, created = TaskTemplate.objects.update_or_create(defaults=defaults, id=row_id)
            result_info.append({
                'created': created,
                'id': obj.id
            })
        return JsonResponse({
            'code': const.STATUS200,
            'msg': 'ok',
            'result_info': result_info
        })


class CappFileManagmentView(View):
    """
    子文档模板查询
    """
    def get(self, request):
        response_data = {
            'code': const.STATUS200,
            'msg': 'ok',
            'data': []
        }
        objs = CappFileManagment.objects.filter(parent_id__exact=0)
        for obj in objs:
            one_data = {
                'id': obj.id,
                'file_name': obj.file_name,
                'file_path': obj.file_path,
                'file_type': obj.file_type,
                'create_time': obj.create_time,
                'parent_id': obj.parent_id,
            }
            response_data['data'].append(one_data)
        return JsonResponse(response_data)
