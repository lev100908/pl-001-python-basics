# Функции как объекты высшего порядка

> **Главная мысль.** В Python функция — это **обычный объект**, такой же
> «полноправный гражданин» (*first-class object*), как число или строка. У
> функции есть **собственный тип** (`function`), ее можно **присвоить
> переменной**, **положить в коллекцию**, **передать как аргумент** другой
> функции, **вернуть** из функции как результат и даже **создать во время
> выполнения программы**. Функции, которые принимают другие функции или
> возвращают их, называются **функциями высшего порядка**. Именно эта
> возможность лежит в основе таких механизмов, как `sorted(key=...)` и
> декораторы.

---

## 1. У функции есть тип

Инструкция `def` создает **объект**. Как и у любого объекта, у него есть тип,
идентичность и атрибуты:

```python
def square(number: int) -> int:
    return number * number


print(type(square))      # <class 'function'>
print(callable(square))  # True
```

Функции пользователя имеют тип `function` (он доступен как
`types.FunctionType`). Функция —
**вызываемый (callable)** объект: проверить, можно ли вызвать объект, можно
встроенной функцией `callable()`.

У объекта-функции есть набор атрибутов, часть из которых мы уже встречали:

```python
print(square.__name__)         # square -- имя функции
print(square.__doc__)          # None -- docstring
print(square.__defaults__)     # None -- значения по умолчанию
print(square.__annotations__)  # {'number': <class 'int'>, 'return': <class 'int'>}
```

---

## 2. Функция как значение переменной

Имя функции — обычная переменная, которая ссылается на объект-функцию. Этот
объект можно присвоить другой переменной — получится **второе имя** для той же
функции (а не ее копия):

```python
def square(number: int) -> int:
    return number * number


calculate = square  # без скобок: присваиваем сам объект, а не результат вызова

print(calculate(4))         # 16
print(square(4))            # 16 -- вызов по исходному имени дает тот же результат
print(calculate is square)  # True -- один и тот же объект
```

Поскольку имя функции — просто переменная, ее можно **перепривязать** к чему
угодно, в том числе потерять функцию:

```python
square = 10

print(square(3))  # TypeError: 'int' object is not callable
```

Именно по этой причине нельзя давать переменным имена существующих функций
(`sum = 0`, `max = 5`).

---

## 3. Функция как элемент коллекции

Раз функция — объект, ее можно хранить в списках, кортежах, словарях и других
коллекциях:

```python
def square(number: int) -> int:
    return number * number


def cube(number: int) -> int:
    return number * number * number


functions = [square, cube, abs]

for function in functions:
    print(function.__name__, function(-3))
```

Вывод:
```
square 9
cube -27
abs 3
```

Особенно полезны **словари, значениями которых являются функции**
(*таблицы диспетчеризации*, dispatch table). Они заменяют длинные цепочки
`if`/`elif`:

```python
def add(first_term: float, second_term: float) -> float:
    return first_term + second_term


def subtract(first_term: float, second_term: float) -> float:
    return first_term - second_term


def multiply(first_term: float, second_term: float) -> float:
    return first_term * second_term


operations = {
    "+": add,
    "-": subtract,
    "*": multiply,
}

operator = "*"

print(operations[operator](6, 7))  # 42 -- берем функцию по ключу и сразу вызываем
```

Чтобы добавить новую операцию, достаточно дописать в словарь еще одну пару —
логику выбора менять не придется.

---

## 4. Функция как аргумент другой функции

Функцию можно передать в другую функцию как аргумент. Принимающая
функция вызывает ее по мере необходимости. Так программисты «параметризуют»
поведение: *что* сделать с данными — решает вызывающий код, *как* обойти и
организовать — принимающая функция.

```python
from typing import Callable


def apply_to_all(function: Callable[[int], int], numbers: list[int]) -> list[int]:
    result = []

    for number in numbers:
        result.append(function(number))

    return result


def square(number: int) -> int:
    return number * number


print(apply_to_all(square, [1, 2, 3]))  # [1, 4, 9]
print(apply_to_all(abs, [-1, -2, 3]))   # [1, 2, 3]
```

Обратите внимание: передается `square`, а не `square(...)` — мы отдаем сам
объект, а не результат вызова.

Для аннотации такого параметра используют `Callable` из модуля `typing`
(см. предыдущий конспект): `Callable[[int], int]` — функция, принимающая один
`int` и возвращающая `int`.

### Функции высшего порядка

**Функцией высшего порядка** (*higher-order function*) называется функция,
которая выполняет хотя бы одно из двух действий:

- принимает другую функцию в качестве аргумента;
- возвращает функцию в качестве результата.

Функция `apply_to_all` из примера выше относится к функциям высшего порядка,
так как принимает функцию через параметр `function`. Сами передаваемые функции
(`square`, `abs`) при этом остаются обычными функциями. Пример функции,
возвращающей функцию, приведен в разделе 5.

Многие встроенные функции также являются функциями высшего порядка:

```python
words = ["banana", "kiwi", "apple"]

print(sorted(words, key=len))  # ['kiwi', 'apple', 'banana'] -- сортировка по длине
print(max(words, key=len))     # banana
print(min(words, key=len))     # kiwi
```

Параметр `key` у `sorted`, `min`, `max`, `list.sort` — самый частый пример. Он
получает функцию, которая для каждого элемента вычисляет «ключ» сравнения.

---

## 5. Создание функций во время выполнения и возврат функции как результата

`def` — исполняемая инструкция, а значит, функции можно создавать
**в процессе работы программы**, в том числе внутри другой функции. Внешняя
функция может **вернуть** созданную функцию:

```python
from typing import Callable


def make_greeter() -> Callable[[str], str]:
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    return greet  # возвращаем саму функцию, не вызывая ее


greeter = make_greeter()

print(greeter("Alice"))           # Hello, Alice!
print(make_greeter()("Bob"))      # Hello, Bob! -- вызов результата вызова
print(greeter is make_greeter())  # False
```

При каждом вызове `make_greeter` создается **новый** объект-функция `greet`,
поэтому `greeter is make_greeter()` возвращает `False`.

---

## Вывод

- Функция в Python — полноценный объект: у нее есть тип (`function`),
  идентичность и атрибуты (`__name__`, `__doc__`, `__defaults__`,
  `__annotations__`). Это **вызываемый** объект (`callable()`).
- Имя функции — обычная переменная, поэтому функцию можно присвоить другой
  переменной (получится второе имя того же объекта), хранить в коллекциях
  (списки, словари-диспетчеры) и перепривязывать.
- Функцию можно передать в другую функцию как аргумент (`sorted(key=...)`,
  `min(key=...)`, `max(key=...)`). Передается сам объект — **без скобок**.
- Функции можно создавать во время выполнения (`def` внутри функции)
  и возвращать как результат.
- Функции, принимающие и/или возвращающие другие функции, называются
  **функциями высшего порядка**.

---

## Источники

- [Python documentation. The Python Language Reference — The standard type hierarchy (User-defined functions)](https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy);
- [Python documentation. Functional Programming HOWTO](https://docs.python.org/3/howto/functional.html);
- [Python documentation. The Python Standard Library — Built-in Functions (`sorted`, `min`, `max`)](https://docs.python.org/3/library/functions.html).
