# import sqlite3
# import csv

# def create_db_from_csv(csv_file, db_file):
#     conn = sqlite3.connect(db_file)
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS financial_data (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             step INTEGER,
#             customer TEXT,
#             age INTEGER,
#             gender TEXT,
#             zipcodeOri TEXT,
#             merchant TEXT,
#             zipMerchant TEXT,
#             category TEXT,
#             amount REAL,
#             fraud INTEGER
#         )
#     ''')
#     with open(csv_file, 'r') as file:
#         reader = csv.DictReader(file)  # Use DictReader for easier mapping
#         for row in reader:
#             cursor.execute('''
#                 INSERT INTO financial_data (step, customer, age, gender, zipcodeOri, merchant, zipMerchant, category, amount, fraud)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#             ''', (
#                 row['step'],
#                 row['customer'],
#                 row['age'],
#                 row['gender'],
#                 row['zipcodeOri'],
#                 row['merchant'],
#                 row['zipMerchant'],
#                 row['category'],
#                 row['amount'],
#                 row['fraud']
#             ))

#     conn.commit()
#     conn.close()

# if __name__ == '__main__':
#     create_db_from_csv('HSBC.csv', 'financial_data.db')

import pymongo
import sqlite3
import csv

def create_db_from_csv(csv_file, mongodb_db_name, mongodb_collection_name, sqlite_db_file):
    # Connect to MongoDB
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    mongo_db = client[mongodb_db_name]
    mongo_collection = mongo_db[mongodb_collection_name]

    # Connect to SQLite
    sqlite_conn = sqlite3.connect(sqlite_db_file)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Create SQLite table if it does not exist
    sqlite_cursor.execute('''
        CREATE TABLE IF NOT EXISTS financial_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            step INTEGER,
            customer TEXT,
            age INTEGER,
            gender TEXT,
            zipcodeOri TEXT,
            merchant TEXT,
            zipMerchant TEXT,
            category TEXT,
            amount REAL,
            fraud INTEGER
        )
    ''')

    # Read CSV file and insert into both databases
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        mongo_data = []
        sqlite_data = []
        for row in reader:
            try:
                step = int(row['step'].strip("'\" "))
                age = int(row['age'].strip("'\" "))
                amount = float(row['amount'].strip("'\" "))
                fraud = int(row['fraud'].strip("'\" "))
            except ValueError:
                continue
            
            # Prepare data for MongoDB
            mongo_data.append({
                'step': step,
                'customer': row['customer'].strip("'\" "),
                'age': age,
                'gender': row['gender'].strip("'\" "),
                'zipcodeOri': row['zipcodeOri'].strip("'\" "),
                'merchant': row['merchant'].strip("'\" "),
                'zipMerchant': row['zipMerchant'].strip("'\" "),
                'category': row['category'].strip("'\" "),
                'amount': amount,
                'fraud': fraud
            })

            # Prepare data for SQLite
            sqlite_data.append((
                step,
                row['customer'].strip("'\" "),
                age,
                row['gender'].strip("'\" "),
                row['zipcodeOri'].strip("'\" "),
                row['merchant'].strip("'\" "),
                row['zipMerchant'].strip("'\" "),
                row['category'].strip("'\" "),
                amount,
                fraud
            ))

        # Insert data into MongoDB
        if mongo_data:
            mongo_collection.insert_many(mongo_data)

        # Insert data into SQLite
        if sqlite_data:
            sqlite_cursor.executemany('''
                INSERT INTO financial_data (
                    step, customer, age, gender, zipcodeOri, merchant, zipMerchant, category, amount, fraud
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sqlite_data)

    # Commit SQLite changes and close connections
    sqlite_conn.commit()
    sqlite_conn.close()
    client.close()

if __name__ == '__main__':
    create_db_from_csv('HSBC.csv', 'financial_data_db', 'financial_data', 'financial_data.db')