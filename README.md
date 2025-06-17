# 🧠 Alpha 1 | Schema Comparison & Difference Export Tool

A **powerful Python utility** to compare schemas between a **Source** and **Target** database — built for developers, DBAs, and data engineers to identify inconsistencies with precision.

---

## ✨ Features

✅ **Visual Comparison**:  
See the differences in a clear, color-coded table format using the `rich` library.

📊 **Detailed Difference Types**:
- Missing Tables
- Missing Columns
- Column Data Type Mismatches
- Primary Key Mismatches
- Unique Constraint Differences

📁 **Export to Excel**:  
Easily export results to an Excel file with multiple tabs:
- `Summary`
- `Tables Only in Source/Target`
- `Column Type Mismatches`
- And more...

🛠 **Built with**:
- `SQLAlchemy` for DB inspection  
- `Pandas` for data structuring  
- `OpenPyXL` for Excel export  
- `Rich` for elegant terminal output

---

## 🚀 Ideal For

- Pre- & Post-deployment validation  
- CI/CD data integrity checks  
- Migration consistency checks  
- Multi-environment (Dev → QA → Prod) schema syncing

---

## 📦 Supported Databases

Any SQL engine supported by **SQLAlchemy**:  
PostgreSQL, MySQL, SQLite, MSSQL, and more.

---

## 🖥️ Sample Output

```bash
📌 Tables Only in Source
┏━━━━━━━━━━━━━━━━━━━━━━┓
┃ Table                ┃
┡━━━━━━━━━━━━━━━━━━━━━━┩
│ employee_archive     │
│ legacy_customers     │
└──────────────────────┘

🟢 Do you want to export these differences to Excel? (y/n):
```

---
