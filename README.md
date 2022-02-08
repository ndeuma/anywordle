# anywordle
A highly configurable command line implementation of the "Wordle" word guessing game. Needs Python and the "dict" utility (installable on most Linux distributions). 

![screenshot](https://user-images.githubusercontent.com/136928/153071478-f202cd05-ac76-48d8-86a8-0690453da1a1.png)

```
usage: anywordle.py [-h] [-a ATTEMPTS] [-l LENGTH] [-s] [-v] [wordlist]

A highly configurable implementation of the 'Wordle' word-guessing game.

positional arguments:
  wordlist              Word list file (default: English 'dict' dictionary
                        files)

optional arguments:
  -h, --help            show this help message and exit
  -a ATTEMPTS, --attempts ATTEMPTS
                        Allowed number of attempts (default: 6)
  -l LENGTH, --length LENGTH
                        Length of word to guess (default: 5)
  -s, --strict          Strict mode (hints must be used in subsequent guesses)
  -v, --verbose         Print detailed output
```




