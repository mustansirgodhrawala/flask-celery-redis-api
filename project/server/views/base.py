from . import api_blueprint

@api_blueprint.route("/",methods=["GET"])
def index():
	return 'Base Endpoint.'