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
litio run
```

### litio.yml
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



litio.yml:
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

litio.yml:
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

# Litio commands

- ## `run`
  - Action: Runs the tests.
  - parameters:
    - `--verbose`(aliases: `-V`): Prints the full function call.
    - `--output`(aliases: `-o`): The style of the output. It can be `capybara` or `classic` or you can install a custom style.
    - `--ai`/`--no-ai`: enable/disable auto-fix using AI.
- ## `install`
  - Action: Installs a Litio package.
  - parameters:
    - `module`: The name of the module to install, must be in format `author/module` or `author/module@version`.
    - `--upgrade`(aliases: `-u`): install the latest version of the module.
 - ## `uninstall`
  - Action: Uninstalls a Litio package.
  - parameters:
    - `module`: The name of the module to uninstall, must be in format `author/module`.
# Litio config file reference

### The config file must be in YAML format and named `litio.yml`

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

## The expected parameter

- The `comparator` parameter is the way to compare the expected value.
- The `value` parameter is the expected value.
+ you can access the attributes of the returned object using the dot notation. Look like this:
```yaml
...
- add_lists:
    inputs:
      a: [1, 2]
      b: [3, 4]
    expected:
      # the value returned is [1, 2, 3, 4]
      value.0: 1 # access to value[0]
      comparator: Equals
```
you also can use ranges:
```yaml
...
- add_lists:
    inputs:
      a: [1, 2]
      b: [3, 4]
    expected:
      # the value returned is [1, 2, 3, 4]
      value.1;3: 1 # access to the range value[1:3]
      # NOTE: use semicolon(;) to indicate the range(e.g. value.1;3), not the colon(:) because conflict with the yaml syntax
      comparator: Equals
```
you can also use spacing in the range:
```yaml
...
- add_lists:
    inputs:
      a: [1, 2]
      b: [3, 4]
    expected:
      value.;;2: [1, 3] # access to value[::2]
      comparator: Equals
```
you also can access to a key in the dictionary:
```yaml
...
- add_dicts:
    inputs:
      a: {"a": 1, "b": 2}
      b: {"c": 3, "d": 4}
    expected:
      value.a: 1
      comparator: Equals
```
you also can use dot notation multiple times:
```yaml
...
- add_dicts:
    inputs:
      a: {"a": {"b": 1}}
      b: {"c": {"d": 2}}
    expected:
      value.a.b: 1 # access to value["a"]["b"]
      comparator: Equals
```
if function returns an object, you can access to the attributes of that object using the dot notation:
```yaml
...
- create_person_object:
    inputs:
      name: John
      age: 30
    expected:
      value.name: John # access to value.name
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
- `IsNot`
- `IsNone`
- `IsNotNone`
- `IsInstance`
- `IsNotInstance`

# How can i create a module?

### Every module must have a `litio.py` file in root directory.

### Example module for output styles:

#### litio.py
```python
import ... # your dependecies here

def my_own_output_style(args):
    ... # your code here

litio = {
  'output': {
    'my-own-output-style-name': my_own_output_style
  }
}
```

### When your module is ready to use, you can publish it to github and install it using `litio install you/your-module-name` example: `litio install lizardwine/litio-package`

## litio dictionary reference
### you can repleace any litio function
- output: you can add and replace any output style
  - `classic`: classic output
  - `capybara`: capybara output
- options: you can add and replace any option for litio command
  - `--version`: shows the litio version and exit

- sub_commands: you can add and replace any sub command
  - `run`: run the tests in litio.yml
  - `install`: install a module
  - `uninstall`: uninstall a module
- utils: you can add and replace any utility
  - `extract_function_code`: extract the code of a function from a file
  - `Args`: set self attributes from a dictionary
  - `OutputArgs`: an organizer for the output arguments
  - `params_to_dict`: convert a list of parameters to a dictionary
  - `eval_param_values`: evaluate the values of a list of parameters
  - `Kwargs`: set self attributes from a keyword arguments

- tester: you can replace the tester function
  - `test`: test a function with the given inputs and expected values

- ai: you can add or replace any AI powered function
  - `BugFixer`: class for bug fixing
  - `fix_bug`: fix a bug in a function with BugFixer



#### If you module has dependencies, you must add them in `requirements.txt` file in root directory.