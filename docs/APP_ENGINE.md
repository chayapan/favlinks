Main documentation
1. https://cloud.google.com/appengine/docs/standard/python3/runtime
2. https://cloud.google.com/python/django/appengine

See this example Django configuration
3. 
  https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/standard/django
  https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/appengine/standard_python3/django


Reference for the YAML configuration
4. https://cloud.google.com/appengine/docs/standard/reference/app-yaml?tab=python

See notes on migrating to Python 3 environment
5. https://cloud.google.com/appengine/migration-center/standard/migrate-to-second-gen/python-differences

Specify dependency in requirements.txt
6. https://cloud.google.com/appengine/docs/standard/python3/specifying-dependencies

```
pipenv requirements > favlinks/requirements.txt
```

By default, App Engine caches fetched dependencies to reduce build times. To install an uncached version of the dependency, use the command:

```
gcloud app deploy --no-cache
```

Check running status
```
gcloud app logs tail -s default
```

Browse the app
```
gcloud app services browse default
```


Manage firewall
```
gcloud app firewall-rules list
```


```
# [START django_app]
runtime: python27
api_version: 1
threadsafe: yes

handlers:
- url: /static
  static_dir: static/
- url: .*
  script: mysite.wsgi.application

# Only pure Python libraries can be vendored
# Python libraries that use C extensions can
# only be included if they are part of the App Engine SDK 
# Using Third Party Libraries: https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27
libraries:
- name: MySQLdb
  version: 1.2.5
# [END django_app]

# Google App Engine limits application deployments to 10,000 uploaded files per
# version. The skip_files section allows us to skip virtual environment files
# to meet this requirement. The first 5 are the default regular expressions to
# skip, while the last one is for all env/ files.
skip_files:
- ^(.*/)?#.*#$
- ^(.*/)?.*~$
- ^(.*/)?.*\.py[co]$
- ^(.*/)?.*/RCS/.*$
- ^(.*/)?\..*$
- ^env/.*$
```
