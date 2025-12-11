Aqui está um **markdown pronto para colocar no README** do seu trabalho:

````markdown
# 2º Trabalho de Arquitetura e Organização de Computadores  
## Simulador de Coerência de Cache

Este projeto implementa um simulador de coerência de cache configurável, capaz de processar diferentes conjuntos de operações com base em um arquivo de configuração.

---

## 📌 Como rodar o programa

### 1. Entre na pasta do simulador
```bash
cd SimuladorCoerenciaCache
````

### 2. Execute o simulador passando:

* O arquivo de **configuração** (`config.toml`)
* O arquivo com as **operações** (`S1.data`)

```bash
python main.py config.toml S1.data
```

---

## 📁 Arquivos

### **config.toml**

Arquivo de configurações do simulador.
Define parâmetros como:

* Número de processadores
* Tamanhos de cache
* Políticas de substituição

### **S1.data**

Arquivo contendo as operações a serem executadas pelo simulador:
