"""
Продолжаем работу с таблицами из домашнего задания №5 и классом Заяка из домашнего задания №2:

Расширить поведение класса Заявка. Теперь заявка должна иметь следующие методы, которые будут взаимодействовать
с БД (получать данные, изменять данные, удалять данные и т.д.):
создание новой заявки;
изменение статуса;
изменение описания;
изменение id создателя;
При изменении данных заявки в БД необходимо изменять поле updated_dt.

Аналогичные классы создать для департаментов и сотрудников. Во время выполнения задания постарайтесь максимально
использовать концепции ООП (инкапсуляцию, наследование, полиморфизм).
"""
import datetime
import psycopg2
from abc import ABC, abstractmethod

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


class Employees(BaseModel):
    INSERT_EMPLOYEES = ("""INSERT INTO employees (fio, position, department_id) 
        VALUES (%s, %s, %s) RETURNING employee_id""")

    def __init__(self, fio, position, department_id, employee_id=None):
        self.fio = fio
        self.position = position
        self.department_id = department_id
        self.employee_id = employee_id

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


class Departments(BaseModel):
    INSERT_DEPARTMENTS = ("""INSERT INTO departments (department_name) 
            VALUES (%s) RETURNING department_id""")

    def __init__(self, department_name, department_id=None):
        self.department_name = department_name
        self.department_id = department_id

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


order1 = Orders('business', 'fast', 'new', 11111, 43)
order2 = Orders('private', 'tel', 'new', 3333, 1)
order3 = Orders('fast', 'auto', 'old', 123, 333341)
order3.insert_new_data()
print(order1, order2)
order1.insert_new_data()
order2.insert_new_data()
order1.change_status('open', 1)
order2.change_status('close', 70)
Orders.change_description('good', 2)
Orders.change_id(5, 3)
Orders.delete_data_by_id(4)

emp = Employees('dl Kon', 'middle', 777)
emp.insert_new_data()
emp.delete_data_by_id(2)

depart = Departments('asus')
dep2 = Departments('nokia')
depart.insert_new_data()
dep2.insert_new_data()
dep2.delete_data_by_id(5)