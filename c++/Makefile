# Compilador
CXX = g++
# Flags de compilação
CXXFLAGS = -Wall -Wextra -std=c++17 -g
# Nome do executável
TARGET = simulador_cache.exe

PATHSRCS = src/
PATHOBJS = objects/
# Arquivos fonte
SRCS = main.cpp
# Arquivos objeto com path completo
OBJS = $(addprefix $(PATHOBJS), $(SRCS:.cpp=.o))

# Regra principal
$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

# Regra genérica para .cpp -> .o
$(PATHOBJS)%.o: $(PATHSRCS)%.cpp
	if not exist $(PATHOBJS) mkdir $(PATHOBJS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpeza
clean:
	if exist $(PATHOBJS) rmdir /s /q $(PATHOBJS)
	if exist $(TARGET) del $(TARGET)

# Recompilar tudo
re: clean $(TARGET)

.PHONY: clean re
