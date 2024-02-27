import requests
import os
from bs4 import BeautifulSoup
import pyarrow.parquet as pq

# Step 1: Fetch the HTML content of the webpage
url = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
response = requests.get(url)

# Step 2: Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Step 3: Find all links on the webpage
links = soup.find_all("a")

# Step 4: Filter links that point to Parquet files for the desired month and file type
desired_month = "2023-01"  # Change this to the desired month
desired_file_type = "yellow_tripdata"  # Change this to the desired file type
parquet_links = [link["href"] for link in links if link["href"].endswith(".parquet")
                 and desired_month in link["href"]
                 and desired_file_type in link["href"]]

# Step 5: Download Parquet files
for parquet_link in parquet_links:
    file_name = parquet_link.split("/")[-1]
    # Check if file already exists to avoid re-downloading
    if not os.path.exists(file_name):
        parquet_response = requests.get(parquet_link)
        with open(file_name, "wb") as f:
            f.write(parquet_response.content)
        print(f"Downloaded {file_name}")
    else:
        print(f"File {file_name} already exists. Skipping download.")

# Step 6: Optionally, you can load the Parquet files using pyarrow for further processing
for parquet_link in parquet_links:
    file_name = parquet_link.split("/")[-1]
    # Load Parquet file using pyarrow
    table = pq.read_table(file_name)
    # Print schema
    print("Schema:")
    print(table.schema)
    # Optionally convert to pandas DataFrame
    df = table.to_pandas()
    # Process DataFrame as needed
    print(df.head())  # Example: Print first few rows
