<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-delicioushorse
description: CTF writeups and security challenges by DeliciousHorse.
---

# Writeups by DeliciousHorse

Source repository: `/repos/DeliciousHorse`

## Repository Index

- writeups/TeaserConfidence2019/GoMachine/README.md
- writeups/Sharif2016/Locky/README.md
- writeups/RCTF2017/HelloDalvik/README.md

## Writeup Content


### File: writeups/RCTF2017/HelloDalvik/README.md

# HelloDalvik 645 pts

### Author: florek

We start with an apk file `HelloDalvik.apk`. After unzipping it we get standard set of android application files like `classes.dex` but also natively compiled library. Application most likely uses this native library, and fortunately for us it was built for multiple platforms including x86 so it can be analyzed more easily.
We are also told that apk requires `API < 21` to run, which implies that it needs `Dalvik VM` instead of `ART` to run, which is suspicious.

To analyze this application we have to process `classes.dex` to get _java code_ or _smali_, but since it isn’t obfuscated, decompiled java code is easily readable.

Decompilation could simply be done using the following command:
```
d2j-dex2jar.bat C:\Workspace\Files\classes.dex
```

As an output we get `classes-dex2jar.jar` which can be further decompiled with `BytecodeViewer` (FernFlower decompiler).

![Decompiling with BytecodeViewer](decompiled.png)

Most interesting files for us are: `MainActivity.class`, `MainActivity$1.class` and `MathMethod.class`. The rest of the files are android libraries. To ease analysis those files can be exported to text files with some (especially unicode) identifiers renamed.

Here are the files after "deobfuscation":
* [MainActivity](MainActivity.java)
* [MainActivity$1](MainActivity$1.java)
* [MathMethod](MathMethod.java)

First thing that can be noticed is that native library is used only in one place:
```java
    public MainActivity() {
        System.loadLibrary("native-lib");
        Log.d("Have Fine! ", this.stringFromJNI() + "");
    }
    public native int stringFromJNI();  
```
It can be ignored for now. To better understand what is going on it's helpful to run this apk, we can setup `AVD` with an old enough OS to run it (eg. `Android 4.4 KitKat`).

To install the application simply type:
```
adb install HelloDalvik.apk
```

![HelloDalvik running in AVD](avd.png)

All processing is done after `CHECK` button is clicked, following this in decompiled code we get:

```java
    public void onClick(View var1) {
      String var5 = String.valueOf(this.val$editText.getText());
      String var8 = "";
      boolean var3 = false;
      char[] var6 = var5.toCharArray();

      for(int var2 = 0; var2 < var6.length; var8 = var5) {
         boolean var4 = var3;
         var5 = var8;
         if(var2 % 3 == 0) {
            var5 = "";

            for(int var9 = 0; var9 < 3; ++var9) {
               var5 = var5 + var6[(var2 + var9) % var6.length];
            }

            char[] var7 = MainActivity.process_1(this.this$0, var5);
            this.val$kk[0] = MainActivity.process_2(this.this$0, var7, var5);
            if(this.val$kk[0].equals(MainActivity.angryHashArray(this.this$0)[var2 / 3 % 4])) {
               var5 = var8 + var5;
               var4 = var3;
            } else {
               this.val$tv.setText("Too Young!!");
               var4 = true;
               var5 = var8;
            }
         }

         ++var2;
         var3 = var4;
      }

      if(!var3) {
         this.val$tv.setText("RCTF{" + var8 + "}");
      }

   }
```

User input is divided into 3 characters long chunks and processed with two function calls, after that result is compared with precalculated hashes.
Because computation is done on very short strings, writing a brute-forcer is the easiest option to find the correct input.

