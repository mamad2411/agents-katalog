<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dhicc
description: CTF writeups and security challenges by DHICC.
---

# Writeups by DHICC

Source repository: `/repos/DHICC`

## Repository Index

- writeups/README.md
- writeups/CTF/README.md
- writeups/python/README.md
- writeups/python/write-ups/Make It Good/README.md
- writeups/CTF/resources/README.md
- writeups/CTF/write-ups/hextroadinary.md
- writeups/CTF/write-ups/the_simpsons.md

## Writeup Content


### File: writeups/CTF/README.md

# This folder is for CTF Write-ups

Take note: naming convention for this folder is as such: `challengeName.md` so for example a write-up on the challenge _Defying Hell_ would be named as `defyinghell.md`

---

**Upload your *__completed__* write-ups in `/write-ups`**

CTF WriteUps:
- [x] Hextroadinary (ctflearn.com) -- Evangeline
- [x] The Simpsons (ctflearn.com) -- Hongshuo

---

The write-up should be in the format below: 

# _insert challenge name here_

**Challenge link:** _insert challenge url here_

**Challenge category:** _insert the category here_

**Challenge points:** _insert the challenge points here_

**Challenge description:** 

_insert the challenge description here. copy pasting from the site itself would work_

**Challenge solution:**

_insert your solution here. you can add pictures, gifs, videos etc... but most importantly is your thought process when solving this question. Do note: if you wish to include pictures, videos, etc you would need to upload the pictures into the `resources` folder then reference it in your markdown file_



### File: writeups/CTF/resources/README.md

## Naming Conventions:
Please follow the following naming convention when naming your files to be uploaded in this page: ```challengeName_pictureName```

So for eg: if this is a picture on the question _Defying Hell_ then a possible naming of the picture could be: `defyinghell_picture1`



### File: writeups/README.md

# DHICC WriteUps

**Upload your *__completed__* write-ups in the correct (respective) folder**

CTF WriteUps:
- [x] Hextroadinary (ctflearn.com) -- Evangeline
- [x] The Simpsons (ctflearn.com) -- Hongshuo

