import os.path as osp
import unittest

from voluptuous import (
    MultipleInvalid,
    Schema,
)
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma no cover
    from yaml import Loader

import yamlious


class TestExclusive(unittest.TestCase):
    def get_yamlious(self, test):
        f = osp.splitext(__file__)[0] + '.yaml'
        with open(f) as istr:
            content = yaml.load(istr, Loader=Loader)
        return yamlious.from_dict(content[test])

    def test_type_only(self):
        schema, options = self.get_yamlious('type_only')
        schema = Schema(schema, **options)

        self.assertEquals(
            schema(dict(alpha=42)),
            dict(alpha=42)
        )
        self.assertEquals(
            schema(dict(beta=42)),
            dict(beta=42)
        )
        with self.assertRaises(MultipleInvalid) as exc:
            schema(dict(alpha='42'))
        self.assertEquals(
            str(exc.exception),
            "expected int for dictionary value @ data['alpha']"
        )
        with self.assertRaises(MultipleInvalid) as exc:
            schema(dict(alpha=42, beta=43))
        self.assertEquals(
            str(exc.exception),
            "two or more values in the same group of exclusion 'angles'"
        )

    def test_nested_schema(self):
        schema, options = self.get_yamlious('nested_schema')
        schema = Schema(schema, **options)

        valid_email_auth = dict(email=dict(email='foo@bar.com',
                                           password='secret'))
        self.assertEqual(schema(valid_email_auth), valid_email_auth)
        valid_internal_auth = dict(internal=dict(secret_key='secret'))
        self.assertEqual(schema(valid_internal_auth), valid_internal_auth)
        valid_social_auth = dict(social=dict(social_network='twitter',
                                             token='token42'))
        self.assertEqual(schema(valid_social_auth), valid_social_auth)
        with self.assertRaises(MultipleInvalid) as exc:
            invalid = valid_email_auth.copy()
            invalid.update(valid_internal_auth)
            schema(invalid)
        self.assertEquals(
            str(exc.exception),
            "two or more values in the same group of exclusion 'auth'"
        )

    def test_type_only_required(self):
        schema, options = self.get_yamlious('type_only_required')
        schema = Schema(schema, **options)

        self.assertEquals(
            schema(dict(foo=42)),
            dict(foo=42)
        )
        with self.assertRaises(MultipleInvalid) as exc:
            schema(dict(foo='42'))
        self.assertEquals(
            str(exc.exception),
            "expected int for dictionary value @ data['foo']"
        )


if __name__ == '__main__':
    unittest.main()
