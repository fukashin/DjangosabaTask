# Pythonベースのイメージを使用
FROM python:3.10

# ワーキングディレクトリを設定
WORKDIR /usr/src/app

# 環境変数を設定
#要なディスクスペースを消費する可能性があるため、この環境変数を設定して生成を抑制します
ENV PYTHONDONTWRITEBYTECODE 1
#バッファリングを無効にすることでログメッセージがリアルタイムに見えるようになります
ENV PYTHONUNBUFFERED 1

# 依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースをコピー
COPY . .

# ポートのエクスポーズ
EXPOSE 8000

# コンテナ起動時のコマンド
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
