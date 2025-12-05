from app.models import UserDb
import mariadb
from app.models import UserDb

users: list[UserDb] = [
    UserDb(id=1, name="alice", username="alice", email="juan@gmail.com", tlf=687678899, password="$2b$12$CUgVgUwbXO9EuBm2FbTLie2aY/blRe6zuT0bEP40gL8NTSz3YYv.2")
]

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
            
    

def get_user_by_username(username: str) -> UserDb | None:
    with mariadb.connect(**db_config) as conn:
        with conn.cusor() as cursor:
            cursor.execute(insert_user,(3, "jose","jose","jose@gmail.com",356764567,"jose"))
            
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