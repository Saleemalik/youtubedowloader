# env activation
python3 -m venv env
source env/bin/activate 
pip install -r requirements.txt 

# Start Redis Server
redis-server
# Starting the worker process
celery -A youtube worker -l info

# start django server

python manage.py runserver