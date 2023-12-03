# Advent of Code 23

Solutions for the advent of code 2023 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2023

## Python

Break out of nested loop:

```
for y in range(10):
    for x in range(10):
        if <condition>:
            break
    else:
        continue
    break
```

## Regexp

Find overlapping matches:
```
import regex
regex.findall(pattern, text, overlapped=True)]
```
Note that there is (syntax) support for this in the ordinary re module but not as convenient.
