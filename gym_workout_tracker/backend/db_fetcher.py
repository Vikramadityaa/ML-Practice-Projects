import mysql.connector
from contextlib import contextmanager
from logger import setup_logger

logger = setup_logger('db_fetcher')

@contextmanager
def db_cursor(commit=False):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='workout_base',
    )
    cursor = connection.cursor(dictionary=True)
    yield cursor
    if commit:
        cursor.execute("COMMIT")
    cursor.close()
    connection.close()

def fetch_workout_info_from_db(w_name):
    logger.info('fetching from db: {}'.format( w_name))
    with db_cursor() as cursor:
        cursor.execute("select * from daily_workout where workout_name = '{}'  order by workout_date desc limit 5".format(w_name))
        workout_info = cursor.fetchall()
        return workout_info

def delete_workout_for_date(workout_date, workout_name):
    logger.info("delete from db '{}', '{}'".format(workout_date, workout_name))
    with db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM daily_workout WHERE workout_date = %s and workout_name = %s", (workout_date,workout_name))

def insert_workout_for_date(workout_date, workout_name="No Workout", repetitions = 0, max_weight=0.0):
    logger.info('inserting into db: {} {}'.format( workout_name, workout_date))
    with db_cursor(commit=True) as cursor:
        cursor.execute("Insert Into workout_base.daily_workout (workout_name, repetitions, max_weight, workout_date) VALUES (%s, %s, %s, %s)",
                       (workout_name, repetitions, max_weight, workout_date)
                       )
if __name__ == '__main__':
    # insert_workout_for_date('2025-03-19','Curl', '10', '12.5')
    print(fetch_workout_info_from_db('Curl'))
    # delete_workout_for_date('2025-10-10', 'curl')



