import json
import hashlib
import os
from django.http import JsonResponse
from django.template import loader
from django.views import View
from django.conf import settings

from capp_doc.models import Entry, EntryType, EntryTypeDict

STATUS200 = 200
STATUS400 = 400


class EntryView(View):
    """
    数据类型视图
    """

    def handle_uploaded_file(self, f, tag_id):
        """
        按 tag_id 保存数据
        :param f:
        :param tag_id:
        :return:
        """
        file_path = os.path.join(settings.BASE_DIR, 'capp_doc', 'tag_files', tag_id)
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path

    def get(self, request):
        query_data = request.GET.dict()
        response_data = {
            'code': STATUS200,
            'msg': 'ok',
            'data': []
        }
        row_id = query_data.get('id')
        obj = Entry.objects.filter(id=row_id)
        if obj:
            response_data = {
                'code': STATUS200,
                'msg': 'ok',
                'data': [{
                    'id': obj.id,
                    'value': obj.value,
                    'entry_type_key': obj.entry_type_key,
                },
                ]
            }
        else:
            response_data['data'] = {}
        return JsonResponse(response_data)

    def post(self, request):
        """
        新增或者修改，
        提供 row_id 时修改 taskId,templeteId,spaceId
        :param request:
        :return:
        """
        post_data = request.POST
        row_id = post_data.get('id')
        # 任务id
        task_id = post_data.get('task_id')
        # 模板id
        template_id = post_data.get('template_id')
        # 子文档标记区域的 tag_id
        tag_id = post_data.get('tag_id')
        # tag_file 子文档二进制对象
        tag_file = request.FILES['tag_file']
        tag_file_path = self.handle_uploaded_file(tag_file, tag_id)
        defaults = {
            'task_id': task_id,
            'template_id': template_id,
            'tag_id': tag_id,
            'tag_file': tag_file_path,
            'tag_file_url': tag_file_path,
        }
        obj, created = Entry.objects.update_or_create(defaults=defaults, id=row_id)
        return JsonResponse({
            'code': STATUS200,
            'msg': 'ok',
            'created': created,
            'id': obj.id
        })


class EntryTypeView(View):
    """
    数据类型视图
    """

    def get(self, request):
        query_data = request.GET.dict()
        response_data = {
            'code': STATUS200,
            'msg': 'ok',
            'data': []
        }
        key = query_data.get('key')
        objs = EntryType.objects.all()
        if key:
            objs = objs.filter(key=key)
        if objs:
            for obj in objs:
                one_data = {
                    'id': obj.id,
                    'key': obj.key,
                    'html_type': obj.html_type,
                    'field_type': obj.field_type
                }
                response_data['data'].append(one_data)
        else:
            response_data['data'] = {}
        return JsonResponse(response_data)

    def post(self, request):
        post_data = json.loads(request.body)
        key = post_data.get('key')
        field_type = post_data.get('field_type')
        html_type = post_data.get('html_type')
        file_name_key = post_data.get('file_name_key', '')

        defaults = {
            'field_type': field_type,
            'html_type': html_type,
            'file_name_key': file_name_key
        }

        obj, created = EntryType.objects.update_or_create(defaults=defaults, key=key)
        return JsonResponse({
            'code': STATUS200,
            'msg': 'ok',
            'created': created,
            'key': key
        })


class TemplateView(View):
    """
    html 渲染
    """
    md5 = hashlib.md5()

    def get(self, request):
        response_data = {
            'code': STATUS200,
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


class EntryTypeDictView(View):
    """
    返回数据类型
    """
    def get(self, request):
        query_data = request.GET.dict()
        response_data = {
            'code': STATUS200,
            'msg': 'ok',
            'data': []
        }
        key = query_data.get('key')
        objs = EntryTypeDict.objects.all()
        if key:
            objs = objs.filter(key=key)
        if objs:
            for obj in objs:
                one_data = {
                    'code': obj.code,
                    'name': obj.name,
                    # 'html_type': obj.html_type,
                    # 'doc_value_type': obj.doc_value_type,
                    'comments': obj.comments,
                }
                response_data['data'].append(one_data)
        else:
            response_data['data'] = {}
        return JsonResponse(response_data)

    def post(self, request):
        post_data = json.loads(request.body)
        code = post_data.get('code')
        html_type = post_data.get('html_type')
        doc_value_type = post_data.get('doc_value_type')
        name = post_data.get('name')
        comments = post_data.get('comments')
        row_id = post_data.get('id')
        defaults = {
            'code': code,
            'name': name,
            'html_type': html_type,
            'doc_value_type': doc_value_type,
            'comments': comments,
        }

        obj, created = EntryTypeDict.objects.update_or_create(defaults=defaults, id=row_id)
        return JsonResponse({
            'code': STATUS200,
            'msg': 'ok',
            'created': created,
            'id': obj.id
        })
