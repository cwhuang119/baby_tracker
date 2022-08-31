run:
	python3 manage.py runserver
migrate baby:
	python3 manage.py makemigrations baby
create superuser:
	python3 manage.py createsuperuser --username admin --email tom.huang@smasoft.com.tw
migrate:
	python3 manage.py makemigrations baby && python3 manage.py migrate

delete:
	rm -r baby/__pycache__ && rm -r baby/migrations && rm db.sqlite3
