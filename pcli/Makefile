# Makefile for standalone Playlist service (S2)

VER=v0.8

SERVER=`docker inspect s2 --format '{{.NetworkSettings.IPAddress}}'`
PORT=30001

build-pcli:
	docker image build -f Dockerfile -t pcli:$(VER) .

run-pcli:
	docker container run -it --rm --name pcli pcli:$(VER) python3 pcli.py $(SERVER) $(PORT)
