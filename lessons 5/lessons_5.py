"""SQL и базы данных
Создать базу данных с названием order_service_db. Создать в ней несколько таблиц:
Таблица ЗАЯВКИ (orders)
- id заявки (order_id) - целое число
- дата создания (created_dt) - текст / date
- дата обновления заявки (updated_dt) - текст / date
- тип заявки (order_type) - текст
- описание (description) - текст
- статус заявки (status) - текст
- серийный номер аппарата (serial_no) - целое число
- id создателя заявки (creator_id) - целое число
Таблица СОТРУДНИКИ (employees)
- id сотрудника (employee_id) - целое число
- ФИО (fio) - текст
- должность (position) - текст
- id подразделения (department_id) - целое число
Таблица ПОДРАЗДЕЛЕНИЯ (departments)
- id подразделения (department_id) - целое число
- название подразделения (department_name) - текст
Написать код создания таблиц на языке SQL, предусмотреть необходимые ограничения.
"""

"""
CREATE DATABASE order_service_db

CREATE TABLE IF NOT EXISTS orders (
order_id SERIAL PRIMARY KEY,
created_dt date,
updated_dt date,
order_type TEXT NOT NULL,
description TEXT NOT NULL,
status TEXT ,
serial_no INTEGER,
creator_id INTEGER
);

CREATE TABLE IF NOT EXISTS employees (
employee_id INTEGER,
fio TEXT,
position TEXT,
department_id INTEGER
);

CREATE TABLE IF NOT EXISTS departments (
department_id INTEGER,
department_name TEXT
);

DROP TABLE IF EXISTS orders
DROP TABLE IF EXISTS employees
DROP TABLE IF EXISTS departments

SELECT * FROM orders;

INSERT INTO orders (order_type, description, status, serial_no, creator_id) 
VALUES ('private application', 'telephone repair', 'active', 1212, 007);
"""