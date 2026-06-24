.PHONY: prerequisites test validate lint security-scan deploy destroy local-demo score

RELEASE ?= ml-platform
NAMESPACE ?= ml-platform

test:
	python -m unittest discover -s tests

validate: test
	python scripts/validate_layout.py

lint: validate
	helm lint helm/ml-platform

security-scan:
	trivy config .

prerequisites:
	@command -v helm >/dev/null || (echo "helm is required" && exit 1)
	@command -v kubectl >/dev/null || (echo "kubectl is required" && exit 1)

deploy: prerequisites
	helm upgrade --install $(RELEASE) helm/ml-platform --namespace $(NAMESPACE) --create-namespace

destroy: prerequisites
	helm uninstall $(RELEASE) --namespace $(NAMESPACE)

local-demo:
	docker compose -f mlflow/docker-compose.yml up

score:
	python -m ml_platform.scoring --model models/sample_model.json --rooms 3 --sqft 1100
