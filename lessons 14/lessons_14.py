"""
Перевести все существующие модели (Заявки, Департаменты, Сотрудники) на Flask-SQLAlchemy.
Перевести все ручки Flask-приложения из прошлого ДЗ на использование этих моделей.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgresdb@localhost:5432/order_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Departments(db.Model):
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name = db.Column(db.String(25))


class Employees(db.Model):
    employees_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fio = db.Column(db.String(100))
    position = db.Column(db.String(25))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_dt = db.Column(db.DateTime, nullable=False, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_dt = db.Column(db.DateTime, nullable=True, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    order_type = db.Column(db.String(20))
    description = db.Column(db.String(100))
    status = db.Column(db.String(15))
    serial_no = db.Column(db.Integer)
    creator_id = db.Column(db.Integer, db.ForeignKey('employees.employees_id'))

    def __str__(self):
        return f'Order_id: {self.order_id}\n' \
               f'Created_dt: {self.created_dt}\n' \
               f'Update_dt: {self.updated_dt}\n'\
               f'Order_type: {self.order_type}\n' \
               f'Description: {self.description}\n' \
               f'Status: {self.status}\n' \
               f'Serial_no: {self.serial_no}\n' \
               f'Creator_id: {self.creator_id}\n'


@app.route('/insert_order', methods=['POST'])
def insert_db():
    if request.method == 'POST':
        data_order = json.loads(request.data)
        order_profile = Orders(order_type=data_order['order_type'],
                               description=data_order['description'],
                               status=data_order['status'],
                               serial_no=data_order['serial_no'],
                               creator_id=data_order['creator_id'])
        db.session.add(order_profile)
        db.session.flush()
        db.session.commit()
        return 'Create order'


@app.route('/insert_department', methods=['POST'])
def insert_department():
    if request.method == 'POST':
        data_department = json.loads(request.data)
        department_profile = Departments(department_name=data_department['department_name'])
        db.session.add(department_profile)
        db.session.flush()
        db.session.commit()
        return 'Create department'


@app.route('/insert_employee', methods=['POST'])
def insert_employee():
    if request.method == 'POST':
        data_employee = json.loads(request.data)
        employee_profile = Employees(fio=data_employee['fio'],
                                     position=data_employee['position'],
                                     department_id=data_employee['department_id'])
        db.session.add(employee_profile)
        db.session.flush()
        db.session.commit()
        return 'Create employee'


@app.route('/change_status', methods=['PATCH'])
def change_status():
    if request.method == 'PATCH':
        data_status = json.loads(request.data)
        get_id = Orders.query.filter_by(order_id=data_status['order_id']).first()
        get_id.update_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
        return f'Change_status'


@app.route('/search_order_id/<string:search_id>', methods=['GET'])
def search_by_id(search_id):
    search_order = Orders.query.filter_by(order_id=search_id).first()
    return f'{search_order}'


@app.route('/delete_order_id/<string:delete_id>', methods=['DELETE'])
def delete_order(delete_id):
    del_id = Orders.query.filter_by(order_id=delete_id).first()
    db.session.delete(del_id)
    db.session.commit()
    return f'order {delete_id} delete!'


app.run(debug=True)