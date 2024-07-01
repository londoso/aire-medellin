
# Aire-Medellin
Datos de calidad del aire recolectados por sensores [PurpleAir](https://www2.purpleair.com/) en la ciudad de Medellín y toda el área metropolitana del valle del aburrá.

Actualmente se están recolectando los datos de las partículas [PM 2.5](https://oehha.ca.gov/calenviroscreen/indicator/pm25) con una periodicidad de 5 minutos y diariamente se consolidan todas las lecturas en un solo archivo CSV para ser almacenadas en un bucket de S3 público.

## Lista de sensores

Última actualización: 2024-07-01 01-17-06

|   sensor_index | last_seen           | name                     | model    |   latitude |   longitude | mapa                                                                                  |
|---------------:|:--------------------|:-------------------------|:---------|-----------:|------------:|:--------------------------------------------------------------------------------------|
|          11338 | 2024-07-01 01:15:13 | PRS13MED                 | PA-II    |    6.23251 |    -75.5769 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=11338">ver mapa</a>  |
|          27552 | 2024-07-01 01:16:04 | Rosales del Parque       | PA-II    |    6.22955 |    -75.5918 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=27552">ver mapa</a>  |
|          27597 | 2024-07-01 01:15:50 | Sensor La Villa          | PA-II    |    6.2352  |    -75.6043 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=27597">ver mapa</a>  |
|          27617 | 2024-07-01 01:14:41 | Buenos Aires             | PA-II    |    6.23967 |    -75.5547 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=27617">ver mapa</a>  |
|          52163 | 2024-07-01 01:15:01 | Edificio Miró, El Tesoro | PA-II-SD |    6.20039 |    -75.5584 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=52163">ver mapa</a>  |
|          86891 | 2024-07-01 01:14:46 | Summan S.A.S. 5          | PA-II    |    6.1568  |    -75.5887 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=86891">ver mapa</a>  |
|          86937 | 2024-07-01 01:14:37 | Summan S.A.S.            | PA-II    |    6.21409 |    -75.5717 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=86937">ver mapa</a>  |
|          99091 | 2024-07-01 01:16:00 | S.O.S                    | PA-II-SD |    6.37818 |    -75.4513 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=99091">ver mapa</a>  |
|         170207 | 2024-07-01 01:16:10 | Almeria: Indoor          | PA-I-LED |    6.24362 |    -75.6156 | <a href="https://map.purpleair.com/1/mAQI/a10/p604800/cC0?select=170207">ver mapa</a> |

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

    