"""
Database connector for training ML models from PostgreSQL/MySQL
This allows you to train models directly from your database
"""
import os
import pandas as pd

# Database configuration (set via environment variables for security)
DB_TYPE = os.environ.get('DB_TYPE', 'mysql')  # mysql or postgresql
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
DB_NAME = os.environ.get('DB_NAME', 'u412552698_dbhanapbahay')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', '')

def get_connection():
    """Get database connection based on DB_TYPE"""
    if DB_TYPE == 'postgresql':
        import psycopg2
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
    else:  # mysql
        import mysql.connector
        return mysql.connector.connect(
            host=DB_HOST,
            port=int(DB_PORT),
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )

def fetch_training_data(query=None):
    """
    Fetch training data from database

    Example query:
    SELECT
        capacity as Capacity,
        bedroom as Bedroom,
        unit_sqm,
        property_type as Type,
        kitchen as Kitchen,
        kitchen_type as 'Kitchen type',
        gender_specific as 'Gender specific',
        pets as Pets,
        location as Location,
        price
    FROM tblistings
    WHERE is_verified = 1
        AND is_deleted = 0
        AND price IS NOT NULL
        AND price > 0
    """
    if query is None:
        # Default query for HanapBahay schema
        query = """
        SELECT
            capacity,
            bedroom,
            unit_sqm,
            property_type,
            kitchen,
            kitchen_type,
            gender_specific,
            pets,
            COALESCE(location, 'Unknown') as location,
            price
        FROM tblistings
        WHERE is_verified = 1
            AND is_deleted = 0
            AND price IS NOT NULL
            AND price > 0
            AND unit_sqm IS NOT NULL
            AND unit_sqm > 0
        """

    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()

    return df

def calculate_derived_features(df):
    """Add derived features like cap_per_bedroom"""
    df = df.copy()

    # Rename columns to match Colab format
    df = df.rename(columns={
        'capacity': 'Capacity',
        'bedroom': 'Bedroom',
        'unit_sqm': 'unit_sqm',
        'property_type': 'Type',
        'kitchen': 'Kitchen',
        'kitchen_type': 'Kitchen type',
        'gender_specific': 'Gender specific',
        'pets': 'Pets',
        'location': 'Location',
        'price': 'price'
    })

    # Calculate cap_per_bedroom
    df['cap_per_bedroom'] = df['Capacity'] / df['Bedroom'].replace(0, pd.NA)
    df['cap_per_bedroom'] = df['cap_per_bedroom'].fillna(df['Capacity'])

    return df

if __name__ == "__main__":
    # Test database connection
    print("Testing database connection...")
    try:
        df = fetch_training_data()
        print(f"Successfully fetched {len(df)} rows")
        print(f"\nColumns: {df.columns.tolist()}")
        print(f"\nFirst few rows:\n{df.head()}")

        df = calculate_derived_features(df)
        print(f"\nWith derived features:\n{df.columns.tolist()}")

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set environment variables:")
        print("  DB_TYPE (mysql or postgresql)")
        print("  DB_HOST")
        print("  DB_USER")
        print("  DB_PASS")