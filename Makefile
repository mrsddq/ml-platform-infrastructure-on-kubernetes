.PHONY: test validate score

test:
	python -m unittest discover -s tests

validate: test
	python scripts/validate_layout.py

score:
	python -m ml_platform.scoring --model models/sample_model.json --rooms 3 --sqft 1100
