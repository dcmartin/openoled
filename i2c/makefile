###
# makefile
###

VERSION := 0.0.1

LOCAL_IP_ADDRESS := $(shell hostname -I | awk '{ print $$1 }')

all: run

stop:
	-docker stop oled

remove: stop
	-docker rm -f oled

run: remove build
	docker run \
	  -d \
          -e LOCAL_IP_ADDRESS=$(LOCAL_IP_ADDRESS) \
	  --privileged \
          --name oled \
	  --restart unless-stopped \
          --net=host \
          ${USER}/oled:${VERSION}

build:
	docker build -t ${USER}/oled:${VERSION} .

push: build
	docker push ${USER}/oled:${VERSION}
