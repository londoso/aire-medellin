import pandas as pd
import os
import requests
import json
import tabulate
from datetime import datetime, timedelta

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
    params = {'fields': 'name, model, latitude, longitude, last_seen'}
    response = requests.get(api_url, params=params, headers=headers)
    return response

respuesta = leer_sensores()
campos = respuesta.json()['fields']
datos = respuesta.json()['data']
df = pd.DataFrame(datos, columns=campos)
df['last_seen'] = pd.to_datetime(df['last_seen'], unit='s') - pd.Timedelta(hours=5)
df['mapa'] = '<a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=' + df['sensor_index'].astype(str) + '">ver mapa</a>'
md = df.to_markdown(index=False)
act = (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d %H-%M-%S')

readme = \
    """
# Aire-Medellin
Datos de calidad del aire recolectados por sensores [PurpleAir](https://www2.purpleair.com/) en la ciudad de Medellín y toda el área metropolitana del valle del aburrá.

Actualmente se están recolectando los datos de las partículas [PM 2.5](https://oehha.ca.gov/calenviroscreen/indicator/pm25) con una periodicidad de 5 minutos y diariamente se consolidan todas las lecturas en un solo archivo CSV para ser almacenadas en un bucket de S3 público.

## Lista de sensores

Última actualización: {}

{}

## Metadatos

| Campo         | Tipo de dato | Ejemplo                |
| :----------   | :----------: | :--------------------: |
| sensor_index  | int          | 11338                  |
| pm2.5         | float        | 16.4                   |
| pm2.5_a       | float        | 19.0                   |
| pm2.5_b       | float        | 13.9                   |
| pm2.5_alt     | float        | 9.7                    |
| pm2.5_alt_a   | float        | 10.7                   |
| pm2.5_alt_b   | float        | 8.7                    |
| pm2.5_atm     | float        | 16.4                   |
| pm2.5_atm_a   | float        | 19.02                  |
| pm2.5_atm_b   | float        | 13.88                  |
| pm2.5_cf_1    | float        | 16.4                   |
| pm2.5_cf_1_a  | float        | 19.02                  |
| pm2.5_cf_1_b  | float        | 13.88                  |
| timestamp     | datetime     | 2024-01-17 14:17:55    |

[Ver más detalles de los metadatos](https://api.purpleair.com/#api-groups-get-members-data)

## Consulta del dataset (no requiere cuenta de AWS)

- Los datos del día en curso se pueden consultar en el bucket:

`aws s3 ls --no-sign-request s3://aire-medellin/`

- Los datos históricos consolidados se pueden consultar en el bucket:

`aws s3 ls --no-sign-request s3://aire-medellin-datos/`

## Roadmap

Validar los programas de apoyo para datos públicos

### AWS Open Data

https://aws.amazon.com/opendata

### AWS Open Data Sponsorship Program

https://aws.amazon.com/opendata/open-data-sponsorship-program/

### Amazon Sustainability Data Initiative

https://registry.opendata.aws/collab/asdi/

## Contacto

**Anderson Londoño**<br>
<londoso@gmail.com>

    """.format(act, md)

with open('./README.md', 'w') as f:
        f.write(readme)