import psycopg2
import configparser


def create_table(conn, name):
    with conn.cursor() as cur:
        cur.execute("""
              DROP TABLE IF  EXISTS Clients;
              DROP TABLE IF  EXISTS telephones;
              """)
        cur.execute("""
          CREATE TABLE IF NOT EXISTS "%s"(
            id SERIAL PRIMARY KEY,
            first_name varchar(60)NOT NULL,
            last_name varchar(60)NOT NULL,
            email varchar(60)
            );""", (name,))
        conn.commit()

    # cur.execute("""
    #          INSERT INTO Clients (first_name, last_name, email)
    #          VALUES ("Dima", "Dmitrov", "1@1.ru");
    #                 """)

        cur.execute("""
              CREATE TABLE IF NOT EXISTS telephones(
                id SERIAL PRIMARY KEY,
                telephone_num varchar(20),
                client_id INTEGER NOT NULL REFERENCES "%s"(id)
            );
              """, (name,))
        conn.commit()




def create_user(conn, name, lastname, email, tel_num):

    with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO "'Clients'" (first_name, last_name, email) 
          VALUES ("%s", "%s", "%s") RETURNING id;
              """, (name, lastname, email ))
        i = cur.fetchone()

        if tel_num != '':
            cur.execute("""
              INSERT INTO "'telephones'" (telephone_num, client_id) 
          VALUES("%s", "%s");
              """, (tel_num, i))

        print(cur.fetchone())

def add_tel_num(conn, id, tel_num):
    with conn.cursor() as cur:
        if tel_num != '':
            cur.execute("""
              INSERT INTO telephones(telephone_num, client_id) 
          VALUES("%s", "%s");
              """, (tel_num, id))

        return cur.fetchone()

def change_data(conn, id: int, email: str) -> int:
    with conn.cursor() as cur:
        if email != '':
            cur.execute("""
              UPDATE Clients SET email="%s" WHERE id=%s;
              """, (id, email))

        return cur.fetchone()[0]

def del_telephone(conn, id: int) -> int:
    with conn.cursor() as cur:
        cur.execute("""
              DELETE FROM telephones WHERE client_id="%s";
              """, (id))

        return cur.fetchone()[0]


def del_user(conn, id: int) -> int:
    with conn.cursor() as cur:
        cur.execute("""
              DELETE FROM telephones WHERE client_id="%s";
              """, (id))

        cur.execute("""
                  DELETE FROM Clients WHERE id="%s";
                  """, (id))
        return cur.fetchone()[0]

def find_user(conn,  name: str, lastname: str, email: str, tel_num: str) -> int:
    with conn.cursor() as cur:
        if tel_num != '':
            cur.execute("""
              SELECT id FROM Clients WHERE first_name="%s" and last_name="%s" or email="%s";
              """, (name, lastname, email))
        else:
            cur.execute("""
                  SELECT c.id FROM Clients c 
                  join telephones t on t.client_id==c.id 
                  WHERE t.telephone_num="%s";
                  """, (tel_num))
        return cur.fetchone()

if __name__ == '__main__':

    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read("settings.ini")  # читаем конфиг

    password_my = config["Passwords"]["Password"]
    user_my = config["Passwords"]["User"]

    with psycopg2.connect(database="postgres", user=user_my, password=password_my) as conn:
        python_id = create_table(conn, "Clients")
        print('Clients_id', python_id)
        conn.commit()

    #    python_id = create_user(conn, "Ivan", "Petrov", "test@test.ru", "+79111234567")
        python_id = create_user(conn, 1, 2, 3, 4)

        print('Clients_insert', python_id)
        conn.commit()

        python_id = add_tel_num(conn, 1, '+79123333333')
        print('add_tel_num', python_id)

        python_id = change_data(conn, 1, 'example@mail.ru')
        print('change_data', python_id)

        python_id = del_telephone(conn, 1)
        print('del_telephone', python_id)

        python_id = find_user(conn, '+79123333333')
        print('find_user', python_id)

        python_id = del_user(conn, 10)
        print('del_user', python_id)




