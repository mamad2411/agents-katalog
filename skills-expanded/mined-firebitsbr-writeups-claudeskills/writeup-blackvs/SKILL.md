<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-blackvs
description: CTF writeups and security challenges by BlackVS.
---

# Writeups by BlackVS

Source repository: `/repos/BlackVS`

## Repository Index

- CTFs/README.md
- CTFs/GRUCon2021/README.md
- CTFs/HWIO2021/README.md
- CTFs/NNC2019/README.md
- CTFs/r2con2020/README.md
- CTFs/r2con2020/tasks/aesthetic/README.md
- CTFs/r2con2020/tasks/defuse/README.md
- CTFs/r2con2020/tasks/exit/README.md
- CTFs/r2con2020/tasks/hellcode/README.md
- CTFs/r2con2020/tasks/license/README.md
- CTFs/NNC2019/Binary Hero/blackvs.md
- CTFs/NNC2019/BruteSearcher/blackvs.md
- CTFs/NNC2019/Extra/README.md
- CTFs/NNC2019/Mr Bean Walker/blackvs.md
- CTFs/NNC2019/NoNameCon SpyNet/blackvs.md
- CTFs/NNC2019/Ployka PWNer/blackvs.md
- CTFs/NNC2019/Side Blennel/blackvs.md
- CTFs/NNC2019/Extra/1. Firmware builder/README.md
- CTFs/NNC2019/Extra/2. Patching/README.md
- CTFs/NNC2019/Extra/2. Patching/part1.md
- CTFs/NNC2019/Extra/2. Patching/part2.md
- CTFs/NNC2019/Extra/3. MITM/README.md
- CTFs/NNC2019/Extra/3. MITM/part1/README.md
- CTFs/NNC2019/Extra/3. MITM/part2/README.md
- CTFs/NNC2019/Extra/3. MITM/part2/README_0x4.md
- CTFs/NNC2019/Extra/3. MITM/part3/README.md
- CTFs/HWIO2021/BHV/README.md
- CTFs/HWIO2021/CTS/DESC.md
- CTFs/HWIO2021/CTS/README.md
- CTFs/HWIO2021/CTS/cts-get-signal.md
- CTFs/HWIO2021/CTS/cts-signals.md
- CTFs/HWIO2021/CTS/cts-tools.md
- CTFs/HWIO2021/CTS/cts-utils.md
- CTFs/HWIO2021/CTS/task1.md
- CTFs/HWIO2021/CTS/task2.md
- CTFs/HWIO2021/CTS/task3.md
- CTFs/HWIO2021/CTS/task4.md
- CTFs/HWIO2021/CTS/task5.md
- CTFs/HWIO2021/CTS/task6.md
- CTFs/HWIO2021/CTS/task7.md
- CTFs/GRUCon2021/ssh1/README.md
- CTFs/GRUCon2021/ssh2/README.md
- CTFs/GRUCon2021/ssh3/README.md
- CTFs/GRUCon2021/ssh4/README.md
- CTFs/GRUCon2021/surprise/README.md
- CTFs/GRUCon2021/task1/README.md
- CTFs/GRUCon2021/task2/README.md
- CTFs/GRUCon2021/task3/README.md
- CTFs/GRUCon2021/task4/README.md
- CTFs/GRUCon2021/task5/README.md
- CTFs/GRUCon2021/task6/README.md
- CTFs/GRUCon2021/task7/README.md
- CTFs/GRUCon2021/task8/README.md
- CTFs/GRUCon2021/task9/README.md

## Writeup Content


### File: CTFs/GRUCon2021/README.md

![Title](img/conf_title.png)


## Rules 

[GRUCon Home](https://events.gnuradio.org/event/8/)

[CTS CTF Home page](https://cts.gnuradio.org/)

[Scoreboard](img/scoreboard.png)

Top teams ( my team is **Radio Coders** %)

* [Place 1](img/place1_team.png)
* [Place 2](img/place2_team.png)
* [Place 3](img/place3_team.png)

My writeups:

## Write-ups

[Tasks graph](img/tasks.png)
## Level 1
 - [Task 1](task1/README.md)
 - [Task 2](task2/README.md)
## Level 2
 - [Task 3](task3/README.md)
## Level 3
 - [Task 4](task4/README.md)
 - [Task 5](task5/README.md)
## Level 4
 - [Task 6](task6/README.md)
 - [Task 7](task7/README.md)
## Level 5
 - [Task 8](task8/README.md)
 - [Task 9](task9/README.md)

## Surprise level
 - [Surprise Signal 1](surprise/README.md)

## Ssh! level
 - [Whisper 1](ssh1/README.md)
 - [Whisper 2](ssh2/README.md)
 - [Whisper 3](ssh3/README.md)
 - [Whisper 4](ssh4/README.md)



### File: CTFs/GRUCon2021/ssh1/README.md

# Whisper 1

![text](img/desc.png)

## Input files:

* [wsprspots.csv](input/wsprspots.csv )

## Solution:

Input file containes data in [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format:

```
Reporter,Distance,Call Sign,Reporter's Grid,Grid
KA7OEI-1,2955,1Z2CPJ,DN31uo,FN25dj
DB9OH,816,2E0SXX,JO52ji,IO91
DC1RDB,945,2E0SXX,JN58ss,IO91
DJ4FF,886,2E0SXX,JN47vq,IO91
...
```
PS: first line is column's names!

To find country with the most reports reporter I wrote simple Python [script](script/task1.php):

```Python
#!/usr/bin/env python3

import os, sys
from collections import Counter
from pyhamtools import LookupLib, Callinfo

res_reporter = Counter()

res_maxdst = 0
res_reporter_most = None
res_most_distant = None

with open("../input/wsprspots.csv","rt") as f:
    lines=f.readlines()
    for l in lines[1:]:
        l=l.strip()
        reporter, sdistance, callsign, reporter_grid, grid = l.split(',')
        distance = int(sdistance)
        res_reporter[reporter] +=1
    res_reporter_most = res_reporter.most_common(1)[0][0]

    my_lookuplib = LookupLib(lookuptype="countryfile")
    cic = Callinfo(my_lookuplib)
    try:
        print("Reporter with the most reports located in: {}, {}".format(res_reporter_most, cic.get_country_name(res_reporter_most)))
    except:
        pass
```

To get country name from call sign's I used [pyhamtools](https://github.com/dh1tw/pyhamtools) module.


### File: CTFs/GRUCon2021/ssh2/README.md

# Whisper 2

![text](img/desc.png)

## Input files:

* [wsprspots.csv](input/wsprspots.csv )

## Solution:

Input file containes data in [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format:

```
Reporter,Distance,Call Sign,Reporter's Grid,Grid
KA7OEI-1,2955,1Z2CPJ,DN31uo,FN25dj
DB9OH,816,2E0SXX,JO52ji,IO91
DC1RDB,945,2E0SXX,JN58ss,IO91
DJ4FF,886,2E0SXX,JN47vq,IO91
...
```
PS: first line is column's names!

To find for reporter from previous task country of origin of the most distant receved message I extended Python script to [script](script/task2.php):

```Python
#!/usr/bin/env python3

import os, sys
from collections import Counter
from pyhamtools import LookupLib, Callinfo

res_reporter = Counter()

res_maxdst = 0
res_reporter_most = None
res_most_distant = None

with open("../input/wsprspots.csv","rt") as f:
    lines=f.readlines()
    for l in lines[1:]:
        l=l.strip()
        reporter, sdistance, callsign, reporter_grid, grid = l.split(',')
        distance = int(sdistance)
        res_reporter[reporter] +=1
    res_reporter_most = res_reporter.most_common(1)[0][0]

    my_lookuplib = LookupLib(lookuptype="countryfile")
    cic = Callinfo(my_lookuplib)
    try:
        print("Reporter with the most reports located in: {}, {}".format(res_reporter_most, cic.get_country_name(res_reporter_most)))
    except:
        pass

    for l in lines[1:]:
        l=l.strip()
        reporter, sdistance, callsign, reporter_grid, grid = l.split(',')
        distance = int(sdistance)
        if reporter == res_reporter_most and distance>res_maxdst:
            res_maxdst = distance
            res_most_distant = callsign

    print("Country of origin of the most distant received messages: {}, {}, {}".format(res_most_distant, res_maxdst, cic.get_country_name(res_most_distant)))
```




### File: CTFs/GRUCon2021/ssh3/README.md

# Whisper 3

![text](img/desc.png)


## Input files:

* [wsprspots.csv](input/wsprspots.csv )

## Solution:

Input file containes data in [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format:

```
Reporter,Distance,Call Sign,Reporter's Grid,Grid
KA7OEI-1,2955,1Z2CPJ,DN31uo,FN25dj
DB9OH,816,2E0SXX,JO52ji,IO91
DC1RDB,945,2E0SXX,JN58ss,IO91
DJ4FF,886,2E0SXX,JN47vq,IO91
...
```
PS: first line is column's names!

Just simple python coding %) - I have such expirience from competitive programming CTFs.
Some notes:
* I used BFS for nodes conenctivity checking
* BFS run only once due - during this run we calculate minimal distance to every reachable node. If node is not reachable distance is left 0 and correspindent value in V is False.
* at the end of BFS method I just count number of not-visited and divide on the number of all nodes except myself. Due to first I forgot to not count myself %) - I spent a lot of false tries %))) 
* before BFS I converted all nodes names (i.e. call signs) to numbers. It will simplifies arrays usage + increase total perfomance.

```python
#!/usr/bin/env python3

import os, sys
from collections import Counter
from types import DynamicClassAttribute
from collections import *
from itertools import *
#from pyhamtools import LookupLib, Callinfo


# For the file in Whisper 1, what percent of the other nodes are unreachable 
# regardless of hop count from "F5MAF"? 
# Assume any node that is visible to a reporter may be reached by the reporter. Round to two decimal places.

node2check = "F5MAF"

# vertices have nums 0..N-1
class Graph(object):
    def __init__(self,n):
        self.VN=n
        self.G = [[] for _ in range(n)]
        # BFS
        self.V  = None # visited
        self.D  = None # min distance
        self.PR = None # parent


    def add_edge(self,x,y):
        self.G[x].append(y)
        #not directed:
        self.G[y].append(x)

    def BFS(self,root=0):
        N =self.VN
        P  = self.PR  = [None]*N
        D  = self.D   = [0]*N
        V  = self.V = [False]*N 

        G  = self.G 
        i=0
        # start from root node
        v=root
        D[root]=0
        q=deque([root])
        while q:
            v=q.popleft()
            pv=P[v]
            dv=D[v]
            V[v] = True
            for w in G[v]:
                if V[w]: 
                    continue #already visited
                P[w]=v
                D[w]=dv+1
                q.append(w)
        # count unreachable
        notvisited = len(V)-sum(V)
        return notvisited/(len(V)-1) # -1 to exclude root from result

# vertices have nums 0..N-1
map_cs2num = dict()
map_num2cs = []
edges = set() 

# maps callsigns to numeric node ids
# nodes numbered 0..N-1 where N is a numberof distinct call signs
def get_cs_idx(cs):
    # try get numeric id of node
    n_cs =  map_cs2num.get(cs, None)
    if n_cs!=None:
        return n_cs #if found - return it
    #assign id to new node
    n_cs = len(map_cs2num)
    map_num2cs.append(cs)
    map_cs2num[cs]=n_cs
    return n_cs

# parse input file 
with open("../input/wsprspots.csv","rt") as f:
    lines=f.readlines()
    for l in lines[1:]:
        l=l.strip()
        reporter, sdistance, callsign, reporter_grid, grid = l.split(',')
        n_rep = get_cs_idx(reporter)
        n_cs  = get_cs_idx(callsign)
        edges.add( (n_rep, n_cs) )
        if reporter == node2check:
            print(n_rep, n_cs)

# get a number of distinct nodes
nodes_cnt = len(map_num2cs)

# create graph
graph = Graph(nodes_cnt)
for u,v in edges:
    graph.add_edge(v, u)

# get id of node to check
n_src = get_cs_idx(node2check)

# run BFS and print result
print("{:.2f}".format(graph.BFS(n_src)*100))
```


### File: CTFs/GRUCon2021/ssh4/README.md

# Whisper 4

![text](img/desc.png)

## Input files:

* [wsprspots.csv](input/wsprspots.csv )

## Solution:

