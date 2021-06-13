"""
Продолжаем работу с таблицами из домашнего задания №5:

1. Создать тестовый набор данных по каждой из таблиц в модуле python (лучше всего использовать список списков или
список кортежей). Написать скрипт, который бы осуществлял подключение к существующей БД и последовательно запускал
сначала скрипты на создание таблиц (из прошлого ДЗ: departments, employees, orders), а затем последовательно загружал
туда данные.
"""

import psycopg2


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print('Connection to PostgreSQL DB successful')
    except Exception as err:
        print(f'The error {err} occurred')
    return connection


def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('Query executed successfully')
    except Exception as err:
        print(f'The error {err} occurred')


create_table_orders = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id SERIAL PRIMARY KEY,
        created_dt date,
        updated_dt date,
        order_type TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT,
        serial_no INTEGER,
        creator_id INTEGER
)
"""

create_table_employees = """
    CREATE TABLE IF NOT EXISTS employees (
        employee_id SERIAL PRIMARY KEY,
        fio TEXT,
        position TEXT,
        department_id INTEGER 
)
"""

create_table_departments = """
    CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER,
    department_name TEXT,
    product_id SERIAL PRIMARY KEY,
    FOREIGN KEY (product_id) REFERENCES orders (order_id),
    FOREIGN KEY (department_id) REFERENCES employees (employee_id)
)
"""

create_orders = """
INSERT INTO 
    orders (order_type, description, status, serial_no, creator_id) 
VALUES 
    ('private application', 'telephone repair', 'active', 1212, 007),
    ('open application', 'notebook', 'close', 5555444, 1)
"""

create_employees = """
INSERT INTO 
    employees (fio, position)
VALUES
    ('Yar', 'trainee'),
    ('Ivan', 'junior')
"""

create_departments = """
INSERT INTO
    departments (department_name)
VALUES
    ('Apple'),
    ('Samsung')
"""

# 1
connection = create_connection('order_service_db', 'postgres', 'yarisgerc85', '127.0.0.1', '5432')
# 2
execute_query(connection, create_table_orders)
# 3
execute_query(connection, create_table_employees)
# 4
execute_query(connection, create_table_departments)
# 5
execute_query(connection, create_orders)
# 6
execute_query(connection, create_employees)
# 7
execute_query(connection, create_departments)


"""
2. По тестовым данным необходимо написать следующие запросы:
    - запрос для получения заявок в определенном статусе (можно выбрать любой) за конкретный день, созданных
    конкретным сотрудником;
    - запрос, возвращающий список сотрудников и департаментов, в которых они работают
    - запрос, позволяющий получить количество заявок в определенном статусе (можно выбрать любой) по дням;
"""


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as err:
        print(f"The error {err} occurred")


select_orders_active = """
    SELECT * FROM orders
    WHERE status = 'active'
"""

activ = execute_read_query(connection, select_orders_active)
for a in activ:
    print(a)


select_employees_departments = """
    SELECT * FROM employees CROSS JOIN departments WHERE employees.employee_id = departments.product_id
"""

employees_departments = execute_read_query(connection, select_employees_departments)
for empl in employees_departments:
    print(empl)


number_of_close_orders = """
    SELECT COUNT(*)     
    FROM orders
    WHERE status = 'close'
    """

num_close = execute_read_query(connection, number_of_close_orders)
print(f'number of completed applications {num_close}')
