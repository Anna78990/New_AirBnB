# ベースイメージ
FROM python:3.10

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y default-jdk python3-dev libffi-dev build-essential libsqlcipher-dev && \
    export JDK_HOME=/usr/lib/jvm/java-17-openjdk-amd64 && \
    export PATH=$PATH:$JDK_HOME/bin

# 作業ディレクトリを設定
WORKDIR /New_AirBnB/api

# 依存関係をインストール
RUN pip install --upgrade pip
RUN pip install Cython==0.29.21
RUN pip install --no-cache-dir -r requirements.txt

COPY ./requirements.txt .

COPY ./api /New_AirBnB/api
# ポートを公開
EXPOSE 5001

# アプリケーションの実行コマンド
CMD ["python3", "-m", "api.v1.app"]
