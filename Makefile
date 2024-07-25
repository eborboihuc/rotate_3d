##
# Docker project makefile.
##
.SHELL := bash
MAKEFLAGS += --warn-undefined-variables
# .SHELLFLAGS := -euo pipefail -c
.DEFAULT_GOAL := none

THIS_MAKEFILE := $(abspath $(firstword $(MAKEFILE_LIST)))
THIS_MAKEFILE := `python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' ${THIS_MAKEFILE}`
SRC_ROOT := $(shell dirname ${THIS_MAKEFILE})

DOCKER_IMAGE_NAME?=imgrot
DOCKER_ORG?=robotwranglers
SHORT_SHA=$(shell git rev-parse --short HEAD)
PYNCHON_CLI_VERSION=baf56b7
# pynchon.run=docker run -v `pwd`:/workspace -w/workspace robotwranglers/pynchon:${PYNCHON_CLI_VERSION} 
pynchon.run=pynchon

.PHONY: build docs

init:
build: docker.build
clean: docker.clean py-clean

docs: docs.vhs docs.jinja docs.rotations
	python imgrot.py img/icon.png --stream > img/demo.gif
docs.jinja: 
	${pynchon.run} jinja render README.md.j2
docs.vhs:; PS1="$$ " sh -c "${pynchon.run} vhs apply"
docs.rotations:
	python imgrot.py img/graph.png --bg lightblue --rotation x --stream > img/rx.gif
	python imgrot.py img/graph.png --bg lightblue --rotation y --stream > img/ry.gif
	python imgrot.py img/graph.png --bg lightblue --rotation s --stream > img/rs.gif
	python imgrot.py img/graph.png --bg lightblue --rotation j --stream > img/rj.gif
	python imgrot.py img/graph.png --bg lightblue --rotation w --stream > img/rw.gif
	python imgrot.py img/graph.png --bg lightblue --rotation f --stream > img/rf.gif
	python imgrot.py img/graph.png --bg lightblue --rotation exit-ul --stream > img/rul.gif
	python imgrot.py img/graph.png --bg lightblue --rotation exit-ur --stream > img/rur.gif
	python imgrot.py img/graph.png --bg lightblue --rotation exit-lr --stream > img/rlr.gif
	python imgrot.py img/graph.png --bg lightblue --rotation exit-ll --stream > img/rll.gif


docker.clean:
	docker rmi $(DOCKER_IMAGE_NAME) >/dev/null || true

docker.build build.docker:	
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker tag $(DOCKER_IMAGE_NAME) ${DOCKER_ORG}/imgrot:latest
	docker tag $(DOCKER_IMAGE_NAME) ${DOCKER_ORG}/imgrot:${SHORT_SHA}

docker.push:
	docker push ${DOCKER_ORG}/imgrot:latest
	docker push ${DOCKER_ORG}/imgrot:${SHORT_SHA}

docker.shell:
	docker run -it --rm -v `pwd`:/workspace -w /workspace \
		--entrypoint bash $(DOCKER_IMAGE_NAME)

docker.base=docker run --rm -v `pwd`:/workspace -w /workspace 
docker.test:
	set -x \
	&& ${docker.base} \
		--entrypoint sh $(DOCKER_IMAGE_NAME) \
		-x -c "ls /opt/imgrot > /dev/null" \
	&& ${docker.base} $(DOCKER_IMAGE_NAME) \
		img/icon.png \
		--range 360 --img-shape 200x200 \
		--stream > .tmp.output.gif \
	&& (which imgcat && .tmp.output.gif || true) \
	&& ${docker.base} $(DOCKER_IMAGE_NAME) \
		img/icon.png --display

test: docker.test

py-clean:
	rm -rf tmp.pypi* dist/* build/* \
	&& rm -rf src/*.egg-info/
	find . -name '*.tmp.*' -delete
	find . -name '*.pyc' -delete
	find . -name  __pycache__ -delete
	find . -type d -name .tox | xargs -n1 -I% bash -x -c "rm -rf %"
	rmdir build || true
# version:
# 	@python setup.py --version
# pypi-release:
# 	PYPI_RELEASE=1 make build \
# 	&& twine upload \
# 	--user $${PYPI_USER} \
# 	--password $${PYPI_TOKEN} \
# 	dist/*

release: clean normalize static-analysis test

tox-%:
	tox -e ${*}

normalize: tox-normalize
lint static-analysis: tox-static-analysis
# smoke-test stest: tox-stest
# test-integrations itest: tox-itest
# utest test-units: tox-utest
# dtest: tox-dtest
# docs-test: dtest
# test: test-units test-integrations smoke-test
# iterate: clean normalize lint test