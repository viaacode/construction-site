import pytest

from construction_site.airflow.hooks.sparql_update import SparqlUpdateHook


def test_construction():
    SparqlUpdateHook(method="GET")
