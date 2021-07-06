"""
1. Напишите декоратор для класса, который бы при создании экземпляра этого класса осуществлял бы запись информации об
этом в текстовый файл. Пример записи: 2012-01-01 15:04 Создан экземпляр класса TestClass по адресу памяти x01223342
"""
from datetime import datetime
import datetime
import psycopg2
from abc import ABC, abstractmethod
import json


def decorator(cls):
    def inner():
        with open('file.txt', 'a') as f_obj:
            instance = f'{datetime.datetime.now()} Создан экземпляр класса {cls} по адресу памяти {id(cls)}\n'
            f_obj.write(instance)
        return cls

    return inner


@decorator
class TestClass:
    print('Hello World')


test = TestClass()

"""
2. На основе прошлых ДЗ необходимо создать модели представлений для классов ДЕПАРТАМЕНТЫ (Departments),
СОТРУДНИКИ (Employees), ЗАЯВКИ (Orders). Реализовать магические методы вывода информации на экран как для пользователя,
так и для "машинного" отображения.

Предусмотреть все необходимые ограничения и связи моделей между собой.

У каждой модели предусмотрите метод, который бы мог осуществлять запись хранимой в экземпляре информации в отдельный
json-файл с именем вида <id записи>.json. Если id не существует - выдавать ошибку.
"""

connection = psycopg2.connect(
    database='order_service_db',
    user='postgres',
    password='yarisgerc85',
    host='127.0.0.1',
    port='5432'
)


class BaseModel(ABC):
    @abstractmethod
    def insert_new_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete_data_by_id(self, *args, **kwargs):
        pass


