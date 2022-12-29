import os
import sys
from django.core.management import execute_from_command_line
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
current_dir = os.path.dirname(os.path.realpath(__file__))
execute_from_command_line(sys.argv)
