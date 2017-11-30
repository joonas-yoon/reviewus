from reviewus.db import DBManager as DB


def get_program_list(page=1, nums=20):
    page = max(0, int(page) - 1)
    nums = max(0, int(nums))

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

