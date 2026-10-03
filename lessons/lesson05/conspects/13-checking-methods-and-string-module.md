# Методы проверки строк и модуль `string`

> **Главная мысль.** Методы `islower()`, `isupper()`, `isalpha()`, `isdigit()`,
> `isalnum()` и `isspace()` отвечают на вопрос «из каких символов состоит
> строка?» и возвращают `bool`. Все они возвращают `False` для **пустой
> строки**. Эти методы учитывают весь Unicode, а не только латиницу и
> цифры `0`–`9`. Если нужен именно **ASCII-набор символов**, используют константы
> модуля `string`: `ascii_lowercase`, `digits`, `punctuation` и другие.

---

## 1. Методы проверки

Эти методы **ничего не изменяют** — они проверяют строку и возвращают
`True` или `False`. Типичные применения — проверить, что введенное
значение состоит из ожидаемых символов, прежде чем с ним работать, и
отсечь заведомо некорректные данные.

### Проверка регистра: `islower()`, `isupper()`

- `islower()` — `True`, если в строке есть хотя бы одна буква, и **все буквы
  строчные**;
- `isupper()` — аналогично для заглавных.

Символы, не являющиеся буквами (цифры, пробелы, знаки), проверку не
затрагивают:

```python
print("hello".islower())      # True
print("hello 123".islower())  # True  -- цифры и пробел не мешают
print("Hello".islower())      # False -- есть заглавная буква
print("123".islower())        # False -- в строке нет ни одной буквы

print("HELLO".isupper())        # True
print("HELLO world".isupper())  # False
```

### Проверка состава: `isalpha()`, `isdigit()`, `isalnum()`

- `isalpha()` — `True`, если строка непустая и **все символы — буквы**;
- `isdigit()` — `True`, если строка непустая и **все символы — цифры**;
- `isalnum()` — `True`, если строка непустая и все символы — **буквы или
  цифры**.

```python
print("hello".isalpha())        # True
print("hello world".isalpha())  # False -- пробел не буква
print("hello1".isalpha())       # False

print("12345".isdigit())  # True
print("-5".isdigit())     # False -- минус не цифра
print("3.14".isdigit())   # False -- точка не цифра

print("abc123".isalnum())   # True
print("abc_123".isalnum())  # False -- подчеркивание не буква и не цифра
```

Буквами для `isalpha()` считаются буквы **любых алфавитов**, а не только
латинские:

```python
print("é".isalpha())       # True
print("\u03c0".isalpha())  # True -- греческая буква "пи"
```

### Проверка пробельных символов: `isspace()`

`isspace()` возвращает `True`, если строка непустая и **состоит только из
пробельных символов**: пробела, табуляции `\t`, перевода строки `\n`,
`\r`, `\v`, `\f` и других пробельных символов Unicode:

```python
print("   ".isspace())    # True
print(" \t\n".isspace())  # True
print(" a ".isspace())    # False
```

### Пустая строка

Все методы проверки возвращают `False` для пустой строки:

```python
print("".isalpha())  # False
print("".isdigit())  # False
print("".isspace())  # False
```

### Сводка

| Метод | Истинно, если строка непустая и... |
|---|---|
| `islower()` | в ней есть буквы, и все они строчные |
| `isupper()` | в ней есть буквы, и все они заглавные |
| `isalpha()` | все символы — буквы |
| `isdigit()` | все символы — цифры |
| `isalnum()` | все символы — буквы или цифры |
| `isspace()` | все символы — пробельные |

---

## 2. Наборы символов из модуля `string`

Модуль стандартной библиотеки `string` содержит готовые **строковые
константы** с наборами символов. Они содержат только символы **ASCII**:

| Константа | Содержимое |
|---|---|
| `string.ascii_lowercase` | `abcdefghijklmnopqrstuvwxyz` |
| `string.ascii_uppercase` | `ABCDEFGHIJKLMNOPQRSTUVWXYZ` |
| `string.ascii_letters` | `ascii_lowercase + ascii_uppercase` |
| `string.digits` | `0123456789` |
| `string.punctuation` | все ASCII-знаки препинания и символы (`!`, `#`, `@`, `~` и другие — вывод см. в примере ниже) |
| `string.whitespace` | пробельные символы: пробел, `\t`, `\n`, `\r`, `\v`, `\f` |
| `string.printable` | все печатаемые ASCII-символы (цифры, буквы, знаки, пробельные) |

```python
import string

print(string.ascii_lowercase)   # abcdefghijklmnopqrstuvwxyz
print(string.digits)            # 0123456789
print(string.punctuation)       # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
print(repr(string.whitespace))  # ' \t\n\r\x0b\x0c'
```

### Зачем нужны константы, если есть методы `isalpha()` и другие

1. **Строгий ASCII.** `isalpha()` для `"é"` вернет `True`, а
   `"é" in string.ascii_letters` — `False`. Когда формат данных
   подразумевает только латиницу (идентификаторы, коды), константы
   точнее:

   ```python
   print("é".isalpha())                # True
   print("é" in string.ascii_letters)  # False
   ```

2. **Нестандартные группы.** Для знаков препинания у строк нет метода
   `ispunctuation()` — зато есть `string.punctuation`:

   ```python
   print("!" in string.punctuation)  # True
   print("a" in string.punctuation)  # False
   ```

3. **Источник символов.** Константы удобны, когда нужны сами **наборы
   символов** — для генерации паролей, шифров, проверки допустимых
   символов. Позицию буквы в алфавите можно узнать через `index()`:

   ```python
   print(string.ascii_lowercase.index("d"))  # 3
   print(string.ascii_lowercase[3])          # d
   ```

Константы можно комбинировать операцией `+` и срезами — например, составить
алфавит для генерации паролей:

```python
password_alphabet = string.ascii_letters + string.digits

print(len(password_alphabet))  # 62
```

---

## Вывод

- `islower()` / `isupper()` проверяют регистр букв, `isalpha()` / `isdigit()` /
  `isalnum()` — состав строки, `isspace()` — что строка состоит только из
  пробельных символов. Все возвращают `bool`.
- Для **пустой строки** все эти методы возвращают `False`.
- Методы работают со всем Unicode: `isalpha()` принимает буквы любых
  алфавитов. `isdigit()` — **не** проверка на число (`"-5"`, `"3.14"` — `False`).
- Модуль `string` предоставляет ASCII-наборы: `ascii_lowercase`,
  `ascii_uppercase`, `ascii_letters`, `digits`, `punctuation`, `whitespace` и
  другие — они пригодны для проверки принадлежности (`in`) и как
  источник символов.

---

## Источники

- [Python documentation. Built-in Types — str.isalpha(), str.isdigit(), str.isalnum() и другие](https://docs.python.org/3/library/stdtypes.html#str.isalpha);
- [Python documentation. string — String constants](https://docs.python.org/3/library/string.html#string-constants);
- [Python documentation. Built-in Types — str.isspace()](https://docs.python.org/3/library/stdtypes.html#str.isspace).
