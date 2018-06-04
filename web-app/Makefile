# https://github.com/ruddra/docker-django/blob/master/Makefile

build:
	docker-compose build

up:
	docker-compose up -d

up-non-daemon:
	docker-compose up

start:
	docker-compose start

stop:
	docker-compose stop

restart:
	docker-compose stop && docker-compose start

shell-nginx:
	docker exec -ti ng01 bash

shell-web:
	docker exec -ti dg01 bash

shell-db:
	docker exec -ti ps01 bash

log-nginx:
	docker-compose logs nginx

log-web:
	docker-compose logs web

log-db:
	docker-compose logs db

collectstatic:
	docker exec dz01 /bin/sh -c "python manage.py collectstatic --noinput"

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate