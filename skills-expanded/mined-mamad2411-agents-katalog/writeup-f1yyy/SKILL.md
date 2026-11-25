<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-f1yyy
description: CTF writeups and security challenges by f1yyy.
---

# Writeups by f1yyy

Source repository: `/repos/f1yyy`

## Repository Index

- RealWorldCTF/README.md
- RealWorldCTF/SCSI/README.md
- RealWorldCTF/kid-vm/README.md
- RealWorldCTF/state-of-the-art vm/README.md

## Writeup Content


### File: RealWorldCTF/README.md

Here are four virtulization escape challenges and writeups used in realworld CTF.



### File: RealWorldCTF/SCSI/README.md

writeup:https://blog.rpis.ec/2018/08/realworld-quals-2018-scsi.html



### File: RealWorldCTF/kid-vm/README.md

writeup:</br>
https://github.com/perfectblue/ctf-writeups/blob/master/RealWorldCTF-2018/kidvm.md</br>



### File: RealWorldCTF/state-of-the-art vm/README.md

# writeup
It's just a newsest qemu run without -monitor.So you can use qemu-monitor to execve some commands.</br>
Once you enter into qemu monitor,you can use this to execve a command(The qemu process must run as root):</br>
netdev_add tap,id=net0,ifname=flag,script=/bin/cat</br>

