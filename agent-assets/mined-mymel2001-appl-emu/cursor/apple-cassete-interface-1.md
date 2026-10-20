---
description: 
globs: 
alwaysApply: false
---

Obviously it was all a matter of lack of program memory which caused this undocumented feature.
The Write routine starts by writing a 10 seconds long
header, after that the data bytes are written to tape.
Each time a new byte is collected from memory, which
is then shifted out bit by bit. Then the begin address is
incremented until it is higher than the end address.
Because all timing is done in software loops you'll see
quite a lot of compensation instructions in the different
parts of the process. Their purpose is to compensate for
the extra work which is needed to get new bytes, shift
bits and increment addresses.
The Read routine may appear to be a little more
complicated at first, but we'll manage it all the same.
First we try to detect a full cycle of the input signal to
assure us that the tape really has been started. Then
we introduce a short delay to allow the tape speed to
stabilize. The write header routine is abused to create
this delay. This has one extra benefit, it saves the X
pointer for us which we need later in order to parse the
next command. Finally another full cycle is detected to
synchronize the timing with the tape signal.
Then we start a loop which must detect the start bit,
which is shorter than the other bits in the header. When
the start bit is detected we have to wait for the second
half of the start-bit before we can start reading the
actual data.
Now it's time to read in the data. Obviously all bytes contain 8 bits, which explains the RDBIT loop. Inside
this loop we measure the duration of a full cycle. If the timer value passes the 0 we know that the time was
longer than the average between a "1" and a "0", and vice versa. As soon as a byte is read it is stored in
memory, after which the begin address is incremented until it is larger than the end address.
Here we also see some compensation values for the timing to overcome the differences in workload.
The FULLCYCLE routine simply calls the CMPLEVEL routine, which is effectively executed twice this way. The
timer is decremented, which will finally indicate the interval time for a full cycle. And now we come to the
clever part of Steve's hardware. Remember the way we read the input, by manipulating address line A0 to
the PROM? Well the LDA TAPEIN instruction may effectively load the accumulator with the value on $C080
or $C081. We're not interested in the actual value in neither of these addresses, we only want them to be
different. And fortunately they are different.
The CMP #128 instruction at the end will set the Carry flag according to the measured time. If the timer
crosses the 0 the carry will be set, otherwise the carry will be cleared. Now the carry represents the level
of the new bit.
The WHEADER routine is responsible for writing the header to the tape. First of all the parse pointer X is
saved. Then we see two nested loops.
The inner loop uses the X register, which counts a full cycle each time. Well not each time, the first time the
X register doesn't contain 0 to start with. But that is only a marginal difference, which is hardly noticeable.
The outer loop uses the Accumulator as counter. Since there is no DEA instruction on the NMOS version of
the 6502 we have to use the ADC instruction. We only subtract 1 here, because the carry is always set
inside the loop! The end result is indeed a header with a time of about 10 seconds.
When the program finally falls through the outer loop a relatively short bit is written (LDA #30) which will
function as start bit.
Now we arrive at the WRITEBIT routine. This routine is a concatenation of some timing loops. The first loop
times a single phase of the 2 kHz frequency (in case the data bit is 0), this loop is only followed by a second
loop if a 1 kHz phase is required.
The WDELAY routine is executed twice to create a full cycle of the selected frequency.
Finally the INCADDR routine first compares the begin address with the end address to see if we're done.
The actual decision is postponed though to the calling routine, only the Carry flag is set accordingly.
Then the address is simply incremented. And then the 256 bytes of the PROM are completely filled again.
I have only a few last remarks to make regarding the ACI software. First of all there was no room to
initialize the stack pointer again. This means that you cannot read data into page $01 and expect it to
survive the stack actions of the ACI program because the stack can be all over the place.
The second memory space you stay clear of are the addresses $0024 to $0029, which are used by the ACI
program.
Finally you should be aware of the use of page $02 as input buffer. If you keep the tape commands short,
you should be able to use most of page $02 though.