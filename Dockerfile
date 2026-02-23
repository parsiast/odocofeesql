FROM python:3.12-bookworm


WORKDIR /app

RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]

