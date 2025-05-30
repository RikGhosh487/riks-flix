import sys
from enum import Enum
from app_init import db


class Pagination:
    def __init__(self, page, per_page) -> None:
        self.page = page
        self.per_page = per_page


class Status(Enum):
    SUCCESS = {"status": "success", "code": 200}
    FAIL = {"status": "fail", "code": 400}
    ERROR = {"status": "error", "code": 500}
    NOT_FOUND = {"status": "fail", "code": 404}


def query_pages(query, schema, pagination: Pagination) -> dict:
    """
    Paginate a SQLAlchemy query and serialize the results using the provided schema.

    Args:
        query (SQLAlchemy Query): The SQLAlchemy query to paginate.
        schema (Marshmallow Schema): The schema to serialize the results.
        pagination (Pagination): An instance of Pagination containing page and per_page values.

    Returns:
        dict: A dictionary containing the status and paginated data.
    """
    # make a SQL query
    try:
        results = db.paginate(query, page=pagination.page, per_page=pagination.per_page)
        instances = schema.dump(results.items, many=True)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return {**Status.ERROR.value, "message": "data fetch failed"}

    return {
        **Status.SUCCESS.value,
        "data": {
            "instances": instances,
            "total": results.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
        },
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


def parse_pagination_parameters(request_args) -> Pagination:
    """
    Parse pagination parameters from request arguments.

    Args:
        request_args (dict): The request arguments containing pagination parameters.

    Returns:
        Pagination: An instance of Pagination with parsed page and per_page values.
    """
    page = int(request_args.get("page", 1))
    per_page = int(request_args.get("per_page", 10))

    return Pagination(page, per_page)
