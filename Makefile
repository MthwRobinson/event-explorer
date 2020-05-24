lint:
	npx prettier@2.0.5 ui/src --check

tidy:
	npx prettier@2.0.5 ui/src --write

start-ui:
	cd ui && npm run start

install-ui:
	cd ui && npm install
