import datetime
import sqlite3
import random
import json

from config import use_case_dict


# creates the db tables. Gets called when there is no existing DB
def create_db_tables(con: sqlite3.Connection):
    con.execute("""
        CREATE TABLE
            use_cases
            (user_id TEXT, use_case_id SMALLINT, use_case_step SMALLINT, user_emotion JSON, datetime TIMESTAMP WITH TIME ZONE, PRIMARY KEY (user_id, use_case_id, use_case_step));
    """)


# get a use case the user hasn't done before and the use case step
def get_use_case(con: sqlite3.Connection, user_id: str) -> dict:
    cur = con.cursor()

    # get use cases for user and their completion status
    select_sql = """
        SELECT 
            use_case_id, use_case_step
        FROM 
            use_cases
        WHERE 
            user_id = ?;
    """
    cur.execute(select_sql, (user_id, ))
    user_use_case_completion_status = cur.fetchall()

    # loop through the available use cases and compare them
    to_do_use_cases = []
    for use_case_id, use_case_description in use_case_dict.items():
        # check if use case has been (at least partially) completed by the user
        if (use_case_id, 1) not in user_use_case_completion_status:
            to_do_use_cases.append({
                "use_case_id": use_case_id,
                "use_case_step": 1,
            })

        # if it has been (at least partially) completed by the user, check if the second part has also been completed. If not, that one has high priority and need to be done first
        elif (use_case_id, 2) not in user_use_case_completion_status:
            return {
                "use_case_id": use_case_id,
                "use_case_step": 2,
            }

    # return a random use case
    return random.choice(to_do_use_cases)


# returns the number of use cases the user has fully completed
def get_number_of_completed_use_cases(con: sqlite3.Connection, user_id: str) -> int:
    cur = con.cursor()

    select_sql = """
        SELECT 
            COUNT(t1.use_case_id)
        FROM (
            SELECT
                use_case_id
            FROM
                use_cases
            WHERE 
                user_id = ?
                AND use_case_step = 1
        ) as t1
        JOIN (
            SELECT
                use_case_id
            FROM
                use_cases
            WHERE 
                user_id = ?
                AND use_case_step = 2
        ) as t2
        ON (
            t1.use_case_id = t2.use_case_id
        );    
    """
    cur.execute(select_sql, (user_id, user_id, ))
    return cur.fetchone()[0]


# checks if the user has completed a single use case step
def user_is_new(con: sqlite3.Connection, user_id: str) -> bool:
    cur = con.cursor()

    # get use cases for user and their completion status
    select_sql = """
        SELECT 
            *
        FROM 
            use_cases
        WHERE 
            user_id = ?;
    """
    cur.execute(select_sql, (user_id, ))
    return not bool(cur.fetchone())


# inserts a user and their use case status into the DB
def update_db_user(con: sqlite3.Connection, user_id: str, use_case_id: int, use_case_step: int, user_emotion: dict, time: datetime.datetime) -> None:
    cur = con.cursor()

    insert_sql = """
        INSERT INTO 
            use_cases 
            (user_id, use_case_id, use_case_step, user_emotion, datetime)
        VALUES
            (?, ?, ?, ?, ?);
    """
    cur.execute(insert_sql, (user_id, use_case_id, use_case_step, json.dumps(user_emotion), time, ))
    con.commit()

