# swe1-app

Django polls application (Django tutorial parts 1-4), deployed on AWS Elastic Beanstalk.

## Run locally

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # then add questions at /admin/
python manage.py runserver         # http://127.0.0.1:8000/polls/
python manage.py test polls
```

## Deploy to Elastic Beanstalk

```bash
eb init          # pick a Python 3.11+ platform, region, and set up SSH
eb create swe1-app-env
eb deploy        # after any later change (commit first)
eb open          # then visit /polls/
```

Add the EB domain to `ALLOWED_HOSTS` in `mysite/settings.py` if it is not
covered by `.elasticbeanstalk.com`. Never commit AWS keys.
