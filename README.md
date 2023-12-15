# Advent of Code 23

Solutions for the advent of code 2023 puzzles, implemented in Python. The
puzzles can be found here: https://adventofcode.com/2023

## Algorithms

### Dynamic Programming

Dynamic programming is basically memoization. If a certain state occurs several times we can cache
the result and instantly get the result instead of computing it multiple times. The import part is
to find what the state is and what to include, if the state space is too large DP might not be
feasible. It is also important that we actually encounters the same state several times for DP to
have an affect. See day 12 for an example.

### Backtracking

Backtracking incrementally builds the solution and abandons a certain part as soon as it doesn't
fulfill the constraints. See day 12 for an example where the current path is abandon as soon as the
solution does not follow the rules.

### Intervals/Ranges

Instead of processing each element one by one try to find a group that is processed in the equally.
Then it is possible to process an entire group, which could lead to big speed ups in case of many
objects. It might also be beneficial to define a range as `[start, end[`, as e.g.
`len(range) = b - a` and `[a, b[ + [c, d[ = [a, c[`. See day 5.

### Hamming Distance

The number of different elements in two sequences (e.g. binary numbers).

### Cycle Detection

For some problems that needs to run for many iteration it might be possible to detect a cycle
(e.g. by keeping track of the current state via a set). Then all iterations can efficiently be run
by ignoring all cycles and only run the part before the cycle is entered and the number of steps
remaining after the cycle to fit the exact number of iterations. See day 14.

```
def f(steps):
    states = {}
    t = 0
    while t < steps:
        t += 1
        do_stuff()
        state = get_state()
        if state in states:
            cycle_length = t - states[state]
            num_cycles = (steps - t) // cycle_length
            t += num_cycles * cycle_length
        else:
            states[state] = t
```

### Inside/outside Detection

To detect if we are inside or outside a geometric figure (e.g. loop or rectangle) we can scan for
crossings and change the inside/outside state at each crossing. See `get_insides` in algorithms.

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

Flatten 2D list:
```
[e for row in array_2d for e in row]
```

Rotate 2D list clockwise:
```
list(map(list, zip(*grid[::-1]))
```

Assignment in list comprehension:
```
sum(x**2 for e in elements if (x := f(e)) is not None)
```

Delete from dict without KeyError for missing elements:
```
dictionary.pop(key, None)
```

## Regexp

Find overlapping matches:
```
import regex
regex.findall(pattern, text, overlapped=True)]
```
Note that there is (syntax) support for this in the ordinary re module but not as convenient.
