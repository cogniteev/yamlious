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
