# urls.py
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import  TaskCreateView ,task_detail,KindListView,KindCreateView
from .sort_views import TaskViewSet
from .comment_view import CommentListCreateAPIView ,CommentRetrieveUpdateDestroyAPIView
from . import user_views
router = DefaultRouter()
router.register(r'update-info', TaskViewSet, basename='task')

urlpatterns = [
    path('tasks/', TaskCreateView.as_view(), name='create_task'),
    path('', include(router.urls)),
    path('comments/', CommentListCreateAPIView.as_view(), name='comment_list_create_api'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment_retrieve_update_destroy_api'),
    path('tasks/<int:task_id>', task_detail, name='task_detail'),
    path('signup/', user_views.signup, name='signup'),
    path('signin/', user_views.signin, name='signin'),
    path('user_info/', user_views.get_user_info, name='user_info'),
    path('kinds/',KindListView.as_view() ,name='get_kind'),
    path('kinds_create/', KindCreateView.as_view(), name='create_kind'),
]
