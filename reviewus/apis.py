from datetime import datetime
from urllib.parse import urlencode

from reviewus.db import DBManager as DB

from django.http import HttpRequest, QueryDict


def query_from_request(req):
    query = QueryDict()
    if type(req) == type(QueryDict()):
        query = req
    elif type(req) == type(dict()):
        query = QueryDict(urlencode(req))
    else:
        query = QueryDict(req)
    return query


def parse_date(date):
    return datetime.strftime(datetime.strptime(date, '%Y년 %m월 %d일'), '%Y-%m-%d') if date else None

"""
######################################################
#
# PROGRAM
#
######################################################
"""
def get_programs(page=1, nums=20):
    page = max(0, int(page or 1) - 1)
    nums = max(0, int(nums or 20))

    sql = 'SELECT P.*, G.name AS genre_name, B.name AS broad_name, \
               COUNT(E.id) AS num_episodes, \
               AVG(E.avg_star) AS avg_star \
           FROM \
               ru_program AS P, \
               ( \
                 SELECT epi.*, AVG(R.star) AS avg_star \
                 FROM ru_episode AS epi \
                 LEFT JOIN ru_review AS R \
                 ON R.episode_id = epi.id \
                 GROUP BY epi.id \
               ) AS E, \
               ru_genre AS G, ru_broadcast_system AS B \
           WHERE \
               P.broadcast_id = B.id \
                   AND E.program_id = P.id \
                   AND P.genre_id = G.id \
           GROUP BY P.id \
           ORDER BY start_date IS NULL DESC, start_date DESC, end_date IS NULL DESC, end_date DESC, title \
           LIMIT %s OFFSET %s'

    params = (nums, page * nums)

    programs = DB.execute_and_fetch_all(sql, param=params, as_list=True)
    return programs


def get_program(id):
    id = int(id or 0)

    sql = 'SELECT P.*, B.name as broadcast_name, G.name as genre_name \
           FROM \
               ru_program AS P, \
               ru_broadcast_system AS B, \
               ru_genre AS G \
           WHERE \
               P.id = %s \
               AND P.broadcast_id = B.id \
               AND P.genre_id = G.id'
    param = (id)
    program = DB.execute_and_fetch(sql, param=param, as_row=True)

    if not program:
        return None

    program['episodes'] = get_episodes_by_program(id)
    return program


def create_program(req):
    query = query_from_request(req)

    sql = 'INSERT INTO ru_program \
               (title, content, broadcast_id, genre_id, start_date, end_date) \
           VALUES \
               (%s, %s, %s, %s, %s, %s)'
    data = (
        query.get('title'),
        query.get('content'),
        int(query.get('broadcast_id') or 0),
        int(query.get('genre_id') or 0),
        parse_date(query.get('start_date')),
        parse_date(query.get('end_date')),
    )

    print(data)
    
    res = DB.execute(sql, param=data, cursor=True)
    try:
        newpid = int(res.lastrowid)
    except:
        return None

    print("new program id = {}".format(newpid))
    create_episode({
        'program_id': newpid,
        'title': 'ALL'
    })
    try:
        return newpid
    except:
        pass
    return None


def update_program(req, id):
    query = query_from_request(req)

    sql = 'UPDATE ru_program \
           SET title=%s, content=%s, broadcast_id=%s, genre_id=%s, start_date=%s, end_date=%s \
           WHERE id = %s'
    data = (
        query.get('title'),
        query.get('content'),
        int(query.get('broadcast_id') or 0),
        int(query.get('genre_id') or 0),
        parse_date(query.get('start_date')),
        parse_date(query.get('end_date')),
        int(id)
    )

    try:
        res = DB.execute(sql, param=data)

        return id
    except:
        pass

    return None


def delete_program(id):
    sql = 'DELETE FROM ru_program WHERE id = %s'

    try:
        res = DB.execute(sql, param=(id, ))
        return res > 0
    except:
        pass
    return False


"""
######################################################
#
# EPISODE
#
######################################################
"""
def get_episode(id):
    sql = 'SELECT * FROM ru_episode WHERE id = %s'
    return DB.execute_and_fetch(sql, param=(id), as_row=True)


def get_episodes(page=1, nums=10):
    page = max(0, int(page or 1) - 1)
    nums = max(0, int(nums or 10))

    sql = 'SELECT * FROM ru_episode WHERE title != "ALL" ORDER BY airdate IS NULL DESC, airdate DESC LIMIT %s OFFSET %s'

    params = (nums, page * nums)

    return DB.execute_and_fetch_all(sql, param=params, as_list=True)


def get_episodes_by_program(program_id):
    program_id = int(program_id or 0)
    sql = 'SELECT E.*, \
               AVG(R.star) as avg_star, \
               COUNT(R.id) as total_reviews \
           FROM ru_episode AS E \
           LEFT JOIN ru_review AS R \
           ON R.episode_id = E.id \
           WHERE E.program_id = %s \
           GROUP BY E.id \
           ORDER BY airdate IS NULL DESC, airdate DESC'

    return DB.execute_and_fetch_all(sql, param=(program_id), as_list=True)


def create_episode(req):
    query = query_from_request(req)

    sql = 'INSERT INTO ru_episode \
              (program_id, title, content, airdate) \
          VALUES \
              (%s, %s, %s, %s)'

    data = (
        int(query.get('program_id')),
        query.get('title'),
        query.get('content') or '',
        parse_date(query.get('airdate'))
    )

    res = DB.execute(sql, param=data, cursor=True)
    try:
        return res.lastrowid
    except:
        pass
    return None


