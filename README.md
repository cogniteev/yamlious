## Yamlious Python module

Yamlious is a Python module that allows you to declare
[voluptous](https://github.com/alecthomas/voluptuous) schemas in YAML format.

This module is at a very early stage, only tested according to our use-cases.

## Installation

```shell
$ pip install yamlious
```

## Usage

```python
import voluptuous
import yamlious

# build voluptuous schema
with open('my-schema.yaml') as istr:
  _schema, options = yamlious.from_yaml(istr)
  schema = voluptuous.schema(_schema, **options)
# check your data
schema({
  'firstname': 'John',
  'lastname': 'Doe',
})
```

## Syntax

a yamlious schema is a `dict` of 2 keys:

* `content`: a mandatory `dict` describing the first argument given to the `voluptuous.Schema` function.
* `options`: an optional `dict` passed as `**kwargs` to the `voluptuous.Schema` function.

### Show me an example

The following examples are extracted from the voluptuous documentation.

#### Twitter user search API schema
```python
>>> from voluptuous import Schema
>>> schema = Schema({
...   'q': str,
...   'per_page': int,
...   'page': int,
... })
```

Yamlious can create the very same schema with the following YAML input:

```yaml
content:
    q: str
    per_page: str
    page: int
```

### Twitter user search API schema with semantic

```python
>>> from voluptuous import Required, All, Length, Range
>>> schema = Schema({
...   Required('q'): All(str, Length(min=1)),
...   Required('per_page', default=5): All(int, Range(min=1, max=20)),
...   'page': All(int, Range(min=0)),
... })
```

the corresponding Yamlious file is:
```yaml
content:
    q:
        key: Required
        All:
            - str
            - Length:
                min: 1
    per_page:
        key:
            Required:
                default: 5
        All:
          - int
          - Range:
              min: 1
              max: 20
    page:
        All:
            - int
            - Range:
                min: 0
```

Regarding the `q` key description:

* `key` specifies the *key* part of `Required('q'): All(str, Length(min=1)),`
* There is no need to repeat `q` to `Required` argument, because inside `key`, there is no need to do it.
* The key function can be passed as `string` if there is no extra argument to pass, like `q` for instance.
* There are possible variants:
        
    ```yaml
    # key function is a dict without argument
    q:
        key:
          Required:
    ```
        
    ```yaml
    # provides all arguments to function, even the key:
    q:
        key:
            Required:
                - q
    ```


## Tests

You can use `tox` to run the test-suite on every supported platform:

```shell
# Install and load virtualenv
$ pip install virtualenv
$ virtualenv .env
$ .env/bin/activate
# Install tox
$ pip install tox
# Run the test suites
$ tox
```

## Issues

Pull-requests are welcome. You can also submit your issues to the
[issues tracker](https://github.com/cogniteev/yamlious/issues)

## License

`yamlious` is licensed under the Apache License, Version 2.0.
See [LICENSE](LICENSE) file for full license text.
