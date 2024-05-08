# 使用官方 Python 镜像作为基础镜像
FROM python:3.8

# 设置工作目录
WORKDIR /app

# 复制当前目录下的所有文件到容器的 /app 目录下
COPY . /app

# 安装 OR-Tools 和相关依赖
RUN pip install ortools

# 指定容器启动时要执行的命令
CMD ["python", "test01.py"]