def update_episode(req, id):
    query = query_from_request(req)

    sql = 'UPDATE ru_episode \
           SET program_id=%s, title=%s, content=%s, airdate=%s \
           WHERE id = %s'
    data = (
        int(query.get('program_id') or 0),
        query.get('title'),
        query.get('content'),
        parse_date(query.get('airdate')),
        int(id)
    )

    try:
        res = DB.execute(sql, param=data)
        return id
    except:
        pass

    return None


def delete_episode(id):
    sql = 'DELETE FROM ru_episode WHERE id = %s'

    try:
        res = DB.execute(sql, param=(id, ))
        return res > 0
    except:
        pass
    return False


def get_episodes_by_person(id=None, name=None):
    sql = 'SELECT \
          PRO.id AS program_id,\
          PRO.title AS program_title,\
          EPI.id AS episode_id,\
          EPI.title AS episode_title,\
          EPI.content AS episode_content,\
          EPI.airdate AS episode_airdate,\
          PER.name AS person_name\
      FROM\
          reviewus.ru_program AS PRO,\
          reviewus.ru_episode AS EPI,\
          reviewus.ru_person AS PER,\
          reviewus.ru_cast AS CA\
      WHERE\
          CA.episode_id = EPI.id AND EPI.program_id = PRO.id AND CA.person_id = PER.id'\

    if id is not None:
        sql += ' AND CA.person_id = %s'
        return DB.execute_and_fetch_all(sql, param=(id), as_list=True)
    else:
        # search by name
        sql += ' AND PER.name like %s'
        search_name = '%' + name + '%'
        return DB.execute_and_fetch_all(sql, param=(search_name), as_list=True)


"""
######################################################
#
# Broadcast System
#
######################################################
"""
def get_broadcastsystems():
    sql = 'SELECT \
        B.id AS broadcast_id,\
        B.name AS broadcast_name,\
        COUNT(P.id) AS program_count\
    FROM\
        ru_broadcast_system AS B\
            LEFT JOIN\
        ru_program AS P ON P.broadcast_id = B.id\
    GROUP BY B.id\
    ORDER BY B.name'

    return DB.execute_and_fetch_all(sql, as_list=True)


def get_broadcastsystem(id):
    sql = 'SELECT \
        B.id AS id,\
        B.name AS name,\
        COUNT(P.id) AS program_count\
    FROM\
        ru_broadcast_system AS B\
            LEFT JOIN\
        ru_program AS P ON P.broadcast_id = B.id\
    WHERE B.id = %s'

    row = DB.execute_and_fetch(sql, param=(id,), as_row=True)
    if not row['id']:
        return None
    return row


def create_broadcastsystem(req):
    query = query_from_request(req)

    sql = 'INSERT INTO ru_broadcast_system (name) VALUES (%s)'
    data = (
        query.get('name')
    )

    res = DB.execute(sql, param=data, cursor=True)
    try:
        return res.lastrowid
    except:
        pass
    return None


def update_broadcastsystem(req, id):
    query = query_from_request(req)

    sql = 'UPDATE ru_broadcast_system \
           SET name = %s \
           WHERE id = %s'
    data = (
        query.get('name') or '',
        int(id or 0)
    )

    try:
        res = DB.execute(sql, param=data)
        return id
    except:
        pass

    return None


def delete_broadcastsystem(id):
    sql = 'DELETE FROM ru_broadcast_system WHERE id = %s'

    try:
        res = DB.execute(sql, param=(id, ))
        return res > 0
    except:
        pass
    return False


"""
######################################################
#
# Genre
#
######################################################
"""
def get_genres():
    sql = 'SELECT * FROM ru_genre ORDER BY name'
    return DB.execute_and_fetch_all(sql, as_list=True)


def get_genre(id):
    sql = 'SELECT * FROM ru_genre WHERE id = %s'
    return DB.execute_and_fetch(sql, param=(id, ), as_row=True)


"""
######################################################
#
# Person
#
######################################################
"""
def get_people():
    sql = 'SELECT * FROM ru_person ORDER BY name'
    return DB.execute_and_fetch_all(sql, as_list=True)


def get_person(id):
    sql = 'SELECT * FROM ru_person WHERE id = %s'
    return DB.execute_and_fetch(sql, param=(id, ), as_row=True)


def get_people_by_name(name):
    sql = 'SELECT * FROM ru_person WHERE name like %s'
    return DB.execute_and_fetch_all(sql, param=('%' + name + '%'), as_list=True)


"""
######################################################
#
# Job
#
######################################################
"""
def get_jobs():
    sql = 'SELECT * FROM ru_job ORDER BY name'
    return DB.execute_and_fetch_all(sql, as_list=True)


def get_job(id):
    sql = 'SELECT * FROM ru_job WHERE id = %s'
    return DB.execute_and_fetch(sql, param=(id, ), as_row=True)


"""
######################################################
#
# Cast
#
######################################################
"""
def get_casts():
    sql = 'SELECT E.id as episode_id, \
               E.program_id, E.title, E.content, \
               P.id as person_id, P.name \
           FROM \
               ru_cast AS C, \
               ru_episode AS E, \
               ru_person AS P \
           WHERE \
               C.episode_id = E.id AND C.person_id = P.id'
    return DB.execute_and_fetch_all(sql, as_list=True)


def get_casts_by_episode(id):
    sql = ''
    return DB.execute_and_fetch_all(sql, param=(id,), as_list=True)


def get_casts_by_program(id):
    sql = ''
    return DB.execute_and_fetch_all(sql, param=(id,), as_list=True)

