from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
import logging

logger = logging.getLogger(__name__)
class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)  # タスク名
    kind = models.CharField(max_length=20)  # タスクの種類
    current_time = models.DateTimeField()  # 開始予定日
    due_date = models.DateTimeField()  # 終了予定日
    creator = models.CharField(max_length=200)  # タスク作成者
    assignee = models.CharField(max_length=200)  # タスク実行者
    STATUS_CHOICES = [
        ('O', 'Open'),  # オープン
        ('C', 'Closed'),  # クローズ
    ]
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='O',
    )  # ステータス（デフォルトはオープン）

    # 重要度を追加します。
    IMPORTANCE_CHOICES = [
        ('3', '大'),  # 大
        ('2', '中'),  # 中
        ('1', '小'),  # 小
    ]
    importance = models.CharField(
        max_length=1,
        choices=IMPORTANCE_CHOICES,
        default='2',  # デフォルトは中
    )
    
class Comment(models.Model): 
    comment_id = models.AutoField(primary_key=True)  # 自動でインクリメントされる主キー
    comment_number =models.IntegerField(default=0)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')  # スレッドへの外部キー参照
    content = models.TextField()  # コメントの内容
    user_id = models.CharField(max_length=255)  # ユーザーID
    createdAt = models.DateTimeField(null=True, auto_now_add=True)  # コメントが作成された日時

    class Meta:
        unique_together = ('task_id', 'comment_number')  # スレッドIDとコメントIDの組み合わせを一意にする
        

    
    
    

    def __str__(self):
        return self.name
#python manage.py makemigrations
#python manage.py migrate
#python manage.py runserver


# カスタムユーザーマネージャ
class CustomUserManager(BaseUserManager):
    # 通常のユーザーを作成するメソッド
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        logger.info(f"Before creating user model instance: email={email}, username={username}, extra_fields={extra_fields}")
        user = self.model(email=email, username=username, **extra_fields)
        logger.info(f"Before setting password: user={user}")
        user.set_password(password)
        logger.info(f"Before saving user: user={user}")
        user.save(using=self._db)
        return user

    # スーパーユーザーを作成するメソッド
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

# カスタムユーザーモデル
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # 一意のメールアドレス
    username = models.CharField(max_length=30, unique=True)  # 一意のユーザー名
    is_active = models.BooleanField(default=True)  # ユーザーがアクティブかどうか
    is_staff = models.BooleanField(default=False)  # ユーザーがスタッフかどうか
    
    groups = models.ManyToManyField(Group, related_name='+')
    user_permissions = models.ManyToManyField(Permission, related_name='+')

    objects = CustomUserManager()  # カスタムユーザーマネージャを設定

    USERNAME_FIELD = 'email'  # ユーザー名フィールドをメールアドレスに設定
    REQUIRED_FIELDS = ['username']  # 必須フィールド

    def __str__(self):
        return self.email
    
    
class Kind(models.Model):
    kind = models.CharField(max_length=20)
