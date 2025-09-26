# MAINTAINER Chayapan Computing <boss@chayapan.com>
# Version: v0.1
FROM python:3.10-slim

# nslookup, dig
USER root
RUN apt-get update
RUN apt-get install dnsutils --yes --fix-missing
RUN useradd zq1
RUN mkdir -p /app/data /logs /home/zq1
# Make data directory writable
RUN chmod 777 /app/data /logs
RUN chown -R zq1:zq1 /app /home/zq1 /logs
# install app server
RUN apt-get install uwsgi --yes

# Switch to workspace account
# The script aws is installed in '/home/tegan/.local/bin
# Use pipenv to generate requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install pipenv gunicorn
ADD ./Pipfile /app/Pipfile
WORKDIR /app
RUN pipenv clean
RUN pipenv lock
RUN pipenv requirements > /requirements.txt
RUN pip3 install -r /requirements.txt

RUN apt-get install -y curl
USER zq1

# https://linuxize.com/post/how-to-add-directory-to-path-in-linux/
# https://stackoverflow.com/questions/27093612/in-a-dockerfile-how-to-update-path-environment-variable
ENV PATH="/home/zq1/.local/bin:${PATH}"

# Tools: google-oauthlib-tool, django-admin, inv, invoke, aws, unidecode, fab

# The app folder is mounted at /app
EXPOSE 8000

# Dev server
CMD python manage.py runserver 0.0.0.0:8000
# serve django
#   check uwsgi.ini for virtualenv location
#
# CMD uwsgi --ini uwsgi.ini
# CMD ["gunicorn", "kitchen.wsgi:application", "--bind", "0.0.0.0:8000"]