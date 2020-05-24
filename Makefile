lint:
	npx prettier@2.0.5 ui/src --check
	black event_explorer --check

tidy:
	npx prettier@2.0.5 ui/src --write
	black event_explorer

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
