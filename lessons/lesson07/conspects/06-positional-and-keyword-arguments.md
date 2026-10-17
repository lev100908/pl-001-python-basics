# Позиционные, именованные, строго позиционные и строго именованные аргументы

> **Главная мысль.** При вызове функции аргументы можно передавать **по
> позиции** (`greet("Alice", "Hi")`) и **по имени** (`greet(name="Alice",
> greeting="Hi")`); все позиционные аргументы должны идти перед именованными.
> По умолчанию любой параметр функции можно передать и по позиции, и по имени.
> Python позволяет **ограничить** способ передачи с помощью двух специальных
> маркеров в списке параметров. Параметры **до `/`** — **строго позиционные**
> (positional-only, Python 3.8+): аргументы для них должны передаваться только
> по порядку. Параметры **после `*`** — **строго именованные** (keyword-only):
> аргументы для них должны передаваться только по имени. Параметры между `/` и
> `*` — «обычные»
> (positional-or-keyword). Ограничения нужны, чтобы сделать интерфейс функции
> понятнее, безопаснее и свободнее для будущих изменений.

---

## 1. Позиционные и именованные аргументы

Есть два основных способа сопоставить аргументы вызова с параметрами функции.

**Позиционные аргументы** сопоставляются с параметрами по **порядку**:
первый аргумент — первому параметру, второй — второму и т. д.

**Именованные аргументы (keyword arguments)** передаются в виде
`parameter_name=value` и сопоставляются с параметрами по **имени**, поэтому
их порядок не важен:

```python
def describe_user(name: str, age: int, city: str) -> str:
    return f"{name}, {age}, {city}"


print(describe_user("Alice", 25, "Paris"))                # Alice, 25, Paris -- по позиции
print(describe_user(city="Paris", name="Alice", age=25))  # Alice, 25, Paris -- по имени
```

Способы можно комбинировать, но **все позиционные аргументы должны идти
перед именованными**:

```python
print(describe_user("Alice", city="Paris", age=25))  # Alice, 25, Paris

print(describe_user(name="Alice", 25, "Paris"))  # SyntaxError: positional argument follows keyword argument
```

Именованные аргументы делают вызов самодокументируемым. Сравните
`create_window(800, 600, True, False)` и
`create_window(width=800, height=600, resizable=True, fullscreen=False)` —
во втором случае понятно, что означает каждое значение.

### Типичные ошибки при вызове

Если состав аргументов в вызове не соответствует сигнатуре функции, возникает
`TypeError`. Речь идет о **способе сопоставления**
аргументов с параметрами: не хватает обязательного аргумента, передан лишний
позиционный аргумент, указано имя, которого нет среди параметров, либо один
параметр получил значение дважды.

Каждая строка ниже — отдельный пример; формулировки сообщений приведены в
сокращенном виде и могут немного отличаться в разных версиях Python:

```python
describe_user("Alice", 25)                           # TypeError: missing 1 required positional argument: 'city'
describe_user("Alice", 25, "Paris", "extra")         # TypeError: takes 3 positional arguments but 4 were given
describe_user("Alice", 25, "Paris", country="FR")    # TypeError: got an unexpected keyword argument 'country'
describe_user("Alice", name="Bob", age=25, city="")  # TypeError: got multiple values for argument 'name'
```

Последняя ошибка возникает, когда один и тот же параметр получает значение
дважды: по позиции (`"Alice"` занял место параметра `name`) и по имени
(`name="Bob"`).

---

## 2. Общая схема списка параметров

В примере выше любой параметр можно было передать и по позиции, и по имени.
Способ передачи можно ограничить маркерами `/` и `*`:

```python
def function(positional_only: int, /, normal: int, *, keyword_only: int) -> None:
    ...
```

```
def function(  first, second,  /,  third, fourth,  *,  fifth, sixth  ):
               ───────────────      ───────────────      ──────────────
               только по позиции    по позиции или       только по имени
                                    по имени
```

| Вид параметров | Расположение | Способ передачи аргумента |
|---|---|---|
| строго позиционные | до `/` | только по позиции |
| обычные | между `/` и `*` (или без маркеров вообще) | по позиции **или** по имени |
| строго именованные | после `*` | только по имени |

Оба маркера необязательны: можно использовать только `/`, только `*` или оба.
Сами `/` и `*` — **не параметры**, а разделители, значения для них передавать
не нужно.

---

## 3. Строго именованные аргументы (keyword-only)

Аргументы для всех параметров, указанных **после одиночной звездочки `*`**,
должны передаваться только по имени:

```python
def create_window(width: int, height: int, *, resizable: bool, fullscreen: bool) -> str:
    return f"{width}x{height}, resizable={resizable}, fullscreen={fullscreen}"


print(create_window(800, 600, resizable=True, fullscreen=False))  # 800x600, resizable=True, fullscreen=False
print(create_window(800, 600, resizable=False, fullscreen=True))  # 800x600, resizable=False, fullscreen=True

print(create_window(800, 600, True, False))  # TypeError: takes 2 positional arguments but 4 were given
```

Здесь `width` и `height` можно передавать любым способом, а `resizable` и
`fullscreen` — только по имени.

Зачем это нужно:

- **читаемость вызовов.** Для логических флагов и настроек вызов
  `create_window(800, 600, True, False)` не говорит, что означают `True` и
  `False`, а `resizable=True, fullscreen=False` — говорит. Строго именованные
  параметры **принуждают** вызывающий код писать понятно;
