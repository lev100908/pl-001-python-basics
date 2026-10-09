# Методы итерирования словарей: keys, values, items

> **Главная мысль.** Обычный цикл `for` по словарю обходит его **ключи**.
> Чтобы обойти **значения** или **пары «ключ — значение»**, используют
> методы `values()` и `items()`; метод `keys()` явно возвращает ключи. Эти
> методы возвращают не списки, а **объекты-представления (view objects)** —
> «окна» в словарь, которые всегда отражают его актуальное состояние.
> Изменять **размер** словаря (добавлять и удалять ключи) во время обхода
> нельзя — это приводит к `RuntimeError`.

---

## 1. Обход ключей

Цикл `for` по самому словарю перебирает ключи в порядке вставки:

```python
prices = {"apple": 100, "banana": 60, "cherry": 250}

for name in prices:
    print(name)
```

Вывод:
```
apple
banana
cherry
```

---

## 2. Методы `keys()`, `values()` и `items()`

| Метод | Что возвращает | Тип результата |
|---|---|---|
| `keys()` | ключи словаря | `dict_keys` |
| `values()` | значения словаря | `dict_values` |
| `items()` | пары `(ключ, значение)` в виде кортежей | `dict_items` |

```python
prices = {"apple": 100, "banana": 60, "cherry": 250}

print(prices.keys())    # dict_keys(['apple', 'banana', 'cherry'])
print(prices.values())  # dict_values([100, 60, 250])
print(prices.items())   # dict_items([('apple', 100), ('banana', 60), ('cherry', 250)])
```

Все три результата можно обходить в цикле `for`. Пары из `items()` удобно
сразу **распаковывать** в две переменные:

```python
for price in prices.values():
    print(price)
```

Вывод:
```
100
60
250
```

```python
for name, price in prices.items():
    print(name, "costs", price)
```

Вывод:
```
apple costs 100
banana costs 60
cherry costs 250
```

Метод `keys()` обходит ключи так же, как и обычный цикл по словарю, но
делает это явно: цикл `for name in prices.keys()` эквивалентен циклу
`for name in prices`. На практике чаще пишут короткий вариант.

Благодаря тому, что `values()` и `items()` возвращают итерируемые объекты,
их результат можно передавать в функции вроде `sum()`, `max()`, `sorted()`,
а также в конструкторы `list()`, `set()` и `dict()`:

```python
prices = {"apple": 100, "banana": 60, "cherry": 250}

print(sum(prices.values()))    # 410
print(max(prices.values()))    # 250
print(list(prices.keys()))     # ['apple', 'banana', 'cherry']
print(sorted(prices.items()))  # [('apple', 100), ('banana', 60), ('cherry', 250)]
```

---

## 3. Объекты-представления (view objects)

Методы `keys()`, `values()` и `items()` возвращают **объекты-представления**
(`dict_keys`, `dict_values`, `dict_items`). Это специальные легковесные
объекты, которые:

- **не копируют** данные словаря, а лишь дают доступ к ним — поэтому их
  создание выполняется очень быстро и не зависит от размера словаря;
- **динамичны** — отражают текущее содержимое словаря: если словарь изменился
  после создания представления, представление «увидит» эти изменения;
- **итерируемы**, поддерживают `len()` и проверку `in`;
- не являются списками: у них нет индексов и срезов. Если нужен именно
  список, представление можно превратить в него с помощью вызова `list()`.

```python
prices = {"apple": 100, "banana": 60}
names_view = prices.keys()

print(names_view)  # dict_keys(['apple', 'banana'])

prices["cherry"] = 250

print(names_view)       # dict_keys(['apple', 'banana', 'cherry']) -- представление обновилось
print(len(names_view))  # 3

print(names_view[0])
# TypeError: 'dict_keys' object is not subscriptable

names_list = list(names_view)  # "снимок" ключей в виде обычного списка

print(names_list[0])  # apple
```

Представления `keys()` и `items()` ведут себя как множества (с ними можно
выполнять операции над множествами — подробнее на семинаре), потому что
ключи уникальны.

---

## 4. Опасность модификации словаря во время итерирования

Во время обхода словаря нельзя менять его **размер**: добавлять новые ключи
или удалять существующие. Python отслеживает размер словаря в процессе
итерирования и при его изменении возбуждает `RuntimeError`:

```python
numbers = {"a": 1, "b": 2, "c": 3}

for key in numbers:
    if numbers[key] == 1:
        del numbers[key]
# RuntimeError: dictionary changed size during iteration
```

Аналогичная ошибка возникает при добавлении нового ключа в цикле.

Безопасные варианты:

- **изменение значений** существующих ключей разрешено — размер словаря при
  этом не меняется:

  ```python
  numbers = {"a": 1, "b": 2, "c": 3}

  for key in numbers:
      numbers[key] *= 10

  print(numbers)  # {'a': 10, 'b': 20, 'c': 30}
  ```

- если нужно **удалить или добавить** ключи, обходите **копию** (снимок)
  ключей — например, `list(numbers)` или `list(numbers.items())`; сам
  словарь в этот момент можно спокойно менять:

  ```python
  numbers = {"a": 1, "b": 2, "c": 3}

  for key in list(numbers):
      if numbers[key] % 2 == 1:
          del numbers[key]

  print(numbers)  # {'b': 2}
  ```

- **построение нового** словаря — например, с помощью словарного
  включения:

  ```python
  numbers = {"a": 1, "b": 2, "c": 3}

  even_numbers = {key: value for key, value in numbers.items() if value % 2 == 0}

  print(even_numbers)  # {'b': 2}
  ```

---

## Вывод

- `for key in my_dict` обходит ключи; значения и пары получают через
  `values()` и `items()` (пары удобно распаковывать:
  `for key, value in my_dict.items()`).
- `keys()`, `values()` и `items()` возвращают **объекты-представления**
  (`dict_keys`, `dict_values`, `dict_items`) — динамичные «окна» в словарь,
  а не копии и не списки. Для получения списка — `list(...)`.
- Менять размер словаря (добавлять и удалять ключи) во время обхода нельзя —
  будет `RuntimeError: dictionary changed size during iteration`. Значения
  существующих ключей менять можно. Для добавления и удаления — обходить
  копию ключей или создавать новый словарь.

---

## Источники

- [Python documentation. Built-in Types — Dictionary view objects](https://docs.python.org/3/library/stdtypes.html#dictionary-view-objects);
- [Python documentation. The Python Tutorial — Looping Techniques](https://docs.python.org/3/tutorial/datastructures.html#looping-techniques);
- [Python documentation. Built-in Types — dict.keys(), dict.values(), dict.items()](https://docs.python.org/3/library/stdtypes.html#dict.items).
