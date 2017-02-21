CONFIG += C++11
CXXFLAGS += -O3 -Wall -Wno-c++11-extensions

prog=graph
file=main.cpp
all:$(file)
	g++ $< -o $(prog) $(CXXFLAGS)
	./$(prog)
	rm ./$(prog)
	@echo "$@ compiled"