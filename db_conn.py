import psycopg2
import settings


class QueryDbCommit:

    def __tuple_greate(self, cursor):
        try:
            answer = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            list_answer = []
            for i in range(len(answer)):
                dict_ = dict(zip(column_names, answer[i]))
                list_answer.append(dict_)

            return list_answer
        except:
            pass

    def run_query(self, query, func_tuple: object = __tuple_greate):
        cursor = self.connect.cursor()
        cursor.execute(query)
        list_answer = func_tuple(cursor)
        self.connect.commit()
        if list_answer:
            return list_answer


class DBConnect(QueryDbCommit):
    def __init__(self):
        self.connect = psycopg2.connect(
            database=settings.DATA_BASE['database'],
            user=settings.DATA_BASE['user'],
            password=settings.DATA_BASE['password'],
            host=settings.DATA_BASE['host'],
            port=settings.DATA_BASE['port'],
        )



