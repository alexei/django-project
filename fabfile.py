from fabric.api import run
from fabric.operations import prompt

import json
import os
import random

def backdrop():
    config = {}

    project_name = prompt('Project name: ', default='{{ project_name }}')

    config['DEBUG'] = True

    secret_key = prompt('Secret key: ', default=_random_string(50))
    config['SECRET_KEY'] = secret_key

    print 'Database settings:'
    database_ids = ['mysql', 'pgsql', 'sqlite']
    database_default_id = 'sqlite'
    database_type = prompt('Type (%s): ' % ', '.join(database_ids), default=database_default_id, validate=lambda database_id: database_id if database_id in database_ids else database_default_id)
    if database_type is not database_default_id:
        database_engines = {
            'mysql': 'django.db.backends.mysql',
            'pgsql': 'django.db.backends.postgresql_psycopg2',
        }
        database_engine = database_engines[database_type]
        database_host = prompt('Host: ', default='localhost')
        database_ports = {
            'mysql': '3306',
            'pgsql': '5432',
        }
        database_port = prompt('Port:', default=database_ports[database_type])
        database_name = prompt('Name: ', default='{{ project_name }}')
        database_username = prompt('Username: ', default=database_name)
        database_password = prompt('Password: ', default=_random_string(16))
        config['DATABASES'] = {
            'default': {
                'ENGINE': database_engine,
                'NAME': database_name,
                'USER': database_username,
                'PASSWORD': database_password,
                'HOST': database_host,
                'PORT': database_port,
            }
        }

    home_dir = os.path.expanduser('~')
    file_name = "%s.json" % project_name
    file_path = os.path.join(home_dir, '.backdrop', file_name)
    file = open(file_path, 'w+')
    json.dump(config, file, indent=4)
    file.close()

def _random_string(length):
    return ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(length)])
