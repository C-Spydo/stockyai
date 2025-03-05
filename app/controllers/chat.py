from . import routes_blueprint
from ..services import chat
from flask import request
# from flask_parameter_validation import ValidateParameters, Query
from typing import Optional
from ..error_handler import url_validation_error_handler
from ..helpers import create_response
from ..constants import SUCCESS_MESSAGE
from ..enums import CustomStatusCode
from flask_restx import Api, Resource

api = Api(routes_blueprint, doc="/swagger/")

@routes_blueprint.route('/start-chat', methods=['POST'])
def start_chat():
    response = chat.start_chat(request.get_json())
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, response), 200

@routes_blueprint.route('/prompt', methods=['POST'])
def prompt_bot():
    response = chat.prompt_bot(request.get_json())
    return create_response(CustomStatusCode.SUCCESS.value, SUCCESS_MESSAGE, response), 200


@routes_blueprint.route('/ping', methods=['GET'])
@api.doc()
def ping():
    return create_response(CustomStatusCode.SUCCESS.value, "API is Awake"), 200
