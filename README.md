A simple tool for testing

# litio

## how to use

## example 1: The basics

### install
```bash
pip install litio
```
### run
```bash
python3 -m litio -c litio-config.yml
```

### litio-config.yml:
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
```

### test1.py:
```python
def pow(base, exponent):
    return base**exponent
```

## example 2: If something fails?

### test2.py:
```python
def pow(base, exponent):
    return base / exponent # it's obviously not working.
```



litio-config.yml:
```yaml
name: My Awesome Title
api-key: YOUR_OPENAI_API_KEY_ENVIRONMENT_VARIABLE # the name of the environment variable, NOT THE API KEY!
tests:
  failed-test:
    path: ./tests/test2.py
    functions: 
      - pow:
          inputs:
            base: 2
            exponent: 2
          expected:
            value: 4
            comparator: Equals
          verbose: true 
          auto-fix: true # auto fix function using AI if call fails
```

## how auto-fix works?
The "auto-fix" parameter instructs litio to use artificial intelligence to automatically repair and replace the function in the source code. If you prefer to confirm before consulting AI, you can use the "use-ai" parameter instead of "auto-fix."

## example 3: if a tests is not ready yet?

### test3.py:
```python
def coming_soon():
    pass # it's not ready yet
```

litio-config.yml:
```yaml
name: My Awesome Title
tests:
  not-ready-test:
    path: ./tests/test3.py
    functions: 
      - coming_soon:
          expected:
            value: i am not ready yet
            comparator: Equals
          ignore: true # ignore this test and continue
```


# Litio config file reference

## `name` paramater

- The `name` parameter is the title of the config file.

## `api-key` parameter

- The `api-key` parameter is the name of the environment variable that contains the OpenAI API key, NOT THE API KEY!

## `output-style` parameter
- The `output-style` parameter is the style of the output. It can be `capybara` or `classic` for now.

## `tests` parameter

- The `tests` parameter is a dictionary of tests.

## Tests structure

- The test name is the name of the test.
- The `path` parameter is the path to the Python file that contains the functions, methods or classmethods to test.
- The `functions` parameter is a list of functions to test.

Looks like this:
```yaml
...
tests:
  first-test:
    path: ./src/utils.py
    functions:
      - add: # function name
          ...


```

## Function structure

- The function name is the name of the function.
- The `inputs` parameter is a dictionary of inputs.
- The `expected` parameter is a dictionary with expected value and comparator.
- The `verbose` parameter is a boolean that indicates whether to print the full function call.
- The `auto-fix` parameter is a boolean that indicates whether to use AI to automatically fix the function. Only can be used with the `Equals` comparator.
- The `use-ai` parameter is a boolean that indicates whether to use AI to fix the function. Only can be used with the `Equals` comparator.
- The `ignore` parameter is a boolean that indicates whether to ignore the function.

Looks like this:
```yaml
...
tests:
  first-test:
    path: ./src/utils.py
    functions:
      - FUNCTION_NAME: # (e.g. subtract)
          inputs:
            a: 1 # arguments with name of parameters
            b: 2 # must be the same as the name of the parameter
          expected:
            value: -1 # expected value
            comparator: Equals

```

## Using methods

The syntax for a method is the same as that of a function, except that you need to add the "instance" parameter with the values to instantiate an object of that class.

Looks like this:
```yaml
...
tests:
  first-test:
    path: ./src/utils.py
    functions:
      - Person.get_age:
          instance:
            name: John
            age: 30
          expected:
            value: 30
            comparator: Equals

```

## What comparators are there?

- `Equals`
- `Greater`
- `Less`
- `GreaterOrEqual`
- `LessOrEqual`
- `NotEquals`
- `Is`
- `isNot`
- `IsNone`
- `IsNotNone`
- `IsInstance`
- `IsNotInstance`