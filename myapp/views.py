from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from .models import Task ,Kind
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .serializers import KindsSerializer
from rest_framework.views import APIView
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class TaskCreateView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        task = Task(
            name=data.get('name'),
            current_time=timezone.now(),
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
    
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    data = {
        'task_id': task.task_id,
        'name': task.name,
        'kind': task.kind,
        'importance': task.importance,
        'current_time': task.current_time,
        'due_date': task.due_date,
        'creator': task.creator,
        'assignee': task.assignee,
        'status': task.status,
        
        
        # 他のフィールド...
    }
    return JsonResponse(data)

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