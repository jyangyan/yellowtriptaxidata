import requests
import os
from bs4 import BeautifulSoup
import pyarrow.parquet as pq
import configparser
import pandas as pd
from sqlalchemy import create_engine
import pyodbc
from sqlalchemy import text  # Import the text function for handling raw SQL

class yellow_trip(object):
    def __init__(self):
        config_loc = "C:\\Users\\Samae\\PycharmProjects\\pythonProject\\yellowtriptaxi\\config.ini"
        config = configparser.RawConfigParser()
        config.read(config_loc)
        self.url = config['PARQUET']['url']
        self.desired_month = config['PARQUET']['desired_month']
        self.desired_file_type = config['PARQUET']['desired_file_type']
        self.server = config['SQL']['server']
        self.database = config['SQL']['database']
        self.trusted_connection = config['SQL']['trusted_connection']
        self.driver = config['SQL']['driver']
        self.parquet_file_path = config['SQL']['parquet_file_path']
        self.table_name = config['SQL']['table_name']
        self.sql_file_path = config['SQL']['sql_file_path']

    def download_data(self):

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("a")

        parquet_links = [link["href"] for link in links if link["href"].endswith(".parquet")
                         and self.desired_month in link["href"]
                         and self.desired_file_type in link["href"]]

        for parquet_link in parquet_links:
            file_name = parquet_link.split("/")[-1]
            if not os.path.exists(file_name):
                parquet_response = requests.get(parquet_link)
                with open(file_name, "wb") as f:
                    f.write(parquet_response.content)
                print(f"Downloaded {file_name}")
            else:
                print(f"File {file_name} already exists. Skipping download.")

        for parquet_link in parquet_links:
            file_name = parquet_link.split("/")[-1]
            table = pq.read_table(file_name)
            print("Schema:")
            print(table.schema)
            df = table.to_pandas()
            print(df.head())

    def load_data(self):

        conn_str = f'mssql+pyodbc://{self.server}/{self.database}?trusted_connection={self.trusted_connection}&driver={self.driver}'
        engine = create_engine(conn_str)

        df = pd.read_parquet(self.parquet_file_path)
        table_name = self.table_name

        df.to_sql(table_name, con=engine, if_exists='replace', index=False)

        print("Data loaded successfully into SQL Server.")

    def execute_sp(self):

        conn_str = f'mssql+pyodbc://{self.server}/{self.database}?trusted_connection={self.trusted_connection}&driver={self.driver}'
        engine = create_engine(conn_str)

        sql_file_path = self.sql_file_path  # Corrected part

        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        with engine.connect() as conn:
            sp_query = text(sql_script)
            conn.execute(sp_query)

        print("Stored procedure executed successfully.")


if __name__ == "__main__":
    yellow_data = yellow_trip()
    yellow_data.download_data()
    yellow_data.load_data()
    yellow_data.execute_sp()

