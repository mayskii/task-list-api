from flask import Blueprint, make_response, abort, request, Response
from app.models.task import Task
from ..db import db

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_dict(), 201)
