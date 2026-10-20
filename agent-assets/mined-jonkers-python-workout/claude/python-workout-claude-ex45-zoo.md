# Exercise 45: Zoo

## Requirements

- Create a `Zoo` class in order to house `Cage` instances introduced in exercise 44.
- Given a Zoo z, we should be able to print all the cages (with their ID numbers) and the animals inside just by invoking print(z).
- We should be able to get the animals with a particular colour by invoking the method z.animals_by_colour(colour). The result should be a list of Animal objects.
- We should be able to get the animals with a particular number of legs by invoking the method z.animals_by_legs(legs). The result should be a list of Animal objects.
- We also need to be able to invoke z.number_of_legs() and get a count of the total number of legs for all the animals in our zoo.
- Use Pythonic conventions.

## Exercise Notes

- Consider use of the splat operator on parameters provided to add_cages.
- Consider directly extending the code in exercises 43 and 44.
- You might need to use nested for loops and a conditional within list comprehensions / generators.

