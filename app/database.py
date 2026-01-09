from app.models import UserDb
import mariadb
from app.models import UserDb


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
            
    
def get_all():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, name, username, email, tlf, password FROM users "
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            users = []
            for row in rows:    
                user = UserDb(
                    id = row[0],
                    name=row[1],
                    username = row[2],
                    email = row[3],
                    tlf = row[4],
                    password = row[5]
                )
                
                users.append(user)
                
            return users
        
        
def get_by_id(id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, name, username, email, tlf, password FROM users WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row is None:
                return None
            
            user = UserDb(
                id = row[0],
                username = row[1],
                name=row[2],
                email = row[3],
                tlf = row[4],
                password = row[5]
            )
            return user
        
        
def delete_user_by_id(id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount
           

def get_user_by_username(username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, name, username, email, tlf, password FROM users WHERE username = ?"
            values = (username,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row is None:
                return None
            
            user = UserDb(
                id = row[0],
                username = row[1],
                name=row[2],
                email = row[3],
                tlf = row[4],
                password = row[5]
            )
            return user
        

def modify_user(id:int, name:str = None, username:str = None, email:str = None, tlf:str = None, password:str = None):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            
            sql = "SELECT id, name, username, email, tlf, password FROM users WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row is None:
                return None
            
            new_name = name if name is not None else row[1]
            new_username = username if username is not None else row[2]
            new_email = email if email is not None else row[3]
            new_tlf = tlf if tlf is not None else row[4]
            new_password = password if password is not None else row[5]
            
            sql = "UPDATE users SET username = ?, name = ?, email = ?, tlf = ?, password = ? WHERE id = ?"
            values = (new_username, new_name, new_email, new_tlf, new_password, id)
            cursor.execute(sql, values)
            
            user = UserDb(
                id = id,
                username = new_username,
                name=new_name,
                email = new_email,
                tlf = new_tlf,
                password = new_password
            )
            return user
            
                  
#users: list[UserDb] = [UserDb(id=1,name="Alice",username="alice",email="alice@gmail.com",tlf=7658364593,password="$2b$12$9DAIvp9W0ls6hY3mE.x.5elr0VsUgOpkFpQ3rp/4XOTPAckgaWztu"),UserDb(id=2,name="Bob",username="bob",email="alice@gmail.com",tlf=7658364593,password="$2b$12$qs8F6B3JpINiXDAjhN6cYe9zTuHAE2xoeQ8NNvFtpCzIjg.iFzq3C")]
#users: list[UserDb] = [UserDb(id=1, name="alice", username="alice", email="juan@gmail.com", tlf=687678899, password="$2b$12$CUgVgUwbXO9EuBm2FbTLie2aY/blRe6zuT0bEP40gL8NTSz3YYv.2")]