🔍 Alpha1

A Python-based utility to compare database schemas between a source and target PostgreSQL (or other SQLAlchemy-supported) databases.
It identifies differences in:

Tables (missing in source/target)

Columns (missing or extra)

Data types

Primary keys

Unique constraints

💡 Features:

CLI-based output using rich for colored tabular display

Optional Excel export with categorized sheets (Summary, Tables Only in Source, Columns Only in Target, etc.)

Modular design for easy extension (e.g., data comparison, foreign key diff)

📦 Tech Stack:

SQLAlchemy, Pandas, OpenPyXL, Rich

🚀 Use this tool to ensure schema consistency across environments (Dev → QA → Prod), during migrations, or in CI/CD pipelines.
