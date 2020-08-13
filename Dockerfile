ARG CODE_VERSION=3.7.4
FROM python:${CODE_VERSION}

# Set environment variables
ENV PYTHONUNBUFFERED 1
# setting default value for build_env
ARG build_env=local 
ENV ENV_Setting=$build_env

COPY requirements.txt /

# Install dependencies.
RUN pip install --no-cache-dir -r /requirements.txt

# Set work directory.
RUN mkdir /code
WORKDIR /code

# Copy project code.
COPY . /code/

# RUN python manage.py makemigrations && python manage.py migrate

# CMD export ENV_Setting=development && python manage.py makemigrations && python manage.py migrate && python manage.py runserver
