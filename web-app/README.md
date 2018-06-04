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