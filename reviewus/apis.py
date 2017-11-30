from datetime import datetime

from reviewus.db import DBManager as DB

from django.http import HttpRequest, QueryDict


def get_program_list(page, nums):
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

    sql = 'SELECT E.*, \
               COUNT(DISTINCT E.id) AS num_episodes, \
               AVG(R.star) AS avg_star \
           FROM \
               ru_program AS P, \
               ru_episode AS E, \
               ru_review AS R \
           WHERE \
               P.id = %d \
               AND E.program_id = P.id \
                   AND R.episode_id = E.id \
           GROUP BY E.id' % id
    program['episodes'] = DB.execute_and_fetch_all(sql, as_list=True)

    return program


def create_program(req):
    query = QueryDict()
    if type(req) == type(QueryDict()):
        query = req
    else:
        try:
          query = QueryDict(req)
        except:
            return None

    def parse_date(date):
        return datetime.strftime(datetime.strptime(date, '%Y년 %m월 %d일'), '%Y-%m-%d') if date else 'NULL'

    print(dict(query))

    try:
        data = {
            'title': query.get('title'),
            'content': query.get('content'),
            'broadcast_id': int(query.get('broadcast_id')),
            'genre_id': int(query.get('genre_id')),
            'start_date': parse_date(query.get('start_date')),
            'end_date': parse_date(query.get('end_date'))
        }

        print(data)

        sql = 'INSERT INTO ru_program \
                   (title, content, broadcast_id, genre_id, start_date, end_date) \
               VALUES \
                   ("{title}", "{content}", {broadcast_id}, \
                   {genre_id}, "{start_date}", "{end_date}")'.format(**data)

        print(sql)
        res = DB.execute(sql, cursor=True)
        try:
            return res.lastrowid
        except:
            print("...except...!!")
            return None

    except:
        return None


def get_broadcastsystem_list():
    sql = 'SELECT * FROM ru_broadcast_system'
    return DB.execute_and_fetch_all(sql, as_list=True)

def get_genre_list():
    sql = 'SELECT * FROM ru_genre'
    return DB.execute_and_fetch_all(sql, as_list=True)

