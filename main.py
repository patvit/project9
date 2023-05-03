import psycopg2
from psycopg2 import sql
import configparser


def create_table(cur, name):
    # cur.execute("""
    #           DROP TABLE IF  EXISTS Clients;
    #           DROP TABLE IF  EXISTS telephones;
    #           """)
    stmt = sql.SQL("""
          CREATE TABLE IF NOT EXISTS {name}(
            id SERIAL PRIMARY KEY,
            first_name varchar(60)NOT NULL,
            last_name varchar(60)NOT NULL,
            email varchar(60)
            )
            """).format(
        name = sql.Identifier(name),
                       )
    cur.execute(stmt)

    # cur.execute("""
    #       CREATE TABLE IF NOT EXISTS %s(
    #         id SERIAL PRIMARY KEY,
    #         first_name varchar(60)NOT NULL,
    #         last_name varchar(60)NOT NULL,
    #         email varchar(60)
    #         )
    #         """, (name,))
    conn.commit()

    cur.execute("""
           INSERT INTO Clients (first_name, last_name, email)
           VALUES ('Dima', 'Dmitrov', '1@1.ru');
                  """)

    cur.execute("""
              CREATE TABLE IF NOT EXISTS telephones(
                id SERIAL PRIMARY KEY,
                telephone_num varchar(20),
                client_id INTEGER NOT NULL REFERENCES Clients(id)
            );
              """)
    conn.commit()




def create_user(cur, name, lastname, email, tel_num):

        #cursor.execute("SELECT admin FROM users WHERE username = %s'", (username,));
        #cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});
   # cur.execute("""
        #   INSERT INTO Clients (first_name, last_name, email)
        #   VALUES (%(name)s, %(lastname)s1, %(email)s2) RETURNING id
        #       """, {'name': name}, {'lastname': lastname}, {'email': email});

        # stmt = sql.SQL("""
        #       CREATE TABLE IF NOT EXISTS {name}(
        #         id SERIAL PRIMARY KEY,
        #         first_name varchar(60)NOT NULL,
        #         last_name varchar(60)NOT NULL,
        #         email varchar(60)
        #         )
        #         """).format(
        #     name=sql.Identifier(name),
        # )
        # cur.execute(stmt)


    # stmt = sql.SQL("""
    # INSERT INTO Clients(first_name, last_name, email)
    #       VALUES ({name}, {lastname}, {email}) RETURNING id;
    #                       """).format(
    #         name, lastname, email = sql.Identifier(name, lastname, email),
    # )
    # cur.execute(stmt)
    cur.execute("""INSERT INTO Clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING id;""", (name, lastname, email))

    # cur.execute("""
    #       INSERT INTO Clients (first_name, last_name, email)
    #       VALUES (%s, %s, %s) RETURNING id;
    #           """, (name, lastname, email))
    i = cur.fetchone()

    if tel_num != '':
        cur.execute("""
          INSERT INTO telephones (telephone_num, client_id) 
          VALUES(%s, %s);
          """, (tel_num, i))

    print(f'указан телефон {tel_num} для ID {i}')
    return i

def add_tel_num(cur, id, tel_num):
    if tel_num != '':
        cur.execute("""INSERT INTO telephones(telephone_num, client_id) VALUES(%s, %s);""", (tel_num, id))

    #return cur.fetchone()

def change_data(cur, id: int, name='', lastname='', email='', telnum=''):
    s=''
    if email != '':
        cur.execute("""
              UPDATE Clients SET email=%s WHERE id=%s;
              """, (email, id))
        s += ' новый email: '+(email)
    if lastname != '':
        cur.execute("""
                      UPDATE Clients SET last_name=%s WHERE id=%s;
                      """, (lastname, id))
        s += ' новая фамилия: '+(lastname)
    if name != '':
        cur.execute("""
                              UPDATE Clients SET first_name=%s WHERE id=%s;
                              """, (name, id))
        s += ' новое имя: '+(name)
    if telnum != '':
        cur.execute("""
                              UPDATE telephones SET telephone_num=%s WHERE client_id=%s;
                              """, (telnum, id))
        s += ' новый номер телефон: '+(telnum)

    return s

def del_telephone(cur, id: int) -> int:
    cur.execute("""
              DELETE FROM telephones WHERE client_id=%s;
              """, (id,))

    return id


def del_user(cur, id) -> int:
    cur.execute("""
              DELETE FROM telephones WHERE client_id=%s;
              """, (id,))

    cur.execute("""
                  DELETE FROM Clients WHERE id=%s;
                  """, (id,))
    return id

def find_user(cur,  table='', name='', lastname='', email='', tel_num='') -> int:

    # cursor.execute("SELECT admin FROM users WHERE username = %s'", (username,));
    # cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});
    if tel_num != '':
         #cur.execute("SELECT first_name FROM Clients WHERE last_name = %s", (lastname,));
         cur.execute("SELECT c.id FROM clients c join telephones t on t.client_id=c.id WHERE t.telephone_num= %s", (tel_num,));

    elif lastname != '':
        cur.execute("SELECT first_name FROM Clients WHERE last_name = %s", (lastname,));
    elif email != '':
        cur.execute("SELECT first_name FROM Clients WHERE email = %s", (email,));
    else:
        cur.execute("SELECT first_name FROM Clients WHERE first_name = %s", (name,));

        # cur.execute("""
        # SELECT id FROM Clients WHERE first_name="%s" and last_name="%s" or email="%s";
        # """, (name, lastname, email))
    return cur.fetchall()

if __name__ == '__main__':

    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг

    password_my = config["Passwords"]["Password"]
    user_my = config["Passwords"]["User"]

    with psycopg2.connect(database="postgres", user=user_my, password=password_my) as conn:
        with conn.cursor() as cur:

            python_id = create_table(cur, 'Clients')
            print('Clients_id', python_id)
            conn.commit()

            id = create_user(cur, 'Ivan', 'Petrov', 'test@test.ru', '+79111234567')
     #   python_id = create_user(conn, 1, 2, 3, 4)

            print('Clients_insert', id)
            conn.commit()

            python_id = add_tel_num(cur, id, '+79123333334')
            print('add_tel_num', python_id)
            conn.commit()

            python_id = change_data(cur, 4, 'Ivan', 'Petrov', 'example@mail.ru','+79123333334')
            print('change_data', python_id)
            python_id = change_data(cur, 5, name='Sveta')
            print('change_data', python_id)
            python_id = change_data(cur, 5, lastname='Smirnova')
            print('change_data', python_id)
            python_id = change_data(cur, 5, email='primer@primer.ru')
            print('change_data', python_id)
            python_id = change_data(cur, 5, telnum='+79158887766')
            print('change_data', python_id)
            #
        #
            python_id = del_telephone(cur, 33)
            print('del_telephone', python_id)

            python_id = find_user(cur, 'clients', 'Ivan', 'Petrov', '33','+79123333334')
            print('find_user', python_id)
            python_id = find_user(cur, tel_num='+79123333334')
            print('find_user', python_id)
            python_id = find_user(cur, name='Ivan')
            print('find_user', python_id)
            python_id = find_user(cur, lastname='Dmitrov')
            print('find_user', python_id)
            python_id = find_user(cur, email='1@1.ru')
            print('find_user', python_id)

            python_id = del_user(cur, 3)
            print('del_user', python_id)
            conn.commit()




