import os
from abcpet_project.wsgi import application

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abcpet_project.settings')
    port = int(os.environ.get('PORT', '8000'))
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])
