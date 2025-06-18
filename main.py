from prerequisites import install_missing_packages
install_missing_packages()
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from config import get_db_config, build_conn_string
from schema_diff import compare_schemas
from rowcount_diff import compare_rowcount

console = Console()

def print_menu():
    console.print(Panel.fit("📊 [bold cyan]Database Comparison Tool[/bold cyan]"))
    console.print("[1] Schema Differences")
    console.print("[2] Data Differences")
    console.print("[3] Object Differences (Views, Functions, Triggers)")
    console.print("[4] Permissions & Roles Differences")
    console.print("[5] Configuration Settings")
    console.print("[6] Generate Sync Scripts")
    console.print("[7] Export Comparison Report")
    console.print("[0] Exit")

def main():
    while True:
        print_menu()
        choice = Prompt.ask("\nEnter your choice", choices=["0", "1", "2", "3", "4", "5", "6", "7"])
        
        if choice == "0":
            console.print("[bold green]Goodbye![/bold green] 👋")
            break
        elif choice == "1":
            console.print("[yellow]Schema Comparison...[/yellow]")
            src_cfg = get_db_config("Source")
            tgt_cfg = get_db_config("Target")

            src_conn = build_conn_string(src_cfg)
            tgt_conn = build_conn_string(tgt_cfg)

            compare_schemas(src_conn, tgt_conn)

        elif choice == "2":
            console.print("[yellow]Row Count Comparison[/yellow]")
            src_cfg = get_db_config("Source")
            tgt_cfg = get_db_config("Target")

            src_conn = build_conn_string(src_cfg)
            tgt_conn = build_conn_string(tgt_cfg)

            compare_rowcount(src_conn, tgt_conn)
        console.print()

if __name__ == "__main__":
    main()