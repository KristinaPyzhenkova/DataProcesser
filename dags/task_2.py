import os
import re
from datetime import timedelta
import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models.baseoperator import BaseOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime.datetime(2024, 2, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'provide_context': True
}


class DataProcessingOperator(BaseOperator):
    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filename = filename
        self.file_path = os.path.join('/usr/local/airflow/data', self.filename)
        self.dir_output_path = os.path.join('/usr/local/airflow/data', 'Result')

    def execute(self, **kwargs):
        self.log.info('start execute')
        data = self.read_file()
        if data is None:
            return
        result = self.process_data(data)
        self.write_file(result)

    def read_file(self):
        self.log.info('read_file  start')
        with open(self.file_path, 'r') as file:
            data = file.read()
        return data

    def write_file(self, data):
        self.log.info('write_file  start')
        part_filename = re.search(r'TEST_AUCHAN(.*?)\.txt', self.filename)
        filename_output = f'TEST_AUCHAN_success{part_filename.group(1)}.txt'
        path_output = os.path.join(self.dir_output_path, filename_output)
        os.makedirs(os.path.dirname(path_output), exist_ok=True)
        with open(path_output, 'w') as file:
            file.write(data)
        self.log.info(f'Task completed for {filename_output}!')

    def process_data(self, data):
        self.log.info('process_data  start')
        data = re.findall(r'\d+-\d+|\d+', data)
        result = ''
        for val in data:
            if '-' in val:
                start_val, end_val = map(int, val.split('-'))
                result += '\n'.join(str(i) for i in range(start_val, end_val + 1))
            else:
                result += str(int(val))
            result += '\n'
        return result


def get_files(directory):
    for root, _, files in os.walk(directory):
        if not re.search(r'/data/TEST_Folder', root):
            continue
        for file_name in files:
            if file_name.startswith('TEST_'):
                yield os.path.join(root, file_name)


with DAG(
    'data_processing_dag',
    default_args=default_args,
    description='A DAG for processing data',
    schedule_interval='*/1 * * * *',
    catchup=False
) as dag:
    for file_path in get_files('/usr/local/airflow/data'):
        part_filename = re.search(r'TEST_AUCHAN(.*?)\.txt', file_path)
        part_filename = part_filename.group(1)
        task_id = f'process_data{part_filename}'
        processor = DataProcessingOperator(
            filename=file_path,
            dag=dag,
            task_id=task_id
        )
        process_task = PythonOperator(
            task_id=task_id,
            python_callable=processor.execute
        )