Python WriteUps:
- [ ] [Count Divisors](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/count-divisors/) -- Kingold 
- [x] [e-maze-in](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/e-maze-in-1aa4e2ac/) -- Rose
- [ ] [IT’S MAGIC!](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/its-magic/) -- Evangeline
- [x] [Two Strings](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/two-strings-4/) -- Jia Xiang
- [ ] [Friend's Relationship](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/friends-relationship-1/) -- Hongshuo
- [x] [Ali and Helping innocent people](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/cartag-948c2b02/) -- Joel
- [x] [Make It Good](https://codeforces.com/contest/1385/problem/C) -- Isaac



### File: writeups/python/README.md

# This folder is for Python Write-ups/Codes

Take note: naming convention for this folder is as such: `questionName.md` or `questionName.py` so for example a write-up/python file on the challenge about _converting an integer to binary keep leading zeros_  then the file could be named as `integer_to_binary_keep_leading_zeros.md` or `integer_to_binary_keep_leading_zeros.py` (this is just an example, as long as the file names are not repeating and understandable then it is fine)

---

**Upload your *__completed__* write-ups/python files through making a pull request to this folder**

Python WriteUps/Code:
- [ ] [Count Divisors](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/count-divisors/) -- Kingold 
- [x] [e-maze-in](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/e-maze-in-1aa4e2ac/) -- Rose
- [ ] [IT’S MAGIC!](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/its-magic/) -- Evangeline
- [x] [Two Strings](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/two-strings-4/) -- Jia Xiang
- [ ] [Friend's Relationship](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/friends-relationship-1/) -- Hongshuo
- [ ] [Ali and Helping innocent people](https://www.hackerearth.com/practice/basic-programming/input-output/basics-of-input-output/practice-problems/algorithm/cartag-948c2b02/) -- Joel
- [x] [Make It Good](https://codeforces.com/contest/1385/problem/C) -- Isaac

---

The write-up (**if its a md file**) should be in the format below:

# _insert question name here_

**Question link:** _insert question url here_

**Question description:**

_insert the question description here. copy pasting from the site itself would work_

**Question solution:**

_insert your solution here. you can add pictures, gifs, videos etc... but most importantly is your thought process when solving this question. Do note: if you wish to include pictures, videos, etc you would need to upload the pictures into the `resources` folder then reference it in your markdown file_

**If it is a python file, do also use the format above, but place it in the comments at the top of the file**

Thanks! :pray:



### File: writeups/python/write-ups/Make It Good/README.md

# Make It Good

_Question is extremely long, so you can find it here at [this contest link](https://codeforces.com/contest/1385/problem/C)_

tl;dr: This question involves an array 𐤀 of size n. 𐤀 needs to be made into a _good_ array, where a _good_ array is defined by an array which can be completely made into a non-decreasing array by transferring either the first or last element one by one. Here's an example:

b = [1,2,3,4,4,2,1] . This array is _good_ because we can obtain a non-decreasing array c from it by the following sequence of operations:

take the first element of b, so b=[2,3,4,4,2,1], c=[1]<br/>
take the last element of b, so b=[2,3,4,4,2], c=[1,1]<br/>
take the last element of b, so b=[2,3,4,4], c=[1,1,2]<br/>
take the first element of b, so b=[3,4,4], c=[1,1,2,2]<br/>
take the first element of b, so b=[4,4], c=[1,1,2,2,3]<br/>
take the last element of b, so b=[4], c=[1,1,2,2,3,4]<br/>
take the only element of b, so b=[], c=[1,1,2,2,3,4,4] — c is non-decreasing.

To make 𐤀 into a _good_ array, we can remove a prefix of size 𐡀, where a prefix is defined as a subarray starting from the first element of 𐤀. The task is to find the smallest possible value of 𐡀.

<ins>*Attempt to solve this question for yourself before proceeding*</ins>

## Question Analysis

This question was given in Codeforces Round #656, and I only made it past 3 questions before deciding to sleep. I did find my solution to the 3rd question quite cool, but I'm not really sure if its the most cost-efficient one. I will be going through my thought process and solving method below.

#### Initial Thoughts

Looking at the question at a glance, you can instantly know what this question is actually asking: Find the longest _good_ array ending at the last element of 𐤀. After you've found the length of this array, simply output the index of the beginning element of the _good_ array, which will be the length of the prefix to remove. Here's an example:

b = [4,3,3,8,4,5,2]. This array is not good yet, but we can see that the longest _good_ array ending at the last element 2 is [4,5,2], which gives a resulting non-decreasing array of [2,4,5]. Since the _good_ array starts at element 4 which is at index 4, the length of the prefix we have to remove is 4 (because an array starts from 0).

#### Pattern Recognition

If we find out what defining features a _good_ array has, we can check for those to determine its length. During the actual contest I was extremely stressed (like every other contest), so I usually wouldn't be able to catch such details at a glance. In such cases, it really helps to write out a few simple cases and extrapolate from there.

Listing out a few examples of _good_ arrays:<br/>
```
[1,2,1]
[3,2,2]
[2,2,3]
[2,3,4,4,2,1]
[1,2,3,4,4,3,2,2,1]
[5,25,26,1]
[1,2,4,5]
```

From these examples, it was clear that _good_ arrays were all in the form of a mountain (I made this up this isn't an actual term), where a mountain is defined by some length of non-decreasing elements followed by some other length of non-increasing elements. Note that these lengths can be 0, meaning that the array can be completely non-increasing/non-decreasing. In other words, the array goes up and down, just like a mountain.

Because an array is in this form, it is also symmetrical, meaning that it will still be _good_ if reversed. What that means is that we can traverse from the back of it to the front, instead of traversing from front to back, because the end of the _good_ array is much more well defined than the beginning.

From this analysis, we can identify 2 features of _good_ arrays:
- In mountain form
- Symmetrical

With this knowledge, all we have to do is traverse from the end to the beginning of the array, and find the point where the mountain stops.

## Writing Code

To find a mountain, we have to keep track of the gradient of the array, and the mountain ends when a minimum point is reached. I'll explain more about what this means in the next few lines.

An array's gradient (Once again I'm making this term up) will be defined as the change from the previous element to the current element. For example when traversing an array [3,4,5] the gradient is always +1, while in an array [4,5,3] the gradient goes from +1 (from 4 to 5) to -2 (from 5 to 3). When an array's gradient goes from positive to negative, a maxima is reached, and the mountain reaches its peak. When an array's gradient goes from negative to positive, a minima is reached, and the mountain ends.

To do this, I keep track of the gradient's polarity using a boolean `up`, which turns true when the gradient is positive, false when it's negative, and unchanged when it's 0. To calculate the polarity of the gradient, I traverse the array backwards, keeping track of the previous element, `foot`, and compare it to the current element `v[i]` at every interval. Using the boolean value and the polarity, we can easily identify the minimum point by checking if the mountain is descending and if the gradient is positive. If both are true, the point is minima and we output the current index -1.

I have uploaded 2 files, the `.cpp` one is the one I wrote during the contest, it's uncommented to save time but as a result it's also extremely short. The `.py` one I translated for the purpose of this write-up thing, which has relevant comments and descriptive variable names.



### File: writeups/CTF/write-ups/hextroadinary.md

# Hextroadinary

**Challenge link:** _https://ctflearn.com/challenge/158_

 **Challenge category:** _Cryptography_

**Challenge points:** _30 points_

**Challenge description:** 

Meet ROXy, a coder obsessed with being exclusively the worlds best hacker. She specializes in short cryptic hard to decipher secret codes. The below hex values for example, she did something with them to generate a secret code, can you figure out what? Your answer should start with 0x.            

0xc4115 0x4cf8

**Challenge solution:**

First, take out '0x' in front of each hex. Then, using XOR Calculator from http://xor.pw/# key in each individual input. Then click on 'Calculate XOR'. Then you would get the answer: c0ded. After this, you would need to add the 0x in front of your calculated XOR to give you the flag: 0xc0ded.



### File: writeups/CTF/write-ups/the_simpsons.md

## The Simpsons
Challenge link: https://ctflearn.com/challenge/160


Challenge category: Cryptography, hard 

Challenge points: 80 points

Challenge description:

Ya know, I was thinking... wouldn't the Simpsons use octal as a base system? They have 8 fingers... Oh, right! The problem! Ummm, something seems odd about this image... https://mega.nz/#!yfp1nYrQ!LOz_eucuKkjAaDqVvz3GWgbfdKWn8BhussKZbx6bUMg

Challenge solution:

 1. firstly, go to the link provided and download it as jpg.

 2. open the jpg with notepad -- in case there is something hidden. 
 We open it in **notepad or cyber chef** is to check if there are any hidden text in the meta data of the photo which in this case there  is!
 this will show a series of garbled characters on the notepad.
   such as : **"L&@��dQ�Q15ǭ��z"**

    

> We open it in notepad or cyber chef is to check if there are any
> hidden text in the meta data of the photo which in this case there is!

3. scroll down to the bottom, there are lines of python code 
   the python code states that: 
   
	   
	   encoded = 152 162 152 145 162 167 150 172 153 162 145 170 141 162
	   
	   key = chr(SolutionToDis(110 157 167 040 155 165 143 150 040 144 151 144 040 115 141 147 147 151 145 040 157 162 151 147 151    156 141 154 154 171 040 143 157 163 164 077 040 050 104 151 166 151 144 145 144 040 142 171 040 070 054 040 164 157 040 164    150 145 040 156 145 141 162 145 163 164 040 151 156 164 145 147 145 162 054 040 141 156 144 040 164 150 145 156 040 160 154    165 163 040 146 157 165 162 051)).
	   
	   key = key + key + chr(ord(key)-4). 
	   print(DecodeDat(key=key,text=encoded))
	   
   
4. decode the `encoded` and key from the code above using octal
   this is done by using cyberchef, choose "from octal"
   then put in the series of encoded numbers `(152 162 152 145 162 167 150 172 153 162 145 170 141 162)` as input
	
  >why use octal? -- because it is mentioned by the description :
  "wouldn't the Simpsons use octal as a base system"

  
5. After decoding the encoded text above, you would get text like `jrjerwhzkrexar`
   it suggests that after converting this series of number from octal, it returns you the original text, which is        `jrjerwhzkrexar`.
   Check out the website of cyberchef: https://gchq.github.io/CyberChef/#recipe=From_Octal('Space')&input=MTUyIDE2MiAxNTIgMTQ1IDE2MiAxNjcgMTUwIDE3MiAxNTMgMTYyIDE0NSAxNzAgMTQxIDE2Mg
   
6. After which you can get key using the instructions as stated in the hex-dumped value of the picture. The instructions are as follows:
- 'How much did Maggie originally cost? 
- Divided by 8, to the nearest integer, and then plus four)'

7. search the answers of the question in key online and do calculation get `110`

   for the answer of the first question, it can be found on this website:
   https://mashable.com/2014/08/21/simpsons-facts/#:~:text=1.,raising%20a%20child%20in%201989.
   
   it gives `$847.67`
   then `847.67 / 8`, to the nearest integer, it will be `110`
   
8. follow the key - `use chr(the result of the key)`
 get key = n
   
    as the code states: `chr(the solution)`
   > **chr()** means **convert the number to letter according to the ACSII table**:
   the table can be found here : http://www.asciitable.com/
   
   the letter returned is `n` 
   
9. then the line below gives a new value of 
`key = key + key + chr(ord(key)-4)`, 
get **new key** as `nnj`

	  key is assigned to `key + key + chr(ord(key)-4)`
	   `key + key = n + n = nn`
	   then `chr(ord(key)-4)`:
    > **ord()** means to **convert the key value 
     back to the number according to the ascii table**
	   
	  so it gives value as 110, then `110 - 4 = 106`
	   so `chr(ord(key)-4) == chr(106) == j`
	   so `key = nnj` 
	   
10. finally, use the new key to decipher the text `jrjerwhzkrexar`

	   as it says need to decode the text `jrjerwhzkrexar`, 
	   it will be done on cyberchef again
	   use **vigenere decoded**, use **nnj as keyword**, put `jrjerwhzkrexar` in the input window 
	   then it will return `wearenumberone`
   
12. get the flag `wearenumberone`, submit 

