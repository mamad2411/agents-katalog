<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-darkhole1
description: CTF writeups and security challenges by DarkHole1.
---

# Writeups by DarkHole1

Source repository: `/repos/DarkHole1`

## Repository Index

- writeups/damctf-2021/misc-Imp3rs0nAt0r-1.md

## Writeup Content


### File: writeups/damctf-2021/misc-Imp3rs0nAt0r-1.md

# DamCTF 2021
## misc/Imp3rs0nAt0r-1

Автор врайтапа: Влад Росков ([@mrvos](https://t.me/mrvos))

## Задание

#### `misc/Imp3rs0nAt0r-1`, автор perchik

Some dumb college student thought he was leet enough to try and hack our university using a school computer. Thankfully we were able to stop the attack and we confiscated the equipment for forensic analysis.

Can you help us figure out what their next moves are?

Flag is in standard flag format.

https://damctf-2021-prod-storage.storage.googleapis.com/uploads/692dcb7893364b68c358becb02b1e2cb854b9dfd3d149fee2e5d2d7cdc25d78b/UsrClass.dat


## Осматриваемся

В этом таске единственная осмысленная вещь, доступная нам изначально — это файл `UsrClass.dat`. Давайте посмотрим, что это за файл:
```sh
root@vsi:/mnt/f/dam# file UsrClass.dat
UsrClass.dat: MS Windows registry file, NT/2000 or above
```

Окей, это сырой куст реестра Windows. Поискав по имени файла, мы можем также найти, что это ветка `HKEY_CURRENT_USER\Software\Classes`.


## Извлекаем ShellBag

Мы можем изучить содержимое этой ветки реестра например с помощью тулзы [Windows Registry Recovery](https://www.mitec.cz/wrr.html). Файл не слишком большой, так что можно проглядеть всю ветку глазами, используя Raw Data в WRR. 

Часть, в которой содержится что-то полезное — это `Local Settings\Software\Microsoft\Windows\Shell\BagMRU`, в которой содержатся ShellBag-и. В них накапливается история папок, посещённых пользователем. 

Мы можем либо пробежаться по иерархической структуре ShellBag-ов в реестре руками, заглядывая в длинные значения, где хранятся названия папок:

![](https://img.vos.uz/2byilutl.png)
(`2020faExploit_scripts`)

, либо отпарсить шеллбэги автоматом, например с помощью тулзы скрипта на питоне https://github.com/williballenthin/shellbags:
```sh
root@vsi:/mnt/f/dam/shellbags# python shellbags.py ../UsrClass.dat
No handlers could be found for logger "shellbags"
<...>
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts (Shellbag)|0|0|0|0|0|1620859104|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts\.git (Shellbag)|0|0|0|0|0|1620859104|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts\.git\info (Shellbag)|0|0|0|0|0|1620859104|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts\.git\objects (Shellbag)|0|0|0|0|0|1620859104|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts\.git\objects\info (Shellbag)|0|0|0|0|0|1620859104|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts\.git\objects\db (Shellbag)|0|0|0|0|0|1620859456|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2020faExploit_scripts\.git\objects\pack (Shellbag)|0|0|0|0|0|1620859104|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021spExploit_scripts (Shellbag)|0|0|0|0|0|1620859112|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021spExploit_scripts\.git (Shellbag)|0|0|0|0|0|1620859112|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021spExploit_scripts\.git\branches (Shellbag)|0|0|0|0|0|1620859112|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021spExploit_scripts\.git\refs (Shellbag)|0|0|0|0|0|1620859112|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021spExploit_scripts\.git\refs\tags (Shellbag)|0|0|0|0|0|1620859112|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021suExploit_scripts (Shellbag)|0|0|0|0|0|1620859066|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021suExploit_scripts\.git (Shellbag)|0|0|0|0|0|1620859066|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021wiExploit_scripts (Shellbag)|0|0|0|0|0|1620859120|-62135596800|-62135596800|-62135596800
0|\{My Computer}\E:\\hacking\Scripts\2021wiExploit_scripts\.git (Shellbag)|0|0|0|0|0|1620859120|-62135596800|-62135596800|-62135596800
<...>
```

Полезные нам имена папок — `2020faExploit_scripts`, `2021spExploit_scripts`, `2021suExploit_scripts`, `2021wiExploit_scripts`. По именам папок внутри них мы видим, что это Git-репозитории.


## Дискорд-бот в репозитории

Давайте погуглим по "2020faExploit_scripts"

![](https://img.vos.uz/zqu2f9mg.png)

Мы находим профиль на гитхабе https://github.com/nc-lnvp, у которого есть как раз все четыре обнаруженных нами репозитория. Помимо них, у юзера есть репозиторий https://github.com/nc-lnvp/h4ckerman-3000-bot с кодом бота для Discord. 

В исходниках `bot.py` прописал API-токен для доступа к дискорду от имени бота:
```python
token = base64.b64decode(b'T0RReU1qUTNPRFl6TWpVek56STVNamt3LllKeWljZy5EdENIcVlTNVl5ekFmdGJoaVFFclZuYm5ORzA=').decode()
```

А это значит, что мы можем попробовать пойти с этим токеном в дискорд и выполнять действия от имени бота. 

Возьмём пример кода прямо из `bot.py`:
```python
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

token = base64.b64decode(b'T0RReU1qUTNPRFl6TWpVek56STVNamt3LllKeWljZy5EdENIcVlTNVl5ekFmdGJoaVFFclZuYm5ORzA=').decode()
client.run(token)
```

Запускаем:
```sh
root@vsi:/mnt/f/dam# pip3 install discord
<...>
Successfully installed discord-1.7.3 discord.py-1.7.3

root@vsi:/mnt/f/dam# ./ds.py
We have logged in as wtfisthis#8603
```

Успех, пустило!


## Осматриваемся под ботом

Следующими действиями подёргаем API-шку дискорда, извлекая информацию, доступную с правами этого бота. 

Помогут нам в этом две вещи:
1. **Документация** по API модуля discord: https://discordpy.readthedocs.io/en/stable/api.html
2. **IPython.** Нагугливаем, как успешно вызвать интерактивную консоль внутри `async`-функции, чтобы можно было прямо в ней дёргать всякие свойства у инициализированного объекта `client`: https://stackoverflow.com/questions/56415470/calling-ipython-embed-in-asynchronous-code-specifying-the-event-loop  
Вставляем `from IPython import embed; import nest_asyncio; nest_asyncio.apply(); embed(using='asyncio')` прямо в функцию on_ready(), и получаем интерактивный шелл:

```python
root@vsi:/mnt/f/dam# ./ds.py
We have logged in as wtfisthis#8603
Python 3.8.10 (default, Jun  2 2021, 10:49:15)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.22.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: client
Out[1]: <discord.client.Client at 0x7fcdfef43af0>

In [2]:
```

### Получаем каналы, доступные боту:
```python
In [63]: for i in client.get_all_channels():
    ...:     print(i)
    ...:
Text Channels
Voice Channels
g3n3ral
t0p-53cr3t-l33t-h4x0r-ch4nn3l
l33t-m3mz

In [64]: chans = [i for i in client.get_all_channels()]

In [66]: chans
Out[66]:
[<CategoryChannel id=842247340744376341 name='Text Channels' position=0 nsfw=False>,
 <CategoryChannel id=842247341196443667 name='Voice Channels' position=0 nsfw=False>,
 <TextChannel id=842247341196443668 name='g3n3ral' position=0 nsfw=False news=False category_id=842247340744376341>,
 <TextChannel id=842252598173892629 name='t0p-53cr3t-l33t-h4x0r-ch4nn3l' position=1 nsfw=False news=False category_id=842247340744376341>,
 <TextChannel id=842252688745562133 name='l33t-m3mz' position=2 nsfw=False news=False category_id=842247340744376341>]
```


### Выбираем наиболее понравившийся нам канал:
```python
In [68]: chans[3]
Out[68]: <TextChannel id=842252598173892629 name='t0p-53cr3t-l33t-h4x0r-ch4nn3l' position=1 nsfw=False news=False category_id=842247340744376341>

In [71]: ch = chans[3]
```


### Учимся извлекать из канала сообщение
```python
In [74]: ch.last_message_id
Out[74]: 906403780109697043

In [89]: m = await ch.fetch_message(906403780109697043)

In [90]: m
Out[90]: <Message id=906403780109697043 channel=<TextChannel id=842252598173892629 name='t0p-53cr3t-l33t-h4x0r-ch4nn3l' position=1 nsfw=False news=False category_id=842247340744376341> type=<MessageType.default: 0> author=<User id=197460469336899585 name='WholeWheatBagels' discriminator='3140' bot=False> flags=<MessageFlags value=0>>

In [91]: m.content
Out[91]: '7h3yr3 g0nn4 s33 4ll 0ur s3cr3t5!!!!@!!!!!!!@@!!@!!!!111!!!'
```


### Учимся доставать все сообщения в канале (историю):
```python
In [119]: await ch.history(limit=123).flatten()
Out[119]:
[<Message id=906403780109697043 channel=<TextChannel id=842252598173892629 name='t0p-53cr3t-l33t-h4x0r-ch4nn3l' position=1 nsfw=False news=False category_id=842247340744376341> type=<MessageType.default: 0> author=<User id=197460469336899585 name='WholeWheatBagels' discriminator='3140' bot=False> flags=<MessageFlags value=0>>,
 <Message id=906402970969702401 channel=<TextChannel id=842252598173892629 name='t0p-53cr3t-l33t-h4x0r-ch4nn3l' position=1 nsfw=False news=False category_id=842247340744376341> type=<MessageType.default: 0> author=<User id=842246220927991809 name='nc-lnvp' discriminator='9645' bot=False> flags=<MessageFlags value=0>>,
<...>

In [121]: [i.content for i in await ch.history(limit=1000).flatten()]
Out[121]:
['7h3yr3 g0nn4 s33 4ll 0ur s3cr3t5!!!!@!!!!!!!@@!!@!!!!111!!!',
 '😠 💢',
 'h0W d0 1 m4K3 th3m l34vE??!',
 "1 D0N'T kNOW D:<<<<",
 '🤯 😠 🤯 😠 h0w 4r3 p3opl3 f1nd1ng u5???!!!???!! 🤬 🤬 🤬',
 '💵💸💵💸💵💸💵💸💵',
 '💰💰💰💰💰',
 '😏😏\U0001f978🤑🤤🤤🤖👹👹👹',
 "Ju5t r3mem3R th4t **I'm** in ch4rg3 h3re 😉\nIf I s4y we ar3 d0ing it, th3n we 4re do1ng it",
<...>
<...>
<...>
 "we lauNch 0ur a7Tack r1ght after n3xt DAM CTF\nTh3y w0n't suspecT a 7h1ng",
 '🤫 \U0001f978',
 '😲 😲 🤑 🤓',
 '',
 "I'v3 g0t i7 4ll RighT h3re in dis At7acHm3Nt",
 's0 when d0 we st4rt? 😏 😏',
 'wassup epic g4mers']
```


### В старых сообщениях что-то про аттачи, учимся доставать аттачи:
```python
In [128]: [i.attachments for i in await chans[3].history(limit=1000).flatten()]
Out[128]:
[[],
 [],
 [],
 [],
<...>
<...>
<...>
 [],
 [],
 [<Attachment id=842536367631368252 filename='sOOp3r_5ecRet_Pl4n5.txt' url='https://cdn.discordapp.com/attachments/842252598173892629/842536367631368252/sOOp3r_5ecRet_Pl4n5.txt'>],
 [],
 [],
 []]
```


Качаем аттач по ссылке https://cdn.discordapp.com/attachments/842252598173892629/842536367631368252/sOOp3r_5ecRet_Pl4n5.txt

```
=== MASTER HACKER PLAN (do not share) ===

1) Get acc3ss t0 un1v3R5i7y
2) F0rK b0mB 33Cs Serv3r
3) ???????????
4) sT3al 4ll t3h R0buX
5) Pr0fiT
6) dam{Ep1c_Inf1ltr4t0r_H4ck1ng!!!!!!1!}

=========================================
```


## Pwned!

