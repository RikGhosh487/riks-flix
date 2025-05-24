import sys
from app_init import db
from enum import Enum


class Status(Enum):
    SUCCESS = {"status": "success", "code": 200}
    FAIL = {"status": "fail", "code": 400}
    ERROR = {"status": "error", "code": 500}
    NOT_FOUND = {"status": "fail", "code": 404}


def query_pages(query, schema) -> dict:
    # make a SQL query
    try:
        results = db.paginate(query, per_page=100)
        instances = schema.dump(results.items, many=True)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {**Status.ERROR.value, "message": "data fetch failed"}

    return {
        **Status.SUCCESS.value,
        "data": {"instances": instances, "total": results.total},
    }


def query_by_id(model, id, schema) -> dict:
    try:
        int_id = int(id)
        instance = schema.dump(model.query.get(int_id))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {**Status.FAIL.value, "message": "invalid id"}

    if not instance:
        return {**Status.NOT_FOUND.value, "message": "not found"}

    return {**Status.SUCCESS.value, "data": {"instance": instance}}


def query_relations_by_id(model, id, relation_name, relation_schema) -> dict:
    try:
        int_id = int(id)
        instance = model.query.get(int_id)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {**Status.FAIL.value, "message": "invalid id"}

    if not instance:
        return {**Status.NOT_FOUND.value, "message": "not found"}

    try:
        relation = getattr(instance, relation_name)
        instances = relation_schema.dump(relation, many=True)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {**Status.FAIL.value, "message": "relation fetch failed"}

    return {
        **Status.SUCCESS.value,
        "data": {relation_name: instances},
    }
