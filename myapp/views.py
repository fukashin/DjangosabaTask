from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from .models import Task ,Kind
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .serializers import KindsSerializer,TaskSerializer,TaskDateSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

# まず、ロガーを取得します。これは通常、モジュールのトップレベルで行います。
logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class TaskCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        task = Task(
            name=data.get('name'),
            current_time=data.get('current_time'),
            due_date=data.get('due_date'),
            creator=data.get('creator'),
            assignee=data.get('assignee'),
            status=data.get('status', 'O'),
            kind=data.get('kind'),
            importance=data.get('importance'),
            
            
        )
        task.save()
        return JsonResponse({'message': 'Task created successfully.'})
    
class TaskListView(View):
    def get(self, request, *args, **kwargs):
        tasks = Task.objects.all()
        task_list = list(tasks.values())
        return JsonResponse(task_list, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def task_date_update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        # 例外が発生した場合（つまり、要求されたタスクが存在しない場合）、HTTP 404 Not Foundステータスを返します
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        logger.info('PUT1')
        # タスクデータのシリアライザを作成し、リクエストから得られた新しいデータを使って更新します
        serializer = TaskDateSerializer(task, data=request.data)
        logger.info('PUT2')
        # シリアライザのデータが正しい形式かどうか検証します
        if serializer.is_valid():
            logger.info('PUT3')
            # データが正しい場合、シリアライザを保存（DBに更新を反映）します
            serializer.save()
            # 更新されたタスクデータをHTTPレスポンスとして返します
            return Response(serializer.data)
        # データが不正な場合、HTTP 400 Bad Requestステータスと共にエラー情報を返します
        logger.error(f"Serializer validation error: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# デコレータ 'api_view' は、関数ベースのビューに特定のHTTPメソッド (GET, PUT, DELETE) のみを許可するよう制限を加えます
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, task_id):
    # Taskモデルから主キー(pk)を使って特定のタスクを取得しようとします
    # もし該当のタスクが存在しなければ、Task.DoesNotExist例外が発生します
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        # 例外が発生した場合（つまり、要求されたタスクが存在しない場合）、HTTP 404 Not Foundステータスを返します
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GETリクエストが来た場合（タスクの詳細を取得したい場合）
    if request.method == 'GET':
        # タスクをシリアライズ（Pythonのデータ型からJSONへ変換）します
        serializer = TaskSerializer(task)
        # シリアライズされたタスクデータをHTTPレスポンスとして返します
        return Response(serializer.data)

    # PUTリクエストが来た場合（タスクの詳細を更新したい場合）
    elif request.method == 'PUT':
        logger.info('PUT1')
        # タスクデータのシリアライザを作成し、リクエストから得られた新しいデータを使って更新します
        serializer = TaskSerializer(task, data=request.data)
        logger.info('PUT2')
        # シリアライザのデータが正しい形式かどうか検証します
        if serializer.is_valid():
            logger.info('PUT3')
            # データが正しい場合、シリアライザを保存（DBに更新を反映）します
            serializer.save()
            # 更新されたタスクデータをHTTPレスポンスとして返します
            return Response(serializer.data)
        # データが不正な場合、HTTP 400 Bad Requestステータスと共にエラー情報を返します
        logger.error(f"Serializer validation error: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETEリクエストが来た場合（タスクを削除したい場合）
    elif request.method == 'DELETE':
        # タスクを削除します
        task.delete()
        # HTTP 204 No Contentステータスを返します（削除が成功したことを示します）
        return Response(status=status.HTTP_204_NO_CONTENT)


class KindListView(View):
    def get(self, request, *args, **kwargs):
        kinds = Kind.objects.all()
        kinds_list = [{"value": kind.kind, "label": kind.kind} for kind in kinds]
        return JsonResponse(kinds_list, safe=False)
    
class KindCreateView(APIView):
    def post(self, request):
        # request data should contain the kind kind
        kind = request.data.get('kind')

        # check if the kind with this kind already exists
        if Kind.objects.filter(kind=kind).exists():
            return JsonResponse({'message': 'A kind with this kind already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # if it doesn't exist, create a new kind
        new_kind = Kind(kind=kind)
        new_kind.save()

        # return the newly created kind data
        serializer = KindsSerializer(new_kind)
        return JsonResponse(serializer.data, safe=False)