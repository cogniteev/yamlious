import copy
import os.path as osp
import unittest

import voluptuous

from yamlious import from_yaml


class TestComplete(unittest.TestCase):
    @classmethod
    def get_yaml_file(cls, test_file):
        return osp.splitext(__file__)[0] + '.yaml'

    def test_docido_crawler(self):
        with open(self.get_yaml_file('docido-crawler')) as istr:
            schema, options = from_yaml(istr)
        schema = voluptuous.Schema(schema, **options)

        valid_item = {
            'id': 'my_id',
            'title': 'my_title',
            'description': 'my_description',
            'date': 12345,
            'kind': 'my_kind',
            'author': {
                'name': 'my_name'
            },
            'attachments': [],
        }
        valid_item_one_attachment = copy.deepcopy(valid_item)
        valid_item_one_attachment['attachments'].append({
            'title': 'my_title1',
            'origin_id': 'my_origin_id1',
            'type': 'my_type1',
            'description': 'my_description1',
        })
        valid_item_two_attachment = copy.deepcopy(valid_item_one_attachment)
        valid_item_two_attachment['attachments'].append({
            'title': 'my_title2',
            'origin_id': 'my_origin_id2',
            'type': 'my_type2',
            'description': 'my_description2',
        })
        self.assertEqual(schema(valid_item), valid_item)
        self.assertEqual(
            schema(valid_item_one_attachment),
            valid_item_one_attachment
        )
        self.assertEqual(
            schema(valid_item_two_attachment),
            valid_item_two_attachment
        )
