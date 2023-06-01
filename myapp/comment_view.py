# RESTフレームワークのジェネリッククラスをインポートします
# これらは一般的なビュー操作（リスト作成、詳細取得、作成、更新、削除など）をサポートします
from rest_framework import generics 

import logging
logger = logging.getLogger(__name__)
# Commentモデルをインポートします。これはコメントデータのDB構造を定義します
from .models import  Comment 

# CommentSerializerをインポートします。これはモデルインスタンスをJSONなどの形式に変換（シリアライズ）したり、その逆の操作を行うためのクラスです
from .serializers import CommentSerializer 

# コメントを作成するための関数
def create_comment(task_id, content, user_id):
    logger.info("処理開始")
    # まず、特定のタスクに関連する最新のコメントを取得します
    last_comment = Comment.objects.filter(task_id=task_id).order_by('-comment_number').first()
    logger.info("最新コメ取得")
    
    # 新しいコメントナンバーを計算します。これは最新のコメントナンバー+1か、もしそのタスクにまだコメントがない場合は1とします
    new_comment_number = last_comment.comment_number + 1 if last_comment else 1
    logger.info("最新コメ生成")

    # 新しいコメントオブジェクトを作成し、DBに保存します
    new_comment = Comment(comment_number=new_comment_number, task_id_id=task_id, content=content, user_id=user_id)
    new_comment.save()
    logger.info("最新コメ保存")

    # 作成したコメントオブジェクトを返します
    return new_comment



# コメントの一覧を取得・作成するためのビュークラス
class CommentListCreateAPIView(generics.ListCreateAPIView):
    logger.info("処理開始1")
    # 全てのコメントをデフォルトのクエリセットとして設定します
    queryset = Comment.objects.all() 
    logger.info("処理開始1")

    # Commentモデルをシリアライズするクラスを設定します
    serializer_class = CommentSerializer 
    logger.info("処理開始2")

    # クエリセットを特定のタスクのコメントに絞り込むための関数
    def get_queryset(self):
        logger.info("処理開始3")
        # リクエストからタスクIDを取得します。これを元にコメントを絞り込みます
        task_id = self.request.query_params.get('taskid', None)
        logger.info("処理開始4")
        if task_id:
            return Comment.objects.filter(task_id=task_id) # タスクIDがある場合はそのタスクのコメントだけを返します
        return Comment.objects.all() # タスクIDがない場合は全てのコメントを返します

    # コメントを作成するための関数をオーバーライドします
    def perform_create(self, serializer):
        logger.info("処理開始4")
        task_id = self.request.data.get('task_id')  # リクエストからタスクIDを取得します
        content = self.request.data.get('content')  # リクエストからコメントの内容を取得します
        user_id = self.request.data.get('user_id')  # ユーザーIDを取得します
        create_comment(task_id, content,user_id)  # 上で定義したcreate_comment関数を使ってコメントを作成します

# コメントの詳細を取得・更新・削除するためのビュークラス
class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # 全てのコメントをデフォルトのクエリセットとして設定します
    queryset = Comment.objects.all() 

    # Commentモデルをシリアライズするクラスを設定します
    serializer_class = CommentSerializer 
