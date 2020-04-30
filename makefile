###
# makefile
###

default: i2c spi server listen


i2c:
	make -C i2c all

spi:
	make -C spi all

server: i2c spi
	./sh/server.sh

listen:
	./sh/listen.sh

.PHONY: i2c spi server listen
