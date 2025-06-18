from rich.console import Console
from rich.table import Table
import pandas as pd
import os
import time
from sqlalchemy import create_engine, inspect

def get_table_name(conn_string):
    engine = create_engine(conn_string)
    inspector = inspect(engine)

    schema_info = {}
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        pk = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        uniques = set()
        for uc in inspector.get_unique_constraints(table_name):
            for col in uc["column_names"]:
                uniques.add(col)

        schema_info[table_name] = {
            "columns": {col["name"]: str(col["type"]) for col in columns},
            "primary_key": pk,
            "uniques": uniques,
        }
    return schema_info

def compare_rowcount(src_engine, tgt_engine):
    console = Console()
    src_schema = get_table_name(src_engine)
    tgt_schema = get_table_name(tgt_engine)

    src_tables = set(src_schema.keys())
    tgt_tables = set(tgt_schema.keys())
    common_tables = src_tables & tgt_tables

    mismatches = []

    table = Table(title="🔍 Row Count Mismatches", show_lines=True)
    table.add_column("Table", style="cyan", no_wrap=True)
    table.add_column("Source Row Count", style="green")
    table.add_column("Target Row Count", style="red")

    for table_name in sorted(common_tables):
        src_count = pd.read_sql(f'SELECT COUNT(*) FROM "{table_name}"', src_engine).iloc[0, 0]
        tgt_count = pd.read_sql(f'SELECT COUNT(*) FROM "{table_name}"', tgt_engine).iloc[0, 0]
        if src_count != tgt_count:
            mismatches.append((table_name, src_count, tgt_count))
            table.add_row(table_name, str(src_count), str(tgt_count))

    console.print()
    console.print("[yellow]Fetching details![/yellow]")
    time.sleep(2)
    os.system('cls')
    if mismatches:
        console.print(table)
    else:
        console.print("[bold green]✅ All tables have matching row counts![/bold green]")

    return mismatches
