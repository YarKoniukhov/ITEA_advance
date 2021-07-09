from flask import Flask, request
from lessons_10 import *
import json

app = Flask('app')


@app.route('/create_departments', methods=["POST"])
def create_departments():
    depart_data = json.loads(request.data)
    Departments(department_id=depart_data['department_id'],
                department_name=depart_data['department_name']).create_departments()
    return f'Department {json.loads(request.data)} create!'


@app.route('/search_departments_id/<string:user_id>', methods=["GET"])
def search_depart_by_id(user_id):
    return str(Departments.objects(pk=user_id))


@app.route('/update_departments/<string:dep_id>', methods=['PATCH'])
def update_departments(dep_id):
    depart_data = json.loads(request.data)
    Departments.objects(pk=dep_id).update(department_id=depart_data['department_id'],
                                          department_name=depart_data['department_name'])
    return f'departament {json.loads(request.data)} update'


@app.route('/delete_departments_by_id/<string:dep_id>', methods=['DELETE'])
def delete_department_by_id(dep_id):
    Departments.objects(pk=dep_id).delete()
    return f'departament {dep_id} delete'


@app.route('/create_employees', methods=["POST"])
def create_employees():
    empl_data = json.loads(request.data)
    Employees(fio=empl_data['fio'],
              position=empl_data['position'],
              department_id=empl_data['department_id'],
              employee_id=empl_data['employee_id']).create_employees()
    return f'Employees {json.loads(request.data)} create!'


@app.route('/search_employees_id/<string:user_id>', methods=["GET"])
def search_employees_by_id(user_id):
    return str(Employees.objects(pk=user_id))


@app.route('/update_employees/<string:dep_id>', methods=['PATCH'])
def update_employees(dep_id):
    empl_data = json.loads(request.data)
    Employees.objects(pk=dep_id).update(fio=empl_data['fio'],
                                        position=empl_data['position'],
                                        department_id=empl_data['department_id'],
                                        employee_id=empl_data['employee_id'])
    return f'employees {json.loads(request.data)} update'


@app.route('/delete_employees_by_id/<string:dep_id>', methods=['DELETE'])
def delete_empl_by_id(dep_id):
    Employees.objects(pk=dep_id).delete()
    return f'employees {dep_id} delete'


@app.route('/create_order', methods=["POST"])
def create_order():
    order_data = json.loads(request.data)
    Orders(order_type=order_data['order_type'],
           description=order_data['description'],
           status=order_data['status'],
           serial_no=order_data['serial_no'],
           creator_id=order_data['creator_id'],
           order_id=order_data['order_id']).create_order()
    return f'Order {json.loads(request.data)} create!'


@app.route('/search_order_id/<string:user_id>', methods=["GET"])
def search_order_by_id(user_id):
    return str(Orders.objects(pk=user_id))


@app.route('/update_order/<string:dep_id>', methods=['PATCH'])
def update_order(dep_id):
    order_data = json.loads(request.data)
    Orders.objects(pk=dep_id).update(order_type=order_data['order_type'],
                                     description=order_data['description'],
                                     status=order_data['status'],
                                     serial_no=order_data['serial_no'],
                                     order_id=order_data['order_id'])
    return f'order {json.loads(request.data)} update'


@app.route('/delete_order_by_id/<string:dep_id>', methods=['DELETE'])
def delete_order_by_id(dep_id):
    Orders.objects(pk=dep_id).delete()
    return f'order {dep_id} delete'


app.run(debug=True)
