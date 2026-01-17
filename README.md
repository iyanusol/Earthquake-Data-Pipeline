# 🌍 Earthquake Data Pipeline  
**Production-Oriented Data Ingestion, Transformation & Validation**

---

## 📌 Overview
This project demonstrates a **complete, production-aware data pipeline** built to ingest, transform, and validate earthquake data for analytics and reporting use cases.

Rather than focusing solely on moving data from source to destination, this pipeline emphasizes the engineering fundamentals that make analytics trustworthy in real-world environments: **data quality, repeatability, idempotent processing, and validation**.

The result is a clean, analytics-ready staging dataset backed by SQL verification and designed with orchestration in mind.

![Data Pipeline Created](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/Data%20Pipeline%20created.png)

---

## 🎯 Problem Context
In many organizations, dashboards fail not because of visualization issues, but because the **data pipelines feeding them are unreliable**.

Common challenges include:
- Inconsistent timestamps and date formats  
- Encoding issues during ingestion  
- Duplicate or partial loads  
- Lack of validation before reporting

![Transform](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/transform-2.png)

This project intentionally addresses those challenges by applying **practical data engineering patterns** commonly used in production analytics systems.

---

## 🧱 Pipeline Architecture
The pipeline follows a clear and scalable structure aligned with modern analytics stacks:

1. **Extract** – Load raw earthquake records into PostgreSQL  
2. **Transform** – Standardize timestamps, clean text fields, and stage the data  
3. **Validate** – Confirm correctness using SQL-based integrity checks  

This separation of concerns allows for safe re-runs, monitoring, and future orchestration.

```
import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port="5433"
    )
```
---

## 🛠️ Technology Stack
- **Python** – ETL logic and transformations  
- **PostgreSQL** – Persistent storage and staging layer  
- **SQL** – Transformation logic and validation checks  
- **pgAdmin** – Database inspection and verification  
- **Airflow (DAG concept)** – Orchestration-ready design  

---

## 📥 Step 1: Ingesting the Raw Dataset
Raw earthquake data is first ingested into PostgreSQL to create a reliable foundation for downstream processing. This ensures consistency and enables controlled transformations rather than ad-hoc file manipulation.

![Load Dataset](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/LOAD%20DATASET.png)

---
```
def main():
    conn = get_db_connection()
    start_date = "2024-07-05"
    end_date = "2024-07-07"

    try:
        delete_old_records(conn, start_date, end_date)
        transform_earthquake(conn, start_date, end_date)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Pipeline failed: {e}")
    finally:
        conn.close()
```


## 🔄 Step 2: Transforming Into an Analytics-Ready Stage
The raw dataset is transformed into a staging table optimized for analytics. Key transformations include:

- Converting epoch timestamps into proper `timestamp` and `date` fields  
- Cleaning and standardizing location text  
- Preserving numeric precision for magnitude, depth, and coordinates  
- Applying date-bounded logic to support safe, repeatable loads  

![Transform](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/Transform.png)
![Transform Step 2](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/transform-2.png)

---
```
def delete_old_records(conn, start_date, end_date):
    delete_query = """
        DELETE FROM raw.stage_earthquake
        WHERE dt BETWEEN %s AND %s;
    """
    cur = conn.cursor()
    cur.execute(delete_query, (start_date, end_date))
    conn.commit()
    cur.close()
```

## ⚠️ Handling Real-World Ingestion Issues
Production pipelines often fail due to subtle issues such as file encoding. This project explicitly handles encoding behavior during ingestion to ensure stability across environments and prevent silent load failures.

![Loading Issue 1](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/loading-1.png)
![Loading Issue 2](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/loading-2.png)

---

## ✅ Step 3: SQL Validation & Data Integrity Checks
Before the data is considered analytics-ready, validation queries are executed to confirm:

- Records were successfully inserted  
- Date ranges match the intended load window  
- Timestamp conversions are accurate  
- Numeric values fall within expected ranges

```
def load_csv(cur, csv_file_path):
    sql = """
        COPY public.earthquake
        FROM STDIN WITH CSV HEADER
    """
    with open(csv_file_path, "r", encoding="utf-8") as f:
        cur.copy_expert(sql, f)
```

These checks ensure downstream dashboards and analyses are built on **trusted data**.

![PostgreSQL Validation 1](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/postgre%20SQL-1.png)
![PostgreSQL Validation 2](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/pstgre%20SQL-2.png)

---
```
def transform_earthquake(conn, start_date, end_date):
    sql = """
        INSERT INTO raw.stage_earthquake
        SELECT
            to_timestamp(ts::bigint / 1000) AS ts,
            CAST(to_timestamp(ts::bigint / 1000) AS date) AS dt,
            TRIM(SUBSTRING(place FROM POSITION('of ' IN place) + 3)) AS place,
            magnitude,
            longitude,
            latitude,
            depth
        FROM public.earthquake
        WHERE CAST(to_timestamp(ts::bigint / 1000) AS date)
              BETWEEN %s AND %s;
    """
    cur = conn.cursor()
    cur.execute(sql, (start_date, end_date))
    conn.commit()
    cur.close()
```

## 🧭 Orchestration Design (DAG-Ready)
Although executed locally, the pipeline is structured to map cleanly into orchestration tools such as **Apache Airflow**. Tasks are clearly separated (extract → transform → validate), enabling scheduling, retries, and monitoring in production environments.

![Intro to DAG](https://github.com/iyanusol/Earthquake-Data-Pipeline/blob/main/images/intro%20to%20dag.png)

---

## 🧠 Engineering Principles Demonstrated
- **Reliability** – Validation before analytics consumption  
- **Repeatability** – Safe re-runs using date-driven logic  
- **Data Integrity** – SQL checks to prevent silent failures  
- **Scalability** – Clear separation of pipeline stages  
- **Analytics Readiness** – Clean, structured staging data  

```
SELECT
    COUNT(*) AS row_count,
    MIN(dt) AS min_date,
    MAX(dt) AS max_date
FROM raw.stage_earthquake;
```

---

## 📂 Example Project Structure
Earthquake-Data-Pipeline/
├── images/
├── scripts/
│ ├── load_raw_data.py
│ ├── transform_stage.py
│ └── validation_checks.sql
├── README.md
└── requirements.txt

---

## 🚀 Future Enhancements
- Automated data quality testing  
- Incremental and partitioned loads  
- Centralized logging and alerting  
- Full orchestration via managed Airflow services  

---

## 👤 Author
**Iyanu Adebara**  
GitHub: https://github.com/iyanusol  

This project reflects a production-first approach to building data pipelines that analytics teams can trust.

