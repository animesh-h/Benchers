import json
import os
from getpass import getpass

def get_db_config(label="Source"):
    saved_path = "saved_configs.json"
    saved = {}

    if os.path.exists(saved_path):
        with open(saved_path, "r") as f:
            saved = json.load(f)

    print(f"\n=== {label} Database Configuration ===")
    print("1. Use existing connection")
    print("2. Enter new connection")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1" and saved:
        print("\nAvailable saved connections:")
        for i, key in enumerate(saved.keys(), 1):
            print(f"{i}. {key}")
        index = input("Select connection number: ").strip()

        if index.isdigit() and 1 <= int(index) <= len(saved):
            key = list(saved.keys())[int(index) - 1]
            config = saved[key]
            config["password"] = getpass(f"Enter password for '{key}': ")
            return config
        else:
            print("Invalid selection. Proceeding with new connection setup.")

    # Option 2 or fallback
    host = input("Host (e.g., localhost): ").strip()
    port = input("Port (e.g., 5432): ").strip()
    dbname = input("Database name: ").strip()
    user = input("Username: ").strip()
    password = getpass("Password: ").strip()

    config = {
        "host": host,
        "port": port,
        "dbname": dbname,
        "user": user,
        "password": password
    }

    save = input("Save this connection for future use? (y/n): ").strip().lower()
    if save == "y":
        name = input("Enter a name for this config (e.g., dev_db): ").strip()
        save_data = config.copy()
        del save_data["password"]
        saved[name] = save_data
        with open(saved_path, "w") as f:
            json.dump(saved, f, indent=2)
        print(f"✅ Saved config as '{name}'.")

    return config

def build_conn_string(config: dict) -> str:
    return f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"