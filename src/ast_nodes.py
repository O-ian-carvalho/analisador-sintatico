class Programa:
    def __init__(self, comandos):
        self.tipo = "Programa"
        self.comandos = comandos


class Declaracao:
    def __init__(self, tipo_variavel: str, nome: str, linha: int, coluna: int):
        self.tipo = "Declaracao"
        self.tipo_variavel = tipo_variavel
        self.nome = nome
        self.linha = linha
        self.coluna = coluna


class Atribuicao:
    def __init__(self, nome: str, expressao, linha: int, coluna: int):
        self.tipo = "Atribuicao"
        self.nome = nome
        self.expressao = expressao
        self.linha = linha
        self.coluna = coluna


class ExpressaoBinaria:
    def __init__(self, operador: str, esquerda, direita, linha: int, coluna: int):
        self.tipo = "ExpressaoBinaria"
        self.operador = operador
        self.esquerda = esquerda
        self.direita = direita
        self.linha = linha
        self.coluna = coluna


class Identificador:
    def __init__(self, nome: str, linha: int, coluna: int):
        self.tipo = "Identificador"
        self.nome = nome
        self.linha = linha
        self.coluna = coluna


class Numero:
    def __init__(self, valor, tipo_valor: str, linha: int, coluna: int):
        self.tipo = "Numero"
        self.valor = valor
        self.tipo_valor = tipo_valor
        self.linha = linha
        self.coluna = coluna
