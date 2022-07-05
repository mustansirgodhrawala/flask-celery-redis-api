from . import api_blueprint
from project.server import celery

@api_blueprint.route("/api/status",methods=["GET"])
@api_blueprint.route("/api/status/<task_id>",methods=["GET"])
def status(task_id=None):
	if not task_id:
		return {"Message":"Please supply a task_id at /api/status/<task_id> to get the result."}
	else:
		task_result = celery.AsyncResult(task_id)
		result = {
			"task_id": task_id,
			"task_status": task_result.status,
			"task_result": task_result.result,
		}
		return result