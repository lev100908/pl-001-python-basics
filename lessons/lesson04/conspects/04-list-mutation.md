# Изменение списка: срезы, методы, `del`

> **Главная мысль.** Список изменяем, поэтому его содержимое можно менять
> тремя способами: присваиванием по индексу или срезу, специальными
> **методами** (`append()`, `insert()`, `extend()`, `remove()`, `pop()` и
> другими) и ключевым словом `del`. Все эти способы изменяют исходный
> объект списка «на месте», не создавая новый список.

---

## 1. Изменение и удаление элементов с помощью срезов

### Изменение одного элемента по индексу

Присваивание по индексу заменяет элемент в соответствующей позиции:

```python
fruits = ["apple", "banana", "cherry"]
fruits[1] = "blueberry"

print(fruits)  # ['apple', 'blueberry', 'cherry']
```

### Изменение диапазона элементов через срез

Присваивание списка (или любого итерируемого объекта) срезу заменяет
сразу весь диапазон — при этом **количество новых элементов не обязано
совпадать** с количеством элементов в исходном диапазоне: список
автоматически «сжимается» или «расширяется»:

```python
numbers = [0, 1, 2, 3, 4, 5]
numbers[1:4] = [10, 20]

print(numbers)  # [0, 10, 20, 4, 5] -- три элемента заменились на два
```

### Добавление элементов через «пустой» срез

Если в качестве среза указать диапазон нулевой длины (`start == stop`),
присваивание не заменяет ничего, а **вставляет** новые элементы в
указанную позицию, расширяя список:

```python
letters = ["a", "b", "c"]
letters[1:1] = ["x", "y"]

print(letters)  # ['a', 'x', 'y', 'b', 'c']
```

### Удаление элементов через срез

Присваивание пустого списка срезу удаляет соответствующий диапазон
элементов:

```python
numbers = [0, 1, 2, 3, 4, 5]
numbers[1:4] = []

print(numbers)  # [0, 4, 5]
```

---

## 2. Изменение и удаление элементов с помощью методов

У списка есть набор методов, изменяющих его «на месте» (сам объект
списка не пересоздается, меняется его содержимое):

| Метод | Что делает | Возможные исключения |
|---|---|---|
| `append(value)` | добавляет один элемент в конец | — |
| `insert(index, value)` | вставляет элемент в указанную позицию, если `index` выходит за границы, элемент вставляется в начало или в конец | — |
| `extend(iterable)` | добавляет в конец все элементы другого итерируемого объекта | `TypeError`, если аргумент не итерируемый |
| `remove(value)` | удаляет первое вхождение значения | `ValueError`, если значения нет в списке |
| `pop(index)` | удаляет и возвращает элемент по индексу (по умолчанию — последний) | `IndexError`, если список пуст или индекс выходит за границы |
| `clear()` | удаляет все элементы, список становится пустым | — |
| `sort()` | сортирует элементы списка на месте | `TypeError`, если элементы нельзя сравнивать между собой |
| `reverse()` | разворачивает порядок элементов на месте | — |

Примеры использования:

```python
groceries = ["milk", "bread"]

groceries.append("eggs")
print(groceries)  # ['milk', 'bread', 'eggs']

groceries.insert(1, "butter")
print(groceries)  # ['milk', 'butter', 'bread', 'eggs']

groceries.extend(["tea", "coffee"])
print(groceries)  # ['milk', 'butter', 'bread', 'eggs', 'tea', 'coffee']

groceries.remove("butter")
print(groceries)  # ['milk', 'bread', 'eggs', 'tea', 'coffee']

last_item = groceries.pop()
print(last_item)  # coffee
print(groceries)  # ['milk', 'bread', 'eggs', 'tea']

first_item = groceries.pop(0)
print(first_item)  # milk
print(groceries)   # ['bread', 'eggs', 'tea']

groceries.sort()
print(groceries)  # ['bread', 'eggs', 'tea']

groceries.reverse()
print(groceries)  # ['tea', 'eggs', 'bread']

groceries.clear()
print(groceries)  # []
```

