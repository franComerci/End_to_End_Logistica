# 🚛 End-to-End Logistics ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-2022-red?logo=microsoft-sql-server&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-yellow?logo=powerbi&logoColor=black)
![ETL](https://img.shields.io/badge/ETL-Automated-success)

## 📖 Overview
This project demonstrates a complete **End-to-End Data Engineering solution** for a logistics company. It automates the extraction of shipping data from raw CSV files, transforms and cleans the data using advanced SQL logic, and loads it into a Data Warehouse for business intelligence analysis.

The system is designed to handle **incremental loads**, prevent duplicates using Window Functions, and run automatically on a daily schedule via Windows Task Scheduler.

## 🏗️ Architecture
**CSV Files** ➡️ **Python (Extraction)** ➡️ **SQL Server (Staging)** ➡️ **Stored Procedures (Transformation)** ➡️ **SQL Server (Fact Table)** ➡️ **Power BI (Visualization)**

## 🚀 Key Features

### 1. Robust Extraction (Python)
* Connects to SQL Server using **SQLAlchemy** and **PyODBC**.
* Implements **Transaction Management** (`with motor.begin()`) to ensure data integrity (atomic commits).
* Handles file system operations to read and process raw CSVs.

### 2. Advanced Transformation (SQL)
* **Staging Area:** Raw data is first loaded into a temporary `Staging` table.
* **Data Cleaning:** Filters out invalid records (e.g., negative costs, null dates).
* **Deduplication:** Uses Window Functions (`ROW_NUMBER()`) to identify and select only the latest record for each Shipment ID.
* **Incremental Loading:** Implements a `LEFT JOIN` / `IS NULL` strategy to insert only **new** records into the `Fact` table, preventing Primary Key violations.

### 3. Business Intelligence (Power BI)
* **Data Modeling:** Star Schema implementation with a dedicated Date Table.
* **DAX Measures:** Time Intelligence calculations for Month-over-Month (MoM) growth.
* **Modern Dashboard:** Includes dynamic KPIs with conditional formatting and Decomposition Trees for root cause analysis.

## 🛠️ Technologies Used
* **Language:** Python 3.13 (Pandas, SQLAlchemy)
* **Database:** Microsoft SQL Server (LocalDB, T-SQL)
* **Orchestration:** Python & Windows Task Scheduler
* **Visualization:** Microsoft Power BI

## 💻 Code Highlights

### SQL Logic: Deduplication & Incremental Load
This Stored Procedure logic ensures idempotency by filtering duplicates before insertion.

```sql
WITH unique_data AS (
    SELECT 
        enviosID, 
        fecha, 
        costo, 
        estado, 
        ROW_NUMBER() OVER (PARTITION BY enviosID ORDER BY fecha DESC) as row_num
    FROM Staging
    WHERE fecha IS NOT NULL AND costo >= 0
)
INSERT INTO Fact (enviosID, fecha, costo, estado)
SELECT 
    d.enviosID, d.fecha, d.costo, d.estado 
FROM unique_data d
LEFT JOIN Fact f ON d.enviosID = f.enviosID
WHERE d.row_num = 1 AND f.enviosID IS NULL; -- Only insert new records
