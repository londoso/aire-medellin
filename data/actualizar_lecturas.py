import pandas as pd
import os
import requests
import json
import pytz
from datetime import datetime

# Lee las variables de entorno
PURPLEAIR_GROUP_ID = os.getenv('PURPLEAIR_GROUP_ID')
PURPLEAIR_READ_KEY = os.getenv('PURPLEAIR_READ_KEY')
PURPLEAIR_WRITE_KEY = os.getenv('PURPLEAIR_WRITE_KEY')

#Función para consultar los datos de un grupo
## Retorna:
# response: respuesta codificada en json
def leer_sensores():    
    api_url = f'https://api.purpleair.com/v1/groups/{PURPLEAIR_GROUP_ID}/members'
    headers = {'X-API-Key': PURPLEAIR_READ_KEY}
    params = {'fields': 'pm2.5_alt, pm2.5_alt_a, pm2.5_alt_b, pm2.5, pm2.5_a, pm2.5_b, pm2.5_atm, pm2.5_atm_a, pm2.5_atm_b, pm2.5_cf_1, pm2.5_cf_1_a, pm2.5_cf_1_b'}
    response = requests.get(api_url, params=params, headers=headers)
    return response

respuesta = leer_sensores()
campos = respuesta.json()['fields']
datos = respuesta.json()['data']
fecha = datetime.fromtimestamp(respuesta.json()['time_stamp'])

co_tz = pytz.timezone('America/Bogota')
fmt = '%Y-%m-%d-%H-%M-%S'
fecha_col = co_tz.localize(fecha).strftime(fmt)

df = pd.DataFrame(datos, columns=campos)

try:
    if df.size > 0:
        df.to_csv('data/' + fecha_col + '.csv', index=False)
    else:
        raise NameError('No hay lectura de datos de los sensores')
except NameError:
    print('Ha ocurrido un error !')
    raise