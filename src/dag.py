from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime
from pytz import timezone

import _env


local_tz = timezone('Asia/Ho_Chi_Minh')

# Định nghĩa DAG
default_args = {
    'owner': 'Nguyen Hai Long',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

my_dag = DAG(
    dag_id='crawl_news',
    default_args=default_args,
    description='v1',
    start_date=datetime(2024, 8, 1, tzinfo=local_tz),
    schedule='0,30 * * * *', # * == tat ca gia tri. vi tri: so phut trong gio | so gio trong ngay | so ngay trong thang |  thang trong nam | ngay trong tuan
    catchup=False
)

def run_crawl_url_rawl():
    import sys
    sys.path.append(_env.PATH_PROJECT_CRAWL_NEWS)
    import etl_urls
    try:
        etl_urls.main()
    except Exception as e:
        print(f"error:\n{e}")

def run_transform_distinct_url_rawl():
    import sys
    sys.path.append(_env.PATH_PROJECT_CLEAN_DATA_NEWS)
    import main
    try:
        main.main()
    except Exception as e:
        print(f"error:\n{e}")

def run_crawl_detail_news():
    import sys
    sys.path.append(_env.PATH_PROJECT_CRAWL_NEWS)
    import etl_detail
    try:
        etl_detail.main()
    except Exception as e:
        print(f"Exception:\n{e}")

task = PythonOperator(
    task_id='run_main',
    python_callable=run_crawl_url_rawl,
    dag=my_dag
)

task_2 = PythonOperator(
    task_id="run_transfrom_distinct_url_raw",
    python_callable=run_transform_distinct_url_rawl,
    dag=my_dag
)

task_3 = PythonOperator(
    task_id="Run_crawl_detail_news",
    python_callable=run_crawl_detail_news,
    dag=my_dag
)

task >> task_2 >> task_3