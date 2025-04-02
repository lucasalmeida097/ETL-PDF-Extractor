import os
import camelot
import pandas as pd
import logging
from unidecode import unidecode
from src.configs.tools.postgres import RDSPostgreSQLManager

logging.basicConfig(level=logging.INFO)

class PDFTableExtractor:
    def __init__(self, file_name, configs):
        self.path = os.path.abspath(f"src/files/pdf/{configs["name"].lower()\
                    /{file_name}.pdf}")
        self.csv_path = os.path.abspath("src/files/csv")
        self.file_name = file_name
        self.configs = configs

    def start():
        pass

    def get_table_data(self, t_area, t_columns, fix ):
        tables = camelot.read_pdf(
            self.path,
            falvor=self.configs["flavor"],
            table_areas=t_area,
            columns=t_columns,
            strip_text=self.configs["strip-text"],
            page=self.configs["pages"],
            password=self.configs["password"]
        )

        table_content = [self.fix_header(page.df) if fix else page.df for \
                         page in tables]
        result = pd.concat(table_content, ignore_index=True) \
                if len(table_content) > 1 else table_content[0]
        return result

    def save_csv(self, df, file_name):
        if not os.path.exists(self.csv_path):
            os.makedirs(self.csv_path, exist_ok=True)
        path = os.path.join(self.csv_path, f"{file_name}.csv")
        df.to_csv(path, sep=";", index=False)


    def add_infos():
        pass

    @staticmethod
    def fix_header(df):
        df.columns = df.iloc[0]
        df.columns = df.drop(0)
        df = df.drop(df.columns[0], axis=1)
        return df

    def sanitize_column_names():
        pass

    def send_to_db(df, table_name):
        try:
            connection = RDSPostgreSQLManager().alchemy()
            df.to_sql(table_name, connection, if_exists="append", index=False)
            logging.info(f"Data successfully saved to the database {table_name}")
        except Exception as e:
            logging.error(e)

if __name__ == '__main__':
        extractor = PDFTableExtractor().start()