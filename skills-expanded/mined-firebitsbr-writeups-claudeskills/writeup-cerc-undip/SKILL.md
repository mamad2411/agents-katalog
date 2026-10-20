<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-cerc-undip
description: CTF writeups and security challenges by cerc-undip.
---

# Writeups by cerc-undip

Source repository: `/repos/cerc-undip`

## Repository Index

- CTF-Learn-Writeup/README.md
- CTF-Learn-Writeup/basic_injection_COMPLETE/README.md
- CTF-Learn-Writeup/basic_rot_13_COMPLETE/README.md
- CTF-Learn-Writeup/binwalk_COMPLETE/README.md
- CTF-Learn-Writeup/c_e_er_COMPLETE/README.md
- CTF-Learn-Writeup/charater_encoding_COMPLETE/README.md
- CTF-Learn-Writeup/chop_the_tree_COMPLETE/README.md
- CTF-Learn-Writeup/crack_me_COMPLETE/README.md
- CTF-Learn-Writeup/cryptaz_COMPLETE/README.md
- CTF-Learn-Writeup/dont_bump_your_header_COMPLETE/README.md
- CTF-Learn-Writeup/double_encryption_COMPLETE/README.md
- CTF-Learn-Writeup/esrom_leumas_COMPLETE/README.md
- CTF-Learn-Writeup/exhpltoimtilng_COMPLETE/README.md
- CTF-Learn-Writeup/exif_COMPLETE/README.md
- CTF-Learn-Writeup/forensic_101_COMPLETE/README.md
- CTF-Learn-Writeup/git_is_good_COMPLETE/README.md
- CTF-Learn-Writeup/hat_on_my_head_COMPLETE/README.md
- CTF-Learn-Writeup/i_heard_ROT13_COMPLETE/README.md
- CTF-Learn-Writeup/md5_COMPLETE/README.md
- CTF-Learn-Writeup/milk_best_friend_COMPLETE/README.md
- CTF-Learn-Writeup/name_COMPLETE/README.md
- CTF-Learn-Writeup/photo_analysis_COMPLETE/README.md
- CTF-Learn-Writeup/post_practice_COMPLETE/README.md
- CTF-Learn-Writeup/privacy_matters_COMPLETE/README.md
- CTF-Learn-Writeup/pumpkin_carving_COMPLETE/README.md
- CTF-Learn-Writeup/qr_code_COMPLETE/README.md
- CTF-Learn-Writeup/qr_code_v2_COMPLETE/README.md
- CTF-Learn-Writeup/reversal_of_fortune_COMPLETE/README.md
- CTF-Learn-Writeup/reverse_polarity_COMPLETE/README.md
- CTF-Learn-Writeup/simple_image_COMPLETE/README.md
- CTF-Learn-Writeup/so_many_64_COMPLETE/README.md
- CTF-Learn-Writeup/solve_this_111_COMPLETE/README.md
- CTF-Learn-Writeup/taking_ls_COMPLETE/README.md
- CTF-Learn-Writeup/up_for_a_little_challenge_COMPLETE/README.md
- CTF-Learn-Writeup/whats_your_fav_num_alpha_COMPLETE/README.md
- CTF-Learn-Writeup/where_can_my_robot_go_COMPLETE/README.md

## Writeup Content


### File: CTF-Learn-Writeup/README.md

# CTF Learn Writeup
> Made by Computer Engineering Research Club
> Diponegoro University
> Semarang, Indonesia

---

### Dibuat untuk tujuan pembelajaran dan clue.
> Usahakan untuk mengerjakan sebisanya sebelum melihat writeup.

---

## Tools Key
* Web Exploitation
  * **cURL**
  * Python `requests` library
  * SQL Injection
  * bruteforce
* Forensic
  * `file`
  * `strings`
  * `exiftool`
  * `binwalk`
  * `foremost`
* Cryptography
  * **Bash scripting**
  * **Base64**
  * ROT13
  * Caesar Cipher
  * Python Programing Basic
  * Hex to decimal, decimal to char, char to decimal, binary to decimal
  * Array and/or lists
  * Loop
* Miscellaneous
  * **Imagination**
* Programming
  * Python Programming
  * Loop
  * If-else



### File: CTF-Learn-Writeup/basic_injection_COMPLETE/README.md

# Basic Injection
**Category:** web

