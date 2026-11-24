
import pandas as pd
import pymysql
from pathlib import Path
from getpass import getpass

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"

print("========== MYSQL DATA IMPORT ==========")

# Database connection details
host = "localhost"
user = input("MySQL username (default root): ").strip() or "root"
password = getpass("Enter MySQL password: ")

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    database="user_behaviour_analytics",
    port=3306
)

datasets = {
    "users": "users_clean.csv",
    "courses": "courses_clean.csv",
    "enrollments": "enrollments_clean.csv",
    "user_activity": "user_activity_clean.csv"
}

try:
    with connection.cursor() as cursor:

        for table, filename in datasets.items():

            file_path = DATA_DIR / filename
            df = pd.read_csv(file_path)

            # Convert missing values to SQL NULL
            df = df.astype(object).where(pd.notna(df), None)

            columns = list(df.columns)
            column_names = ", ".join(f"`{col}`" for col in columns)
            placeholders = ", ".join(["%s"] * len(columns))

            query = (
                f"INSERT INTO `{table}` ({column_names}) "
                f"VALUES ({placeholders})"
            )

            records = df.values.tolist()

            cursor.executemany(query, records)

            print(f"{table}: {len(records)} rows imported")

    connection.commit()
    print("\nAll datasets imported successfully!")

    with connection.cursor() as cursor:
        for table in datasets:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            count = cursor.fetchone()[0]
            print(f"{table} total rows: {count}")

except Exception as error:
    connection.rollback()
    print("\nImport failed:", error)

finally:
    connection.close()
