# 必要なモジュールをインポートします
from rest_framework import viewsets
from .models import Task  # データベースモデルをインポート
from .serializers import TaskSerializer  # データシリアライズを行うためのクラスをインポート
import logging

logger = logging.getLogger(__name__)

# TaskViewSetは、Taskモデルに対するCRUD（Create, Read, Update, Delete）操作を提供するためのViewクラスです
class TaskViewSet(viewsets.ModelViewSet):
    # TaskSerializerをこのViewに関連付けて、データのシリアライズ（PythonオブジェクトをJSONなどに変換）と
    # デシリアライズ（JSONなどをPythonオブジェクトに変換）を行います
    serializer_class = TaskSerializer
    
    # get_querysetメソッドは、このViewで表示するデータのリストを取得するためのメソッドです
    def get_queryset(self):
        # まず、すべてのTaskオブジェクトを取得します
        queryset = Task.objects.all()
        
        # 次に、リクエストからクエリパラメータ'sort_by'の値を取得します。
        # クエリパラメータはURLの一部で、'?sort_by=value'のような形式で指定します。
        # ここでは、'sort_by'パラメータが指定されていない場合はデフォルトのNoneを設定しています
        sort_by = self.request.query_params.get('sort_by', None)
        
        logger.info('sort_by')

        # もし'sort_by'パラメータが指定されているなら（Noneではないなら）、その値に基づいてquerysetをソートします
        if sort_by is not None:
            queryset = queryset.order_by(sort_by)
            
        # 最後に、ソートされた（もしくは元の）querysetを返します
        return queryset
