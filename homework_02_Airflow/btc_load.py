from datetime import timedelta
from decimal import Decimal
from typing import NamedTuple

import psycopg2
import requests
from airflow import DAG
from airflow.decorators import task
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.utils.dates import days_ago

COINCAP_API_URL = 'http://api.coincap.io/v2/rates/bitcoin'
COINCAP_API_KEY = Variable.get('COINCAP_API_KEY', None)

CONNECTION_ID = 'analytics_db'
ANALYTICS_DB_DSN = BaseHook.get_connection(CONNECTION_ID).get_uri()


class CurrencyRate(NamedTuple):
    id: str
    symbol: str
    currencySymbol: str
    type: str
    rateUsd: Decimal
    timestamp: int


@task
def extract():
    response = requests.get(
        url=COINCAP_API_URL,
        headers={'Authorization': f'Bearer {COINCAP_API_KEY}'} if COINCAP_API_KEY else {},
    )
    response.raise_for_status()
    return response.json()


@task
def transform(json_data) -> CurrencyRate:
    return CurrencyRate(**json_data['data'], timestamp=json_data['timestamp'])


@task
def to_db(rate: CurrencyRate) -> None:
    with psycopg2.connect(ANALYTICS_DB_DSN) as connection:
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO rates (id, symbol, "currencySymbol", type, "rateUsd", timestamp) '
            'VALUES (%s, %s, %s, %s, %s, %s)', rate,
        )


with DAG(
        dag_id='get_bitcoin_rate',
        description="getting bitcoin quotes",
        schedule_interval='*/30 * * * *',
        start_date=days_ago(1),
        catchup=False,
        default_args={
            'retries': 4,
            'retry_delay': timedelta(seconds=30)
        }
) as dag:
    btc_rate_json = extract()
    btc_rate = transform(btc_rate_json)
    to_db(btc_rate)
