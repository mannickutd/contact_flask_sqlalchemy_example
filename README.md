# contact_flask_sqlalchemy_example


## Install
```
pyenv virtualenv contact_flask_sqlalchemy_example
pyenv activate contact_flask_sqlalchemy_example
pip install -r test_requirements.txt
```

## Run tests
```
py.test tests
```

## Run development server
```
python app.py runserver 
```

## Run celery worker
```
celery -A celery_worker.celery worker
```

## Run celery beat
```
celery -A celery_worker.celery beat
```
