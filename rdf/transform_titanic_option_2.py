#from typing import Dict, List, Any

import pandas as pd




#from owlready2 import *

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD

print("---import cleaned data ---")
# Did not work after reverting to Python 3.9
data = pd.read_csv("~/Documents/GitHub/titanic_semantic_web/rdf/titanic/cleaned_titanic.csv")
print(data.dtypes)
print(data.shape)

# Uses https://stackoverflow.com/questions/43524943/creating-rdf-file-using-csv-file-as-input
# to extract passenger first.

p_data = data.loc[:,["name","sex","age"]]
print(p_data.dtypes)
print(p_data.shape)

