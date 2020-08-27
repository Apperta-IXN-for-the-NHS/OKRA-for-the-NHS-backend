from datetime import datetime
from app import Case, db, SearchHistory


# return dictionary format of case info
def get_case_info(case):
    return {'id': case.sys_id if case.sys_id else '',
            'title': case.short_description if case.short_description else '',
            'body': case.content if case.content else '',
            'priority': case.priority if case.priority else 0,
            'date': case.submitted.strftime("%Y-%m-%d") if case.submitted else ''}


# return case by id
def get_case_by_id(case_id):
    res = Case.query.filter_by(sys_id=case_id).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    return get_case_info(res)


# return a list of cases sorted by priority (1 is the highest priority, 4 is the lowest)
# if a request has the query parameter, then search in the db first
def get_cases_sorted_by_date_and_priority(query, limit, start):
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
def add_case_into_db(sys_id, short_description, content, priority, submitted):
    case = Case(sys_id=sys_id, short_description=short_description, content=content, priority=priority, submitted=submitted)
    db.session.add(case)
    db.session.commit()
