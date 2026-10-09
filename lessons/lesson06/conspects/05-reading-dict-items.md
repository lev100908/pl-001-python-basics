# Чтение элементов словаря

> **Главная мысль.** Значение по ключу читают тремя способами.
> **`my_dict[key]`** — самый прямой: если ключа нет, возбуждается
> `KeyError`. **`my_dict.get(key, default)`** — безопасное чтение: вместо
> ошибки возвращает `default` (по умолчанию `None`), словарь не меняется.
> **`my_dict.setdefault(key, default)`** — «модифицирующее» чтение: если
> ключа нет, **добавляет** его со значением `default` в словарь и возвращает
> это значение.

---

## 1. Чтение через квадратные скобки

Значение по ключу читается выражением `my_dict[key]`:

```python
user = {"name": "Alice", "age": 25}

print(user["name"])  # Alice
print(user["age"])   # 25
```

Поиск идет по **ключу**, а не по позиции: в отличие от списка, `user[0]`
будет искать ключ `0`, а не первую пару. Для поиска используется
хеш ключа, поэтому чтение происходит быстро независимо от размера словаря.

### Ошибка `KeyError`

Если запрошенного ключа в словаре нет, возбуждается исключение `KeyError`
— в его сообщении выводится отсутствующий ключ:

```python
user = {"name": "Alice", "age": 25}

print(user["city"])
# KeyError: 'city'
```

Поэтому чтение через `[]` подходит, когда наличие ключа **гарантировано**
логикой программы, а его отсутствие — действительно ошибка, о которой надо
сразу узнать. Если же отсутствие ключа — нормальная ситуация, лучше
использовать `get()`.

---

## 2. Метод `get()`

`my_dict.get(key, default=None)` возвращает значение по ключу `key`, а если
ключа нет — значение `default`. Ошибка не возбуждается, а словарь **не
меняется**.

Параметры метода:

- `key` — обязательный аргумент, ключ, по которому ищется значение;
- `default` — **необязательный** аргумент: значение, которое будет возвращено,
  если ключа `key` в словаре нет. Если `default` не передан, используется
  `None`. Если передан — вернется именно переданное значение (любого типа:
  число, строка, список и т. д.).

Аргумент `default` учитывается **только при отсутствии ключа**: если ключ
есть, `get()` вернет хранящееся в словаре значение, а `default` будет
проигнорирован. Передать `default` нужно позиционно — `user.get("city",
"unknown")`; запись `user.get("city", default="unknown")` приведет к
`TypeError`.

```python
user = {"name": "Alice", "age": 25}

print(user.get("name"))             # Alice
print(user.get("name", "unknown"))  # Alice -- ключ есть, default игнорируется
print(user.get("city"))             # None -- ключа нет, default не указан
print(user.get("city", "unknown"))  # unknown -- ключа нет, вернули переданный default
print(user)                         # {'name': 'Alice', 'age': 25} -- словарь не изменился
```

Обратите внимание: значение `default` лишь **возвращается** из `get()`, но в
словарь не записывается — ключ `"city"` в `user` так и не появился.

Типичное применение — счетчики и значения по умолчанию:

```python
text = "banana"
letters_count = {}

for letter in text:
    letters_count[letter] = letters_count.get(letter, 0) + 1

print(letters_count)  # {'b': 1, 'a': 3, 'n': 2}
```

Здесь, если буква встретилась впервые, `get()` вернет `0`, и счетчик
станет равным `1`; в противном случае к текущему значению прибавится
единица.

Если в словаре лежит значение `None`, то `get()` вернет `None` и когда ключ
есть, и когда его нет — по результату `get()` их не различить. В таких
случаях используйте оператор `in` (см. конспект про поиск в словаре).

---

## 3. Метод `setdefault()`

`my_dict.setdefault(key, default=None)` работает так:

- если ключ `key` **есть** в словаре — возвращает его текущее значение,
  словарь не меняется;
- если ключа **нет** — **добавляет** в словарь пару `key: default` и
  возвращает `default`.

То есть это чтение, которое при отсутствии ключа **модифицирует** словарь:

```python
user = {"name": "Alice"}

print(user.setdefault("name", "Bob"))  # Alice -- ключ был, значение не тронуто
print(user.setdefault("age", 25))      # 25 -- ключа не было, он добавлен
print(user)                            # {'name': 'Alice', 'age': 25}
```

Метод удобен при группировке, когда для каждого ключа нужно создать
изменяемое значение (например, список) при первом обращении:

```python
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
words_by_letter = {}

for word in words:
    words_by_letter.setdefault(word[0], []).append(word)

print(words_by_letter)
# {'a': ['apple', 'avocado'], 'b': ['banana', 'blueberry'], 'c': ['cherry']}
```

Выражение `words_by_letter.setdefault(word[0], [])` либо вернет уже
существующий список для этой буквы, либо создаст новый пустой список,
сохранит его в словаре и вернет его же — после этого в список можно
добавлять слово методом `append()`.

### Что выбрать

| Ситуация | Что выбрать |
|---|---|
| ключ **обязан** быть, отсутствие — ошибка | `my_dict[key]` |
| ключ может отсутствовать, словарь менять не нужно | `my_dict.get(key, default)` |
| ключ может отсутствовать, и его нужно сразу добавить | `my_dict.setdefault(key, default)` |

---

## Вывод

- `my_dict[key]` возвращает значение по ключу; при отсутствии ключа
  возбуждает `KeyError`.
- `my_dict.get(key, default)` возвращает значение или `default` (по
  умолчанию `None`) и никогда не меняет словарь.
- `my_dict.setdefault(key, default)` возвращает значение по ключу; если
  ключа нет, то сначала добавляет в словарь пару `key: default`.

---

## Источники

- [Python documentation. Built-in Types — Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict);
- [Python documentation. Built-in Types — dict.get()](https://docs.python.org/3/library/stdtypes.html#dict.get);
- [Python documentation. Built-in Types — dict.setdefault()](https://docs.python.org/3/library/stdtypes.html#dict.setdefault);
- [Python documentation. Built-in Exceptions — KeyError](https://docs.python.org/3/library/exceptions.html#KeyError).
