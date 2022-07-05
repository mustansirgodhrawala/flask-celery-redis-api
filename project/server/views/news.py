from project.server.views import api_blueprint
from . import cache
import time
from project.server.tasks.crawler import crawler_func
from flask import jsonify
	
@api_blueprint.route("/api/news/<ticker>", methods=["GET"])
@api_blueprint.route("/api/news", methods=["GET"])
@cache.cached(timeout=180, query_string=True)
def news(ticker=None):
	if not ticker:
		return {"Message":"News Endpoint will trigger task, supply ticker in this fashion /news/<ticker>"},200
	else:
		task = crawler_func.delay(ticker)
		return jsonify({
			"Message":"Task Accepted",
			"Task_Id":task.id,
			"Status":"Status will be available at api/status/<taskid>"
		})	