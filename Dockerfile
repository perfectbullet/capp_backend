FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install -Ur requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple &&  \
    pip cache purge

COPY . /code/