See if you can leak the whole database. [https://web.ctflearn.com/web4/](https://web.ctflearn.com/web4/)

## Write-up
Web dengan input seperti ini dapat diselesaikan dengan SQL Injection dasar.
Kebanyakan challenge CTF kategori web dibuat dengan bahasa pemrograman PHP. Input dari form bisa diasumsikan dengan berbagai macam bentuk

```php
$input = "SELECT * FROM user WHERE name = '". $_POST['input'] ."'";
```
atau
```php
$input = 'SELECT * FROM user WHERE name = "'. $_POST['input'] .'"';
```

Perhatikan bahwa input dari user (`$_POST['input']) tidak dilakukan filtering maupun validasi. Dalam kasus seperti ini form sangat mudah untuk di-inject menggunakan syntax SQL biasa.

Kita coba inject input dengan syntax berikut
```
' OR '1' = '1

// atau

" OR "1" = "1
```
Saya sertakan 2 contoh karena terkadang program bisa menggunakan bentuk yang pertama maupun kedua.
Dengan kode injection diatas akan membuat variabel `$input` menjadi:
```
$input = "SELECT * FROM user WHERE name = '' OR '1' = '1';
```

Kode diatas akan dieksekusi di DBMS (_Database Management System_) dan akan selalu menghasilkan nilai TRUE, yang artinya semua record/data yang ada di dalam tabel user akan ditampilkan.

Setelah disubmit, halaman web akan menampilkan semua data yang ada di dalam table `user`. Data dengan Name fl4g__giv3r memiliki flag yang kita cari.

Flag : `th4t_is_why_you_n33d_to_sanitiz3_inputs`



### File: CTF-Learn-Writeup/basic_rot_13_COMPLETE/README.md

# Basic ROT 13
**Category:** cryptography
> Possibly the easiest ever. plore{TrgFuvsgl13}
---

Untuk menyelesaikan challenge ini kita perlu apa itu enkripsi ROT 13. Kalian bisa [baca disini](http://datagenetics.com/blog/july42015/index.html).

Kita akan gunakan command `tr` untuk mentranslasikan setiap huruf sebanyak 13 kali.
```bash
echo plore{TrgFuvsgl13} | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```
```
A-Za-z       akan menjadi ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
N-ZA-Mn-za-m akan menjadi NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm
```

![ROT 13](http://datagenetics.com/blog/july42015/big.png "sumber: datagenetics.com")

Setelah perintah diatas dieksekusi maka kita akan mendapatkan flag yang diinginkan.

flag : `cyber{GetShifty13}`


### File: CTF-Learn-Writeup/binwalk_COMPLETE/README.md

# Binwalk
**Category:** forensic
```
https://mega.nz/#!4UEnAZKT!-deNdQJxsQS8bTSMxeUOtpEclCI-zpK7tbJiKV0tXYY
```
---

Pada challenge Binwalk ini kita tidak diberikan clue sama sekali, melainkan hanya judul dan alamat file untuk didownload

Kita buka file gambar yang baru saja didownload
```
eog PurpleThing.jpeg
```

Ketika membuka file, kita mendapatkan error. Hal ini terjadi kemungkinan karena gambar sudah disisipi file yang lain (atau:_Steganografi_).

Kita akan lihat string yang ada di dalam file ini dan jenisnya.
```
strings PurpleThing.jpeg
file PurpleThing.jpeg
```

Perintah `strings` tidak menghasilkan data yang kita inginkan.

Dengan perintah `file` kita tahu bahwa sebenarnya file `PurpleThing.jpeg` bukanlah jenis file **JPEG** melainkan file **PNG**. Maka kita ubah ekstensinya menjadi `.png`.
```
mv PurpleThing.jpeg PurpleThing.png
```

setelah itu kita cek apakah file `PurpleThing.png` _corrupt_ atau tidak dengan menggunakan perinah `pngcheck`. Jika belum menginstall maka bisa gunakan perintah `sudo apt-get install pngcheck`.
```
pngcheck PurpleThing.png
```

Setelah dieksekusi ternyata file `PurpleThing.png` corrupt
```
PurpleThing.png  additional data after IEND chunk
ERROR: PurpleThing.png
```

Untuk melakukan _recovering_ kita gunakan perintah `foremost`. Jika belum menginstall bisa gunakan perintah `sudo apt-get install foremost`.
```
foremost PurpleThing.png -v
```
* `-v`: menampilkan urutan eksekusi, sehingga kita bisa lihat berapa file yang di-recover (_verbose_)

```
...
File: PurpleThing.png
Start: Sat Jan 34 22:31:28 2500
Length: 160 KB (164802 bytes)
 
Num  Name (bs=512)         Size  File Offset   Comment 

0:  00000000.png       149 KB             0     (780 x 720)
1:  00000299.png        11 KB        153493     (802 x 118)
*|
...
```

Setelah _recovering_ terdapat 1 folder `output` dan 2 file baru, satu file PurpleThing asli, dan satunya lagi adalah file gambar dengan format `.png` yang tersisip di dalam gambar `PurpleThing.png`.
* `00000000.png` merupakan file asli
* `00000299.png` merupakan file yang tersisip

```
cd output/png
eog 00000299.png
```
flag : `ABCTF{B1nw4lk_is_us3ful}`


### File: CTF-Learn-Writeup/c_e_er_COMPLETE/README.md

# C_e_er
**Category:** cryptography
> I got a message from a Roman General who liked the number 13 and he liked keys.
> This is the message:
> xwfsutyfxwsubvrohirbjvehojbrveoljrbvjrbivlojrbevhipojrbviuobvurosibjvrhsuoibjrvshiouljrbhsioujrbsiluorjsbihjrlosynt{PnrfneVfAbgFrpher}jbr;hsucjrvhucjrvhujrbvsiljrvbhujvbfqywyfxwiusc2vheucrhsucjvrhucjrvhtsbjrvltjrbevltjrheltjrheltjrbhltbjhrletsbhjrletjhrlestjrvhstrjvehsltjrehvljtvhltvhjlt
---

Pada challenge ini kita diminta untuk mendekripsi pesan yang disediakan dan menemukan flag-nya.

Ada beberapa clue untuk menyelesaikan challenge ini, yaitu:
* Dari judul "C_e_er"
* Kata "Roman"
* Kata "who liked the number 13"

Dari sini kita dapat simpulkan bahwa algoritma yang dipakai untuk mengenkripsi pesan ini adalah Caesar dengan rotasi sebanyak 13 kali. Jika belum paham apa itu **Caesar** dan **ROT 13** silahkan [baca disini](http://datagenetics.com/blog/july42015/index.html).

Simpan pesan rahasia kedalam file bernama `quest.txt` agar kita bisa dengan mudah untuk memprosesnya.

```bash
echo xwfsutyfxwsubvrohirbjvehojbrveoljrbvjrbivlojrbevhipojrbviuobvurosibjvrhsuoibjrvshiouljrbhsioujrbsiluorjsbihjrlosynt{PnrfneVfAbgFrpher}jbr;hsucjrvhucjrvhujrbvsiljrvbhujvbfqywyfxwiusc2vheucrhsucjvrhucjrvhtsbjrvltjrbevltjrheltjrheltjrbhltbjhrletsbhjrletjhrlestjrvhstrjvehsltjrehvljtvhltvhjlt > quest.txt
```

Selanjutnya mari kita dekripsi pesan tersebut dengan perintah `tr` untuk mentranslasikan setiap huruf.
```bash
cat quest.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

> Jika belum paham dengan _command_ diatas maka silahkan lihat writeup challenge [Basic ROT 13](https://github.com/cerc-undip/CTF-Learn-Writeup/tree/update/basic_rot_13_COMPLETE).

Setelah dieksekusi maka kita akan melihat kumpulan kata acak tanpa spasi. Namun di bagian tengah terdapat flag yang kita cari.

flag : `flag{CaesarIsNotSecure}`


### File: CTF-Learn-Writeup/charater_encoding_COMPLETE/README.md

# Character Encoding
**Categori:** cryptography
> In the computing industry, standards are established to facilitate information interchanges among American coders. Unfortunately, I've made communication a little bit more difficult. Can you figure this one out? 41 42 43 54 46 7B 34 35 43 31 31 5F 31 35 5F 55 35 33 46 55 4C 7D
---

Pada challenge ini kita diminta untuk men-_decode_ karakter yang tertera. Namun sebelum bisa men-_decode_ kita perlu tahu teknik _decoding_ apa yang dipakai di dalam soal.

Kita melihat susunan karakter `41 42 43 54 46 7B ...` dimana hanya terdapat angka dan huruf yang terdiri dari A sampai F saja. Ini merupakan encoding karakter **ASCII**. Untuk menyelesaikannya kita gunakan bahasa pemrograman Python.

```
touch script.py
chmod +x script.py
```

Buka file `script.py` menggunakan text editor.

```
#!/usr/bin/python3

soal = "41 42 43 54 46 7B 34 35 43 31 31 5F 31 35 5F 55 35 33 46 55 4C 7D"
soal = soal.split(" ")
hasil = ""

for i in soal:
  temp = int(i, 16)
  hasil += chr(temp)

print(hasil)
```

* `soal = soal.split(" ")`: memasukkan setiap karakter yang dipisahkan dengan spasi kedalam variabel soal. Tipe data soal sekarang adalah _list_ (_array_ dalam bahasa pemrograman lain)
* `for i in soal:`: akan mengakses setiap nilai di variabel soal dan memasukkannya kedalam variabel `i`
* `int(i, 16)`: konversi dari _hex_ ke _integer_
* `chr(temp)`: konversi dari _integer_ ke _character_

Setelah program dijalankan. Gotcha! kita dapat flag-nya.

flag : `ABCTF{45C11_15_U53FUL}`


### File: CTF-Learn-Writeup/chop_the_tree_COMPLETE/README.md

# Chop the Three
**Category:** cryptography
> i'm a lumberjack. i just need to swing my axe to make the three fall. can you do it too?
> d2FvLCBhbG1vc3QgdGhlcmUNClpHOXVKM1FnZDI5eWNua3NJSE52YjI0TkNscHRlR2hhTTNSd1pFWTVjR014T1hwaU1UbHNXVmhPTldaUlBUMD0=
---

Pada challenge ini kita diminta untuk melakukan decoding terhadap pesan dalam bentuk Base64. Bentuk Base64 dapat dengan mudah dikenali dengan tanda "sama dengan" (`=`) di akhir. ([Baca disini](https://en.wikipedia.org/wiki/Base64))

Langsung saja kita _decode_ pesan tersebut menggunakan bash.
```bash
echo d2FvLCBhbG1vc3QgdGhlcmUNClpHOXVKM1FnZDI5eWNua3NJSE52YjI0TkNscHRlR2hhTTNSd1pFWTVjR014T1hwaU1UbHNXVmhPTldaUlBUMD0= | base64 -d
```

> wao, almost there
> ZG9uJ3Qgd29ycnksIHNvb24NClpteGhaM3RwZEY5cGMxOXpiMTlsWVhONWZRPT0=

Setelah di-_decode_ ternyata pesan ini masih memiliki pesan dalam bentuk Base64 dan terdapat pesan lain sebelumnya.

Dari kata "Three" di judul kita bisa mengetahui bahwa kemungkinan pesan rahasia ini di-_encode_ sebanyak 3 kali. Jadi, kita tidak perlu membuat script panjang seperti pada challenge [So many 64s](https://github.com/cerc-undip/CTF-Learn-Writeup/tree/master/so_many_64_COMPLETE).

Paste hasil _decoding_ sebelumnya dan _decode_ lagi sampai flag-nya ketemu.
```bash
echo ZG9uJ3Qgd29ycnksIHNvb24NClpteGhaM3RwZEY5cGMxOXpiMTlsWVhONWZRPT0= | base64 -d
echo ZmxhZ3tpdF9pc19zb19lYXN5fQ== | base64 -d
```

Setelah dilakukan _decoding_ sebanyak 3 kali maka kita dapatkan flag yang kita cari. Yoyoy.

flag : `flag{it_is_so_easy}`


### File: CTF-Learn-Writeup/crack_me_COMPLETE/README.md

# Crack Me
**Category:** binary exploitation
> I forgot the secret code to my program can you help me find it?
> https://mega.nz/#!x2xwQS7S!-Id_VR5BDMQv3MEVo89zxA51LWlkQQHy8r7WBBN45CI
---

Challenge kali ini berkategori **Binary Exploitation** yang artinya kita perlu melakukan teknik _reverse engineering_ terhadap program agar kita mendapatkan informasi yang kita inginkan. ([Baca disini](https://en.wikipedia.org/wiki/Reverse_engineering))

Namun dalam menyelesaikan challenge **Crack Me** kita tidak perlu melakukan **reverse engineering** terhadap program melainkan kita bisa menyelesaikannya seperti pada challenge berkategori **Forensic**.

Download file dan lihat jenis file-nya
```bash
$ file crackme.exe
crackme.exe: PE32 executable (console) Intel 80386, for MS Windows
```

Dari sini kita tahu bahwa format file ini adalah **PE32** yang bisa dijalankan melalui sistem console Windows. Tentu kita tidak perlu menjalankannya melalui OS Windows. Mari kita lihat informasi string yang ada di dalamnya.
```bash
strings crackme.exe | more
```

Ketika kita _scroll_ informasi string kita dapat melihat beberapa kalimat yang akan ditampilkan oleh program ketika dijalankan. Namun ada sebuah string berawalan `flag` yang dimana itu adalah flag yang kita cari.

flag : `flag{h4ck3rm3n_4ss3mbl3}`


### File: CTF-Learn-Writeup/cryptaz_COMPLETE/README.md

# Crack Me
**Category:** cryptography
> If A=Z, B=Y..., then what is:
> XGU{Rmhvxfiv=Vzhb}
---

Challenge Cryptaz ini sudah memberikan algoritma yang dipakai untuk merahasiakan pesannya. Jika kita lihat lagi bahwa algoritma yang dipakai ini adalah algoritma yang pernah dipakai pada saat kita mengikuti Pramuka, yaitu sandi A-Z. Keren kan? Wkwkwk

![Sandi A-Z](https://aboutpramuka.files.wordpress.com/2015/12/sandi-abjad-az.jpg "sumber: aboutpramuka.wordpress.com")

Untuk menyelesaikan challenge ini kita cukup mentranslasikannya saja dengan perintah `tr`. Jika ingin lebih paham bisa baca manualnya `man tr`.
```bash
echo XGU{Rmhvxfiv=Vzhb} | tr 'A-Za-z' 'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba'
```
* Penulisan huruf dari A sampai dengan Z dan a sampai dengan z bisa ditulis dengan `A-Za-z`.
* Namun untuk sebaliknya tidak bisa dilakukan, maka ditulis secara manual.

flag : `CTF{Insecure=Easy}`


### File: CTF-Learn-Writeup/dont_bump_your_header_COMPLETE/README.md

# Don't Bump Your Head(er)
**Category:** web
```
Try to bypass my security measure on this site! https://ctflearn.com/header.php
```
---

Untuk menyelesaikan challenge ini kita akan menggunakan bahasa pemrograman Python (_versi 3.x). Jika belum menginstal bisa gunakan perintah `sudo apt-get install python3`.

Challenge ini juga bisa diselesaikan dengan menginstall _Chrome Extension_ bernama **Modify Headers**

Kita akan menuliskan script yang akan dijalankan oleh terminal. Buat file bernama `script.py` dan ubah aksesnya menjadi _executable file_.
```
touch script.py
chmod +x script.py
```

Kemudian kita tulis program menggunakan _text editor_. (Bisa menggunakan **gedit**, **sublime**, **atom**, **vim**, **vi**, dsb)
```
#!/usr/bin/python3
import requests
re = requests.get('https://ctflearn.com/header.php')
print(re.text)

```

* `#!/usr/bin/python3`: terminal akan menjalankan program dengan python3. [Baca disini](https://stackoverflow.com/questions/7670303/purpose-of-usr-bin-python3).
* `import requests`: library untuk melakukan _HTTP Request_.
* `re = requests.get('https://ctflearn.com/header.php')`: melakukan request ke url dengan method HTTP GET.
* `print(re.text)`: menampilkan _response_ dari request yang telah dikirim

> Library requests sangat berguna untuk menyelesaikan setiap challenge dengan kategori **web**

Simpan dan eksekusi file tersebut dengan perintah `./script.py`.

Saat dieksekusi, response yang akan diterima adalah bahwa request yang dikirimkan ditolak karena `user agent is not correct`.

Setelah itu terdapat string/kata yang kemungkinan besar bisa kita gunakan untuk inject header selanjutnya.

```
Sorry, it seems as if your user agent is not correct, in order to access this website. The one you supplied is: python-requests/2.9.1
<!-- Sup3rS3cr3tAg3nt  -->
```
Masalah disini dapat kita selesaikan dengan mengirimkan _custom header_ yang kita inginkan, yaitu dengan mengganti header `User-Agent` dengan `Sup3rS3cr3tAg3nt`. [Pelajari tentang Header](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)

```
#!/usr/bin/python3
import requests
re = requests.get('https://ctflearn.com/header.php', headers={'user-agent': 'Sup3rS3cr3tAg3nt'})
print(re.text)
```
Ketika dieksekusi muncul pemberitahuan baru yang menyertakan link `awesomesauce.com`.

Solusi di langkah ini bukanlah mengunjungi website tersebut melainkan kita mengirimkan _custom header_ tambahan lagi yang bernama [Referer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer)

```
#!/usr/bin/python3
import requests
re = requests.get('https://ctflearn.com/header.php', headers={'user-agent': 'Sup3rS3cr3tAg3nt', 'referer': 'awesomesauce.com'})
print(re.text)
```

Gotcha!! Kita dapat flagnya!

flag : `flag{did_this_m3ss_with_y0ur_h34d}`


### File: CTF-Learn-Writeup/double_encryption_COMPLETE/README.md

# Double Encryption
**Category:** cryptography
> 0101101001101101011110000110100001011010001100110111010000110101011000100011001101010101011011100110001101101101010101010110011101011001010100110100001001101010011000100011001000111001011100110100100101000111010100100011000101011010010001110101011000111001

> Good Luck
---

Untuk menyelesaikan ini kita perlu mengubah bentuk biner tersebut menjadi karakter/teks. Kita bisa akan selesaikan challenge ini menggunakan bahasa pemrograman Python, atau jika ingin cepat bisa gunakan [Binary to Text online](https://www.rapidtables.com/convert/number/binary-to-ascii.html).

Oke, kita buat file `script.py` dan ubah menjadi _executable_, kemudian buka filenya.
```bash
touch script.py
chmod +x script.py
```

Untuk pertama kita membuat 2 variabel: `soal` untuk menyimpan pesan biner dan `hasil_temp` untuk menyimpan setiap 8 bit pesan kedalam list/array.

```python
#!/usr/bin/python3
soal = "0101101001101101011110000110100001011010001100110111010000110101011000100011001101010101011011100110001101101101010101010110011101011001010100110100001001101010011000100011001000111001011100110100100101000111010100100011000101011010010001110101011000111001"
hasil_temp = []

for i in range(len(soal) // 8):
  hasil_temp.append(soal[:8])
  soal = soal[8:]

print(hasil)
```

Selanjutnya kita ubah tiap 8 bit tersebut menjadi karakter ASCII.

| Dari | Menjadi | Perintah |
|---|---|---|
| biner  | desimal | int(var_biner, 2) |
| desimal| ASCII   | chr(var_desimal)  |


```python
#!/usr/bin/python3
soal = "0101101001101101011110000110100001011010001100110111010000110101011000100011001101010101011011100110001101101101010101010110011101011001010100110100001001101010011000100011001000111001011100110100100101000111010100100011000101011010010001110101011000111001"
hasil_temp = []

for i in range(len(soal) // 8):
  hasil_temp.append(soal[:8])
  soal = soal[8:]

hasil = ""

for j in range(len(hasil_temp)):
  temp = chr(int(hasil_temp[j], 2))
  hasil += temp

print(hasil)
```

Setelah dijalankan, ternyata pesan biner ini menghasilkan pesan lain dalam bentuk Base64. Selanjutnya kita akan _decode_ pesan ini menggunakan library python `base64`. Jika belum terinstal bisa gunakan `sudo pip install base64` atau `sudo pip3 install base64`.

```python
#!/usr/bin/python3
import base64

soal = "0101101001101101011110000110100001011010001100110111010000110101011000100011001101010101011011100110001101101101010101010110011101011001010100110100001001101010011000100011001000111001011100110100100101000111010100100011000101011010010001110101011000111001"

hasil_temp = []

for i in range(len(soal) // 8):
  hasil_temp.append(soal[:8])
  soal = soal[8:]

hasil = ""

for j in range(len(hasil_temp)):
  temp = chr(int(hasil_temp[j], 2))
  hasil += temp

hasilAkhir = base64.b64decode(hasil).decode('utf-8')
print(hasilAkhir)
```

Terakhir, jalankan program tersebut `./script.py` dan kita akan mendapatkan flag yang kita inginkan.

flag : `flag{you're a cool dude}`


### File: CTF-Learn-Writeup/esrom_leumas_COMPLETE/README.md

# Esrom Leumas
**Category:** cryptography
> I got a message from Esrom Leumas:
> ..-. .-.. .- --. ... .- -- ..- . .-.. -- --- .-. ... . .. ... -.-. --- --- .-.. -... -.-- - .... . .-- .- -.-- .. .-.. .. -.- . -.-. .... . . ... .
> The flag has format: flag{FourWordsInCamelCase}
---

Kata kunci untuk menyelesaikan challenge ini adalah pada judulnya "Esrom Leumas". Jika dibalik, kata ini berarti "Samuel Morse". Oke, kita kembali lagi ke masa Pramuka untuk menyelesaikan challenge ini.

Kita bisa gunakan bahasa pemrograman Python atau jika ingin cepat bisa gunakan [Morse Code Translator Online](https://morsecode.scphillips.com/translator.html?utm_source=hootsuite).

Mari kita buat file `script.py` dan ubah menjadi _executable_, kemudian buka file tersebut.
```bash
touch script.py
chmod +x script.py
```

```python
#!/usr/bin/python3
soal = "..-. .-.. .- --. ... .- -- ..- . .-.. -- --- .-. ... . .. ... -.-. --- --- .-.. -... -.-- - .... . .-- .- -.-- .. .-.. .. -.- . -.-. .... . . ... ."

hasil = soal.split(" ")
print(hasil)
```

Dengan program diatas, kita masukkan tiap kode yang dipisahkan dengan spasi kedalam variabel `hasil`.

Pasangan antara kode morse dengan huruf kita gunakan tipe data `dictionary` dari Python.
```python
#!/usr/bin/python3
soal = "..-. .-.. .- --. ... .- -- ..- . .-.. -- --- .-. ... . .. ... -.-. --- --- .-.. -... -.-- - .... . .-- .- -.-- .. .-.. .. -.- . -.-. .... . . ... ."

sandi = {
  ".-": "A",
  "-...": "B",
  "-.-.": "C",
  "-..": "D",
  ".": "E",
  "..-.": "F",
  "--.": "G",
  "....": "H",
  "..": "I",
  ".---": "J",
  "-.-": "K",
  ".-..": "L",
  "--": "M",
  "-.": "N",
  "---": "O",
  ".--.": "P",
  "--.-": "Q",
  ".-.": "R",
  "...": "S",
  "-": "T",
  "..-": "U",
  "...-": "V",
  ".--": "W",
  "-..-": "X",
  "-.--": "Y",
  "--..": "Z"
}

hasil = soal.split(" ")

decoded = []
for j in range(len(hasil)):
  decoded.append(sandi[hasil[j]])

print("".join(decode))
```

Program diatas akan otomatis mengakses setiap kode di variabel `hasil` dan mencocokkan dengan _dictionary_ di variabel `sandi`. Hasil dari pencocokkan tersebut dimasukkan kedalam list/array decoded. Terakhir kita tampilkan hasil penggabungan kata di dalam variabel `decoded`.

Kalian bisa kontribusi perbaiki kode **Morse Decoder** diatas di [repository ini](https://github.com/fannyhasbi/morse-decoder).

Perhatikan bahwa format flag-nya adalah **flag{FourWordsInCamelCase}**.

flag : `flag{SamuelMorseIsCool}`



### File: CTF-Learn-Writeup/exhpltoimtilng_COMPLETE/README.md

# exHplToiMtiLng
**Category:** miscellaneous
> What is li123456789fe?
> 
> Ignore that nonsense ^
> 
> https://mega.nz/#!9ZsDFbYL!y8agy4iFlDq-MX5CCDf5fuUcwyFUOSy3A3aSLFzqXnk
---

Oke, no intro langsung saja download file-nya dan coba buka file tersebut.
```bash
eog 1234568-doesn\'t-that-bother-you.jpg
```

Saat membuka gambar kita akan mendapatkan error. Kemungkinan jenis file ini berbeda dari yang terlihat atau bahkan telah dilakukan teknik _steganografi_.

Saat kita melihat jenis file tersebut dengan perintah `file` kita tahu bahwa itu bukanlah file gambar, melainkan adalah dokumen HTML.

Selanjutnya kita ubah file tersebut menjadi `quest.html`.
```
$ file 1234568-doesn\'t-that-bother-you.jpg
1234568-doesn't-that-bother-you.jpg: HTML document, UTF-8 Unicode text, with very long lines
$ mv 1234568-doesn't-that-bother-you.jpg quest.html
```

Buka `quest.html` dengan text editor. Perhatikan disana ada flag yang kita cari. Bisa dicari dengan Ctrl+F atau jika menggunakan terminal gunakan perintah:
```bash
cat quest.html | grep -i ctf{
```

flag : `CTF{HTML=fun}`


### File: CTF-Learn-Writeup/exif_COMPLETE/README.md

# Exif
**Category:** forensic
> If only the password were in the image?
> https://mega.nz/#!QDZGiLSZ!fkkhBJuBBtBKGsLTDiF2NuLihP2WRd97Iynd3PhWqRw
> 
> You could really "own" it with exif
---

Pada challenge ini kita diminta untuk mencari flag dari gambar yang disediakan. Di judul juga sudah diberikan clue untuk menggunakan Exif (Exchangeable Image File). ([Baca disini](https://en.wikipedia.org/wiki/Exif)).

> Exif cukup sering digunakan untuk mencari informasi di dalam file gambar

Oke, kita akan melihat informasi EXIF ini di terminal dengan perintah `exiftool`. Jika belum menginstal silahkan gunakan `sudo apt-get install exiftool`.
```bash
exiftool Computer-Password-Security-Hacker\ -\ Copy.jpg | more
```

Dengan perintah diatas kita dapat mengetahui semua informasi EXIF yang ada di dalam gambar ini. Pada baris `Owner Name` terdapat flag yang kita cari.

flag : `flag{3l1t3_3x1f_4uth0r1ty_dud3br0}`


### File: CTF-Learn-Writeup/forensic_101_COMPLETE/README.md

# Forensic 101
**Category:** forensic

Untuk menyelesaikan challenge bertipe **forensic** awali dengan cek tipe file dan strings, karena dari sini bisa saja terdapat informasi yang dapat digunakan untuk menemukan clue selanjutnya.

Cek file menggunakan terminal
```
file pic.jpg
```

Dari perintah diatas ternyata file tersebut merupakan file berjenis `JPEG Image`. Dalam kasus lain gambar bisa berjenis `ZIP`, `TAR.GZ`, `RAR`, maupun yang lain
```
pic.jpg: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 236x218, frames 3
```

Jika file dibuka tidak akan didapat informasi yang penting. Hanya terdapat gambar minion dan tulisan yang tidak berkaitan dengan challenge
```
eog pic.jpg
```
![](./pic.jpg)

> Hal terpenting ketika menyelesaikan challenge bertipe `forensic`
> dengan mengecek kata-kata yang ada di dalam file tersebut

```
strings pic.jpg
```
Dari perintah diatas kita dapatkan kata-kata yang acak. Namun pada bagian terakhir ada string yang dapat dibaca, dan itu merupakan flag-nya.
```
...
X`( 
8kF=
~9%]Tn
flag{wow!_data_is_cool}
$lqU
AG{u
Xm*CnC
@'hnQ
ax+p
bdQG
D_ O
```

flag `flag{wow!_data_is_cool}`


### File: CTF-Learn-Writeup/git_is_good_COMPLETE/README.md

# Git is Good
**Category:** forensic

> The flag used to be there. But then I redacted it. Good Luck. https://mega.nz/#!C483DAYB!Jjr55hfJQJ5-jspnyrnVtqBkMHGJrd6Nn_QqM7iXEuc
---

Pada judul sudah terpampang dengan jelas apa yang akan kita lakukan di challenge ini, yaitu menggunakan **git**. Jika belum menginstal silahkan download dan install git [disini](https://git-scm.com/downloads)

_Extract_ file yang baru kita download. Setelah itu akan muncul semua informasi file apa saja yang di-_extract_
```
unzip gitIsGood.zip
cd gitIsGood
ls -la
```

Ketika masuk ke folder `gitIsGood` disitu terdapat 1 file `flag.txt` dan 1 folder `.git` yang menandakan bahwa folder ini adalah _repository_ git. Kita coba baca isi file `flag.txt`.
```
cat flag.txt
```

Ketika `flag.txt` dibaca, ada tulisan flag. Tetapi ini bukanlah flag yang kita cari, karena flag tersebut sudah diedit (_redacted_).

Dengan **git** kita bisa melihat _history_ pengeditan pada repository dengan perintah `log`.
```
git log
```

Dari sini kita bisa lihat _history_ pengeditan yang pernah dilakukan serta tanggal dan keterangannya. Dari sini juga kita tahu bahwa file `flag.txt` telah diedit 3 kali.

Untuk melihat detail perubahannya kita bisa menggunakan _option_ `-p` (_patch_).
```
git log -p
```

Gotcha! Kita bisa melihat flag sebelum dilakukan perubahan.

flag : `flag{protect_your_git}`



### File: CTF-Learn-Writeup/hat_on_my_head_COMPLETE/README.md

# Hat on my HEAD
**Category:** forensic
> A Tip of the Hat to anyone who can solve this.
> 
> https://mega.nz/#!lKZ2VaiY!DkGHSZZh6msYsvP_iuHDryQdRO-pd7b6qhbWb_f4noY
---

Pada challenge ini kita diminta untuk mencari flag yang ada di gambar yang sudah disediakan.

Karena file tersebut beresktensi `.png` mari kita cek dulu apakah file ini terdapat _corrupt_ atau tidak.
```bash
pngcheck whitehat.png
```
> whitehat.png:  CORRUPTED by text conversion
> ERROR: whitehat.png

Setelah di-_run_ ternyata file ini _corrupt_. Karena file ini corrupt perlu dilakukan _recovering_. Tetapi sebelum itu kita coba untuk melihat string yang ada pada file ini.
```bash
strings whitehat.png | more
```

Ternyata dengan melihat string kita menemukan flag yang kita cari tanpa melakukan _recovering_ datanya. Tetapi jika kalian ingin mencoba _recovering_ silahkan saja.
```bash
foremost -v whitehat.png
```

Ternyata ketika proses _recovering_ tidak terdapat data apapun didalamnya. Kemungkinan file ini corrupt karena ditambahkan string flag.

flag : `Cyber{M'Lady}`


### File: CTF-Learn-Writeup/i_heard_ROT13_COMPLETE/README.md

# I Heard You Can't ROT13 Numbers
**Category:** cryptography
> I saw this in a file but I can't figure out what it meant: MzkuM3gaMKE0nJ5aK3A0LKW0MJE9
> 
> Can you help?
---

Dari judul kita sudah bisa menebak apa algoritma yang digunakan untuk menyembunyikan pesan rahasianya, yaitu ROT13. Logika dari algoritma enkripsi ini adalah dengan memutar huruf abjad dari A sampai dengan Z sebanyak 13 kali. ([Baca disini](http://datagenetics.com/blog/july42015/index.html))

![ROT 13](http://datagenetics.com/blog/july42015/big.png "sumber: datagenetics.com")

Oke, kita langsung saja perintahkan terminal untuk menyelesaikannya.
```bash
echo MzkuM3gaMKE0nJ5aK3A0LKW0MJE9 | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

> Jika belum paham arti perintah `tr` silahkan baca writeup challenge [Basic ROT 13](https://github.com/cerc-undip/CTF-Learn-Writeup/tree/update/basic_rot_13_COMPLETE).

Setelah kita eksekusi perintahnya, kita menemukan bahwa pesan ini masih dirahasiakan lagi. Namun pesan ini merupakan besan berbentuk Base64 ([Baca disini](https://en.wikipedia.org/wiki/Base64)), maka dari itu kita perlu men-_decode_ pesan ini
```bash
echo MzkuM3gaMKE0nJ5aK3A0LKW0MJE9 | tr 'A-Za-z' 'N-ZA-Mn-za-m' | base64 -d
```

Terakhir, kita akan mendapatkan flag yang kita cari.

flag : `flag{getting_started}`


### File: CTF-Learn-Writeup/md5_COMPLETE/README.md

# MD5
**Category:** cryptography
> MD5 hash practice. does not start with cyber{}
> b0439fae31f8cbba6294af86234d5a28
---

Penyelesaian challenge ini sangat mudah. Kita hanya menggunakan fasilitas MD5 Decrypter Online.

flag : `securepassword`


### File: CTF-Learn-Writeup/milk_best_friend_COMPLETE/README.md

# Milk's Best Friend
**Category:** forensic

> There's nothing I love more than oreos, lions, and winning. https://mega.nz/#!qpFlCTiZ!P8UotyST_6n2iW5BS1yYnum8KnU0-2Amw2nq3UoMq0Y Have Fun :)
---

Pada challenge ini tidak diberikan clue yang membantu sehingga kita perlu mencari sendiri solusi untuk menyelesaikannya.

![Oreo](./oreo.jpg)

> Seperti biasa, setelah mendownload pastikan lihat jenis file dan juga _string_ yang terdapat di dalam file. Karena file gambar bisa saja disisipi file lain (_Steganografi_)

```bash
file oreo.jpg
strings oreo.jpg
```

Dengan command `file` kita tahu bahwa file gambar ini memang benar file gambar berformat **JPEG**. Namun ketika kita eksekusi command `strings` kita hanya melihat kata-kata acak yang bukan kita cari.

Selanjutnya kita coba cari tahu apakah file gambar ini telah dilakukan steganografi atau belum dengan menggunakan perintah `binwalk`. Jika belum menginstal bisa gunakan `sudo apt-get install binwalk`.
```
binwalk oreo.jpg
```

Setelah diteliti ternyata `oreo.jpg` ini telah dilakukan steganografi dan terdapat 1 file berformat RAR.
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
9515          0x252B          RAR archive data, first volume type: MAIN_HEAD
```

Maka dari itu kita _extract_ file tersembunyi itu menggunakan perintah `foremost`.
```bash
foremost -v oreo.jpg
```

Setelah diekstrak terdapat 2 file baru di folder output. 1 file asli oreo sebelum dilakukan steganografi dan 1 nya lagi berekstensi `.rar`.

Kita masuk ke folder tersebut dan _extract_ file yang ada di dalamnya.
```bash
cd output/rar
unrar x 00000018.rar
```

> Jika belum paham dengan perintah ekstraksi bisa [baca disini](https://linux.die.net/man/1/unrar).

Setelah di-_extract_ kita mendapat 1 file teks dan 1 file gambar. Gambar ini hampir sama dengan gambar yang pertama, namun ketika kita lihat _string_ yang ada di dalam gambar maka kita akan menemukan flag-nya.
```bash
cd 1
strings b.jpg
```

flag : `flag{eat_more_oreos}`


### File: CTF-Learn-Writeup/name_COMPLETE/README.md

# Name
**Category:** miscellaneous
> I don't understand, I only see hello at the end
> 
> Flag={reDnAxElA si e*an ym ,u0y llet lli2 I nois*cco laic*ps a si ti sa tub tErces sI emAn ym dn*irf olleH}
> 
> Help me please!!!
---

Pada challenge **Name** kita diminta untuk mencari nama yang ada di dalam pesan "rahasia" yang disediakan.

Untuk menyelesaikan ini kita bisa menggunakan **bash script** maupun bahasa pemrograman **Python**. Namun pada writeup ini akan dijelaskan menggunakan **bash script**. Script **Python** tetap akan disediakan untuk pembelajaran.

Pesan rahasia ini dapat dengan mudah ditebak karena pesan ini hanya dibalik saja. Maka kita akan gunakan _command_ `rev` pada bash.

```bash
echo reDnAxElA si e*an ym ,u0y llet lli2 I nois*cco laic*ps a si ti sa tub tErces sI emAn ym dn*irf olleH | rev
```

Dengan perintah ini kita bisa melihat pesan aslinya, dan pada akhir kalimat kita melihat nama yang dicari (flag).

Perintah ini bisa diubah agar hanya menampilkan namanya saja dengan memotong string.
```bash
echo reDnAxElA si e*an ym ,u0y llet lli2 I nois*cco laic*ps a si ti sa tub tErces sI emAn ym dn*irf olleH | cut -d ' ' -f 1 | rev
```

flag : `AlExAnDer`


### File: CTF-Learn-Writeup/photo_analysis_COMPLETE/README.md

# Photo Analysis
**Category:** miscellaneous
> You can do it, you just gotta belieeeeeeeeeeeeeeeve! 
> 
> I used the same wrap as with all my other problems.
> 
> https://mega.nz/#!MNNAhaSK!IKDHTx9oXNSa4dsn9DG_rwA08yycqc3yC4iFkQY8lvc
---

Pada challenge ini kita diberikan 1 file gambar. Mari kita buka file ini dengan image viewer.
```bash
eog dank\ trump.jpeg
```

Ketika kita lihat, gambar bagian bawah terlihat rusak dan tidak jelas. Kemungkinan gambar ini telah dilakukan _steganografi_. ([Baca disini](https://id.wikipedia.org/wiki/Steganografi))

Selanjutnya kita coba lihat data string yang dapat terlihat di file ini.
```bash
strings dank\ trump.jpeg
```

Gotcha! Di bagian bawah kita bisa menemukan flag yang kita cari.

flag : `CTF{OMG_You_Believed}`


### File: CTF-Learn-Writeup/post_practice_COMPLETE/README.md

# POST Practice
**Categori:** web
```
These website requires authentication, via POST. However, it seems as if someone has defaced our site. Maybe these is still some way to authenticate? https://ctflearn.com/post.php
```
---

Clue dari challenge ini sangat jelas, yaitu mengirimkan request dengan motode `POST`. Pertama, kita cari tahu dahulu isi dari alamat url `https://ctflearn.com/post.php`

Challenge ini dapat diselesaikan dengan `bash script` maupun bahasa pemrograman Python. Namun dalam contoh ini menggunakan `bash script`.
```
curl https://ctflearn.com/post.php
```

Dengan mengeksekusi perintah diatas, kita mengirimkan request dengan method `GET` ke alamat `https://ctflearn.com/post.php`. Response dari web menyertakan _credential_ yang dapat kita gunakan untuk menembus web ini.

Selanjutnya kita mengirim request dengan metode `POST` dengan _credential_ yang sudah kita dapatkan,
```
curl https://ctflearn.com/post.php -d username=admin -d password=71urlkufpsdnlkadsf
```
* `-d username=admin`: mengirim data username dengan nilai `admin`
* `-d password=71urlkufpsdnlkadsf`: mengirim data password dengan nilai `71urlkufpsdnlkadsf`

> Dalam bahasa pemrograman PHP sama saja dengan `$_POST['username'] = "admin"`, `$_POSt['password'] = "71urlkufpsdnlkadsf"`

Setelah perintah dieksekusi maka kita akan mendapatkan flag yang kita cari.

flag : `flag{p0st_d4t4_4ll_d4y}`


### File: CTF-Learn-Writeup/privacy_matters_COMPLETE/README.md

# Privacy Matters
**Category:** programming

> The URL that has the flag got corrupted again... here it is: êööòõ¼±±åñæçòçð°ëñ±ðëåîçø´²±è÷îî±øûÛÓüÉ±
---

Solusi dan langkah penyelesaian challenge ini hampir sama dengan [What's Your Favorite Number of the Alpha](https://github.com/cerc-undip/CTF-Learn-Writeup/tree/update/whats_your_fav_num_alpha_COMPLETE).

Pada challenge ini kita diberikan kumpulan karakter yang tidak bisa dibaca. Untuk memecahkannya kita perlu mengetahui algoritma _encoding_ yang dipakai untuk membuat karakter "_unreadable_" itu.

Clue dari soal yang dapat membantu adalah `The URL that has the flag ...`. Ini berarti kumpulan karakter tersebut adalah kumpulan karakter yang membentuk suatu URL

URL terdiri dari kata `http` atau `https` pada awalnya (Baca [disini](https://en.wikipedia.org/wiki/URL)), sehingga kita bisa mencoba untuk decoding karakter tersebut menggunakan bahasa pemrograman Python. Karena bahasa ini menyediakan konversi dari karakter ASCII ke desimal.

Kita jalankan interpreter Python versi 3.
```bash
python3
```

Kita coba konversi 4 karakter awal dari karakter menjadi desimal.

```python
>>> ord('ê')
234
>>> ord('ö')
246
>>> ord('ö')
246
>>> ord('ò')
242
```

Perhatikan ada 2 kali karakter `ö`. Kemungkinan besar membentuk kata `http` ataupun `https`.

Selanjutnya kita coba konversi karakter `http` menjadi desimal.
```python
>>> ord('h')
104
>>> ord('t')
116
>>> ord('t')
116
>>> ord('p')
112
```

Oke, dari sini kita coba cocokkan algoritmanya.

| Encoded | Desimal(Enc) | Decoded | Desimal(Dec) |
|---------|--------------|---------|--------------|
| ê       | 234          | h       | 104          |
| ö       | 246          | t       | 116          |
| ö       | 246          | t       | 116          |
| ò       | 242          | p       | 112          |

Ternyata proses decodingnya adalah adalah dengan mengurangi 130 dari angka desimal dari ASCII. Atau bisa kita modelkan seperti ini:
> decode(kar) = desimal(kar) - 130

Kita bisa mencoba satu-satu seperti pada contoh sebelumnya. Tetapi agar efisien kita gunakan perulangan pada Python.
```python
>>> soal = "êööòõ¼±±åñæçòçð°ëñ±ðëåîçø´²±è÷îî±øûÛÓüÉ±"
>>> hasil = ""
>>> 
>>> for karakter in soal:
...     temp = ord(karakter) - 130
...     hasil += chr(temp)
... 
>>> print(hasil)
```

Setelah di-_decode_ ternyata menghasilkan suatu URL. Kemudian kita langsung saja buka url yang tertera.
```
https://codepen.io/niclev20/full/vyYQzG/
```

Pada website Codepen, kita buka Editor View untuk melihat source code project tersebut. Pada kolom HTML, disitulah flag yang kita cari. Mantap!

flag : `ABCTF{harder_this_time}`


### File: CTF-Learn-Writeup/pumpkin_carving_COMPLETE/README.md

# Pumpkin Carving
**Category:** forensic
> Something seems to be wrong with the image that I tried to download for Halloween. Perhaps someone has tampered with it.
> 
> https://mega.nz/#!kTpy3JqA!9zID1eTwNRHUCxPXl191uDuKoCj1rcMWt6GtwDx5yG8
> 
> Hint: The flag is in flag{flag_value} format.
---

Pada challenge ini kita diminta untuk mencari flag yang ada di dalam gambar yang disediakan.

Silahkan download file tersebut dan buka menggunakan image viewer.
```bash
eog Pumpkin_.png
```

Ketika dibuka, terjadi error yang mengakibatkan gambar tidak bisa dilihat. Kemungkinan besar file ini telah dilakukan _steganografi_. ([Baca disini](https://id.wikipedia.org/wiki/Steganografi))

Selanjutnya kita cek jenis file ini. Karena file ini merupakan `.png` maka kita bisa sekaligus mengecek apakah terdapat _corrupt_.
```bash
file Pumpkin_.png
pngcheck Pumpkin_.png
```

Dengan perintah `pngcheck` kita tahu bahwa file `Pumpkin_.png` memang corrupt. Selanjutnya kita coba lihat data string yang dapat dibaca dari file ini.
```bash
strings Pumpkin_.png | more
```

Gotcha! Kita temukan flag-nya di bagian atas! Good job!

flag : `flag{happy_halloween!}`


### File: CTF-Learn-Writeup/qr_code_COMPLETE/README.md

# QR Code
**Category:** miscellaneous

> Do you remember something known as QR Code? Simple. Here for you : 
> https://mega.nz/#!Ej4n3RSI!8mbiqg3kosk93qJCP-DBxIilHH2rf7iIVY-kpwyrx-0
---

![QR Code CTFLearn v1](./qrcode.39907201.png "QR Code")

Untuk menyelesaikan challenge QR Code ini kita perlu membaca pesan yang tersimpan di dalamnya. Kita bisa gunakan [QR Scanner online](https://webqr.com/index.html).

Kita mulai dengan scan QR Code dan simpan hasilnya kedalam file hasil_scan.txt
```bash
echo c3ludCB2ZiA6IGEwX29icWxfczBldHJnX2RlX3BicXI= > hasil_scan.txt
```

Bila diperhatikan pesan ini adalah bentuk dari **Base64 Encoding** ([Baca disini](https://en.wikipedia.org/wiki/Base64)) karena terdapat simbol "sama dengan" (`=`) di akhir. Maka kita perlu melakukan _decoding_ terhadap pesan ini.
```bash
cat hasil_scan.txt | base64 -d
```

> synt vf : a0\_obql\_s0etrg\_de\_pbqr

Setelah di-_decode_ kita mendapat pesan yang sulit dibaca, namun pesan ini sebenarnya mengandung. Bisa dilihat dari karakteristik pesan tersebut bisa jadi merupakan _ciphertext_ dari enkripsi **ROT13** ([Baca disini](http://datagenetics.com/blog/july42015/index.html)).

Mari kita coba dekripsi _ciphertext_ ini dengan ROT13.

```bash
cat hasil_scan.txt | base64 -d | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```
* `tr`: _translate_ karakter sesuai dengan bentuk yang kita inginkan. Baca keterangan _command_ ini dengan `man tr`.
* `A-Za-z`: bentuk pertama (`ABC...XYZabc....xyz`)
* `N-ZA-Mn-za-m`: di-_translate_ menjadi bentuk kedua (`NOP...XYZABC...KLMnop...xyzabc...klm`)

![ROT13 Encryption](http://datagenetics.com/blog/july42015/big.png "sumber: datagenetics.com")

flag : `n0_body_f0rget_qr_code`


### File: CTF-Learn-Writeup/qr_code_v2_COMPLETE/README.md

# QR Code v2
**Category:** miscellaneous
> How well are you in the ways of the QR Code?
> https://mega.nz/#!JItR3aqI!QKGxexShAPt-HUU_2DAdJKUljXc69sx1fXuaGUeoKaY
---

![QR Code Challenge V2](./qr_code.jpg "QR Code V2")

Penyelesaian challenge kali ini hampir sama dengan penyelesaian challenge [QR Code v1](https://github.com/cerc-undip/CTF-Learn-Writeup/tree/master/qr_code_COMPLETE)

Untuk menyelesaikan challenge ini kita perlu membaca pesan yang tersimpan di dalamnya. Kita bisa gunakan [QR Scanner Online](https://webqr.com/index.html).

Setelah upload kode QR-nya kita jadi tahu bahwa kode QR tersebut mengandung url. Langsung saja buka url tersebut dan download file didalamnya.
> https://mega.nz/#!9NFhUbwQ!vtrLVum8z-ZXzur33RrGJ4uivMJhA9_5TW2ulHucXoU

Buka file yang baru saja didownload, disitulah flag-nya tersimpan. Mantap!

flag : `CTF{2_QR_4_U}`


### File: CTF-Learn-Writeup/reversal_of_fortune_COMPLETE/README.md

# Reversal of Fortune
**Category:** miscellaneous
```
Our team of agents have been tracking a hacker that sends cryptic messages to other hackers about what he's doing. We intercepted the below message he sent recently, can you figure out what it says? He mentions his hacker name in it, that's the code you need. .nac uoy fi tIe$reveRpilF eldnah ym gnisu em egassem ,avaj yllacificeps ,gnidoc emos htiw pleh deen I ,deifitnedi tegrat txeN
```
---

Di challenge ini kita diminta untuk memasukkan nama hacker yang terdapat di dalam pesan yang di "Enkripsi".

Pada kalimat terakhir terdapat pesan yang cukup aneh, jika diperhatikan setiap kata adalah kata yang dibalik posisinya. Untuk menyelesaikan soal ini bisa menggunakan bahasa pemrograman Python dengan teknik substring. [Baca disini](https://www.dotnetperls.com/substring-python)

```python
soal  = ".nac uoy fi tIe$reveRpilF eldnah ym gnisu em egassem ,avaj yllacificeps ,gnidoc emos htiw pleh deen I ,deifitnedi tegrat txeN"
hasil = soal[::-1]
print(hasil)
```

Pada bagian akhir kalimat terdapat nama hacker yang kita cari, dan itu adalah flag yang kita cari.

flag : `FlipRever$eIt`



### File: CTF-Learn-Writeup/reverse_polarity_COMPLETE/README.md

# Reverse Polarity
**Category:** cryptography

> I got a new hard drive just to hold my flag, but I'm afraid that it rotted. What do I do?

> The only thing I could get off of it was this: 
> 01000011010101000100011001111011010000100110100101110100010111110100011001101100011010010111000001110000011010010110111001111101
---

Pada challenge ini kita hanya diminta untuk mengkonversi bentuk biner kedalam bentuk teks.

Untuk menyelesaikan challenge ini kita bisa menggunakan bahasa pemrograman Python atau jika ingin cepat maka bisa gunakan [Binary to Text translator online](https://www.rapidtables.com/convert/number/binary-to-ascii.html).

```bash
touch script.py
chmod +x script.py
```

Kemudian buka file `script.py` dengan text editor.
```python
#!/usr/bin/python3

baca = "01000011010101000100011001111011010000100110100101110100010111110100011001101100011010010111000001110000011010010110111001111101"
temp = []

for i in range(16):
  temp.append(baca[:8])
  baca = baca[8:]

for i in temp:
  print(chr(int(i, 2)), end="")
```

* Kita memecah setiap 8 karakter bit kedalam list/array temp
* Sisa dari 8 karakter itu disimpan kedalam variabel `baca` agar bisa dipecah kembali
* Setiap nilai di `temp` diubah dari bentuk biner menjadi karakter (`chr()`)

flag : `CTF{Bit_Flippin}`



### File: CTF-Learn-Writeup/simple_image_COMPLETE/README.md

# Simple Image
**Category:** forensic
> Hi, i like this website, ctflearn.com so i decided to share my happiness to you all guys. please, can i smile for you all guys?
> 
> https://drive.google.com/open?id=17NUxdVfobLpFfJpbXf0EZ6WLkjsbGPSa
---

Ketika kita buka gambar yang didownload disana tidak ada informasi apa-apa yang dapat membantu.

Kita juga tidak menemukan informasi dengan perintah `strings`, `file`, `pngcheck`, `binwalk`, `foremost`. Hmm sungguh "**tersembunyi**".

Untuk menyelesaikan challenge ini kita perlu **Image Editor** untuk bisa mengedit saturasi dan komposisi warna yang ada pada gambar. Karena mungkin gambar ini sudah dilakukan _steganografi_.

Tools yang dipakai bisa bermacam-macam, seperti Photoshop, GIMP, dll yang memiliki fitur filter dan komposisi warna. Namun yang akan kita gunakan adalah aplikasi khusus _steganografi_, sehingga kita hanya memilih komposisi yang kita inginkan.

Download dan instal aplikasi yang diperlukan, yaitu Stegsolve.
```bash
wget http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar
chmod +x stegsolve.jar
```
* Baris pertama kita download dari situsnya dan simpan di file `stegsolve.jar`
* Baris kedua kita membuat file `stegsolve.jar` menjadi _executable_

Selanjutnya kita buka aplikasi ini. Karena aplikasi ini berekstensi `.jar` maka ita perlu membukanya menggunakan **Java Runtime**.
```bash
java -jar ./stegsolve.jar
```

![Stegsolve](./filtered.bmp "Filter Red Plane 1")

Selanjutnya buka gambar yang akan kita teliti. Dan terakhir hanya pilih filter komposisi warna dengan klik tanda panah sampai akhirnya kalian menemukan flag-nya.

> Flag terlihat jelas di filter: **Red plane 0**, **Green plane 0**, dan **Blue plane 0**

flag : `flag{smile_for_you}`




### File: CTF-Learn-Writeup/so_many_64_COMPLETE/README.md

# So Many 64s
**Category:** cryptography 

> Help! My friend stole my flashdrive that had the flag on it. When he gave it back the flag was changed! Can you help me decrypt it? https://mega.nz/#!UcYQEArA!H9WxSdG1O7eVcCm0dffggNB0-dBemSpBAXiZ0OXJnLk
---

Pada challenge ini sudah diberikan clue pada judul, yaitu **64** yang menandakan bahwa kita perlu menggunakan bentuk encoding dari **Base64** (Baca [disini](https://en.wikipedia.org/wiki/Base64)).

> Pengunaan Base64 sangat sering di challenge CTF. Maka dari itu diperlukan pemahaman dasar tentang bentuk encoding ini.

Setelah selesai mendownload mari kita buka file tersebut. Karena ekstensi file ini `.txt` maka kita bisa langsung membacanya.
```
cat flag.txt
```

Ketika dibaca, file ini terdiri dari banyak sekali karakter. Sekumpulan karakter ini adalah hasil dari encoding **Base64**. Bisa dengan mudah ditebak dari simbol "sama dengan" (=) di akhir.
```
...ZIZEZaU2JGcFdWRlZTY2xCUlBUMD0=
```

Saat dihitung, file ini memiliki 288956 karakter
```
cat flag.txt | wc -c
```

Untuk menyelesaikan ini kita bisa menggunakan bash script ataupun dengan bahasa pemrograman Python. Tetapi sebelum itu mari kita telaah lagi file `flag.txt` ini dengan men-`decode` karakternya dengan **Base64 decoding**.
```
cat flag.txt | base64 -d
```

Setelah di-_decode_ ternyata hasilnya adalah dalam bentuk Base64 juga. Tetapi jika diperhatikan, hasil decode ini berbeda dengan file decode aslinya. Mari kita coba decode sekali lagi.
```
cat flag.txt | base64 -d | base64 -d
```

Dan memang benar, ketika di-_decode_ kedua kalinya ternyata menghasilkan bentuk Base64 yang berbeda. Bisa dipastikan ini adalah bentuk rekursif Base64 (berulang-ulang).

Jika kita menulis perintah secara manual maka akan memakan waktu sangat banyak, karena kita tidak tahu berapa kali pesan ini di-_encoding_. Maka dari itu dalam writeup ini kita akan menggunakan bahasa pemrograman Python, namun saya sertakan juga penyelesaian dalam bentuk _bash script_.

Langsung saja kita buat file python dan ubah aksesnya menjadi _executable_. Kemudian buka file-nya.
```
touch script.py
chmod +x script.py
```

Untuk bisa men-_decode_ base64 kita perlu menambahkan library base64. Jika belum terinstal maka gunakan perintah `sudo pip install base64`. Karena kita sudah punya file pesan encoding-nya, maka kita akan membaca dari file-nya saja.

```python
#!/usr/bin/python3
import base64

f = open('flag.txt', 'r')
hasil = f.read()

print(hasil)
```

Simpan kemudian jalankan dengan `./script.py`. Dalam program ini kita baru membaca file asli dari pesan yang di-_encoding_. Ketika pesannya muncul sesuai dengan file aslinya, maka bisa kita lanjutkan.

Untuk men-_decode_ pesan kita gunakan _method_ dari library `base64` yaitu `b64decode()`.

```python
#!/usr/bin/python3
import base64

f = open('flag.txt', 'r')
hasil = f.read()
hasil = base64.b64decode(hasil)

print(hasil)
```

Kode diatas baru men-_decode_ satu kali, maka dari itu kita buat perulangan agar program bekerja otomatis. Ketika hasil decoding-nya memiliki karakter `{` (_karakter yang ada di dalam flag biasanya terdiri dari kurung kurawal_) maka kita akan menghentikan program dan menampilkan hasilnya.
```python
#!/usr/bin/python3
import base64

f = open('flag.txt', 'r')
hasil = f.read()

while True:
  hasil = base64.b64decode(hasil).decode('utf-8')

  if '{' in hasil:
    print(hasil)
    break
```
* `.decode('utf-8')`: mengkonversi dari bentuk bytes (hasil decoding) menjadi string.

Setelah program dijalankan maka, Gotcha! Kita menemukan flag-nya!



flag : `ABCTF{pr3tty_b4s1c_r1ght?}`


### File: CTF-Learn-Writeup/solve_this_111_COMPLETE/README.md

# Solve this 111
**Category:** miscellaneous
> 01001001001000000110110001101111 01110110011001010010000001100011 01101000011010010110001101101011 01100101011011100010000001100001 01101110011001000010000001101100 01100101011011010110111101101110
> Solve this
---

Pada challenge ini kita hanya diminta untuk mengkonversi dari bentuk biner kedalam bentuk karakter/string.

Untuk menyelesaikan ini kita bisa menggunakan bahasa pemrograman Python atau jika ingin cepat bisa gunakan [Binary to Text Online](https://www.rapidtables.com/convert/number/binary-to-ascii.html).

Penjelasan kode sama dan sudah dijelaskan pada writeup sebelumnya yaitu [Double Encryption](https://github.com/cerc-undip/CTF-Learn-Writeup/tree/update/double_encryption_COMPLETE).

Buat file `script.py` dan ubah aksesnya menjadi _executable_.
```bash
touch script.py
chmod +x script.py
```

Buka dan simpan kode ini di `script.py` kemudian jalankan menggunakan `./script.py`.
```python
#!/usr/bin/python3

soal = "01001001001000000110110001101111 01110110011001010010000001100011 01101000011010010110001101101011 01100101011011100010000001100001 01101110011001000010000001101100 01100101011011010110111101101110"
soal = "".join(soal.split(" "))
hasil_temp = []

for i in range(len(soal) // 8):
  hasil_temp.append(soal[:8])
  soal = soal[8:]

hasil = ""

for j in hasil_temp:
  temp = int(j, 2)
  hasil += chr(temp)

print(hasil)
```

flag : `I love chicken and lemon`


### File: CTF-Learn-Writeup/taking_ls_COMPLETE/README.md

# Taking LS
**Category:** forensic

```
Just take the Ls
https://mega.nz/#!9Mk00LxR!_FtmAm8s_mpsHr7KWv8GYUzhbThNn0I8cHMBi4fJQp8
NOTE: Problem is really only for mac users - sorry in advance - free points if you have a different operating system though :)
```

Extract file download menggunakan terminal
```
unzip The\ Flag.zip
ls -l
```

Setelah di-ekstrak, akan ada folder baru bernama `The Flag`. Masuk ke folder `The Flag`
```
cd The\ Flag
```

Setelah itu, list semua file yang ada di dalam folder `The Flag`
```
ls -l
```

Disini hanya terdapat file `The Flag.pdf`. Kita coba buka file tersebut, bisa menggunakan **gnome** maupun buka melalui **nautilus**
```
gnome-open The\ Flag.pdf
```
atau
```
nautilus ./
```

Ketika kita coba buka ternyata file tersebut di-password. Langkah selanjutnya adalah kita mencari password-nya.
Kali ini kita coba list semua file di dalam folder `The Flag` agar kita bisa melihat file yang tersembunyi.
```
ls -la
```
* `l`: menampilkan dalam bentuk list lengkap
* `a`: menampilkan semua file, termasuk file tersembunyi

Setelah mencoba perintah diatas ternyata ada 2 file dan folder baru yang tersembunyi (_tanda `.` di awal_), yaitu `.DS_Store` dan `.ThePassword`.
File `.DS_Store` bukan merupakan file yang kita cari. Kita masuk ke folder `.ThePassword`. Di dalam folder ini terdapat 1 file berekstensi `.txt` maka bisa langsung kita lihat isinya.
```
cd .ThePassword
ls -la
cat ThePassword.txt
```

Setelah melihat isi file, kita mendapatkan password yang kita inginkan. Kemudian kembali lagi ke folder sebelumnya dan kita buka lagi file pdf dengan memasukkan password yang sudah kita dapat.
```
cd ..
gnome-open The\ Flag.pdf
```

flag `ABCTF{T3Rm1n4l_is_C00l}`


### File: CTF-Learn-Writeup/up_for_a_little_challenge_COMPLETE/README.md

# Up For A Little Challenge?
**Category:** forensic

> https://mega.nz/#!LoABFK5K!0sEKbsU3sBUG8zWxpBfD1bQx_JY_MuYEWQvLrFIqWZ0 You Know What To Do ...
---

Challenge ini tidak memberikan clue apapun dan beranggapan bahwa kita tahu apa yang kita lakukan. Oke mari kita buka file `Begin Hack.jpg` yang baru didownload
```bash
eog Begin\ Hack.jpg
```

![Begin Hack](https://raw.githubusercontent.com/cerc-undip/CTF-Learn-Writeup/update/up_for_a_little_challenge_COMPLETE/Begin%20Hack.jpg)

Setelah dibuka dengan _image viewer_ tidak ada keterangan yang berarti dan hanya gambar biasa.

Selalu perhatikan untuk file yang bertipe gambar pasti sudah dilakukan Steganografi, yaitu pesan disembunyikan di dalam gambar ([Baca disini](https://id.wikipedia.org/wiki/Steganografi)). Untuk itu kita perlu mengecek informasi apa saja yang ada di dalam gambar ini dalam bentuk _string_ (karakter yang bisa dibaca oleh manusia).
```bash
strings Begin\ Hack.jpg | more
```

Perhatikan beberapa kata yang bisa dibaca ketika kita _scroll_. Disitu terdapat satu URL, buka URL itu dan download file yang ada.

> https://mega.nz/#!z8hACJbb!vQB569ptyQjNEoxIwHrUhwWu5WCj1JWmU-OFjf90Prg

Extract file tersebut
```bash
unzip Up\ For\ A\ Little\ Challenge.zip
```

Setelah di-_extract_ kita mendapat ada 2 folder yaitu `Did I Forget Again?` dan `__MACOSX`. Folder yang akan kita jelajah adalah `Did I Forget Again?`, sedangkan folder `__MACOSX` adalah folder yang otomatis dibuat ketika membuat arsip menggunakan komputer Mac. ([Baca disini](https://gotoes.org/sales/Zip_Mac_Files_For_PC/What_Is__MACOSX.php))
```
cd Did\ I\ Forget\ Again\?
ls -la
```

Disini ada 1 file gambar dan 1 file tersembunyi dengan ekstensi `cerb4`. Jika kita buka file `Loo Nothing Becomes Useless ack.jpg` tidak akan ada informasi yang disediakan, begitu juga ketika kita melihat string dari gambar ini.
```bashi
eog Loo\ Nothing\ Becomes\ Useless\ ack.jpg
strings eog Loo\ Nothing\ Becomes\ Useless\ ack.jpg
```

Kali ini kita coba telaah apa itu file .Processing.cerb4
```
file .Processing.cerb4
```

Setelah dilihat, ternyata jenis file ini adalah **Zip**. maka dari itu kita perlu mengubah/menambah ekstensi `.zip` di belakang nama file. Kemudian lakukan _extracting_.
```bash
mv .Processing.cerb4 .Processing.cerb4.zip
unzip .Processing.cerb4.zip
```

Saat mencoba meng-_extract_ file ini, kita diminta untuk memasukkan password. Lalu dimana kita bisa mendapat password-nya?

Oke, sekarang kita kembali lagi ke file yang pertama dan lihat lagi bahwa disitu terdapat password yang dapat digunakan untuk meng-_extract_ file tadi.
```
cd ..
strings Begin\ Hack.jpg | more
```

> Nothing Is As It Seems

Kemudian kita extract file `.Processing.cerb4.zip` dengan password yang telah kita dapat. Terakhir, kita buka file yang telah di-_extract_.
```
cd Did\ I\ Forget\ Again\?
unzip .Processing.cerb4.zip
eog skycoder.jpg
```

Gotcha! Kita dapat flag-nya! Ada di pojok kanan bawah.

flag : `flag{hack_complete}`



### File: CTF-Learn-Writeup/whats_your_fav_num_alpha_COMPLETE/README.md

# What's Your Favorite Number of the Alpha
**Category:** programming

> The flag accidentally got changed into something else. Here is the flag: ¥¦§¸ªßØÌÉÃÊÐÅËá If it helps, I think the first letter was an A (capitalized)... Title is supposed to be "What's Your Favorite Number of the Alphabet, got cut off :(
---

Pada challenge ini kita langsung diberikan flag-nya, hanya saja dalam bentuk yang tidak bisa dibaca. Kita diharuskan untuk mengubah bentuk itu menjadi bentuk yang bisa dibaca.

Di soal juga diberikan clue bahwa huruf pertama adalah huruf `A` kapital.

| Dari | Menjadi |
|------|---------|
| ¥    | A       |

Kita akan coba menyelesaikan challenge ini menggunakan bahawa pemrograman Python karena bahasa ini menyediak konversi dari karakter ASCII menjadi desimal (_ASCII to Decimal_) sehingga kita bisa melihat algoritma yang dipakai untuk membuat rangkaian hurufnya.

Langsung saja jalankan Python3 interpreter
```
python3
```

Kita coba ubah karakter pertama soal menjadi desimal
```python
>>> ord('¥')
165
```
Ternyata didapat bahwa karakter `¥` memiliki angka desimal 165. Kemudian kita coba dengan karakter A.
```python
>>> # karakter -> desimal
>>> ord('A')
65
>>> # sebaliknya (desimal -> karakter)
>>> chr(65)
'A'
```

Nah, dari sini kita tahu bahwa algoritma yang dipakai untuk _decoding_ adalah dengan mengurangi 100 dari angka desimal dari ASCII. Atau bisa kita modelkan seperti ini:
> decode(kar) = desimal(kar) - 100

Kita bisa mencoba satu-satu seperti pada contoh sebelumnya. Tetapi agar efisien kita gunakan perulangan pada Python.
```python
>>> soal = "¥¦§¸ªßØÌÉÃÊÐÅËá"
>>> hasil = ""
>>> for karakter in soal:
...   temp = ord(karakter) - 100
...   hasil += chr(temp)
...
>>> print(hasil)
```

Gotcha! Kita dapat flag-nya!

flag : `ABCTF{the flag}`


### File: CTF-Learn-Writeup/where_can_my_robot_go_COMPLETE/README.md

# Where Can My Robot Go?
**Category:** miscellaneous
```
Hint: Where do robots find what pages are on a website?
Hint 2: What does disallow tell a robot? Hint 3: The flag is not 70r3hnanldfspufdsoifnlds
```
---

Di challenge ini diberikan clue yang cukup membantu untuk menyelesaikan. Robot yang dimaksud disini adalah file `robots.txt` yang ada di setiap halaman web.

File `robots.txt` dipasang di web untuk menentukan folder mana saja yang diizinkan atau tidak diizinkan untuk di-index oleh mesin pencari.

Kita coba akses file `robots.txt` website CTFLearn melalui browser
```
https://ctflearn.com/robots.txt
```

Di dalam file ini, _developer_ tidak memperbolehkan _search engine_ untuk mengakses file `/70r3hnanldfspufdsoifnlds.html`. Tapi, kita akses file ini dengan harapan bisa mendapatkan flag yang kita cari.
```
https://ctflearn.com/70r3hnanldfspufdsoifnlds.html
```

Ternyata kita menemukan flag di dalamnya.

> Untuk mempersingkat kita bisa menggunakan cURL untuk mendapatkan halaman yang kita akses
> cURL sangat berguna ketika menyelesaikan challenge dengan kategori **web**

```
curl https://ctflearn.com/70r3hnanldfspufdsoifnlds.html
```

flag : `abctf{r0b0ts_4r3_th3_futur3}`
