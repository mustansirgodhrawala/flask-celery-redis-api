from . import api_blueprint

@api_blueprint.route("/api",methods=["GET"])
def index():
	return 'Base Endpoint.'