Input file containes data in [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format:

```
Reporter,Distance,Call Sign,Reporter's Grid,Grid
KA7OEI-1,2955,1Z2CPJ,DN31uo,FN25dj
DB9OH,816,2E0SXX,JO52ji,IO91
DC1RDB,945,2E0SXX,JN58ss,IO91
DJ4FF,886,2E0SXX,JN47vq,IO91
...
```
PS: first line is column's names!

Based on the BFS as in the previous task.

Some notes:
* I used BFS for nodes conenctivity checking
* BFS run only once due - during this run we calculate minimal distance to every reachable node. If node is not reachable distance is left 0 and correspindent value in V is False. Distance counts both source and destination nodes.
* at the end of BFS method I just count avg disatnces excluding myself 
* before BFS I converted all nodes names (i.e. call signs) to numbers. It will simplifies arrays usage + increase total perfomance.




```python
#!/usr/bin/env python3

import os, sys
from collections import Counter
from types import DynamicClassAttribute
from collections import *
from itertools import *
#from pyhamtools import LookupLib, Callinfo


# For the file in Whisper 1, what percent of the other nodes are unreachable 
# regardless of hop count from "F5MAF"? 
# Assume any node that is visible to a reporter may be reached by the reporter. Round to two decimal places.

node2check = "IZ7BOJ"

# vertices have nums 0..N-1
class Graph(object):
    def __init__(self,n):
        self.VN=n
        self.G = [[] for _ in range(n)]
        # BFS
        self.V  = None # visited
        self.D  = None # min distance
        self.PR = None # parent


    def add_edge(self,x,y):
        self.G[x].append(y)
        #not directed:
        self.G[y].append(x)

    def BFS(self,root=0):
        N =self.VN
        P  = self.PR  = [None]*N
        D  = self.D   = [0]*N
        #PTH= self.PATH= [ [] for _ in range(N) ]

        G=self.G #no need to save G
        i=0
        v=root
        D[root]=1
        q=deque([root])
        while q:
            v=q.popleft()
            pv=P[v]
            dv=D[v]
            for w in G[v]:
                if w==pv: #not go back
                    continue
                if D[w]: 
                    continue #already visited and counted
                P[w]=v
                D[w]=dv+1
                q.append(w)

        print("reachable from root: {}".format( sum(map(lambda x: x>0, D))-1 )) # -1 to exclude myself
        print("farthest  distance : {}".format( max(D) ))

        
        # check avg path
        res = 0
        res_cnt = 0
        for i,d in enumerate(D):
            if d==0:
                continue
            if i==root:
                continue #not check myself
            assert(d>0)
            res += d  # hops includes source and dest
            res_cnt+=1

        return res/res_cnt


# vertices have nums 0..N-1
map_cs2num = dict()
map_num2cs = []
edges = set() 

# maps callsigns to numeric node ids
# nodes numbered 0..N-1 where N is a numberof distinct call signs
def get_cs_idx(cs):
    # try get numeric id of node
    n_cs =  map_cs2num.get(cs, None)
    if n_cs!=None:
        return n_cs #if found - return it
    #assign id to new node
    n_cs = len(map_cs2num)
    map_num2cs.append(cs)
    map_cs2num[cs]=n_cs
    return n_cs

# parse input file 
with open("../input/wsprspots.csv","rt") as f:
    lines=f.readlines()
    for l in lines[1:]:
        l=l.strip()
        reporter, sdistance, callsign, reporter_grid, grid = l.split(',')
        n_rep = get_cs_idx(reporter)
        n_cs  = get_cs_idx(callsign)
        edges.add( (n_rep, n_cs) )

# get a number of distinct nodes
nodes_cnt = len(map_num2cs)

graph = Graph(nodes_cnt)
for u,v in edges:
    graph.add_edge(v, u)

n_src = get_cs_idx(node2check)
print("{:.2f}".format(graph.BFS(n_src)))
```


### File: CTFs/GRUCon2021/surprise/README.md

# Surprise Signal 1

![text](img/desc.png)

## Input files:

* [hamcap.sigmf-data](input/hamcap.sigmf-data)
* [hamcap.sigmf-meta](input/hamcap.sigmf-meta)

## Solution:

If check meta file we will see that data coded "ci16_le" i.e. complex (signed) integer little endian

Due to in most cases better have the cf32/complex32 (i.e. complex float) enocded one I wrote simple Python [script](scripts/convert.py) basing on read/write [SigMF examples](https://github.com/gnuradio/SigMF).

As result I got cf32 **hamcap.raw** file which used later in GQRX

PS: the same ci16_le to cf32 conversion can be easily done using [SoX](http://sox.sourceforge.net/):
```
sox.exe -r 48000 -c2 -t s16 -L hamcap.sigmf-data -c2 -t f32 -L hamcap.raw
```


![g00](img/gqrx00.png)

### Part 1: *K6OF is operating in the Amateur Extra part of the band. What's his flag? This will lead you to Part1flag*

### Part 2: *What frequency is KM6YOU operating at in kHZ? This will lead you to Part2flag*

### Part 3: *What\'s KM6YOU\'s flag? This will lead you to Part3flag*

### part 4: *What azimuth is the antenna pointed? This will lead you to Part4flag*

It is the simplest - just check the meta file ( 97.1 )






### File: CTFs/GRUCon2021/task1/README.md

# Task 1

![text](img/desc.png)

## Input file:

[signal1.data](input/signal1.data)

## Solution:

The same as in 
[HWIO2021 CTS, Task 1](https://github.com/BlackVS/CTFs/blob/master/HWIO2021/CTS/task1.md)



### File: CTFs/GRUCon2021/task2/README.md

# Task 2

![text](img/desc.png)

## Input file:

[signal2.data](input/signal2.data)

## Solution:

The same as in 
[HWIO2021 CTS, Task 2](https://github.com/BlackVS/CTFs/blob/master/HWIO2021/CTS/task2.md)



### File: CTFs/GRUCon2021/task3/README.md

# Task 3

![text](img/desc.png)

## Input file:

[signal3.data](input/signal3.data)

## Solution:

The same as in 
[HWIO2021 CTS, Task 3](https://github.com/BlackVS/CTFs/blob/master/HWIO2021/CTS/task3.md):

[Script](scripts/task3.py)




### File: CTFs/GRUCon2021/task4/README.md

# Task 4

![text](img/desc.png)

## Input file:

[signal4.data](input/signal4.data)

## Solution:

1. Open in URH:
![00](img/img00.png)

2. Check waveform:
![01](img/img01.png)

3. Check spectrum. Looks like only 2 near frequencies i.e. 2FSK:
![02](img/img02.png)

4. Select modulation FSK and bit/symbol=1 and click autodetect:
![03](img/img03.png)

...and get decoded bitstream:

6. To decode bistream use we same [script](scripts/task4.py) as in task3.




### File: CTFs/GRUCon2021/task5/README.md

# Task 5

![text](img/desc.png)

## Input file:

[track.wav](input/track.wav)

## Solution:

The task same as in  

[HWIO2021 CTS, Task 5](https://github.com/BlackVS/CTFs/blob/master/HWIO2021/CTS/task5.md)

but write-up from link above contains few errors - DTMF part was not accuratly decoded (one wrong symbol) and one mistake is in decoded part3 %)) Just do more accuratly.




### File: CTFs/GRUCon2021/task6/README.md

# Task 6

![text](img/desc.png)

## Input file:

[capture_custom_RF.cfile](input/capture_custom_RF.cfile)

## Solution:

1. Open in URH, amplitude is constant:
![00](img/img00.png)

2. Frequencies - we have hopping between 3 distinct frequencies i.e. 3FSK
![00](img/img01.png)

3. Make FFT window minimal as possible - we see that at any moment only one of frequencies is used:
![00](img/img02.png)

4. Measure pulse ...:
![00](img/img03.png)

...and pause width:
![00](img/img04.png)

5. I decided convert signal to 012 sequence basing on the next considerations:
- each symbol is 400 samples length
- at the beginning of such 400 samples block we have "strobe" 100 samples width which defines the symbol - 0, 1, 2
- due to URH uses only power two FSK size i.e.2FSK, 4FSK etc I decided decode as 4FSK with "11" unused i.e. 00->0, 01->1, 10->2
- I set symbol width equal to 100 not 400. In such case 0->00000000, 1->01000000, 2->10000000

![00](img/img05.png)

![00](img/img06.png)

Demodulated bistream was saved to [bits.txt](scripts/bits.txt)

6. To convert bitstream from p.5 I wrote simple python [script](scripts/task6.py)

As result I got base 3 sequence [string](scripts/out.txt).

This string is 1 to 1 equal to source signal.

But what next?

Just some CyberChef [magic](https://gchq.github.io/CyberChef/#recipe=Fork('%5C%5Cn','%5C%5Cn',false)From_Base(3)From_Decimal('Line%20feed',false)Merge()Remove_whitespace(true,true,true,true,true,false)&input=MDEwMDEwCjAwMjIxMgowMDIxMTEKMDEwMDEwCjAwMjEyMQowMTExMjAKMDEwMDEyCjAwMTIxMAowMTExMDIKMDAxMjIwCjAxMDIwMQowMTAxMTIKMDEwMDAwCjAxMTEwMAowMDEyMjEKMDExMDAwCjAwMTAyMAowMTAyMTAKMDExMTExCjAxMDExMgowMTAyMjIKMDAxMDIwCjAxMTAwMAowMDEyMTAKMDEwMjExCjAxMDAwMQowMTAxMjEKMDAyMjEyCjAxMDExMgowMTEwMDIKMDExMTAwCjAwMjAwMQowMDIwMDEKMDAxMDIwCjAxMTAwMgowMDEyMjAKMDExMDIxCjAxMTAyMQowMTAxMTIKMDAxMjIwCjAxMDIxMAowMTAyMTAKMDAxMjIwCjAxMDIwMAowMTEwMjIKMDEwMjIwCjAxMTEwMQowMDEyMjAKMDEwMTEyCjAxMDIwMAowMDIyMjEKMDExMDAyCjAxMTAyMgowMTAyMDIKMDExMDAxCjAxMTAxMQowMDIwMDEKMDEwMTEyCjAxMDIxMgowMDEyMjEKMDExMDAyCjAxMDIwMQowMTAyMDAKMDExMTAwCjAxMDIxMAowMTAyMTAKMDEwMTEyCjAxMTAxMQowMTEwMDAKMDAxMjIxCjAxMTAyMgowMTExMTEKMDExMDExCjAxMTEwMAowMTAwMDIKMDEwMTEyCjAxMTAyMAowMDEyMjAKMDEwMjEwCjAxMTEwMAowMTEwMjIKMDEwMTIxCjAxMDEyMgowMTEwMDAKMDEwMjAyCjAxMDExMgowMTAyMDEKMDAyMTIwCjAxMTAxMQowMTExMDAKMDExMDIyCjAxMDIyMAowMTExMTIKMDEwMjAyCjAxMDExMgowMDIyMjIKMDExMDIwCjAwMTIyMAowMTEwMjIKMDExMTEyCjAwMTIyMAowMTEwMDAKMDEwMTEyCjAxMTAyMAowMDEyMjAKMDExMDIyCjAxMDIxMgowMDEwMjAKMDExMDAyCjAxMDIyMgowMTExMjI) %)



### File: CTFs/GRUCon2021/task7/README.md

# Task 7

![text](img/desc.png)

## Input file:

[capture.pcapng](input/capture.pcapng)

## Solution:

The task the same same as in 
[HWIO2021 CTS, Task 7](https://github.com/BlackVS/CTFs/blob/master/HWIO2021/CTS/task7.md)

I was right in general solution approach and some assumptions made at the end of mentioned write-up but


## 1. USB data parsing

Just to extract using:
```bash
"C:\Program Files\Wireshark\tshark.exe" -r data.pcapng -T fields -e usb.capdata -Y usb.capdata > capdata.raw
```
was not correct way.

If look more carefully to packets flow we will see that each write operation consist of 2 steps:

![shark0](img/wshark00.png)

- send address to be written to (LBA - Logical Bloak Address)
- send data

Filter only this packets and check them

![shark0](img/wshark01.png)

We see that packets not written sequentially - sometimes other blocka written and it is normal due to it is USB drive which is random access device.

To extract data more accuratly we need check LBA addresses and sort written data in LBA order.

I.e. to extract raw USB data I did:

1. Filter specific packets (image above)
2. Exported them to the old fromat .pcap (I didn't exported to .pcapng due to need only raw packets processing in my Python script
3. Extracted ordered raw data using my Python [script](sricpts/parse.py):
```python
#!/usr/bin/python
import binascii
import dpkt
import struct
import sys

# Start the pcap file parsing
f = open("usbtraffic.pcap", 'rb')
pcap = dpkt.pcap.Reader(f)
#print(pcap)
lba = 0
packets = []
for ts, buf in pcap:
    #print(ts)
    if buf[64:68] == b'USBC':
        #lba = int( buf[], 16)
        a = buf[0x51:0x55]
        lba = int.from_bytes(a, 'big')
        b = buf[0x56:0x58]
        blen = int.from_bytes(b, 'big')
        print(hex(lba))
    else:
        packets.append(  (lba, blen, ts, buf[64:] ) )

packets.sort()
with open("usbtraffic.raw","wb+") as f:
    for lba, blen, ts, b in packets:
        print("Writing lba={} len={} ts={}".format(lba, blen, ts))
        f.write(b)
```

Offsets like "0x51:0x55" I got inspecting packets in Wireshark

4. Now we have **usbtraffic.raw** file which I analyzed using binwalk with -e option.
Surprise - extracted data much larger comparing to the extrected in my write-p from HWIO2021 %)


## 2. Demodulating

Basing on [gr-gsm](https://github.com/ptrkrysik/gr-gsm))

My suggestion in [HWIO2021 CTS, Task 7](https://github.com/BlackVS/CTFs/blob/master/HWIO2021/CTS/task7.md) was correct - it is GSM signal.

But why grgsm_decode decoded nothing?

Reson is quite ... silly? Thanks to Don (flamewires team) who pushed me in right direction.

Opening signal using gr-gsm livemon graph ( https://github.com/ptrkrysik/gr-gsm/tree/master/apps, sure replacing input block to File Source - like [here](rgc/grgsm_livemon_file_orig.grc) ) we will see:

![livemon00](img/grc_fft_orig.png)

and now decoded data seen:

![decoded00](img/grc_decoded_orig.png)

If check original [livemon graph](https://github.com/ptrkrysik/gr-gsm/blob/master/apps/grgsm_livemon.grc) more carefully we will see Rotator block which shifts spectre left:
```
-2*pi*shiftoff/samp_rate
```
Just removing this block (or making it zero) not helps

![livemon00](img/grc_fft_shift_0.png)

but making it opposite sign i.e.:

```
+2*pi*shiftoff/samp_rate
```
(or the same as make shiftoff=+400e3):

![livemon00](img/grc_fft_shift_oppo.png)

looks like give us some signal in the middle and

![decoded00](img/grc_decoded_rotated.png)

we see decoded data!!!!

Next what I did - wrote shifted signal to file (adding File Sink in file):

[2file](grc/grgsm_livemon_2file.grc)

Saved file named *telesignal_1msps_rotated.complex32* and later worked with it.

## 3. Decode

Next I did basing on [GSM:Sniffing SMS traffic](https://www.ckn.io/blog/2015/11/29/
gsm-sniffing-sms-traffic/)


Run Wireshak to listen local loppback and filter only gsmtap:

```bash
sudo wireshark -k -Y gsmtap -i lo
```

![wr00](img/wr_00.png)


Next decode BCCH:

```bash
grgsm_decode -a 34 -c telesignal_1msps_rotated.complex32 -t 0 -m BCCH
```

We will decoded packets (like we saw in GNU Radio before but here they are parsed):

![wr00](img/wr_01.png)

... and I stuck here %) during CTF.

Thanks to ElyKar for sharing it's [writeup](https://blog.tclaverie.eu/posts/grcon-2021---capture-the-signal/#s7p2):

Normally, Wireshark should display GSM packets now. We can see some have been correctly decoded, like "System Information" or "Paging Request".

There is one packet of type "Immediate Assignment", which indicates an equipment is connecting to the network.

![wr00](img/wr_02.png)

In this packet, we need the channel description :

- Timeslot (it is 0)
- SDCCH4

![wr00](img/wr_03.png)

Now, we can decode the control channel of the connection : 
```
grgsm_decode -a 34 -c telesignal_1msps_rotated.complex32 -t 0 -m BCCH_SDCCH4 -v -p
```

We see new packets in Wireshark. In particular, the "Paging Response" indicates that there is no encryption key available, meaning that the data sent won't be encrypted.

![wr00](img/wr_04.png)

Finally, we can see a decoded SMS packet which was not encrypted. We can read the content of the SMS:

![wr00](img/wr_05.png)




### File: CTFs/GRUCon2021/task8/README.md

# Task 8

![text](img/desc.png)

## Input file:

[signal8.iqdata](input/signal8.iqdata)

## Solution:

As base I used Drake's Signal 5 [write-up](https://batchdrake.github.io/ctsII/).

First I tried solve it using URH:

![sig00](img/sig00.png)

![sig01](img/sig01.png)

![sig02](img/sig02.png)

![sig03](img/sig03.png)

![sig04](img/sig04.png)


and try decode demodulated bitstream (4FSK) but failed.

Finally I switched to SigDigger due to it allow more accurate timespace operations:

![sd00](img/sd00.png)

![sd01](img/sd01.png)

![sd02](img/sd02.png)

![sd03](img/sd03.png)

![sd04](img/sd04.png)

![sd05](img/sd05.png)

![sd06](img/sd06.png)

Demodulated data were decoded using [C++ programm](script/check1.cpp).






### File: CTFs/GRUCon2021/task9/README.md

# Task 9

![text](img/desc.png)

I didn't solve it - but we have [writeup](https://blog.tclaverie.eu/posts/grcon-2021---capture-the-signal/#sig9) by ElyKar %) - thanks for sharing it!



### File: CTFs/HWIO2021/BHV/README.md

# HWIO2021

# Hardwear.io Security Trainings and Conference, USA 2021

![Logo](img/ctf_top.png)
[Home](https://hardwear.io/usa-2021/)

 Date : 5th - 10th July 2021

[CTFs Home page](https://hardwear.io/usa-2021/ctf.php)

My writeups and some useful info:

## CTF
 - [CTS](CTS/README.md)
 - [BHV](BHV/README.md)



### File: CTFs/HWIO2021/CTS/README.md

# Capture the Signal, HWIO2021


[CTFs Home page](https://hardwear.io/usa-2021/ctf.php)

[Official info](DESC.md)

## Useful info
 - [Installing tools](cts-tools.md)
 - [Receiving signal](cts-get-signal.md)
 - [How to run local server](cts-utils.md)
 - [How signals are sent from server?](cts-signals.md)


Info: for all tasks I recorded signals during CTF.
For each task there is "input" folder with "signalX.raw" recorded signal and "tx_file.grc/tx_file.py" graph/script.
To replay recorded signal localy just run
```
./tx_file.py
```

## Tasks
 - [Task1](task1.md)
 - [Task2](task2.md)
 - [Task3](task3.md)
 - [Task4](task4.md)
 - [Task5](task5.md)
 - [Task6](task6.md)
 - [Task7](task7.md)



### File: CTFs/HWIO2021/README.md

# HWIO2021

# Hardwear.io Security Trainings and Conference, USA 2021

![Logo](img/ctf_top.png)
[Home](https://hardwear.io/usa-2021/)

 Date : 5th - 10th July 2021

[CTFs Home page](https://hardwear.io/usa-2021/ctf.php)

My writeups and some useful info:

## CTF
 - [CTS](CTS/README.md)
 - [BHV](BHV/README.md)



### File: CTFs/NNC2019/Extra/1. Firmware builder/README.md

# Badge Firmware builder

ESP32 allows both [secure boot and flash encryption](https://docs.espressif.com/projects/esp-idf/en/latest/security/secure-boot.html#secure-boot-and-flash-encr) but NoNameBadge uses only the first one - i.e. unencrypted but signed flash image. 

The structure of image is quite simple - https://github.com/espressif/esptool/wiki/Firmware-Image-Format

I.e. actually we have two levels of protection:

- simple, checksum (is defined as the xor-sum of all bytes and the byte 0xEF)
- complex, signing

After solving **Ployka PWNer** you already have needed private key for signing %)
Here is few simple scripts for reassembling badge image and signing it.

## 1. Image disassembly

Image can be patched inplace and re-signed but it is more convinient to extract all segments, open and patch needed segment using some tools (I used radare2) and assemble, sign.
I made *nnc_assemble.py* Python 3 script to do this job (check *Extra\1. Firmware builder\\scripts\\* folder ).
To use it you need *Python3* and *argparse*, *esptool* modules installed:

```bash
pip install argparse
pip install esptool
```

To disaasemble (not to be confused with dissassembling using disassembler):

```bash
nnc_disassemble.py nn-badge195.bin 
```

As result a set of files nn-badge195.bin.* will be produced:
*nn-badge195.bin.info* - human-friendly file info, also printed on console;
*nn-badge195.bin.map* - file map, similar to file info but in compact, machine-friendly form (used by *nnc_assemble.py* script) );
We same info can be get via

```bash
esptool.py --chip esp32 image_info nn-badge195.bin
```

*nn-badge195.bin.segN* - raw dump of each segment (in our case it consists of 6 segments).
I.e. running 

```bash
nnc_disassemble.py nn-badge195.bin 
```

you should see something similar to:
```bash
Image version: 1
Entry point: 40080ffc
secure_pad: False
flash_mode: 2
flash_size_freq: 32
6 segments

Segment 1: len 0x2bcb0 load 0x3f400020 file_offs 0x00000018
  addr=0x3f400020 file_offs=0x18 include_in_checksum=True

Segment 2: len 0x03614 load 0x3ffbdb60 file_offs 0x0002bcd0
  addr=0x3ffbdb60 file_offs=0x2bcd0 include_in_checksum=True

Segment 3: len 0x00400 load 0x40080000 file_offs 0x0002f2ec
  addr=0x40080000 file_offs=0x2f2ec include_in_checksum=True

Segment 4: len 0x00914 load 0x40080400 file_offs 0x0002f6f4
  addr=0x40080400 file_offs=0x2f6f4 include_in_checksum=True

Segment 5: len 0xd1f18 load 0x400d0018 file_offs 0x00030010
  addr=0x400d0018 file_offs=0x30010 include_in_checksum=True

Segment 6: len 0x15b64 load 0x40080d14 file_offs 0x00101f30
  addr=0x40080d14 file_offs=0x101f30 include_in_checksum=True

Checksum: 33 (valid)
Validation Hash: 94f0a1f483bf3b0db3ec20f26bf4f7dab910487b228b6d4885bfdf79562074f5 (valid)
END
```

and map file should look like (if you analyze 1.95 image file):

```bash
0x40080ffc
6
False 2 32 
1 nn-badge195.bin.seg1 0x3f400020 0x18 True
2 nn-badge195.bin.seg2 0x3ffbdb60 0x2bcd0 True
3 nn-badge195.bin.seg3 0x40080000 0x2f2ec True
4 nn-badge195.bin.seg4 0x40080400 0x2f6f4 True
5 nn-badge195.bin.seg5 0x400d0018 0x30010 True
6 nn-badge195.bin.seg6 0x40080d14 0x101f30 True
```

Some useful information can be seen in debug info during badge reboot:

```bash
I (63) boot:  0 nvs              WiFi data        01 02 00009000 00004000
I (70) boot:  1 otadata          OTA data         01 00 0000d000 00002000
I (78) boot:  2 phy_init         RF data          01 01 0000f000 00001000
I (85) boot:  3 ota_0            OTA app          00 10 00010000 00180000
I (93) boot:  4 ota_1            OTA app          00 11 00190000 00180000
I (100) boot:  5 nvs_key          NVS keys         01 04 00310000 00001000
```

Our firmware image is ... ota_1. Why? ota_0 - is factory image. I.e. it is badge life preserver if custom image (ota_1) is broken %)
You can read in details about boot process [here](https://docs.espressif.com/projects/esp-idf/en/latest/api-guides/bootloader.html)

## 2. Patching

To get all flags we need patch badge code. 
After *Binary Hero* task we already know - we have to patch *nn-badge195.bin.seg5* (flag generating function are in this segment address space).
To do this you may load it to *radare2* mapping to address *0x400d0018* and patch (but as it will be shown in the second article it is not so easy task as could be expected)

## 3. Assemble image

I patched in-place without changing segments sizes.
It allows assemble all segments very easy using the same map file *nn-badge195.bin.map*:

```bash
nnc_assemble.py nn-badge195.bin.map nn-test.bin
```

If you change segments sizes you need update accordingly map file.

## 4. Signing

```bash
espsecure.py sign_data -k private.pem nn-test.bin
```

output is:
```bash
espsecure.py v2.6
Signed 1145536 bytes of data from nn-test.bin with key private.pem
```
## 5. Verifying

```bash
espsecure.py verify_signature -k public.key nn-test.bin
```
->
```bash
espsecure.py v2.6
Verifying 1145536 bytes of data
Signature is valid
```
**Signature must be valid!**

and check image info of patched file:

```bash
esptool.py --chip esp32 image_info nn-test.bin
```
->
```bash
esptool.py v2.6
Image version: 1
Entry point: 40080ffc
6 segments
Segment 1: len 0x2bcb0 load 0x3f400020 file_offs 0x00000018
Segment 2: len 0x03614 load 0x3ffbdb60 file_offs 0x0002bcd0
Segment 3: len 0x00400 load 0x40080000 file_offs 0x0002f2ec
Segment 4: len 0x00914 load 0x40080400 file_offs 0x0002f6f4
Segment 5: len 0xd1f18 load 0x400d0018 file_offs 0x00030010
Segment 6: len 0x15b64 load 0x40080d14 file_offs 0x00101f30
Checksum: 33 (valid)
Validation Hash: 94f0a1f483bf3b0db3ec20f26bf4f7dab910487b228b6d4885bfdf79562074f5 (valid)
```

**You must have both checksum and validation hash valid!!!**

## 6. Flashing

```bash
esptool.py -p com4 -c esp32 write_flash 0x190000 nn-test.bin
```
(you may have different from my com port).

As you see we flashing *ota_1* .


## Useful links

* https://www.espressif.com/en/support/download/documents
* https://docs.espressif.com/projects/esp-idf/en/latest/security/secure-boot.html
* https://github.com/espressif/esptool/wiki/Firmware-Image-Format
* https://docs.espressif.com/projects/esp-idf/en/latest/api-guides/partition-tables.html
* https://github.com/espressif/esptool
* http://cholla.mmto.org/esp8266/xtensa.html
* https://medium.com/@tomac/turning-a-10-esp32-into-a-hacker-arsenals-winx-portable-clone-46c37c1508cd
 
## Useful commands

```bash
esptool.py --chip esp32 --port com4 chip_id
esptool.py --chip esp32 --port com4 read_flash 0x9000 0x4000 nvs.flash
esptool.py --chip esp32 --port com4 read_flash 0x190000 0x00180000 ota1.flash
```



### File: CTFs/NNC2019/Extra/2. Patching/README.md

# Badge Firmware patching

## Part 1: [analyzing](part1.md)

## Part 2: [patching](part2.md)



### File: CTFs/NNC2019/Extra/3. MITM/README.md

# MITM 

To successfully implement MITM attack we have to:

* route/intercept traffic from/to badge;
* somehow deal with built-in CA certificates check;
* seamlessly decode SSL/TLS traffic using our self-signed certificate.

## Part 1: [route traffic from badge](part1/README.md)
This task is quite easy due to we have full physical access to device and able to edit it's firmware.

## Part 2: [certificates](part2/README.md)
Here is we have to modify firmware in such way that badge is able to communicate with target Techmaker accepting non Techmamer's CA certificates.




### File: CTFs/NNC2019/Extra/3. MITM/part1/README.md

# Route/intercept traffic from/to badge

To implement MITM attack we must first to intercept traffic to/from badge.

## Hotspot (Kali)
Due to badge can connect to any (or about any %) Wi-Fi hotspot using DHCP client - just create custom hotspot.

Standart Kali image uses Network Manager to manage network.

If you switch Wi-Fi to Hotspot mode it will create hotspot with:

* SSID equal to hostname (kali1 in my case)
* WPA2 
* password - randomly generated

If you wish change some parameters you may modify them via (in console):

```bash
nmtui
```
or

```bash
nm-connection-editor
```

For example, I changed password to test1234:

![alt text](img/02.png "")

![alt text](img/03.png "")

switched Hotspot on:

![alt text](img/04.png "")

joined badge to this hotspot:

![alt text](img/05.png "")

and... got:

![alt text](img/06.png "")
 

Google said that it seems to be badge not able use chosen in Kali by default security settings.

Let's relax them.

All connections properties stored in */etc/NetworkManager/system-connections/* folder. Let edit connection started with "*Hotspot*" - in my case "Hotspot.nmconnection":

![alt text](img/07.png "")

and change security settings to:

```
[wifi-security]
group=ccmp;tkip;
key-mgmt=wpa-psk
pairwise=ccmp;tkip;
proto=wpa;
psk=test1234
```

![alt text](img/08.png "")


After run in console (or Network Manager will rewrite your changes):

```
nmcli conn reload
```

and restart your Hotspot.

As only badge reconnected to your hotspot your will see:

![alt text](img/09.png "")

Next we have to get all needed information for next steps:

![alt text](img/10.png "")

![alt text](img/11.png "")

![alt text](img/12.png "")


For Kali
* WiFi interfaces and ip (**wlan0** : 10.42.0.1/24). All traffic to/from badge comnes through this interface.
* interface with access to Internet (**eth0** : 192.168.6.200/24, Internet gateway/DNS server is 192.168.6.1/24)
* forwarding is enabled i.e. Kali acts as router
* all forwarded traffic to/from wlan0 is masquaraded (not the best solution for us but it was done by Network Manager by default). For Kali-as-router better solution would be to masquarade forwarded to *eth0* traffic.
* Kali acts as DNS proxy/DHCP server for wlan0

For badge:
* MAC and ip address: 3c:71:bf:9d:5e:a0, 10.42.0.22/24
* DNS request sent to Kali


## Kali (hotspot based on hostapd+dnsmasq)

https://cybergibbons.com/security-2/quick-and-easy-fake-wifi-access-point-in-kali/

https://nims11.wordpress.com/2012/04/27/hostapd-the-linux-way-to-create-virtual-wifi-access-point/comment-page-5/

https://github.com/BASH-Auto-Tools/wifi-host-ap-bash

## External AP with gateway for badge set (via DHCP) to ip of Kali 
How to do this depends on contrete AP you use.

## Arp spoofing 
Can be usefull (and one of possible ways) when you haven't physical access to badge.

But be carefull - arp spoofing may infect arp tables not only of desired targets but any devices which receive infected arp traffic (i.e. for example have network cards in promiscoius 
mode).

https://www.valbrux.it/blog/2017/11/26/mitm-using-arpspoof-burp-or-mitmproxy-on-kali-linux/

## Intercepting traffic (the first try)

First redirect https traffic to other port (where MITM proxy is hosted):

```bash
iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 8080
```

### mitmproxy

```bash
mitmproxy --mode transparent -p 8080
```
and ...

![alt text](img/13.png "")

![alt text](img/14.png "")


in CA we don't trust ... 
yep.
Badge has build-in check for remote CA certificate - we must somehow to deal with this stuff %)


### File: CTFs/NNC2019/Extra/3. MITM/part2/README.md

# 3. CA stuff

## 3.1. Changing built-in in firmware CA certificate

It is easy to see that badge firmware has built-in certificate - 

![alt text](img/01.png "")

![alt text](img/02.png "")

Certificate in PEM (i.e. base64) format - it is important!

For convinience I extracted it to *.\Extra\3. MITM\part2\scripts\1. CA substitution"\badge_cert_ca.cer* and check using standard Windows tools:

![alt text](img/04.png "")

![alt text](img/05.png "")

![alt text](img/06.png "")

Or using *certutil* :

![alt text](img/08.png "")

I.e. it is full-chain CA certificate to verify remote server.

Let's try substitute it by our one.

I will use Burp Suite here for MITM.

What we have to do:

* export CA certificate from Burp Suit (don't use my - it is different for different Burp Suits installations!)
* convert it in proper format
* insert it in firmware image
* flash
* enjoy

### Getting CA from Burp Suite

![alt text](img/09.png "")

![alt text](img/10.png "")

![alt text](img/11.png "")

Certificate in DER (i.e. raw ASN format):

![alt text](img/12.png "")

We need convert it to PEM.

To convert it to PEM in Windows:

```bash
certutil -encode kali1_burp_ca.der kali1_burp_ca.pem
```

or in Linux:

```bash
openssl x509 -inform der -in kali1_burp_ca.der -out kali1_burp_ca.pem
```

Check :

![alt text](img/13.png "")

![alt text](img/14.png "")

Important - certificate ends with 0x0a symbol. We need add 0x00 byte to the end due to formware uses C-style strings.

To do this just type in Linux (or use any other tool like Hiew, FlexHex, WinHex in Windows):

```bash
truncate -s +1 kali1_burp_ca.pem
```
i.e. we are "truncating" file on -1 bytes i.e. adding 1 zero-byte %)

![alt text](img/15.png "")

Good.

Now we are ready to replace original CA certificate with our us.

To do this first disassemble image:

```bash
nnc_disassemble.py nn-badge.bin
```

And check all segments for original CA certificate - it is in *nn-badge.bin.seg1* :

![alt text](img/03_0.png "")

![alt text](img/03_1.png "")

CA starts from 0x2f22 offset and ends in 0x431e. Length of certificate is 0x13fd (5117) bytes including final zero-byte (that why we added zero to our certificate).

Our certificate much shorter - in my case 0x560 (1376) bytes i.e. we may just put it inplace of old:

```bash
cp nn-badge.bin.seg1 nn-badge.bin.seg1.orig
dd bs=1 seek=$((0x2f22)) conv=notrunc if=kali1_burp_ca.pem of=nn-badge.bin.seg1
```

(or use any other hex tool to do this).

![alt text](img/16.png "")

Compare original and patched files:

![alt text](img/17.png "")

Looks good.

Assemble patched image:
```bash
nnc_assemble.py nn-badge.bin.map nn-badge-patched.bin
```

Sign it:
```bash
espsecure.py sign_data -k private.pem nn-badge-patched.bin
```

Verify:
```bash
espsecure.py verify_signature -k public.key nn-badge-patched.bin
```

Flash:
```bash
esptool.py -p com4 -c esp32 write_flash 0x190000 nn-badge-patched.bin
```

![alt text](img/19.png "")

Connect to badge and .. it alive!!! :

![alt text](img/20.png "")

and able coonect to remote site %) :

![alt text](img/21.png "")

and we able to inspect secure traffic:

![alt text](img/22.png "")


## 3.2. Disabling CA cert check (4 bytes decision %)

## Check [4-bytes solution](README_0x4.md)


### File: CTFs/NNC2019/Extra/3. MITM/part3/README.md

# MITM implementation

## mitmproxy (simplest)

## burp suite

## OWASP ZAP

## modlishka?



### File: CTFs/NNC2019/Extra/README.md

# NoNameBadge 2019 CTF, Extra

Some more stuff regarding NonameBadge %)

## Firmare re-builder

 How to patch badge firmware
 
 [Re-builder](1. Firmware builder/README.md)

## Get all flags at once

 Patch firmware to generate all flags
 
 [Patching](2. Patching/README.md)

## MITM
 
 How replace built-in certificate or totally disable remote server identity check to make MITM attack possible
 
 [MITM](3. MITM/README.md)




### File: CTFs/NNC2019/README.md

# NoNameBadge 2019 CTF

[NoNameBadge Instruction page](https://2019.nonamecon.org/badge)

# Contents

## Rooting

[Take a closer look at NoNameBadge Trailer](https://www.youtube.com/watch?v=chfoAWevHMs)

## Tasks

 - [Mr Bean Walker](Mr%20Bean%20Walker/blackvs.md)
 - [BruteSearcher](BruteSearcher/blackvs.md)
 - [NoNameCon SpyNet](NoNameCon%20SpyNet/blackvs.md)
 - [Ployka PWNer](Ployka%20PWNer/blackvs.md)
 - [Binary Hero](Binary%20Hero/blackvs.md)
 - [Side Blennel](Side%20Blennel/blackvs.md)



### File: CTFs/README.md

# CTFs

Here is some my write-ups

## NoNameCon 2019 CTF (NNCBadge2019)
- [Official info](https://2019.nonamecon.org/badge)
- [My write-ups](NNC2019/README.md)


## NoNameCon 2020 CTF (NNCBadge2020)
- [My write-ups](https://gitlab.com/coders-in-ua/nonamebadge-2020-ctf)

## r2con2020 2020 CTF
 - [Write-ups](r2con2020/README.md)

## HWIO2021 CTFs
 - [CTS - capture the Signal](HWIO2021/CTS/README.md)

## GRUCon2021
 - [CTS - capture the Signal](GRUCon2021/README.md)



### File: CTFs/r2con2020/README.md

# r2con2020 CTF

[Scoreboard](https://ctf.radare.org/scoreboard)

![4th place](img/scoreboard.png)

# Tasks

 - [eXit, easy, 50](tasks/exit/README.md)
 - [Hellcode, easy, 50](tasks/hellcode/README.md)
 - [Defuse, easy, 50](tasks/defuse/README.md)
 - [aesthetic, medium, 200](tasks/aesthetic/README.md)
 - [Radare License Checker, medium, 182](tasks/license/README.md)



### File: CTFs/r2con2020/tasks/aesthetic/README.md

# AESTHETIC

## recon

First open in radare2 or Cutter and check main:

![](img/main.png)

Let's go deeper, to aes_128_table_encrypt .. awful:

![](img/aes_128_table_encrypt.png)

Let's check exports...

![](img/exports.png)

and google for AES, SBox, TyiBoxes, TyiTables.
Very soon you will get these links:

https://en.wikipedia.org/wiki/Rijndael_S-box

https://github.com/Gr1zz/WhiteBoxAES

Now we know our opponent - WhiteBOX AES %) 


## analysis

Let's check found sources and... we are lucky!!! -> our program is about 100% is 

https://github.com/Gr1zz/WhiteBoxAES/blob/master/aes_table.c


Checking deeper I found that:

- the secret key is used to generate tables (https://github.com/Gr1zz/WhiteBoxAES/blob/master/genTables.cpp)
- tables after compiled with aes_table.c, original secret key not
- only way to recover the secret key is to recover it back from tables

### getting Tables

First we need get tables. 

TBoxes is part of binary (offset 0x86020). Good.

SBox - must be standart AES 128 (https://en.wikipedia.org/wiki/Rijndael_S-box) but I prefer to be 100% sure in this %)

![](img/tboxes-hex.png)

It seems to be not directly present in binary (but I was wrong %)

![](img/sbox-hex.png)

But used in **subBytes** function.

![](img/subbytes.png)

Run in debugger, set breakpoint at main (due to **subBytes** never called) and check memory.

I tried radare2 debug but got warning to not debug (anti-debug protection?) %) Switching to gdb led to success:

![](img/sbox-gdb.png)

Searching by hex in file I found that table also present in binary at offset 0x1b40.

No need to extract.

### breaking tables

Take closer look to https://github.com/Gr1zz/WhiteBoxAES/blob/master/genTables.cpp , especially to *computeTables* function.
After stripping all that not related to SBox, TBoxes we will get:

```C
void computeTables (u8 expandedKey[176])
{
... 
  // Compute tboxes and compose them at their output with Tyi tables
  for (int i = 0; i < 10; i++)
  {
    shiftRows (expandedKey + 16*i);

    for (int j = 0; j < 16; j++)
    {
...
      for (int x = 0; x < 256; x++)
      {
        u32 tmp = x;
      
        // Input mixing bijection
        if ((i > 0) && (i < 9)) { 
          tmp = vec2int(mb_8x8[i-1][j].invMat * int2vec(x, 8), 8);       
        }
        
        if ((i > 0) && (i < 9))
        {
          tmp = mixBijIn[i-1][j][tmp];
        }
        tmp = SBox[tmp ^ expandedKey[16 * i + j]];
        TBoxes[i][j][x] = tmp;

        if (i == 9)
        {
          TBoxes[i][j][x] ^= expandedKey[160 + j];
        }
        else
        {
          TyiBoxes[i][j][x] = TyiTables[j % 4][tmp];
        }
      }
    } 
  }
```

Still looks awful ? Let's consider only i==0 case:

```C
void computeTables (u8 expandedKey[176])
{
... 
  // Compute tboxes and compose them at their output with Tyi tables
  for (int i = 0; i < 10; i++)
  {
    shiftRows (expandedKey + 16*i);

    for (int j = 0; j < 16; j++)
    {
...
      for (int x = 0; x < 256; x++)
      {
        u32 tmp = x;
...      
        tmp = SBox[tmp ^ expandedKey[16 * i + j]];
        TBoxes[i][j][x] = tmp;
      }
    } 
  }
 ```

Awesome! Why?

```
TBoxes[0][j][x] = Sbox[x^expandedKey[j]]
```
i.e.

```
expandedKey[j]= SboxInv[ TBoxes[0][j][x] ] ^ x
```

Even simpler if take x==0:

```
expandedKey[j]= SboxInv[ TBoxes[0][j][0] ] 
```


## pwn

Let's code:
[script](scripts/solve.py)

PS: in first version of script I forgot about shiftRows which permutes bytes of initial secret key. 
I.e. to extract secret key from expanded key I had to make reverse permutation (**shiftab_rev** list).
x can be any value from 0 to 255 - result must be the same. If not - something wrong with tables %)





### File: CTFs/r2con2020/tasks/defuse/README.md

# Defuse

Open in Cutter:

![](img/defuse_main_asm.png)

Decompile it:

![](img/defuse_main_dec.png) 

Main points we see are:
- strange 20 numbers
- validation of input string len = must be also 20 (it is pure coincidence? I don't think...)
- together with size validation the other function is called. After I renamed it to islowerascii():

![](img/defuse_isalowerascii.png)

I.e. defuse sequence must be 20 chars string of lower ASCII.

Inside loop we see two things happenn:

- called some function (I renamed it to decode_char() later)

![](img/defuse_decode.png)

- result if compared with strange 20 numbers

![](img/defuse_validation.png)

Check decoding function in deep. It is very simple:
```
decoded = ( (input^0x28) + 0x15 ) & 0xf5
```
I wrote 0xf5 due to only last byte validated later.

Very interesting - bitwise AND causes that can be few variants of input which produces the same result.


Check validation:

```
bVar1 = (bool)(bVar1 & iVar2 == *(int32_t *)((int64_t)&var_60h + (int64_t)(var_6ch._4_4_ + -1) * 4));
```

or more compact

```
 decoded[i] == strangekey[20-1+i]
```
 where decoded[i] - decoded by decode_char() i-th input char.
 
 Also important - decoded input chars and strange_numbers copmared in reverse order %)
 
 
 Time to script:
 
```python
#!/usr/bin/env python3
import os,sys
from itertools import *
coded = [ 0x60, 0x70, 0x54, 0x51, 0x65, 0x70, 0x51, 0x60, 0x65, 0x54, 0x51, 0x60, 0x50, 0x54, 0x65, 0x60, 0x71, 0x54, 0x50, 0x60 ]

cand = ""
idx = 1
for i in range(20):
    res=""
    for c in range(97,123):
        if ((c^0x28)+0x15)&0xf5 == coded[i]:
            res+=chr(c)
    print("{:2}: {:4} {}".format(i,res, " ".join( map(lambda c: hex(ord(c)), res ) ) ))
    cand+=res[idx]
    idx ^= 1
print(cand)
```

run

```
 ./solve1.py 
 0: ce   0x63 0x65
 1: su   0x73 0x75
 2: aio  0x61 0x69 0x6f
 3: ln   0x6c 0x6e
 4: prxz 0x70 0x72 0x78 0x7a
 5: su   0x73 0x75
 6: ln   0x6c 0x6e
 7: ce   0x63 0x65
 8: prxz 0x70 0x72 0x78 0x7a
 9: aio  0x61 0x69 0x6f
10: ln   0x6c 0x6e
11: ce   0x63 0x65
12: km   0x6b 0x6d
13: aio  0x61 0x69 0x6f
14: prxz 0x70 0x72 0x78 0x7a
15: ce   0x63 0x65
16: tv   0x74 0x76
17: aio  0x61 0x69 0x6f
18: km   0x6b 0x6d
19: ce   0x63 0x65
The first good candidate is: esilrsncrancmarcvamc
Amount of variants is: 42467328
```

take the first good sequence and ... success???? :

![](img/defuse_solve1.png)

Trying found sequence as a flag and... fault!

What to do?

To check all 42467328 flags is unreal.
After checking task hint and looking to results above we can reduce varinats on 2x2x3x2 (flag started with "esil") but 1 769 472 variants are too much tooo...

Will try reduce variants:

All variants, worst way:

```python
#!/usr/bin/env python3
import os,sys
from itertools import *

for p in product( 'prxz', 'su', 'ln', 'ce', 'prxz', 'aio', 'ln', 'ce', 'km', 'aio', 'prxz', 'ce', 'tv', 'aio', 'km', 'ce' ):
    print("esil"+"".join(p))
```

But lets try found readble words inside.
Try prefix:

```python
#!/usr/bin/env python3
import os,sys
from itertools import *

for p in product( 'prxz', 'su', 'ln', 'ce', 'prxz', 'aio' ):
    print("esil"+"".join(p))
```

It seems only 'rule' good.

Try last 6:
```python
#!/usr/bin/env python3
import os,sys
from itertools import *
for p in product( 'prxz', 'ce', 'tv', 'aio', 'km', 'ce' ):
    print("esil"+"".join(p))
```

The best candidates are:

['take','time','tome']

```python
#!/usr/bin/env python3
import os,sys
from itertools import *
for p in product( ['rule'], , 'prxz', 'aio', 'ln', 'ce', 'km', 'aio', 'prxz', 'ce', ['take','time','tome']):
    print("esil"+"".join(p))
```

'tome' it seems to be wrong way, let's check only 'time':

```python
#!/usr/bin/env python3
import os,sys
from itertools import *
for p in product( ['rule'], 'prxz', 'aio', 'ln', 'ce', 'km', 'aio', 'prxz', 'ce', ['time']):
    print("esil"+"".join(p))
```

Checking output I mentioned very interesting 'more'. "More time"? Why not...

```python
#!/usr/bin/env python3
import os,sys
from itertools import *
for p in product( ['rule'], 'prxz', 'aio', 'ln', 'ce', ['more'], ['time']):
    print("esil"+"".join(p))
```

Just 48 variants - correct flag among them ^)
(I checked - it is true!)





### File: CTFs/r2con2020/tasks/exit/README.md

# eXit

## recon

I used both Cutter (for static analisys, on one display) and radare2 as debugger (to gather dynamic data, on second display).

First open in Cutter and decompiler:

![](img/main_dec.png)

First look gives obvious way:

- Move barrel
- Enter tunnel
- Read note
- Leave

but it is wrong way.

Investigating deeper I mentioned "strncat_14dd", which inside looks not like strncat %) :

![](img/strncat_dec.png)

Inside such pseudo-strncat I found strange pseudo-strlen (strlen_13a9)

![](img/strlen_dec.png)

Due to I'me too lazy to decode all stuff I switched to debugger

## debug time

Start debug session:

![](img/main.png)

Locate pseudo-strncat:

![](img/main_strncat.png)

Go inside pseudo-strncat:

![](img/strncat.png)

Locate psedo-strlen:

![](img/strlen.png)

Go inside pseudo-strlen and check passed arguments:

![](img/strlen_args.png)

Remeber that arguments passed via registers in order ( https://en.wikipedia.org/wiki/X86_calling_conventions ):
RDI, RSI, RDX, RCX, R8, R9 :

* rdi => Input string
* rsi => some_secret_key

Below in the 

```C
        if ((uint8_t)((*(uint8_t *)(param_1 + i) ^ *(uint8_t *)((int64_t)&var_60h + (int64_t)i)) +
                     *(char *)((int64_t)&var_40h + (int64_t)i)) != *(char *)(param_2 + i)) {
            uVar2 = 0;
            goto code_r0x000014a7;
        }
```
where:
- param_1=some_secret_key, 
- param_2=input text
- var_40 and var_60 - also some secret keys. Debugging and dumping memory I found that they are same for each check, only param_1 changed i.e. param_1 is coded answer, which can be decoded using var_40 and var_60


var_40 and var_60 I dumped from memory (sure I could decode them from set of *mov* operations at the beginning of pseudo-strlen but I'm too lazy, remember?)

I named them as d1 and d2 in the script.

Reversing C-code above I got final script:

```python
#!/usr/bin/env python3

import os, sys

d1=bytearray.fromhex("deadbeefdeadbeefcafe1337cafe13370102030405060708090a")
d2=bytearray.fromhex("0a09080706050403020137133713feca37133713fecaefbeadde")

def decode(rx):
    r=bytearray.fromhex(rx)
    res=""
    for i in range(len(r)):
        v = ( r[i] - d2[i])
        v = (v+0x100)%0x100
        #print("{:02x} - {:02x} = {:02x}".format(r[i], d2[i], v))
        v ^= d1[i]
        v = (v+0x100)%0x100
        #print("v ^ {:02x} = {:02x}".format(d1[i], v))
        res+=chr(v)
    print(res)


decode("97cdd2d6c0c7cd84ec91ad62f5f165225882b137613e5d2b144c")
decode("9ccde18eb092d791c09eb2")
decode("97e2e79d")
```

Last two *secret_code_key* strings were received just entering correct answer and catching param_1 on the next answer.




### File: CTFs/r2con2020/tasks/hellcode/README.md

# Hellcode

Open in Cutter, decompile and... yes I found flag:

![](img/binary0_dummy_key.png)

The flag is r2con{n0t_s0_easy} ... and not accepted...

Ok, try debug.. but odd *syscall 0x22* broke game:

![](img/binary0_main.png)

https://filippo.io/linux-syscall-table/
```
34	pause	sys_pause	kernel/signal.c
```

Ok, nopping all these *syscall 0x22*:

```
radiff2 binary0 binary0_patched 
0x00001004 48c7c0220000000f05 => 909090909090909090 0x00001004
0x0000105e 48c7c0220000000f05 => 909090909090909090 0x0000105e
0x00001073 48c7c0220000000f05 => 909090909090909090 0x00001073
0x0000108c 48c7c0220000000f05 => 909090909090909090 0x0000108c
0x000010b1 48c7c0220000000f05 => 909090909090909090 0x000010b1
0x000010bd 48c7c0220000000f05 => 909090909090909090 0x000010bd
0x000010cb 48c7c0220000000f05 => 909090909090909090 0x000010cb
0x00001166 48c7c0220000000f05 => 909090909090909090 0x00001166
```
(I patched directly in ... midnight commander - some habits are difficult to change).

Reopen patched binary and found this (or run debugger and trace until you see where input validated):

![](img/binary0_dummy_patched.png)

```
0x100000ba      80ea53                 sub     dl, 0x53 ; 83 ; dl=0xffffffffffffffad ; of=0x0 ; sf=0x1 ; zf=0x0 ; pf=0x0 ; cf=0x1
0x100000bd      90                     nop
0x100000be      90                     nop
0x100000bf      90                     nop
0x100000c0      90                     nop
0x100000c1      90                     nop
0x100000c2      90                     nop
0x100000c3      90                     nop
0x100000c4      90                     nop
0x100000c5      90                     nop
0x100000c6      4831c9                 xor     rcx, rcx ; rcx=0x0 ; zf=0x1 ; pf=0x1 ; sf=0x0 ; cf=0x0 ; of=0x0
0x100000c9      759c                   jne     trolololololololo ; unlikely
0x100000cb      90                     nop
0x100000cc      90                     nop
0x100000cd      90                     nop
0x100000ce      90                     nop
0x100000cf      90                     nop
0x100000d0      90                     nop
0x100000d1      90                     nop
0x100000d2      90                     nop
0x100000d3      90                     nop
0x100000d4      80faff                 cmp     dl, 0xff ; 255 ; zf=0x0 ; cf=0x1 ; pf=0x0 ; sf=0x1 ; of=0x0
0x100000d7      7558                   jne     error ; rip=0x10000131 -> 0x20646268 loc.error ; likely
```

I.e.
```
input-=0x53
if(input==0xff) SUCCESS
```
To get desired input just do reverse (don't forget about overflow!):
```
input = (0x53+0xff) % 256 = 0x52
```
or 'R'

Checking:

![](img/binary0_success.png)

Next we have two choices - manually re-do for each binary or... Sure **OR** - time for scripting:

```python
#!/usr/bin/env python3

import os, sys

base ="binary"

text = ""
for i in range(111):
    fname = "{}{}".format(base, i)
    with open(fname, "rb") as f:
        buf = f.read()
        a, b = buf[0x10bc], buf[0x10d6]
        if buf[0x10ba]==0x80 and buf[0x10bb]==0xea: #sub
            c = a+b
        else:
            assert(0)
        print("{:3}: {:02x} {:02x} = {:02x} {} ".format(i,a,b,c%256,chr(c%256)))
        text+=chr(c%256)
print(text)
```

I added **assert** to catch *different* binaries i.e. I suspected that game is not over %)
Getting assert I rechecked *different* binary and found other validation algorithm, added it to script and so on.

Final script is:

```python
#!/usr/bin/env python3

import os, sys

base ="binary"

text = ""
for i in range(111):
    fname = "{}{}".format(base, i)
    with open(fname, "rb") as f:
        buf = f.read()
        a, b = buf[0x10bc], buf[0x10d6]
        if buf[0x10ba]==0x80 and buf[0x10bb]==0xea: #sub
            c = a+b
        elif buf[0x10ba]==0x80 and buf[0x10bb]==0xf2: #xor
            c = a^b
        elif buf[0x10ba]==0x80 and buf[0x10bb]==0xc2: #add 
            c = b-a
        else:
            assert(0)
        print("{:3}: {:02x} {:02x} = {:02x} {} ".format(i,a,b,c%256,chr(c%256)))
        text+=chr(c%256)

print(text)
```



### File: CTFs/r2con2020/tasks/license/README.md

# Radare License Checker

## First run

![](img/first_run.png)

We need to know correct size first.

Open binary in Cutter to check.

## Get correct size

Locate incorrect size warning in the Strings:

![](img/err_wrong_size_1.png)

Go to the needed string:

![](img/err_wrong_size_2.png) 

Locate X-Ref to it:

![](img/err_wrong_size_3.png) 

Go back to conditional jump (strlen is hint):

![](img/strlen_0.png)

Correct size is 0x22 :

![](img/strlen_1.png)

The same by decompiling:

![](img/strlen_2.png)

## Second run

Try run with any 34-bytes key:

![](img/second_run.png)

Ok. Even more - we saw how much correct numbers at the start of tested key (zero in last case %)

## time to script

But first remember a delay during program run. It seems to be brute-force protection in it.

Remove it - it was very easy found by **sleep** call:

![](img/sleep.png)

I just NOP-ed it.

Script:

### 
```python
#!/usr/bin/env python

import os, sys
from py_execute.process_executor import execute
from mock import Mock

cmd = "radarelicensechecker_patched.exe "
key_pre = "r2con{"
key_sfx = "}"
key_mid = [' '] * (34 - len(key_pre) - len(key_sfx))

i=0
while i<len(key_mid):
    key = "\""+key_pre + "".join(key_mid) + key_sfx + "\""
    ret = execute(cmd+key, ui=Mock())
    msg = "ERROR: decryption error in block "
    if  msg not in ret[1]:
        print(key)
        break
    pos1 = ret[1].find(msg) + len(msg)
    pos2 = ret[1].find("!", pos1)
    blk = int( ret[1][pos1:pos2].strip())
    if blk == i+len(key_pre):
        key_mid[i] = chr( ord(key_mid[i]) + 1)
        if key_mid[i]=="\"":
            key_mid[i] = chr( ord(key_mid[i]) + 1)
    else:
        i+=1
        print(key)
        continue
```

Voila :

![](img/script.png)



### File: CTFs/HWIO2021/CTS/DESC.md

# Hardwear.io Security Trainings and Conference, USA 2021
## Capture the Signal, HWIO2021

## 10th Place 
UAteam

![0](img/cts_scoreboard.png)

![0](img/cts_schedule.png)
![0](img/cts_intro.png)
![0](img/cts_format.png)
![0](img/cts_prizes.png)




### File: CTFs/HWIO2021/CTS/cts-get-signal.md

# Receiving and recording signals

## Official way

As decsribed in [official docs](https://github.com/capturethesignal/cts-tools) to startreceiving your should do 2 things:

A) start piping data from input fifo to desired file (or somewhere else).
B) Run network streamer rx_to_fifo.py.

You have run these two command in difefrent terminal windows.

For example, if we have local signal source at 400Mhz:

terminal A

```bash
cat ~/cts.fifo > ~/cts.raw
```

terminal B
```bash
./rx_to_fifo.py --server-ip 127.0.0.1 --rx-frequency=400000000
```

and you will see:

![RX run](img/rx_start_0.png)

To stop recording push Ctrl-C:

![RX stop](img/rx_start_1.png)

As result cts.raw file will be created in home directory with written signal.

Also you will see symbol rate (here is one trick - symbol rate sent by server as tag value *rx_rate*)

If you just want to see if server alaive run
```
cat ~/cts.fifo | xxd -g 4 -c 8 -e
```
as A command:

![RX check](img/rx_start_2.png)


## VVS way %)

Due to I'm too lazy I modified rx_to_fifo and named it [rx_to_file](https://github.com/BlackVS/cts-tools.git). 
Sure it is Python 3 only but you can do the same for Python 2 cts tools easily too:

![RX to File](img/rx_to_file.png)

Differences - it writes directly to file (file is overwritten at start, official rx_to_fifo ), also GUI shown to chacke signal on-the-fly + printing tagged values if are in stream.

Usage the same as for rx_to_fifo but with no need to copy anything from cts.fifo (cts.fifo not crteated!).

I.e. just one command:

```bash
./rx_to_file.py --server-ip 127.0.0.1 --rx-frequency=400000000
```

![RX to File](img/rx_to_file_res.png)








### File: CTFs/HWIO2021/CTS/cts-signals.md

# Some theory

How signals are sent ?

Here is some trick.

Few constants are defined both on server and cleint side:
- server port base (10000 by default)
- bandwidth per port (1M by default)
- name of tag value for sample rate ('rx_rate')
In such case to "send" signal on 400M it will be sent via port:

= 10000 + ( 400M / 1M ) = 10400

and in sent stream periodically will be inserted tag value "rx_rate" with sample rate value (due to actually data sent via Internet with different from sample rate speed)


GNU Radio has special ZeroMQ blocks to deal with such streams.

But creators of official ctf-tools created special **RF Over IP Source** block which installed during make command.

rx_to_fifo uses this block - it is very simple if you wish create your own graphs - just check rx_to_fifo.grc graph.

Or if you wish use directly ZeroMQ blocks - check my rx_simple.grc / rx_file.grc ( https://github.com/BlackVS/cts-utils/ ) - I played with ZeroMQ a little to understand better it.




### File: CTFs/HWIO2021/CTS/cts-tools.md

# Tools

As written in official CTF info you need [CTS tools](https://github.com/capturethesignal/cts-tools) installed and tested prior CTF starts.

Here is one important note - cts tools build for GNU Radio 3.7 which Python 2 only.

But starting January 1st 2020 Python reached EoL and all as result GNU Radio 3.7 is the latest Python 2 built version, GNU Radio 3.8+ are Python 3 based.

Here are few options (really tehre are a lot of options but below are simplest ones):


## A. Install Ubuntu 18.04, GNU Radio 3.7, official cts-tools. 

Why Ubuntu 18.04? It is one of latest Ubuntu builds which have Python 2 as main + GNU Radio 3.7 can be easily installed from Ubuntu repositories.

To help in this way a Ubuntu 18.04 VMs with installed GNU radio can be downloaded from [downloads](https://cts.ninja/downloads/). VM password are given before CTF starts (I'm not sure if I can share it here %).
If you use these VMs then you can skip 1..4 steps

But if don't want wait for password you can just:

1. Install Ubuntu 18.04 ( [downloads](https://releases.ubuntu.com/18.04.5/ ) )

2. disable annoying annatended updates running:
    ```bash
        sudo dpkg-reconfigure unattended-upgrades
    ```
    and choosing "No". Why? Unnatented updates can block you to installing any software manually.

    Also I blocked software updates/upgrades from GUI - very important: Do No Update to later Ubuntu version!!!

    ![No updates](img/ubnt_no_updates_1.png)


3. Install GNU Radio:
    ```bash
    sudo apt update
    sudo apt install gnuradio
    ```

4. Install some other needed software:
    ```bash
    sudo apt install git
    sudo apt install make
    sudo apt install xterm
    ```

5. Install cts-tools (I installed them to home dir):
    ```bash
    cd ~
    git clone https://github.com/capturethesignal/cts-tools.git
    cd cts-tools/cts-cli
    make all
    ```
    You should see python files:

    ```
    epy_chdir.py
    epy_mkfifo.py
    epy_tags_to_vars.py
    rf_over_ip_source.py
    rx_test.py
    rx_to_fifo.py
    ```

6. Test - run GNU radio and open rx_test.grc, then execute it. You should see:
    ![rx_test](img/rx_test.png)

7. Install some other useful for CTS CTF software (on your choice - I installed all of them %) :
    ```bash
    sudo apt install inspectrum
    sudo apt-get install gqrx-sdr
    sudo apt-get install urh
    sudo snap install urh
    sudo apt install terminator
    ```


## B. Install Ubuntu 21.04, GNU Radio 3.8, non-official cts-tools and cts-utils

If you wish use latest GNU Rdaio or have already installed latest Ubuntu you can follow this way:

1..4 are the same as for Ubuntu 18.04 (sure you have install latest Ubuntu not 18.04 %)

5. Install cts-tools adapted by me to Python 3/GNU 3.8+ (I installed them to home dir):
    ```bash
    cd ~
    git clone https://github.com/BlackVS/cts-tools.git
    cd cts-tools/cts-cli
    make all
    ```
    You should see python files:

    ```
    epy_chdir.py
    epy_mkfifo.py
    epy_tags_to_vars.py
    rf_over_ip_source.py
    rx_to_fifo.py
    rx_to_file.py
    ```
    PS: rx_test.py will not be generated due to flow graph error. I did not manage it yet due to it is the first mye expirience with GNU Radio %) But you can open rx_test.grc from GNU Radio GUI and run/compile to Pyhton from GUI

6. Install cts-utils. It is few simple graphs/scripts to help with writeups:

    ```bash
    cd ~
    git clone https://github.com/BlackVS/cts-utils.git
    ```




### File: CTFs/HWIO2021/CTS/cts-utils.md

# CTS Utils

To play with CTF signals after CTF ended I created few simple graphs: 

https://github.com/BlackVS/cts-utils/


tx_simple.grc / tx_simple.py - just sends 1kHz 32 ksps at 400MHz on localhost
tx_file.grc / tx_file.py - just sends 1kHz 32 ksps at 400MHz on localhost

rx_simple / rx_file - just receives sent signal

I.e. if run tx_simple.py in one terminal and rx_simple.py in other you should see:

![Sample test](img/cts_utils_test.png)

Sure you see the same on both side (i.e. sent and received signals are the same)

For each task I will put corresponding graphs which sends recorded during CTF signals to allow play with them.

Or you can just use recorded signal %)




### File: CTFs/HWIO2021/CTS/task1.md

# Task 1

![text](img/cts_task1.png)

First we have to tune 454MHz and grab the signal (I reading recorded signal from 127.0.0.1, during real CTF use remote IP of server instead 127.0.0.1 ):

```bash
./rx_to_file.py --server-ip 127.0.0.1 --rx-frequency=454000000
```

![RX to File](img/task1_1.png)

Switching to waterfall we will something interesting:

![RX to File](img/task1_2.png)

Check in inpsectrum:

![RX to File](img/task1_inspectrum.png)

Check in GQRX:
```
file=/home/vvs/cts.raw,freq=454e6,rate=192000,repeat=true,throttle=true
```

![RX to File](img/task1_gqrx_1.png)

![RX to File](img/task1_gqrx_2.png)

Check in URH:

![RX to File](img/task1_urh.png)

**Welcome To HWIO2021 Listen@212MHz**

Let's go to 212MHz %)

[Task 2](task2.md)


### File: CTFs/HWIO2021/CTS/task2.md

# Task 2

![text](img/cts_task2.png)

From [Task 1](task1.md) we alredy know that need to listem @212MHz:

```bash
./rx_to_file.py --server-ip 127.0.0.1 --rx-frequency=212000000
```

Symbol rate reported is 48000

Signal looks like AM:

![AM](img/task2_rx2file.png)

Let's check in URH:

![AM](img/task2_urh.png)

and Gqrx:

```
file=~/cts.raw,freq=212e6,rate=48000,repeat=true,throttle=true
```

![AM](img/task2_gqrx_1.png)

![AM](img/task2_gqrx_2.png)

and ...
"Hello Radio Hackers Your next challenge is at 1.2GHz Sync Word a7"

PS: for me most difficult was recognize "word" - I heard something like "sync(bla-bla)7" %)) Thanks to David Szili for help %)) Also later CTF team helped people who couldn't recognize speech.

Let's go to 1.2GHz %)

[Task 3](task3.md)




### File: CTFs/HWIO2021/CTS/task3.md

# Task 3

![text](img/cts_task3.png)

Let's read signal:

```bash
./rx_to_file.py --server-ip 127.0.0.1 --rx-frequency=1200000000
```

![Read1](img/task3_rx2file_1.png)

![Read2](img/task3_rx2file_2.png)

Difficult to say.

Will check in URH:

![URH](img/task3_urh_1.png)

We see repeting of same (looks like) signal.

Let cut and check closer:

![URH](img/task3_urh_2.png)

Look's like OOK (on-off keying) signal, ASK autodetectiong in URH gives:

```10111010001100101001001000101010100010011101000110001001101010010111000110010001101000100011101001000011110100010110001010011010110010100111001000011001110100011000001111000001101010100001101010101010101011010011100000000```

Similar signal was in https://www.digital.security/en/blog/hardweario-capture-signal-write

Let's try script from there:

```python
#!/usr/bin/env python3

signal = "101110100011001010010010001010101000100111010001100010011010100101110001100100011010001000111010010000111101000101100010100110101100101001110010000110011101000110000011110000011010101000011010101010101010110100111"
for shift in range(8):
    bits=signal[shift:]
    shifted = [ int("".join(map(str,bits[i:i+8])),2) for i in range(0,len(bits),8)]
    temp="".join(map(chr,shifted))
    print(temp.encode())
```

"FREQ:15.24GHz,SYNC:0x5C"

PS: it is brute-forcing approach there we not used info "syncworda7" from previous task

0xA7 = 10100111

but actually data started after "10111" i.e. sync word is 0x17 or just 0x7 ? Or I did mistake (very probably) somethere

In any case go to the 15.24GHz %)

[Task 4](task4.md)







### File: CTFs/HWIO2021/CTS/task4.md

# Task 4

(0 solves)

![text](img/cts_task4.png)

Check the signal:

![Read](img/task4_rx2file.png)

Open in URH:

![Read](img/task4_1.png)

![Read](img/task4_2.png)

![Read](img/task4_3.png)

URH auto detect PSK and gives code:

```001111111111111111111111110111111000000000000111111110011101111011011001111111100110111111001111100011111110111001111011111110110001111111001111100111101111111101111011110110001110111111001110000111110001100111011001110011100111100011001110111110000110111000001110```

But I don't see sync word 0x5c = 01011100 (or 10100011) => in it.

Even more - 1's at least 2 in a row, 0's are 1,2,3 ...

I.e. looks like some additional coding but here my knowledge of coding is of %)

PS: spectre gives ideas that it could be something like GFSK or GMSK 
PPS: later from discord - **OQPSK** . Don't know that it means - need learn more, try harder %)

Go to [Task 5](task5.md)





### File: CTFs/HWIO2021/CTS/task5.md

# Task 5

![text](img/cts_task5.png)

Wav file given.

## Part 1. Morze
Listening it I recognized morze code at the beginning, later DTMF, and later some additional noise.

Decoding Morze (I cut part with Morze code, applied low-band filter and used online Morze decoder ), beginning was recognized good but final part looked broken.
I manually decoded last word and got:

```SOS-STEGHIDE-TOOL-F1N1CKY5HUT```

## Part 2. DTMF

Did the same, tried few also mobile phone, but best result got using http://dialabc.com/sound/detect/index.html

It gives 
```
05208407203506707206507803507008207907703507606907008403508308907806703505065
```

I look close we will saw that it is groups of 3 digits, looks like ASCCII codes:

https://www.dcode.fr/ascii-code

=>


```
DEC /3

4TH#CHAN#FROM#LEFT#SYNC#2A
```

## Part 3. Steg-hide
Hinf from part 1 says that it could steghide coded data with password "F1N1CKY5HUT"

```bash
>steghide --extract -sf track.wav -p F1N1CKY5HUT
wrote extracted data to "iq-data.cfile".
```

Opening in URH and checking spectre gives as clue taht there 6 channels of OOK coded data:

![Spectre](img/task5_part3_spectre.png)

We need "4th from left", it seems to be left is the toward 0 Hz %) i.e. counted from bottom in URH

I opened in URH, see ASK modulation, decoded, tried script from Task 3 and... nothing

At these point I stuck at CTF and switched to other tasks %)

My mistake was that I completely relied on autodetect URH engine.

It fails - URH detected 300 samples/symbol but later (after CTF) I found that correct value 350. I found this value by a lot of different tries, divisions etc %)

I.e. to get part 3:

- open "iq-data.cfile" in URH
- switch spectre view
- select needed band (4th from bottom i.e from left %)
- apply narrow band filter
- choose ASK
- apply noise level 
- autodetect (URH gave me 300 samples/bit)
- set 350 samples
- copy decoded bits to script from Task 3 and

![band4](img/task5_part3_band4.png)

![band4](img/task5_part3_bits.png)


```python
#!/usr/bin/env python3

signal =  "1111001001010011010010110011101110011011000010111011101010011011010010110010001101001011011100110011101010010011001010110011001101001011011000110110001010110011010010111001101100011011011110111001101101001011101000111100101000101010011110100011"

for shift in range(8):
    bits=signal[shift:]
    shifted = [ int("".join(map(str,bits[i:i+8])),2) for i in range(0,len(bits),8)]
    temp="".join(map(chr,shifted))
    print(temp.encode())
```


```
JigsawSidingRefillViscosityEO#
```

I.e. if connect all three parts together flag should be 

TMCTF{SOS-STEGHIDE-TOOL-F1N1CKY5HUT_4TH#CHAN#FROM#LEFT#SYNC#2A_JigsawSidingRefillViscosityEO#}


LATE PS: this flag has 2 mistakes - one mistype in DTMF recovered code and one char wrong in last part) 
But all process of restoring flag is correct - just do it more carefully than I did %)))
During GRUCon 2021 CTF I did it more carefully + used samples/symbol rate 360 in the last part.

[Task 6](task6.md)








### File: CTFs/HWIO2021/CTS/task6.md

# Task 6

(0 solves)

![text](img/cts_task6.png)

Read signal:

![Read](img/task6_rx2file.png)

Signal consists of two parts repeated one by one with big pauses:

![URH](img/task6_1.png)

I split them and analysed separetly.

Surprise:

![Part1](img/task6_2.png)

At the top the part from signal 6, at the bottom - signal from... task4 %)))

Part 2:

![Part1](img/task6_3.png)

![Part1](img/task6_4.png)

![Part1](img/task6_5.png)

At this point I stopped due to time over.

Current idea is:
* 1's are stop bits between symbols
* each symbol is the number of 0's between two consecutive 1's
* each such symbol corresponds to some char, for exampling adding some constant to get ASCII code

![Part1](img/task6_6.png)

[Task 7](task7.md)



### File: CTFs/HWIO2021/CTS/task7.md

# Task 7

![text](img/cts_task7.png)

Open given pcap file in Wireshark:

![1](img/task7_1.png)

Filter shorts packets:

![1](img/task7_2.png)

Checking few packets found interesting file signature %))

![1](img/task7_3.png)

After I switched to console and extracted data from interested packets:

```
"C:\Program Files\Wireshark\tshark.exe" -r data.pcapng -T fields -e usb.capdata -Y usb.capdata > capdata.raw
```

After I run binwalk on capdata.raw with option -e (extract all data),

as result "telesignal_1msps.complex32" was extracted.

Opened in URH:

![1](img/task7_4.png)

Name of file (telesignal) and screenshot above gave me idea that it can be some TV signal ( image line by line ) but my knowledge of RF signals too small and I decided to switch to other task.

PS: if open hints:

- The transmission might contain polluted packets.
- Other default parameters might been tampered, but the capture was at 1Msps.
- ARFCN 34.

PPS: tried:
```bash
grgsm_decode -c telesignal_1msps_cut.complex -a 34 -v -s 1M -m XXX -t YYY
```
with different combinations of XXX and YYY - no succes :(



### File: CTFs/NNC2019/Binary Hero/blackvs.md

# Binary hero

_BlackVS/VVS way_

What we have:
- a badge with a new for me CPU/architecture (Xtensa). Well documented. It is good.
- available from manufacturer toolkits for programming/updating/dumping. Later we will see that this not needed for this task but helped to ... modify firmware to generate all flags at once %)

Let's start.
## Disassembling ... what exactly?
Ok, to disassemble/analyze something we should first get victim :)
Solving Mr. Bean Walker task, you already found first candidate for victim - *https://spynet.techmaker.ua/fw/nn-badge.bin*

Good start but... may be something more interesting in *https://spynet.techmaker.ua/fw/* folder can be found?

Let's see what is there... alleluia!

***https://spynet.techmaker.ua/fw/nn-badge.elf***

Jackpot (maybe).

Now we have bin and ELF at the same time - we have a very good start point for now.

## Disassembling ... using what?
Tools make world. 

Sure, bytecode analysis/coding is good but very slow way... (it is the last way if no other solutions found ^) - thanks to Espressif for good SDK/documentation.

### IDA. Very known and very old tool. Still alive and kicking %)
Surprise. Xtensa architecture is not supported by IDA from box. 

You can find few Python based plugins which can (theoretically) add support for this architecture to IDA but I failed going this way - neither IDA Pro 6.8 nor IDA Pro 7.0 correctly worked with plugins I found ^)
If somebody was able to success in this way - please share your experience with us %))

### Espressif toolkits/SDK
This architecture/CPU is quite good supported by manufacturer - you can download free SDK/toolkits for programming (and not only) this device.
For example, to disassemble ELF file:
```
xtensa-esp32-elf-objdump -dSgtr bootrom.elf > nn-badge192.elf.diasm
```
It is much better comparing to byte coding but... we have Radare2 %)

### Radare2 + Cutter
Because I was out of reverse engineering for a long time Radare2 was for a good surprise for me. 
Yes, It is strange a little bit (comparing to other tools) but it has own good made logic. 
And it can work in console! It is cool. Linux and GUI is not for me...
But to start faster you can choose Cutter - GUI for Radare2. And can you Windows or Linux - on your choice.
The latest release can be downloaded from [here](https://github.com/radareorg/cutter/releases).

## Disassembling ... finally
It is very easy - just run Cutter, choose downloaded before ELF file and set all analysis options %) (use default only is not enough in this case):

![alt text](img/blackvs.00.jpg)

![alt text](img/blackvs.01.jpg)

During Mr.Bean Walker task we reveal (I hope you too) very interesting string "flag{%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x}".
I Especially if you know C++.

Let's locate it using Cutter:

![alt text](img/blackvs.02.jpg)

Ok, here you are!
Now check XRefs for it (right click on string address and choose XRefs):

![alt text](img/blackvs.03.jpg)

and... yessss - secret function found:

![alt text](img/blackvs.04.jpg)

Now is the simplest - just to check it's results... simplest? Oh no, it was big mistake %)

Let's look on pseudo-code:

![alt text](img/blackvs.05.jpg)

Nothing new.

Ok. We can run emulated code. Let's try:

![alt text](img/blackvs.06.jpg)

Seems good, next... 

![alt text](img/blackvs.07.jpg)

Good... what??????

Value 78 stored to a8 shown as 0xffffffce ? WTF (sorry for Code of conduct violation)... but it is really not good - emulation doesn't work properly for ESP32.

Finita la comedia?

Sure not %)

Let's relax and ... I remember 80x, I was too young... (I am sitting on the sun and drinking beer talking this story) ... we coded using... pen and sheet of paper. Really %)

Ok, let's start and... here are the results:

![alt text](img/blackvs.08.jpg)

Flag is on this paper. If you don't see - ok, some hints below:

## Hint 1. ESP32 not using stack
It is true. This processor uses different approach - arguments to called function passed via registers (subset of a0...a15) and stored in buffer values ("window").

Registers a0 and a1 special.

Which registers used depends of call type.

In the case of **call8** registers shifted on 8 i.e. registers a10..a15 of caller function become a2..a7 in the called one.

## Hint 2. movi/movi.n
Store immediate value to specified register.
I.e.
```
movi.n a8, 78
```
means
```
a8 = 78
```

## Hint 3. s32i / s32i.n
Store value of first operand to the buffer (addressed by the second operand) with offset set by third operand. I.e.
```
s32i.n a8, a1, 28
```
means take value of register a8 and store to address a1+28:
```
a1[28]=a8
```
Be careful - 32 means 32-bit value i.e. 4 bytes size.

Offset is set in bytes. 

I.e. for packing 10 4-bytes values we should use offsets 0, 4, ..., 36.

## Hint 4. sprintf

If you [remember](http://www.cplusplus.com/reference/cstdio/sprintf/) - sprintf takes two obligatory arguments - output buffer and format string.
The amount of needed additional parameters depends on format string.
In our case format string is... 

flag{%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x%02x}

**%02x** - it means that needed integer value which will be printed as hex with exactly two hex digits in lower case.
I.e. 10 (decimal) will be printed as 0a in hex.
We need 14 such numbers.
*sprintf* called via *call8* - i.e. arguments passed using a10..a15.
The first two - a10 and a11 - used for output buffer and format (you can easily check this from code).
I.e. next registers - a12..a15 - used to pass next 4 arguments.
Rest 10 arguments passed via buffer. Address of buffer stored in a1.
Element addressed as a1+0, a1+4 ... a1+36.

What you need - just find values of a12, a13, a14, a15, a1+0, a1+4, ..., a1+36 before sprintf call %)

Let's try!

The road is made by walking; Walking makes the road



### File: CTFs/NNC2019/BruteSearcher/blackvs.md

# Brute Searcher

Getting *mr.Bean Walker* flag we discovered remote firmware folder:

![alt text](img/blackvs.11.png "Firmware folder")

But may be https://spynet.techmaker.ua/ has more accessible folders?
Let's check

## dirb

Let's run *dirb* from **Kali** and ... voilà ::

![alt text](img/blackvs.00.png "dirb@Kali")

## dirsearch 

If you don't have Kali you can download [dirsearch](https://github.com/maurosoria/dirsearch) tool and run it everywhere where Python present ^) :

![alt text](img/blackvs.01.png "Dirsearch@powershell")

## dirbuster

If you don't like Python but happy of Java %) - you can use **dirbuster**. It is included in [Kali](https://kali.tools/?p=116) as well as can be used standalone everywhere Java is (see at [OWASP](https://www.owasp.org/index.php/Category:OWASP_DirBuster_Project)).

## Capturing Flag

We discovered few more remote folders:

```
+ https://spynet.techmaker.ua/admin (CODE:401|SIZE:0)                          
+ https://spynet.techmaker.ua/Admin (CODE:401|SIZE:0)                          
+ https://spynet.techmaker.ua/ADMIN (CODE:401|SIZE:0)                          
+ https://spynet.techmaker.ua/docs (CODE:200|SIZE:249)                         
+ https://spynet.techmaker.ua/favicon.ico (CODE:200|SIZE:15086)                
+ https://spynet.techmaker.ua/fw (CODE:301|SIZE:0)                             
+ https://spynet.techmaker.ua/index (CODE:200|SIZE:3586)                       
+ https://spynet.techmaker.ua/Index (CODE:200|SIZE:3585)                       
```
First will check folders with return code 200 (OK) i.e. public available folders. It seems to be we got next prize:

![alt text](img/blackvs.02.png "docs@ptechmaker")

Let's try download/open both discovered files (yep - *secret.txt* sounds very promising).

https://spynet.techmaker.ua/docs/secret.txt

![alt text](img/blackvs.04.png "Flag")

PS: if you see "*flag{wrong deviceid}*" instead or error like this:

![alt text](img/blackvs.06.png "DeviceID missing")

it means no DeviceID cookie present during download request. 

To fix this you can just login to your Badge page:

![alt text](img/blackvs.03.png "Flag")

But if you don't look for easy ways you can manually add needed cookie directly in request. Name and value of cookie can be spied from Badge page:

![alt text](img/blackvs.07.png "Cookie")

This can be very helpful expirience for fulfilling "*NoNameCon SpyNet*" tasks later %))

After getting flag just register it on your badge:


![alt text](img/blackvs.05.png "Cookie")

<div align="center">
![alt text](img/blackvs.08.png "Done")
</div>





### File: CTFs/NNC2019/Extra/2. Patching/part1.md

# Badge Firmware patching

## Part 1: analyzing

First download images for analyzing (they are already in *Scripts* folder):

https://spynet.techmaker.ua/fw/nn-badge.bin
https://spynet.techmaker.ua/fw/nn-badge.elf

Due to we intend modify firmware let make backup:

```bash
copy nn-badge.bin nn-badge.bak
```

Next disassemble firmware to get segments:

```bash
nnc_disassemble.py nn-badge.bin
```

You should see:

```bash
G:\nonamebadge-2019-ctf\Extra\2. Patching\scripts>nnc_disassemble.py nn-badge.bin
Image version: 1
Entry point: 40080ffc
secure_pad: False
flash_mode: 2
flash_size_freq: 32
6 segments

Segment 1: len 0x2bcb0 load 0x3f400020 file_offs 0x00000018
  addr=0x3f400020 file_offs=0x18 include_in_checksum=True

Segment 2: len 0x03614 load 0x3ffbdb60 file_offs 0x0002bcd0
  addr=0x3ffbdb60 file_offs=0x2bcd0 include_in_checksum=True

Segment 3: len 0x00400 load 0x40080000 file_offs 0x0002f2ec
  addr=0x40080000 file_offs=0x2f2ec include_in_checksum=True

Segment 4: len 0x00914 load 0x40080400 file_offs 0x0002f6f4
  addr=0x40080400 file_offs=0x2f6f4 include_in_checksum=True

Segment 5: len 0xd1f18 load 0x400d0018 file_offs 0x00030010
  addr=0x400d0018 file_offs=0x30010 include_in_checksum=True

Segment 6: len 0x15b64 load 0x40080d14 file_offs 0x00101f30
  addr=0x40080d14 file_offs=0x101f30 include_in_checksum=True

Checksum: 33 (valid)
Validation Hash: 94f0a1f483bf3b0db3ec20f26bf4f7dab910487b228b6d4885bfdf79562074f5 (valid)
END
```

We have 6 segments. Question is where is our point of interest located %)

Let's run radare2/cutter and open ELF file first (due to it may contain symbolic/debug information):

![alt text](img/00.png "")

Locate "flag{.." string as we did in *Binary Hero* task:

![alt text](img/01.png "")

Next X-Ref to functions which use this string (in our case it is single function):

![alt text](img/02.png "")

It is already known from *Binary Hero* task function %)) :

![alt text](img/03.png "")

But we will go deeper - let's scroll down and ... we will see *os_isValidFlag* function!

![alt text](img/04.png "")

It seems we go in right direction!

![alt text](img/05.png "")

Let's switch to pseudo-code generation mode 

(PS: I used Cutter v.1.8.2 due to the latest at this moment Cutter v1.8.3 is not supporting xtensa pseudo-code generation ^( ) :

![alt text](img/06.png "")

Now we can reveal system functions like *strcmp* etc:

![alt text](img/07.png "")

Also we see, that after successful check flag is sent via Wi-Fi:

![alt text](img/08.png "")

Let's comment code to mark lines with system functions:

![alt text](img/09.png "")

Hm, strcmp should get 2 arguemnts (due to it compares 2 strings... should compare two strings), by here we see that first string compared to ... zero string. Strange... it seems to be we have stripped ELF.

But we have bin file and we sure that it fully functional %)

Due to *os_isValidFlag* function start at 0x400d257b we need analyze segment 5:

Let's load it in the separate Cutter session (don't close Cutter with ELF session - we will need it later!):

![alt text](img/10_0.png "")

And go to 0x400d257b and ... nothing - it is surely not our os_isValidFlag function.

![alt text](img/10_1.png "")

It seems to be ELF and bin coded shifted to each other.

Let try locate our *os_isValidFlag* Function using power of radare2 %) :

Let's back to our ELF file, to the start of *os_isValidFlag* and remember first 4 bytes it starting with

![alt text](img/10_2.png "")

![alt text](img/10_3.png "")

Now back to out seg5 and let's search all such bytes in it via radare2 console:

```bash
/x 00362101 
```
and ... first hit successful. I've already renamed *fcn.400d5218* to *os_isValidFlag* for convinience:

![alt text](img/10_9.png "")

Now let open both bin and elf files side by side to compare:

![alt text](img/11.png "")

We see that code is different but similar - we easily can match code blocks:

![alt text](img/12.png "")

![alt text](img/13.png "")

Comparing code we can recognize sytem calls.
Also we see new function which not called in ELF file - 0x400d5108:

![alt text](img/14.png "")

It seems to be our flag generation function which was substituted by zero string in ELF file. Let's rename it and check our commented code:

![alt text](img/15.png "")

![alt text](img/16.png "")

Now much better - code is readable %) 

Let check flag generation function - it is main point of interest for people who wish unwind it %))) :

![alt text](img/17.png "")

But we will back to our *os_isValidFlag* function:

![alt text](img/18.png "")

We see that each gen_flag call receives some argument. Let check what exactly passed to it:

![alt text](img/19.png "")

Yep... we need load *seg1* to continue:

![alt text](img/20.png "")

Here is... secret "phrase"?
It seems that generating function accepts only secret phrase, different for each flag and generate flag basing on this phrase and... device id? Who knows %)

Let check our hypothese:

![alt text](img/21.png "")

![alt text](img/22.png "")

![alt text](img/23.png "")

Yep. all secret phrases found.
Now we can... we can patch firmware to generate and print flags when we wish %) 



### File: CTFs/NNC2019/Extra/2. Patching/part2.md

# Badge Firmware patching

## Part 2: patching (to get all flags)

Turn on our badge, connect to it via terminal and check flags.
As you see - no flags (I did factory reset before to ensure):

![alt text](img/100.png "")

The main idea is:
- from [Part1: analyzing](part1.md) we know flag generation function and arguments which should be passed to it to get flag
- we need modify firmware to generate all flags when we need them
- simplest and straigt solution as for me is ... modify *flag* command (see screenshot above) %)
- to find code implementation of this function we can start from static text string printed at the flag command execution i.e. "Challenge..."

This string can be easily found both in binary:

![alt text](img/101.png "")

and in radare2/Cutter:

![alt text](img/102.png "")

Next we need to locate start of string (due to "*Challenge*" is in the middle of *flag* command output).
It is quite easy due to firmware written using C and use zero-terminated strings:

![alt text](img/103.png "")

i.e. 0x3f4025f0 - address of needed string.

Let’s try locate who use it.
Try search for bytes **f0 25 40 3f** (Little Endian byte order!) :

![alt text](img/104.png "")

Yep, we have one hit, super %) :

![alt text](img/105.png "")

But as we see it is in data segment (you may switch from hex to disassemble view to ensure).

I.e. it is cell which stores address - it is usual for dynamic linked libraries for example.

Try to find who is refering to this cell:

![alt text](img/106.png "")

Hm, no hits.
Problem? Not!
X-tensa architecture uses removable code i.e. links/references can be set as offset from current position.
Now we need real power of radare2!

![alt text](img/107.png "")

Command "/c" means to search text in the disassembled code. It is real cool feature - and we have a hit!

Let's check found hit :

![alt text](img/108.png "")

and go to the beginning of function containing this hit:

![alt text](img/109.png "")

We found flags printing function. Simple.

Let's switch on showing hex codes in disaassemble view:

![alt text](img/110.png "")

Now it is the ... no, not simplest.

Hardest %))

Why - radare2 does not support yet inserting assembler code for X-Tensa - you may try check this: right click on any code, Edit, instructions and.. entering any instruction gives "Unknown instruction..."

You can only insert byte-code. It can be helpful in our case due to entering byte code you immediately see corresponding asm-code (due to radare2 can disassemble x-tensa %) 

It was my first solution - I entered byte-codes until got needed instructions.

Trust me - due to bugs this way is slow and hard %)))

But we just need way generate correct byte codes for just two instructions - call8 and l32r.

Why?

All code which I wish to create is:

```asm
|           0x400d548b      call8 fcn.400d51bc ; fcn.400d51ba+0x2
                            call8 printf ; 0x400d689c
                            l32r a10, 0x400d0444
                            call8 gen_flag
                            call8 printf ; 0x400d689c
                            l32r a10, 0x400d044c
                            call8 gen_flag
                            call8 printf ; 0x400d689c
                            l32r a10, 0x400d0454
                            call8 gen_flag
                            call8 printf ; 0x400d689c
                            l32r a10, 0x400d0460
                            call8 gen_flag
                            call8 printf ; 0x400d689c
                            l32r a10, 0x400d043c
                            call8 printf ; 0x400d689c
                            retw.n
```

*retw.n* is always **1d f0** (we can see it from picture above)

But call8 and l32r use relative addressing i.e. offset from current position:

![alt text](img/111.png "")

![alt text](img/112.png "")

I wrote simple Python3 code to generate needed code:

```python
#!/usr/bin/env python
import sys
import argparse
from binascii import *


def rshift(val,n):
    mask1 = 0x80000000
    sign = (val & mask1)
    mask3 = (~((1<<(32-n))-1), 0)[sign==0] #python support big numbers
    return (val>>n) | mask3

#The target instruction
#address of the call is given by the address of the CALL8 instruction with the two
#least significant bits set to zero, plus the sign-extended 18-bit offset field of the instruction
#shifted by two, plus four.
def make_call8(pc,offset):
    start=pc&~0b11
    if offset&0b11:
        print("Offset must have 2 lowest bits equal to zero i.e. 4 bytes aligned")
        return
    # offset = pc + (diff<<<2) + 4 => 
    diff= ( offset - start - 4 ) 
    # instraction = offset (18bit) + 10 + 0101
    byte0 = 0b100101 |( ( diff & 0b1100 )<<4)
    byte1 = (diff & 0b111111110000) >> 4
    byte2 = (diff & 0b11111111000000000000) >> 12
    print("{:08x}: call8 {:08x} = {:02x} {:02x} {:02x}".format(pc, offset, byte0, byte1, byte2))
    return pc+3

#L32R forms a virtual address by adding the 16-bit one-extended constant value encoded
#in the instruction word shifted left by two to the address of the L32R plus three with the
#two least significant bits cleared. Therefore, the offset can always specify 32-bit aligned
#addresses from -262141 to -4 bytes from the address of the L32R instruction. 32 bits
#(four bytes) are read from the physical address. This data is then written to address
#register at.
#  offset = (0b11111111 | imm16) << 2 + 
#  start = ( (pc + 3) & ~0b11 )
#  offset = (0b11111111 | imm16) << 2 + start
#  imm16 = ( (offset - start) >>> 2 ) & 0b11111111

#   where >>> is argipmhetic shift, rshift

def make_l32r(pc,regNum,offset):
    start = (pc+3) & ~0b11
    byte0 = 0b0001 | ( regNum << 4 )
    imm16 = rshift( offset - start, 2 )
    byte1 = imm16 & 0xff
    byte2 = (imm16>>8) & 0xff
    print("{:08x}: l32r a{}, {:08x} = {:02x} {:02x} {:02x}".format(pc, regNum, offset, byte0, byte1, byte2)) #LE
    return pc+3



#            0x400d5488      366100                 entry a1, 48
#            0x400d548b      call8 fcn.400d51bc ; fcn.400d51ba+0x2
#                            call8 printf ; 0x400d689c
#                            l32r a10, 0x400d0444
#                            call8 gen_flag
#                            call8 printf ; 0x400d689c
#                            l32r a10, 0x400d044c
#                            call8 gen_flag
#                            call8 printf ; 0x400d689c
#                            l32r a10, 0x400d0454
#                            call8 gen_flag
#                            call8 printf ; 0x400d689c
#                            l32r a10, 0x400d0460
#                            call8 gen_flag
#                            call8 printf ; 0x400d689c
#                            l32r a10, 0x400d043c
#                            call8 printf ; 0x400d689c


if __name__ == '__main__':
    #0x400d5494      a1eceb                 l32r a10, 0x400d0444
    #pc=0x400d5494
    #pc=make_l32r(pc, 10, 0x400d0444) # => a1 ec eb

    pc=0x400d548b
    pc=make_call8(pc, 0x400d51bc) #hidden flag
    pc=make_call8(pc, 0x400d689c) #printf
    pc=make_l32r(pc, 10, 0x400d0444) #l32r a10, 0x400d0444
    pc=make_call8(pc, 0x400d5108) #gen_flag
    pc=make_call8(pc, 0x400d689c) #printf
    pc=make_l32r(pc,  10, 0x400d044c) #l32r a10, 0x400d044c
    pc=make_call8(pc, 0x400d5108) #gen_flag
    pc=make_call8(pc, 0x400d689c) #printf
    pc=make_l32r(pc,  10, 0x400d0454) #l32r a10, 0x400d0454
    pc=make_call8(pc, 0x400d5108) #gen_flag
    pc=make_call8(pc, 0x400d689c) #printf
    pc=make_l32r(pc,  10, 0x400d0460) #l32r a10, 0x400d0460
    pc=make_call8(pc, 0x400d5108) #gen_flag
    pc=make_call8(pc, 0x400d689c) #printf
    pc=make_l32r(pc,  10, 0x400d043c) #Welcome flag
    pc=make_call8(pc, 0x400d689c) #printf

```

The output of code is:

```bash
400d548b: call8 400d51bc = 25 d3 ff
400d548e: call8 400d689c = e5 40 01
400d5491: l32r a10, 400d0444 = a1 ec eb
400d5494: call8 400d5108 = 25 c7 ff
400d5497: call8 400d689c = 65 40 01
400d549a: l32r a10, 400d044c = a1 ec eb
400d549d: call8 400d5108 = a5 c6 ff
400d54a0: call8 400d689c = a5 3f 01
400d54a3: l32r a10, 400d0454 = a1 ec eb
400d54a6: call8 400d5108 = 25 c6 ff
400d54a9: call8 400d689c = 25 3f 01
400d54ac: l32r a10, 400d0460 = a1 ed eb
400d54af: call8 400d5108 = a5 c5 ff
400d54b2: call8 400d689c = a5 3e 01
400d54b5: l32r a10, 400d043c = a1 e1 eb
400d54b8: call8 400d689c = 25 3e 01
```

All you need is just put these codes in proper place ^) :

![alt text](img/113.png "")

![alt text](img/115.png "")

Let's check modified binary in radare2/Cutter - good, 100% correct code:

![alt text](img/116.png "")

Now assemble firmware from segments (including modified one):

```bash
nnc_assemble.py nn-badge.bin.map nn-badge-patched.bin

G:\nonamebadge-2019-ctf\Extra\2. Patching\scripts>nnc_assemble.py nn-badge.bin.map nn-badge-patched.bin
Entrypoint: 40080ffc
The number of segments: 6
1: file=nn-badge.bin.seg1 map=3f400020 file_ofs=00000018 in_checksum=True
2: file=nn-badge.bin.seg2 map=3ffbdb60 file_ofs=0002bcd0 in_checksum=True
3: file=nn-badge.bin.seg3 map=40080000 file_ofs=0002f2ec in_checksum=True
4: file=nn-badge.bin.seg4 map=40080400 file_ofs=0002f6f4 in_checksum=True
5: file=nn-badge.bin.seg5 map=400d0018 file_ofs=00030010 in_checksum=True
6: file=nn-badge.bin.seg6 map=40080d14 file_ofs=00101f30 in_checksum=True

```

Due to I patched in-place - no modifying of map file needed:

![alt text](img/117.png "")

Sign, verify and flash patched firmware:

```bash
espsecure.py sign_data -k private.pem nn-badge-patched.bin
espsecure.py verify_signature -k public.key nn-badge-patched.bin
esptool.py --chip esp32 image_info nn-badge-patched.bin
esptool.py -p com4 -c esp32 write_flash 0x190000 nn-badge-patched.bin
```

![alt text](img/118.png "")

Connect to badge and ... it is alive!

Cool. Let's run "flags" command:

![alt text](img/119.png "")

Output is little bit ridiculous but we see all flags %) 
Let's verify all them - 
Success.

Ok, let flash original, non patched, firmware (due to we disabled wi-fi connection in the original "flag" command ):

```bash
esptool.py -p com4 -c esp32 write_flash 0x190000 nn-badge.bin
```

Connect to badge and ... - yes, we got all flags 

![alt text](img/120.png "")

and we are successfully registered them:


<div align="center">
![alt text](img/121.png "Flags")
</div>


<div align="center">
![alt text](img/1xx.jpg "Done")

<b>Full success %)</b>
</div>



### File: CTFs/NNC2019/Extra/3. MITM/part2/README_0x4.md

# 3.2. Disabling CA cert check (4 bytes decision %)

As we see in previous part - to allow MITM we have to ptach badge firmware with own CA certificate.

If we change server with MITM or use difefrent MITM proxy software - we have to re-assemble new firmware with new CA certificate.

Or use the same CA certificate in all MITM proxies for concrete patched firmware.

Not very convinient.

May be we can fix this?

Let's check notifications for situation when we use original badge firmware and MITM proxy:

![alt text](img/100.png "")

We see debug messages which includes also modules names/specific labels:

* WiFi
* esp-tls
* TRANS_SSL
* HTTP_CLIENT
 
Remember them!!!


Let's load firmware in Radare2 and try to locate point in the code where any of these messages are printed.

Due to I'm very lazy man I prepared special *badge_bin_sects.elf* which combines segments from BIN file with debug/symbol data from ELF. It makes reverse engineering life much easier.

(How I did this is separate story...)

![alt text](img/101.png "")

Let's check for *spynet.techmaker.ua* url in code:

![alt text](img/102.png "")

Go to the code which uses this URL:

![alt text](img/103.png "")

Scroll up little bit ...

![alt text](img/104.png "")

and we see also our built-in CA certifica here! We go in right direction.

Let's check function to which passed built-in CA.

Adrees of fanction stored at 0x400d054c (idirect call):

![alt text](img/105.png "")

Function has address 0x40167be0:

![alt text](img/106.png "")

Let's look closer:

![alt text](img/107.png "")

scroll down and ... yep - we saw debugimg info:

![alt text](img/108.png "")

I.e. it is call to function in esp_http_client.c - standard ESP-IDF library (thanks to Anvol for diganostic/debug messages %).

ESP-IDF available from https://github.com/espressif/esp-idf :

![alt text](img/109.png "")

But I copied few files for you to *scripts/2. Disabling CA check/esp-idf* folder.

It seems to be found function is (may be I'm wrong but looks very similar %) :

![alt text](img/110.png "")

Let's check passed to it argument type:

![alt text](img/111.png "")

Hm, "if the client requires to verify server..." ... but if not? %)

On the first screenshot we saw "*esp-tls*" and .. we found corresponding files in ESP-IDF toolkit %) 

![alt text](img/112.png "")

Some code investigations:

![alt text](img/113.png "")

![alt text](img/114.png "")

![alt text](img/115.png "")

I.e. it seems if instead of CA certificate we will pass just zero-point server's identity will not be checked.

Let's check this idea.

Certificate address stored at 0x400d0528 :

![alt text](img/116.png "")

![alt text](img/117.png "")

From badge info :

```bash
Image version: 1
Entry point: 40080ffc
secure_pad: False
flash_mode: 2
flash_size_freq: 32
6 segments

Segment 1: len 0x2bcb0 load 0x3f400020 file_offs 0x00000018
  addr=0x3f400020 file_offs=0x18 include_in_checksum=True

Segment 2: len 0x03614 load 0x3ffbdb60 file_offs 0x0002bcd0
  addr=0x3ffbdb60 file_offs=0x2bcd0 include_in_checksum=True

Segment 3: len 0x00400 load 0x40080000 file_offs 0x0002f2ec
  addr=0x40080000 file_offs=0x2f2ec include_in_checksum=True

Segment 4: len 0x00914 load 0x40080400 file_offs 0x0002f6f4
  addr=0x40080400 file_offs=0x2f6f4 include_in_checksum=True

Segment 5: len 0xd1f18 load 0x400d0018 file_offs 0x00030010
  addr=0x400d0018 file_offs=0x30010 include_in_checksum=True

Segment 6: len 0x15b64 load 0x40080d14 file_offs 0x00101f30
  addr=0x40080d14 file_offs=0x101f30 include_in_checksum=True

Checksum: 33 (valid)
```

needed segment for patching is segment 5.

Offset in segment file is 0x400d0528-0x400d0018=0x510 :

![alt text](img/118.png "")

Just make them zero, assemble, sign, verify and flash %)

And enjoy - now badge "trusts" to any remote server %)


### File: CTFs/NNC2019/Mr Bean Walker/blackvs.md

# Intro. Mr. Bean Walker and .. Doom?

## 0. Turn badge on
First of all you have to attach your badge to computer and connect to it via terminal. 

Correspondent instructions can be found at official NonameCon Badge [page](https://nonamecon.org/badge).
After connecting first try 'help' - works :)

![alt text](img/blackvs.00.png "Help command")

![alt text](img/blackvs.01.png "Help command results")

Good. Next try all commands mentioned in the help output:

![alt text](img/blackvs.02.png "Rest of commands")

Not good - we need root to run most of them.

But it seems *restart* works:

![alt text](img/blackvs.03.png "Help command results")

We see a lot of very interesting information including hint at the end.

Ok, now we need find mentioned trailer. Badge trailer. Google will help to us ^)

It was found at the official NonameCon Youtube channel - here it is: [NoNameCon Badge Trailer](https://www.youtube.com/watch?v=chfoAWevHMs)

## 1. Watch and enjoy trailer at Youtube

![alt text](img/blackvs.04.png "Doom...")

Yep, interesting... but what it is????
Password?????
Yesssssss

## 2. Get root
Let's try 'iddqd' found in video in terminal:

![alt text](img/blackvs.05.png "Doom...")

Super:

![alt text](img/blackvs.08.jpg "Doom...")

(hands themselves type 'idkfa' %) Yep, it is not [Doom](http://lurkmore.to/IDDQD) :))

![alt text](img/blackvs.06.png "Doom...")

Let's try other commands, for example:

![alt text](img/blackvs.07.png "...")

Ok. We have root. Now we need flags %)

## 3. Get the first flag

Check rest commands like *dmsg*, *join* etc.
For example, try connect badge to Wi-Fi:

![alt text](img/blackvs.09.png "Wi-Fi...")

and... after some time we will see diagnostic message:

![alt text](img/blackvs.10.png "BIN")

Very interesting. Can we download firmware manually? Yes, we can %)
But let's check folder with binary:

![alt text](img/blackvs.11.png "ELF")

Ok, we have both **bin** and **ELF** images - very good. Let's analyze them.
First of all check for strings inside:

```
rabin2.exe -zz nn-badge195.bin
```

if you have **radare2** installed

or 

![alt text](img/blackvs.12.png "Strings")

if you have Kali.

I used... FAR %) :

![alt text](img/blackvs.13.png "FAR")

Ok, it seems to be found hard-coded flag - let's check it:

![alt text](img/blackvs.14.png "Mr. Bean")

Yehhho!!!

![alt text](img/blackvs.ff.gif "Success RuLeZ")



### File: CTFs/NNC2019/NoNameCon SpyNet/blackvs.md

# NoNameCon SpyNet
*(c) comics by VVS*

Fulfilling BrutSearcher task we discovered https://spynet.techmaker.ua/admin/ - time take a closer look.
Sure, trying access it gives HTTP ERROR 401.

Ok. Let's try [XSS](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)) 

First candidate for injection is DeviceID, for example, let's try 
```DeviceID=<script>alert()</script>```

![alt text](img/blackvs.00.png "")
![alt text](img/blackvs.01.png "")

... not succeeded.

Ok, next user input, which displayed by SpyNet is... flags in terminal:

![alt text](img/blackvs.02.png "")
![alt text](img/blackvs.03.png "")
![alt text](img/blackvs.04.png "")
![alt text](img/blackvs.05.png "")
![alt text](img/blackvs.06.png "")

Yehhho!!! XSS injection possible.

Which limitations we have:
* we can't do flags longer 40 bytes:

![alt text](img/blackvs.07.png "")
 
* due to we intend to catch admin's cookies we need save intercepted information somewhere globally accessed from Techmakers site.

Starting from this point next scenarious possible:
1. If you have own site which quit short URL - you can use it. It was the first my scenarios - I prepared small JS script at my server and injected instead flag URL to it. Stolen cookies were written into the text file.

2. About the same as variant 1 but ... cookies were sent to me via Telegram bot %)

3. Later I was pushed to shorter way - [XSS Hunter](https://xsshunter.com/):

First sign up:
hint - make *yoursubdomain* during signup shorter as possible (remember 40 chars limit? ):
![alt text](img/blackvs.10.png "")

On fetaure page you will found code for injection (just replace *yoursubdomain* with your subdomain which your set during signup)
![alt text](img/blackvs.11.png "")

Then put your injection code instead flag name in terminal:
![alt text](img/blackvs.13.png "")

and ... wait. 

After some period (~5 minutes) your will receive notification mail from XSS Hunter.
Also in XSS Fires seection you will see that SpyNet got caught in XSS nets %) :

![alt text](img/blackvs.14.png "")

Here are cookies:
![alt text](img/blackvs.15.png "")

At my first try I used [PostMan](https://www.getpostman.com/) - it very easy to add/remove cookies for any request.

In the case of Chrome we should little bit to dance - it not allows add cookie (directly or via JS command in console) for https://spynet.techmaker.ua/admin .

What I did in Chrome:

* added stolen cookies for https://spynet.techmaker.ua/ page:

![alt text](img/blackvs.16.png "")

![alt text](img/blackvs.17.png "")

it seems to fail but be patient! Just switch to https://spynet.techmaker.ua/admin/ page :

![alt text](img/blackvs.18.png "")

Ok, we near to win. Wrong DeviceID - ok will change it to our one:

![alt text](img/blackvs.19.png "")
- flag captured!

![alt text](img/blackvs.20.png "")
![alt text](img/blackvs.21.png "")
and accepted.

![alt text](img/blackvs.22.png "")

Used links:
https://xsshunter.com/signup
https://xsshunter.com/features
https://xsshunter.com/app
https://spynet.techmaker.ua/admin/



### File: CTFs/NNC2019/Ployka PWNer/blackvs.md

# Ployka PWNer

## Intro:

**Ployka (плойка)** - it is informal name of PlayStation in Russian

Getting NoNameCon SpyNet flags we saw help message:

![alt text](img/blackvs.00.png "")

Also some hints given by PS3 history itself:

**ECDSA**
https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm

**PS3**

Wiki writes: *In August 2013, it was revealed that bugs in some implementations of the Java class SecureRandom sometimes generated collisions in the {\displaystyle k} k value. This allowed hackers to recover private keys giving them the same control over bitcoin transactions as legitimate keys' owners had, using the same exploit that was used to reveal the PS3 signing key on some Android app implementations, which use Java and rely on ECDSA to authenticate transactions.[11]*

**PS3 breakdown**

https://xakep.ru/2012/10/26/59539/

Additional hints can be found via Key Recovery page:
 
![alt text](img/blackvs.02.png "")

Check all links provided on this page:

http://tiny.cc/nnc-esp-signed-app

http://tiny.cc/nnc-sha-sk

http://tiny.cc/nnc-sha-result

I.e. it seems to be we have to:
* restore private key
* generate Recovery Key as SHA256(DeviceID '+' SHA256(DER)) 
PS: one notice - DER here is DER in HEX format, not raw binary one.

## Version command output

Let's check version command output:

![alt text](img/blackvs.01.png "")

We see:
- two digest (firmware and partition table) and two correspondent SHA256 signatures;
- we are very lucky: both signatures have common part at start. I.e. we have the about same situation as with PS3 breakdown;
- also corresponding public key is available - it is helpful too.

## Check public key

First check public key for additional information.
Save public key as badge_public.crt (PEM format) :

``` badge_public.crt
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE5UQ/BT52Hda1iGUfrgifjNykXpLD
YRY3hSNrqYODGQOfWHbOP8NeN2KMlRazbg92viuDiKnx8Z/ngvWMqi85Og==
-----END PUBLIC KEY-----
```

And get info:

**Linux/MAC**:
```bash
vvs@ubnt-server-0:~/ployka$ openssl asn1parse -in badge_public.crt 
    0:d=0  hl=2 l=  89 cons: SEQUENCE          
    2:d=1  hl=2 l=  19 cons: SEQUENCE          
    4:d=2  hl=2 l=   7 prim: OBJECT            :id-ecPublicKey
   13:d=2  hl=2 l=   8 prim: OBJECT            :prime256v1
   23:d=1  hl=2 l=  66 prim: BIT STRING       

vvs@ubnt-server-0:~/ployka$ openssl pkey -inform PEM -pubin -in badge_public.crt -text -noout
Public-Key: (256 bit)
pub:
    04:e5:44:3f:05:3e:76:1d:d6:b5:88:65:1f:ae:08:
    9f:8c:dc:a4:5e:92:c3:61:16:37:85:23:6b:a9:83:
    83:19:03:9f:58:76:ce:3f:c3:5e:37:62:8c:95:16:
    b3:6e:0f:76:be:2b:83:88:a9:f1:f1:9f:e7:82:f5:
    8c:aa:2f:39:3a
ASN1 OID: prime256v1
NIST CURVE: P-256
```

**Windows**:

Convert it to raw DER format: 
```
certutil -decode badge_public.crt badge_public.raw
```

After get info about this certificate:
```
certutil -asn badge_public.raw > badge_public.info
```

Result is:
```
0000: 30 59					; SEQUENCE (59 Bytes)
0002:    30 13					; SEQUENCE (13 Bytes)
0004:    |  06 07				; OBJECT_ID (7 Bytes)
0006:    |  |  2a 86 48 ce 3d 02 01
         |  |     ; 1.2.840.10045.2.1 ECC
000d:    |  06 08				; OBJECT_ID (8 Bytes)
000f:    |     2a 86 48 ce 3d 03 01 07
         |        ; 1.2.840.10045.3.1.7 ECDSA_P256 (x962P256v1)
0017:    03 42					; BIT_STRING (42 Bytes)
0019:       00
001a:       04 e5 44 3f 05 3e 76 1d  d6 b5 88 65 1f ae 08 9f
002a:       8c dc a4 5e 92 c3 61 16  37 85 23 6b a9 83 83 19
003a:       03 9f 58 76 ce 3f c3 5e  37 62 8c 95 16 b3 6e 0f
004a:       76 be 2b 83 88 a9 f1 f1  9f e7 82 f5 8c aa 2f 39
005a:       3a
CertUtil: -asn command completed successfully.

```

Now we know used encryption method (ECDSA) and curve type - [ECDSA_P256](http://oid-info.com/get/1.2.840.10045.3.1.7) :
prime256v1 / secp256r1 / NIST256p

It is known problem with known solution:
[DSA nonce recovery from repeated nonce](https://cryptopals.com/sets/6/challenges/44)

Let's solve it.

## Variant 1
Based on [DSA nonce recovery from repeated nonce](https://cryptopals.com/sets/6/challenges/44) and as start point was chosen code from:

https://github.com/TeamContagion/CTF-Write-Ups/blob/master/icectf-2016/Crypto/Contract/contract_solve.py
Originally it is Python 2.x + it use initial data in little bit different format.
After converting to Python 3 the next script was created:

```python
#!/usr/bin/python
import binascii
import hashlib
import sys
from ecdsa import numbertheory, util
from ecdsa import VerifyingKey, SigningKey
from os.path import commonprefix
from binascii import hexlify, unhexlify

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE5UQ/BT52Hda1iGUfrgifjNykXpLD
YRY3hSNrqYODGQOfWHbOP8NeN2KMlRazbg92viuDiKnx8Z/ngvWMqi85Og==
-----END PUBLIC KEY----
"""

PRIVATE_DER_FILE = "private.der"

vk = VerifyingKey.from_pem(PUBLIC_KEY.strip())

# Firmware Digest: 
msg1_sha256 = 'c8c366901c1b6b16dc1f18c026a9010f4140888a67e57bbcef595fb2a5e6f8b7'
# Firmware Signature: 
sig1 = '5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011a6282ba0728b828221cbc4ed38ab3f351666be302c7897e22cc0da3cfbc2b72d'
# Partition Table Digest: 
msg2_sha256 = 'c4682ef52a5d54fc66b2a898e83218821d5af26df00d3da6568ad3c4ba4dabd7'
# Partition Table Signature: 
sig2 = '5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011256ea3cee22f9f9549538b277149b691ba706b576db7e14b3acc13f260ce6c40'

res = commonprefix( (sig1, sig2) )
prefix = len(res)
print('common prefix len = %s' % prefix)

r  = int(sig1[:prefix], 16)
s1 = int(sig1[prefix:], 16)
s2 = int(sig2[prefix:], 16)
z1 = int(msg1_sha256, 16)
z2 = int(msg2_sha256, 16)

k = (z1 - z2) * numbertheory.inverse_mod(s1 - s2, vk.pubkey.order) % vk.pubkey.order
d = (s1 * k - z1) * numbertheory.inverse_mod(r, vk.pubkey.order) % vk.pubkey.order

sk = SigningKey.from_secret_exponent(d, curve=vk.curve, hashfunc=hashlib.sha256)

pem = sk.to_pem()
print("PEM:\n{}\n".format(pem.decode()))

der = sk.to_der()

with open(PRIVATE_DER_FILE, "wb+") as file:
  file.write(der)
print("DER key writed to: {}\n".format(PRIVATE_DER_FILE))

der_hex = hexlify(der)
print("DER HEX:\n{}\n".format(der_hex))
print("SHA256(DER):\n{}\n".format(hashlib.sha256(der).hexdigest()))
print("SHA256(DER_HEX):\n{}\n".format(hashlib.sha256(der_hex).hexdigest()))

```

You can find it in the *Scripts/blackvs/v1/* folder

All you need is install *ecdsa* package:
```
pip install ecdsa
```

## Variant 2
Based on [ecdsa-private-key-recovery](https://github.com/tintinweb/ecdsa-private-key-recovery) Python code.
Originally is Python 2.x based. 
I failed to use on Windows system due to problems with installing *pycrypto* module via *pip* (it tryed to compile some modules during install using VS2019 and failed).
But in Ubuntu - no any problems:

```bash
sudo install python
sudo install python-pip
cd ~
mkdir ployka
cd ployka
git clone https://github.com/tintinweb/ecdsa-private-key-recovery.git
cd ecdsa-private-key-recovery
sudo python setup.py install
```

The first script iteration (v2, *Scripts/blackvs/v2/* folder) used manually parsed data :

```python
#!/usr/bin/python
from ecdsa_key_recovery import DsaSignature, EcDsaSignature
from os.path import commonprefix
from binascii import hexlify, unhexlify
import ecdsa
import hashlib

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE5UQ/BT52Hda1iGUfrgifjNykXpLD
YRY3hSNrqYODGQOfWHbOP8NeN2KMlRazbg92viuDiKnx8Z/ngvWMqi85Og==
-----END PUBLIC KEY----
"""
# Firmware Digest: 
msg1_sha256 = 'c8c366901c1b6b16dc1f18c026a9010f4140888a67e57bbcef595fb2a5e6f8b7'
# Firmware Signature: 
sig1 = '5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011a6282ba0728b828221cbc4ed38ab3f351666be302c7897e22cc0da3cfbc2b72d'
# Partition Table Digest: 
msg2_sha256 = 'c4682ef52a5d54fc66b2a898e83218821d5af26df00d3da6568ad3c4ba4dabd7'
# Partition Table Signature: 
sig2 = '5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011256ea3cee22f9f9549538b277149b691ba706b576db7e14b3acc13f260ce6c40'

pub = ecdsa.VerifyingKey.from_pem( PUBLIC_KEY.strip() ).pubkey

r  = 0x5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011
s1 = 0x256ea3cee22f9f9549538b277149b691ba706b576db7e14b3acc13f260ce6c40
digest1 = unhexlify('c4682ef52a5d54fc66b2a898e83218821d5af26df00d3da6568ad3c4ba4dabd7')

s2 = 0xa6282ba0728b828221cbc4ed38ab3f351666be302c7897e22cc0da3cfbc2b72d
digest2 = unhexlify('c8c366901c1b6b16dc1f18c026a9010f4140888a67e57bbcef595fb2a5e6f8b7')

app1 = EcDsaSignature(( r, s1), digest1, pub, curve = ecdsa.NIST256p)
app2 = EcDsaSignature(( r, s2), digest2, pub, curve = ecdsa.NIST256p)

app2.recover_nonce_reuse(app1)
print app2.export_key()

```

The final one (v3, *Scripts/blackvs/v3/* folder) automatically gets curve, nonce etc:

```python
#!/usr/bin/python
from ecdsa_key_recovery import DsaSignature, EcDsaSignature
from os.path import commonprefix
from binascii import hexlify, unhexlify
import ecdsa
import hashlib

PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE5UQ/BT52Hda1iGUfrgifjNykXpLD
YRY3hSNrqYODGQOfWHbOP8NeN2KMlRazbg92viuDiKnx8Z/ngvWMqi85Og==
-----END PUBLIC KEY----
"""
PRIVATE_DER_FILE = "private.der"

# Firmware Digest: 
msg1_sha256 = 'c8c366901c1b6b16dc1f18c026a9010f4140888a67e57bbcef595fb2a5e6f8b7'
# Firmware Signature: 
sig1 = '5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011a6282ba0728b828221cbc4ed38ab3f351666be302c7897e22cc0da3cfbc2b72d'
# Partition Table Digest: 
msg2_sha256 = 'c4682ef52a5d54fc66b2a898e83218821d5af26df00d3da6568ad3c4ba4dabd7'
# Partition Table Signature: 
sig2 = '5e360eb8b0a077f39482c0ffed76cdaed812db64a9c0a22da0d9953605858011256ea3cee22f9f9549538b277149b691ba706b576db7e14b3acc13f260ce6c40'

########## SOLUTION
vk = ecdsa.VerifyingKey.from_pem( PUBLIC_KEY.strip() )
pub = vk.pubkey
curve = vk.curve

res = commonprefix( (sig1, sig2) )
prefix = len(res)
print 'common prefix len = %s' % prefix

r  = int(sig1[:prefix], 16)
s1 = int(sig1[prefix:], 16)
z1 = int(msg1_sha256, 16)
s2 = int(sig2[prefix:], 16)
z2 = int(msg2_sha256, 16)

app1 = EcDsaSignature(( r, s1), z1, pub, curve=curve)
app2 = EcDsaSignature(( r, s2), z2, pub, curve=curve)
app2.recover_nonce_reuse(app1)

pem = app2.export_key(format="PEM")
print("PEM:\n{}\n".format(pem.decode()))

der = app2.export_key(format="DER")
with open(PRIVATE_DER_FILE, "wb+") as file:
  file.write(der)
print("DER key writed to: {}\n".format(PRIVATE_DER_FILE))

der_hex = hexlify(der)
print("DER HEX:\n{}\n".format(der_hex))
print("SHA256(DER):\n{}\n".format(hashlib.sha256(der).hexdigest()))
print("SHA256(DER_HEX):\n{}\n".format(hashlib.sha256(der_hex).hexdigest()))
```

## Getting flag:

v1 and v3 scripts produce the same output (v2 prints only private key in pem format):

![alt text](img/blackvs.03.png "")

(you can find it in "*Ployka PWNer\scripts\blackvs\v1\results.txt*" )

For convinience script produces SHA256(DER_HEX) also - but if you with you can manually convert private key using [CyberChef link](http://tiny.cc/nnc-sha-sk) from [KeyRecovery](https://spynet.techmaker.ua/KeyRecovery) page:

![alt text](img/blackvs.04.png "")

Next just go to [the second CyberChef ](http://tiny.cc/nnc-sha-result) link from [KeyRecovery](https://spynet.techmaker.ua/KeyRecovery) page and put DeviceID and found hash into it:

![alt text](img/blackvs.05.png "")

Resulted hash put into the RecoveryPage:

![alt text](img/blackvs.06.png "")

![alt text](img/blackvs.07.png "")

![alt text](img/blackvs.09.png "")

![alt text](img/blackvs.10.png "")




### File: CTFs/NNC2019/Side Blennel/blackvs.md

# Side Blennel

Let's check *version* command output:

![alt text](img/blackvs.07.png "Version")

We see that device supports Wi-Fi/Bluetooth/BLE.
Also task name little bit sound strange (no 'blennel' found in the Webster dictionary). 

Side Blennel... BLEnnel? Side BLE?

Hm. let's check using mobile phone:

![alt text](img/blackvs.00.jpg "BLE step 0")

Yep, our device is discoverable - we see NNC 0xc06dd4 device that makes me think that it is my Badge - my badge has DeviceID: 1808b9**c06dd4**.

Good, and ... what is it? Description of device is changing! :

![alt text](img/blackvs.01.jpg "BLE step 1")

![alt text](img/blackvs.02.jpg "BLE step 2")

Due to description is changing suddenly let's make screenshot and analyze them. 
Below cropped screenshots:

![alt text](img/blackvs.11.jpg "Base64 1") ![alt text](img/blackvs.12.jpg "Base64 2")

Looks like two parts of Base64.
Let's try to decode and check results.

It is very simple - just write seing symbols and... hm, used in device font confusing me in:
* O - 0 (zero) or 'O' (ou) symbol?
* l - lowercase 'L' or uppercase 'I'?

Ok, O (ou) and 0 (zero) can be easily distinguished by width - "zero" thinner, "O" - thicker. Good.
But 'I' and 'l' really looks similar.
One way to solve this is switch mobile theme to use other font to make this symbols look different.


Ok, I don't wish to play with mobile themes. I will try to somehow solve this else.

Let's our code will be:

> ZmxhZ3s4ODYzZDBiZWQ5NzFhNjdjMDMyNTBkNzJjYTI5fQ==

[Base64 decode](https://www.base64decode.org/)r gives result:

> flag{8863d0bed971a67c03250d72ca29}

Let's verify it:

![alt text](img/blackvs.09.png "Version")

Now we can relax:

![alt text](img/blackvs.10.jpg "Version")


# **BUT!!!**

Let's imagine we have the next code:

![alt text](img/blackvs.03.jpg "Code 2, part 1")
![alt text](img/blackvs.04.jpg "Code 2, part 2")

It seems to be equal to:

> ZmxhZ3tINTkxZjQ5M2M0ZDI2N2E0Y2FIMmNjZjkzYTA3fQ==

and correspondent flag is:

> flag{H591f493c4d267a4caH2ccf93a07} 

But flag is not recognized by badge as valid. Why? It seems to be flag should be in format:
flag{XXX} where XXX are lowercase hex symbols.
But our one contains two non-hex symbols 'H': 

> flag{**H**591f493c4d267a4ca**H**2ccf93a07}

I.e. it seems to be we confuse somewhere I and l.
Let's check our code and mark confusing symbols:

> ZmxhZ3t**I**NTkxZjQ5M2M0ZD**I**2N2E0Y2F**I**MmNjZjkzYTA3fQ==

I.e. 3 symbols.
Totally 2x2x2=8 possible combinations.
Now we may just generate all 8 combinations and corresponding possible flags:

![alt text](img/blackvs.08.png "Brutflags")

Let's check found flag:

> flag{e591f493c4d267a4cae2ccf93a07}

![alt text](img/blackvs.13.jpg "Full success")

