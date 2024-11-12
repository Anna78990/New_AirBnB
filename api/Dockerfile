# api/Dockerfile
FROM python:3.10

# 必要な依存関係のインストール
RUN apt-get update && \
    apt-get install -y default-jdk python3-dev libffi-dev build-essential && \
    export JDK_HOME=/usr/lib/jvm/java-17-openjdk-amd64 && \
    export PATH=$PATH:$JDK_HOME/bin

# JDK_HOME 環境変数の設定
ENV JDK_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# 作業ディレクトリを設定
WORKDIR /api

# requirements.txt と API コードをコピー
COPY ../requirements.txt .
COPY ../api /api

# 依存関係のインストール
RUN pip install Cython
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["python3", "-m", "api.v1.app"]

