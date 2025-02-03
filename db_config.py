import psycopg2

# PostgreSQL Bağlantı Bilgileri
DB_CONFIG = {
    "dbname": "connexease_crm_db",
    "user": "zTRsUVcSV3jjWPOE",
    "password": "fj2Nm8Ra02LZzhbNJO6CNS4EUzfWDktH",
    "host": "connexease-crm-postgresql.chogki0uo1cy.eu-central-1.rds.amazonaws.com",
    "port": "5432"
}

def get_db_connection():
    """PostgreSQL bağlantısını açar ve döner."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"PostgreSQL Bağlantı Hatası: {e}")
        return None
