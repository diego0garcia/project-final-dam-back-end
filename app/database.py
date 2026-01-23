from app.models import UserDb
from app.notification import NotificationIn, NotificationOut
import mariadb
from app.models import UserDb, UserIn
from app.notification import NotificationDb, NotificationIn


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
            
#--------------------------------NOTIFICATIONS-------------------------------------#

    
def get_id():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT count(*) FROM notificacion"
            cursor.execute(sql,)
            rows = cursor.fetchone()
            
            return rows[0]

def insert_notification(notification: NotificationIn):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "Insert into notificacion (nia_alumno, dni_usuario, descripcion, hora) values (?, ?, ?, ?)"
            values = (notification.nia_alumno, notification.dni_usuario, notification.descripcion, notification.hora)
            cursor.execute(sql, values)
            conn.commit()
            
    
def get_all_notification():
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM notificacion"
            cursor.execute(sql)
            rows = cursor.fetchall()
            
            notifications = []
            for row in rows:    
                notification = NotificationOut(
                    id = row[0],
                    nia_alumno = row[1],
                    dni_usuario = row[2],
                    descripcion = row[3],
                    hora = row[4]
                )
                notifications.append(notification)
                
            return notifications
        
def get_by_id(id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "SELECT id, nia_alumno, dni_usuario, descripcion, hora FROM notificacion WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            if row is None:
                return None

            notification = NotificationDb(
                id = row[0],
                nia_alumno = row[1],
                dni_usuario = row[2],
                descripcion = row[3],
                hora = row[4]
            )
            return notification
        return None
    
def delete_notification_by_id(id: int):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            sql = "DELETE FROM notificacion WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount
               

def modify_notification(id:int, nia_alumno: str = None, dni_usuario: str = None, descripcion: str = None, hora: str = None):
    with mariadb.connect(**db_config) as conn:
        with conn.cursor() as cursor:
            
            sql = "SELECT * FROM notificacion WHERE id = ?"
            values = (id,)
            cursor.execute(sql, values)
            row = cursor.fetchone()
            
            if row is None: return None
            
            new_nia_alumno = nia_alumno if nia_alumno is not None else row[1]
            new_dni_usuario = dni_usuario if dni_usuario is not None else row[2]
            new_descripcion = descripcion if descripcion is not None else row[3]
            new_hora = hora if hora is not None else row[4]

            sql = "UPDATE notificacion SET nia_alumno = ?, dni_usuario = ?, descripcion = ?, hora = ? WHERE id = ?"
            values = (new_nia_alumno, new_dni_usuario, new_descripcion, new_hora, id)
            cursor.execute(sql, values)
            conn.commit()
            
            return get_by_id(id)
        