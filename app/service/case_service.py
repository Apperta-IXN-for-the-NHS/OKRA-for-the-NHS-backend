from app import Case


def get_case_info(case):
    return {'id': case.sys_id if case.sys_id else '',
            'title': case.short_description if case.short_description else '',
            'body': case.content if case.content else '',
            'priority': case.priority if case.priority else 0,
            'date': case.opened.strftime("%Y-%m-%d") if case.opened else ''}


def get_case_by_id(case_id):
    res = Case.query.filter_by(sys_id=case_id).first()

    # if not exist, return empty dictionary
    if res is None:
        return {}

    return get_case_info(res)


def get_cases_sorted_by_priority(query, limit, start):
    if query is None:
        res = Case.query.order_by(Case.priority, Case.opened.desc(), Case.sys_id).offset(start).limit(limit)
    else:
        res = Case.query.filter(Case.short_description.ilike(f"%{query}%")).order_by(Case.priority, Case.opened.desc(), Case.sys_id).offset(start).limit(limit)
    return [get_case_info(case) for case in res]
