install:

check:
	docker-compose run --rm hangman flake8 --ignore=E501,E402 /code/hangman/hangman /code/hangman/setup.py

create-egg:
	docker-compose run --rm hangman bash -c "export PYTHONPATH='/tmp/python-tmp' \
		&& cd /code/hangman \
		&& mkdir -p /tmp/python-tmp \
		&& $$(which python3) -c \"import setuptools, tokenize; __file__='/code/hangman/setup.py'; exec(compile(getattr(tokenize, 'open', open)(__file__).read().replace('\\r\\n', '\\n'), __file__, 'exec'))\" develop --exclude-scripts --no-deps --install-dir=/tmp/python-tmp"
