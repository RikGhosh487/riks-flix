import sys
from enum import Enum
from app_init import db
from flask_sqlalchemy.query import Query


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


def parse_exact_filters(request_args, exact_filters) -> dict:
    """
    Parse exact filter parameters from request arguments.

    Args:
        request_args (dict): The request arguments containing filter parameters.
        exact_filters (list): A list of valid fields to filter by.

    Returns:
        dict: A dictionary containing the exact filters.
    """

    filters = dict()
    for filter_field in exact_filters:
        value = request_args.get(filter_field.name)
        if value is not None:
            filters[filter_field] = value

    return filters


def apply_exact_filters(query, filters) -> Query:
    """
    Apply exact filters to a SQLAlchemy query.

    Args:
        query (SQLAlchemy Query): The SQLAlchemy query to apply filters to.
        filters (dict): A dictionary containing the filters to apply.

    Returns:
        SQLAlchemy Query: The modified query with applied filters.
    """
    for field, value in filters.items():
        query = query.filter(field == value)

    return query


def parse_range_filters(request_args, range_filters) -> dict:
    """
    Parse range filter parameters from request arguments.

    Args:
        request_args (dict): The request arguments containing filter parameters.
        range_filters (list): A list of valid fields to filter by.

    Returns:
        dict: A dictionary containing the range filters.
    """
    filters = dict()
    for filter_field in range_filters:
        min_value = request_args.get(f"{filter_field.name}_min")
        max_value = request_args.get(f"{filter_field.name}_max")

        if min_value is not None or max_value is not None:
            filters[filter_field] = (min_value, max_value)

    return filters


def apply_range_filters(query, filters) -> Query:
    """
    Apply range filters to a SQLAlchemy query.

    Args:
        query (SQLAlchemy Query): The SQLAlchemy query to apply filters to.
        filters (dict): A dictionary containing the range filters to apply.

    Returns:
        SQLAlchemy Query: The modified query with applied range filters.
    """
    for field, (min_value, max_value) in filters.items():
        if min_value is not None and max_value is not None:
            query = query.filter(field.between(min_value, max_value))
        elif min_value is not None:
            query = query.filter(field >= min_value)
        elif max_value is not None:
            query = query.filter(field <= max_value)

    return query


def apply_search_filters(query, search_term, search_fields) -> Query:
    """
    Apply search filters to a SQLAlchemy query.

    Args:
        query (SQLAlchemy Query): The SQLAlchemy query to apply search filters to.
        search_term (str): The search term to filter by.
        search_fields (list): A list of valid fields to search by.

    Returns:
        SQLAlchemy Query: The modified query with applied search filters.
    """
    if not search_term:
        return query

    # Apply the search filter to the query
    for field in search_fields:
        query = query.filter(field.ilike(f"%{search_term}%"))

    return query
