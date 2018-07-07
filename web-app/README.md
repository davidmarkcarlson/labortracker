# Labor-Tracker-Med
Labor Tracker Team Med



# Using the Application

## Creating a practitioner

## Creating a patient

## Creating a partograph

## Adding partograph data

# Deploying the Application

`docker-compose build`

`docker-compose up -d`

`docker-compose start`

## Single Production Dockerfile

In `docker-compose.yml` there is an entry for `prod` which references Dockerfile Dockerfile-Prod.  

Dockerfile-Prod pulls in a base Ubuntu 16.04 image and installs required packages. It copies all source code to /home/django and configuration to /config. Finally it exposes port 80 and executes the `./config/start.sh` shellscript. This shell script creates the database, runs the migrations, collects static files, and creates a superuser. 

This process was based on: https://github.com/chenjr0719/Docker-Django-Nginx-Postgres

## Multiple Dockerfiles

This process based on: http://ruddra.com/2016/08/14/docker-django-nginx-postgres/

### Force Push!

## Local Development Setup (without docker)

1. Install Postgres - https://www.postgresql.org/download/

2. Install latest version of Python 3

3. Create virtual environment (optional) - http://docs.python-guide.org/en/latest/dev/virtualenvs/

4. From web-app directory, run:
	
    ```
    pip install -r config\requirements.pip
    ```
    
5. Open settings.py in src\LaborTracker

6. Update Databases section to match local postres installation:
	
    ```
	DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'postgres',
          'USER': 'postgres',
          'PASSWORD': 'postgres',
          'HOST': '127.0.0.1',
          'PORT': 5432,
      }
  	}
    ```

7. Create superuser

	```
    python manage.py createsuperuser
    ```
    
8. From src directory, run:

	python manage.py migrate
    
    python manage.py runserver
    
 9. Application should be accessible at http://127.0.0.1:8000 for main app and http://127.0.0.1:8000/admin for admin app