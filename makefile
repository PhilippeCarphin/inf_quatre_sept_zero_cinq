CONFIG += C++11
CXXFLAGS += -O3 -Wall -Wno-c++11-extensions

prog=graph
file=main.cpp
all:$(prog)

$(prog):$(file)
	g++ $< -o $@ $(CXXFLAGS)
	@echo "$@ compiled"

test:$(prog)
	./$^
