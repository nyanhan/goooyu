A fancy RSS Reader.

## Framework and Enviroment

1. Python2.7
1. Flask on Google Appengine
1. Jinja2

## Install and Run

#### Install Python dependencies
```shell
pip install -r requirements_dev.txt
```

#### Generate secret key for CSRF and session
```shell
python application/generate_keys.py
```
This python script will create a <tt>secret_keys.py</tt> file in <tt>application</tt>:

```python
# CSRF- and Session keys

CSRF_SECRET_KEY = 'random key'
SESSION_KEY = 'random key'
```

#### Run
To preview the application using App Engine's development server, use <tt>dev_appserver.py</tt>

```shell
sh scripts/start.sh
```

Assuming the latest App Engine SDK is installed, the test environment is available at http://localhost:8080

## Deploy
Use <tt>scripts/update.sh</tt> to deploy projects onto Google appengine:
```shell
sh scripts/update.sh
```
Then, you can access http://goooyu-alfa.appspot.com for preview.
