# Изменяемые объекты в качестве значений по умолчанию

> **Главная мысль.** Так как значение по умолчанию создается **один раз** при
> выполнении `def`, изменяемый объект (`[]`, `{}`, `set()`), указанный в
> качестве такого значения, становится **общим для всех вызовов** функции. Если
> функция изменяет этот объект, изменения «накапливаются» между вызовами — это
> одна из самых известных ловушек Python. Стандартное решение — использовать в
> качестве значения по умолчанию **`None`** и создавать новый объект внутри
> функции. Если `None` является допустимым значением аргумента, для отличия
> «аргумент не передан» от «передан `None`» используют уникальный объект-маркер
> **`sentinel = object()`**.

---

## 1. Проблема

Рассмотрим функцию, которая добавляет элемент в список. Если список не
передан, она должна начать с пустого:

```python
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items


print(add_item("apple"))  # ['apple']
print(add_item("pear"))   # ['apple', 'pear'] -- откуда здесь 'apple'?
print(add_item("plum"))   # ['apple', 'pear', 'plum']
```

Ожидалось, что каждый вызов без второго аргумента начнет с нового пустого
списка. Но результаты «накапливаются». Причина описана в предыдущем конспекте:
выражение `[]` вычислено **один раз** при выполнении `def`, и созданный
список сохранен в `add_item.__defaults__`. Каждый вызов без второго аргумента
получает **ссылку на тот же самый список**, а `append` изменяет его на месте:

```python
print(add_item.__defaults__)  # (['apple', 'pear', 'plum'],)
```

Видно, что «пустой список по умолчанию» превратился в хранилище
накопленных данных. Подтвердить, что это один объект, можно через `is`:

```python
first_result = add_item("a")
second_result = add_item("b")

print(first_result is second_result)  # True -- вернулся один и тот же список
```

Если же список передать явно, он используется вместо значения по умолчанию, и
проблемы нет:

```python
print(add_item("kiwi", ["x"]))  # ['x', 'kiwi']
```

Таким образом, ошибка воспроизводится при каждом вызове, в котором
используется значение по умолчанию, и не возникает, если соответствующий
аргумент передан явно.

### Это касается любых изменяемых объектов

Проблема возникает с любым изменяемым значением по умолчанию — списком,
словарем, множеством, экземпляром пользовательского класса:

```python
def register_user(name: str, registry: dict[str, int] = {}) -> dict[str, int]:
    registry[name] = len(registry) + 1
    return registry


print(register_user("alice"))  # {'alice': 1}
print(register_user("bob"))    # {'alice': 1, 'bob': 2} -- общий словарь
```

### Когда это безопасно

Неизменяемые значения по умолчанию (`0`, `""`, `None`, `True`, кортежи из
неизменяемых элементов) **безопасны**: изменить их на месте нельзя, а
присваивание создает лишь новую локальную ссылку.

```python
def increase(value: int, step: int = 1) -> int:
    value += step  # создается новое число; step по умолчанию не пострадает
    return value
```

---

## 2. Решение: `None` в качестве значения по умолчанию

Стандартный способ — вместо изменяемого объекта указать `None`, а настоящий
объект создать **внутри тела функции**, при каждом вызове:

```python
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []  # новый список создается при КАЖДОМ вызове

    items.append(item)
    return items


print(add_item("apple"))  # ['apple']
print(add_item("pear"))   # ['pear']
print(add_item("plum"))   # ['plum']
```

Теперь `__defaults__` содержит только `None`:

```python
print(add_item.__defaults__)  # (None,)
```

Проверку нужно делать именно через `is None`, а не через `if not items:`.
Иначе пустой список, переданный вызывающим кодом, будет интерпретирован как «аргумент
не передан», и функция создаст новый список вместо того, чтобы изменить
переданный:

```python
def add_item_wrong(item: str, items: list[str] | None = None) -> list[str]:
    if not items:  # пустой список тоже "ложный"
        items = []

    items.append(item)
    return items


my_items = []
add_item_wrong("apple", my_items)
print(my_items)  # [] -- функция работала с другим списком!
```

