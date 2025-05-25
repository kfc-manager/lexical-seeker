import psycopg2


class Database:
    def __init__(
        self,
        db_host: str,
        db_port: str,
        db_name: str,
        db_user: str,
        db_pass: str,
    ):
        self.conn = psycopg2.connect(
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        )
        self._create_table()

    def close(self):
        self.conn.close()

    def _create_table(self):
        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS article (
                    link TEXT PRIMARY KEY,
                    size INT DEFAULT NULL,
                    file_name VARCHAR(68) DEFAULT NULL
                );
                """
            )

    def _insert(self, query: str, values):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            # propagate exception
            raise e

    def insert_visit(self, link: str):
        self._insert("""INSERT INTO article (link) VALUES (%s);""", (link,))

    def insert_metadata(self, link: str, size: int, file_name: str):
        self._insert(
            """UPDATE article SET size = %s, file_name = %s
            WHERE link = %s;""",
            (str(size), file_name, link),
        )

    def is_visited(self, link: str) -> bool:
        with self.conn.cursor() as cursor:
            cursor.execute(
                """SELECT 1 FROM article WHERE link = %s LIMIT 1;""", (link,)
            )
            return cursor.fetchone() is not None
