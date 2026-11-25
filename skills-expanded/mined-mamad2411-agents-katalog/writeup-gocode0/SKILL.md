<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gocode0
description: CTF writeups and security challenges by GoCode0.
---

# Writeups by GoCode0

Source repository: `/repos/GoCode0`

## Repository Index

- Writeups/BlueHensCTF-Forensics-The-Quantum-Realm.md
- Writeups/Misc-Forensics-BuckEyeCTF2022-KeyboardWarrior.md
- Writeups/README.md

## Writeup Content


### File: Writeups/README.md

#### CTF Write-ups! 



### File: Writeups/BlueHensCTF-Forensics-The-Quantum-Realm.md

I download the Antman.jpeg file, you can use many steg tools (binwalk, foremost ...) to find that the file contains a text file containing base64 encoded text.
I used this command to store the decoded data to a text file: 
```cat could_this_be_it.txt | base64 -d > b64.txt```
On first look, the data is obviously RGB values of an image. We need the data to be formatted in a certain way in order to use it like in this python script:
```
from PIL import Image
import numpy as np
pixels = [
   [(54, 54, 54), (232, 23, 93), (71, 71, 71), (168, 167, 167)],
   [(204, 82, 122), (54, 54, 54), (168, 167, 167), (232, 23, 93)],
   [(71, 71, 71), (168, 167, 167), (54, 54, 54), (204, 82, 122)],
   [(168, 167, 167), (204, 82, 122), (232, 23, 93), (54, 54, 54)]
]
array = np.array(pixels, dtype=np.uint8)
new_image = Image.fromarray(array)
new_image.save('new.png')
```
I used vim to format the data so I can use it in the python program, if you want to learn vim, this will be a great exercise.
The difficulty of the challenge is finding the correct dimensions of the image, the only information we have is the total number of pixels 22400.

Dividers of 22400:1, 2, 4, 5, 7, 8, 10, 14, 16, 20, 25, 28, 32, 35, 40, 50, 56, 64, 70, 80, 100, 112, 128, 140, 160, 175, 200, 224, 280, 320, 350, 400, 448, 560, 640, 700, 800, 896, 1120, 1400, 1600, 2240, 2800, 3200, 4480, 5600, 11200, 22400.

After many tries and fails, I found out that the correct dimensions were 400x56.
First, use in vim theses exact commands, to remove spaces, replace '\n' with ',' from b64.txt:
```
:%s/ //g
:%s/\n/,/g
```
Then make sure you insert the first '[', after that, we will use a macro to set the number of pixels in each horizontal line, counting the number of pixels by eye is impossible, what we can do is to find a looping sequence (look for the 400th occurence of ')', append '],' then return to line and replace the ',' with '[') using vim macro to automate the task. Make sure your cursor is on the first chars of the file, before first occurence of ')'.
Then type 'qa' to start recording a macro named 'a' then:
```
400f)a],ENTER
ESCAPE
r[q
```
the final q at the end stops the macro from recording, finally all you need to do is to type this remaining command to repeat the sequence 55 times:
```
55@a
```
Make sure the data is properly formatted, insert it in the python script, the script will create the correct image.



### File: Writeups/Misc-Forensics-BuckEyeCTF2022-KeyboardWarrior.md

![](./buckeyeCTF2022-capure2.png)

The challenge pcap [file](./keyboardwarrior.pcap) contains bluetooth usb transmitted data that you can decode following theses two steps:
> Extract the bluetooth data in json format from the pcap file (we will use tshark).

> Create a keymap of each keystroke data from the reference (look page 55+):  https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf


One line bash solution: 
```sh
tshark -r keyboardwarrior.pcap -Y btatt.opcode==0x001b -T json -V > hci.json && python solvepcap.py
```
![](./buckeyeCTF2022Capture.png)
Python code:
```py
from json import load, dump
# Creating keymap
keymap = {'30':'}','2d':'_','2f':'{', '': '', '00': '0', '04': 'a', '05': 'b', '06': 'c', '07': 'd', '08': 'e', '09': 'f', '0a': 'g', '0b': 'h', '0c': 'i', '0d': 'j', '0e': 'k', '0f': 'l', '10': 'm', '11': 'n', '12': 'o', '13': 'p', '14': 'q', '15': 'r', '16': 's', '17': 't', '18': 'u', '19': 'v', '1a': 'w', '1b': 'x', '1c': 'y', '1d': 'z', '1e': '1', '1f': '2', '20': '3', '21': '4', '22': '5', '23': '6', '24': '7', '25': '8', '26': '9', '27': '0', '28': '\n', '2a': '\x08', '2c': ' ', '34': '"', '36': ',', '37': '.', '38': '?'}

# Initiate the flag :
flag = ""

# Open the json file saved by tshark with the filter
with open("hci.json", "r") as f:
    t = load(f)

# Extract the correct values of data
t1 = [x["_source"]["layers"]["btatt"]["btatt.value"][6:8] for x in t]

# Remove "00"
while("00" in t1) :
    t1.remove("00") 

# Append each decoded character to the flag
for x in t1:
    flag += keymap[x]
print(flag)
```

