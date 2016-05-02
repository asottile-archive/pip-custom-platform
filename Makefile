REBUILD_FLAG =

.PHONY: all
all: venv test

.PHONY: venv
venv: .venv.touch
	tox -e venv $(REBUILD_FLAG)

.PHONY: tests test
tests: test
test: .venv.touch
	tox $(REBUILD_FLAG)

.PHONY: docker-tests
docker-tests: .venv.touch
	$(eval REBUILD_FLAG := -- tests --docker)
	tox $(REBUILD_FLAG)

.venv.touch: setup.py requirements-dev.txt
	$(eval REBUILD_FLAG := --recreate)
	touch .venv.touch

.PHONY: clean
clean:
	find -name '*.pyc' -delete
	rm -rf .tox
	rm -rf ./venv-*
	rm -f .venv.touch