**Важно**: `append(value)` добавляет ровно один элемент, даже если
значение само является списком (в отличие от `extend()`, который
«разворачивает» аргумент на отдельные элементы):

```python
numbers = [1, 2, 3]

numbers.append([4, 5])
print(numbers)  # [1, 2, 3, [4, 5]]     -- один новый элемент — список

another_numbers = [1, 2, 3]

another_numbers.extend([4, 5])
print(another_numbers)  # [1, 2, 3, 4, 5]  -- два новых элемента
```

Также у списка есть вспомогательные методы, которые **не изменяют**
список, а только читают информацию о нем:

```python
numbers = [3, 1, 4, 1, 5]

print(numbers.index(4))  # 2  -- индекс первого вхождения значения
print(numbers.count(1))  # 2  -- сколько раз значение встречается в списке
print(numbers.copy())    # [3, 1, 4, 1, 5] -- независимая поверхностная копия
```

Метод `index(value)` возбуждает `ValueError`, если значения нет в списке;
`count()` и `copy()` исключений не возбуждают.

---

## 3. Удаление элементов с помощью `del`

Ключевое слово `del` позволяет удалить элемент по индексу или диапазон элементов по
срезу. В отличие от `pop()`, `del` **не возвращает** удаленное значение —
это отдельная инструкция, а не выражение:

```python
numbers = [10, 20, 30, 40, 50]

del numbers[0]
print(numbers)  # [20, 30, 40, 50]

del numbers[1:3]
print(numbers)  # [20, 50]
```

Если индекс выходит за границы списка, `del` (как и присваивание по
индексу `list[i] = value`) возбуждает `IndexError`. Срезы же за границы
не выходят — они просто обрезаются, поэтому исключения не возникает:

```python
numbers = [10, 20, 30]

del numbers[5]  # IndexError: list assignment index out of range

del numbers[1:100]  # исключения нет -- срез обрезается до границ списка
print(numbers)      # [10]
```

`del`, примененный ко всему списку целиком через срез `[:]`, очищает его
содержимое (эквивалент `clear()`), а `del` без среза, примененный к самой
переменной, удаляет саму переменную (после этого обращение к ней поднимет
`NameError`):

```python
values = [1, 2, 3]
del values[:]
print(values)  # []

del values
print(values)
# NameError: name 'values' is not defined -- переменная values больше не существует
```

---

## Вывод

- Присваивание по индексу (`list[i] = value`) заменяет один элемент;
  присваивание по срезу (`list[a:b] = iterable`) заменяет, вставляет
  (при `a == b`) или удаляет (при пустом правом операнде) целый диапазон.
- Методы `append()`, `insert()`, `extend()`, `remove()`, `pop()`,
  `clear()`, `sort()`, `reverse()` изменяют список «на месте»; `index()`,
  `count()`, `copy()` список не меняют, а только читают информацию о нем.
- Методы возбуждают исключения, если действие невозможно: `pop()` —
  `IndexError` (пустой список или неверный индекс), `remove()` и
  `index()` — `ValueError` (значения нет в списке), `extend()` и
  `sort()` — `TypeError`. Выход индекса за границы при `del list[i]` и
  `list[i] = value` — `IndexError`; срезы исключений не вызывают.
- `del list[i]` и `del list[a:b]` удаляют элемент или диапазон по индексу
  без возврата значения; `del имя_переменной` удаляет саму переменную.

---

## Источники

- [Python documentation. Built-in Types — Mutable Sequence Types](https://docs.python.org/3/library/stdtypes.html#mutable-sequence-types);
- [Python documentation. The Python Tutorial — More on Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists);
- [Python documentation. The Python Language Reference — The del statement](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement);
- [Python documentation. Built-in Types — list.sort()](https://docs.python.org/3/library/stdtypes.html#list.sort).