---

## 3. Когда `None` — допустимое значение: `sentinel = object()`

Иногда `None` — это **осмысленное значение**, которое вызывающий код вправе
передать. Тогда по `None` нельзя понять, был ли аргумент передан вообще.

Пример: функция получения значения из словаря. Если ключа нет, а значение по
умолчанию не указано — нужно возбудить `KeyError`; если указано (в том числе
`None`) — вернуть его:

```python
def get_value(data: dict[str, int | None], key: str, default: int | None = None) -> int | None:
    if key in data:
        return data[key]

    if default is None:
        raise KeyError(key)

    return default


user_data = {"age": 30}

print(get_value(user_data, "city", 0))     # 0
print(get_value(user_data, "city"))        # KeyError: 'city' -- default не передан
print(get_value(user_data, "city", None))  # KeyError: 'city' -- а ожидалось None
```

С `None` в качестве значения по умолчанию вызовы `get_value(user_data, "city")`
и `get_value(user_data, "city", None)` неразличимы: во втором случае `None`
передан явно, но функция считает, что аргумент не указан.

Решение — создать **уникальный объект-маркер (sentinel)** и использовать его
в качестве значения по умолчанию. Простейший способ получить такой объект —
выражение `object()`: оно создает новый экземпляр, не равный по идентичности
никакому другому объекту. Маркер создается один раз, до определения функции,
и тот же объект служит значением по умолчанию при всех вызовах.

```python
sentinel = object()  # уникальный маркер "аргумент не передан"


def get_value(data: dict[str, int | None], key: str, default: object = sentinel) -> object:
    if key in data:
        return data[key]

    if default is sentinel:
        raise KeyError(key)

    return default


user_data = {"age": None}

print(get_value(user_data, "age"))         # None -- ключ есть, значение None
print(get_value(user_data, "city", None))  # None -- ключа нет, но None передан явно
print(get_value(user_data, "city", 0))     # 0
print(get_value(user_data, "city"))        # KeyError: 'city' -- default не передан
```

Маркер сравнивают только через `is`. Так как `sentinel` создан один раз на
уровне модуля и другие объекты не могут быть ему равны по идентичности,
вызывающий код не сможет передать его случайно.

---

## 4. Когда изменяемое значение по умолчанию используют намеренно

Иногда общий объект между вызовами — это именно то, что нужно. Например,
простейший кэш (запоминание уже вычисленных значений):

```python
def square(number: int, cache: dict[int, int] = {}) -> int:
    if number in cache:
        return cache[number]

    print("computing", number)
    cache[number] = number * number
    return cache[number]


print(square(4))
print(square(4))
```

Вывод:
```
computing 4
16
16
```

Второй вызов не пересчитывает результат, а берет его из общего словаря
`cache`.

Такой прием работает, но он **неочевиден** читателю кода и выглядит как
ошибка. Если вы к нему прибегаете, обязательно оставьте комментарий. Чаще
для этого используют специальные средства (например, `functools.cache`)
или хранят состояние в явном виде (в объекте, в замыкании).

---

## Вывод

- Значение по умолчанию создается один раз при `def`. Изменяемый объект
  (`[]`, `{}`, `set()`) в этой роли становится **общим для всех вызовов**,
  и его изменения накапливаются.
- Проблему не вызывают неизменяемые значения по умолчанию (`0`, `""`, `None`,
  `True`, кортежи).
- Стандартное решение: `parameter=None` в сигнатуре и
  `if parameter is None: parameter = []` в теле. Проверять нужно через
  `is None`, а не через `not parameter`.
- Если `None` — допустимое значение аргумента, используют уникальный
  маркер `sentinel = object()` и сравнивают с ним через `is`.
- Общий изменяемый объект между вызовами допустим только как осознанный
  прием (например, кэш) и должен быть прокомментирован.

---

## Источники

- [Python documentation. The Python Tutorial — Default Argument Values (Important warning)](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values);
- [Python documentation. Programming FAQ — Why are default values shared between objects?](https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects);
- [Python documentation. The Python Language Reference — Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).
