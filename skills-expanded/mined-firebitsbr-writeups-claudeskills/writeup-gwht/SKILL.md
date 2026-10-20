<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gwht
description: CTF writeups and security challenges by gwht.
---

# Writeups by gwht

Source repository: `/repos/gwht`

## Repository Index

- 2020YCBCTF/README.md
- 2020YCBCTF/wp/pwn/test.md
- 2020YCBCTF/wp/re/test.md
- 2020YCBCTF/wp/web/a_piece_of_java/test.md
- 2020YCBCTF/wp/web/a_piece_of_java/说明.md
- 2020YCBCTF/wp/web/break_the_wall/test.md
- 2020YCBCTF/wp/web/break_the_wall/说明.md
- 2020YCBCTF/wp/web/easycon/test.md
- 2020YCBCTF/wp/web/easyphp2/introdoction.md
- 2020YCBCTF/wp/web/easyser/test.md
- 2020YCBCTF/wp/misc/badapple/test.md
- 2020YCBCTF/wp/misc/com/test.md
- 2020YCBCTF/wp/misc/故乡的梅花又开了/test.md
- 2020YCBCTF/wp/misc/玩具总动员/test.md
- 2020YCBCTF/wp/misc/秘密传输/test.md
- 2020YCBCTF/wp/misc/逃离东南亚/test.md
- 2020YCBCTF/wp/crypto/CSTPC/test.md
- 2020YCBCTF/wp/crypto/GMC/test.md
- 2020YCBCTF/wp/crypto/INVITATIONS/test.md
- 2020YCBCTF/wp/crypto/Power/test.md
- 2020YCBCTF/wp/crypto/RRRRRRRSA/test.md
- 2020YCBCTF/wp/crypto/Simple/test.md

## Writeup Content


### File: 2020YCBCTF/README.md

# 2020YCBCTF
2020羊城杯官方writeup及源码

这几天会将所有的题目的源码及文件开源，各位师傅们久等了！
各个题目的分散的writeup后续会逐渐上传，所有题目的writeup已经汇总在wp文件夹下的writeup文件里面了！



### File: 2020YCBCTF/wp/crypto/CSTPC/test.md





### File: 2020YCBCTF/wp/crypto/GMC/test.md





### File: 2020YCBCTF/wp/crypto/INVITATIONS/test.md





### File: 2020YCBCTF/wp/crypto/Power/test.md





### File: 2020YCBCTF/wp/crypto/RRRRRRRSA/test.md





### File: 2020YCBCTF/wp/crypto/Simple/test.md





### File: 2020YCBCTF/wp/misc/badapple/test.md


这道题实在是太大了，如果有师傅实在是想做做菜鸡出的题的话，后面会放网盘链接上来的



### File: 2020YCBCTF/wp/misc/com/test.md





### File: 2020YCBCTF/wp/misc/故乡的梅花又开了/test.md

这道题附件实在是太大了，github上不给传，后续如果有师傅需要的话会放网盘链接的！



### File: 2020YCBCTF/wp/misc/玩具总动员/test.md





### File: 2020YCBCTF/wp/misc/秘密传输/test.md





### File: 2020YCBCTF/wp/misc/逃离东南亚/test.md





### File: 2020YCBCTF/wp/pwn/test.md





### File: 2020YCBCTF/wp/re/test.md





### File: 2020YCBCTF/wp/web/a_piece_of_java/test.md





### File: 2020YCBCTF/wp/web/a_piece_of_java/说明.md

### 出题思路

简单的 Java 源码审计反序列化题，分为两步：

1. 源码中对 cookie 的反序列化，里面有 SerialKiller 的白名单限制（而 SerialKiller 同时也引入了 apache-commons-collections 的危险依赖），通过动态代理构造 payload 触发连接数据库的操作。
2. JDBC 反序列化攻击 apache-commons-collections 执行命令。

### 说明

- 定时计划每 3 分钟重启 docker
- 附件压缩包提供给选手进行代码审计
- 无法访问可以尝试加大 pids_limit


### File: 2020YCBCTF/wp/web/break_the_wall/test.md





### File: 2020YCBCTF/wp/web/break_the_wall/说明.md

### 题目思路

通过题目提供的 webshell，绕过 disable_functions 的限制执行根目录下的 readflag 程序读取 flag。

### 注意事项

- flag 只有 root 可读，readflag 需要设置 root 的 suid，www 目录（web 目录）不可写
- 检查 php.ini 中的设置是否生效
- 使用的 docker 镜像为 7.4.8-apache，最好使用 docker 官方源 8 月份发布的最新版
- 无法访问可以尝试加大 pids_limit
- 必须设置定时任务定时重启 docker（3 分钟重启一次），不然会产生内存问题导致无法解题




### File: 2020YCBCTF/wp/web/easycon/test.md





### File: 2020YCBCTF/wp/web/easyphp2/introdoction.md





### File: 2020YCBCTF/wp/web/easyser/test.md



