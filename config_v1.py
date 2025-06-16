from getpass import getpass

def get_db_config(label="Source"):
    print(f"\n=== Enter {label} Database Details ===")
    host = input("Host (e.g., localhost): ").strip()
    port = input("Port (e.g., 5432): ").strip()
    dbname = input("Database name: ").strip()
    user = input("Username: ").strip()
    password = getpass("Password: ").strip()

    return {
        "host": host,
        "port": port,
        "dbname": dbname,
        "user": user,
        "password": password
    }

def build_conn_string(config: dict) -> str:
    return f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"