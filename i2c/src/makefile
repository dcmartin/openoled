###
# makefile
###

OBJ := oled.o oled96.o fonts.o

all: oled

oled: $(OBJ)
	gcc ${OBJ} -lm -lpthread -o $@


.c.o:
	gcc -c -O2 -s -DNDENUG -Wall $<

clean:
	rm -f *.o oled
