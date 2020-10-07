###
# makefile
###

ACLOCAL := $(shell v=$$(aclocal --version | head -1 | awk '{ print $$4 }') && echo $${v%.*})

default: aclocal server.sh.json

aclocal:
ifneq ($(ACLOCAL),1.16)
	@echo "Installing latest aclocal (v1.16); current version: ${ACLOCAL}"
	wget http://mirrors.kernel.org/ubuntu/pool/main/a/automake-1.16/automake_1.16.1-4ubuntu6_all.deb
	sudo dpkg -i automake_1.16.1-4ubuntu6_all.deb
endif

all: default listen.sh.json test

libs: i2c spi

i2c: 
	make -C i2c all

spi:
	make -C spi all

server.sh.json: libs
	./sh/server.sh

listen.sh.json:
	./sh/listen.sh

logs:
	tail -f $(jq -r '.debug.logto' listen.sh.json) $(jq -r '.debug.logto' server.sh.json)

test: server.sh.json
	export URL=$(shell jq -r '.endpoints[]|select(.name=="display/picture").url' $^) \
	  && curl -v $${URL} -d @samples/event_annotated.json

tidy:
	rm -f *.sh.*.out

clean:
	rm -f *.sh.json
	make -C i2c clean
	make -C spi clean

.PHONY: i2c spi test clean tidy listen
