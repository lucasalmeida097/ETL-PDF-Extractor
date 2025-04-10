# 📊 ETL Pipeline for Brokerage Notes with PDF Extraction, dbt-core & Streamlit Dashboard

This project is a complete **ETL (Extract, Transform, Load)** pipeline built in **Python**, designed to process and analyze **brokerage notes** in PDF format.

It enables automated extraction, transformation, and visualization of financial trading data using the following tools:

## 🔧 Technologies Used

- **Python 3.12** – The core programming language for all ETL and analytics logic.
- **[Camelot](https://camelot-py.readthedocs.io/)** – Extracts tabular data from brokerage PDFs.
- **PostgreSQL** – Relational database to store the extracted structured data.
- **[dbt-core](https://docs.getdbt.com/)** – For transforming and modeling raw extracted data following analytics engineering best practices.
- **[Streamlit](https://streamlit.io/)** – Creates an interactive and user-friendly dashboard to explore key financial metrics.

---

## 📂 Project Structure
ETL-PDF-Extractor/ ├── dashboard/ # Streamlit app │ └── app.py ├── dbt/ # dbt-core models │ ├── models/ │ ├── dbt_project.yml ├── etl/ # ETL scripts (PDF parsing and loading to DB) │ ├── extractor.py │ ├── loader.py ├── .env # Environment variables (not committed) ├── poetry.lock ├── pyproject.toml └── README.md


---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/seu-usuario/ETL-PDF-Extractor.git
cd ETL-PDF-Extractor
```

2. Install dependencies with Poetry
Make sure you have Poetry installed:
```bash
poetry install
```


3. Configure your environment
Create a .env file at the root with your PostgreSQL connection info:
```bash
DB_HOST=localhost
DB_NAME=etl_pdf
DB_USER=your_user
DB_PASSWORD=your_password
```
Note: While the dashboard no longer uses dotenv, this file is used by other scripts in the ETL.

## 🛠️ Running the ETL Pipeline
Place your brokerage note PDFs in a designated folder (e.g., file/pdf/jornada or redrex)

Run the extractor to parse and load the raw data into PostgreSQL:
```bash
poetry run python src/start.py
```

Run dbt to transform raw data:
```bash
cd dbt_models/
dbt run
```
## 📊 Running the Dashboard
Once your data is extracted and transformed, launch the dashboard:
```bash
streamlit run dashboard/app.py
```
You’ll be able to:

- Filter by asset (mercadoria) and date

- See KPIs like total movimentation and quantity

- Visualize trends over time

- View the filtered raw data in a clean table

## 📌 Why dbt?
We chose dbt-core to implement the "T" in ETL — making data transformations modular, version-controlled, and testable. It allows clear lineage tracking and is great for team collaboration.






