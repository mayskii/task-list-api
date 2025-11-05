from flask import Blueprint, make_response, abort, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model, apply_sorting
from datetime import datetime
from ..db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

# POST one goal
@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

# GET all goals
@bp.get("")
def get_all_goals():

    query = db.select(Goal)
    query = apply_sorting(query, Goal)

    goals = db.session.scalars(query)
    return [goal.to_dict() for goal in goals]

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

# GET tasks for goal
@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }

    return make_response(response_body, 200)

