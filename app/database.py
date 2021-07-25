import datetime
import os
import asyncpg

from typing import Optional
from app.config import use_case_dict, experiment_steps


class Database:
    connection: asyncpg.Connection

    async def init(self):
        args = {
            "database": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "password": os.environ.get("POSTGRES_PASSWORD"),
            "host": os.environ.get("POSTGRES_HOST"),
        }

        self.connection = await asyncpg.connect(**args)

        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS 
                use_cases
                (user_id TEXT, use_case_id SMALLINT, use_case_step SMALLINT, user_emotion_before_response TEXT, user_emotion_reason_before_response TEXT, user_emotion_after_response TEXT, user_emotion_reason_after_response TEXT, datetime TIMESTAMP WITH TIME ZONE, PRIMARY KEY (user_id, use_case_id, use_case_step));
        """)

        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS 
                emails
                (user_id TEXT PRIMARY KEY, email TEXT);
        """)

        await self.connection.execute("""
            CREATE TABLE IF NOT EXISTS 
                comments
                (user_id TEXT PRIMARY KEY, comment TEXT);
        """)

    # gets the user count for each use case
    async def _get_use_case_count(self) -> dict:
        select_sql = """
            SELECT 
                use_case_id, use_case_step
            FROM 
                use_cases
            WHERE
                use_case_id != 0
                AND use_case_id != -1;
        """
        use_case_completion_status = await self.connection.fetch(select_sql)

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
            status[use_case_completion["use_case_id"]][use_case_completion["use_case_step"]] += 1

        return status

    # get a use case if the user hasn't done one before
    async def get_use_case(self, user_id: str) -> Optional[dict]:
        # get the number of completed use cases
        user_use_case_completed = await self.get_number_of_completed_use_cases(user_id)

        # check if user has done one already. Remember: use case 0 (user data) counts too
        if user_use_case_completed > 1:
            return None

        # get the number of completed use cases and completed steps to balance them
        use_case_completion_status = await self._get_use_case_count()

        # get the use case with the lowest completion
        lowest_use_case_completions = sorted({i: sum([k for k in j.values()]) for i, j in use_case_completion_status.items()}.items(), key=lambda item: item[1])[0][0]

        # get the use case step with the lowest completion
        lowest_use_case_step_completions = sorted(use_case_completion_status[lowest_use_case_completions].items(), key=lambda item: item[1])[0][0]

        # return this info as a dict
        return {
            "use_case_id": lowest_use_case_completions,
            "use_case_step": lowest_use_case_step_completions,
        }

    # gets the in-progress use case
    async def get_in_progress_use_case(self, user_id: str) -> Optional[asyncpg.Record]:
        select_sql = """
            SELECT 
                use_case_id, use_case_step
            FROM 
                use_cases
            WHERE
                user_id = $1
                AND use_case_id != 0
                AND use_case_id != -1;
        """
        return await self.connection.fetchrow(select_sql, user_id)

    # returns the number of use cases the user has completed including the demographic survey
    async def get_number_of_completed_use_cases(self, user_id: str) -> int:
        select_sql = """
            SELECT 
                COUNT(use_case_id)
            FROM
                use_cases
            WHERE 
                user_id = $1;    
        """
        return await self.connection.fetchval(select_sql, user_id)

    # checks if the user has completed a single use case step
    async def user_is_new(self, user_id: str) -> bool:
        # get use cases for user and their completion status
        select_sql = """
            SELECT 
                *
            FROM 
                use_cases
            WHERE 
                user_id = $1;
        """
        return not bool(await self.connection.fetchval(select_sql, user_id))

    # checks if the user is done
    async def user_is_done(self, user_id: str) -> bool:
        # get use cases for user and their completion status
        select_sql = """
            SELECT 
                *
            FROM 
                use_cases
            WHERE 
                user_id = $1;
        """
        return bool(len(await self.connection.fetch(select_sql, user_id)) >= experiment_steps)

    # inserts a user and their use case status into the DB
    async def update_db_user(self, user_id: str, use_case_id: int, use_case_step: int, time: datetime.datetime, user_emotion_before_response: str = None, user_emotion_reason_before_response: str = None, user_emotion_after_response: str = None, user_emotion_reason_after_response: str = None) -> None:
        insert_sql = """
            INSERT INTO 
                use_cases 
                (user_id, use_case_id, use_case_step, user_emotion_before_response, user_emotion_reason_before_response, user_emotion_after_response, user_emotion_reason_after_response, datetime)
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8)
            ON 
                CONFLICT (user_id, use_case_id, use_case_step)
            DO UPDATE
                SET
                    user_emotion_after_response = $6
                    AND user_emotion_reason_after_response = $7;
        """
        await self.connection.execute(insert_sql, user_id, use_case_id, use_case_step, user_emotion_before_response, user_emotion_reason_before_response, user_emotion_after_response, user_emotion_reason_after_response, time)

    # inserts a users email, or changes it
    async def update_email(self, user_id: str, email: str) -> None:
        insert_sql = """
            INSERT INTO 
                emails 
                (user_id, email)
            VALUES
                ($1, $2)        
            ON 
                CONFLICT 
                    (user_id)
            DO UPDATE 
                SET
                    email = $2;
        """
        await self.connection.execute(insert_sql, user_id, email)

    # inserts a users comment, or changes it
    async def update_comment(self, user_id: str, comment: str) -> None:
        insert_sql = """
            INSERT INTO 
                comments 
                (user_id, comment)
            VALUES
                ($1, $2)        
            ON 
                CONFLICT 
                    (user_id)
            DO UPDATE 
                SET
                    comment = CONCAT(comments.comment, ' UPDATED WITH: ', $2);
        """
        await self.connection.execute(insert_sql, user_id, comment)

    # closes the DB
    async def close(self) -> None:
        await self.connection.close()


# helper function to get the DB class
async def get_db() -> Database:
    db = Database()
    await db.init()
    return db
