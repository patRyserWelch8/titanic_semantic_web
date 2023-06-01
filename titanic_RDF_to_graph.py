### https://github.com/SemanticLab/simple-csv-to-rdf/blob/master/convert.py
import csv
from csv import DictReader

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD
import pandas as pd

data = pd.DataFrame(columns=["subject","predicate", "object"])

#input_file: DictReader[csv] = csv.DictReader(open("rdf_titanic.csv"))

# make a graph
output_graph = Graph()
for row in data.itertuples():

	#{'Subject Label': 'Pearl Wilmer Booker', 'Subject URI': 'None', 'Predicate Label': 'Daughter Of', 'Predicate URI': '', 'Predicate Symmetry': 'Asymmetric', 'Object Label': 'Mary Booker', 'Object URI': 'None'}
	# make a literal and add it
	output_graph.add((URIRef(row['subject']), RDFS.label, Literal(row['subject'], lang='en')) )

	# make a triple with the object as uri
	output_graph.add(  (URIRef(row['subject']), URIRef(row['predicate']), URIRef(row['object'])) )



output_graph.serialize(destination='titanic/titanic_graph.nt', format='nt')


import pandas as pd

from rdflib.graph import Graph