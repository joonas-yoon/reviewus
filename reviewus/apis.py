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
    return datetime.strftime(datetime.strptime(date, '%Y년 %m월 %d일'), '"%Y-%m-%d"') if date else 'NULL'

"""
######################################################
#
# PROGRAM
#
######################################################
"""
def get_program_list(page, nums=20):
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
           ORDER BY start_date DESC, title \
           LIMIT %d OFFSET %d' % (int(nums or 20), int(page or 0) * nums)

    programs = DB.execute_and_fetch_all(sql, as_list=True)
    print(programs)
    return programs


def get_program(id):
    id = int(id or 0)

    sql = 'SELECT * FROM ru_program WHERE id = %d' % id
    program = DB.execute_and_fetch(sql, as_row=True)

    if program is None:
        return None

    program['episodes'] = get_episode_list(id)
    return program


def create_program(req):
    query = query_from_request(req)

    print(dict(query))

    data = {
        'title': query.get('title'),
        'content': query.get('content'),
        'broadcast_id': int(query.get('broadcast_id')),
        'genre_id': int(query.get('genre_id')),
        'start_date': parse_date(query.get('start_date')),
        'end_date': parse_date(query.get('end_date'))
    }

    sql = 'INSERT INTO ru_program \
               (title, content, broadcast_id, genre_id, start_date, end_date) \
           VALUES \
               ("{title}", "{content}", {broadcast_id}, \
               {genre_id}, {start_date}, {end_date})'.format(**data)
    
    res = DB.execute(sql, cursor=True)
    newpid = int(res.lastrowid)

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

"""
######################################################
#
# EPISODE
#
######################################################
"""
def get_episode_list(program_id):
    program_id = int(program_id or 0)
    sql = 'SELECT E.*, \
               COUNT(DISTINCT E.id) AS num_episodes \
           FROM \
               ru_program AS P, \
               ru_episode AS E \
           WHERE \
               P.id = %d \
               AND E.program_id = P.id \
           GROUP BY E.id' % program_id

    print(sql)

    return DB.execute_and_fetch_all(sql, as_list=True)


def create_episode(req):
    query = query_from_request(req)

    data = {
        'program_id': int(query.get('program_id')),
        'title': query.get('title'),
        'content': query.get('content') or '',
        'airdate': parse_date(query.get('airdate'))
    }

    print(data)

    sql = 'INSERT INTO ru_episode \
              (program_id, title, content, airdate) \
          VALUES \
              ({program_id}, "{title}", "{content}", {airdate})'.format(**data)

    print(">>>> sql: " + sql)

    res = DB.execute(sql, cursor=True)
    try:
        return res.lastrowid
    except:
        pass
    return None

def get_broadcastsystem_list():
    sql = 'SELECT * FROM ru_broadcast_system'
    return DB.execute_and_fetch_all(sql, as_list=True)

def get_genre_list():
    sql = 'SELECT * FROM ru_genre'
    return DB.execute_and_fetch_all(sql, as_list=True)