Processing functions:
```java
 private char[] processString1(String var1) {
      char[] var3 = new char[32];
      char[] var4 = var1.toCharArray();

      int var2;
      for(var2 = 0; var2 < var4.length; ++var2) {
         var4[var2] = (char)(var4[var2] % 10);
      }

      for(var2 = 0; var2 < 32; ++var2) {
         this.int_8 = (new MathMethod()).rem(var2, var4.length);                
         this.int_2 = (new MathMethod()).rem(var2, this.codeCharArr.length);    
         this.int_3 = (new MathMethod()).div(this.int_2, var4[this.int_8]);        
         this.int_4 = (new MathMethod()).plus(this.int_3, this.codeCharArr[this.int_2]);    
         this.int_6 = (new MathMethod()).mul(this.int_3, this.int_4);            
         this.int_5 = (new MathMethod()).xor(this.int_4, this.codeCharArr[this.int_8]);
         this.int_1 = (new MathMethod()).div(this.int_6, this.int_5);    
         var3[var2] = (char)(this.int_1 & this.int_7);
      }

      return var3;
   }
  private String processString2(char[] var1, String var2) {
      String var4 = "";
      if(var1.length != 32) {
         return null;
      } else {
         char[] var5 = var2.toCharArray();
         char[] var6 = this.hexdigits.toCharArray();

         int var3;
         for(var3 = 0; var3 < var5.length; ++var3) {
            var5[var3] = (char)(var5[var3] / 10 % 10);
         }

         var3 = 0;

         for(var2 = var4; var3 < 32; ++var3) {
            var2 = var2 + var6[(var5[var3 % var5.length] + var1[var3]) % 16];
         }

         return var2;
      }
   }
```
Above functions can be copied into brute-forcer source code. After trying to run this code we get ``Divided by zero exception`` and indeed after further investigation it turns out that this code will always result in dividing by zero, no matter what the input is. But application runs in AVD so it just must work. The only explanation left is that native library does some kind of code hot patching and it actually does just that.
When analyzing native android libraries it is useful to load `jni.h` file into IDA since it contains many useful enum and struct definitions.

First thing this native function does is it decodes some strings by simply adding a value to every character. Those strings are:
```
/data/dalvik-cache/data@app@com.rctf.hellodalvik
MathMethod_1
MathMethod_4
Lcom/rctf/hellodalvik/MathMethod;
```
After that it tries to find DEX file in process memory, by searching for its header in range parsed from `/proc/$PID/maps`, when header is found it calls the patch function twice. Once for `MathMethod_1` once and for `MathMethod_4`. Patch function does some DEX format parsing and at the very end calls `mprotect` to enable code patching without causing access violation exception. Based on the last parameter passed to this function the correct data is written into previously unprotected address.

This written data seems to be Dalvik opcodes corresponding to mul-int, rem-int and add-int operations:
```
.data:0002E004                 public mul_opcodes
.data:0002E004 mul_opcodes     db  92h ;             ; mul opcode
.data:0002E005                 db    0
.data:0002E006                 db    2
.data:0002E007                 db    3
.data:0002E008                 db  0Fh
.data:0002E009                 db    0
.data:0002E00A                 public rem_opcodes
.data:0002E00A rem_opcodes     db  94h ;              ; DATA XREF: .got:off_2DD44
.data:0002E00A                                         ; rem opcode
.data:0002E00B                 db    0
.data:0002E00C                 db    2
.data:0002E00D                 db    3
.data:0002E00E                 db  0Fh
.data:0002E00F                 db    0
.data:0002E010                 public add_opcodes
.data:0002E010 add_opcodes     db  90h ;              ; DATA XREF: .got:off_2DD48
.data:0002E011                 db    0
.data:0002E012                 db    2
.data:0002E013                 db    3
.data:0002E014                 db  0Fh
.data:0002E015                 db    0
```

So `MathMethod_4` is patched with addition opcode and `MathMethod_1` is patched with reminder opcode. With that we can fix brute-forcer.
Sure enough it works this time.

![Correct flag](flag.png)

Flag: `RCTF{2S1QqlY9if_o}`

* [Native module analysis](native.c)
* [Brute-forcer](BruteForcer.java)



### File: writeups/Sharif2016/Locky/README.md

# Locky Forensics 300 + 50 pts

### Author: florek

We are given `memory.dmp` file that is supposed to be a memory dump of ransomware infected PC. File is 256 MB.
First step is to identify used OS, simplest way is to search for some string like *debian*, *ubuntu*, *windows* or use binwalk that will find a bunch of unix paths. 

