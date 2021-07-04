"""
    Преобразовать все самописные классы-модели из прошлых ДЗ (из задачи 1: Заявки - Orders, Департаменты - Departments,
Сотрудники - Employees) в модели для использования в MongoDB. Предусмотреть необходимые связи, валидацию
данных и ограничения.
Написать функции, которые будут:
создавать/изменять/удалять новую заявку/сотрудника/департамент
Подсказка: у вас должно получиться 3 модели и 9 функций =)
"""
import mongoengine as me
import datetime

me.connect('LESSONS_9_DB', host='localhost', port=27017)


class Departments(me.Document):
    department_id = me.IntField()
    department_name = me.StringField(required=True)

    def __str__(self):
        return f'ID: {self.pk} \nDepartment_id: {self.department_id} \nDepartment_name: {self.department_name}'

    def create_departments(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    def update_departments(self, **kwargs):
        return self.update(**kwargs)

    def delete_departments(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


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

    def create_employees(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    def update_employees(self, **kwargs):
        return self.update(**kwargs)

    def delete_employees(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


class Orders(me.Document):
    created_dt = me.DateField(default=datetime.datetime.now(), required=True)
    updated_dt = me.DateTimeField(default=datetime.datetime.now(), required=True)
    order_type = me.StringField(required=True, max_length=50)
    description = me.StringField(max_length=200)
    status = me.StringField(max_length=50)
    serial_no = me.IntField(max_value=99)
    creator_id = me.ReferenceField(Employees, required=True, reverse_delete_rule=me.CASCADE)
    order_id = me.IntField(min_value=100, max_value=200)

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

    def create_order(self, *args, **kwargs):
        return self.save(*args, **kwargs)

    def update_order(self, **kwargs):
        return self.update(**kwargs)

    def delete_order(self, *args, **kwargs):
        return self.delete(*args, **kwargs)

dep = Departments(department_id=341, department_name='tata')
#dep.create_departments()
#print(dep.id)
#dep = Departments.objects.get(id='60e1e2332d9abbdcdf4cc305')
#dep.update_departments(department_id=2332, department_name='porshe')
#dep.delete_departments()
emp = Employees(fio='Jhon Smith', position='team lead', department_id=439, employee_id=1324)
#emp.create_employees()
print(emp)
#emp = Employees.objects.get(id='60e210e733c0452142370d95')
#emp.update_employees(position='senior', department_id=111)
#emp.delete_employees()