- **защита от перепутанных аргументов.** Если параметров много и они одного
  типа, легко перепутать порядок; именованная передача исключает такую
  ошибку;
- **расширяемость.** Порядок строго именованных параметров не влияет на
  вызовы, поэтому их можно свободно переставлять в определении функции.

### Порядок строго именованных параметров

Строго именованные параметры передаются только по имени, поэтому порядок их
определения на вызов не влияет:

```python
def connect(host: str, *, port: int, user: str) -> str:
    return f"{user}@{host}:{port}"


print(connect("localhost", user="admin", port=5432))  # admin@localhost:5432
print(connect("localhost", port=5432, user="admin"))  # admin@localhost:5432
```

Если обязательный строго именованный аргумент не передан, возникает
`TypeError`:

```python
print(connect("localhost", port=5432))  # TypeError: missing 1 required keyword-only argument: 'user'
```

---

## 4. Строго позиционные аргументы (positional-only)

Начиная с Python 3.8 аргументы для всех параметров, указанных **перед `/`**,
должны передаваться только по позиции:

```python
def power(base: float, exponent: float, /) -> float:
    return base ** exponent


print(power(2, 10))  # 1024

print(power(base=2, exponent=10))  # TypeError: some positional-only arguments passed as keyword arguments
```

Многие встроенные функции именно так и устроены: например, у `len(obj, /)`
имя параметра не является частью публичного интерфейса, и передавать его по
имени нельзя (`len(obj=[1, 2, 3])` — `TypeError`). В этом можно убедиться
через `help(len)`: в сигнатуре есть символ `/`.

Зачем это нужно:

- **имя параметра не является частью интерфейса.** Если параметр позиционный,
  его можно свободно переименовать в будущем — внешний код, передающий
  значение по позиции, не сломается. Для обычного параметра переименование
  ломает все вызовы с `name=value`;
- **имя не имеет смысла.** У `len(obj)` или `power(base, exponent)` понятно и
  так, что передается, а имя параметра ничего не добавляет;
- **освобождение имен для `**kwargs`.** Строго позиционный параметр не
  конфликтует с именованными аргументами, попадающими в `**kwargs` (см. следующий
  конспект).

```python
def format_message(template: str, /, **values: str) -> str:
    return template.format(**values)


# параметр "template" -- позиционный, поэтому имя "template" можно использовать как ключ
print(format_message("{template} from {name}", template="Hello", name="Alice"))  # Hello from Alice
```

Без `/` вызов `format_message(..., template="Hello")` завершился бы ошибкой:
значение для `template` пришло бы дважды.

---

## 5. Комбинация `/` и `*`

Оба ограничения можно использовать одновременно:

```python
def build_url(scheme: str, host: str, /, port: int, *, path: str, secure: bool) -> str:
    protocol = f"{scheme}{'s' if secure else ''}"

    return f"{protocol}://{host}:{port}{path}"


print(build_url("http", "example.com", 80, path="/", secure=False))              # http://example.com:80/
print(build_url("http", "example.com", port=8080, path="/index", secure=False))  # http://example.com:8080/index
print(build_url("http", "example.com", 443, path="/", secure=True))              # https://example.com:443/
```

Здесь:

- `scheme`, `host` — строго позиционные;
- `port` — обычный (по позиции или по имени);
- `path`, `secure` — строго именованные.

---

## 6. Как выбрать

- **Обычные параметры — вариант без ограничений.** Не усложняйте интерфейс без
  причины.
- **Строго именованными** делайте флаги, настройки, необязательные параметры и
  вообще все, что при позиционной передаче будет выглядеть как «магическое
  значение» (`True`, `0`, `None`).
- **Строго позиционными** делайте параметры, у которых имя не несет смысла
  (`len(obj, /)`) или может измениться в будущем.
- Если вы раздумываете, нужен ли вам `/` — скорее всего, нет. Он встречается
  главным образом в библиотечном коде и встроенных функциях.

---

## Вывод

- Аргументы можно передавать по позиции и по имени; позиционные должны идти
  перед именованными. Если состав аргументов не соответствует сигнатуре
  (не хватает обязательного, лишний, неизвестное имя, значение дважды),
  возникает `TypeError`.
- Параметры **до `/`** — строго позиционные (Python 3.8+); параметры
  **после `*`** — строго именованные; все, что между ними, — обычные.
  Маркеры `/` и `*` сами параметрами не являются.
- Строго именованные параметры делают вызовы читаемыми и безопасными
  (особенно для флагов); порядок их определения не влияет на вызов.
- Строго позиционные параметры скрывают имя от публичного интерфейса: его можно
  безопасно менять, и оно не конфликтует с ключами `**kwargs`.
- Нарушение ограничений приводит к `TypeError`.

---

## Источники

- [Python documentation. The Python Tutorial — Keyword Arguments](https://docs.python.org/3/tutorial/controlflow.html#keyword-arguments);
- [Python documentation. The Python Tutorial — Special parameters](https://docs.python.org/3/tutorial/controlflow.html#special-parameters);
- [PEP 3102 — Keyword-Only Arguments](https://peps.python.org/pep-3102/);
- [PEP 570 — Python Positional-Only Parameters](https://peps.python.org/pep-0570/);
- [Python documentation. The Python Language Reference — Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions).
