# MAINTAINER Chayapan Computing <boss@chayapan.com>
# Version: v0.1
FROM python:3.10-slim

USER root
# Install required system packages in one layer
# dnsutils: for nslookup, dig
# uwsgi: optional for production serving
# RUN apt-get update && apt-get install -y --no-install-recommends \
#         dnsutils \
#         uwsgi \
#         curl \
#     && rm -rf /var/lib/apt/lists/*



RUN useradd zq1
RUN mkdir -p /app/data /logs /home/zq1
# Make data directory writable
RUN chmod 777 /app/data /logs
RUN chown -R zq1:zq1 /app /home/zq1 /logs

# Switch to workspace account
# The script aws is installed in '/home/tegan/.local/bin
# Use pipenv to generate requirements.txt
RUN pip3 install --upgrade pip
COPY ./favlinks/requirements.txt /tmp/requirements.txt
WORKDIR /app
RUN pip3 install -r /tmp/requirements.txt

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
