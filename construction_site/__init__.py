"""
construction-site.

A usable and scalable API for RDF construction.
"""

__version__ = "0.0.2"
__author__ = 'Miel Vander Sande'
__credits__ = 'meemoo vzw'

from .parse_functions import parse_json, parse_dict
from .airflow.hooks.sparql_update import SparqlUpdateHook
#from .construction_site import ConstructionSite