import pandas as pd

# we need some URI

print("--- import data -----")
data = pd.read_csv("titanic/titanic.csv")
print(data.dtypes)
print(data.shape)

print("---how clean is the data---")
columns = list(data.columns)
rows    = data.shape[0]
print(columns)
print(data[columns].isna().sum()/rows)

### The data needs mostly some work with cabin, home.dest,  age, and boat.

print("---cleaning the data ----")

data.loc[data["name"].isna(),"name"] = "unknown"
data.loc[data["cabin"].isna(),"cabin"] = "unknown"
data.loc[data["boat"].isna(),"boat"] = "unknown"
data.loc[data["sex"].isna(),"sex"] = "unknown"
data.loc[data["embarked"].isna(),"embarked"] = "unknown"
data.loc[data["ticket"].isna(),"ticket"] = "unknown"
data.loc[data["pclass"].isna(),"pclass"] = 0
data.loc[data["survived"].isna(),"survived"] = 0
data.loc[data["fare"].isna(),"fare"] = -1
data.loc[data["home.dest"].isna(),"home.dest"] = "unknown"
data.loc[data["body"].isna(),"body"] = -1
data.loc[data["parch"].isna(),"parch"] = 0
data.loc[data["sibsp"].isna(),"sibsp"] = 0
data.loc[data["age"].isna(),"age"] = 0

print(data[columns].isna().sum()/rows)

print("----write cleaned data---")
data.to_csv("titanic/cleaned_titanic.csv",index=False)