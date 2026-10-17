# Документирование функций: docstring

> **Главная мысль.** **Docstring (строка документации)** — строковый литерал,
> записанный **первой инструкцией** в теле функции. Он не выполняется как
> код, а сохраняется в атрибуте функции **`__doc__`** и используется
> встроенной справкой (`help()`), редакторами кода и инструментами генерации
> документации. Хороший docstring отвечает на вопрос «**что** делает функция,
> какие аргументы принимает и что возвращает», а не пересказывает код.
> Оформление docstring регламентирует **PEP 257**.

---

## 1. Что такое docstring

Если первая инструкция тела функции — строковый литерал, Python считает его
docstring и записывает в атрибут `__doc__` объекта-функции. Docstring
оформляют **тройными двойными кавычками** `"""..."""`:

```python
def square(number: int) -> int:
    """Return the square of a number."""
    return number * number


print(square.__doc__)  # Return the square of a number.
```

Сразу получаем два преимущества:

- описание хранится **рядом с кодом** и не расходится с ним (по крайней мере,
  его легче обновлять вместе с кодом);
- описание доступно **во время выполнения**: через `__doc__`, `help()`,
  `inspect.getdoc()`.

```python
help(square)
```

Вывод:
```
Help on function square in module __main__:

square(number: int) -> int
    Return the square of a number.
```

Документация встроенных функций устроена точно так же: `print(len.__doc__)`
выведет описание функции `len`, а `help(print)` покажет справку по `print`.
Редакторы кода (VS Code, PyCharm) показывают docstring во всплывающей
подсказке при наведении курсора на вызов функции.

### Чем docstring отличается от комментария

| | Комментарий `#` | Docstring |
|---|---|---|
| Что это | игнорируется интерпретатором | строковый литерал, попадает в `__doc__` |
| Для кого | для тех, кто **читает исходный код** | для тех, кто **использует** функцию (в том числе через `help()` и редактор) |
| О чем | **почему** и **как** реализовано | **что** делает и как пользоваться |

Строка, которая не стоит **первой** в теле, docstring не является — это
обычное выражение, не имеющее эффекта:

```python
def example() -> None:
    value = 1
    """This is NOT a docstring"""


print(example.__doc__)  # None
```

Если docstring у функции нет, `__doc__` равен `None`.

---

## 2. Однострочные docstring

Если поведение функции можно описать одним предложением, docstring
записывают в одну строку:

```python
def is_even(number: int) -> bool:
    """Return True if the number is even."""
    return number % 2 == 0
```

Рекомендации PEP 257 для однострочных docstring:

- открывающие и закрывающие кавычки стоят на **одной строке**;
- описание записывается в **повелительном наклонении** («Return ...»,
  «Calculate ...»), а не «Returns ...» или «This function returns ...»;
- в конце ставится точка;
- описание не повторяет сигнатуру (`"""is_even(number) -> bool"""` —
  плохой docstring) — сигнатура и так видна, нужно сказать, **что** функция
  делает.

---

## 3. Многострочные docstring

Для сложных функций docstring делают многострочным. Структура по PEP 257:

- **краткое описание** в одну строку;
- **пустая строка**;
- **подробное описание**: параметры, возвращаемое значение, исключения,
  примеры;
- закрывающие кавычки — на **отдельной строке**.

```python
def divide(dividend: float, divisor: float) -> float:
    """Divide one number by another.

    Args:
        dividend: The number to be divided.
        divisor: The number to divide by.

    Returns:
        The result of the division.

    Raises:
        ZeroDivisionError: If divisor is zero.
    """
    return dividend / divisor


help(divide)
```

Вывод:
```
Help on function divide in module __main__:

divide(dividend: float, divisor: float) -> float
    Divide one number by another.

    Args:
        dividend: The number to be divided.
        divisor: The number to divide by.

    Returns:
        The result of the division.

    Raises:
        ZeroDivisionError: If divisor is zero.
```

Что полезно указывать в подробном описании:

- смысл каждого параметра (тип уже виден из аннотаций, поэтому важнее
  *смысл*, допустимые значения и единицы измерения);
- что функция возвращает и в каких случаях возвращает `None`;
- какие исключения она может возбудить;
- побочные эффекты (изменяет ли функция переданные объекты, пишет ли в файл);
- пример использования.

Docstring — это строковый литерал, поэтому, как и остальные строки в коде,
его принято писать на английском языке.

---

## Вывод

- **Docstring** — строка, записанная первой в теле функции. Она сохраняется в
  `function.__doc__` и используется `help()`, редакторами и генераторами
  документации. Если docstring нет, `__doc__` равен `None`.
- Docstring записывают в тройных двойных кавычках. Однострочный — для
  простых функций (одно предложение в повелительном наклонении, с точкой).
  Многострочный — краткая сводка, пустая строка, подробности (параметры,
  возвращаемое значение, исключения, примеры).
- Docstring объясняет, **что** делает функция и как ее использовать;
  комментарии `#` объясняют, **почему** код написан именно так.

---

## Источники

- [Python documentation. The Python Tutorial — Documentation Strings](https://docs.python.org/3/tutorial/controlflow.html#documentation-strings);
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/);
- [Google Python Style Guide — Comments and Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
