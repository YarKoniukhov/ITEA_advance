import time
"""
1. Написать декоратор, который будет печатать на экран время работы функции.
"""


def timer(func_to_decorate):
    def wrapper(*args, **kwargs):
        t = time.time()
        res = func_to_decorate(*args, **kwargs)
        print("Function execution time: %f" % (time.time()-t))
        return res
    return wrapper


@timer
def foo(a, b):
    return a + b


foo(2, 4)

"""
2. Написать функцию для вычислений очередного числа Фибоначчи (можно через цикл, можно через рекурсию).
"""


def fibo(n):
    result = []
    a = 0
    b = 1
    while b < n:
        result.append(b)
        a, b = b, b + a
    return result


print(fibo(10))

"""
3. Реализовать функцию, которая принимает три позиционных аргумента и возвращает сумму наибольших двух из них.
"""


def num_summ(a, b, c):
    if a >= c and b >= c:
        return a + b
    elif a > b and a > c:
        return a + c
    else:
        return b + c


print(f'Сумма наибольших чисел: {num_summ(3, 5 ,2)}')


"""
4. Написать программу, которая запрашивает у пользователя строку чисел, разделённых пробелом. При нажатии Enter должна 
выводиться сумма чисел. Пользователь может продолжить ввод чисел, разделённых пробелом и снова нажать Enter. Сумма 
вновь введённых чисел будет добавляться к уже подсчитанной сумме. Но если вместо числа вводится специальный символ, 
выполнение программы завершается. Если специальный символ введён после нескольких чисел, то вначале нужно добавить 
сумму этих чисел к полученной ранее сумме и после этого завершить программу.
"""
sum_numbers = 0
polling_active = True
while polling_active:
    try:
        digits = input('Введите числовой ряд или q для выхода - ').split()
        result = 0
        for i in range(len(digits)):
            if digits[i] == 'q':
                print('Завершение программы!')
                polling_active = False
                break
            else:
                result += int(digits[i])
        sum_numbers += result
        print(f'Сумма ваши чисел: {sum_numbers}')
    except Exception as err:
        print(f'Ошибка, вводите число! \n{err}')
