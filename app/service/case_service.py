from app import Case, db


# return dictionary format of case info
def get_case_info(case):
    return {'id': case.sys_id if case.sys_id else '',
            'title': case.short_description if case.short_description else '',
            'body': case.content if case.content else '',
            'priority': case.priority if case.priority else 0,
            'date': case.opened.strftime("%Y-%m-%d") if case.opened else ''}


# return case by id
def get_case_by_id(case_id):
    res = Case.query.filter_by(sys_id=case_id).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    return get_case_info(res)


# return a list of cases sorted by priority (1 is the highest priority, 4 is the lowest)
# if a request has the query parameter, then search in the db first
def get_cases_sorted_by_priority(query, limit, start):
    if query is None:
        res = Case.query.order_by(Case.priority, Case.opened.desc(), Case.sys_id).offset(start).limit(limit)
    else:
        res = Case.query.filter(Case.short_description.ilike(f"%{query}%")).order_by(Case.priority, Case.opened.desc(), Case.sys_id).offset(start).limit(limit)
    return [get_case_info(case) for case in res]


# add a case to the db with the info provided in a request
def add_case_into_db(sys_id, short_description, content, priority, opened):
    case = Case(sys_id=sys_id, short_description=short_description, content=content, priority=priority, opened=opened)
    db.session.add(case)
    db.session.commit()