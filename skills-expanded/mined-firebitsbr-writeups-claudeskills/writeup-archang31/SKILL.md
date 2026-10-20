<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-archang31
description: CTF writeups and security challenges by archang31.
---

# Writeups by archang31

Source repository: `/repos/archang31`

## Repository Index

- aacs4-writeups/README.md
- aacs4-writeups/BinaryExploitation/README.md
- aacs4-writeups/Cryptography/README.md
- aacs4-writeups/Forensics/README.md
- aacs4-writeups/Miscellaneous/README.md
- aacs4-writeups/ReverseEngineering/README.md
- aacs4-writeups/WebSecurity/README.md
- aacs4-writeups/WebSecurity/BlameItOnTheTemp/README.md
- aacs4-writeups/WebSecurity/CookieMonster/README.md
- aacs4-writeups/WebSecurity/DENIED/README.md
- aacs4-writeups/WebSecurity/ExtremelyMaliciousLanguage/README.md
- aacs4-writeups/WebSecurity/FirstFail/README.md
- aacs4-writeups/WebSecurity/IHaveCaughtYouNow/README.md
- aacs4-writeups/WebSecurity/LetMeInnnnnn/README.md
- aacs4-writeups/WebSecurity/MoreOutOfSite/README.md
- aacs4-writeups/WebSecurity/MostOutOfSite/README.md
- aacs4-writeups/WebSecurity/NoEscape/README.md
- aacs4-writeups/WebSecurity/OutOfSite/README.md
- aacs4-writeups/WebSecurity/TheSQLAlwaysSucks/README.md
- aacs4-writeups/WebSecurity/WhoIsThatInThatMirror/README.md
- aacs4-writeups/ReverseEngineering/AreYouMachingMe/README.md
- aacs4-writeups/ReverseEngineering/CLRlyJustACrackMe/README.md
- aacs4-writeups/ReverseEngineering/CandCMusicFactory/README.md
- aacs4-writeups/ReverseEngineering/IntoTheMetaverse/README.md
- aacs4-writeups/ReverseEngineering/LibraryCard/README.md
- aacs4-writeups/ReverseEngineering/Lockbox/README.md
- aacs4-writeups/ReverseEngineering/NationalDex65/README.md
- aacs4-writeups/ReverseEngineering/ReadItAndWeep/README.md
- aacs4-writeups/ReverseEngineering/ReverseEngineering101/README.md
- aacs4-writeups/ReverseEngineering/SayWhat/README.md
- aacs4-writeups/ReverseEngineering/WhatsTheDifference/README.md
- aacs4-writeups/Miscellaneous/AllYourBase/README.md
- aacs4-writeups/Miscellaneous/AssemblyVoyageur/README.md
- aacs4-writeups/Miscellaneous/CanYouLookThisOver/README.md
- aacs4-writeups/Miscellaneous/ISEeYou/README.md
- aacs4-writeups/Miscellaneous/MoveZIG/README.md
- aacs4-writeups/Miscellaneous/PartitionTwiceRecoverOnce/README.md
- aacs4-writeups/Miscellaneous/PassThis/README.md
- aacs4-writeups/Miscellaneous/ProxyList/README.md
- aacs4-writeups/Miscellaneous/RecoveryAndIDentification/README.md
- aacs4-writeups/Miscellaneous/UNOReverseCard/README.md
- aacs4-writeups/Forensics/BootMaster/README.md
- aacs4-writeups/Forensics/BootRacer/README.md
- aacs4-writeups/Forensics/BootRiddle/README.md
- aacs4-writeups/Forensics/Bootcamp/README.md
- aacs4-writeups/Forensics/ControlledAccess/README.md
- aacs4-writeups/Forensics/DrillToTheCenter/README.md
- aacs4-writeups/Forensics/FilingExtension/README.md
- aacs4-writeups/Forensics/KidsOnTheBlock/README.md
- aacs4-writeups/Forensics/NeedleInTheHaystack/README.md
- aacs4-writeups/Forensics/NotSoMeta/README.md
- aacs4-writeups/Forensics/SharingIsCaring/README.md
- aacs4-writeups/Forensics/ThatsMoreThanEnough/README.md
- aacs4-writeups/Forensics/TurtlesAllTheWayDown/README.md
- aacs4-writeups/Cryptography/HeadpieceSilver/README.md
- aacs4-writeups/Cryptography/OverTimePaid/README.md
- aacs4-writeups/Cryptography/PigeonHoles/README.md
- aacs4-writeups/Cryptography/ReallySenselessAdmins/README.md
- aacs4-writeups/Cryptography/RotateMe/README.md
- aacs4-writeups/Cryptography/SpeakPlainly/README.md
- aacs4-writeups/Cryptography/WereRelated/README.md
- aacs4-writeups/BinaryExploitation/AnInterestingStructure/README.md
- aacs4-writeups/BinaryExploitation/BinaryExploitation101/README.md
- aacs4-writeups/BinaryExploitation/DoYouCWhatIC/README.md
- aacs4-writeups/BinaryExploitation/HackerScanThyself/README.md
- aacs4-writeups/BinaryExploitation/LookAtTheTotem/README.md
- aacs4-writeups/BinaryExploitation/PartyROPinInTheHouse/README.md
- aacs4-writeups/BinaryExploitation/SerialKiller/README.md
- aacs4-writeups/BinaryExploitation/SpeedRacer/README.md
- aacs4-writeups/BinaryExploitation/StackCheckFailFail/README.md
- aacs4-writeups/BinaryExploitation/WhoDoesThisBelongTo/README.md
- aacs4-writeups/BinaryExploitation/YourCupOverfloweth/README.md

## Writeup Content


### File: aacs4-writeups/BinaryExploitation/AnInterestingStructure/README.md

# An Interesting Structure

## Binary Exploitation -- 250 points

### Description

There's a really cool simulator someone wrote that lets you run simulations of plants and animals. Check it out! challenge.acictf.com:60151 [structure](./structure) [structure.c](./structure.c)

### Hints

* No Buffer Overflows here...
* Heap Memory Mangement is hard, maybe there are some mistakes here
* What would happen if you could use memory after it's been free'd?


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/interesting-structure)



### File: aacs4-writeups/BinaryExploitation/BinaryExploitation101/README.md

# Binary Exploitation 101

## Binary Exploitation -- 50 points

### Description

Exploiting bugs in programs can definitely be difficult. Not only do you need a certain amount of reverse engineering required to identify vulnerabilities, but you also need to weaponize that vulnerability somehow. To get new hackers started, we included our annotated [BinEx101.c](./BinEx101.c) along with the compiled [BinEx101](./BinEx101).  
If you don't know where to start, download the source code and open it in a program with syntax highlighting such as `notepad++` or `gedit`. If you don't have the ability to use either of those, you can always use `vim`.  

You can connect to the problem at `telnet challenge.acictf.com 24680` or `nc challenge.acictf.com 24680`

### Hints

