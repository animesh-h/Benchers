import importlib
import subprocess
import sys
import time
import os

required_libraries = {
    "psycopg2": "psycopg2-binary",
    "sqlalchemy": "sqlalchemy",
    "pandas": "pandas",
    "openpyxl": "openpyxl",
    "tabulate": "tabulate",
    "rich": "rich"
}

def install_missing_packages():
    print(f"📦 Checking and installing prerequisites")
    for import_name, pip_name in required_libraries.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            print(f"📦 Installing missing package: {pip_name}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])
    print(f"✅ All set, redirecting to main menu!")
    time.sleep(2)
    os.system('cls')
