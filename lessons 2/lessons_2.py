import uuid
import datetime

"""
1. Реализуйте базовый класс Car.
У класса должны быть следующие атрибуты: speed, color, name, is_police (булево).
А также методы: go, stop, turn(direction), которые должны сообщать, что машина поехала, остановилась, повернула (куда);
опишите несколько дочерних классов: TownCar, SportCar, WorkCar, PoliceCar;
добавьте в базовый класс метод show_speed, который должен показывать текущую скорость автомобиля;
для классов TownCar и WorkCar переопределите метод show_speed. При значении скорости свыше 60 (TownCar) и
40 (WorkCar) должно выводиться сообщение о превышении скорости.
Реализовать метод для user-friendly вывода информации об автомобиле.
"""


class Car:
    def __init__(self, speed, color, name, is_police):
        self.speed = speed
        self.color = color
        self.name = name.title()
        self.is_police = is_police

    def __str__(self):
        if self.is_police:
            car_info = '\n' + str(self.name) + ' ' + str(self.color) + ', speed ' + str(self.speed) + \
                       ' km/h.\n This is a police car'
            return car_info
        else:
            car_info = '\n' + str(self.name) + ' ' + str(self.color) + ', speed ' + str(self.speed) + \
                       ' km/h.\nThis is not a police car'
            return car_info

    def car_go(self):
        return f'\nthe car {self.name} is moving forward'

    def car_stop(self):
        return f'\nthe car {self.name} stopped'

    def car_turn_left(self):
        return f'\nthe car {self.name} turned left'

    def car_turn_right(self):
        return f'\nthe car {self.name} turned right'

    def show_speed(self):
        return f'\nthe car {self.name} is moves at a speed of: {self.speed} km/h'

    def info_car(self):
        if self.is_police:
            car_info = '\n' + str(self.name) + ' ' + str(self.color) + ', speed ' + str(self.speed) + ' km/h.\n' \
                                                                                                      'This is a police car'
            return car_info
        else:
            car_info = '\n' + str(self.name) + ' ' + str(self.color) + ', speed ' + str(self.speed) + ' km/h.\n' \
                                                                                                      'This is not a police car'
            return car_info


class TownCar(Car):
    def __init__(self, speed, color, name, is_police, max_speed=60):
        super().__init__(speed, color, name, is_police)
        self.max_speed = max_speed

    def show_speed(self):
        if self.speed > self.max_speed:
            return f'\nSpeed of {self.name} is higher than allowed for a city car'
        else:
            return f'\nSpeed of {self.name} is normal for city car'


class SportCar(Car):
    pass


class WorkCar(Car):
    def __init__(self, speed, color, name, is_police, max_speed=40):
        super().__init__(speed, color, name, is_police)
        self.max_speed = max_speed

    def show_speed(self):
        if self.speed > self.max_speed:
            return f'\nSpeed of {self.name} is higher than allowed for a work car'
        else:
            return f'\nSpeed of {self.name} is normal for work car'


class PoliceCar(Car):

    def police_car(self):
        if self.is_police:
            return f'\n{self.name} is police car'
        else:
            return f'\n{self.name} is not police car'


"""
2. Давайте представим, что мы занимаемся проектированием CRM для сервисного центра по обслуживанию и ремонту техники.
Реализуйте класс Заявка. Каждая заявка должна иметь следующие поля: уникальный идентификатор (присваивается в момент)
создания заявки автоматически, дата и время создания заявки (автоматически), имя пользователя, серийный номер
оборудования, статус (активная заявка или закрытая например, статусов может быть больше). Id заявки сделать приватным
полем.
У заявки должны быть следующие методы:
- метод, возвращающий, сколько заявка находится в активном статусе (если она в нём)
- метод, изменяющий статус заявки
- метод, возвращающий id заявки
"""


class Order:

    def __init__(self, user_name, serial_number, status_request):
        self.__id_number = uuid.uuid4()
        self.data_request = datetime.datetime.now()
        self.user_name = user_name
        self.serial_number = serial_number
        self.status_request = status_request

    def __str__(self):
        return f'\nuser name: {self.user_name.title()}\nserial number: {self.serial_number}\n' \
               f'status request: {self.status_request}'

    def active_status(self):
        if not self.status_request:
            return f'You request closed'
        else:
            today = datetime.datetime.today()
            now = today - self.data_request
            return f'Your request is in progress {now}'

    def change_request_status(self):
        if self.status_request:
            self.status_request = False
            return f'Order status changed to closed!'
        else:
            self.status_request = True
            return f'Request status changed to open!'

    def id(self):
        return f'You id number request- {self.__id_number.hex}'


"""
3. Реализовать класс матрицы произвольного типа. При создании экземпляра передаётся вложенный список. Для объектов
класса реализовать метод сложения и вычитания матриц, а также умножения, деления матрицы на число и user-friendly вывода
матрицы на экран.
"""


class Matrix:
    def __init__(self, list_mat):
        self.list_mat = list_mat

    def __str__(self):
        return '\n'.join('\t'.join(map(str, row))
                         for row in self.list_mat)

    def __add__(self, other):
        result = []
        for i in range(len(self.list_mat)):
            numbers = []
            for j in range(len(self.list_mat[0])):
                summ = self.list_mat[i][j] + other.list_mat[i][j]
                numbers.append(summ)
            result.append(numbers)
        return Matrix(result)

    def __sub__(self, other):
        result = []
        for i in range(len(self.list_mat)):
            numbers = []
            for j in range(len(self.list_mat[0])):
                summ = self.list_mat[i][j] - other.list_mat[i][j]
                numbers.append(summ)
            result.append(numbers)
        return Matrix(result)

    def __mul__(self, other):
        result = [[other * j for j in i] for i in self.list_mat]
        return Matrix(result)

