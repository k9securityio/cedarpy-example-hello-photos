# if BUILD_ID is unset, compute metadata that will be used in builds;
# note that for local development you probably want to set the STAGE to
# something like your username for integration tests, e.g.
# 
# make deploy run-integration-tests STAGE=dev-username
DEPLOYMENT_BUCKET := k9-serverless-deployments-dev

ifeq ($(strip $(BUILD_ID)),)
	VCS_REF := $(shell git rev-parse --short HEAD)
	BUILD_TIME_UTC := $(shell date +'%Y%m%d-%H%M%S')
	BUILD_ID := $(BUILD_TIME_UTC)-$(VCS_REF)
endif

BUILD_BRANCH := $(shell git symbolic-ref --short HEAD)

ifeq ($(strip $(BUILD_BRANCH)),main)
	BUILD_BRANCH_HASH := main
else
	BUILD_BRANCH_HASH := $(shell echo $(BUILD_BRANCH) | openssl dgst -sha1 -r | cut -b 1-8)
endif

# if STAGE is unset, compute ephemeral dev stage
ifeq ($(strip $(STAGE)),)
	STAGE := dev-$(BUILD_BRANCH_HASH)
endif

ifeq ($(strip $(DEPLOY_ARCH)),)
	DEPLOY_ARCH := 'arm64'
endif

AWS_AUTH_VARS :=

ifdef AWS_PROFILE
	AWS_AUTH_VARS += $(AWS_AUTH_VARS) -e AWS_PROFILE=$(AWS_PROFILE)
endif

ifdef AWS_ACCESS_KEY_ID
	AWS_AUTH_VARS += $(AWS_AUTH_VARS) -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID)
endif

ifdef AWS_SECRET_ACCESS_KEY
	AWS_AUTH_VARS += $(AWS_AUTH_VARS) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY)
endif

ifdef AWS_SESSION_TOKEN
	AWS_AUTH_VARS += $(AWS_AUTH_VARS) -e AWS_SESSION_TOKEN=$(AWS_SESSION_TOKEN)
endif

AWS_OPTS := $(AWS_AUTH_VARS) -e AWS_REGION=$(AWS_REGION)

.PHONY: metadata
metadata:
	@echo "Gathering Metadata"
	@echo BUILD_TIME_UTC is $(BUILD_TIME_UTC)
	@echo BUILD_ID is $(BUILD_ID)
	@echo BUILD_BRANCH is $(BUILD_BRANCH)
	@echo BUILD_BRANCH_HASH is $(BUILD_BRANCH_HASH)
	@echo STAGE is $(STAGE)
	@echo DEPLOY_ARCH is $(DEPLOY_ARCH)

.PHONY: timestamp
timestamp:
	@echo Timestamp: $(shell date +'%Y-%m-%d-%H%M%S')

.PHONY: venv
venv:
	@echo Building Python virtual environment
	set -e ;\
	python3 -m venv venv ;\
	source venv/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -r requirements.txt ;\

.PHONY: venv-dev
venv-dev:
	@echo Building Python virtual environment for developer
	set -e ;\
	python3 -m venv venv-dev ;\
	source venv-dev/bin/activate ;\
	pip install --upgrade pip ;\
	pip install -r requirements.txt -r requirements-dev.txt ;\

.PHONY: build-node-modules
build-node-modules:
	npm install

.PHONY: clean-node-modules
clean-node-modules:
	rm -f package-lock.json
	rm -rf node_modules

.PHONY: clean
clean:
	find . -name '.__pycache__' | xargs rm -rf
	find . -name '.pytest_cache' | xargs rm -rf
	find . -name '*.test-report.xml' | xargs rm -f

.PHONY: run-pylint
run-pylint:
	pylint -E **/*.py

.PHONY: quality-metrics
quality-metrics:
	pylint **/*.py | tee pylint.out
	grep ": R[0-9]" pylint.out | wc -l
	grep ": W[0-9]" pylint.out | wc -l
	grep ": E[0-9]" pylint.out | wc -l
	grep ": F[0-9]" pylint.out  | wc -l

.ONESHELL:
.PHONY: run-unit-tests
run-unit-tests:
	# note: unit tests should always run as the 'dev' stage to simplify unit test development
	@echo Running unit tests
	set -ex ;\
	STAGE='dev' ;\
	pytest tests/unit/

.PHONY: quick
quick: metadata run-pylint run-unit-tests

.PHONY: deploy
deploy: metadata
	@echo deploy BUILD_BRANCH is $(BUILD_BRANCH)
	BUILD_BRANCH=$(BUILD_BRANCH) \
	sls deploy --verbose --stage $(STAGE)

