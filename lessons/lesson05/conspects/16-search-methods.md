# Методы поиска в строках

> **Главная мысль.** Методы `startswith()` и `endswith()` проверяют, начинается
> ли (заканчивается ли) строка заданной подстрокой, и возвращают `bool`.
> Методы `find()` / `rfind()` и `index()` / `rindex()` находят **индекс**
> подстроки — первого вхождения (слева) или последнего (справа). Отличие
> внутри пар: `find()` при неудаче возвращает `-1`, а `index()` возбуждает
> `ValueError`. Если нужно лишь узнать, **есть** ли подстрока, достаточно
> оператора `in`.

---

## 1. `startswith()` и `endswith()`

`startswith(prefix)` возвращает `True`, если строка **начинается** с
подстроки `prefix`, а `endswith(suffix)` — если **заканчивается** на `suffix`.
Поиск **регистрозависим**:

```python
file_name = "report_2024.txt"

print(file_name.startswith("report"))  # True
print(file_name.startswith("Report"))  # False -- регистр важен
print(file_name.endswith(".txt"))      # True
print(file_name.endswith(".csv"))      # False
```

Вместо одной подстроки можно передать **кортеж** подстрок — результат будет
`True`, если строка начинается (заканчивается) хотя бы одной из них. Это
позволяет обойтись без цепочек `or`:

```python
url = "https://example.com"
image = "photo.PNG"

print(url.startswith(("http://", "https://")))           # True
print(image.lower().endswith((".png", ".jpg", ".gif")))  # True
```

Необязательные аргументы `start` и `end` ограничивают проверяемый участок
строки (позиции считаются как в срезах):

```python
print("hello world".startswith("world", 6))  # True -- проверяем с индекса 6
```

---

## 2. `find()` и `rfind()`

`find(sub)` возвращает **индекс первого вхождения** подстроки `sub`
(начало подстроки), считая слева. Если подстроки нет — возвращается `-1`.
`rfind(sub)` ищет **справа**, то есть возвращает индекс **последнего**
вхождения:

```python
text = "banana"

print(text.find("an"))   # 1  -- первое вхождение
print(text.rfind("an"))  # 3  -- последнее вхождение
print(text.find("a"))    # 1
print(text.rfind("a"))   # 5
print(text.find("xyz"))  # -1 -- не найдено
```

Подстрока может состоять из любого количества символов, а поиск
регистрозависим.

Необязательные аргументы `start` и `end` задают участок поиска — это
позволяет продолжать поиск после уже найденного вхождения:

```python
text = "banana"

print(text.find("an", 2))     # 3 -- поиск начинается с индекса 2
print(text.find("an", 2, 4))  # -1 -- в срезе text[2:4] == "na" подстроки нет
```

Так можно найти **все** вхождения подстроки:

```python
text = "banana"
position = text.find("an")

while position != -1:
    print(position)
    position = text.find("an", position + 1)
```

Вывод:
```
1
3
```

---

## 3. `index()` и `rindex()`

Методы `index()` и `rindex()` работают так же, как `find()` и `rfind()`, но
если подстрока не найдена, **возбуждают `ValueError`** вместо возврата `-1`:

```python
text = "banana"

print(text.index("an"))   # 1
print(text.rindex("an"))  # 3

print(text.index("xyz"))
# ValueError: substring not found
```

### `find()` или `index()`

| Ситуация | Что выбрать |
|---|---|
| отсутствие подстроки — нормальный случай, который нужно обработать | `find()` |
| подстрока **обязана** быть; ее отсутствие — ошибка в данных | `index()` — программа сразу сообщит о проблеме |
| нужно только узнать, есть ли подстрока | оператор `in` |

---

## Вывод

- `startswith()` / `endswith()` проверяют начало и конец строки; принимают
  **кортеж** вариантов; результат — `bool`.
- `find()` возвращает индекс **первого** вхождения подстроки (слева), `rfind()` —
  **последнего** (справа). Если подстроки нет — `-1`.
- `index()` / `rindex()` ведут себя так же, но при неудаче возбуждают
  `ValueError`.
- Все методы поиска **регистрозависимы** и принимают необязательные
  границы `start` и `end`.

---

## Источники

- [Python documentation. Built-in Types — str.startswith(), str.endswith()](https://docs.python.org/3/library/stdtypes.html#str.startswith);
- [Python documentation. Built-in Types — str.find(), str.rfind()](https://docs.python.org/3/library/stdtypes.html#str.find);
- [Python documentation. Built-in Types — str.index(), str.rindex()](https://docs.python.org/3/library/stdtypes.html#str.index).
