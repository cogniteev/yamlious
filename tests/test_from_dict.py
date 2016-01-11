import unittest

import voluptuous

from yamlious import from_dict


class TestFromDict(unittest.TestCase):
    def test_from_dict(self):
        """ test Python objects specified in `content`"""
        schema = {
            'options': {
                'required': True,
            },
            'content': {
                'foo': str,
            },
        }
        schema, options = from_dict(schema)
        schema = voluptuous.Schema(schema, **options)
        with self.assertRaises(Exception):
            schema({})
        with self.assertRaises(Exception):
            schema({'foo': 42})
        self.assertEqual(schema({'foo': 'bar'}), {'foo': 'bar'})


if __name__ == '__main__':
    unittest.main()
