# Аннотации типов и модуль `typing`

> **Главная мысль.** **Аннотации типов (type annotations, type hints)** —
> необязательные пометки в определении функции, которые указывают, значения
> какого типа ожидаются в качестве аргументов (`parameter: type`) и что
> возвращает функция (`-> type`). Аннотации улучшают читаемость, подсказки
> редактора и позволяют **статическим анализаторам** (mypy, pyright)
> находить ошибки *до* запуска программы. При этом интерпретатор **никак не
> проверяет и не применяет аннотации во время исполнения**: код с неверными
> типами выполнится точно так же, как и без аннотаций. Для описания сложных
> типов (`None` или значение, функции, обобщенные типы) служит модуль
> **`typing`**.

---

## 1. Синтаксис аннотаций

Тип параметра указывается после двоеточия, тип возвращаемого значения — после
стрелки `->` перед двоеточием заголовка:

```python
def repeat_text(text: str, count: int = 2) -> str:
    return text * count
```

- `text: str` — параметр `text` должен быть строкой;
- `count: int = 2` — целочисленный параметр `count` со значением по
  умолчанию `2` (пробелы вокруг `=` при наличии аннотации обязательны по
  PEP 8);
- `-> str` — функция возвращает строку.

Если функция ничего не возвращает (то есть возвращает `None`), указывают
`-> None`:

```python
def print_header(title: str) -> None:
    print("=" * 20)
    print(title)
```

Аннотации можно ставить и у `*args`, и у `**kwargs`. Аннотация записывается
один раз и описывает тип **одного значения**, а не всей коллекции: внутри
функции `*args` является кортежем, а `**kwargs` — словарем, но в аннотации
указывается тип их элементов (для `**kwargs` — тип значений, ключи всегда
строки):

```python
def sum_all(*args: int) -> int:     # args имеет тип tuple[int, ...]
    return sum(args)


def build_tag(tag_name: str, **attributes: str) -> str:  # attributes -- dict[str, str]
    ...
```

Аннотации переменных записываются так же: `age: int = 25` (но в этом конспекте
мы сосредоточимся на функциях).

---

## 2. Аннотации не влияют на выполнение

Это важнейшее свойство аннотаций: **Python не проверяет типы во время
исполнения**. Аннотация — всего лишь метаданные, которые сохраняются в
атрибуте функции `__annotations__`:

```python
def add(first_term: int, second_term: int) -> int:
    return first_term + second_term


print(add.__annotations__)
# {'first_term': <class 'int'>, 'second_term': <class 'int'>, 'return': <class 'int'>}
```

Но при вызове с «неправильными» типами ошибки не будет:

```python
print(add(2, 3))      # 5
print(add("a", "b"))  # ab  -- аннотация требует int, но str работает
print(add(1.5, 2))    # 3.5 -- и float тоже
```

Функция выполнилась, потому что ее тело (`first_term + second_term`)
корректно для этих типов, а аннотации интерпретатор проигнорировал. Если же
операция для переданных типов невозможна, ошибка возникнет, но это будет
обычное исключение времени исполнения (`TypeError` из-за операции `+`), а не
исключение из-за несовпадения типов с аннотацией:

```python
print(add("a", 1))  # TypeError: can only concatenate str (not "int") to str
```

Поэтому аннотации следует воспринимать как **договор** и **документацию**:
они говорят, как функцию *следует* использовать, но не заставляют это делать.

### Где аннотации реально работают

Аннотации используют **инструменты**, которые анализируют код, не запуская
его (**статический анализ**):

- **статические анализаторы типов** — `mypy`, `pyright`, `pyre`: проверяют,
  что функции вызываются с правильными типами, и сообщают об ошибках;
- **редакторы и IDE** (VS Code, PyCharm): подсказки при вводе, автодополнение,
  предупреждения о несоответствии типов;
- **генераторы документации** (Sphinx, pdoc);
- **библиотеки, читающие `__annotations__` во время выполнения по собственной
  инициативе** — например, `pydantic` (валидация данных) и `FastAPI`. Это
  решение библиотеки, а не интерпретатора.

Запуск анализатора на коде выше:

```
$ mypy example.py
example.py:9: error: Argument 1 to "add" has incompatible type "str"; expected "int"  [arg-type]
```

Ошибка найдена **до** запуска программы — в этом основная польза аннотаций.
Исправив типы или аннотацию, можно убедиться, что код корректен для
всех путей выполнения (насколько это может проверить анализатор).

---

## 3. Модуль `typing`

Для простых типов достаточно имен встроенных классов: `int`, `float`, `str`,
`bool`, `bytes`. Для описания более сложных ситуаций служит модуль
**`typing`** (а также встроенные возможности самого языка).

### Типы коллекций

Начиная с Python 3.9 коллекции можно параметризовать **прямо
встроенными типами**, указывая в квадратных скобках типы элементов:

