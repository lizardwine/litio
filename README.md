A simple tool for testing

# litio

## how to use

example 1:

```
python3 -m litio -c litio-config.yml
```

litio-config.yml:
```yaml
name: My Awesome Title

tests:
  firsth-test: # test name
    path: ./tests/test1.py # path to python file
    functions: # functions list
      - pow: # function name
          inputs: # inputs
            # arguments with name of parameters
            base: 2
            exponent: 2
          expected:
            value: 4 # expected value
            comparator: Equals
          print-return: true # print returned value by function
```

test1.py:
```python
def pow(base, exponent):
    return base**exponent
```