from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from ..db import db
from .helper_methods import validate_model, helper_model_from_dict

bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    return helper_model_from_dict(Task, request_body)
    
@bp.get("")
def get_all_tasks():
    tasks = db.session.execute(db.select(Task)).scalars()
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

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")