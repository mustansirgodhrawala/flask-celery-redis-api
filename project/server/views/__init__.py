# server/views/views.py

# from celery.result import AsyncResult
from flask import render_template, Blueprint, jsonify, request
from project.server import cache

# from server.tasks.tasks import create_task
api_blueprint = Blueprint("api_blueprint", __name__)

from .base import *
from .news import *
from .status import *
