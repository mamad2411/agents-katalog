<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0ssigeno
description: CTF writeups and security challenges by 0ssigeno.
---

# Writeups by 0ssigeno

Source repository: `/repos/0ssigeno`

## Repository Index

- Writeups/de1CTF2020/nlfsr/writeup.md
- Writeups/advent2019/Genetic_Mutation/README.md
- Writeups/advent2019/SantaSignature/README.md
- Writeups/advent2019/keygenSSE/README.md
- Writeups/advent2019/mooo/README.md

## Writeup Content


### File: Writeups/advent2019/Genetic_Mutation/README.md

# Genetic Mutation

We have to change 4 bytes and we can give our name as input, so we can put something on the stack of the length that we want.
Of course we want to put a shellcode on the stack, and use the 4 bytes to jump on it.

The first problem is that NX was enabled, so we have to use 1 byte to disable it in the header.
To be honest I didn't know how to do it, well, I knew how to change it, but I didn't know of any software that could give me the address. So i asked one of my teammate, and he game the C script file in this directory. I could use a diff between a modified elf and the starting one, but hey, I ain't the smartest one.


After that i just used 2 bytes to jump on the shellcode: the string is loaded naturally into RDX, at main+113.
So is enought to select an address after that point, but the string still has to be in that register, use 1 byte to modify one opcode to 'push rdx' and another byte to create the 'ret' opcode, so we can jump on our shellcode and have a shell!

![](./bytes.png)




### File: Writeups/advent2019/SantaSignature/README.md

# Santa's Signature
The challenge use a classic RSA sign and verify, without anything strange.

So, differently from the others, I abused the fact that we can give both the Sign and the plaintext as inputs.
Is enought to switch S with M when given as input, where S is calculated encrypting M with the public key that is given.
Since
```Python
verify(m,s):
	return m==encrypt(s,publickey)
```
If we give

```Python
verify(encrypt("AAAA",publicKey),"AAAA") # encrypt("AAAA",publickey)==encrypt("AAAA",publickey) 
```
we will pass the test.
We just have to do this for 3 times!
![](./santa.png)


After reading the explanation by the OverTheWire team, I don't think this was intended, but hey, a flag is a flag.



### File: Writeups/advent2019/keygenSSE/README.md

# Day 10 - ChristmaSSE KeyGen - rev, math

> I ran this program but it never finished... maybe my computer is too slow. Maybe yours is faster?

