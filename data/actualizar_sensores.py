import pandas as pd
import os
import requests
import json

# Lee las variables de entorno
PURPLEAIR_GROUP_ID = os.getenv('PURPLEAIR_GROUP_ID')
PURPLEAIR_READ_KEY = os.getenv('PURPLEAIR_READ_KEY')
PURPLEAIR_WRITE_KEY = os.getenv('PURPLEAIR_WRITE_KEY')

#Función para consultar los miembros de un grupo
## Retorna:
# sensor_index: lista con id de los sensores
# member_id: lista con los id de los sensores en el grupo
def consulta_sensores():    
    api_url = f'https://api.purpleair.com/v1/groups/{PURPLEAIR_GROUP_ID}'
    headers = {'X-API-Key': PURPLEAIR_READ_KEY}
    response = requests.get(api_url, headers=headers)
    members = response.json()['members']
    sensor_index = [ sub['sensor_index'] for sub in members ]
    member_id = [ sub['id'] for sub in members ]
    return sensor_index, member_id

#Función para adicionar un sensor
## Retorna:
# response.status_code
# 200: Success
# 4xx: Error
def adicionar_sensor(sensor_index):    
    api_url = f'https://api.purpleair.com/v1/groups/{PURPLEAIR_GROUP_ID}/members'
    headers = {'Content-Type': 'application/json','X-API-Key': PURPLEAIR_WRITE_KEY}
    data = {'sensor_index': sensor_index}
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    return response.status_code

#Función para eliminar un sensor
## Retorna:
# response.status_code
# 204: Success
# 4xx: Error
def eliminar_sensor(member_id):    
    api_url = f'https://api.purpleair.com/v1/groups/{PURPLEAIR_GROUP_ID}/members/{member_id}'
    headers = {'Content-Type': 'application/json','X-API-Key': PURPLEAIR_WRITE_KEY}
    response = requests.delete(api_url, headers=headers)
    return response.status_code

#Función para gestionar las actualizaciones
## Retorna:
# control: si control.size = 0, entonces no hay cambios a realizar
# adicionar: sensores a adicionar, sensor_index
# eliminar: sensores a eliminar, ['sensor_index','member_id']
def actualizaciones(df_actualizar, df_actual):
    actualizar = pd.merge(df_actualizar,df_actual,how="outer",on="sensor_index",indicator=True)
    control = actualizar.query('_merge!="both"')
    adicionar = actualizar.query('_merge=="left_only"')['sensor_index']
    eliminar = actualizar.query('_merge=="right_only"')[['sensor_index','member_id']]
    return control, adicionar, eliminar

#Crea el dataframe con los sensores a actualizar
sensores_actualizar = pd.read_json('sensores.json')

#Consulta los sensores actuales en el grupo
sensor_index, member_id = consulta_sensores()

#Crea el dataframe con los sensores actuales del grupo
sensores_actuales = pd.DataFrame({'sensor_index': sensor_index, 'member_id': member_id})

#Crea los dataframes con los cambios a realizar
control, adicionar, eliminar = actualizaciones(sensores_actualizar,sensores_actuales)

if control.size > 0:
    if adicionar.size > 0:
        for sensor in adicionar:
            print('### Adicionando:',sensor)
            adicionar_sensor(sensor)
    elif eliminar.size > 0:
        for index, row in eliminar.iterrows():
            print('### Eliminando member_id:',row['member_id'],'| sensor_index:',row['sensor_index'])
            eliminar_sensor(row['member_id'])
else:
    print('### No hay actualizaciones')