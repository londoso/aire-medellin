import os
import awswrangler as wr
from datetime import datetime, timedelta

def fechas_unicas(lista, buscar):
    l_replace = [lst.replace(buscar, '') for lst in lista]
    dates = ['-'.join(lst.split('-')[:3]) for lst in l_replace]
    unique_dates = set(dates)
    return unique_dates

def lambda_handler(event, context):

    bucket_name = os.environ['BucketOrigen']
    bucket_name_prefix = f's3://{bucket_name}/' 
    bucket_destino = os.environ['BucketDestino']
    fecha_col = (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d')
    
    try:
        lista_objetos = wr.s3.list_objects(bucket_name_prefix, bucket_name_prefix)
        fechas = fechas_unicas(lista_objetos)

        for fecha in fechas:
            if fecha != fecha_col:
                fc = fecha.split('-')
                path_origen = f's3://{bucket_name}/{fecha}*'
                path_destino = f's3://{bucket_destino}/{fc[0]}/{fc[1]}/{fc[2]}/consolidado.csv'
                objetos = [i for i in lista_objetos if fecha in i]
                full = wr.s3.read_csv(path_origen)    
                wr.s3.to_csv(df=full, path=path_destino, index=False)
                print('## Guardado:', path_destino)
                wr.s3.delete_objects(path_origen)
                print('## Eliminando objetos:')
                for eliminar in objetos:
                    print('-', eliminar)
        
    except Exception as e:
        print(e)
