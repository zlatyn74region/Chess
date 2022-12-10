import logging
from enum import Enum

class Point:
    v: int
    h: int

    def __str__(self) -> str:
        return chr(self.v + ord('A') - 1) + str(self.h)

    def __init__(self, v: int = None, h: int = None):
        self.v = v
        self.h = h
    
class NameFigures(Enum):
    bishop = 1
    knight = 2
    rook = 3
    queen = 4
    pawn = 5

class Figure:
    p: Point
    name: NameFigures

    def __init__(self, point: Point, name: NameFigures):
        self.p = point
        self.name = name

def input_int(
    msg: str, 
    min: int = None, 
    max: int = None,
) -> int:
    '''
    Берет на ввод у пользователя число с дальнейшей проверкой.
    Параметры:
    msg - Сообщение подающееся на ввод пользователю.
    min - Минимальное значение на ввод.
    max - Максимальное значение на ввод.
    Возврат:
    Корректно введенное число.
    '''
    while True:
        try:
            logging.info(msg)
            num = int(input(msg))
            logging.info('Пользователь ввел: ' + str(num))
            if min != None and num < min or max != None and num > max:
                min_msg = '' if min == None else f' от {min}'
                max_msg = '' if max == None else f' до {max}'
                print(f'Ошибка: нужно ввести число{min_msg}{max_msg}!')
                logging.error(f'Ошибка: нужно ввести число{min_msg}{max_msg}!')
                continue
            logging.info('Корректное значение введенное пользователем: ' + str(num))
            return num
        except:
            logging.error('Ошибка: нужно ввести число!', exc_info=True)
            print('Ошибка: нужно ввести число!')

def check_equals_colors(figure1: Figure, figure2: Figure) -> bool:
    return (figure1.p.v + figure1.p.h) % 2 == (figure2.p.v + figure2.p.h) % 2

def check_risk(figure1: Figure, figure2: Figure) -> bool:
    match figure2.name:
        case NameFigures.bishop.name:
            return abs(figure1.p.v - figure2.p.v) == abs(figure1.p.h - figure2.p.h)
        case NameFigures.knight.name:
            return abs(figure1.p.v - figure2.p.v) == 1 and abs(figure1.p.h - figure2.p.h) == 2 or \
                abs(figure1.p.v - figure2.p.v) == 2 and abs(figure1.p.h - figure2.p.h) == 1 
        case NameFigures.rook.name:
            return figure1.p.v == figure2.p.v or figure1.p.h == figure2.p.h
        case NameFigures.queen.name:
            return figure1.p.v == figure2.p.v or figure1.p.h == figure2.p.h or \
                    abs(figure1.p.v - figure2.p.v) == abs(figure1.p.h - figure2.p.h)

def sec_turn(figure1: Figure, figure2: Figure):
    match figure2.name:
        case NameFigures.bishop.name:
            fig_buffer = figure2
            while fig_buffer.p.v < 8 and fig_buffer.p.h < 8:
                if check_risk(figure1, fig_buffer):
                    return fig_buffer.p
                fig_buffer.p.v += 1
                fig_buffer.p.h += 1

            fig_buffer = figure2
            while fig_buffer.p.v < 8 and fig_buffer.p.h > 1:
                if check_risk(figure1, fig_buffer):
                    return fig_buffer.p
                fig_buffer.p.v += 1
                fig_buffer.p.h -= 1

            fig_buffer = figure2
            while fig_buffer.p.v > 1 and fig_buffer.p.h < 8:
                if check_risk(figure1, fig_buffer):
                    return fig_buffer.p
                fig_buffer.p.v -= 1
                fig_buffer.p.h += 1

            fig_buffer = figure2
            while fig_buffer.p.v > 1 and fig_buffer.p.h > 1:
                if check_risk(figure1, fig_buffer):
                    return fig_buffer.p
                fig_buffer.p.v -= 1
                fig_buffer.p.h -= 1
        case NameFigures.rook.name:
            return Point(v=figure1.p.v, h=figure2.p.h) 
        case NameFigures.queen.name:
            return Point(v=figure1.p.v, h=figure2.p.h) 
    
    return None

logging.basicConfig(level=logging.INFO, filename="logfile.log", filemode="a",
                        format="%(asctime)s %(levelname)s %(message)s")

point1 = Point()
point1.v = input_int('Введите номер вертикали (при счете слева направо) для первой фигуры: ', 1, 8)
point1.h = input_int('Введите номер горизонтали (при счете снизу вверх) для первой фигуры: ', 1, 8)

figure1 = Figure(point=point1, name=NameFigures.pawn)

point2 = Point()
point2.v = input_int('Введите номер вертикали (при счете слева направо) для второй фигуры: ', 1, 8)

while True:
    point2.h = input_int('Введите номер горизонтали (при счете снизу вверх) для второй фигуры: ', 1, 8)
    if point1.v == point2.v and point1.h == point2.h:
        print('Ошибка: фигуры стоят на одной клетке, введите другую горизонталь!')
        logging.error('Ошибка: фигуры стоят на одной клетке, введите другую горизонталь!')
    else:
        logging.info('Введенные координаты клеток отличаются')
        break

choose_fig_msg = 'Выберите название для второй фигуры из предложенных:\n' + \
        '1 - слон\n' + \
        '2 - конь\n' + \
        '3 - ладья\n' + \
        '4 - ферзь'
print(choose_fig_msg)
logging.info(choose_fig_msg)
num_figure = input_int('>>> ', 1, 4)

figure2 = Figure(point=point2, name=NameFigures(num_figure).name)

if check_equals_colors(figure1=figure1, figure2=figure2):
    print('а) Фигуры стоят на одинаковых по цвету клетках')
    logging.info('а) Фигуры стоят на одинаковых по цвету клетках')
else:
    print('а) Фигуры стоят на разных по цвету клетках')
    logging.info('а) Фигуры стоят на разных по цвету клетках')

if check_risk(figure1=figure1, figure2=figure2):
    print('б) Первая фигура находится под угрозой второй')
    logging.info('б) Первая фигура находится под угрозой второй')
    print('в) Вторая фигура может срубить первую за один ход.')
    logging.info('в) Вторая фигура может срубить первую за один ход.')
else:
    print('б) Вторая фигура не угрожает первой')
    logging.info('б) Вторая фигура не угрожает первой')

    p = sec_turn(figure1=figure1, figure2=figure2)
    if p != None:
        print('в) Вторая фигура может срубить первую на клетке ' + str(p))
        logging.info('в) Вторая фигура может срубить первую на клетке ' + str(p))
    else:
        print('в) Вторая фигура не может срубить первую за 2 хода')
        logging.info('в) Вторая фигура не может срубить первую за 2 хода')