Download: [reverse_ctf.out](https://advent2019.s3.amazonaws.com/326c15f8884fcc13d18a60e2fb933b0e35060efa8a44214e06d589e4e235fe34)  
Mirror: [reverse_ctf.out](./reverse_ctf.out)

Inizialmente non avevo letto che la challenge fosse math e quindi ho subito pensato ad un ottimizzazione del codice. Ho iniziato a riscriverlo in python cachando le varie operazioni. Ottendendo cosi le 3 operazioni fondamentali che vengono utilizzate all'interno del \<main\>:

```
@cached(cache={})
def pshufd(src,order):
    line=bin(src)[2:].rjust(128,"0")
    n=32
    src=[line[i:i+n] for i in range(0, len(line), n)][::-1]
    #print(src)
    line=bin(order)[2:].rjust(8,"0")
    n=2
    order=[line[i:i+n] for i in range(0, len(line), n)]
    #print(order)
    res=""
    for i in order:
        val=int(i,2)
        res+=src[val]
    #print(int(res,2))
    return int(res,2)

@cached(cache={})
def pmulld(val1,val2):
    line=bin(val1)[2:]
    line=line.rjust(128,"0")
    n=32
    val1=[line[i:i+n] for i in range(0, len(line), n)]
    line=bin(val2)[2:].rjust(128,"0")
    n=32
    val2=[line[i:i+n] for i in range(0, len(line), n)]
    #print(val1,val2)
    res=""
    for i,j in zip(val1,val2):
        res+=str(int(i,2)*int(j,2)).rjust(32,"0")
    return int(res,16)

@cached(cache={})
def paddd(val1,val2):
    line=bin(val1)[2:]
    line=line.rjust(128,"0")
    n=32
    val1=[line[i:i+n] for i in range(0, len(line), n)]
    line=bin(val2)[2:].rjust(128,"0")
    n=32
    val2=[line[i:i+n] for i in range(0, len(line), n)]
    #print(val1,val2)
    res=""
    for i,j in zip(val1,val2):
        res+=str(int(i,2)+int(j,2)).rjust(32,"0")
    return int(res,16)
```

Successivamente ho individuato che le funzioni venivano sempre chiamate con una sequenza ben precisa, quindi le ho rese delle funzioni:

```
@cached(cache={})
def m_fun(s1, s2, s3):
    m = pmulld(s1, s2)
    m = paddd(m, s3)
    return m


@cached(cache={})
def fun(s1, s2, s3, s4):
    m = m_fun(s1, s2, s3)
    m = paddd(m, s4)
    return m
```

Ho copiato i dati 80 byte di dati in reverse_data.  
Ricostruendo il main:

```
def main():
    start_time = time.time()
    data = open('reverse_data', 'rb').read()

    res = int.from_bytes(data[64:80], byteorder='little')
    i0 = pshufd(res, 0x15)
    i1 = pshufd(res, 0x45)
    i2 = pshufd(res, 0x51)
    i3 = pshufd(res, 0x54)

#    i = [
#            [0, 0, 0, 1],
#            [0, 0, 1, 0],
#            [0, 1, 0, 0],
#            [1, 0, 0, 0]
#        ]

    counter = 0x112210f47de98115
    rax = 0

    d9 =  int.from_bytes(data[:16],   byteorder='little')
    d10 = int.from_bytes(data[16:32], byteorder='little')
    d13 = int.from_bytes(data[32:48], byteorder='little')
    d15 = int.from_bytes(data[48:64], byteorder='little')

    s00 = pshufd(d9,    0)
    s01 = pshufd(d9,   0x55)
    sss5= pshufd(d9,    0xaa)
    s03 = pshufd(d9,    0xff)

    s10 = pshufd(d10,   0)
    s5 = pshufd(d10,   0x55)
    s12 = pshufd(d10,   0xaa)
    s13 = pshufd(d10,   0xff)

    s20 = pshufd(d13,  0)
    s21 = pshufd(d13,   0x55)
    s22 = pshufd (d13, 0xaa)
    s23 = pshufd(d13,  0xff)

    s30 = pshufd(d15,  0)
    s31 = pshufd(d15,   0x55)
    s32 = pshufd(d15,  0xaa)
    s33 = pshufd(d15,  0xff)

    print(hex(s00 ), hex(s01), hex(sss5), hex(s03 ))
    print(hex(s10 ), hex(s5 ), hex(s12), hex(s13 ))
    print(hex(s20), hex(s21 ), hex(s22 ), hex(s23))
    print(hex(s30), hex(s31 ), hex(s32 ), hex(s33))

#    
#    A1 = [[16,15,14,13],
#          [12,11,10, 9],
#          [8 , 7, 6, 5],
#          [4 , 3, 2, 1]]

    sres = int.from_bytes(data[72:76], byteorder='little')

    while(rax != counter):
        # prima colonna
        m6  = pmulld(s00, i3)
        m8  = pmulld(s10, i3)
        m11 = pmulld(s20, i3)
        m14 = pmulld(s30, i3)

        #--------------------
        m12 = m_fun(s01, i2, m6) #xmm12s * xmm2 * xmm6 = xmm12
        m5 = pmulld(s11,  i1) #xmm5s *xmm1 = xmm5
        i3 = fun(s03, i0, m5, m12)
        print(hex(i3))
        exit(0)

        mm5 = m_fun(s11, i2, m8)
        m7 = m_fun(s21, i2, s20)
        mm6 = pmulld(s12, i1)       #64c
        i2 = fun(s13, i0, mm6, mm5) #662

        mmm5 = pmulld(s22, i1)
        mmm6 = pmulld(s32, i1)      #680
        i1 = fun(s23, i0, mmm5, m7)

        m4 = m_fun(s31, i2, m14)
        i0 = fun(s33, i0, mmm6, m4)

        #var ciclo interno
        m4 = pshufd(sres, 0xaa)
        m5 = pshufd(i0, 0)
        edx = 0x3e8
        #internalCycle() 	ignoring overflow internal cycle

        rax += 1
        if rax % 10000000 == 0:		#print time to execute 10.000.000 cycles
            print(time.time()-start_time) #150 seconds every 10.000.000 cycles... mmm... wrong way
```

Dopo aver perso qualche ora cercando di risolverlo nel modo sbagliato, ho realizzato che la challenge era MATH!!!
Ho analizzato come veniva modificata la matrice alla fine di ogni ciclo, ed era una semplice moltiplicazione:

```
A1 = [[16,15,14,13],
      [12,11,10, 9],
      [8 , 7, 6, 5],
      [4 , 3, 2, 1]]

A2 = A*A = [[600 542 484 426]
            [440 398 356 314]
            [280 254 228 202]
            [120 110 100 90]]
```

A questo punto ho cercato il numero di volte che doveva essere eseguito (fibonacci)

```
def calculate_exponentiation():
    res = []
    s = 1234567890123456789
    i=0
    while(s>0):
        if 2**i > s:
            res.append(i-1)
            s -= 2**(i-1)
            i=0
        else:
            i+=1
    return res
```

Ho trovato che il ciclo interno serviva a gestire l'overflow:

```
def overflow(a):
    sres = 0x96433d
    for x in range(4):
        for y in range(4):
            while a[x][y] > sres:
                a[x][y] %= sres
    return a
```

Infine ho emulato la risoluzione della flag:

```
def emulation(tot):
    BASE    = 0x400000
    STACK   = 0x7ffcaf000000
    FLAG    = 0x00600000

    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    mu.mem_map(BASE, 1024*4)
    mu.mem_map(STACK, 1024*4)
    mu.mem_map(FLAG, 1024*1024)

    code = struct.pack ("69B", *[
        0x66,0x0f,0x7f,0x1c,0x24,0x66,0x0f,0x7f,0x54,0x24,0x10,
        0x66,0x0f,0x7f,0x4c,0x24,0x20,0x66,0x0f,0x7f,0x44,0x24,
        0x30,0x31,0xc0,0x66,0x2e,0x0f,0x1f,0x84,0x00,0x00,0x00,
        0x00,0x00,0x0f,0x1f,0x00,0x0f,0xb6,0x0c,0x44,0x30,0x88,
        0x90,0x10,0x60,0x00,0x0f,0xb6,0x4c,0x44,0x01,0x30,0x88,
        0x91,0x10,0x60,0x00,0x48,0x83,0xc0,0x02,0x48,0x83,0xf8,
        0x20,0x75,0xe1])
    flag = struct.pack ("40B", *[
        0xfc,0x14,0xeb,0x09,0xbc,0xae,0xe7,0x47,0x4f,0xe3,0x7c,
        0xc1,0x52,0xa5,0x02,0x8e,0x89,0x71,0xc8,0x8d,0x96,0x23,
        0x01,0x6d,0x71,0x40,0x5a,0xea,0xfd,0x46,0x1d,0x23,0x00,
        0x00,0x00,0x00,0x00,0x00,0x00,0x00])

    mu.reg_write(UC_X86_REG_RSP, STACK)
    mu.reg_write(UC_X86_REG_XMM0, (tot[0][0]<<96) + (tot[0][1]<<64) + (tot[0][2]<<32) + (tot[0][3]))
    mu.reg_write(UC_X86_REG_XMM1, (tot[1][0]<<96) + (tot[1][1]<<64) + (tot[1][2]<<32) + (tot[1][3]))
    mu.reg_write(UC_X86_REG_XMM2, (tot[2][0]<<96) + (tot[2][1]<<64) + (tot[2][2]<<32) + (tot[2][3]))
    mu.reg_write(UC_X86_REG_XMM3, (tot[3][0]<<96) + (tot[3][1]<<64) + (tot[3][2]<<32) + (tot[3][3]))

    mu.mem_write(FLAG+0x1090, flag)

    mu.mem_write(BASE, code)
    mu.emu_start(BASE, BASE + len(code), 2 * UC_SECOND_SCALE)
    print(mu.mem_read(FLAG+0x1090, 0x20))
```



### File: Writeups/advent2019/mooo/README.md

# mooo
The challenge allows the use of cowsay on a website.


You can create a custom one, if you select 'custom' from the input list, meaning that you want to write a custom file that will be executed from cowsay with the '-f' parameter.
So the only things that I can work with is the body had to work with the body, but every command inside was not executed, just printed.

Then I started to read the [source code](https://github.com/schacon/cowsay/blob/master/cowsay)

I searched for the execution of a cowfile, since it was our case, and a line got my attention:
```Perl
177 - do $full;
```
where $full is the path of our cowfile.

It execute the file as if it was Perl!
Then I started to read a cowfile, and the solution was obvious. 

It reads the file till 'EOC', and after that we can inject our code that will be executed.
 So we can just give as input
```Perl
EOC
system("cat flag");
```
and we will get the flag!

![](./moo.jpg)



### File: Writeups/de1CTF2020/nlfsr/writeup.md

# NLFSR

## Information
- category: crypto
- points: 235

## Description
Easy lfsr easy crypto

链接：https://share.weiyun.com/5qZbNLR 密码：n9huwc https://drive.google.com/open?id=1a5GMVZ77CM1rOrayKJcV3UvMwAy-uGsg


## Writeup
First of all, I solved this challenge together with [meowmeowxw](https://meowmeowxw.gitlab.io/)

To understand how a general nlsr works, please read this [article](https://ctf-wiki.github.io/ctf-wiki/crypto/streamcipher/fsr/nfsr/) from ctfwiki.
What did we learn from that article? That we must find a strong correlation between the output and one of the input.
So we made a little script to retrieve the truth table of 
```py 
(ao * bo) ^ (bo * co) ^ (bo * do) ^ co ^ do
```

The table retrieved is the following:


![alt text](table.jpg "Truth Table")



Is possible to see that the parameter A has a strong correlation with the output (75% of times, if A=0 then the output is 0).
So we can calculate this value using the same approach described in the article mentioned before. I modified it slightly and the result is the following code:

```py

mapA = {
    (0,): 0
}

def lfsr(r, m):
    output = ((r << 1) & 0xffffff) ^ (bin(r & m).count('1') % 2)
    last_bit = (bin(r & m).count('1') % 2)
    return output, last_bit

def guessA(maps: {}, rang, a, data, res):
    ma= 0x505a1
    old_a = a
    for a in rang:
        a = old_a
        good = 0
        total = 0
        for j in range(0, len(data)):
            to_check = ()
            output = int(data[j])
            a, a_bit = lfsr(a, ma)
            to_check += (a_bit, )

            expected_res = maps.get(to_check, None)
            if expected_res is None:
                continue
            if expected_res == output:
                good += 1
            total += 1
        if total != 0:
            ratio = good * 100 / total
            if ratio >= 70:
                res.append(var)

    return sorted(res, reverse=True)

```
This function will return the values of every number that has a correlation greater than 70, and only the value 363445 has this property
Now we can retrieve the value of B. This is possible because, reading the truth table, if we know the value of A, and the output O, it is possible to bruteforce the value B having as constraints:
- If A is 1 and the output is 1, B must be 1.
- If A is 0 and the output is 0, B must be 1.


Again only 1 value comply with the constraints.
At this point, we tried to find a correlation with C and D, having A,B and output. But we did not find any correlation, so we decided to bruteforce something.
Since D are only ~40 values, we can try every value of D and use the complete truth table to retrieve the value of C for that particular D.
Of course the last possible value of D was the right one, and thank to that we find the valid value for C.


The values were: A=363445, B=494934, C=4406, D=63.

