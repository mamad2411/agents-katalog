<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-avlidienbrunn
description: CTF writeups and security challenges by avlidienbrunn.
---

# Writeups by avlidienbrunn

Source repository: `/repos/avlidienbrunn`

## Repository Index

- ctf-writeups/insomnihackteaser-2017/README.md
- ctf-writeups/nuitduhack-2016/night_daemonic_heap/README.md

## Writeup Content


### File: ctf-writeups/insomnihackteaser-2017/README.md

##Writeup
**Reversing**

The program allowed the user (robot) to enter a bunch of information:
* name (max input length 255)
* encryption method (either 0, 1 or 2)
* location (max input length 255)
* goal (max input length 255)
* last words (max input length 255)

The information was put into a structure on the heap that looked something like this:
```
struct userinfo{
	char name[260];
	char goal[204];
	char *location;
}
```

The location input was put on the heap, and a pointer to it was put in the userinfo struct.

The 3 encryption method choices (0,1,2) corresponded to 3 different functions in the program, "0" was no encryption, "1" was xor with "A", "2" was xor with "x". These were used on any information sent back to the client. The encryption_function_choice function pointer was put on the heap.

Lastly, the "last words" were also put on the heap.

**Analysing**

Something that looked strange was that ```free(userinfo->location)``` was in the middle of the function (as opposed to at the end, like the other malloc()d stuff). This was indeed the key to the challenge.

By simply using a "goal" larger than 204 bytes, we can overwrite the *location pointer, and when the program reaches ```free(userinfo->location)```, we can use it to free(anything).

I used that to ```free(encryption_function_choice)```. This meant that the next time something of the same size would be allocated, malloc() would return the pointer to the encryption choice.

So I chose my "last words", carefully, to overwrite the encryption_function_choice pointer. When the program then tries to ```encryption_function_choice(userinfo->name)```, we get control over RIP (and first arg, RDI).

**ROP**

First off, I needed a stack shift so that I could ROP properly. I found this gadget to do so:
```
xchg rsp, rdi;
ret;
```

Great, we got stack control (since RDI pointed to userinfo->name). But also not great, because now we don't have RDI control any more. That didn't matter so much because we could control function arguments 1 (RDI) and 2 (RSI) with the following gadgets:
```
pop rdi;
ret;
```
```
pop rsi;
pop r15;
ret;
```

Now, we needed to leak a libc address somehow to be able to ret2libc. I did this by setting RDI (first arg) to 4 (filedescriptor number of our socket), RSI (second arg) to GOT and then returning to a part of the function that called send().

After that, we could calculate offset to libc base and from libc base to system(). The offsets were the same as the "baby" chall, so no need to guess libc version/leak/brute.

Then we could just use all of the ingredients mentioned to system("/bin/sh").

But that was a bit problematic. Because this chall (just like baby chall) didn't forward stdin/stdout to the socket, we first had to ```dup2(socket, stdin)``` and ```dup2(socket, stdout)```.

After that everything worked fine and shell aquired :)
```
leaking heap pointer...
leaking GOT...
libc:    0x0000f738659a0d00
system:  0x0000f73865ea3209
bin_sh:  0x0000f738652c1977
dup2:    0x0000f738659bd309
> cat flag
INS{RealWorldFlawsAreTheBest}
```



### File: ctf-writeups/nuitduhack-2016/night_daemonic_heap/README.md

## Writeup

The challenge allowed users (players) to create characters, print their name, delete them and change their name. You could create either a barbarian or a wizzard (I only used barbarians).

There was an off-by-one write when creating new characters which could be exploited using the "shrink_free_hole_alloc_overlap_consolidate_backward" technique found at  https://googleprojectzero.blogspot.se/2014/08/the-poisoned-nul-byte-2014-edition.html.

It works by first allocating three blocks. Then free() the middle one. Then making it smaller by overwriting the size field of the free() one (Allocated_block1 overwrites 1 byte into Freed_block2).

