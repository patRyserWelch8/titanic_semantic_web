import pandas
import pandas as pd

from owlready2 import *

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD

print("---import cleaned data ---")
data = pd.read_csv("titanic/cleaned_titanic.csv")
print(data.dtypes)
print(data.shape)

# Problem to solve: how does the age difference varies between spouses?
# MODEL
# Each passenger is a person
# A woman is a subclass of a person
# A man is a subclass of a person
# Each passenger is either a woman or a man
# Each passenger may have an age. It may be unknown
# predicates is a  and object https://en.wikipedia.org/wiki/Woman
# predicates is a  and object https://en.wikipedia.org/wiki/Man
# spouse of
# has an oge of or has an unknown age  none
# has as name
# subject data:titanic:passenger:
# has a marital status


#onto = get_ontology("file://titanic_ontology.xml").load()

rdfs = pd.DataFrame(columns=["subject","predicate", "object"])

#print("-----women-----")
#filter_rows = (data["sex"] == "female")
#filter_cols = ["name","sex","age","sibsp","parch"]
#women = data.loc[filter_rows,filter_cols]
#print(women)

class Passenger_RDF:
    def __init__(self, anIndex: int, aName : str, aGender : str, anAge: float, someSibSp : int, someParch: int):
        self.uri: str    = "data:titanic:passenger:" + str(anIndex)
        self.name: str   = aName
        self.age: float  = anAge
        self.gender:str  = aGender
        self.sibsp:int   = someSibSp
        self.Parch:int   = someParch
        self._IS_A : str = "is_a"
        self._HAS_A_NAME : str = "has_a_name"
        self._HAS_A_MARITAL_STATUS : str = "has_a_marital_status"
        self._HAS_AN_AGE_OF : str = "has_an_age_of"
    def is_a(self) -> pd.DataFrame:
        if self.gender.__eq__("female"):
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._IS_A,
                                 "object": "https://en.wikipedia.org/wiki/Woman"},
                                 index=[0])
        if self.gender.__eq__("male"):
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._IS_A,
                                 "object": "https://en.wikipedia.org/wiki/Man"},
                                index=[0])
        else:
            return pd.DataFrame({"subject":self.uri,
                                 "predicate": self._IS_A,
                                 "object": "unknown gender"},
                                index=[0])
    @property
    def has_a_name(self) -> pd.DataFrame:
        if self.name.__contains__('('):
            name = self.name.split("(")
            name = name[1]
            name = name[:-1]
        if self.name.__contains__("unknown"):
            name = self.name
        else:
            name = self.name.split(", ")
            surname = name[0]
            if len(name) <= 0:
                name = name[0]
            else:
                first_name = str(name[1])
                first_name = first_name.split(". ")
                first_name = first_name[1]
                name = first_name + " " + surname
        return pd.DataFrame({"subject": self.uri,
                             "predicate": self._HAS_A_NAME,
                             "object": name},
                            index=[0])
    def has_a_marital_status(self) -> pd.DataFrame:
        if self.name.__contains__('Miss.') or self.name.__contains__('Master.'):
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._HAS_A_MARITAL_STATUS,
                                 "object": "https://en.wikipedia.org/wiki/Single_person"},
                                index=[0])
        if self.name.__contains__('Mrs.'):
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._HAS_A_MARITAL_STATUS,
                                 "object": "https://en.wikipedia.org/wiki/Marriage"},
                                index=[0])
        if self.name.__contains__('Mr.') and self.sibsp > 0:
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._HAS_A_MARITAL_STATUS,
                                 "object": "https://en.wikipedia.org/wiki/Marriage"},
                                index=[0])
        else:
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._HAS_A_MARITAL_STATUS,
                                  "object": "Unknown"},
                                index=[0])
    def has_an_age_of(self) -> pd.DataFrame:
        if self.age > 0:
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._HAS_AN_AGE_OF,
                                 "object": self.age},
                                index=[0])
        else:
            return pd.DataFrame({"subject": self.uri,
                                 "predicate": self._HAS_AN_AGE_OF,
                                 "object": "Unknown"},
                                index=[0])
for row in data.itertuples():
    rdf = Passenger_RDF(row.Index, row.name, row.sex, row.age, row.sibsp, row.parch)
    is_a = rdf.is_a()
    rdfs = pd.concat([rdfs.loc[:],is_a]).reset_index(drop=True)
    has_a_name = rdf.has_a_name
    rdfs = pd.concat([rdfs.loc[:], has_a_name]).reset_index(drop=True)
    has_a_marital_status = rdf.has_a_marital_status()
    rdfs = pd.concat([rdfs.loc[:], has_a_marital_status]).reset_index(drop=True)
    has_an_age_of = rdf.has_an_age_of()
    rdfs = pd.concat([rdfs.loc[:], has_an_age_of]).reset_index(drop=True)

rdfs.to_csv("titanic/rdf_titanic.csv")
