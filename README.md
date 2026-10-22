# swe1-app

[![Build Status](https://app.travis-ci.com/DecodeAndCode/swe1-app.svg?branch=main)](https://app.travis-ci.com/DecodeAndCode/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/DecodeAndCode/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/DecodeAndCode/swe1-app?branch=main)

Django polls application (Django tutorial parts 1-4), deployed on AWS Elastic Beanstalk.

## Continuous integration

Travis CI runs on every push and pull request (`.travis.yml`):

1. `black --check .` for code formatting
2. `flake8 .` for linting (`.flake8` sets max line length 88 to match black)
3. `coverage run` over the test suite, reported to Coveralls
4. On success for `main` only, deploys to Elastic Beanstalk

```bash
pip install -r requirements-dev.txt
black --check . && flake8 . && coverage run --source=mysite,polls manage.py test
```

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

Each deploy runs `python manage.py seed_polls`, which creates a sample poll
only when the database is empty. Create an admin with `createsuperuser` over
`eb ssh` to add more polls at `/admin/`.

Add the EB domain to `ALLOWED_HOSTS` in `mysite/settings.py` if it is not
covered by `.elasticbeanstalk.com`. Never commit AWS keys.
