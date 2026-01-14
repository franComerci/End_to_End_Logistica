import pandas as pd
import sqlalchemy as sa
import urllib as ul
import os
from sqlalchemy import text # Necesario para ejecutar el SP

arch = "envios_20260114.csv" 

SERVER = r'(localdb)\MSSQLLocalDB'
DATABASE = 'logistica'

def loadData():
    print("1. Leyendo archivo...")
    try:
        # Como los nombres ya vienen bien en el CSV, leemos directo
        df = pd.read_csv(arch)
        print(f"Archivo {arch} leído: {len(df)} filas.")
    except FileNotFoundError:
        print(f"El archivo {arch} no existe.")
        return
    
    # Configuración del driver
    params = ul.parse.quote_plus(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

    try:
        motor = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
        
        
        with motor.begin() as connection:
            
            # Cargar CSV a Staging      
            df.to_sql('Staging', con=connection, if_exists='append', index=False)
            
            # Ejecutar el Stored Procedure
            connection.execute(text("EXEC spLimpiarDatos"))
            
        print("Proceso ETL terminado. Datos limpios en tabla Fact.")

    except Exception as e:
        print(f"Error durante el proceso:")
        print(e)

if __name__ == "__main__":
    loadData()