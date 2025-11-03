from flask import Blueprint, make_response, abort, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model
from datetime import datetime
from ..db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# POST one goal
@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(new_goal.to_dict(), 201)

# GET all goals
@bp.get("")
def get_all_goals():

    query = db.select(Goal)

    sort_order = request.args.get("sort")

    if sort_order == "asc":
        query = query.order_by(Goal.title.asc())
    elif sort_order == "desc":
        query = query.order_by(Goal.title.desc())
    else:
        query = query.order_by(Goal.id)

    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response

# GET obe goal
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return make_response(goal.to_dict(), 200)

# PUT one goal
@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


# DELETE one goal
@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

# CREATE connected tasks to goal
@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        tasks.append(task)
    goal.tasks = tasks
    
    db.session.commit()

    return make_response({"id": goal.id, "task_ids": task_ids}, 200)