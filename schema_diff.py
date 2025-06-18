from rich.table import Table
from rich.console import Console
from pathlib import Path
import pandas as pd
import os
from sqlalchemy import create_engine, inspect

def get_schema_details(conn_string):
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

def compare_schemas(src_conn, tgt_conn):
    console = Console()
    src_schema = get_schema_details(src_conn)
    tgt_schema = get_schema_details(tgt_conn)

    src_tables = set(src_schema.keys())
    tgt_tables = set(tgt_schema.keys())
    in_both = src_tables & tgt_tables

    excel_data = {
        "Tables_Only_in_Source": [(t,) for t in sorted(src_tables - tgt_tables)],
        "Tables_Only_in_Target": [(t,) for t in sorted(tgt_tables - src_tables)],
        "Columns_Only_in_Source": [],
        "Columns_Only_in_Target": [],
        "Column_Type_Mismatches": [],
        "Primary_Key_Mismatches": [],
        "Unique_Constraint_Mismatches": [],
    }

    def print_table(title, headers, rows):
        if not rows:
            return
        table = Table(title=title, show_lines=True)
        for h in headers:
            table.add_column(h)
        for row in rows:
            table.add_row(*[str(item) for item in row])
        console.print(table)

    for table in sorted(in_both):
        src_info = src_schema[table]
        tgt_info = tgt_schema[table]

        src_cols = src_info["columns"]
        tgt_cols = tgt_info["columns"]

        src_col_names = set(src_cols.keys())
        tgt_col_names = set(tgt_cols.keys())

        for col in src_col_names - tgt_col_names:
            excel_data["Columns_Only_in_Source"].append((table, col))
        for col in tgt_col_names - src_col_names:
            excel_data["Columns_Only_in_Target"].append((table, col))

        for col in src_col_names & tgt_col_names:
            if src_cols[col] != tgt_cols[col]:
                excel_data["Column_Type_Mismatches"].append((table, col, src_cols[col], tgt_cols[col]))

        if set(src_info["primary_key"]) != set(tgt_info["primary_key"]):
            excel_data["Primary_Key_Mismatches"].append(
                (table, str(src_info["primary_key"]), str(tgt_info["primary_key"]))
            )

        src_uniques = src_info["uniques"]
        tgt_uniques = tgt_info["uniques"]
        if src_uniques != tgt_uniques:
            excel_data["Unique_Constraint_Mismatches"].append(
                (table, ", ".join(src_uniques - tgt_uniques), ", ".join(tgt_uniques - src_uniques))
            )
    summary_data = [
        ["Total Tables in Source", len(src_schema)],
        ["Total Tables in Target", len(tgt_schema)],
        ["Common Tables", len(in_both)],
        ["Tables only in Source", len(excel_data["Tables_Only_in_Source"])],
        ["Tables only in Target", len(excel_data["Tables_Only_in_Target"])],
        ["Column Mismatches (Missing/Extra)", len(excel_data["Columns_Only_in_Source"]) + len(excel_data["Columns_Only_in_Target"])],
        ["Column Type Mismatches", len(excel_data["Column_Type_Mismatches"])],
        ["Primary Key Mismatches", len(excel_data["Primary_Key_Mismatches"])],
        ["Unique Constraint Mismatches", len(excel_data["Unique_Constraint_Mismatches"])],
    ]
    summary_table = Table(title="📊 Schema Comparison Summary", show_lines=True)
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="magenta")
    for row in summary_data:
        summary_table.add_row(str(row[0]), str(row[1]))
    os.system('cls')
    console.print(summary_table)

    print_table("📌 Tables Only in Source", ["Table"], excel_data["Tables_Only_in_Source"])
    print_table("📌 Tables Only in Target", ["Table"], excel_data["Tables_Only_in_Target"])

    print_table("📌 Columns Only in Source", ["Table", "Column"], excel_data["Columns_Only_in_Source"])
    print_table("📌 Columns Only in Target", ["Table", "Column"], excel_data["Columns_Only_in_Target"])
    print_table("📌 Column Type Mismatches", ["Table", "Column", "Source Type", "Target Type"], excel_data["Column_Type_Mismatches"])
    print_table("📌 Primary Key Mismatches", ["Table", "Source PK", "Target PK"], excel_data["Primary_Key_Mismatches"])
    print_table("📌 Unique Constraint Mismatches", ["Table", "Unique in Source", "Unique in Target"], excel_data["Unique_Constraint_Mismatches"])

    # ⏳ Prompt to export
    choice = input("\n🟢 Do you want to export these differences to Excel? (y/n): ").strip().lower()
    if choice == "y":
        Path("exports").mkdir(exist_ok=True)
        output_path = Path("exports") / "schema_differences.xlsx"
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            only_in_src = src_tables - tgt_tables
            only_in_tgt = tgt_tables - src_tables
            col_src_rows = excel_data["Columns_Only_in_Source"]
            col_tgt_rows = excel_data["Columns_Only_in_Target"]
            col_type_mismatches = excel_data["Column_Type_Mismatches"]
            pk_mismatches = excel_data["Primary_Key_Mismatches"]
            unique_mismatches = excel_data["Unique_Constraint_Mismatches"]

            summary_data = [
                ["Total Tables in Source", len(src_schema)],
                ["Total Tables in Target", len(tgt_schema)],
                ["Common Tables", len(in_both)],
                ["Tables only in Source", len(only_in_src)],
                ["Tables only in Target", len(only_in_tgt)],
                ["Column Mismatches (Missing/Extra)", len(col_src_rows) + len(col_tgt_rows)],
                ["Column Type Mismatches", len(col_type_mismatches)],
                ["Primary Key Mismatches", len(pk_mismatches)],
                ["Unique Constraint Mismatches", len(unique_mismatches)],
            ]

            summary_df = pd.DataFrame(summary_data, columns=["Metric", "Value"])
            summary_df.to_excel(writer, sheet_name="Summary", index=False)

            for sheet, rows in excel_data.items():
                df = pd.DataFrame(rows)
                column_map = {
                    "Tables_Only_in_Source": ["Table"],
                    "Tables_Only_in_Target": ["Table"],
                    "Columns_Only_in_Source": ["Table", "Column"],
                    "Columns_Only_in_Target": ["Table", "Column"],
                    "Column_Type_Mismatches": ["Table", "Column", "Source Type", "Target Type"],
                    "Primary_Key_Mismatches": ["Table", "Source PK", "Target PK"],
                    "Unique_Constraint_Mismatches": ["Table", "Unique in Source", "Unique in Target"],
                }
                if not df.empty:
                    df.columns = column_map[sheet]
                else:
                    df = pd.DataFrame(columns=column_map[sheet])

                df.to_excel(writer, sheet_name=sheet, index=False)

        console.print(f"\n✅ Differences exported to [green]{output_path}[/green]")
    else:
        console.print("[yellow]⚠️ Skipping export. Exiting...[/yellow]")
