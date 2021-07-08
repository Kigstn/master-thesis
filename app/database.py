import datetime
import os
import sqlite3
import json
from typing import Optional

from app.config import use_case_dict


class Database:
    con: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, db_name: str):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

        # add tables to db if first start
        if not os.path.isfile(db_name):
            self._create_db_tables()

    # creates the db tables. Gets called when there is no existing DB
    def _create_db_tables(self):
        self.con.execute("""
            CREATE TABLE
                use_cases
                (user_id TEXT, use_case_id SMALLINT, use_case_step SMALLINT, user_emotion JSON, datetime TIMESTAMP WITH TIME ZONE, PRIMARY KEY (user_id, use_case_id, use_case_step));
        """)

        self.con.execute("""
            CREATE TABLE
                emails
                (user_id TEXT PRIMARY KEY, email TEXT);
        """)

        self.con.execute("""
            CREATE TABLE
                comments
                (user_id TEXT PRIMARY KEY, comment TEXT);
        """)

    # gets the user count for each use case
    def _get_use_case_count(self) -> dict:
        select_sql = """
            SELECT 
                use_case_id, use_case_step
            FROM 
                use_cases
            WHERE
                use_case_id != 0;
        """
        self.cur.execute(select_sql)
        use_case_completion_status = self.cur.fetchall()

        # prepare return dict
        status = {}
        for use_case in use_case_dict:
            status.update({
                use_case: {}
            })
            for use_case_step in range(1, 3):
                status[use_case].update({
                    use_case_step: 0
                })

        # fill return dict
        for use_case_completion in use_case_completion_status:
            status[use_case_completion[0]][use_case_completion[1]] += 1

        return status

    # get a use case if the user hasn't done one before
    def get_use_case(self, user_id: str) -> Optional[dict]:
        # get the number of completed use cases
        user_use_case_completed = self.get_number_of_completed_use_cases(user_id)

        # check if user has done one already. Remember: use case 0 (user data) counts too
        if user_use_case_completed > 1:
            return None

        # get the number of completed use cases and completed steps to balance them
        use_case_completion_status = self._get_use_case_count()

        # get the use case with the lowest completion
        lowest_use_case_completions = sorted({i: sum([k for k in j.values()]) for i, j in use_case_completion_status.items()}.items(), key=lambda item: item[1])[0][0]

        # get the use case step with the lowest completion
        lowest_use_case_step_completions = sorted(use_case_completion_status[lowest_use_case_completions].items(), key=lambda item: item[1])[0][0]

        # return this info as a dict
        return {
            "use_case_id": lowest_use_case_completions,
            "use_case_step": lowest_use_case_step_completions,
        }

    # returns the number of use cases the user has completed including the demographic survey
    def get_number_of_completed_use_cases(self, user_id: str) -> int:
        select_sql = """
            SELECT 
                COUNT(use_case_id)
            FROM
                use_cases
            WHERE 
                user_id = ?;    
        """
        self.cur.execute(select_sql, (user_id, ))
        return self.cur.fetchone()[0]

    # checks if the user has completed a single use case step
    def user_is_new(self, user_id: str) -> bool:
        # get use cases for user and their completion status
        select_sql = """
            SELECT 
                *
            FROM 
                use_cases
            WHERE 
                user_id = ?;
        """
        self.cur.execute(select_sql, (user_id, ))
        return not bool(self.cur.fetchone())

    # inserts a user and their use case status into the DB
    def update_db_user(self, user_id: str, use_case_id: int, use_case_step: int, user_emotion: dict, time: datetime.datetime) -> None:
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
        self.cur.execute(insert_sql, (user_id, use_case_id, use_case_step, json.dumps(user_emotion), time, ))
        self.con.commit()

    # inserts a users email, or changes it
    def update_email(self, user_id: str, email: str) -> None:
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
        self.cur.execute(insert_sql, (user_id, email, email, ))
        self.con.commit()

    # inserts a users comment, or changes it
    def update_comment(self, user_id: str, comment: str) -> None:
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
        self.cur.execute(insert_sql, (user_id, comment, comment,))
        self.con.commit()

    # closes the DB
    def close(self) -> None:
        self.con.close()