* Signed integers on modern computers generally use something called ["Two's Complement"](https://en.wikipedia.org/wiki/Two%27s_complement) for representing them. If this is your first time dealing with integers at this level, it is probably worth taking some time to get a basic understanding of them. In particular, you will need to understand what the largest positive number looks like, what -1 looks like, and how [overflow](https://en.wikipedia.org/wiki/Integer_overflow) is generally "handled".
* We've also included debug symbols in the binary and disabled compiler optimizations. Once you understand how the C code works from the source code, it is probably worth opening the compiled binary in something like [Ghidra](https://ghidra-sre.org/) to see both what the assembly looks like and how the recovered C code compares to the source code. Most of the other binary exploitation problems do not give you access to the raw source code.
* While many binary exploitation situations involve "non-standard" inputs (such as feeding shellcode as input to the name of something), this challenge does not. Once you understand the vulnerability, you can trigger it through normal interaction with the challenge. If you are having trouble on the math side, treating the binary representation of your 'target' number as an unsigned integer may be helpful.
* If you are new to binary exploitation (or C code), we really recommend reading the source file in its entirety as the comments try to explain many of the key concepts for this category of problems. For this specific problem, anyone not familiar C should definitely read the source file because the behavior of s.numbers[-1] is *very* different between C and some other popular languages (e.g. Python).


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#binary-exploitation-101---points-50)



### File: aacs4-writeups/BinaryExploitation/DoYouCWhatIC/README.md

# Do you C what I C

## Binary Exploitation -- 250 points

### Description

Remembering numbers is hard, luckily we've made [do\_you\_c\_what\_I\_c.exe](./do\_you\_c\_what\_I\_c.exe) to remember them for us! Launch it now!

### Hints

* It looks like they only added bounds checks on writes - I wonder if we can do anything with that?
* Where are stack cookies stored?
* I wonder what happens if you try to write more than 4 bytes?
* Maybe the [\_\_cdecl](https://docs.microsoft.com/en-us/cpp/cpp/cdecl?view=vs-2019) call puts something interesting on the stack?
* What memory protections are disabled?
* The flag is at D:\flag.txt


### Write-up

- [Write-up by psmitty](https://github.com/psmitty7373/ctf-writeups/tree/master/ACI-CS-2020/do_you_c_what_i_c)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/do-you-c-what-i-see)
- [Solve by dz00](https://github.com/dz00/ctf-writeups/blob/master/2020/acictf/pwn/do_you_c_what_i_c.py)



### File: aacs4-writeups/BinaryExploitation/HackerScanThyself/README.md

# Hacker, Scan Thyself

## Binary Exploitation -- 100 points

### Description

Hey, check out this really advanced port scanner!

### Hints

* Did you know you can use a negative index for arrays?
* The GOT and PLT sections look pretty [interesting](https://ctf101.org/binary-exploitation/what-is-the-got/)


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/HackerScanThyself)



### File: aacs4-writeups/BinaryExploitation/LookAtTheTotem/README.md

# Look At The Totem

## Binary Exploitation -- 500 points

### Description

What's at the top of the Totem? Let's grab our [qemu-system-arm](./qemu-system-arm) and find out.  
Building this monolith takes a bit of time. Please allow a minute for everything to boot.

### Hints

* QEMU escapes have a lot of [research](http://www.phrack.org/papers/vm-escape-qemu-case-study.html) [online](https://vishnudevtj.github.io/notes/qemu-vm-escape-cve-2019-14378).
* QEMU is not running within KVM.


### Write-up

- [Write-up by drewbards](https://github.com/drewbarbs/acictf-2020-writeups/tree/master/look-at-the-totem)



### File: aacs4-writeups/BinaryExploitation/PartyROPinInTheHouse/README.md

# Party ROPin in the House

## Binary Exploitation -- 300 points

### Description

Reading is good for the mind! Files: [client.py](./client.py). Listening on challenge.acictf.com:27746

### Hints

* Watch out for stack cookies!
* [ROPgadget](https://github.com/JonathanSalwan/ROPgadget) can be used to find gadgets in an ELF.
* Not everything will fit in one spot, you'll need a stack pivot to keep going.


### Write-up

- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/binex/party-roppin)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/party-roppin)



### File: aacs4-writeups/BinaryExploitation/README.md

## Binary Exploitation

**Total Problems:** 11
**Total Points:** 2475

| Challenge Name               | Points  | Concept |
| -----------------------------|---------|---------|
| [Binary Exploitation 101](./BinaryExploitation101/README.md) | 50 | |
| [Your Cup Overfloweth](./YourCupOverfloweth/README.md) | 75 | |
| [Hacker, Scan Thyself](./HackerScanThyself/README.md) | 100 | |
| [Serial Killer](./SerialKiller/README.md) | 100 | |
| [Stack Check Fail Fail](./StackCheckFailFail/README.md) | 150 | |
| [An Interesting Structure](./AnInterestingStructure/README.md) | 250 | |
| [Do you C what I C](./DoYouCWhatIC/README.md) | 250 | |
| [Who Does This Belong To](./WhoDoesThisBelongTo/README.md) | 250 | |
| [Party ROPin in the House](./PartyROPinInTheHouse/README.md) | 300 | |
| [Speed Racer](./SpeedRacer/README.md) | 450 | |
| [Look At The Totem](./LookAtTheTotem/README.md) | 500 | |



### File: aacs4-writeups/BinaryExploitation/SerialKiller/README.md

# Serial Killer

## Binary Exploitation -- 100 points

### Description

Serial Killer. Challenge Source: [Serial-Killer-Source.zip](./Serial-Killer-Source.zip). Listening on challenge.acictf.com:43821 - Connect with [NoteKeeperClient.jar](./NoteKeeperClient.jar)

### Hints

* You will need to run the client with `Java. ex: java -jar NoteKeeperClient.jar`  
* Use the client to connect to the server
* Java 8!
* Make sure you read the source...
* ncat is installed on the target machine
* The 'Security Manager' in recent versions of Java for Windows 10 is known to interfere with solutions to this problem. You may need to experiment with different/older versions of Java if your solution does not work as expected.


### Write-up

- [Video Walk-through by John Hammond](https://www.youtube.com/watch?v=GjwduwSltNU)



### File: aacs4-writeups/BinaryExploitation/SpeedRacer/README.md

# Speed Racer

## Binary Exploitation -- 450 points

### Description

We're off to the races! Go Speed Racer, Go Speed Racer, Go! Grab the challenge [files.tar.gz](./files.tar.gz) and start the challenge.

### Hints

* The dastardly Car Acrobatic Team has setup a bunch of [roadblock](https://github.com/angrave/SystemProgramming/wiki/Synchronization,-Part-1:-Mutex-Locks) along the race track. Watch out!
* The race organizer has taken measures to ensure that we're all racing in the same [arena](https://sourceware.org/glibc/wiki/MallocInternals#Arenas_and_Heaps).
* Netcat (`nc`) is installed on the server
* Latency is known to affect solutions to this challenge. If your solution works when tested locally but not against the Docker instance, try launching your solution from our shell server (SSH is enabled).


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/speed-racer)
- [Write-up by dz00](https://github.com/dz00/ctf-writeups/blob/master/2020/acictf/pwn/speed_racer_writeup.md)



### File: aacs4-writeups/BinaryExploitation/StackCheckFailFail/README.md

# Stack Check Fail Fail

## Binary Exploitation -- 150 points

### Description

We've found someone's password manager connected to the network. See if you can't extract the passwords from it. Grab the server files [files.tar.gz](./files.tar.gz).

### Hints

* Stack cookies always make things harder (or do they)?
* Take a look at the implementation of \_\_stack\_chk\_fail in libc.so
* Hmm, I wonder where \_\_stack\_chk\_fail gets the name of the program from?


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/who-does-this-belong-to)



### File: aacs4-writeups/BinaryExploitation/WhoDoesThisBelongTo/README.md

# Who Does This Belong To

## Binary Exploitation -- 250 points

### Description

The authors of the newly created dius archive format have setup a web server to demonstrate it. Take a look at the website and see if you can exploit it. Remember, RCE is just the beginning.

### Hints

* The challenge server has netcat (openbsd version) installed. It might be [useful](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet).
* 'DIUS'[::-1] files are a good place to start looking. However, they are useless once they've dropped privileges. Don't worry though, there are [plenty](https://jlajara.gitlab.io/posts/2019/06/15/Privesc_Ret2libc_ASLR_64.html) [of](https://recipeforroot.com/suid-binaries/) [guides](https://lwn.net/Articles/250468/) and [examples](https://git.zx2c4.com/calibre-mount-helper-exploit/about/) on the subject.
* Did you know that libraries can have [constructor and destructor routines](http://www.faqs.org/docs/Linux-HOWTO/Program-Library-HOWTO.html#INIT-AND-CLEANUP) too? Yeah, they're not just for classes anymore.


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/who-does-this-belong-to)
- [Write-up by drewbards](https://github.com/drewbarbs/acictf-2020-writeups/tree/master/who-does-this-belong-to)



### File: aacs4-writeups/BinaryExploitation/YourCupOverfloweth/README.md

# Your Cup Overfloweth

## Binary Exploitation -- 75 points

### Description

Your cup overfloweth. Drink up. Challenge Binary: [cup](./cup). Listening on challenge.acictf.com:44960

### Hints

* Your cup (the stack) is executable.
* Your cup will bounce when it hits the floor in the right spot [gadget](https://github.com/JonathanSalwan/ROPgadget)


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/YourCupOverfloweth)



### File: aacs4-writeups/Cryptography/HeadpieceSilver/README.md

# Headpiece Silver

## Cryptography -- 200 points

### Description

Can you break our unbreakable crypto? challenge.acictf.com:57715

### Hints

* How large is the N that you receieved?
* The password is alphanumeric
* telnet is known to interact poorly with the challenge instance. We recommend using 'netcat' to connect to the challenge.


### Write-up

No write-up or walk-through has been published for this challenge yet.



### File: aacs4-writeups/Cryptography/OverTimePaid/README.md

# Over Time: Paid

## Cryptography -- 50 points

### Description

After many months of hard work by our agents, we've gained access to a sensitive payroll document from a competitor. Unfortunately, it looks heavily encrypted. [document.encrypted](./document.encrypted) [source.py](./source.py)

### Hints

* Isn't it strange how each line of text in their document is of an identical length?
* Key Management is a difficult problem on the battlefield; maybe they reused key material in this document?
* Previous documents we've recovered had lines of encrypted whitespace as a result of text-formatting in the plaintext... Maybe that applies to this document too?


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#over-time-paid---points-50)



### File: aacs4-writeups/Cryptography/PigeonHoles/README.md

# Pigeon Holes

## Cryptography -- 350 points

### Description

Cars are just computers on wheels these days! See if you can extract the secret device key from this electronic key customization server: challenge.acictf.com:28973 [firmware\_server.py](./firmware\_server.py)

### Hints

* The flag will be a recognizable english phrase
* The flag will consist of ascii characters, digits, and underscores (\_)
* The flag will contain a bit of '1337' speak


### Write-up

- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/crypto/pigeon_holes)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/pigeon-holes)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/PigeonHoles)



### File: aacs4-writeups/Cryptography/README.md

## Cryptography

**Total Problems:** 7
**Total Points:** 1040

| Challenge Name               | Points  | Concept |
| -----------------------------|---------|---------|
| [Rotate Me](./RotateMe/README.md) | 5 | |
| [Really Senseless Admins](./ReallySenselessAdmins/README.md) | 35 | |
| [Over Time: Paid](./OverTimePaid/README.md) | 50 | |
| [Speak Plainly](./SpeakPlainly/README.md) | 150 | |
| [Headpiece Silver](./HeadpieceSilver/README.md) | 200 | |
| [We're Related](./WereRelated/README.md) | 250 | |
| [Pigeon Holes](./PigeonHoles/README.md) | 350 | |



### File: aacs4-writeups/Cryptography/ReallySenselessAdmins/README.md

# Really Senseless Admins

## Cryptography -- 35 points

### Description

We fired Julius, but the new guy apparently misplaced the file with our pivate key. All he could find was the encrypted flag and some file labeled 'params'. [flag.enc](./flag.enc) [params.txt](./params.txt)

### Hints

* The new guy apparently just treated the flag text as a [big-endian](https://en.wikipedia.org/wiki/Endianness#Big-endian) integer. Apparently, this made it easier for him to use the online tools he had found.
* Wouldn't it be nice if there were detailed [write-ups](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) about these cryptosystems?
* We found a few notes on the admin's desk. One note just had the URL of an online [RSA tool](https://www.cryptool.org/en/cto-highlights/rsa-step-by-step). The second note had [two](https://www.rapidtables.com/convert/number/decimal-to-hex.html) [URLs](https://www.rapidtables.com/convert/number/ascii-hex-bin-dec-converter.html) on it with 'plaintext ⇒ hex ⇒ int' scribbled beside it. The third one makes it look like the plaintext generated by the RSA tool will start with 104.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#really-senseless-admins---points-35)



### File: aacs4-writeups/Cryptography/RotateMe/README.md

# Rotate Me

## Cryptography -- 5 points

### Description

Our security manager, Julius, is confident nobody can break his encryption and so left the flag for everyone to see. [ciphered\_flag.txt](./ciphered\_flag.txt)

### Hints

* Does knowing the flag format give you any information about how the flag was encrypted?
* When in [Rome](https://en.wikipedia.org/wiki/Caesar_cipher)?
* Julius is notorious for playing games with the problem names...


### Write-up

This is a [rotational/shift cipher](https://en.wikipedia.org/wiki/Caesar_cipher) so just test for the rotation. See the [solve](./solve.py)

```
$ python3 solve.py
ACI{CrYpTo_FuN_fOr_AlL_vHYZgabJ}
```



### File: aacs4-writeups/Cryptography/SpeakPlainly/README.md

# Speak Plainly

## Cryptography -- 150 points

### Description

There's something suspicious about how account logins happen on this server... ? http://challenge.acictf.com:48438

### Hints

* Your username and the secret strongtoken are the only components of the encrypted cookie
* How does the length of your username effect the length of the cookie?
* It is possible to guess strongtoken one byte-at-a-time because of how AES-ECB works
* The strongtoken itself does not contain any ';' characters


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/speak-plainly)



### File: aacs4-writeups/Cryptography/WereRelated/README.md

# We're Related

## Cryptography -- 250 points

### Description

Recently, the Beacon Messenger App added support for one-time-read, 'disappearing' messages. We need you to find a flaw in their implementation, then decrypt an intercepted message provided to you upon connection. challenge.acictf.com:41413 [messenger.py](./messenger.py)

### Hints

* The server does not use any padding scheme and so ciphertexts are deterministic!
* RSA ciphertexts are 'just numbers'; they are malleable
* Can you create a ciphertext that is 'related to' the flag ciphertext? Maybe the server will respond with a 'related' plaintext!


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/were-related)



### File: aacs4-writeups/Forensics/BootMaster/README.md

# Boot Master

## Forensics -- 75 points

### Description

We found another floppy disk [files.tar.gz](./files.tar.gz), but we can't get this one to boot like we did the last one. The disk had been sitting around for a while so we're wondering if some of the data was corrupted. Any ideas?

### Hints

* It looks like file floppy.img identifies this one as just "data"...
* How does file recognize that an image contains a [master boot record](https://en.wikipedia.org/wiki/Master_boot_record)?
* You'll probably need some kind of 'hex editor' for this problem.
* Can we change one bit in the image and fix the problem?


### Write-up

 - [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/BootMaster)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/boot_master)



### File: aacs4-writeups/Forensics/BootRacer/README.md

# Boot Racer

## Forensics -- 150 points

### Description

We've found one last floppy disk [files.tar.gz](./files.tar.gz) that boots, but it looks like we're just being toyed with at this point.

### Hints

* Maybe the messages aren't lying. Are they printed at the same time?


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/Boot-racer.md)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/boot_racer)



### File: aacs4-writeups/Forensics/BootRiddle/README.md

# Boot Riddle

## Forensics -- 100 points

### Description

This floppy disk [files.tar.gz](./files.tar.gz) boots, but instead of a flag we see some silly riddle...

### Hints

* If only we could inspect the device's memory while it is running...
* QEMU's [monitor](https://en.wikibooks.org/wiki/QEMU/Monitor) or Bochs' [debugger](http://bochs.sourceforge.net/doc/docbook/user/internal-debugger.html) might be useful to read up on.


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/Boot-riddle.md)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/BootRiddle)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/boot_riddle)



### File: aacs4-writeups/Forensics/Bootcamp/README.md

# Bootcamp

## Forensics -- 20 points

### Description

We found an old floppy-drive laying around and think that there may be a flag hidden on it somewhere. We managed to copy the drive [files.tar.gz](./files.tar.gz), but there doesn't appear to be any kind of filesystem on it. In fact, all of the data appears to be on the first sector of the disk.

### Hints

* It looks like file floppy.img identifies it as a "DOS/MBR Boot Record"...
* What happens if you try booting the image?
* You probably don't have a real floppy drive that you can use, but what about a 'virtual' one?
* qemu-system-i386 floppy.img is our favorite means of 'booting' floppies, but 'Virtual Box' and 'bochs' are other alternatives (and they are all free).


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#bootcamp---points-20)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/boot_camp)



### File: aacs4-writeups/Forensics/ControlledAccess/README.md

# Controlled Access

## Forensics -- 50 points

### Description

We've been asked to help a certificate authority figure out what a [device](https://shop.hak5.org/products/shark-jack) they found plugged into their network was doing. They were able to dump the [firmware.bin](./firmware.bin) and would like to know if it allowed the attacker to connect to any devices that their firewall (which blocks inbound SSH) would have stopped. Their internal domain uses 'digisigner.local' for DNS host names. The flag is the hostname of the *internal* host that the hacker targeted (i.e. ACI{[local hostname targeted]}).

### Hints

* A tool like [binwalk](https://github.com/ReFirmLabs/binwalk) might be useful for inspecting the firmware.
* The [documentation](https://docs.hak5.org/hc/en-us/categories/360002117973-Shark-Jack) mentions that the 'attack' payload for this device lives in a very particular spot on the filesystem...


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#controlled-access---points-50)
- [Write-up by starkindustries Pt2](https://github.com/starkindustries/CyberStakes2020/tree/master/ControlledAccess)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/controlled_access)



### File: aacs4-writeups/Forensics/DrillToTheCenter/README.md

# Drill to the Center

## Forensics -- 300 points

### Description

It looks like our [drill](./drill) is [core](./core) - can you take a look at it for us?

### Hints

* [Core Dump](https://en.wikipedia.org/wiki/Core_dump)
* How much can I malloc?


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/DrillToTheCenter)
- [Write-up by Nic Hartley](https://nic-hartley.github.io/acictf-writeups/drill-to-the-center)



### File: aacs4-writeups/Forensics/FilingExtension/README.md

# Filing Extension

## Forensics -- 10 points

### Description

We went to apply for a tax-filing extension with the IRS, and they replied with this image saying it contained the code we needed. Unfortunately, our computer refuses to display it and just says that it isn't a PNG... [flag.png](./flag.png)

### Hints

* Is the extension the only way to tell a file's type?
* Wouldn't it be awesome if there was a [list](https://en.wikipedia.org/wiki/List_of_file_signatures) of way to identify files.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#filing-extension---points-10)

Use `file` to determine the type of file and then interact with it as appropriate.

```
$ file flag.png
flag.png: Zip archive data, at least v2.0 to extract
$ mv flag.png flag.zip
$ unzip flag.zip
Archive:  flag.zip
  inflating: flag.txt
$ ls
flag.txt  flag.zip
$ cat flag.txt
ACI{Something_witty_ec22b3a9}%
```



### File: aacs4-writeups/Forensics/KidsOnTheBlock/README.md

# Kids on the Block

## Forensics -- 400 points

### Description

Help! I was ransomwared and payed the ransom. Now I want to track my coins down and [find the culprit](http://{{server}}:{{port}}).

### Hints

* You can access transactions pragmatically with geth's javascript API
* All ransom transactions will move the ransom value or a logical fraction of it (such as a half or a fourth)
* Contracts take arguments from the transaction input data


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/kids-on-the-block)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/KidsOnTheBlock)
- [Write-up by Nic Hartley](https://nic-hartley.github.io/acictf-writeups/kids-on-the-block)



### File: aacs4-writeups/Forensics/NeedleInTheHaystack/README.md

# Needle in the Haystack

## Forensics -- 300 points

### Description

My PC crashed while I was running some program I found on the internet. I forgot what I typed into it, can you look through the [ram.img.tar.gz](https://challenge.acictf.com/static/fd6851d0187f64596550b2f8b2b517e2/ram.img.tar.gz) to find it?

**Note:** I did not download this locally due to size.

### Hints

* https://github.com/iAbadia/Volatility-Plugin-Tutorial
* volatility -f ram.img --profile=Win10x86\_15063 pslist | grep FlagApp
* .text:00311560 ; int \_\_cdecl main(int argc, co........


### Write-up

No write-up or walk-through has been published for this challenge yet.



### File: aacs4-writeups/Forensics/NotSoMeta/README.md

# Not So Meta

## Forensics -- 50 points

### Description

Look, it's the flag! Oh wait...it looks like we need to take a closer look... [not\_so\_meta.jpg](./not\_so\_meta.jpg)

### Hints

* How do images keep contextual information when they're created? (e.g., GPS data, creation timestamp, etc.)
* How do you [encode](https://en.wikipedia.org/wiki/Base64) binary data into common ASCII characters?


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/Not-so-meta.md)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/not_so_meta)



### File: aacs4-writeups/Forensics/README.md

## Forensics

**Total Problems:** 13
**Total Points:** 1905

| Challenge Name               | Points  | Concept |
| -----------------------------|---------|---------|
| [Filing Extension](./FilingExtension/README.md) | 10 | |
| [Bootcamp](./Bootcamp/README.md) | 20 | |
| [Controlled Access](./ControlledAccess/README.md) | 50 | |
| [Not So Meta](./NotSoMeta/README.md) | 50 | |
| [Boot Master](./BootMaster/README.md) | 75 | |
| [Boot Riddle](./BootRiddle/README.md) | 100 | |
| [That's More Than Enough](./ThatsMoreThanEnough/README.md) | 100 | |
| [Turtles All the Way Down](./TurtlesAllTheWayDown/README.md) | 100 | |
| [Boot Racer](./BootRacer/README.md) | 150 | |
| [Sharing is Caring](./SharingIsCaring/README.md) | 250 | |
| [Drill to the Center](./DrillToTheCenter/README.md) | 300 | |
| [Needle in the Haystack](./NeedleInTheHaystack/README.md) | 300 | |
| [Kids on the Block](./KidsOnTheBlock/README.md) | 400 | |



### File: aacs4-writeups/Forensics/SharingIsCaring/README.md

# Sharing is Caring

## Forensics -- 250 points

### Description

Hey Challanger. I know you're putting together that Veteran's Day presentation. Here's all the U.S. service seals straight from Wikipedia. I think you'll only need four of them to get the points across. More than that is just excessive, but it's up to you. [files.tgz](./files.tgz)

### Hints

* Research split secret schemes
* Four out of five secrets are required


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/Sharing-Is-Caring.md)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/sharing-is-caring)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/sharing_is_caring)



### File: aacs4-writeups/Forensics/ThatsMoreThanEnough/README.md

# That's More Than Enough

## Forensics -- 100 points

### Description

We think Jolly Jeff is up to no good. See if you can find the hidden message in his [JPEG Jammer](http://{{server}}:{{port}}).

### Hints

* Hex editors, such as bless or wxHexEditor, are great for viewing file contents. Install bless with "sudo apt install bless" or wxhexeditor with "sudo apt install wxhexeditor".
* Take a look at the [JPEG file format specification](https://en.wikipedia.org/wiki/JPEG_File_Interchange_Format#File_format_structure).


### Write-up

- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/thats_more_than_enough)



### File: aacs4-writeups/Forensics/TurtlesAllTheWayDown/README.md

# Turtles All the Way Down

## Forensics -- 100 points

### Description

Early this morning, a breach occurred on the server hosting our next-gen drone development repository. It is your job to figure out what was taken: [challenge.zip](./challenge.zip)

### Hints

* Our analysts are using IRC to share information and investigate this breach
* Everything you need lives within these PCAP's, you simply need to carve out the relevant files
* These ZIPS appear to have been generated with 7z
* FTP is a simple text-based protocol, with passive binary streams for file transfers


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/turtles-all-the-way-down.md)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/turtles_all_the_way_down)



### File: aacs4-writeups/Miscellaneous/AllYourBase/README.md

# All Your Base Are Belong to Us

## Miscellaneous -- 50 points

### Description

In honor of 30 years of terrible [translations](https://en.wikipedia.org/wiki/All_your_base_are_belong_to_us), we figured we'd give you a try at a series of (easier) translation problems. All you have to do is to translate bases by connecting to {{server}}:{{port}}. In case you're new to network programs, we even have some Python [starter\_code.py](./starter\_code.py) you can use.

### Hints

* You *could* do this by hand, but is it really worth that much effort?
* While we only want the final encoding, it's probably easier to break that into separate decode and encode steps for each question.
* Don't overthink 'raw' encoding...
* Your code for encoding/decoding will probably be very similar for 4 out of 6 encodings.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/AllYourBaseAreBelongToUs)



### File: aacs4-writeups/Miscellaneous/AssemblyVoyageur/README.md

# Assembly Voyageur

## Miscellaneous -- 300 points

### Description

It's time for an adventure. [Begin your travels here](http://challenge.acictf.com:31092/).

### Hints

* A good traveler knows that you should bring the right tools for the job: sudo apt install gcc gcc-aarch64-linux-gnu gcc-mips-linux-gnu gcc-powerpc-linux-gnu gdb-multiarch qemu-user-static
* Some assemblers support pseudo-instructions that aren't defined in the Instruction Set. Other assemblers may not support those pseudo-instructions, but do support the underlying instruction.


### Write-up

- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/misc/assembly_voyageur)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/assembly-voyageur)
- [Write-up by starfleetcadet75](http://starfleetcadet75.github.io/writeups/2020/05/03/cyberstakes-assembly-voyageur.html)



### File: aacs4-writeups/Miscellaneous/CanYouLookThisOver/README.md

# Can You Look This Over?

## Miscellaneous -- 150 points

### Description

Our ops guys found a malware author's staging server, we managed to exfiltrate the source to a backdoor they are spreading: [backdoor.tar.gz](./backdoor.tar.gz). I need you to report back once you have cracked their secret password.

### Hints

* What version / release of OpenSSH is in the provided archive?
* We know that their backdoor allows 'root' to login with a secret password
* Try diffing the backdoor tarball against the original source!
* The hashed password may be mixed case alphanumreic, but there shouldn't be any symbols!


### Write-up

- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/can_you_look_this_over)



### File: aacs4-writeups/Miscellaneous/ISEeYou/README.md

# I SEe You

## Miscellaneous -- 200 points

### Description

We think someone has been attacking our web server, can you help us by finding the IP address of the attacker in our logs? [audit.log.gz](./audit.log.gz)

### Hints

* The flag is the IP address of the attacker without any prefixes or braces around it.
* Audit logs can be read via the [ausearch](https://linux.die.net/man/8/ausearch) command.


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/i-see-you.md)



### File: aacs4-writeups/Miscellaneous/MoveZIG/README.md

# Move ZIG

## Miscellaneous -- 75 points

### Description

CATS is back at it on challenge.acictf.com:21191. Only this time he's throwing 500 problems at you. If you didn't use a program to solve the last one, you'll probably want [starter\_code.py](./starter\_code.py)...

### Hints

* We'll be impressed if you solve this without writing code. The hints on 'All Your Base Are Belong to Us' are still relevant here as well.


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/move-zig)



### File: aacs4-writeups/Miscellaneous/PartitionTwiceRecoverOnce/README.md

# Partition Twice, Recover Once

## Miscellaneous -- 250 points

### Description

I think I may have overwritten my secure file store, do you think you could recover the data for me? The password for the encrypted partition is "secret1234". [image.bin](./image.bin)

### Hints

* What is the current format of the image?
* What data is leftover from the original partition?
* Look at the last chunk of data in the image


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/partition-twice-recover-once)



### File: aacs4-writeups/Miscellaneous/PassThis/README.md

# PassThis

## Miscellaneous -- 250 points

### Description

Passing unit tests is harder than it looks. Use our sender: [send.sh](./send.sh), to test your code. Here's a base that you can start with [start\_tools.c](./start\_tools.c), and the header file it's based on: [mytools.h](./mytools.h). Go start the challenge!

### Hints

* Some string functions are REALLY unsafe, you should be able to find them online
* Using null pointers is usually bad news, checking for them is important


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/PassThis)



