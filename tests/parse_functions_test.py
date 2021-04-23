import json

import pytest
from ijson import IncompleteJSONError
from rdflib import BNode, Graph, Literal, Namespace
from rdflib.compare import graph_diff, to_isomorphic

from construction_site import parse_dict, parse_json

NS = Namespace("http://localhost/")


def dump_nt_sorted(g, prefix=""):
    for l in sorted(g.serialize(format="nt").splitlines()):
        if l:
            print(prefix + l.decode("ascii"))


def assert_graph_isomorphic(given, expected):
    iso1 = to_isomorphic(given)
    iso2 = to_isomorphic(expected)

    in_both, in_first, in_second = graph_diff(iso1, iso2)
    dump_nt_sorted(in_first, "got: ")
    dump_nt_sorted(in_second, "expected: ")

    assert iso1 == iso2


def assert_json_isomorphic(j, expected):
    g = Graph()
    for t in parse_json(j, namespace=NS):
        g.add(t)

    assert_graph_isomorphic(g, expected)


def assert_dict_isomorphic(d, expected):
    g = Graph()
    for t in parse_dict(d, namespace=NS):
        g.add(t)

    assert_graph_isomorphic(g, expected)


def assert_isomorphic(j, expected):
    assert_json_isomorphic(j, expected)
    assert_dict_isomorphic(json.loads(j), expected)


def test_invalid():
    with pytest.raises(IncompleteJSONError):
        assert_json_isomorphic("{ ", Graph())


def test_empty():
    assert_isomorphic("[ { } ]", Graph())


def test_object():
    expected = Graph()
    expected.add((BNode(), NS.key, Literal("val")))

    assert_isomorphic('{ "key": "val" }', expected)


def test_duplicate_keys():
    expected = Graph()
    subject = BNode()
    expected.add((subject, NS.key, Literal("val1")))
    expected.add((subject, NS.key, Literal("val2")))
    expected.add((subject, NS.key, Literal("val3")))
    expected.add((subject, NS.key, Literal("val4")))

    assert_json_isomorphic(
        '{ "key": "val1", "key": [ "val2" ], "key": [ "val3" ], "key": "val4" }',
        expected,
    )


def test_nested_objects():
    expected = Graph()
    b1 = BNode()
    b2 = BNode()
    expected.add((b1, NS.before, Literal("val")))
    expected.add((b1, NS.obj, b2))
    expected.add((b2, NS.key, Literal("val")))
    expected.add((b1, NS.after, Literal("val")))

    assert_isomorphic(
        '{ "before": "val", "obj": { "key": "val" }, "after": "val" }', expected
    )


def test_mixed_arrays():
    expected = Graph()
    b1 = BNode()
    b2 = BNode()
    b3 = BNode()
    expected.add((b1, NS.array, Literal("before")))
    expected.add((b1, NS.array, b2))
    expected.add((b2, NS.key, Literal("val")))
    expected.add((b1, NS.array, Literal("middle")))
    expected.add((b1, NS.array, b3))
    expected.add((b3, NS.key1, Literal("val1")))
    expected.add((b1, NS.array, Literal("after")))

    assert_isomorphic(
        '{ "array": [ "before", { "key": "val" }, "middle", { "key1": "val1" }, "after" ] }',
        expected,
    )


def test_nested_arrays():
    expected = Graph()
    b1 = BNode()
    b2 = BNode()
    expected.add((b1, NS.array, Literal("before")))
    expected.add((b1, NS.array, Literal("val")))
    expected.add((b1, NS.array, b2))
    expected.add((b2, NS.key, Literal("val")))
    expected.add((b1, NS.array, Literal("after")))

    assert_isomorphic(
        '{ "array": [ "before", [ "val", { "key": "val" } ], "after" ] }', expected
    )


def test_literal_values():
    expected = Graph()
    b1 = BNode()

    expected.add((b1, NS.bool_true, Literal(True)))
    expected.add((b1, NS.bool_false, Literal(False)))
    expected.add((b1, NS.int, Literal(42)))
    expected.add((b1, NS.float, Literal(66.6)))

    assert_isomorphic(
        '{ "bool_true": true, "bool_false": false, "int": 42, "float": 66.6 }', expected
    )


def test_null_value():
    assert_isomorphic('{ "key": null }', Graph())
