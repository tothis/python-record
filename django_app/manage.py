#!/usr/bin/env python
import os
import sys


def main():
    # 设置环境变量DJANGO_SETTINGS_MODULE=Social_networking_sites.settings 即django项目settings.py所在路径
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # 运行项目 python manage.py runserver
    main()
