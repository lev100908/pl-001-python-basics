# Возврат значений из функции: `return` и `None`

> **Главная мысль.** Функция может не только выполнять действия, но и
> **возвращать результат** вызывающему коду. Для этого служит инструкция
> **`return`**: она немедленно завершает выполнение функции и «подставляет»
> указанное значение на место вызова. Если `return` не выполнился (или записан
> без значения), функция возвращает специальный объект **`None`**. Через
> `return` можно вернуть сразу несколько значений — Python упакует их в
> кортеж. Не следует путать **вывод на экран** (`print`) и **возврат значения**
> (`return`): результат, выведенный через `print`, программа дальше
> использовать не может.

---

## 1. Инструкция `return`

### Зачем нужен `return`

Функция принимает данные через параметры и выполняет над ними вычисления.
Чтобы результат можно было использовать в остальной программе, его нужно
передать вызывающему коду. Без `return` это невозможно: локальные переменные
функции существуют только во время вызова (подробнее — в конспекте про
пространства имен) и снаружи недоступны. Инструкция `return` — основной способ
передать результат из функции в место ее вызова.

```python
def square(number: int) -> int:
    return number * number


result = square(4)

print(result)                 # 16
print(square(3) + square(4))  # 25
```

Вызов `square(4)` возвращает число `16`. Это значение можно сохранить в
переменную `result` или сразу использовать в выражении, как во второй
строке с `print`.

### Как работает `return`

Инструкция `return expression` делает две вещи:

1. **завершает** выполнение функции — все, что записано в теле после
   выполненного `return`, пропускается;
2. **возвращает** значение выражения `expression` в то место, откуда функцию
   вызвали.

```python
def add(first_term: int, second_term: int) -> int:
    return first_term + second_term


result = add(2, 3)

print(result)           # 5
print(add(10, 20) * 2)  # 60 -- результат вызова участвует в выражении
```

Вызов `add(2, 3)` вычисляет сумму аргументов и возвращает ее вызывающей стороне.
Возвращенное значение (`5`) можно сохранить в переменную, передать в другую функцию или использовать в выражении.

Код после `return` никогда не выполняется:

```python
def get_number() -> int:
    return 1
    print("This line is never reached")


print(get_number())  # 1
```

---

## 2. Ранний возврат

Функция может содержать несколько `return`. Это удобно для **раннего
возврата (early return)**: когда результат уже ясен, функция сразу
завершается, а остальной код не нужно оборачивать в `else`.

```python
def get_sign(number: int) -> str:
    if number > 0:
        return "positive"

    if number < 0:
        return "negative"

    return "zero"


print(get_sign(5))   # positive
print(get_sign(-3))  # negative
print(get_sign(0))   # zero
```

Еще один типичный пример — проверка корректности данных в начале функции:

```python
def divide(dividend: float, divisor: float) -> float | None:
    if divisor == 0:
        return None

    return dividend / divisor


print(divide(10, 4))  # 2.5
print(divide(10, 0))  # None
```

`return` можно использовать и внутри цикла — он прервет и цикл, и всю
функцию:

```python
def find_first_even(numbers: list[int]) -> int | None:
    for number in numbers:
        if number % 2 == 0:
            return number

    return None


print(find_first_even([1, 3, 4, 6]))  # 4
print(find_first_even([1, 3, 5]))     # None
```

---

## 3. Возврат `None`

В Python **любая функция что-то возвращает**. Если в функции нет инструкции
`return`, либо `return` записан без выражения, либо выполнение дошло до конца
тела без `return`, то функция возвращает **`None`** — единственное значение
типа `NoneType`, которое означает «нет значения».

```python
def no_return() -> None:
    print("working")


def bare_return() -> None:
    print("working")
    return


first_result = no_return()     # working
second_result = bare_return()  # working

print(first_result)   # None
print(second_result)  # None
```

Запись `return None`, `return` и отсутствие `return` в конце функции
равнозначны. Принятое соглашение:

- если функция **ничего не возвращает** — `return` не пишут вовсе (допустим
  голый `return` для раннего выхода из середины функции);