### File: aacs4-writeups/Miscellaneous/ProxyList/README.md

# Proxy List

## Miscellaneous -- 100 points

### Description

We need you to perform geolocation analysis on this list of IPs. We have attributed it to a malicious proxy network. Report back with the prevalent country of origin: [ips.txt](./ips.txt)

### Hints

* The flag is the name of the origin country (case-sensitive) found most frequently in the list
* Offline geolocation IP analysis can be scripted with a python package or two
* These IPs were collected in late 2019, if necessary you may need to use 'historical' geolocation data


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/Proxy-list.md)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#proxy-list)
- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/proxy_list)



### File: aacs4-writeups/Miscellaneous/README.md

## Miscellaneous

**Total Problems:** 12
**Total Points:** 1830

| Challenge Name               | Points  | Concept |
| -----------------------------|---------|---------|
| [All Your Base Are Belong to Us](./AllYourBase/README.md) | 50 | |
| [Move ZIG](./MoveZIG/README.md) | 75 | |
| [Proxy List](./ProxyList/README.md) | 100 | |
| [Can You Look This Over?](./CanYouLookThisOver/README.md) | 150 | |
| [Recovery And IDentification](./RecoveryAndIDentification/README.md) | 150 | |
| [I SEe You](./ISEeYou/README.md) | 200 | |
| [Partition Twice, Recover Once](./PartitionTwiceRecoverOnce/README.md) | 250 | |
| [PassThis](./PassThis/README.md) | 250 | |
| [Assembly Voyageur](./AssemblyVoyageur/README.md) | 300 | |
| [UNO Reverse Card](./UNOReverseCard/README.md) | 300 | |



