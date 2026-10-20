# Exercise 49: Elapsed Since

## Requirements

- Write a generator function `elapsed_since` whose argument must be iterable.
- With each iteration, the generator returns a two-element tuple:
  - The first element in the tuple will be an integer specifying how many seconds have elapsed since the last iteration.
  - The second element will be the next element from the passed, iterable argument.
- Timing should be relative to the previous iteration, not when the generator was first created or invoked. The timing number in the first iteration will be 0.
- Use Pythonic conventions.

## Exercise Notes

- Consider using perf.time_counter, which returns the number of seconds since the program was started. It is considered more reliable than time.time.
- Take care in handling the timing number in the first iteration.
- In a generator function, the stack frame is maintained between calls, so local variables retain their values across calls.
