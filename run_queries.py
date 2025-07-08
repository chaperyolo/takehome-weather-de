import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "db/weather_data.db")
QUERIES_DIR = os.getenv("QUERIES_DIR", "queries")

def run_query(file_name):
    '''runs a sql query and prints the result'''
    query_path = os.path.join(QUERIES_DIR, file_name)
    if not os.path.exists(query_path):
        print(f"Query file '{file_name}' not found in '{QUERIES_DIR}'")
        return
    
    with open(query_path, "r") as file:
        query = file.read()

    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(query, conn)

    print(f"\nResult of '{file_name}':")
    print(df)

if __name__ == "__main__":
    print("running sql queries...\n")
    #this will run all .sql files in the queries folder
    for file in os.listdir(QUERIES_DIR):
        if file.endswith(".sql"):
            run_query(file)