After doing this we have a heap looking like:
```
|--------------------------------------------|
|       Allocated_block1                     |
|--------------------------------------------|
|                                            |
|                                            |
|                                            |
|                                            |
|                                            |
|        Freed_block2                        | <- heap manager thinks this block is smaller 
|                                            | than it is because we overflowed 1 byte from 
|                                            | Allocated_block1
|                                            |
|                                            |
|                                            |
|                                            |
|                                            |
|--------------------------------------------|
| Ghost space not seen by heap manager       |
|--------------------------------------------|
|       Allocated_block3                     |
|--------------------------------------------|
```
We then allocate 2 blocks inside Freed_block2, heap will look like:
```
|--------------------------------------------|
|       Allocated_block1                     |
|--------------------------------------------|
|       Allocated_block4                     |
|--------------------------------------------|
|       Allocated_block5                     |
|--------------------------------------------|
|                                            | 
|                                            |
|                                            |
|                                            |
|       Freed_block2                         | <- heap manager thinks this block is smaller 
|                                            |   than it is because we overflowed 1 byte from 
|                                            |   Allocated_block1
|                                            |
|--------------------------------------------|
| Ghost space not seen by heap manager       |
|--------------------------------------------|
|       Allocated_block3                     |
|--------------------------------------------|
```
When we then free() Allocated_block4 and Allocated_block3, the entire block will be free()'d because the original previous size (stored in "Ghost space") will still be there. Result:
```
|--------------------------------------------|
|       Allocated_block1                     |
|--------------------------------------------|
|                                            |
|- - - - - - - - - - - - - - - - - - - - - - |
|       Allocated_block5                     |<- We still have a pointer to Allocated_block5, but the heap  
|- - - - - - - - - - - - - - - - - - - - - - |  manager will think it's in free space 
|                                            | = use-after-free scenario.
|                                            |
|                                            |
|                                            |
|       Freed_block2                         |
|                                            |
|                                            |
|                                            |
|                                            |
|                                            |
|                                            |
|                                            |
|--------------------------------------------|
```

We can create a "write_what_where" by placing the name of a new barbarian over Allocated_block5. This means we can control the name pointer of the barbarian allocated inside Allocated_block5.

By changing the name of the new barbarian (and therefore changing the name pointer of Allocated_block5 barbarian) we can leak data anywhere. By changing it and using "change [whatever_string_is_at_that_address] [what_we_wanna_change_it_to]" we can write data anywhere.

Using the same technique (shrink free chunk) we can leak addresses from the heap. If we leak the VTable pointer of a barbarian, we can calculate the offset to got and then leak libc addresses.

Since I didn't know which libc version it was running, I wrote a leak loop searching for system() and the rop gadget I used (add_rsp90_pop3ret). I guessed the starting offsets by using the offsets of my local libc. They were ~300 bytes off.

We could then change the "print" function of one of the barbarians to point to the add_rsp_90_pop3ret gadget (rsp+0x90 will point to our input). That gadget would return into pop_rdi_ret (to get "/bin/sh" in rdi), which in turn returns to system().

Output of exploit:
```
Shrinking chunk and creating use-after-free state...
leak vtable pointer: 0x7f85a4d42c28
leak mapped pointer: 0x7f85a407bb98
leak heap pointer: 0x7f85a5356450
exit: 0x7f85a3cf9690
add_rsp90_pop3ret: 0x00007f85a3cf52b2
system: 0x00007f85a3d03da0
system: [4885ff740be986faffff660f1f44]
shift_stack: [4881c490]
bin_sh: 0x00007f85a5356450
pop_rdi: 0x00007f85a4b41e53
pop_rdi: [5fc366662e0f1f84]
Shifting stack...
Dropping shell...
id
uid=1000(my_chall_pwned) gid=1000(pwned) groups=1000(pwned)
cat /home/my_chall_pwned/flag
He4p_H3ap$He4p?H0ur4\o/
```
PS. Thanks for the help+rubber ducking+whatnot [alex](https://twitter.com/defendtheworld) \o/

