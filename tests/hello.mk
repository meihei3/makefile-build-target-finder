hello.o: hello.c
	gcc -c hello.c

world.o: world.c
	gcc -c world.c

helloWorld: hello.o world.o
	gcc -o helloWorld hello.o world.o
