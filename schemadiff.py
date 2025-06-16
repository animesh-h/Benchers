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
    src_schema = get_schema_details(src_conn)
    tgt_schema = get_schema_details(tgt_conn)

    src_tables = set(src_schema.keys())
    tgt_tables = set(tgt_schema.keys())

    only_in_src = src_tables - tgt_tables
    only_in_tgt = tgt_tables - src_tables
    in_both = src_tables & tgt_tables

    print("\n📌 Tables only in Source:")
    for t in sorted(only_in_src):
        print(f"  - {t}")

    print("\n📌 Tables only in Target:")
    for t in sorted(only_in_tgt):
        print(f"  - {t}")

    print("\n📌 Column & Constraint Differences (in common tables):")
    for table in sorted(in_both):
        src_info = src_schema[table]
        tgt_info = tgt_schema[table]

        src_cols = src_info["columns"]
        tgt_cols = tgt_info["columns"]

        src_col_names = set(src_cols.keys())
        tgt_col_names = set(tgt_cols.keys())

        col_only_src = src_col_names - tgt_col_names
        col_only_tgt = tgt_col_names - src_col_names
        col_both = src_col_names & tgt_col_names

        if col_only_src or col_only_tgt:
            print(f"\n  🔸 Table: {table}")
            if col_only_src:
                print(f"    Columns only in Source: {sorted(col_only_src)}")
            if col_only_tgt:
                print(f"    Columns only in Target: {sorted(col_only_tgt)}")

        for col in col_both:
            src_type = src_cols[col]
            tgt_type = tgt_cols[col]
            if src_type != tgt_type:
                print(f"    ⚠️ Column type mismatch in '{table}.{col}': Source = {src_type}, Target = {tgt_type}")

        # Compare primary key
        if set(src_info["primary_key"]) != set(tgt_info["primary_key"]):
            print(f"\n  ⚠️ Primary key mismatch in '{table}':")
            print(f"    Source PK: {src_info['primary_key']}")
            print(f"    Target PK: {tgt_info['primary_key']}")

        # Compare unique constraints
        unique_only_src = src_info["uniques"] - tgt_info["uniques"]
        unique_only_tgt = tgt_info["uniques"] - src_info["uniques"]

        if unique_only_src or unique_only_tgt:
            print(f"\n  ⚠️ Unique constraint mismatch in '{table}':")
            if unique_only_src:
                print(f"    Unique columns only in Source: {sorted(unique_only_src)}")
            if unique_only_tgt:
                print(f"    Unique columns only in Target: {sorted(unique_only_tgt)}")