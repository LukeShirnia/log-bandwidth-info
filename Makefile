export TZ=Europe/London

test tests: unittests pycodestyle

unittests:
	@PYTHONPATH=. pytest --cov=getbandwidthinfo --cov-report xml:cobertura.xml --cov-report term-missing

pycodestyle:
	@pycodestyle getbandwidthinfo.py

pylint:
	@pylint --rcfile=pylint.cfg getbandwidthinfo.py -j 4 -f parseable -r n 

clean:
	find . -name \*.pyc -delete
	rm -rf __pycache__ .cache .coverage .pytest_cache
	rm -rf tests/__pycache__ tests/.cache tests/.coverage tests/.pytest_cache