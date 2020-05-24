lint:
	prettier ui/src --check
	black event_explorer --check

lint-black:
	black event_explorer --check
	black test_event_explorer --check

tidy:
	prettier ui/src --write
	black event_explorer
	black test_event_explorer

test:
	pytest test_event_explorer --cov=event_explorer

start-ui:
	cd ui && npm run start

install-ui:
	cd ui && npm install
	cd ..

install-nvm:
	sh scripts/install_nvm.sh

pip-compile:
	pip-compile requirements/base.in
	pip-compile requirements/dev.in
	pip-compile requirements/test.in

pip-install:
	pip install -r requirements/base.txt
	pip install -r requirements/dev.txt
	pip install -r requirements/test.txt
	pip install -e .
