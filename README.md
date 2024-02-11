# DataProcesser
Решение задачи 1 - task_1.py
Решение задачи 2 - dags/task_2.py

## Как запустить решение для задачи 2: 
Добавить .env по шаблону .env.template
Собрать контейнер и запустить контейнер:
```
docker-compose up -d --build
```
Админка Airflow доступен по адресу (далее url):
```
http://localhost:8080/admin/
```