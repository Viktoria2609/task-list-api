from flask import abort,make_response
from sqlalchemy import asc, desc
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"{cls.__name__} id {model_id} is invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} with id {model_id} not found"}
        abort(make_response(response, 404))

    return model

def helper_model_from_dict(cls, request_body):
    required_fields = ["title", "description"]
    for field in required_fields:
        if field not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))

    new_instance = cls.from_dict(request_body)
    
    db.session.add(new_instance)
    db.session.commit()

    return {"task": new_instance.to_dict()}, 201

def helper_get_sorted_query(cls, sort_param):
    if sort_param == "asc":
        return db.select(cls).order_by(asc(cls.title))
    elif sort_param == "desc":
        return db.select(cls).order_by(desc(cls.title))
    return db.select(cls)