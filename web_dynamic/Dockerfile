# web_dynamic/Dockerfile
# ベースイメージ
FROM python:3.10

# 必要な依存関係をインストール
RUN apt-get update && \
    apt-get install -y default-jdk python3-dev libffi-dev build-essential openjdk-17-jdk libsqlcipher-dev libsqlite3-dev && \
    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 && \
    export PATH=$PATH:$JAVA_HOME/bin

# pipとCythonをアップグレード
RUN pip install --upgrade pip
RUN pip install Cython==0.29.21

# jniusのインストール（Cythonの後に実行）
RUN pip install pyjnius


# pysqlcipher3のインストール
RUN pip install pysqlcipher3


# 必要に応じて作業ディレクトリを設定
WORKDIR /web_dynamic

COPY ../web_dynamic /web_dynamic
# requirements.txt を親ディレクトリからコピー
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# ポートを公開し、コンテナ起動時のコマンドを設定
EXPOSE 5000
CMD ["python3", "-m", "web_dynamic.hbnb"]
