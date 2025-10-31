from flask import Blueprint, make_response, abort, request, Response
from app.models.task import Task
from .route_utilities import validate_model
from ..db import db

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


# POST one task
@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_dict(), 201)

# GET all tasks
@bp.get("")
def get_all_tasks():

    query = db.select(Task)

    sort_order = request.args.get("sort")

    if sort_order == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_order == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

# GET obe task
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response(task.to_dict(), 200)

# PUT one task
@bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at", None)

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# DELETE one task
@bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")