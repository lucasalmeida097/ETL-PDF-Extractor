import os
import psycopg2
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)
logging.basicConfig(level=logging.INFO)


class RDSPostgreSQLManager:
    def __init__(
        self, db_name=None, db_user=None, db_password=None, db_host=None, db_port="5432"
    ):
        if (
            not self.check_environment_variables
            and db_name is None
            and db_user is None
            and db_password is None
            and db_host is None
        ):
            raise ValueError("Bank credentials were not provided.")

        self.db_name = db_name or os.getenv("DB_NAME")
        self.db_user = db_user or os.getenv("DB_USER")
        self.db_password = db_password or os.getenv("DB_PASSWORD")
        self.db_host = db_host or os.getenv("DB_HOST")
        self.db_port = db_port

    def connect(self):
        try:
            connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
            )
            logging.info("Successful connection to PostgreSQL database.")
            return connection
        except psycopg2.Error as e:
            logging.error(f"Error connecting to PostgreSQL database: {e}")
            return None

    def execute_query(self, query):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                connection.commit()
                connection.close()
                return result
            else:
                logging.warning(
                    "Unable to establish connection to the\
                                 database."
                )
                return None
        except psycopg2.Error as e:
            logging.error(f"Error executing SQL query: {e}")
            return None

    def execute_insert(self, query, values):
        try:
            connection = self.connect()
            if connection:
                cursor = connection.cursor()
                cursor.execute(query, values)
                connection.commit()
                cursor.close()
                connection.close()
                logging.info("Data successfully inserted into the database.")
            else:
                logging.warning(
                    "Unable to establish connection to the\
                                 database."
                )
        except psycopg2.Error as e:
            logging.error(f"Error executing SQL insert: {e}")

    @staticmethod
    def check_environment_variables():
        if (
            not os.getenv("DB_NAME")
            or not os.getenv("DB_USER")
            or not os.getenv("DB_PASSWORD")
            or not os.getenv("DB_HOST")
        ):
            logging.warning(
                "The database environment variables are not \
                            configured."
            )
            return False
        else:
            logging.info(
                "Environment variables for the Bank have been \
                         configured correctly."
            )
            return True

    def alchemy(self):
        self.engine = create_engine(
            f"postgresql://{self.db_user}:{self.db_password}@"
            f"{self.db_host}:{self.db_port}/{self.db_name}"
        )

        return self.engine
