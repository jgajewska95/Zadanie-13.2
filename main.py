import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


def add_student(conn, student):
    sql = '''
        INSERT INTO students(first_name, last_name, birth_date)
        VALUES (?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, student)
    conn.commit()
    return cur.lastrowid


def add_grade(conn, grade):
    sql = '''
        INSERT INTO grades(student_id, subject, grade, date)
        VALUES (?,?,?,?)
    '''
    cur = conn.cursor()
    cur.execute(sql, grade)
    conn.commit()
    return cur.lastrowid


def select_all(conn, table):
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()

    return rows


def select_where(conn, table, **query):
    cur = conn.cursor()
    qs = []
    values = ()
    for k, v in query.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)
    cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
    rows = cur.fetchall()
    return rows


def update(conn, table, id, **kwargs):
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (id,)

    sql = f''' UPDATE {table}
             SET {parameters}
             WHERE id = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print("OK")
    except sqlite3.OperationalError as e:
        print(e)


def delete_where(conn, table, **kwargs):
    qs = []
    values = tuple()
    for k, v in kwargs.items():
        qs.append(f"{k}=?")
        values += (v,)
    q = " AND ".join(qs)

    sql = f'DELETE FROM {table} WHERE {q}'
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Deleted")


def delete_all(conn, table):
    sql = f'DELETE FROM {table}'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Deleted")


if __name__ == "__main__":
    create_students_sql = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        birth_date TEXT
    );
    """

    create_grades_sql = """
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        grade REAL NOT NULL,
        date TEXT,
        FOREIGN KEY (student_id) REFERENCES students (id)
    );
    """

    db_file = "students.db"

    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_students_sql)
        execute_sql(conn, create_grades_sql)

        student = ("Adam", "Małysz", "1980-05-11 00:00:00")
        add_student(conn, student)
        student = ("Jan", "Kowalski", "2001-12-03 00:00:00")
        add_student(conn, student)
        student = ("Jon", "Doe", "1997-08-23 00:00:00")
        add_student(conn, student)

        grade = (1, "Matematyka", 4.5, "2023-11-05 00:00:00")
        add_grade(conn, grade)
        grade = (1, "J. Polski", 3.0, "2023-11-04 00:00:00")
        add_grade(conn, grade)
        grade = (2, "Matematyka", 5.0, "2023-11-01 00:00:00")
        add_grade(conn, grade)
        grade = (2, "J. Angielski", 3.5, "2023-11-02 00:00:00")
        add_grade(conn, grade)
        grade = (2, "Fizyka", 4.5, "2023-11-05 00:00:00")
        add_grade(conn, grade)
        grade = (3, "Muzyka", 4.0, "2023-11-02 00:00:00")
        add_grade(conn, grade)

        all_students = select_all(conn, "students")
        for student in all_students:
            print(student)

        all_grades = select_all(conn, "grades")
        for grade in all_grades:
            print(grade)

        grades_list = select_where(conn, "grades", grade=5.0)
        print(grades_list)

        update(conn, 'students', 3, first_name="John")

        all_students = select_all(conn, "students")
        for student in all_students:
            print(student)

        delete_where(conn, "students", id=3)
        delete_all(conn, "grades")

        all_students = select_all(conn, "students")
        for student in all_students:
            print(student)

        all_grades = select_all(conn, "grades")
        for grade in all_grades:
            print(grade)

        conn.close()