After quick search it looks like a debian, so we can download appropriate [volatility profiles](https://github.com/volatilityfoundation/profiles/tree/master/Linux/Debian/x64). With those profiles we can do some investigation. [Here are useful profile commands](https://github.com/volatilityfoundation/volatility/wiki/Linux-Command-Reference)

Exact OS version
```bash
> volatility-2.5.standalone.exe --plugins=profiles --profile=LinuxDebian86x64 linux_banner -f d:\workspace\CTFS\Sharif16\memory.dmp

Linux version 3.16.0-4-amd64 (debian-kernel@lists.debian.org) (gcc version 4.8.4 (Debian 4.8.4-1) ) #1 SMP Debian 3.16.36-1+deb8u2 (2016-10-19)
```
Despite deb8u2 version it looks like profile LinuxDebian86x64 works better than LinuxDebian82x64 so I will keep using it

Executed commands 
```bash
> volatility-2.5.standalone.exe --plugins=profiles --profile=LinuxDebian86x64 linux_bash -f d:\workspace\CTFS\Sharif16\memory.dmp

Pid      Name                 Command Time                   Command
-------- -------------------- ------------------------------ -------
	...
     610 bash                 2016-11-30 12:54:50 UTC+0000   rm file_*
     610 bash                 2016-11-30 12:54:50 UTC+0000   grep -ril "BEGIN PUBLIC KEY"
     610 bash                 2016-11-30 12:54:50 UTC+0000   cat .locky_1480503269
     610 bash                 2016-11-30 12:54:50 UTC+0000   head -c 10 file_2.locky | hexdump
     610 bash                 2016-11-30 12:54:50 UTC+0000   apt-get install binutils
     610 bash                 2016-11-30 12:54:50 UTC+0000   hexdump -C file_3
     610 bash                 2016-11-30 12:54:50 UTC+0000   apt-get install curl
     610 bash                 2016-11-30 12:54:50 UTC+0000   hexdump -C file_3.locky
     610 bash                 2016-11-30 12:54:50 UTC+0000   head -c 10 | hexdump
     610 bash                 2016-11-30 12:54:50 UTC+0000   rm privkey.pem
     610 bash                 2016-11-30 12:54:50 UTC+0000   ./run.sh
     610 bash                 2016-11-30 12:54:50 UTC+0000   cd dump/
     610 bash                 2016-11-30 12:54:50 UTC+0000   dd if=/dev/fmem of=memo.dmp bs=1M count=256
	... (some elements removed)
```
We can see here some post infection actions, like removing the private key. We can also see some *.locky files

Running processes
```bash
> volatility-2.5.standalone.exe --plugins=profiles --profile=LinuxDebian86x64 linux_pslist -f d:\workspace\CTFS\Sharif16\memory.dmp

Offset             Name                 Pid             Uid             Gid    DTB                Start Time
------------------ -------------------- --------------- --------------- ------ ------------------ ----------
...
0xffff88000d1615f0 login                496             0               0      0x000000000d0c2000 0
0xffff88000a6e0190 fail2ban-server      503             0               0      0x000000000d399000 0
0xffff88000bc162d0 bash                 530             0               0      0x000000000dc1e000 0
0xffff88000cbf6b60 bash                 610             0               0      0x000000000d032000 0
0xffff88000a4fe210 python               617             0               0      0x000000000dfcf000 0
0xffff88000a5b0310 dd                   652             0               0      0x000000000d15b000 0
```

By searching for `locky` string in the memory dump we can find a part of python script that was used to infect the system. Following this lead we can try to dump `python's` heap and and recover some of its objects.

```bash
> volatility-2.5.standalone.exe --plugins=profiles --profile=LinuxDebian86x64 linux_proc_maps -p 617 -f d:\workspace\CTFS\Sharif16\memory.dmp

Offset             Pid      Name                 Start              End                Flags               Pgoff Major  Minor  Inode      File Path
------------------ -------- -------------------- ------------------ ------------------ ------ ------------------ ------ ------ ---------- ---------
...
0xffff88000a4fe210      617 python               0x0000000000caa000 0x0000000000e6c000 rw-                   0x0      0      0          0 [heap]
...
> volatility-2.5.standalone.exe --plugins=profiles --profile=LinuxDebian86x64 linux_dump_map -p 617 -s 0x0caa000 -f d:\workspace\CTFS\Sharif16\memory.dmp --dump-dir=dump

Task       VM Start           VM End                         Length Path
---------- ------------------ ------------------ ------------------ ----
       617 0x0000000000caa000 0x0000000000e6c000           0x1c2000 dump\task.617.0xcaa000.vma
```
Dumped file has only 2MB and contains all the information that we need to recover encrypted files. To get the list of encrypted files, we can use the following command:
```bash
> volatility-2.5.standalone.exe --plugins=profiles --profile=LinuxDebian86x64 linux_enumerate_files -f d:\workspace\CTFS\Sharif16\memory.dmp

     Inode Address Inode Number              Path
------------------ ------------------------- ----
...
0xffff880000c3ec80                   1966090 /root/.locky_1480510736
0xffff88000cceac80                   1966091 /root/file_3.locky
0xffff88000ccea898                   1966092 /root/file_4.locky
0xffff88000992dc80                   1966088 /root/file_5.locky
0xffff8800099aa0c8                   1966089 /root/file_1.locky
0xffff8800099aa4b0                   1966093 /root/file_2.locky
```
Unfortunately trying to dump those files using `linux_find_file` yields empty 512 B files, but we get the correct size which will be useful later.

By examining python's heap we can find following elements:
* [Ransomware code at the beginning](ransomware.py)
* [Public key in PEM format](publickey.pem) (searching for `----BEGIN PUBLIC`)
* [Private key in PEM format](privatekey.pem) (searching for `---BEGIN RSA`)

Ransomware script encrypted files using 4096 bit RSA. Every file was encrypted multiple times:
```python
home = expanduser("~")
files = glob.glob(home + '/*')
LC, i = [], 0
for f in files:
    if isfile(f):
        if not f.endswith('.locky'):
            fd = open(f, 'r')
            g = open(f + '.locky', 'w')
            round = stamp % 14
            msg = fd.read()
            for _ in xrange(round):
                msg = privkey.encrypt(msg, 0)[0]
            LC.append(msg)
```
Here is script that will decrypt those files using extracted private key:
```python
from Crypto.PublicKey import RSA
privkey = open('privatekey.pem').read()
decryption_key = RSA.importKey(privkey)
iterations = 1480510736 % 14	# timestamp recovered from file listing

for i in range(1, 6):
	data = open('file_%d.locky' % (i,), 'rb').read()
	for _ in range(iterations):
		data = decryption_key.decrypt(data)
	open('file_%d.dec' % (i,), 'wb').write(data)
```

Now all we have to do is to extract encrypted files and run decrypter on them. Fortunately ransomware stored encrypted files in a `LC` list, so it should be possible to find them in memory. To get an idea what to look for to identify those list elements we can create simple python script that fills in the list with `0xAA` bytes, dump its heap and look for those bytes in memory. It looks like the list entries are proceeded by `size 00000000 FFFFFFFF` sequence and are located near the end of heap. 
We can now look for `00020000 00000000 FFFFFFFF ` (`00020000` is 512 in little endian) to locate our files. Since files are encrypted their entropy will be high, this fact also helps locating them.
Encrypted files can be dumped using for example hiew:

![Encrypted file in memory](encrypted_file.png)

After running decryption script on extracted files `file_4` contains our flag `SharifCTF{df90036c153c345dc707d693225f29e3}`


### File: writeups/TeaserConfidence2019/GoMachine/README.md

Go Machine 
==========
#### Reversing, 306pts, 10 sovles

Overview
--------------------------------

As one may guess from the task title, this is a binary written in Go. Furthermore it implements custom virtual machine. To make finding the actual main function easier I used [IDAGolangHelper](https://github.com/sibears/IDAGolangHelper), an awesome IDA script that renames function based on metadata found in the binary. After running this script, main function can be found under **main_main** name.
![Overview](img/overview.PNG)
Looking at the function graph and decompiled snipped it seems that indeed this is a vm.

vm analysis
---------------------------
At the beginning it loads the bytecode of size `0x32ABE` from address `0x04BE653`. My initial idea was to do everything that avoids analyzing it, because of its size :) I started from analyzing handlers
### Handlers
This vm has 15 handlers and is a stack-based one. The latter part becomes apparent after analyzing a few handlers. Here are supported operations, most of them pops operands from the top of the stack, and then pushes back the result.

* Subtract `stack[top-1] = stack[top-1] - stack[top]; top--;`
* Add `stack[top-1] = stack[top-1] + stack[top]; top--;`
* Negate `stack[top] = ~stack[top];`
* Multiply `stack[top-1] = stack[top-1] * stack[top]; top--;`
* Modulo `stack[top-1] = stack[top-1] % stack[top]; top--;`
* Push immediate `stack[++top] = imm;`
* Pop and ignore `top--;`
* Read char `stack[++top] = char;`
* Write char `print stack[top];`
* Duplicate `stack[top+1] = stack[top]; top++;`
* Store at addr `mem[addr] = stack[top];`
* Load from addr `stack[top] = mem[addr];`
* Pop to top-1	`stack[top-1] = stack[top]; top--;`
* Shift left `stack[top-1] = stack[top-1] << stack[top]; top--;`
* Compare `stack[top-1] == stack[top]`
* Shuffle

Most of them are simple arithmetic operations, or memory loads/stores. Except the last one.  
vm determines the handler to be executed based on finding current opcode's index in string `0123456789OEQLCI`. If for example currently executing instruction is `L` it will find that its index is 13, and execute handler number 13 (shift left). But when handler **Shuffle** is executed it shuffles this string. As a result, opcodes change their meaning. After **Shuffle** aforementioned string could look like this `ECI031456O7982LQ` and now instruction `L` has index 14 and executes completely different handler (compare). What is more interesting,  **Shuffle** handler is implemented using LCG generator:

```c
qword_56F0C0 = v131;
for ( j = 15LL; j > 0; j = v127 - 1 )
{
  v128 = result;
  v127 = j;
  v139 = (unsigned int)(0x19660D * qword_56F0C0 + 0x3C6EF35F) % (unsigned __int64)j;
  qword_56F0C0 = (unsigned int)(0x19660D * qword_56F0C0 + 0x3C6EF35F);
  v140 = *((_BYTE *)&handler_list + v127);
  if ( v139 >= 0x10 )
    runtime_panicindex(v127, result, v139, v131);
  v129 = *((unsigned __int8 *)&handler_list + v139);
  *((_BYTE *)&handler_list + v127) = v129;
  *((_BYTE *)&handler_list + v139) = v140;
} 
```
![Seed](img/seed.png)
Number used as a seed to this LCG is a result of previously executed vm operations. Each handler updates it in a unique way. This makes rewriting such a vm a much more error prone task.

Compare handler is also interesting. When it fails a loop that zeros stack, bytecode and memory is executed. This results in application crashing.


Different approaches
---------------------
As stated previously I wanted to avoid writing bytecode disasembler/emulator at all cost due to perceived difficulty. Here are few observations that I made, that later lead me to solving the task.

1. Compare handler is used to check the flag for correctness (duh), it compares hash calculated based on user input with expected one.
2. Hash is calculated from four characters. I checked that by feeding the program two strings `aaaabbbbbbbbbbbbbbb` and `aaaaaaaaaaaaaaaaaa` for both of them first comparison was the same. Hence only four characters are used.
3. It is therefore possible to find the input that produces correct hashes by bruteforcing four characters long inputs

### IDAPython approach
I figured that I could script debugger in such a way that it will feed the program with four characters combinations and break on comparison checking if a correct hash was generated.  
The idea is sound, but in reality it was way too slow. I was able to get the first part of the flag `p4{g` and that's only because I already knew first three letters :P

### Recording and replaying the trace
Since I already figured out scripting IDA debugger I might as well use it again.
I decided to dump all the instructions executed by the VM, that way I will get correct instruction trace, no need to rewrite anything. That's all assuming that instruction trace doesn't change based on the user input, which is the case here.  
Here is my [script](dump_vm_trace.py) that creates conditional breakpoint at the instruction dispatcher and dumps the currently executed instruction. Additionaly it dumps current stack state.   
Here is a trace snippet:

```
push (0x0)	(0x61000000|0x610000|0x6100|0x0)
add	(0x61000000|0x610000|0x6100|0x0|0x0)
load at (0xd)	(0x61000000|0x610000|0x6100|0x0)
add	(0x61000000|0x610000|0x6100|0x61)
add	(0x61000000|0x610000|0x6161)
add	(0x61000000|0x616161)
save at (0x3c)	(0x61616161)        # user input was 'aaaa'
pop(ignore)	(0x61616161)
push (0x0)	
push (0x0)	(0x0)
mul	(0x0|0x0)
shuffle	(0x0)
```

Having this dump I tried to duplicate my original idea. But this time not in a debugger but in python emulated environment. I wrote a script that parses whole trace dump and replays it. It also feeds different four chararacter sequences and checks the resulting hash. Here is a snippet of that script:

```python
elif line.startswith('shuffle'):
	pass
elif line.startswith('read_input'):
	top += 1
	stack[top] = ord(flag[flag_ctr])
	flag_ctr += 1
elif line.startswith('save at'):
	val = int(line[line.index('(')+1: line.index(')')], 16) 
	mem[val] = stack[top]
elif line.startswith('load at'):
	val = int(line[line.index('(')+1: line.index(')')], 16) 
	stack[top] = mem[val]

# calculated hash is written at this offset to be compared later
# no need to replay further
if line.startswith('save at (0x51)'):
	return stack[top] == expected_hash
```  

Huge advantage over full blown vm interpreter is that I didn't need to parse raw bytecode and handle shuffle operations, that as already explained is a bit tricky.  
Unfortunately this solution proved to be too slow to check every combination, even when I tried to optimize it.

### Trace analysis and comaprsion
Funny thing is that despite tring so hard not to analyze the bytecode I already analyzed it quite a bit by reading vm trace and finding for example location where calculated hash is stored.  
Having failed with my previous _clever_ attempts I decided to dump traces for two simillar user inputs and compare them in order to understand what is this vm actually doing. And this turned out not to be as hard as I expected at first.
Here is a trace comparison for inputs `abcd` and `dcba`
![Diff1](img/trace_diff1.PNG)
I noticed that a lot of values are the same, so it was easy to scroll through the trace and identify important places. First input is multiplied by itself, as shown on above picture. Then `mod 0x8405b751` of that multiplication is calculated
![Diff2](img/trace_diff2.PNG)
The result is again multipied by itself and modulo is calculated.
This process repeats 8 times, and at the end it is multipied by unmodified input and `mod 0x8405b751` of that is the final hash. 
![Diff3](img/trace_diff3.PNG)
Calculated hash is stored in memory, starting at `0x50`
![Diff4](img/trace_diff4.PNG)

So the algorithm turns out to be really simple:
```python
def calc_hash(input, mod):
    val = input
    for i in range(8):
        val = val*val % mod
    return val*input % mod
``` 
Let's test it:

![Hashing function](img/calc_hash.PNG)

We get the same results.  
Checking out next parts of the flag, their hashes are calculated the same, just modulo is different.  
Only thing left to do is to collect expected hashes, and write a script that will brute force correct inputs. Hashes can be extracted from trace, just remember that program will crash when the first mismatch occurs. Se either re-run the trace after each four characters input is found, or patch the comparison.
![Hashing comparison](img/hash_comparison.PNG)

Here is the final script:
```python
import string
import itertools
import sys
import struct

mod = [0x88ca6b51, 0x8405b751, 0xbfa08c87, 0x82013f23, 0x4666751b, 0x5271083f]
expected = [0xf2227a5, 0x4e053304, 0x706fc204, 0x4283b66c, 0x1e5cc83a, 0x1faf011c]

def calc_hash(input, mod):
    val = input
    for i in range(8):
        val = val*val % mod
    return val*input % mod

for i in range(len(mod)):
    for perm in itertools.permutations(string.printable, 4):
        input = struct.unpack('>I', ''.join(perm))[0]
        hash = calc_hash(input, mod[i])
        if hash == expected[i]:
            print ''.join(perm)
            break
```

The flag
------ 

![Flag](img/flag.PNG)

### Final thought
![Meme](img/meme.jpg)


