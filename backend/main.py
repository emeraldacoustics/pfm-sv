import json
from pymongo import MongoClient
from utils import load_csv, _extract_file
import requests
from lambda_decorators import cors_headers
 
def initialize_collection(collection_name, url):
    client = MongoClient('mongodb+srv://douglasletz56:UE17m4lk8DNi9mbu@cluster0.lgpz914.mongodb.net/')
    db = client['pfm-sv']
    collection = db[collection_name]
    collection.drop()
    response = requests.get(url, stream=True)
    csv_content = response.content.decode('utf-8')
    data = load_csv(csv_content)
    if data:
        collection.insert_many(data)
        client.close()
        return f"Successfully initialized {collection_name}."
    else:
        client.close()
        return f"Failed to load data for {collection_name}."

@cors_headers
def initialize_products(event, context):
    result_message = initialize_collection('products', 'https://pfm-sv.s3.amazonaws.com/product_master.csv')
    response = {
        "statusCode": 200,
        "body": result_message
    }
    return response

@cors_headers
def initialize_populations(event, context):
    result_message = initialize_collection('populations', 'https://pfm-sv.s3.amazonaws.com/population_master.csv')
    response = {
        "statusCode": 200,
        "body": result_message
    }
    return response

@cors_headers
def lookup_products(event, context):    
    client = MongoClient('mongodb+srv://douglasletz56:UE17m4lk8DNi9mbu@cluster0.lgpz914.mongodb.net/')
    db = client['pfm-sv']
    productDB = db["products"]

    query_params = event.get('queryStringParameters', {})
    param_value = query_params.get('url')
    
    response = requests.get(param_value, stream=True)
    csv_content = response.content.decode('utf-8')
    data = load_csv(csv_content)

    headers = ["Zip", "Product", "Recorded", "ORG User", "Modified User"]
    results = []
    results.append(headers)
    
    for row in data:
        document = productDB.find_one(row)
        new_data = []
        for header in headers:
            if document and document[header]:
                new_data.append(json.dumps(document[header]))
            else:
                new_data.append('N/A')
        new_data[0] = row['Zip']
        results.append(new_data)

    client.close()

    response = {
        "statusCode": 200,
        "body": json.dumps(results)
    }

    return response

@cors_headers
def lookup_populations(event, context):    
    client = MongoClient('mongodb+srv://douglasletz56:UE17m4lk8DNi9mbu@cluster0.lgpz914.mongodb.net/')
    db = client['pfm-sv']
    populationDB = db["populations"]

    query_params = event.get('queryStringParameters', {})
    param_value = query_params.get('url')
    
    response = requests.get(param_value, stream=True)
    csv_content = response.content.decode('utf-8')
    data = load_csv(csv_content)

    headers = ["Zip", "5 Mile Population", "Recorded", "ORG User", "Modified User"]
    results = []
    results.append(headers)
    
    for row in data:
        document = populationDB.find_one(row)
        new_data = []
        for header in headers:
            if document and document[header]:
                new_data.append(json.dumps(document[header]))
            else:
                new_data.append('N/A')
        new_data[0] = row['Zip']
        results.append(new_data)

    client.close()

    response = {
        "statusCode": 200,
        "body": json.dumps(results)
    }

    return response

@cors_headers
def update_products(event, context):    
    client = MongoClient('mongodb+srv://douglasletz56:UE17m4lk8DNi9mbu@cluster0.lgpz914.mongodb.net/')
    db = client['pfm-sv']
    productDB = db["products"]

    query_params = event.get('queryStringParameters', {})
    param_value = query_params.get('url')
    
    response = requests.get(param_value, stream=True)
    csv_content = response.content.decode('utf-8')
    data = load_csv(csv_content)

    headers = ["Zip", "Product", "Recorded", "ORG User", "Modified User"]
    for row in data:
        for header in headers:
            if header == "Modified User":
                continue
            if row.get(header) is None or row.get(header) == "N/A":
                response = {
                    "statusCode": 400,
                    "body": "Data contains 'N/A' value"
                }
                return response
    
    for row in data:
        if row.get("Modified User") and row.get("Modified User") != "N/A":
            productDB.update_one({"Zip": row["Zip"]}, {"$set": row}, upsert=True)

    client.close()

    response = {
        "statusCode": 200,
        "body": json.dumps('Updated Successfully.')
    }

    return response

@cors_headers
def update_populations(event, context):    
    client = MongoClient('mongodb+srv://douglasletz56:UE17m4lk8DNi9mbu@cluster0.lgpz914.mongodb.net/')
    db = client['pfm-sv']
    populationDB = db["populations"]

    query_params = event.get('queryStringParameters', {})
    param_value = query_params.get('url')
    
    response = requests.get(param_value, stream=True)
    csv_content = response.content.decode('utf-8')
    data = load_csv(csv_content)

    headers = ["Zip", "5 Mile Population", "Recorded", "ORG User", "Modified User"]

    for row in data:
        for header in headers:
            if header == "Modified User":
                continue
            if row.get(header) is None or row.get(header) == "N/A":
                response = {
                    "statusCode": 400,
                    "body": "Data contains 'N/A' value"
                }
                return response
    
    for row in data:
        if row.get("Modified User") and row.get("Modified User") != "N/A":
            populationDB.update_one({"Zip": row["Zip"]}, {"$set": row}, upsert=True)

    client.close()

    response = {
        "statusCode": 200,
        "body": "Updated Successfully"
    }

    return response
