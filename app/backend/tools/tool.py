import pandas as pd
import duckdb

def querycsv(query: str) -> str:
    """
query resource.csv using SQL only. The resource.csv contains subject and marks column.
Table name in SQL is always df
    """
    df = pd.read_csv("resources/resource.csv")
    query = query.replace("resource.csv", "df")

    mod_df = duckdb.query(query).df()
    return mod_df.to_string()