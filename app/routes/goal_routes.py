from flask import Blueprint, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .helper_methods import validate_model, helper_model_from_dict, helper_get_sorted_query

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")



@bp.post("")
def create_goal():
    request_body = request.get_json()
    return helper_model_from_dict(Goal, request_body, required_fields=["title"])

@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body.get("task_ids", [])
    # goal.tasks.clear()
    for task in goal.tasks:
        task.goal_id = None
    
    for id in task_ids:
        task = validate_model(Task, id)
        task.goal_id = goal.id
        # goal.tasks.append(task)

    db.session.commit()

    return {
        "id": int(goal.id),
        "task_ids": task_ids
    }, 200


@bp.get("")
def get_goals():
    sort_param = request.args.get("sort")
    query = helper_get_sorted_query(Goal, sort_param)
    goals = db.session.execute(query).scalars().all()
    return [goal.to_dict() for goal in goals]

@bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = [task.to_dict() for task in goal.tasks]

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }, 200

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")