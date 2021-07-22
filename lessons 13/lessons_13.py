"""
Сделать шаблоны для отображения сотрудников, заявок и департаментов и прикрутить их к соответствующим flask-методам.
Используйте 1 базовый шаблон, от которого унаследуйте все остальные. Что хотелось бы видеть:
- навигационную панель (можно взять из классной работы или написать свою собственную)
- удобный вывод информации (ограничение по количеству записей, выводимых на экран и использование
списка с точками или цифрами при выводе)
"""
import mongoengine as me
from flask import Flask, render_template
import datetime

me.connect('LESSONS_9_DB', host='localhost', port=27017)


class Departments(me.Document):
    department_id = me.IntField()
    department_name = me.StringField(required=True)

    def __str__(self):
        return f'ID: {self.pk} \nDepartment_id: {self.department_id} \nDepartment_name: {self.department_name}'


class Employees(me.Document):
    fio = me.StringField(required=True, max_length=200)
    position = me.StringField()
    department_id = me.IntField(max_value=999)
    employee_id = me.IntField(required=True)

    def __str__(self):
        return f'ID: {self.pk}' \
               f'\nFIO: {self.fio}' \
               f'\nPosition: {self.position}' \
               f'\nDepartment_id: {self.department_id}' \
               f'\nEmployee_id: {self.employee_id}'


class Orders(me.Document):
    created_dt = me.DateField(default=datetime.datetime.now(), required=True)
    updated_dt = me.DateTimeField(default=datetime.datetime.now(), required=True)
    order_type = me.StringField(required=True, max_length=50)
    description = me.StringField(max_length=200)
    status = me.StringField(max_length=50)
    serial_no = me.IntField(max_value=999)
    creator_id = me.IntField()
    order_id = me.IntField(min_value=1, max_value=1000)

    def __str__(self):
        return f'ID: {self.pk}' \
               f'\nCreated_dt: {self.created_dt}' \
               f'\nUpdated_dt: {self.updated_dt}' \
               f'\nOrder_type: {self.order_type}' \
               f'\nDescription: {self.description}' \
               f'\nStatus: {self.status}' \
               f'\nSerial_no: {self.serial_no}' \
               f'\nCreator_id: {self.creator_id}' \
               f'\nOrder_id: {self.order_id}'


app = Flask('h_w')


@app.route('/view_departments')
def view_departments():
    list1 = Departments.objects.all()[:5]
    return render_template('view_departments.html', params=list1)


@app.route('/view_employees')
def view_employees():
    list1 = Employees.objects.all()[:5]
    return render_template('view_employees.html', params=list1)


@app.route('/view_orders')
def view_orders():
    list1 = Orders.objects.all()[:5]
    return render_template('view_orders.html', params=list1)


@app.route('/about_us')
def about_us():
    return render_template('condition.html')


app.run(debug=True)