#######################
# Linting and Testing
#######################

lint:
	black event_explorer --check

lint-black:
	black event_explorer --check
	black test_event_explorer --check

tidy:
	black event_explorer
	black test_event_explorer

test:
	pytest test_event_explorer --cov=event_explorer

#################
# Node Frontend
# ###############

start-ui:
	cd ui && npm run start

install-ui:
	cd ui && npm install
	cd ..

install-nvm:
	sh scripts/install_nvm.sh

################
# Python Backend
# ##############

pip-compile:
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/test.in

pip-install:
	pip install -r requirements/base.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/test.txt
	pip install -e .

#############
# Database
#############

setup-db:
	psql --host=${FIDDLER_RDS} \
			 --username=master \
			 --dbname=event_explorer \
			 -f database/schema.sql
	psql --host=${FIDDLER_RDS} \
			 --username=master \
			 --dbname=event_explorer \
			 -f database/users.sql
	psql --host=${FIDDLER_RDS} \
			 --username=master \
			 --dbname=event_explorer \
			 -f database/events.sql
	psql --host=${FIDDLER_RDS} \
			 --username=master \
			 --dbname=event_explorer \
			 -f database/attendees.sql
