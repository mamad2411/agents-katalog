# Project: Restaurant Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Create a new constant dict, called MENU, representing the possible items you can order at a restaurant.
  - The keys will be strings and the values will be prices (integers for the sake of simplicity).
- Write a function - restaurant() - that asks the user to enter an order.
  - If the user enters the name of a dish on the menu, the program prints the price and the running total. It then asks the user again for their order.
  - If the user enters the name of a dish not on the menu, the program mildly scolds the user, and then asks again for their order.
  - If the user enters an empty string, the program stops prompting and prints the total amount.
- An example session is as follows:
```
Order: sandwich
sandwich costs 10, total is 10
Order: tea
tea costs 7, total is 17
Order: elephant
Sorry, we are fresh out of elephant today.
Order: <enter>
Your total is 17
```
- Use Pythonic conventions.

## Exercise notes
- You can check to see if a key is in a dict with the in operator.
- Consider using strip on a user's input to tidy up any inadvertent whitespace.
- Consider using str.casefold to make sure key lookups are consistent.
