import functools
import inspect
import logging
import re

import voluptuous
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:  # pragma: no cover
    from yaml import Loader


__version__ = '0.2.1'

TYPE_RE = re.compile('[a-zA-Z][_a-zA-Z0-9]*')
LOGGER = logging.getLogger(__name__)


def merge_dict(lhs, rhs):
    """ Merge content of a dict in another

    :param: dict: lhs
      dict where is merged the second one
    :param: dict: rhs
      dict whose content is merged
    """
    assert isinstance(lhs, dict)
    assert isinstance(rhs, dict)
    for k, v in rhs.iteritems():
        if k not in lhs:
            lhs[k] = v
        else:
            lhs[k] = merge_dict(lhs[k], v)
    return lhs


def merge_dicts(*dicts):
    """ Merge a collection of dict """
    return reduce(merge_dict, list(dicts))


def from_dict(data):
    """ Build input parameters of `voluptuous.Schema` constructors from a
    Python `dict` description.

    :param :dict: data:
       same structure than what the YAML loader below loads.

    :return: tuple of 2 arguments. The first argument is the dict that must
      be given to `voluptuous.Schema` class. The second one is the optional
      `kwargs` argument. Example:

      >>> schema, options = from_dict(dict)
      >>> voluptuous.Schema(schema, **options)
    """
    assert isinstance(data, dict)
    options = data.get('options', {})
    content = data.get('content', {})

    def get_type(key, type_str):
        if TYPE_RE.match(type_str) is not None:
            return eval(type_str)
        else:
            raise Exception((u"Value of key '{}' must match the "
                             u"following regular expression: {}").format(
                 key, TYPE_RE.pattern
             ))

    def to_func(key, func_str, args):
        if isinstance(args, (str, float, int)):
            # It is very dangerous to try to convert every string argument
            # to a Python type...
            try:
                args = get_type(key, args)
            except:
                pass
        elif isinstance(args, list):
            if any(args) and key is not None and args[0] == key:
                args.pop(0)
                if len(args) == 1:
                    return to_func(key, func_str, args[0])
            for i in range(len(args)):
                arg = args[i]
                if isinstance(arg, dict):
                    if len(arg) > 1:
                        raise Exception(
                            u"Invalid parameter {} in function {}".format(
                                arg.keys()[0], func_str
                            ))
                    elif not any(arg):
                        raise Exception(
                            u"Empty dict parameter in function {}".format(
                                func_str
                            )
                        )
                    else:
                        args[i] = to_func(None, *(next(arg.iteritems())))
                elif isinstance(arg, (str, int, float)):
                    try:
                        args[i] = get_type(key, arg)
                    except:
                        pass
                else:
                    raise NotImplementedError(
                        u"Unhandled parameter {} in function {}".format(
                            arg, func_str
                        )
                    )
        elif isinstance(args, dict):
            pass  # FIXME: might be required to recursively evaluate values
        elif args is None and key is not None:
            pass
        else:
            return get_type(key, func_str)

        func = getattr(voluptuous, func_str, None)
        if func is None:
            return (func_str, args)
        else:
            call = u'{}('.format(func.__name__)
            if key is not None:
                func = functools.partial(func, key)
                call += '%r, ' % key
            call += '%r)' % args
            LOGGER.debug(u'yamlious call: {}'.format(call))
            if isinstance(args, list):
                return func(*args)
            elif isinstance(args, dict):
                return func(**args)
            else:
                return func(args)

    def extract_content(content, schema=None):
        schema = schema or dict()
        for k, v in content.iteritems():
            k = str(k)
            if isinstance(v, (int, str, float)):
                schema[k] = get_type(k, str(v))
            elif inspect.isclass(v):
                schema[k] = v
            elif isinstance(v, list):
                schema[k] = [extract_content(e) for e in v]
            elif isinstance(v, dict):
                key = v.pop('key', None)
                nested = v.pop('nested', None)
                if key is not None:
                    # Special key for Required('bla')
                    if isinstance(key, basestring):
                        key = {key: None}
                    if not isinstance(key, dict):
                        raise Exception("'key' value must be a dict")
                    elif len(key) != 1:
                        raise Exception("'key' dict value size must be 1")
                    k = to_func(k, *next(key.iteritems()))
                if nested is not None and any(v):
                    raise Exception((
                        "In key {}: cannot have both nested dict and extra"
                        u"key(s): {}").format(
                            k, ','.join(map(str(v.keys())))
                        ))
                if nested is not None:
                    schema[k] = extract_content(nested)
                elif len(v) > 1:
                    raise Exception(
                        "In key " + k +
                        ": cannot have more than function value"
                    )
                elif len(v) == 0:
                    raise Exception(
                        "In key " + str(k) +
                        ": value cannot be an empty dict"
                    )
                else:
                    schema[k] = to_func(None, *next(v.iteritems()))

        return schema
    return (extract_content(content), options)


def from_yaml(*streams):
    """ Build voluptuous.Schema function parameters from a streams of YAMLs
    """
    return from_dict(merge_dicts(*map(
        lambda f: yaml.load(f, Loader=Loader),
        list(streams)
    )))
