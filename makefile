###
# makefile
###

default: server.json test listen.json

libs: i2c spi

i2c: 
	make -C i2c all

spi:
	make -C spi all

server.json: libs
	./sh/server.sh | tee server.json


test: server.json
	export URL=$(shell jq -r '.endpoints[]|select(.name=="display/picture").url' $^) \
	  && curl -v $${URL} -d @samples/event_annotated.json

listen.json:
	./sh/listen.sh | tee listen.json

tidy:
	rm -f *.sh.*.out

clean:
	rm -f *.sh.json
	make -C i2c clean
	make -C spi clean

.PHONY: i2c spi test clean tidy
