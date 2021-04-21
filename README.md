# construction-site: a usable library for RDF construction

Uses:
- rdflib >= 5.0.0



Rough API design:

``` python
ConstructionSite()
.load(file1.json)   # Creates graph from direct json mapping
.construct(query1)  # Creates new graph containing mapping from file1.json graph
.construct(query2)  # Creates new graph containing mapping from file1.json graph
.load(file2.json)   # Creates graph from direct json mapping
.construct(query3)  # Creates new map graph containing mapping from file2.json graph
.collect() # aggregate all constructed graphs into one
.check(shacl) # validate the constructed graph against shacl
.run()

```