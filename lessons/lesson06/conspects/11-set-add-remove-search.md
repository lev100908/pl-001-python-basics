# Добавление, удаление и поиск элементов множества

> **Главная мысль.** Элемент добавляют методом **`add()`**, несколько
> элементов сразу — методом **`update()`**. Удалять можно методами
> **`remove()`** (ошибка `KeyError`, если элемента нет), **`discard()`**
> (молча ничего не делает, если элемента нет), **`pop()`** (удаляет и
> возвращает **произвольный** элемент) и **`clear()`** (удаляет все).
> Поиск элемента — оператор **`in`**: у множества нет индексов, а значит
> нет и методов вроде `index()` или `find()`; зато проверка принадлежности
> выполняется практически мгновенно.

---

## 1. Добавление элементов

### `add()`

`my_set.add(element)` добавляет **один** элемент. Если такой элемент уже
есть, множество не меняется (и ошибки нет). Метод изменяет множество на
месте и возвращает `None`. Добавляемый элемент должен быть хешируемым:

```python
colors = {"red", "green"}

colors.add("blue")
colors.add("red")  # такой элемент уже есть -- ничего не изменилось

print(sorted(colors))  # ['blue', 'green', 'red']

colors.add(["black"])
# TypeError: unhashable type: 'list'
```

### `update()`

`my_set.update(iterable)` добавляет **все элементы** переданного
итерируемого объекта (список, кортеж, строка, другое множество и т. д.).
Можно передать сразу несколько итерируемых объектов через запятую:

```python
numbers = {1, 2, 3}

numbers.update([3, 4, 5])
numbers.update({5, 6}, (7, 8))

print(numbers)  # {1, 2, 3, 4, 5, 6, 7, 8}
```

Нужно различать: `add("abc")` добавит *одну строку* `"abc"`, а
`update("abc")` — *три символа* `"a"`, `"b"`, `"c"`, потому что строка — это
итерируемый объект:

```python
letters = set()

letters.add("abc")
print(letters)  # {'abc'}

letters.update("abc")
print(sorted(letters))  # ['a', 'abc', 'b', 'c']
```

---

## 2. Удаление элементов

### `remove()`

`my_set.remove(element)` удаляет элемент. Если элемента нет, возбуждается
`KeyError`:

```python
colors = {"red", "green", "blue"}

colors.remove("green")
print(sorted(colors))  # ['blue', 'red']

colors.remove("yellow")
# KeyError: 'yellow'
```

### `discard()`

`my_set.discard(element)` удаляет элемент, если он есть, а если нет — **не
делает ничего** и не возбуждает ошибку:

```python
colors = {"red", "green", "blue"}

colors.discard("green")
colors.discard("yellow")  # элемента нет -- ошибки нет

print(sorted(colors))  # ['blue', 'red']
```

`remove()` стоит использовать, когда отсутствие элемента — признак ошибки в
программе, а `discard()` — когда нужно просто гарантировать, что элемента в
множестве нет.

### `pop()`

`my_set.pop()` удаляет и возвращает **произвольный** элемент множества.
Так как множество неупорядочено, нельзя заранее сказать, какой именно
элемент будет удален (в отличие от `list.pop()`, который удаляет последний
элемент или элемент по индексу). У `pop()` нет аргументов, а на пустом
множестве метод возбуждает `KeyError`:

```python
numbers = {10, 20, 30}

removed_number = numbers.pop()

print(removed_number in {10, 20, 30})  # True -- какой-то из элементов
print(len(numbers))                    # 2

set().pop()
# KeyError: 'pop from an empty set'
```

Метод пригодится, когда нужно по очереди «разобрать» множество, не
заботясь о порядке:

```python
tasks = {"write", "test", "deploy"}

while tasks:
    task = tasks.pop()

    print("Processing:", task)
```

### `clear()`

`my_set.clear()` удаляет **все** элементы, оставляя пустое множество (сам
объект сохраняется):

```python
numbers = {1, 2, 3}

numbers.clear()

print(numbers)  # set()
```

### Сводка

| Метод | Что делает | Если элемента нет |
|---|---|---|
| `add(x)` | добавляет элемент | — (если уже есть, ничего не происходит) |
| `update(iterable)` | добавляет все элементы итерируемого объекта | — |
| `remove(x)` | удаляет элемент | `KeyError` |
| `discard(x)` | удаляет элемент | ничего не происходит |
| `pop()` | удаляет и возвращает произвольный элемент | `KeyError` (для пустого множества) |
| `clear()` | удаляет все элементы | — |

---

## 3. Поиск элементов

Поскольку у множества нет индексов, **найти позицию** элемента нельзя —
методов `index()` или `find()` у `set` нет. Единственный вид поиска — это
проверка **принадлежности**: оператор `in` возвращает `True`, если элемент
есть в множестве, а `not in` — если его нет:

```python
colors = {"red", "green", "blue"}

print("red" in colors)         # True
print("yellow" in colors)      # False
print("yellow" not in colors)  # True
```

Проверка `in` во множестве, как и поиск ключа в словаре, использует хеш
элемента и выполняется за примерно постоянное время, не зависящее от размера
множества (в списке же `in` перебирает все элементы по очереди). Поэтому
множество — хороший выбор, когда нужно часто проверять, есть ли значение в
наборе, например, в списке допустимых значений:

```python
allowed_names = {"alice", "bob", "charlie"}  # множество допустимых имен

user_name = "bob"

if user_name in allowed_names:
    print("Access granted")

else:
    print("Access denied")
```

Вывод:
```
Access granted
```

Если искомый объект нехешируемый, `in` возбуждает `TypeError`:

```python
print([1, 2] in {1, 2, 3})
# TypeError: unhashable type: 'list'
```

---

## Вывод

- `add(x)` добавляет один элемент, `update(iterable)` — все элементы
  итерируемого объекта; дубликаты во множество не попадают.
- `remove(x)` удаляет элемент и возбуждает `KeyError`, если его нет;
  `discard(x)` в этом случае ничего не делает.
- `pop()` удаляет и возвращает **произвольный** элемент (на пустом множестве
  — `KeyError`); `clear()` удаляет все элементы.
- Поиск во множестве — оператор `in` / `not in`; он работает быстро
  (по хешу). Позицию элемента узнать нельзя — индексов нет.

---

## Источники

- [Python documentation. Built-in Types — Set Types — set, frozenset](https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset);
- [Python documentation. Built-in Types — set.add(), set.update()](https://docs.python.org/3/library/stdtypes.html#set.add);
- [Python documentation. The Python Tutorial — Sets](https://docs.python.org/3/tutorial/datastructures.html#sets).
