#script para generar un .csv con datos random
import pandas as pd
import random as rnd 
import numpy as np
from datetime import datetime, timedelta
import os

def generateData():
    print("Generating random data")
    nRegistros = 50 
    data = {
        'enviosID': range(1000, 1000 + nRegistros),
        'fecha': [datetime.now() - timedelta(days=rnd.randint(1, 30)) for _ in range(nRegistros)],
        'costo': [round(rnd.uniform(10, 500), 2) for _ in range (nRegistros)],
        'estado': [rnd.choice (['Entregado', 'Pendiente', 'Cancelado'])for _ in range(nRegistros)]
        }
    df = pd.DataFrame(data)

    #en esta parte pongo datos erroneos a propósito
    df.loc[0:4, 'costo'] = -50.00 #desde la fila 0 a la 4 van a tener -50 de costo
    df.loc[5:9, 'fecha'] = np.nan #pongo nulos en las fechas 
    df = pd.concat([df, df.iloc[0:21]]) #aca meto datos duplicados al final del archivo

    arch = f"envios_{datetime.now().strftime('%Y%m%d')}.csv"
    #en el nombre del archivo le meto envios + la fecha
    df.to_csv(arch, index = False)

    print(f"se creo el archivo :b")
    print(f"ubicacion: {os.getcwd()}")




if __name__ == "__main__":
    try:
        generateData()
    except ImportError:
        print("pandas no esta instalado")


