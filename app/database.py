import datetime
import sqlite3
import random
import json
from typing import Optional

from app.config import use_case_dict


# creates the db tables. Gets called when there is no existing DB
def create_db_tables(con: sqlite3.Connection):
    con.execute("""
        CREATE TABLE
            use_cases
            (user_id TEXT, use_case_id SMALLINT, use_case_step SMALLINT, user_emotion JSON, datetime TIMESTAMP WITH TIME ZONE, PRIMARY KEY (user_id, use_case_id, use_case_step));
    """)

    con.execute("""
        CREATE TABLE
            emails
            (user_id TEXT PRIMARY KEY, email TEXT);
    """)

    con.execute("""
        CREATE TABLE
            comments
            (user_id TEXT PRIMARY KEY, comment TEXT);
    """)


# get a use case the user hasn't done before with a random use case step. A user is done with a use case once he has done one of the steps
def get_use_case(con: sqlite3.Connection, user_id: str) -> Optional[dict]:
    cur = con.cursor()

    # get use cases for user and their completion status
    select_sql = """
        SELECT 
            use_case_id
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
        # check both steps if any has been completed.
        if use_case_id not in user_use_case_completion_status:
            # add both steps to the to_do list where one gets randomly chosen at the end
            for i in range(1, 3):
                to_do_use_cases.append({
                    "use_case_id": use_case_id,
                    "use_case_step": i,
                })

    # return a random use case
    return random.choice(to_do_use_cases) if to_do_use_cases else None


# returns the number of use cases the user has fully completed
def get_number_of_completed_use_cases(con: sqlite3.Connection, user_id: str) -> int:
    cur = con.cursor()

    select_sql = """
        SELECT 
            COUNT(use_case_id)
        FROM
            use_cases
        WHERE 
            user_id = ?
            AND NOT use_case_id = 0;    
    """
    cur.execute(select_sql, (user_id, ))
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
            (?, ?, ?, ?, ?)
        ON 
            CONFLICT 
        DO 
            NOTHING;
    """
    cur.execute(insert_sql, (user_id, use_case_id, use_case_step, json.dumps(user_emotion), time, ))
    con.commit()


# inserts a users email, or changes it
def update_email(con: sqlite3.Connection, user_id: str, email: str) -> None:
    cur = con.cursor()

    insert_sql = """
        INSERT INTO 
            emails 
            (user_id, email)
        VALUES
            (?, ?)        
        ON 
            CONFLICT 
                (user_id)
        DO 
            UPDATE SET
                email = ?;
    """
    cur.execute(insert_sql, (user_id, email, email, ))
    con.commit()


# inserts a users comment, or changes it
def update_comment(con: sqlite3.Connection, user_id: str, comment: str) -> None:
    cur = con.cursor()

    insert_sql = """
        INSERT INTO 
            comments 
            (user_id, comment)
        VALUES
            (?, ?)        
        ON 
            CONFLICT 
                (user_id)
        DO 
            UPDATE SET
                comment = comment || " UPDATED WITH: " || ?;
    """
    cur.execute(insert_sql, (user_id, comment, comment,))
    con.commit()
