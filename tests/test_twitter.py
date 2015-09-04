import os.path as osp
import unittest

import voluptuous
from voluptuous import (
    MultipleInvalid,
)
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma no cover
    from yaml import Loader

import yamlious


class TestTwitter(unittest.TestCase):
    def get_yamlious(self, test):
        f = osp.splitext(__file__)[0] + '.yaml'
        with open(f) as istr:
            content = yaml.load(istr, Loader=Loader)
        return yamlious.from_dict(content[test])

    def test_simple(self):
        self.assertEqual(
            self.get_yamlious('simple'),
            ({
                'q': str,
                'per_page': str,
                'page': int,
            }, {})
        )

    def test_semantic_key_is_empty_dict(self):
        self._semantic_scenario('key_is_empty_dict')

    def test_semantic_key_is_string(self):
        self._semantic_scenario('key_is_string')

    def test_semantic_key_repeat_key(self):
        self._semantic_scenario('key_repeat_key')

    def _semantic_scenario(self, scenario):
        schema, options = self.get_yamlious('semantic_' + scenario)
        schema = voluptuous.Schema(schema, **options)

        # Test 'q' parameter

        with self.assertRaises(MultipleInvalid):
            # 'q' is missing
            schema({'foo': 'bar', 'per_page': 1})

        with self.assertRaises(MultipleInvalid):
            # 'q' must be a str
            schema({'q': 42, 'per_page': 1})

        with self.assertRaises(MultipleInvalid):
            # 'q' must not be an empty string
            schema({'q': '', 'per_page': 1})
        schema({u'q': "valid_value", 'per_page': 1})
        schema({'q': "valid_value", 'per_page': 1})

        # Test 'per_page' parameter

        # 'per_page' is optional
        val = schema({'q': 'not-empty'})
        # but have a default value
        self.assertEqual(val.get('per_page'), 5)

        with self.assertRaises(MultipleInvalid):
            # 'per_page' must be an integer
            schema({'q': 'not-empty', 'per_page': 'foo'})

        with self.assertRaises(MultipleInvalid):
            # 'per_page' must be between 1 and 20
            schema({'q': 'not-empty', 'per_page': 0})

        with self.assertRaises(MultipleInvalid):
            # 'per_page' must be between 1 and 20
            schema({'q': 'not-empty', 'per_page': 21})
        schema({'q': 'not-empty', 'per_page': 1})
        schema({'q': 'not-empty', 'per_page': 10})
        schema({'q': 'not-empty', 'per_page': 20})

        # Test 'page' parameter
        val = schema({'q': 'not-empty'})
        self.assertTrue('page' not in val)

        with self.assertRaises(MultipleInvalid):
            # 'page' must be an integer
            schema({'q': 'not-empty', 'page': "42"})

        with self.assertRaises(MultipleInvalid):
            # 'page' must be an integer greater than 0
            schema({'q': 'not-empty', 'page': -1})

        schema({'q': 'not-empty', 'page': 0})
        schema({'q': 'not-empty', 'page': 1})


if __name__ == '__main__':
    unittest.main()
