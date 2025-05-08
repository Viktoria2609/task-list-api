from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from datetime import datetime
import os
import requests
from ..db import db
from .helper_methods import validate_model, helper_model_from_dict, helper_get_sorted_query

bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return helper_model_from_dict(Task, request_body)
    
@bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort") 
    query = helper_get_sorted_query(Task, sort_param)
    tasks = db.session.execute(query).scalars()
    task_list = [task.to_dict() for task in tasks]
    return task_list

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task": task.to_dict()}

@bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    slack_token = os.environ.get("SLACKBOT_TOKEN")
    if slack_token:
        slack_message = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
        headers = {
            "Authorization": f"Bearer {slack_token}",
            "Content-type": "application/json"
        }
        requests.post("https://slack.com/api/chat.postMessage", json=slack_message, headers=headers)
    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")