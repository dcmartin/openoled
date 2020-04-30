###
# makefile
###

OBJ := oled96.o fonts.o

all: main oled

oled: oled.o $(OBJ)
	gcc $^ -lm -lpthread -o $@

main: main.o $(OBJ)
	gcc $^ -lm -lpthread -o $@

.c.o:
	gcc -c -O2 -s -DNDENUG -Wall $<

clean:
	rm -f *.o oled main
