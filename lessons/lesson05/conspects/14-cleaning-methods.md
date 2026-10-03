# Методы очистки строк

> **Главная мысль.** Данные из внешнего мира — пользовательский ввод,
> файлы, сеть — редко приходят «чистыми»: в них бывают лишние пробелы,
> переводы строк, служебные префиксы и суффиксы. Для очистки используют
> методы `strip()`, `lstrip()`, `rstrip()` (убирают символы с **краев**),
> `replace()` (заменяет подстроки **везде**), `removeprefix()` и
> `removesuffix()` (убирают **точный** префикс или суффикс). Все они
> возвращают **новую** строку.

---

## 1. Мотивация

Типичный пример: пользователь вводит команду и случайно оставляет пробел
в конце, а строка из файла приходит вместе с переводом строки `\n`.
Для компьютера `"yes "` и `"yes"` — разные строки, поэтому такие данные
нужно очищать, прежде чем с ними работать:

```python
answer = "  yes \n"

print(answer == "yes")          # False
print(answer.strip() == "yes")  # True
```

---

## 2. `strip()`, `lstrip()`, `rstrip()`

Эти методы убирают символы **с краев** строки (но не из середины):

- `strip()` — с обоих концов;
- `lstrip()` — только слева (left);
- `rstrip()` — только справа (right).

Без аргументов убираются **пробельные символы** (пробел, `\t`, `\n`,
`\r`, `\v`, `\f` и прочие пробельные символы Unicode):

```python
text = "  \t hello  world \n"

print(repr(text.strip()))   # 'hello  world'
print(repr(text.lstrip()))  # 'hello  world \n'
print(repr(text.rstrip()))  # '  \t hello  world'
```

Обратите внимание: пробелы **внутри** строки (между словами) остаются
нетронутыми.

### Аргумент: набор символов

Методам можно передать строку с символами, которые нужно убрать с краев.
**Важно:** аргумент — это не подстрока, а **набор отдельных символов**.
Метод удаляет с края любые символы из этого набора в любом порядке и
останавливается на первом символе, которого в наборе нет:

```python
print("***hello***".strip("*"))  # hello
print("xyxhelloyx".strip("xy"))  # hello
print("[1, 2, 3]".strip("[]"))   # 1, 2, 3
print("line\n".rstrip("\n"))     # line
```

Из-за этого `strip()` с аргументом часто ведет себя неожиданно, если
думать, что он удаляет подстроку целиком:

```python
print("happy.py".rstrip(".py"))  # ha -- удалены все символы '.', 'p', 'y' справа
```

Здесь вместо ожидаемого `happy` получилось `ha`: после удаления `.py`
справа метод продолжил удалять символы `p` и `y`, потому что они тоже
входят в набор `.py`. Для удаления **именно подстроки** предназначены
`removeprefix()` и `removesuffix()` (см. ниже).

Типичные применения: удалить знаки препинания по краям слов (вместе с
`string.punctuation`) и перевод строки при чтении:

```python
import string

word = "...Hello, world!!!"

print(word.strip(string.punctuation))  # Hello, world
```

---

## 3. `replace()`

Метод `replace(old, new)` возвращает копию строки, в которой **все**
вхождения подстроки `old` заменены на `new`. Необязательный третий
аргумент `count` ограничивает количество замен (считая слева):

```python
text = "one fish, two fish, red fish"

print(text.replace("fish", "cat"))     # one cat, two cat, red cat
print(text.replace("fish", "cat", 1))  # one cat, two fish, red fish
```

Если подстрока не найдена, возвращается строка без изменений. Замена
подстрокой `""` — это **удаление**:

```python
phone = "+7 (999) 123-45-67"

print(phone.replace(" ", ""))                   # +7(999)123-45-67
print(phone.replace(" ", "").replace("-", ""))  # +7(999)1234567
```

Замена работает **только по точному совпадению**, учитывает регистр и
не использует шаблоны (для шаблонов существует модуль `re`):

```python
print("Hello hello".replace("hello", "bye"))  # Hello bye -- "Hello" с заглавной не затронуто
```

Как и все остальные методы, `replace()` не изменяет исходную строку:

```python
original = "a-b-c"
changed = original.replace("-", "+")

print(original)  # a-b-c
print(changed)   # a+b+c
```

---

## 4. `removeprefix()` и `removesuffix()`

Методы `removeprefix(prefix)` и `removesuffix(suffix)` (появились в
Python 3.9) убирают **точную** подстроку в начале или в конце строки — и
**не более одного раза**. Если строка не начинается с префикса
(не заканчивается суффиксом), она возвращается без изменений:

```python
file_name = "report.txt"
url = "https://example.com"

print(file_name.removesuffix(".txt"))  # report
print(file_name.removesuffix(".csv"))  # report.txt -- такого суффикса нет
print(url.removeprefix("https://"))    # example.com
```

В отличие от `strip()`, они не «съедают» лишнего:

```python
print("happy.py".removesuffix(".py"))  # happy
print("ababab".removesuffix("ab"))     # abab -- убран только один суффикс
```

Это самый безопасный способ убрать расширение файла, протокол из адреса
или единицу измерения из значения.

---

## 5. Выбор метода

| Задача | Метод |
|---|---|
| убрать пробелы и переводы строк по краям | `strip()` / `lstrip()` / `rstrip()` |
| убрать с краев любые символы из набора | `strip(chars)` и аналоги |
| заменить или удалить подстроку **везде** | `replace(old, new)` |
| убрать конкретный префикс / суффикс | `removeprefix()` / `removesuffix()` |

Для очистки данных эти методы часто объединяют в **цепочку**.

---

## Вывод

- `strip()`, `lstrip()`, `rstrip()` убирают символы с краев строки (по
  умолчанию — пробельные); середину строки не затрагивают.
- Аргумент `strip(chars)` — это **набор символов**, а не подстрока:
  `"happy.py".rstrip(".py")` вернет `"ha"`.
- `replace(old, new, count)` заменяет **все** (или первые `count`)
  вхождения подстроки; замена на `""` удаляет подстроку.
- `removeprefix()` / `removesuffix()` убирают **точный** префикс / суффикс
  не более одного раза — безопасная альтернатива `strip()` для подстрок.
- Все методы возвращают **новую** строку; результат нужно сохранять.

---

## Источники

- [Python documentation. Built-in Types — str.strip(), str.lstrip(), str.rstrip()](https://docs.python.org/3/library/stdtypes.html#str.strip);
- [Python documentation. Built-in Types — str.replace()](https://docs.python.org/3/library/stdtypes.html#str.replace);
- [Python documentation. Built-in Types — str.removeprefix(), str.removesuffix()](https://docs.python.org/3/library/stdtypes.html#str.removeprefix);
- [PEP 616 — String methods to remove prefixes and suffixes](https://peps.python.org/pep-0616/).
