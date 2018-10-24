start_django:
	python manage.py runserver 0.0.0.0:8000

create_user_db:
	#creating username for postgres
	sudo -u postgres psql -c "CREATE USER $(PG_USERNAME) WITH SUPERUSER PASSWORD '$(PG_PASSWORD)';" ;

drop_user_db:
	#deleting username for postgres
	sudo -u postgres psql -c "DROP ROLE $(PG_USERNAME);"

create_db:
	#Creating Databases
	sudo -u postgres psql -c "CREATE DATABASE $(PG_WORLDMAP_DJANGO_DB) WITH OWNER $(OWNER);"
	sudo -u postgres psql -d $(PG_WORLDMAP_DJANGO_DB) -c "CREATE EXTENSION postgis;"
	sudo -u postgres psql -d $(PG_WORLDMAP_DJANGO_DB) -c "CREATE EXTENSION dblink;"
	sudo -u postgres psql -c "CREATE DATABASE $(PG_WORLDMAP_UPLOADS_DB) WITH OWNER $(OWNER);"
	sudo -u postgres psql -d $(PG_WORLDMAP_UPLOADS_DB) -c "CREATE EXTENSION postgis;"

drop_db:
	#Deleting Databases
	sudo -u postgres psql -c "DROP DATABASE $(PG_WORLDMAP_DJANGO_DB);"
	sudo -u postgres psql -c "DROP DATABASE $(PG_WORLDMAP_UPLOADS_DB);"

build: create_user_db create_db sync

clean: drop_db drop_user_db

sync:
	python manage.py migrate --noinput
	python manage.py loaddata fixtures/sample_admin.json
	python manage.py loaddata fixtures/default_oauth_apps.json
	python manage.py loaddata fixtures/initial_data.json
	python manage.py loaddata fixtures/default_auth_groups.json

sync_gazetteer:
	python manage.py migrate --noinput
