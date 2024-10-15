import os

DB_HOST = "my-postgresql.postgres.database.azure.com"
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

QUERY_RESPONSE_SIZE = 25
