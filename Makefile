VENV_DIR=IDS706
DOCKER_IMAGE=management:latest
AWS_REGION=us-east-1
ECR_URL=381492212823.dkr.ecr.$(AWS_REGION).amazonaws.com/ids706_group_project

venv:
	python3 -m venv $(VENV_DIR)

install: venv
	. $(VENV_DIR)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r requirements.txt

build:
	docker build -t ${DOCKER_IMAGE} .

push:
	rm -rf ~/.docker/config.json
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_URL)
	docker tag ${DOCKER_IMAGE} $(ECR_URL)
	docker push $(ECR_URL)

clean:
	rm -rf $(VENV_DIR)

lint:
	. $(VENV_DIR)/bin/activate && \
	ruff check . --fix --verbose

format:	
	black . --line-length 100 --verbose --exclude 'IDS706'

test:
	. $(VENV_DIR)/bin/activate && python load_test.py

run:
	make build
	docker run -p 8080:8080 ${DOCKER_IMAGE}