class Orders(BaseModel):
    INSERT_ORDER = ("""INSERT INTO orders (created_dt, updated_dt, order_type, description, status, 
            serial_no, creator_id) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING order_id""")

    def __init__(self, order_type, description, status, serial_no, creator_id, order_id=None):
        self.created_dt = datetime.datetime.now()
        self.updated_dt = datetime.datetime.now()
        self.order_type = order_type
        self.description = description
        self.status = status
        self.serial_no = serial_no
        self.creator_id = creator_id
        self.__order_id = order_id

    def __str__(self):
        return f'order_id: {self.__order_id}\n' \
               f'created_dt: {self.created_dt}\n' \
               f'updated_dt: {self.updated_dt}\n' \
               f'type_order: {self.order_type}\n' \
               f'description: {self.description}\n' \
               f'status: {self.status}\n' \
               f'serial_number: {self.serial_no}\n' \
               f'creator_id: {self.creator_id}\n'

    def __repr__(self):
        return {self.__order_id, self.created_dt, self.updated_dt, self.order_type, self.description, self.status,
                self.serial_no, self.creator_id}

    def insert_new_data(self):
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(self.__class__.INSERT_ORDER,
                       (datetime.datetime.now(), datetime.datetime.now(), self.order_type, self.description,
                        self.status, self.serial_no, self.creator_id))
        order_id = cursor.fetchone()[0]
        self.__order_id = order_id
        return {'order_id': order_id}

    def get_order_id(self):
        return self.__order_id

    @staticmethod
    def change_status(status, order_id):
        query = f"""UPDATE orders SET {'status'} = %s, updated_dt = %s WHERE order_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, [status, datetime.datetime.now(), order_id])

    @staticmethod
    def change_description(description, order_id):
        query = f"""UPDATE orders SET {'description'} = %s, updated_dt = %s WHERE order_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, [description, datetime.datetime.now(), order_id])

    @staticmethod
    def change_id(creator_id, order_id):
        query = f"""UPDATE orders SET {'creator_id'} = %s, updated_dt = %s WHERE order_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, [creator_id, datetime.datetime.now(), order_id])

    @staticmethod
    def check_order_id(order_id):
        queue = f"""SELECT order_id FROM orders WHERE order_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(queue, [order_id])
        data = cursor.fetchone()
        if not data:
            return False
        else:
            return True

    @staticmethod
    def delete_data_by_id(order_id):
        query = """DELETE FROM orders WHERE order_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, [order_id])

    def save_json_file(self):
        data = {
            'order_id': self.__order_id,
            'created_dt': str(self.created_dt),
            'updated_dt': str(self.updated_dt),
            'type_order': self.order_type,
            'description': self.description,
            'status': self.status,
            'serial_number': self.serial_no,
            'creator_id': self.creator_id
        }

        if self.__order_id is None:
            print('There is no such order ID!')
        else:
            with open(f'order_id {self.__order_id}.json', 'w') as f_obj:
                data['Data of creation'] = f'{datetime.datetime.now()}'
                f_obj.write(json.dumps(data, indent=4, ensure_ascii=False))


class Employees(BaseModel):
    INSERT_EMPLOYEES = ("""INSERT INTO employees (fio, position, department_id) 
        VALUES (%s, %s, %s) RETURNING employee_id""")

    def __init__(self, fio, position, department_id, employee_id=None):
        self.fio = fio
        self.position = position
        self.department_id = department_id
        self.employee_id = employee_id

    def __str__(self):
        return f'fio: {self.fio}\n' \
               f'position: {self.position}\n' \
               f'department_id: {self.department_id}\n' \
               f'employee_id: {self.employee_id}'

    def __repr__(self):
        return {self.fio, self.position, self.department_id, self.employee_id}

    def insert_new_data(self):
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(self.__class__.INSERT_EMPLOYEES, (self.fio, self.position, self.department_id))
        employee_id = cursor.fetchone()[0]
        self.employee_id = employee_id
        return {'employee_id': employee_id}

    @staticmethod
    def delete_data_by_id(employee_id):
        query = """DELETE FROM employees WHERE employee_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, [employee_id])

    def save_json_file(self):
        data = {
            'fio': self.fio,
            'position': self.position,
            'department_id': self.department_id,
            'employee_id': self.employee_id
        }

        if self.employee_id is None:
            print('There is no such employee ID!')
        else:
            with open(f'employee_id {self.employee_id}.json', 'w') as f_obj:
                data['Data of creation'] = f'{datetime.datetime.now()}'
                f_obj.write(json.dumps(data, indent=4, ensure_ascii=False))


class Departments(BaseModel):
    INSERT_DEPARTMENTS = ("""INSERT INTO departments (department_name) 
            VALUES (%s) RETURNING department_id""")

    def __init__(self, department_name, department_id=None):
        self.department_name = department_name
        self.department_id = department_id

    def __str__(self):
        return f'department_name: {self.department_name}\n' \
               f'department_id: {self.department_id}'

    def __repr__(self):
        return {self.department_name, self.department_id}

    def insert_new_data(self):
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(self.__class__.INSERT_DEPARTMENTS, (self.department_name,))
        department_id = cursor.fetchone()[0]
        self.department_id = department_id
        return {'department_id': department_id}

    @staticmethod
    def delete_data_by_id(product_id):
        query = """DELETE FROM departments WHERE product_id = %s"""
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query, [product_id])

    def save_json_file(self):
        data = {
            'department_name': self.department_name,
            'product_id': self.department_id
        }

        if self.department_id is None:
            print('There is no such department ID!')
        else:
            with open(f'department_id {self.department_id}.json', 'w') as f_obj:
                data['Data of creation'] = f'{datetime.datetime.now()}'
                f_obj.write(json.dumps(data, indent=4, ensure_ascii=False))

q = Orders('business', 'ipod', 'active', 4667, 7)
q.insert_new_data()
print(q.__repr__())
print(q)
print(q.check_order_id(3))
q.save_json_file()
emp = Employees('шатунов', 'manager', 9876, 34567)
emp.insert_new_data()
emp.save_json_file()
dep = Departments('htc')
dep.insert_new_data()
dep.save_json_file()