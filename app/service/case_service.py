"""
This is the module providing services for cases.
"""
import uuid
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from app import Case, db, SearchHistory


def get_case_info(case: Case) -> dict:
    """Get case info according to the given Case object.

    :param case: a Case object
    :return: a dict of case info
    """
    return {'id': case.sys_id if case.sys_id else '',
            'title': case.short_description if case.short_description else '',
            'body': case.content if case.content else '',
            'priority': case.priority if case.priority else 0,
            'date': case.submitted.strftime("%Y-%m-%d") if case.submitted else ''}


def get_case_by_id(case_id: str) -> dict:
    """Get the info of the case with the specified id

    :param case_id: the id of a Case object
    :return: a dict of case info
    """
    res = Case.query.filter_by(sys_id=case_id).limit(1).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    return get_case_info(res)


def get_cases_sorted_by_date_and_priority(query: str, limit: int, start: int) -> list:
    """Get a list of case info sorted by date and priority.
    
    For priority, 1 is the highest priority, 4 is the lowest.
    If a request has the query parameter, then search in the db first.

    :param query: search query
    :param limit: number of returned cases
    :param start: start index
    :return: a list of case info
    """
    if query is None:
        res = Case.query.order_by(Case.submitted.desc(), Case.priority, Case.sys_id).offset(start).limit(limit)
    else:
        # save query
        history = SearchHistory(type="case", content=query, search_date=datetime.now())
        db.session.add(history)
        db.session.commit()

        res = Case.query.filter(Case.short_description.ilike(f"%{query}%")).order_by(Case.submitted.desc(), Case.priority, Case.sys_id).offset(start).limit(limit)
    return [get_case_info(case) for case in res]


# add a case to the db with the info provided in a request
def add_new_case(short_description: str, content: str, priority: int) -> bool:
    """Add a new case.

    :param short_description: case title
    :param content: case content
    :param priority: case priority
    :return: True for success, False for failure
    """
    sys_id = uuid.uuid4().hex
    submitted = date.today()
    try:
        case = Case(sys_id=sys_id, short_description=short_description, content=content, priority=priority, submitted=submitted)
        db.session.add(case)
        db.session.commit()
        return True
    except IntegrityError:
        return False
