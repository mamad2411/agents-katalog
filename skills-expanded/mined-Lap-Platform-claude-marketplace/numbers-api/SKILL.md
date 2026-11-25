---
name: numbers-api
description: "Numbers API skill. Use when working with Numbers for numbers. Covers 26 endpoints."
version: 1.0.0
generator: lapsh
---

# Numbers API
API version: 1.5

## Auth
ApiKey X-Mathtools-Api-Secret in header

## Base URL
https://api.math.tools

## Setup
1. Set your API key in the appropriate header
2. GET /numbers/nod -- verify access

## Endpoints

26 endpoints across 1 groups. See references/api-spec.lap for full details.

### numbers
| Method | Path | Description |
|--------|------|-------------|
| GET | /numbers/nod | Get the number of the day for current day |
| GET | /numbers/fact | Get a random fact about a number |
| GET | /numbers/random | Generate random number(s) |
| GET | /numbers/ordinal | Get the ordinal of the given number |
| GET | /numbers/cardinal | Get the cardinal of the given number |
| GET | /numbers/currency | Spells out the number as a currency |
| GET | /numbers/numeral/egyptian | Convert base 10 representation of a given number to egyptian numeral. |
| GET | /numbers/numeral/chinese | Convert base 10 representation of a given number to chinese numeral. |
| GET | /numbers/numeral/roman | Convert base 10 representation of a given number to roman numeral. |
| GET | /numbers/base/binary | Convert a given number to binary |
| GET | /numbers/base/octal | Convert a given number to octal |
| GET | /numbers/base/hex | Convert a given number to hexadecimal |
| GET | /numbers/base | Convert a given number from one base to another base |
| GET | /numbers/pi | Get digits of pi (Ï€) |
| GET | /numbers/prime/is-prime | Checks whether a given number is a known prime number or not. |
| GET | /numbers/prime/is-mersenne-prime | Checks whether a given number is a known mersenne prime number or not. |
| GET | /numbers/prime/is-fermat-prime | Checks whether a given number is a known fermat prime number or not. |
| GET | /numbers/prime/is-pell-prime | Checks whether a given number is a known pell prime number or not. |
| GET | /numbers/prime/is-partition-prime | Checks whether a given number is a known partition prime number or not. |
| GET | /numbers/prime/is-fibonacci-prime | Checks whether a given number is a known fibonacci prime number or not. |
| GET | /numbers/prime/factors | Get the prime factors of a given number. |
| GET | /numbers/is-palindrome | Checks whether a given number is a palindrome number or not. |
| GET | /numbers/is-triangle | Checks whether a given number is a triangle number or not. |
| GET | /numbers/is-cube | Checks whether a given number is a cube number or not. |
| GET | /numbers/is-square | Checks whether a given number is a square number or not. |
| GET | /numbers/prime/is-perfect | Checks whether a given number is a perfect number or not. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all nod?" -> GET /numbers/nod
- "List all fact?" -> GET /numbers/fact
- "List all random?" -> GET /numbers/random
- "List all ordinal?" -> GET /numbers/ordinal
- "List all cardinal?" -> GET /numbers/cardinal
- "List all currency?" -> GET /numbers/currency
- "List all egyptian?" -> GET /numbers/numeral/egyptian
- "List all chinese?" -> GET /numbers/numeral/chinese
- "List all roman?" -> GET /numbers/numeral/roman
- "List all binary?" -> GET /numbers/base/binary
- "List all octal?" -> GET /numbers/base/octal
- "List all hex?" -> GET /numbers/base/hex
- "List all base?" -> GET /numbers/base
- "List all pi?" -> GET /numbers/pi
- "List all is-prime?" -> GET /numbers/prime/is-prime
- "List all is-mersenne-prime?" -> GET /numbers/prime/is-mersenne-prime
- "List all is-fermat-prime?" -> GET /numbers/prime/is-fermat-prime
- "List all is-pell-prime?" -> GET /numbers/prime/is-pell-prime
- "List all is-partition-prime?" -> GET /numbers/prime/is-partition-prime
- "List all is-fibonacci-prime?" -> GET /numbers/prime/is-fibonacci-prime
- "List all factors?" -> GET /numbers/prime/factors
- "List all is-palindrome?" -> GET /numbers/is-palindrome
- "List all is-triangle?" -> GET /numbers/is-triangle
- "List all is-cube?" -> GET /numbers/is-cube
- "List all is-square?" -> GET /numbers/is-square
- "List all is-perfect?" -> GET /numbers/prime/is-perfect
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
