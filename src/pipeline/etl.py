import pandas as pd
import os
from sqlalchemy import create_engine


#CONSTANTS
filepath = "data/"
file_names=os.listdir(filepath)

def read_data(filepath: str):
        try:
            red = pd.read_csv(f"{filepath}red.csv")
            rose = pd.read_csv(f"{filepath}rose.csv")
            sparkling = pd.read_csv(f"{filepath}sparkling.csv")
            white = pd.read_csv(f"{filepath}white.csv")

            red.columns = [col.lower() for col in red.columns]
            rose.columns = [col.lower() for col in rose.columns]
            sparkling.columns = [col.lower() for col in sparkling.columns]
            white.columns = [col.lower() for col in white.columns]

            return red, rose, sparkling, white
        except FileNotFoundError:
            print(f"File not found: {filepath}")
            return None
            

def insert_to_db(
    df: pd.DataFrame,
    table_name: str,
    db_host: str="localhost",
    db_user: str="root",
    db_pass: str="root",
    db_name: str="winedb",
):
    connection_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{5432}/{db_name}'
    engine = create_engine(connection_string)
    try:
        df.to_sql(name=table_name, con=engine, if_exists="append", index=False)
        print(f"DataFrame inserted into {table_name} table successfully.")
    except Exception as e:
        print(f"Error inserting DataFrame into {table_name} table: {e}")

def main():
   file_names = os.listdir(filepath)
   red, rose, sparkling, white = read_data(filepath)
   insert_to_db(df=red, table_name="red")
   insert_to_db(df=rose, table_name="rose")
   insert_to_db(df=sparkling, table_name="sparkling")
   insert_to_db(df=white, table_name="white")
if __name__ == "__main__":
    main()
