#!/bin/bash

# System housekeeping
pip3 install -r /config/requirements.pip
/etc/init.d/postgresql start & sleep 5s

# Django Housekeeping
su - postgres -c 'psql -f /home/django/init.sql'  # Create db and user
python3 /home/django/manage.py makemigrations
python3 /home/django/manage.py migrate
echo yes | python3 /home/django/manage.py collectstatic
echo "from authentication.models import User; User.objects.create_superuser('admin', 'Admin', 'Admin', 'admin@example.com', ';Hv=2mJQ3;K@ZtgmU3')" | python3 /home/django/manage.py shell
python3 /home/django/manage.py loaddata /home/django/authentication/fixtures/*.json  # Fixtures
python3 /home/django/manage.py loaddata /home/django/portal/fixtures/*.json
/etc/init.d/postgresql stop

# Bring it up
/usr/bin/supervisord -n
