# Compilador
CXX = g++
# Flags de compilação
CXXFLAGS = -Wall -Wextra -std=c++17 -g
# Nome do executável
TARGET = simulador_cache

# Arquivos fonte
SRCS = src/main.cpp
# Arquivos objeto (substitui .cpp por .o)
OBJS = $(SRCS:.cpp=.o)

# Regra principal
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Regra genérica para .cpp -> .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpeza
clean:
	rm -f $(OBJS) $(TARGET)

# Recompilar tudo
re: clean $(TARGET)

.PHONY: clean re
