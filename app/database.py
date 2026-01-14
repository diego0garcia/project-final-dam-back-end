from app.models import UserDb
import mariadb
from app.models import UserDb, UserIn


db_config = {
    "host": "myapidb",
    "port": 3306,
    "user": "myapi",
    "password": "myapi",
    "database": "myapi"
}

def check_if_exists(username:str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id FROM usuario WHERE username = ?"
            values = (username,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            
            if not row:
                return False
            
            return True
    
def get_id():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT count(*) FROM usuario"
            cursor.execute(sql,)
            rows = cursor.fetchone()
            
            return rows[0]

def insert_user(user: UserIn):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "Insert into usuario (dni, username, password, nombre, email, tlf) values (?, ?, ?, ?, ?, ?)"
            values = (user.dni, user.username, user.password, user.name, user.email, user.tlf)
            cursor.execute(sql, values)
            conn.commit()
            
    
def get_all():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM usuario"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            users = []
            for row in rows:    
                user = UserDb(
                    id = row[0],
                    dni = row[1],
                    username = row[2],
                    password = row[3],
                    name=row[4],
                    email = row[5],
                    tlf = row[6]
                )
                users.append(user)
                
            return users
        
        
def get_by_id(id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, dni, username, password, nombre, email, tlf FROM usuario WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row is None:
                return None
            
            user = UserDb(
                id = row[0],
                dni = row[1],
                username = row[2],
                password = row[3],
                name=row[4],
                email = row[5],
                tlf = row[6]
            )
            return user
        
        
def delete_user_by_id(id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM usuario WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount
           

def get_user_by_username(username: str):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM usuario WHERE username = ?"
            values = (username,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row is None:
                return None
            
            user = UserDb(
                id = row[0],
                dni = row[1],
                username = row[2],
                password = row[3],
                name=row[4],
                email = row[5],
                tlf = row[6]
            )
            return user
        

def modify_user(id:int, dni:str = None, name:str = None, username:str = None, email:str = None, tlf:int = None, password:str = None):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            
            sql = "SELECT * FROM usuario WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            
            if row is None: return None
            
            new_dni = dni if dni is not None else row[0]
            new_username = username if username is not None else row[1]
            new_password = password if password is not None else row[2]
            new_name = name if name is not None else row[3]
            new_email = email if email is not None else row[4]
            new_tlf = tlf if tlf is not None else row[5]
            
            sql = "UPDATE usuario SET dni = ?, username = ?, password = ?, nombre = ?, email = ?, tlf = ? WHERE id = ?"
            values = (new_dni, new_username, new_password, new_name, new_email, new_tlf, id)
            cursor.execute(sql, values)
            conn.commit()
            
            return get_by_id(id)
            
                  
#users: list[UserDb] = [UserDb(id=1,name="Alice",username="alice",email="alice@gmail.com",tlf=7658364593,password="$2b$12$9DAIvp9W0ls6hY3mE.x.5elr0VsUgOpkFpQ3rp/4XOTPAckgaWztu"),UserDb(id=2,name="Bob",username="bob",email="alice@gmail.com",tlf=7658364593,password="$2b$12$qs8F6B3JpINiXDAjhN6cYe9zTuHAE2xoeQ8NNvFtpCzIjg.iFzq3C")]
#users: list[UserDb] = [UserDb(id=1, name="alice", username="alice", email="juan@gmail.com", tlf=687678899, password="$2b$12$CUgVgUwbXO9EuBm2FbTLie2aY/blRe6zuT0bEP40gL8NTSz3YYv.2")]