### File: aacs4-writeups/Miscellaneous/RecoveryAndIDentification/README.md

# Recovery And IDentification

## Miscellaneous -- 150 points

### Description

Given two out of three disk images used in a RAID array, see if you can recover the data: [disk1.img.xz](./disk1.img.xz) [disk2.img.xz](./disk2.img.xz)

### Hints

* [Creating your own RAID array](https://unix.stackexchange.com/questions/302766/persistent-use-of-loop-block-device-in-mdadm) would be a good place to start.
* Try to [use your existing array to assemble a RAID array with the given disk images](https://superuser.com/questions/962395/assemble-3-drive-software-raid5-with-one-disk-missing).
* The flag will be in one of the recovered files


### Write-up

- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/recovery_and_identification)



### File: aacs4-writeups/Miscellaneous/UNOReverseCard/README.md

# UNO Reverse Card

## Miscellaneous -- 300 points

### Description

We've done it! We found an open service that will run code we give it! It looks like the server is multithreaded though... Files: [uno](./uno). Listening on challenge.acictf.com:48355

### Hints

* The flag is in a file named "flag".
* [Shellcode](https://bufferoverflows.net/developing-custom-shellcode-x64-linux/) doesn't always need to spawn a shell.


### Write-up

- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/misc/uno_reverse)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/uno-reverse-card)



