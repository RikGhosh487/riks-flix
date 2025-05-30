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
    """
    Query a single instance by its ID and serialize it using the provided schema.

    Args:
        model (SQLAlchemy Model): The SQLAlchemy model to query.
        id (str): The ID of the instance to query.
        schema (Marshmallow Schema): The schema to serialize the instance.

    Returns:
        dict: A dictionary containing the status and data of the query.
    """
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
    """
    Query a relation of a model by its ID and serialize it using the provided schema.

    Args:
        model (SQLAlchemy Model): The SQLAlchemy model to query.
        id (str): The ID of the instance to query.
        relation_name (str): The name of the relation to fetch.
        relation_schema (Marshmallow Schema): The schema to serialize the relation instances.

    Returns:
        dict: A dictionary containing the status and data of the relation query.
    """
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


def parse_sort_parameters(request_args, sort_fields):
    """
    Parse sorting parameters from request arguments.

    Args:
        request_args (dict): The request arguments containing sorting parameters.
        sort_fields (list): A list of valid fields to sort by.

    Returns:
        SQLAlchemy Sort Expression or None: The sort expression if valid, otherwise None.
    """
    sort_by = request_args.get("sort_by")
    if not sort_by:
        return None

    ascending = request_args.get("ascending", "true").lower() == "true"
    chosen_field = next(filter(lambda field: field.name == sort_by, sort_fields), None)

    if not chosen_field:
        return None

    if ascending:
        return chosen_field.asc()
    return chosen_field.desc()