```python
def get_average(numbers: list[int]) -> float:
    return sum(numbers) / len(numbers)


def count_words(words: list[str]) -> dict[str, int]:
    result = {}

    for word in words:
        result[word] = result.get(word, 0) + 1

    return result


def get_point() -> tuple[int, int]:      # кортеж из ровно двух int
    return 1, 2


def get_scores() -> tuple[int, ...]:     # кортеж из любого числа int
    return 1, 2, 3


def get_unique(items: list[str]) -> set[str]:
    return set(items)
```

Алиасы `typing.List`, `typing.Dict`, `typing.Tuple`, `typing.Set` — это более
старый способ записи (для Python 3.8 и ниже); в современном коде
используйте встроенные `list`, `dict`, `tuple`, `set`.

### «Значение или `None`»: `Optional` и `|`

Если значение может быть `None`, тип записывают как объединение с `None`.
Начиная с Python 3.10 для этого используется оператор `|`:

```python
def find_index(items: list[str], target: str) -> int | None:
    if target in items:
        return items.index(target)

    return None
```

Эквивалентная старая запись — `typing.Optional[int]` (то же, что
`Union[int, None]`):

```python
from typing import Optional


def find_index(items: list[str], target: str) -> Optional[int]:
    ...
```

Параметр со значением по умолчанию `None` тоже аннотируют как «тип или
`None`» — именно так мы записывали решение проблемы изменяемых значений по
умолчанию: `items: list[str] | None = None`.

### Объединение типов: `Union` и `|`

Если допустимо несколько типов, их объединяют оператором `|` (Python 3.10+) или
`typing.Union`:

```python
from typing import Union


def to_number(value: int | str) -> int:
    return int(value)


def to_number_old(value: Union[int, str]) -> int:  # эквивалентно
    return int(value)
```

### `Any`

`typing.Any` означает «любой тип»: анализатор не будет проверять использование
такого значения. Его применяют, когда тип действительно произвольный или
слишком сложен для описания, но злоупотреблять им не стоит — он «отключает»
проверку:

```python
from typing import Any


def describe(value: Any) -> str:
    return f"{value!r} of type {type(value).__name__}"
```

### `Callable` — функции как аргументы

Тип вызываемого объекта (функции) описывается как
`Callable[[типы_аргументов], тип_результата]`. Это нужно, когда функция
принимает другую функцию (подробнее — в конспекте про функции как объекты):

```python
from typing import Callable


def apply_twice(function: Callable[[int], int], value: int) -> int:
    return function(function(value))


def add_ten(number: int) -> int:
    return number + 10


print(apply_twice(add_ten, 1))  # 21
```

`Callable[..., Any]` — «любая функция с любыми аргументами».
В современном коде `Callable` рекомендуется импортировать из
`collections.abc`, а не из `typing` — запись та же.

### `Literal` — только конкретные значения

`Literal` ограничивает допустимые значения конкретным набором констант:

```python
from typing import Literal


def open_file(path: str, mode: Literal["r", "w", "a"]) -> None:
    ...
```

Анализатор разрешит `open_file("a.txt", "r")` и сообщит об ошибке для
`open_file("a.txt", "x")`. Во время исполнения оба вызова одинаково допустимы.

### Другие возможности `typing`

Модуль `typing` содержит много других конструкций (`Iterable`, `Sequence`,
`TypeVar`, `NoReturn` и т. д.). Для начала они не нужны; при необходимости
всю информацию можно найти в официальной документации модуля
([typing](https://docs.python.org/3/library/typing.html)).

---

## Вывод

- Аннотации записываются как `parameter: type` и `-> type`; для функций,
  ничего не возвращающих, указывают `-> None`. Они сохраняются в
  `function.__annotations__`.
- Во время исполнения аннотации **ничего не проверяют и не влияют на
  работу кода**: функция с аргументами «неправильных» типов выполнится так
  же, как и без аннотаций. Они нужны для документации, подсказок
  редакторов и **статического анализа** (mypy, pyright).
- Модуль `typing` и современный синтаксис языка позволяют описывать сложные
  типы: `list[int]`, `dict[str, int]`, `tuple[int, ...]`, `X | None`
  (`Optional`), `X | Y` (`Union`), `Any`, `Callable`, `Literal`.
- Аннотации — это договор о том, как использовать функцию, а не механизм
  принуждения.

---

## Источники

- [Python documentation. The Python Tutorial — Function Annotations](https://docs.python.org/3/tutorial/controlflow.html#function-annotations);
- [Python documentation. The Python Standard Library — typing](https://docs.python.org/3/library/typing.html);
- [Static Typing with Python (документация сообщества typing)](https://typing.python.org/en/latest/);
- [PEP 484 — Type Hints](https://peps.python.org/pep-0484/);
- [PEP 604 — Allow writing union types as X | Y](https://peps.python.org/pep-0604/);
- [PEP 585 — Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/).
