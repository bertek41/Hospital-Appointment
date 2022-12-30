lint:
	black .

venv: lint
	.venv\Scripts\activate

run: venv
	python hospital-appointment/main.py

