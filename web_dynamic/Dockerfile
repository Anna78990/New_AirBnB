# ベースイメージ
FROM python:3.10

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y default-jdk python3-dev libffi-dev build-essential openjdk-17-jdk libsqlcipher-dev libsqlite3-dev && \
    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 && \
    export PATH=$PATH:$JAVA_HOME/bin

# pip と Cython をアップグレード
RUN pip install --upgrade pip
RUN pip install Cython==0.29.21

# jnius と pysqlcipher3 のインストール
RUN pip install pyjnius
RUN pip install pysqlcipher3

WORKDIR /New_AirBnB/web_dynamic
# 作業ディレクトリを設定

# requirements.txt と Web Dynamic コードをコピー
COPY ./requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

COPY ./web_dynamic /New_AirBnB/web_dynamic
# ポートを公開
EXPOSE 5000

# アプリケーションの実行コマンド
CMD ["python3", "-m", "web_dynamic.hbnb"]
