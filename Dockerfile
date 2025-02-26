# 使用官方 Python 基础镜像
FROM python:3.6-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .

ENV PIP_INDEX_URL=https://mirrors.tencent.com/pypi/simple
ENV PIP_TRUSTED_HOST=mirrors.tencent.com
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器中
COPY . .

# 声明容器暴露的端口（与 Python 应用监听的端口一致）
EXPOSE 8080

# 启动命令
CMD ["python", "app.py"]