"""
1. Создать Телеграм-бота. Создать таблицу, в которую при обращении к Телеграм-боту будет сохраняться следующая информация:
- nickname пользователя;
- идентификатор чата, через которое происходит общение;
- дата и время получения сообщения


2. Создать новую модель "Клиенты" (Customers), в которой предусмотреть на своё усмотрение необходимые поля,
ограничения и связи. Обязательным будет наличие в вашей модели поля is_subscribed (для подписки на уведомления).

Данная модель будет ответственна за работу с информацией о пользователях, которые оставляют заявки на консультацию
или ремонт. Подумайте над тем, какие дополнения потребует ваша модель Orders и внесите их.

Желаю удачи ;)
"""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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


class Customers(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fio = db.Column(db.String(100))
    number_phone = db.Column(db.Integer)
    email = db.Column(db.String(100))
    is_subscribed = db.Column(db.Boolean, default=False)


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), nullable=False)
    chat_id = db.Column(db.Integer, nullable=False)
    create_dt = db.Column(db.DateTime, default=datetime.utcnow())


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


@app.route('/delete_chat_id/<string:del_chat_id>', methods=['DELETE'])
def delete_chat_id(del_chat_id):
    del_id = Users.query.filter_by(chat_id=del_chat_id).first()
    db.session.delete(del_id)
    db.session.commit()
    return f'order {del_chat_id} delete!'


db.create_all()
if __name__ == '__main__':
    app.run(debug=True)

