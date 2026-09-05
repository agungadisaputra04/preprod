from database import get_connection


def create_user(nama: str, umur: int, connection_factory=get_connection):
    with connection_factory() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (nama, umur)
                VALUES (%s, %s)
                RETURNING id, nama, umur;
                """,
                (nama, umur)
            )
            return cur.fetchone()


def get_users(connection_factory=get_connection):
    with connection_factory() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nama, umur
                FROM users
                ORDER BY id;
                """
            )
            return cur.fetchall()


def get_user_by_id(user_id: int, connection_factory=get_connection):
    with connection_factory() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nama, umur
                FROM users
                WHERE id = %s;
                """,
                (user_id,)
            )
            return cur.fetchone()


def update_user(
    user_id: int,
    nama: str,
    umur: int,
    connection_factory=get_connection
):
    with connection_factory() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET nama = %s,
                    umur = %s
                WHERE id = %s
                RETURNING id, nama, umur;
                """,
                (nama, umur, user_id)
            )
            return cur.fetchone()


def patch_user(
    user_id: int,
    nama: str | None,
    umur: int | None,
    connection_factory=get_connection
):
    with connection_factory() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET nama = COALESCE(%s, nama),
                    umur = COALESCE(%s, umur)
                WHERE id = %s
                RETURNING id, nama, umur;
                """,
                (nama, umur, user_id)
            )
            return cur.fetchone()


def delete_user(user_id: int, connection_factory=get_connection):
    with connection_factory() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM users
                WHERE id = %s
                RETURNING id, nama, umur;
                """,
                (user_id,)
            )
            return cur.fetchone()
