from app.models import UserDb
import mariadb

db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

def insert_user(user: UserDb):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "Insert into users (id, name, username, email, tlf, password) values (?, ?, ?, ?, ?, ?)"
            values = (user.id, user.name, user.username, user.email, user.tlf, user.password)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.lastrowid
    

def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cusor() as cursor:
            sql = "Select id, name, username, email, tlf, password from users where username = ?"
            cursor.execute(sql, (username,))
            result = cursor.fetchone()
            if result:
                return UserDb(
                    id=result[0],
                    name=result[1],
                    username=result[2],
                    email=result[3],
                    tlf=result[4],
                    password=result[5]
                )
            else:
                return None
            
users: list[UserDb] = [
    UserDb(
        id=1,
        name="Alice",
        username="alice",
        email="alice@gmail.com",
        tlf=7658364593,
        password="$2b$12$9DAIvp9W0ls6hY3mE.x.5elr0VsUgOpkFpQ3rp/4XOTPAckgaWztu"
    ),
    UserDb(
        id=2,
        name="Bob",
        username="bob",
        email="alice@gmail.com",
        tlf=7658364593,
        password="$2b$12$qs8F6B3JpINiXDAjhN6cYe9zTuHAE2xoeQ8NNvFtpCzIjg.iFzq3C"
    )
]