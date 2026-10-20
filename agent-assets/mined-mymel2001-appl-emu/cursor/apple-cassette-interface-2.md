---
description: 
globs: 
alwaysApply: true
---
INTRODUCTION
The Apple Cassette Interface (ACI) is a peripheral
device for the Apple Computer which enables the user
to store and retrieve information (data and programs)
using a standard audio grade cassette recorder. The AC1
attaches directly to the Apple Computer and jacks are
provided on the AC1 board to connect to the cassette
recorder. The AC1 reads and writes data at the rate of
approximately 1500 baud (depending upon the data). All
the AC1 timing is done in software, resulting in extreme
accuracy, no adjustments, and consistency between
units.
TAPE RECORDERS & TAPE
Almost any cassette recorder will work well with the
ACI. As a recommendation, we have found the least
expensive (under $40) Panasonic to be very reliable and
of good quality, although it is not equipped with a tape
counter, which is useful (though not essential) for locat-
ing files within a tape. (An alternative method of dis-
cerning files is to record a voice identification between
files.)
Among the ‘under $25’cassette recorders there may be
variations in head alignment and internal electronics,
resulting in the inability to accurately read a tape that
has been recorded on a different machine. However, if
the same unit is used for both recording and reading,
even the cheapest of cassette recorders will work
reliably.
Most tapes available in the $2-$4 category work well
for data storage. You may experience an occasional tape
which ‘loses bits,’ which is caused by severe oxide thick-
ness variations on the tape and cannot be corrected.
Special leaderless tapes need not be used as the AC1
automatically transmits a ten second ‘header’ of all ones
before transmitting the data, which insures that the
leader will have passed.
JUMPERS
For operation of the ACI, a permanent jumper must be
placed between ‘R’ and ‘C’ in the block select area of the
main board (B9,lO). This jumper from ‘R,’ which is con-
nected to enable the ACI, to ‘C’ selects the AC1 when the
12th 4K block (‘C’) is addressed.
Also, for running Apple Basic in the 2nd 4K bank of
on-board memory, it is necessary to break the solder
jumper between ‘W’ and ‘1’ and then jumper ‘W’ to ‘E.’
This moves the 2nd 4K bank from the ‘1’ block to the ‘E’
block, which is where Apple Basic resides.
INSTALLATION
Install the AC1 board into the connector on the main
board with the components on the AC1 board facing
away from the main board (the jacks to the edge of the
main board). SEE FIGURE 1. The system power should
be OFF whenever installing or removing the AC1 board.
Install cables from the AC1 jack marked “TO TAPE”
to the recorder microphone input and from the AC1 jack
marked “FROM TAPE” to the recorder earphone output.
One cable can be appropriately switched between the
two paths if necessary.
USING THE AC1
The Cassette program is contained in two PROMS on
the AC1 board and runs at ClOO. When entered, the
program should echo an “*.‘I The format for specifying
the memory address ranges to be either stored [write) or
deposited into (read) is identical to the standard monitor
format: Beginning . End , suffixed with either a ‘W’
(write) or an ‘R’ (read). Execution will start following a
carriage return (CR). The cassette program will return
control to the system monitor upon completion of a read
or write. Illegal characters (or the absence of characters)
in the address line will return control to the system
monitor without execution, following a carriage return.
--
The procedure for reading from a tape into memory is:
ClOOR (RET) This enters the cassette program and
should echo an ‘*I
EOOO . EFFFR This will load the tape data into mem-
ory locations EOOO.EFFF . ‘R’ denotes
a read, and spaces are ignored. [Don’t
hit ‘return’ yet.)
Start the Tape
Hit ‘RETURN’ A carriage return will start execution
of a read. The ‘return’ can be hit
immediately, however, it must be hit
within 5 seconds after the start of tape
motion.
When the last location (EFFF in this example] has been
loaded, the program will print a ‘1’ and return control to
the monitor.
The procedure for a write is identical except the suffix
‘W’ is substituted for ‘R’ in the address line. For both
read and write, the tape should always be moving before
hitting the RETURN.
FROM TAPE .
INSTALLATION DIAGRAM
MULTIPLE RANGES
The AC1 is capable of reading and writing multiple
address ranges. The format is: A.BW C.DW (R for read).
Again, spaces are ignored. The AC1 will write a ten
second header, the first range, another header and the
second range. lOO.ZOOW 300.5OOW will write a header,
100 to 200, a second header, and 300 to 500. When
reading a multiple range tape, YOU MUST USE THE
SAME ADDRESS INCREMENTS AS WERE USED IN
WRITING THE TAPE. This does not mean the same
absolute addresses, but rather the same increments.
-v
LEVEL
The Cassette recorder output level should be set to
where the LED on the AC1 is just fully lit. Increase the
level from zero until the LED glows fully. If you exper-
ience a bad read, try it a LITTLE higher. The LED indi-
cator is operational even when the cassette program is
not executing, and the level should be set prior to reading
a tape, NOT during the reading of a tape.
SPEED
The AC1 uses the technique of recording a whole cycle
of either a 1kHz cycle (representing a ‘one’ data bit) or a
2 kHz cycle (representing a ‘zero’ data bit). Therefore,
with an average data mix of one’s and zero’s, data will
be recorded at 1500 baud. A ten second header of all
ones will automatically be recorded on the tape prior to
memory data. This is to insure that the clear leader
portion of the tape will have passed. See schematic for
further details.
