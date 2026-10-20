# Exercise 36: Sales Tax

## Requirements

- You are building a program that calculates sales tax for the imaginary country of Freedonia.
- Create a module `freedonia.py` that implements a function `calculate_tax` that takes three arguments:
  - Amount of the purchase.
  - The province in which the purchase took place. There are four provinces in Freedonia: Chico, Groucho, Harpo, Zeppo.
  - The hour (an integer from 0-23) at which the purchase took place.
- calculate_tax() should return the final price, as a float.
- The base tax rates are different for each province:
  - Chico: 50%
  - Groucho: 70%
  - Harpo: 50%
  - Zeppo: 40%
- The amount of tax also depends on the hour at which the purchase was made. The hour acts as a scalar on the tax rate:
  - At midnight (hour 0), there's no sales tax at all.
  - At midday (hour 12), the sales tax is scaled by 12/24 (1/2).
  - In the last hour of the day (hour 23), the sales tax is scaled by 23/24.
- Example: calculate_tax(500, 'Harpo', 12)
  - A £500 purchase in Harpo would normally result in £250 additional tax, so £750 overall.
  - As the purchase was at midday, the tax is scaled back by half to £125, for a total of £625.
- Write the solution using two separate files:
  - freedonia.py: contains supporting data and functions, including calculate_tax().
  - use_freedonia.py: the program that calls calculate_tax.py.
- Use Pythonic conventions.

## Exercise Notes

- The freedonia module should define data structures and functions that provide functionality to one or more other programs.
- Consider using a dict for holding rates.
- Consider using a separate function for handling the scaling behaviour.
- Consider using custom exceptions for handling invalid inputs.