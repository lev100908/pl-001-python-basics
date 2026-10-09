# Удаление элементов словаря

> **Главная мысль.** Удалить пару из словаря можно четырьмя способами.
> **`del my_dict[key]`** удаляет пару по ключу (`KeyError`, если ключа
> нет). **`my_dict.pop(key, default)`** удаляет пару и **возвращает
> значение**; с `default` не возбуждает ошибку. **`my_dict.popitem()`**
> удаляет и возвращает **последнюю добавленную** пару. **`my_dict.clear()`**
> удаляет **все** пары, оставляя пустой словарь.

---

## 1. Оператор `del`

`del my_dict[key]` удаляет пару с ключом `key`. Если такого ключа нет —
возбуждается `KeyError`:

```python
user = {"name": "Alice", "age": 25, "city": "Paris"}

del user["city"]

print(user)  # {'name': 'Alice', 'age': 25}

del user["job"]
# KeyError: 'job'
```

Оператор `del` ничего не возвращает: удаленное значение «теряется». Если оно
нужно — используйте `pop()`.

---

## 2. Метод `pop()`

`my_dict.pop(key[, default])` удаляет пару с ключом `key` и **возвращает ее
значение**. Если ключа нет:

- когда `default` **не указан** — возбуждается `KeyError`;
- когда `default` **указан** — возвращается `default`, ошибки нет, словарь
  не меняется.

```python
user = {"name": "Alice", "age": 25, "city": "Paris"}

removed_city = user.pop("city")

print(removed_city)  # Paris
print(user)          # {'name': 'Alice', 'age': 25}

print(user.pop("job", None))  # None -- ключа нет, вернули default
print(user.pop("job"))
# KeyError: 'job'
```

Форма `pop(key, default)` позволяет «удалить ключ, если он есть» без
дополнительной проверки и без `try/except`:

```python
user.pop("job", None)  # безопасно: если ключа нет, ничего не произойдет
```

---

## 3. Метод `popitem()`

`my_dict.popitem()` удаляет и возвращает **последнюю добавленную** пару в
виде кортежа `(ключ, значение)` (порядок **LIFO** — последним пришел,
первым вышел). Для пустого словаря возбуждается `KeyError`. Метод
не принимает аргументов:

```python
user = {"name": "Alice", "age": 25, "city": "Paris"}

last_item = user.popitem()
print(last_item)  # ('city', 'Paris')
print(user)       # {'name': 'Alice', 'age': 25}

key, value = user.popitem()  # результат можно сразу распаковать
print(key, value)  # age 25

empty_dict = {}
empty_dict.popitem()
# KeyError: 'popitem(): dictionary is empty'
```

Метод подходит, например, для разбора словаря «с конца» в цикле `while`:

```python
tasks = {"first": "write", "second": "test", "third": "deploy"}

while tasks:
    task_name, task_action = tasks.popitem()
    print(task_name, task_action)
```

Вывод:
```
third deploy
second test
first write
```

---

## 4. Метод `clear()`

`my_dict.clear()` удаляет **все** пары, оставляя пустой словарь. Объект
остается тем же самым (в отличие от присваивания `my_dict = {}`, которое
создает *новый* объект и лишь перепривязывает имя):

```python
user = {"name": "Alice", "age": 25}
same_user = user  # вторая ссылка на тот же словарь

user.clear()

print(user)       # {}
print(same_user)  # {} -- словарь один, поэтому очистился и по второй ссылке
```

### Что выбрать

| Задача | Что использовать |
|---|---|
| удалить пару по ключу, ключ точно есть | `del my_dict[key]` |
| удалить пару и получить ее значение | `my_dict.pop(key)` |
| удалить, если ключ есть, без ошибки | `my_dict.pop(key, None)` |
| удалить последнюю добавленную пару | `my_dict.popitem()` |
| удалить все пары | `my_dict.clear()` |

---

## Вывод

- `del my_dict[key]` удаляет пару по ключу; при отсутствии ключа —
  `KeyError`.
- `my_dict.pop(key, default)` удаляет пару и возвращает значение; если ключа
  нет — возвращает `default` (или возбуждает `KeyError`, если `default` не
  указан).
- `my_dict.popitem()` удаляет и возвращает последнюю добавленную пару как
  кортеж `(ключ, значение)`; на пустом словаре — `KeyError`.
- `my_dict.clear()` очищает словарь, сохраняя сам объект.

---

## Источники

- [Python documentation. The Python Tutorial — Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries);
- [Python documentation. Built-in Types — dict.pop(), dict.popitem(), dict.clear()](https://docs.python.org/3/library/stdtypes.html#dict.pop);
- [Python documentation. Simple statements — The del statement](https://docs.python.org/3/reference/simple_stmts.html#the-del-statement).