### File: aacs4-writeups/README.md

# All-Army CyberStakes 4 Write-ups

Write-ups and Walk-throughs for the challenges in All-Army CyberStakes 4 (AACS 4).

I am accepting Pull Requests. If you have a write-up that you want included (linked), please let me know!

![acictf](https://github.com/eesantiago/Writeups/blob/master/CyberStakes_2020/acictf.JPG)

## Acknowledgements

I want to directly acknowledge and sincerely thank the Army Cyber Institute (ACI) for putting together this amazing competition and financially supporting it year after year. In particular, I want to recognize the hard work of [Roy Ragsdale](https://github.com/royragsdale) who was the driving force behind the continuation of All-Army CyberStakes and spent countless hours both championing CTFing as a learning mechanism as well as pouring his sweat and certainly tears into picoCTF platform upgrades (like the on-demand challenges you all know and love). Finally, I want to recognize the amazing work done by [GRIMM](https://www.grimm-co.com/) (all capitals!) - they created some amazing challenges this year and helped make AACS 4 a big success.

# Challenges by Category

## [Binary Exploitation](./BinaryExploitation/README.md)

**Total Problems:** 11
**Total Points:** 2475

| Challenge Name               | Points  | Write-up |
| -----------------------------|:-------:|:--------:|
| [Binary Exploitation 101](./BinaryExploitation/BinaryExploitation101/README.md) | 50 | ✔️ |
| [Your Cup Overfloweth](./BinaryExploitation/YourCupOverfloweth/README.md) | 75 | ✔️ |
| [Hacker, Scan Thyself](./BinaryExploitation/HackerScanThyself/README.md) | 100 | ✔️ |
| [Serial Killer](./BinaryExploitation/SerialKiller/README.md) | 100 | ✔️ |
| [Stack Check Fail Fail](./BinaryExploitation/StackCheckFailFail/README.md) | 150 | ✔️ |
| [An Interesting Structure](./BinaryExploitation/AnInterestingStructure/README.md) | 250 | ✔️ |
| [Do you C what I C](./BinaryExploitation/DoYouCWhatIC/README.md) | 250 | ✔️ |
| [Who Does This Belong To](./BinaryExploitation/WhoDoesThisBelongTo/README.md) | 250 | ✔️ |
| [Party ROPin in the House](./BinaryExploitation/PartyROPinInTheHouse/README.md) | 300 | ✔️|
| [Speed Racer](./BinaryExploitation/SpeedRacer/README.md) | 450 | ✔️ |
| [Look At The Totem](./BinaryExploitation/LookAtTheTotem/README.md) | 500 | ✔️ |

## [Cryptography](./Cryptography/README.md)

**Total Problems:** 7
**Total Points:** 1040

| Challenge Name               | Points  | Write-up |
| -----------------------------|:-------:|:--------:|
| [Rotate Me](./Cryptography/RotateMe/README.md) | 5 | ✔️ |
| [Really Senseless Admins](./Cryptography/ReallySenselessAdmins/README.md) | 35 | ✔️ |
| [Over Time: Paid](./Cryptography/OverTimePaid/README.md) | 50 | ✔️ |
| [Speak Plainly](./Cryptography/SpeakPlainly/README.md) | 150 | ✔️ |
| [Headpiece Silver](./Cryptography/HeadpieceSilver/README.md) | 200 | |
| [We're Related](./Cryptography/WereRelated/README.md) | 250 | ✔️ |
| [Pigeon Holes](./Cryptography/PigeonHoles/README.md) | 350 | ✔️ |

## [Forensics](./Forensics/README.md)

**Total Problems:** 13
**Total Points:** 1905

| Challenge Name               | Points  | Write-up |
| -----------------------------|:-------:|:--------:|
| [Filing Extension](./Forensics/FilingExtension/README.md) | 10 | ✔️ |
| [Bootcamp](./Forensics/Bootcamp/README.md) | 20 | ✔️ |
| [Controlled Access](./Forensics/ControlledAccess/README.md) | 50 | ✔️ |
| [Not So Meta](./Forensics/NotSoMeta/README.md) | 50 | ✔️ |
| [Boot Master](./Forensics/BootMaster/README.md) | 75 | ✔️ |
| [Boot Riddle](./Forensics/BootRiddle/README.md) | 100 | ✔️ |
| [That's More Than Enough](./Forensics/ThatsMoreThanEnough/README.md) | 100 | ✔️ |
| [Turtles All the Way Down](./Forensics/TurtlesAllTheWayDown/README.md) | 100 | ✔️ |
| [Boot Racer](./Forensics/BootRacer/README.md) | 150 | ✔️ |
| [Sharing is Caring](./Forensics/SharingIsCaring/README.md) | 250 | ✔️ |
| [Drill to the Center](./Forensics/DrillToTheCenter/README.md) | 300 | ✔️ |
| [Needle in the Haystack](./Forensics/NeedleInTheHaystack/README.md) | 300 | |
| [Kids on the Block](./Forensics/KidsOnTheBlock/README.md) | 400 | ✔️ |

## [Miscellaneous](./Miscellaneous/README.md)

**Total Problems:** 12
**Total Points:** 1830

| Challenge Name               | Points  | Write-up |
| -----------------------------|:-------:|:--------:|
| [All Your Base Are Belong to Us](./Miscellaneous/AllYourBase/README.md) | 50 | ✔️ |
| [Move ZIG](./Miscellaneous/MoveZIG/README.md) | 75 | ✔️ |
| [Proxy List](./Miscellaneous/ProxyList/README.md) | 100 | ✔️ |
| [Can You Look This Over?](./Miscellaneous/CanYouLookThisOver/README.md) | 150 | ✔️ |
| [Recovery And IDentification](./Miscellaneous/RecoveryAndIDentification/README.md) | 150 | ✔️ |
| [I SEe You](./Miscellaneous/ISEeYou/README.md) | 200 | ✔️ |
| [Partition Twice, Recover Once](./Miscellaneous/PartitionTwiceRecoverOnce/README.md) | 250 | ✔️ |
| [PassThis](./Miscellaneous/PassThis/README.md) | 250 | ➖ |
| [Assembly Voyageur](./Miscellaneous/AssemblyVoyageur/README.md) | 300 | ✔️ |
| [UNO Reverse Card](./Miscellaneous/UNOReverseCard/README.md) | 300 | ✔️ |

## [Reverse Engineering](./ReverseEngineering/README.md)

**Total Problems:** 11
**Total Points:** 2125

| Challenge Name               | Points  | Write-up |
| -----------------------------|:-------:|:--------:|
| [Reverse Engineering 101](./ReverseEngineering/ReverseEngineering101/README.md) | 25 | ✔️ |
| [Lockbox](./ReverseEngineering/Lockbox/README.md) | 50 | ✔️ |
| [National Dex #65](./ReverseEngineering/NationalDex65/README.md) | 100 | ✔️ |
| [Read it and Weep](./ReverseEngineering/ReadItAndWeep/README.md) | 100 | ✔️ |
| [What's the Difference?](./ReverseEngineering/WhatsTheDifference/README.md) | 100 | ✔️ |
| [Library Card](./ReverseEngineering/LibraryCard/README.md) | 150 | ✔️ |
| [Say What?](./ReverseEngineering/SayWhat/README.md) | 200 | ✔️ |
| [C&C Music Factory](./ReverseEngineering/CandCMusicFactory/README.md) | 300 | ✔️ |
| [CLRly just a crack-me](./ReverseEngineering/CLRlyJustACrackMe/README.md) | 300 | |
| [Are You Maching Me](./ReverseEngineering/AreYouMachingMe/README.md) | 350 | |
| [Into the Metaverse](./ReverseEngineering/IntoTheMetaverse/README.md) | 450 | ✔️ |

## [Web Security](./WebSecurity/README.md)

**Total Problems:** 13
**Total Points:** 1960

| Challenge Name               | Points  | Write-up |
| -----------------------------|:-------:|:--------:|
| [Out of Site](./WebSecurity/OutOfSite/README.md) | 5 | ✔️ |
| [More Out of Site](./WebSecurity/MoreOutOfSite/README.md) | 10 | ✔️ |
| [Most Out of Site](./WebSecurity/MostOutOfSite/README.md) | 20 | ✔️ |
| [Let me INNNNNN](./WebSecurity/LetMeInnnnnn/README.md) | 40 | ✔️ |
| [No Escape](./WebSecurity/NoEscape/README.md) | 60 | ✔️ |
| [DENIED](./WebSecurity/DENIED/README.md) | 75 | ✔️ |
| [Blame it on the Temp](./WebSecurity/BlameItOnTheTemp/README.md) | 150 | ✔️|
| [The SQL Always Sucks](./WebSecurity/TheSQLAlwaysSucks/README.md) | 150 | ✔️ |
| [Cookie Monster](./WebSecurity/CookieMonster/README.md) | 200 | ✔️ |
| [I Have Caught You Now](./WebSecurity/IHaveCaughtYouNow/README.md) | 250 | ✔️ |
| [Extremely Malicious Language](./WebSecurity/ExtremelyMaliciousLanguage/README.md) | 300 | ✔️ |
| [Who Is That In That Mirror](./WebSecurity/WhoIsThatInThatMirror/README.md) | 300 | ✔️ |
| [FirstFail](./WebSecurity/FirstFail/README.md) | 400 | ✔️ |



### File: aacs4-writeups/ReverseEngineering/AreYouMachingMe/README.md

# Are You Maching Me

## Reverse Engineering -- 350 points

### Description

Management has decided we need to start using this awesome "four-factor authenticated" password safe that also "self-destructs" every 18 hours so that the passwords inside can never be recovered. According to the vendor, it requires four different factors to work: the server program, the client program, the command line keys, and a separate lock combo entered once the program is running.  
  
Using the system has been a serious hit to our productivity! What used to be a simple encrypted email is now entering the password into a web form, sending out a link to the programs, downloading the programs, telling the OS that I'm not an idiot for running the programs, and entering all of the "factors" correctly (which we of course distributed via encrypted email...). And *then*, we have to hand jam the password out of a stupid PNG file! What's worse is it only works correctly on a single version of Mojave (10.14.6).  
  
Our security manager is also pretty skeptical it's as secure as the vendor says. He held onto the first set of programs he got when testing it in April, and thinks we can probably still get the key out of it. Challenge Files: [files.tar.gz](./files.tar.gz)

### Hints

* Try to figure out what bytes you actually control in the key.
* The vendor claims that they're digital safe is future proof. I'm not quite sure though.
* Static and dynamic analysis will both be useful.
* `binwalk -E cmachme` will show a graph of the entropy of a file. This can be useful for finding encrypted regions in a program.


### Write-up

No write-up or walk-through has been published for this challenge yet.




### File: aacs4-writeups/ReverseEngineering/CLRlyJustACrackMe/README.md

# CLRly just a crack-me

## Reverse Engineering -- 300 points

### Description

We found this digital safe program being used to protect important data. See if you can manage to extract it. Challenge Files: [files.tgz](./files.tgz)

### Hints

* Find the documentation for unfamiliar APIs on the MSDN website
* There are many tools for .NET analysis, if you find diminishing returns with one, try another.
* Static and dynamic analysis will both be useful.
* Break the challenge into it's component parts. Solve them one at a time. Delegate to experts on your team if the situation permits


### Write-up

No write-up or walk-through has been published for this challenge yet.




### File: aacs4-writeups/ReverseEngineering/CandCMusicFactory/README.md

# C&C Music Factory

## Reverse Engineering -- 300 points

### Description

We've recovered a portion of the payload of a targeted malware campaign aimed at recording executives. Can you pull out the server it is trying to exfiltrate data to? [music\_factory](./music\_factory)

### Hints

* Only submit the subdomain as the flag
* Some of the control flow looks pretty convoluted... maybe you can patch your way through it instead?


### Write-up

[Video Walk-through by Tim Nosco](https://www.youtube.com/watch?v=FyxkcxC701I&list=PL-nPhof8EyrGKytps3g582KNiJyIAOtBG&index=5)




### File: aacs4-writeups/ReverseEngineering/IntoTheMetaverse/README.md

# Into the Metaverse

## Reverse Engineering -- 450 points

### Description

We extracted the DRM module from a target device but haven't been able to reverse engineer its validation logic. See what you can do: [metaverse](./metaverse)

### Hints

* Have you heard of 'virtualization obfuscation'?
* The custom VM architecture is based on a 'stack machine cpu'
* Debugging a virtualized obfuscator can be hard... it might be best to extract the VM 'logic' and emulate it!


### Write-up

- [Write-up by starfleetcadet75](https://starfleetcadet75.github.io/writeups/2020/05/03/cyberstakes-into-the-metaverse.html)
- [Video Walk-through by Tim Nosco](https://www.youtube.com/watch?v=1oRm529jI34&list=PL-nPhof8EyrGKytps3g582KNiJyIAOtBG)
- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/re/into_the_metaverse)
- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/into-the-metaverse)\
- [Write-up by Nic Hartley](https://nic-hartley.github.io/acictf-writeups/into-the-metaverse/)



### File: aacs4-writeups/ReverseEngineering/LibraryCard/README.md

# Library Card

## Reverse Engineering -- 150 points

### Description

We have recovered a [liblibrary\_card.so](./liblibrary\_card.so) from the target. Can you reverse engineer it to recover any hidden secret information?

### Hints

* Are any functions different than the rest?
* Try cross referencing from the print\_flag function :)
* If trying to link the library with your own code, double check your LD\_LIBRARY\_PATH!


### Write-up

[Video Walk-through by Tim Nosco](https://www.youtube.com/watch?v=pyxxEmyGZCA&list=PL-nPhof8EyrGKytps3g582KNiJyIAOtBG)



### File: aacs4-writeups/ReverseEngineering/Lockbox/README.md

# Lockbox

## Reverse Engineering -- 50 points

### Description

We developed this password-protected [lockbox](./lockbox) which uses a super-secure, military-grade hash function with 256-bits of security to ensure only someone with the proper password can print the flag.

### Hints

* You do not need to crack the password.
* Tools like [ghidra](https://ghidra-sre.org/) are helpful when strings isn't enough.
* Looking at calls to printf and puts is probably a good place to start.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/Lockbox)



### File: aacs4-writeups/ReverseEngineering/NationalDex65/README.md

# National Dex #65

## Reverse Engineering -- 100 points

### Description

We found the encryptor ([encrypt](./encrypt)) but it won't decrypt [encrypted](./encrypted)?

### Hints

* I think they're using a cipher designed by Bruce Schneier.
* When reversing, it's useful to look for magic constants or use a tool like [findcrypt](http://www.hexblog.com/?p=27) ([idapython version](https://github.com/you0708/ida/tree/master/idapython_tools/findcrypt) or [Ghidra version](https://github.com/d3v1l401/FindCrypt-Ghidra)).
* Make sure you're using CBC mode.


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/national-dex-65)



### File: aacs4-writeups/ReverseEngineering/README.md

## Reverse Engineering

**Total Problems:** 11
**Total Points:** 2125

| Challenge Name               | Points  | Concept |
| -----------------------------|---------|---------|
| [Reverse Engineering 101](./ReverseEngineering101/README.md) | 25 | |
| [Lockbox](./Lockbox/README.md) | 50 | |
| [National Dex #65](./NationalDex65/README.md) | 100 | |
| [Read it and Weep](./ReadItAndWeep/README.md) | 100 | |
| [What's the Difference?](./WhatsTheDifference/README.md) | 100 | |
| [Library Card](./LibraryCard/README.md) | 150 | |
| [Say What?](./SayWhat/README.md) | 200 | |
| [C&C Music Factory](./CandCMusicFactory/README.md) | 300 | |
| [CLRly just a crack-me](./CLRlyJustACrackMe/README.md) | 300 | |
| [Are You Maching Me](./AreYouMachingMe/README.md) | 350 | |
| [Into the Metaverse](./IntoTheMetaverse/README.md) | 450 | |



### File: aacs4-writeups/ReverseEngineering/ReadItAndWeep/README.md

# Read it and Weep

## Reverse Engineering -- 100 points

### Description

We've found a mysterious binary lying around... Can you read it's secrets? challenge.acictf.com:40850 [read\_it](./read\_it)

### Hints

* There are two parts to the hidden message...
* A disassembler will help you make sense of the obfuscation
* A XOR B = C ::: A = C XOR B


### Write-up

- [Video Walk-through by Tim Nosco](https://www.youtube.com/watch?v=aBKY4kfnY_c&list=PL-nPhof8EyrGKytps3g582KNiJyIAOtBG)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/ReadItAndWeep)



### File: aacs4-writeups/ReverseEngineering/ReverseEngineering101/README.md

# Reverse Engineering 101

## Reverse Engineering -- 25 points

### Description

Reverse engineering can definitely be intimidating so we have a simple [RE101](./RE101) with which you can start. If you don't know where to start, check out the hints where we'll walk you through two different ways to solve this problem.

### Hints

* **Static analysis**: Static analysis is a process for examining a program without having a computer execute any code.

	+ From a command line on Linux, executing objdump -d RE101 will display the assembly code for the executable sections of the program (assumes you downloaded the file to the same folder).
	+ Flow of this program starts at \_start and proceeds 'down' the code.
	+ objdump -t RE101 will print all of the 'symbols' in the program. These are human-readable names for specific spots in memory. Symbols in the '.text' section tend to be function names and symbols in '.bss', '.data', and '.rodata' tend to be variable names.
	+ You should be able to see that the address of the 'flag' symbol (second command) appears in the first instruction of the '\_start' (first command).
	+ The hex values that are moved look like they are in the printable ASCII range.


* **Dynamic analysis**: Dynamic analysis is a method of examining the program as it is running to learn more about what it does. A common tool to help with this is a "debugger" like gdb.

	1. gdb RE101 will launch GDB and prepare it to debug our target, the RE101 executable. You may need to change the permissions on the downloaded file in order to make it executable (chmod a+x RE101).
	2. break \_exit will add a "breakpoint" which will pause the program's execution when we reach this point in the code. We're able to use '\_exit' here as a convenience and could have also specified a memory address instead.
	3. run will start execution and keep running until we hit the breakpoint we specified above.
	4. x /s &flag tells GDB to 'examine' a 'string' located at the address of the 'flag' symbol ('&' is the C symbol for 'address of').


* Instead of the dynamic analysis above, we could have also continued our static analysis by studying the assembly code we produced earlier. In particular, we can observe that the code is moving a pointer to the 'flag' variable into the EDI register in the first line. It then 'moves' a series of byte-constants into the memory location to which EDI points, 'incrementing' EDI in between each move. The final three lines in '\_exit' execute a Linux system call to 'exit', but that is relevant for this problem.
* When doing reverse engineering of x86 and x86-64 programs, Intel's [instruction set reference](https://www.intel.com/content/dam/www/public/us/en/documents/manuals/64-ia-32-architectures-software-developer-instruction-set-reference-manual-325383.pdf) can be very helpful. It can be intimidating to look at, but looking up the assembly instruction in this document will tell you exactly what it does.


### Write-up

- [Video Walk-through by Tim Nosco](https://www.youtube.com/watch?v=9dQFM5O4KFk&list=PL-nPhof8EyrGKytps3g582KNiJyIAOtBG)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#reverse-engineering-101---points-25)



### File: aacs4-writeups/ReverseEngineering/SayWhat/README.md

# Say What?

## Reverse Engineering -- 200 points

### Description

We intercepted some foreign documents. We think there's interesting information inside but the file is protected with a unique password algorithm: [chall.docm](./chall.docm)

### Hints

* Microsoft Office documents sometimes carry with them a powerful set of macros
* Microsoft Office is not required to extract the malicious macro, or solve the challenge
* There are a number of open source security tooling to script the extraction of Office macros
* The macro's obfuscation is rather light, try inserting some MsgBox prints to make sense of what it is doing
* If you're not careful, the document might ... change itself. Double check that your solution works against a 'fresh' copy of the challenge.


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/say-what)



### File: aacs4-writeups/ReverseEngineering/WhatsTheDifference/README.md

# What's the Difference?

## Reverse Engineering -- 100 points

### Description

Of course it's safe to download programs ([npp.6.8.7.bin.minimalist.7z](./npp.6.8.7.bin.minimalist.7z)) from the internet. Although the official archive from https://notepad-plus-plus.org/repository/6.x/6.8.7/npp.6.8.7.bin.minimalist.7z is different ([official.npp.6.8.7.bin.minimalist.7z](./official.npp.6.8.7.bin.minimalist.7z))...

**WARNING:** There apparently is some not very nice stuff in the npp source. This was not known prior to creating this challenge (who would have thought such a well-respected binary would have such trash).

### Hints

* Maybe the binary has been modified.
* You can try using BinDiff, Diaphora, or Ghidra's Program Differences Tool on npp.exe and notepad++.exe.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020/tree/master/WhatsTheDifference)



### File: aacs4-writeups/WebSecurity/BlameItOnTheTemp/README.md

# Blame it on the Temp

## Web Security -- 150 points

### Description

We had our intern create this awesome new secure file storage app! http://challenge.acictf.com:41843

### Hints

* https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Template%20Injection#jinja2
* https://werkzeug.palletsprojects.com/en/0.16.x/utils/#werkzeug.utils.secure\_filename


### Write-up

- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/web/blame_it_on_the_temp)



### File: aacs4-writeups/WebSecurity/CookieMonster/README.md

# Cookie Monster

## Web Security -- 200 points

### Description

Lets make some yummy cookies! Maybe you can even find some extra tasty ones: http://challenge.acictf.com:21188/.

### Hints

* The admin can see the flag on the admin page.
* You can control the value so select all you want.
* If you need an endpoint for a callback, [postb.in](https://postb.in) is a useful resource. You could also run a simple server on the competition's [shell server](/shell) using a command like python -m SimpleHTTPServer.


### Write-up

- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/cookie_monster)



### File: aacs4-writeups/WebSecurity/DENIED/README.md

# DENIED

## Web Security -- 75 points

### Description

Sometimes websites are afraid of the terminator finding things out. http://challenge.acictf.com:15499/ The flag is in flag.txt.

### Hints

* How can websites keep search engines from finding private information?
* Sometimes the developers leave some comments that give you a hint about what to do...
* You can use the cat command to read files


### Write-up

- [Write-up by allpurposebucket](https://github.com/allpurposebucket/CTF-Writeups/blob/master/ACICTF/DENIED.md)
- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#denied---points-75)



### File: aacs4-writeups/WebSecurity/ExtremelyMaliciousLanguage/README.md

# Extremely Malicious Language

## Web Security -- 300 points

### Description

There is a sick [ CYBER MAP ](http://challenge.acictf.com/problem/54863/). See if you can gain RCE to execute ./flag!

### Hints

* Stage 1: When a black hat crosses your xpath.
* Stage 2: A dark entity can reveal a lot about your operation.
* Stage 3: Take command of the system.
* Stuck? Check out /src.zip.


### Write-up

- [Video Walk-through by John Hammond](https://www.youtube.com/watch?v=kiGoOuuXWFI)
- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/web/extremely_malicious_language)



### File: aacs4-writeups/WebSecurity/FirstFail/README.md

# FirstFail

## Web Security -- 400 points

### Description

We are devloping a new secure password manager! Test it out here: http://challenge.acictf.com:57799

### Hints

* Does the password manager page perform any insecure actions?
* Try to create a new entry directly


### Write-up

- [Write-up by flakjacket](https://github.com/flakjacket95/cyberstakes_2020/tree/master/web/first_fail)



### File: aacs4-writeups/WebSecurity/IHaveCaughtYouNow/README.md

# I Have Caught You Now

## Web Security -- 250 points

### Description

XSS is a thing of the past! Read all about it here: http://challenge.acictf.com:41956

### Hints

* See what happens if you send XSS to the search
* This WAF might make you less secure
* Use parameter names to your advantage


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/i-have-caught-you-now)



### File: aacs4-writeups/WebSecurity/LetMeInnnnnn/README.md

# Let me INNNNNN

## Web Security -- 40 points

### Description

Let's see if you can break into our [secure vault](http://{{server}}:{{port}}).

**WARNING**: This problem is currently disabled.

### Hints

* How is the email determined for the password resending?


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#let-me-innnnnn---points-40)



### File: aacs4-writeups/WebSecurity/MoreOutOfSite/README.md

# More Out of Site

## Web Security -- 10 points

### Description

Well that was embarrassing... Who knew there was more to a web site then what the browser showed? Not to worry, we're back with a new and improved Javascript version! http://challenge.acictf.com:63225

### Hints

* The Javascript code in an onInput gets called anytime you interact with a text field.
* Is there anyway to view the Javascript definition of this function? It should just be text and your browser has it somewhere (it is running it after all).


### Write-up

Instead of validating it within the HTML `<input>`, you see this line when you look at the html source.

```
<input type="text" id="flag" name="flag" placeholder="ACI{...}" onInput="check_flag()" required>
```

So you then need to view the JavaScript source [./flag_checker.js](./flag_checker.js). This line is the check:

```
if (flag == "ACI{client_side_fail_bb3503bf}") {
        submit_button.disabled=false;
        status_field.innerHTML = "";
    } else {
        submit_button.disabled=true;
        status_field.innerHTML = "error: does not match flag";
    }
```

Note: If you have a hard time seeing the source in your browser when you click on flag_check.js, view it as source in your browser with [view-source:http://challenge.acictf.com:24637/flag_checker.js](view-source:http://challenge.acictf.com:24637/flag_checker.js)



### File: aacs4-writeups/WebSecurity/MostOutOfSite/README.md

# Most Out of Site

## Web Security -- 20 points

### Description

Alright, one more try. We had to think long and hard about how to keep you from viewing the flag. After a quick snack break, we had an epiphany. Your tricks won't work this time. http://challenge.acictf.com:35515/

### Hints

* What on earth could [snack food](https://en.wikipedia.org/wiki/HTTP_cookie) have to do with this problem?
* The browser must be storing these cookies somewhere...
* If you're getting tired of using a browser, the Python [Requests](https://requests.readthedocs.io/en/master/) library is pretty useful for interacting with web servers.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#most-out-of-site---points-20)

Same as before, but the string that it is checked against is not directly in the JavaScript. Looking at [./flag_checker.js](./flag_checker.js), you can see it gets the flag with this line: `var secret_flag = get_cookie("most_out_of_site_flag");`. It is checking against your cookie so let's go check out our network traffic (developer tools->network). Look at the response header when you visit http://challenge.acictf.com:35515/, you see:

```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 984
Set-Cookie: most_out_of_site_flag="ACI{cookies_fail_too_60f43d39}"; Expires=Wed, 06-May-2020 23:36:17 GMT; Max-Age=300; Path=/; SameSite=Strict
```

You can also just run the code from [./flag_checker.js](./flag_checker.js) in your console:

```
> get_cookie("most_out_of_site_flag")
"ACI{cookies_fail_too_60f43d39}"
```



### File: aacs4-writeups/WebSecurity/NoEscape/README.md

# No Escape

## Web Security -- 60 points

### Description

Since in-person events are currently banned, some magician we've never heard of is trying to sell us on the idea of a "digital" magic show where the magician logs in using an impossible password. For added assurances, one lucky audience member is able to login and see the hash of the password as proof the password is impossible. We're willing to bet the secret to this magic trick is not all that complicated. http://challenge.acictf.com:43248/

### Hints

* Inexperienced web application developers don't always esacpe/sanitize user inputs in there database query strings. This frequently allows [SQL injection](https://en.wikipedia.org/wiki/SQL_injection) attacks that result in unintended behavior.
* The developer was pretty new, so just causing the query to error out may get you more information for the exploit. What happens when you use a single ' or " in each of the login fields?
* You'll need to login as a specific user. If you're new to SQL syntax, [this](https://www.w3schools.com/sql/sql_where.asp) might be useful resource for understanding the intended query and how you can manipulate it for your purposes.


### Write-up

- [Write-up by starkindustries](https://github.com/starkindustries/CyberStakes2020#no-escape---points-60)

So you need to log in. Start by just putting `'` as both username and password. You then get this error:

```
Oops! It looks like the following query caused an error...
SELECT username FROM users WHERE username = ''' AND pwHash = '265fda17a34611b1533d8a281ff680dc5791b0ce0a11c25b35e11c8e75685509'
```

So you now know the query. Try the very traditional `admin' OR 1=1; -- ` and you log in, but you do not get the flag. Instead, you get `Welcome admin! The "hash" for account 'houdini' is 'Not a hash'.`. Ok, so you need to log in as 'houdini'. So lets try this as 'houdini' with `houdini' OR 1=1; -- `. You get the same `Welcome admin! The "hash" for account 'houdini' is 'Not a hash'.`. So this is still matching the same user as before based on the 'Welcome admin!'. The issue is the `OR 1=1` part is just making and, mostlikely, returning the first match and 'admin' is early in the alphabet. Lets just try to sort with `houdini' OR 1=1 ORDER BY username DESC LIMIT 1; -- `. And that works!

`Welcome Houdini, here's your flag: ACI{6a4352fb5adfa2bbccbe3a09965}`.

Note:
So I was super dumb and missed the obvious (but I noticed it doing this write-up)! Just do not do the `OR 1=1`. You can just log in with `houdini'; -- `. Problem solved.



### File: aacs4-writeups/WebSecurity/OutOfSite/README.md

# Out of Site

## Web Security -- 5 points

### Description

The flag submission system lets us see the strings you submitted even when they're wrong. Since some of you may consider that a privacy issue, we decided to demo a flag validation system that checks it client-side before sending the flag to us for checking. Why don't you give it a try: http://challenge.acictf.com:63225

### Hints

* How does your browser know what the right key is to do the check?
* If only there were a way to control+U're view of what the server sent you.


### Write-up

This problem validates a pattern in the input field of the html. Just go and view the source:

```
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Out of Site</title>
</head>

<body>
  <h1>Out of Site</h1>
  <h2>Flag Validation</h2>
  <p>Look we gave you an easy way to check the flag before you officially submit it!  Best of all, it checks it <i>twice</i>:  once on your end and once on our end.</p>
  <!-- Page Content -->
  <div>
    <form action="check" method="post">
      <label for="flag"><b>Flag:</b></label>
      <input type="text" id="flag" name="flag" placeholder="ACI{...}" pattern="ACI{hidden_in_plain_site_536af5dc}" required>
      <input type="submit">
    </form>
  </div>

</body>

</html>
```



### File: aacs4-writeups/WebSecurity/README.md

# Web Security

**Total Problems:** 13
**Total Points:** 1960

| Challenge Name               | Points  | Concept |
| -----------------------------|---------|---------|
| [Out of Site](./OutOfSite/README.md) | 5 | |
| [More Out of Site](./MoreOutOfSite/README.md) | 10 | |
| [Most Out of Site](./MostOutOfSite/README.md) | 20 | |
| [Let me INNNNNN](./LetMeInnnnnn/README.md) | 40 | |
| [No Escape](./NoEscape/README.md) | 60 | |
| [DENIED](./DENIED/README.md) | 75 | |
| [Blame it on the Temp](./BlameItOnTheTemp/README.md) | 150 | |
| [The SQL Always Sucks](./TheSQLAlwaysSucks/README.md) | 150 | |
| [Cookie Monster](./CookieMonster/README.md) | 200 | |
| [I Have Caught You Now](./IHaveCaughtYouNow/README.md) | 250 | |
| [Extremely Malicious Language](./ExtremelyMaliciousLanguage/README.md) | 300 | |
| [Who Is That In That Mirror](./WhoIsThatInThatMirror/README.md) | 300 | |
| [FirstFail](./FirstFail/README.md) | 400 | |



### File: aacs4-writeups/WebSecurity/TheSQLAlwaysSucks/README.md

# The SQL Always Sucks

## Web Security -- 150 points

### Description

We discovered an application in our environment that is apparently under development. Please identify the risk it poses.

**THIS PROBLEM HAS BEEN DISABLED**

**Note:** Solutions to this problem are known to be sensitive to connection latency. If your solution is working but very slowly, you may be able to speed up the process by running it from the competition's [shell server](/shell).

### Hints

* It's sometimes useful to know what kind of database is behind a webapp before trying to attack it. It can save you time and really narrow your efforts. I wonder if the developers accidentally left any clues laying around.
* SQL injuection attacks don't always result in you getting raw database contents sent directly back to you. Sometimes it is all about [patience](https://www.sqlinjection.net/time-based/) and [timing](https://hackernoon.com/timing-based-blind-sql-attacks-bd276dc618dd).
* Some attacks just are not practical to do by hand because they require precision and *lots* of repetition. Thankfully, tools like [sqlmap](https://github.com/sqlmapproject/sqlmap/wiki/Usage) can automate much of this for you. It even comes pre-installed on our shell server!
* Many tools use unique user-agent strings by default. If you notice that curl or sqlmap don't appear to be working properly, you may need to look into whether you can configure them to "impersonate" something else.


### Write-up

- [Write-up by eesantiago](https://github.com/eesantiago/Writeups/tree/master/CyberStakes_2020/sql_always_sucks)



### File: aacs4-writeups/WebSecurity/WhoIsThatInThatMirror/README.md

# Who Is That In That Mirror

## Web Security -- 300 points

### Description

We found a database backup from the Mirror Warehouse on the dark web. Take a look at the [database.sql](./database.sql) and see if you can compromise the Mirror Warehouse Website.  
The 'dark web' is slow, dont't worry, it may take up to 60 seconds for the site to come up.

### Hints

* Sometimes [SQL injection](https://media.blackhat.com/bh-us-12/Briefings/Cutlip/BH_US_12_Cutlip_SQL_Exploitation_WP.pdf) is just the beginning of an exploit.
* The website is written in Flask (and thus python3 is installed on the server).


### Write-up

- [Write-up by welchbj](https://github.com/welchbj/ctf/tree/master/writeups/2020/CyberStakes/who-is-that-in-that-mirror)