- если функция в одних ветках возвращает значение, а в других «ничего», то
  `return None` пишут явно — так читателю очевидно, что это сделано
  намеренно, а не по забывчивости.

Большинство встроенных методов, **изменяющих объект на месте**, также
возвращают `None`: `list.append()`, `list.sort()`, `dict.update()`. Это
распространенный источник ошибок:

```python
numbers = [3, 1, 2]

sorted_numbers = numbers.sort()

print(sorted_numbers)  # None -- sort() изменил список на месте и вернул None
print(numbers)         # [1, 2, 3]
```

Значение `None` нужно сравнивать через `is` / `is not`, а не через `==`:

```python
result = divide(10, 0)

if result is None:
    print("Division is impossible")
```

---

## 4. `print` и `return` — не одно и то же

Частая ошибка новичков — считать, что функция, которая вывела результат на
экран, этот результат «вернула». Это разные вещи:

- `print(value)` — **побочный эффект**: значение выводится на экран и
  пропадает; программа не может использовать его дальше;
- `return value` — **результат работы функции**: значение передается
  вызывающему коду, который решает, что с ним делать (вывести, сохранить,
  использовать в вычислениях).

```python
def add_with_print(first_term: int, second_term: int) -> None:
    print(first_term + second_term)


def add_with_return(first_term: int, second_term: int) -> int:
    return first_term + second_term


result_with_print = add_with_print(2, 3)    # 5 -- на экране
result_with_return = add_with_return(2, 3)  # на экран ничего не выводится

print(result_with_print)        # None
print(result_with_return)       # 5
print(result_with_return * 10)  # 50 -- результат можно использовать дальше
```

Функция, которая только печатает значение, не содержит `return`, поэтому ее
вызов возвращает `None`. Если использовать такой вызов в вычислениях, возникнет
ошибка:

```python
total = add_with_print(2, 3) * 10  # TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

Хорошая практика: функции, выполняющие вычисления, **возвращают** результат,
а выводом на экран занимается отдельный код (например, главная часть
программы). Такую функцию проще тестировать и переиспользовать.

---

## 5. Возврат нескольких значений

Через `return` можно перечислить несколько значений через запятую. На самом
деле Python возвращает **один объект — кортеж (`tuple`)**, скобки при этом
можно опустить:

```python
def get_min_max(numbers: list[int]) -> tuple[int, int]:
    return min(numbers), max(numbers)


result = get_min_max([4, 1, 7, 3])

print(result)        # (1, 7)
print(type(result))  # <class 'tuple'>
```

Вызывающий код обычно сразу **распаковывает** кортеж в отдельные переменные:

```python
minimum, maximum = get_min_max([4, 1, 7, 3])

print(minimum)  # 1
print(maximum)  # 7
```

Количество переменных слева должно совпадать с количеством возвращаемых
значений, иначе будет `ValueError`. Если нужно только одно значение, его
можно взять по индексу результата (кортеж поддерживает индексацию):

```python
minimum = get_min_max([4, 1, 7, 3])[0]

print(minimum)  # 1
```

---

## Вывод

- `return expression` завершает функцию и возвращает значение выражения в
  место вызова. Код после выполненного `return` не выполняется. Функция может
  содержать несколько `return` (ранний возврат).
- Любая функция возвращает значение. Если `return` отсутствует, записан без
  выражения или выполнение дошло до конца тела, возвращается `None`.
  С `None` сравнивают через `is` / `is not`, а не через `==`.
- `print` выводит значение на экран, а `return` передает его вызывающему коду;
  использовать можно только возвращенное значение.
- `return a, b` возвращает кортеж из двух значений, который можно сразу
  распаковать: `first, second = function()`.

---

## Источники

- [Python documentation. The Python Tutorial — Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions);
- [Python documentation. The Python Language Reference — The return statement](https://docs.python.org/3/reference/simple_stmts.html#the-return-statement);
- [Python documentation. Built-in Constants — None](https://docs.python.org/3/library/constants.html#None).
