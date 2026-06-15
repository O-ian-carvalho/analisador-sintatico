from src.exceptions import ErroSintatico
from src.ast_nodes import (
    Programa, Declaracao, Atribuicao,
    ExpressaoBinaria, Identificador, Numero,
)


MAPA_TOKEN_LEXER_PARA_GRAMATICA = {
    "INTEIRO": "inteiro",
    "REAL": "real",
    "TEXTO": "texto",
    "ID": "id",
    "NUM_INT": "num_int",
    "NUM_REAL": "num_real",
    "MAIS": "mais",
    "MENOS": "menos",
    "MULT": "multiplicacao",
    "DIV": "divisao",
    "MOD": "modulo",
    "ATRIBUICAO": "atribuicao",
    "PONTO_VIRGULA": "ponto_virgula",
    "ABRE_PAREN": "abre_parenteses",
    "FECHA_PAREN": "fecha_parenteses",
}

TABELA_LL = {
    ("P", "inteiro"): 0,
    ("P", "real"): 0,
    ("P", "texto"): 0,
    ("P", "id"): 0,
    ("P", "$"): 0,
    ("L", "inteiro"): 1,
    ("L", "real"): 1,
    ("L", "texto"): 1,
    ("L", "id"): 1,
    ("L", "$"): 2,
    ("C", "inteiro"): 3,
    ("C", "real"): 4,
    ("C", "texto"): 5,
    ("C", "id"): 6,
    ("E", "abre_parenteses"): 7,
    ("E", "id"): 7,
    ("E", "num_int"): 7,
    ("E", "num_real"): 7,
    ("E1", "mais"): 8,
    ("E1", "menos"): 9,
    ("E1", "ponto_virgula"): 10,
    ("E1", "fecha_parenteses"): 10,
    ("T", "abre_parenteses"): 11,
    ("T", "id"): 11,
    ("T", "num_int"): 11,
    ("T", "num_real"): 11,
    ("T1", "multiplicacao"): 12,
    ("T1", "divisao"): 13,
    ("T1", "modulo"): 14,
    ("T1", "mais"): 15,
    ("T1", "menos"): 15,
    ("T1", "ponto_virgula"): 15,
    ("T1", "fecha_parenteses"): 15,
    ("F", "abre_parenteses"): 16,
    ("F", "id"): 17,
    ("F", "num_int"): 18,
    ("F", "num_real"): 19,
}

PRODUCAO_NOME = {
    0: "P -> L",
    1: "L -> C L",
    2: "L -> epsilon",
    3: "C -> inteiro id ponto_virgula",
    4: "C -> real id ponto_virgula",
    5: "C -> texto id ponto_virgula",
    6: "C -> id atribuicao E ponto_virgula",
    7: "E -> T E1",
    8: "E1 -> mais T E1",
    9: "E1 -> menos T E1",
    10: "E1 -> epsilon",
    11: "T -> F T1",
    12: "T1 -> multiplicacao F T1",
    13: "T1 -> divisao F T1",
    14: "T1 -> modulo F T1",
    15: "T1 -> epsilon",
    16: "F -> abre_parenteses E fecha_parenteses",
    17: "F -> id",
    18: "F -> num_int",
    19: "F -> num_real",
}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ("$", "$", 1, 1)

    def tipo_gramatical(self, token):
        if token[0] == "$":
            return "$"
        return MAPA_TOKEN_LEXER_PARA_GRAMATICA.get(token[0])

    def consumir(self, tipo_esperado=None):
        token = self.token_atual()
        tipo = self.tipo_gramatical(token)
        if tipo is None:
            self.erro(
                f"Token '{token[1]}' ({token[0]}) nao pertence ao "
                f"subconjunto sintatico LL(1)"
            )
        if tipo_esperado is not None and tipo != tipo_esperado:
            self.erro(
                f"Esperado '{tipo_esperado}', encontrado '{token[1]}' "
                f"do tipo '{token[0]}'"
            )
        self.pos += 1
        return token

    def erro(self, mensagem):
        token = self.token_atual()
        raise ErroSintatico(mensagem, token[2], token[3])

    def consultar_tabela(self, nao_terminal):
        token = self.token_atual()
        tipo = self.tipo_gramatical(token)
        if tipo is None:
            self.erro(
                f"Token '{token[1]}' ({token[0]}) nao pertence ao "
                f"subconjunto sintatico LL(1) durante expansao de "
                f"{nao_terminal}"
            )
        producao = TABELA_LL.get((nao_terminal, tipo))
        if producao is None:
            esperados = {
                term
                for (nt, term) in TABELA_LL
                if nt == nao_terminal
            }
            self.erro(
                f"Token inesperado '{token[1]}' ({token[0]}). "
                f"Esperado um dos terminais: {sorted(esperados)} "
                f"durante expansao de {nao_terminal}"
            )
        return producao

    def parse(self):
        programa = self.parse_P()
        token = self.token_atual()
        if token[0] != "$":
            self.erro(
                f"Tokens nao processados apos o fim do programa: "
                f"'{token[1]}' ({token[0]})"
            )
        return programa

    def parse_P(self):
        prod = self.consultar_tabela("P")
        if prod == 0:
            comandos = self.parse_L()
            return Programa(comandos)
        raise AssertionError(f"Producao inesperada para P: {prod}")

    def parse_L(self):
        prod = self.consultar_tabela("L")
        if prod == 1:
            cmd = self.parse_C()
            resto = self.parse_L()
            if isinstance(resto, list):
                return [cmd] + resto
            return [cmd]
        elif prod == 2:
            return []
        raise AssertionError(f"Producao inesperada para L: {prod}")

    def parse_C(self):
        prod = self.consultar_tabela("C")
        if prod == 3:
            tok_tipo = self.consumir("inteiro")
            tok_nome = self.consumir("id")
            self.consumir("ponto_virgula")
            return Declaracao(
                tok_tipo[1], tok_nome[1], tok_tipo[2], tok_tipo[3]
            )
        elif prod == 4:
            tok_tipo = self.consumir("real")
            tok_nome = self.consumir("id")
            self.consumir("ponto_virgula")
            return Declaracao(
                tok_tipo[1], tok_nome[1], tok_tipo[2], tok_tipo[3]
            )
        elif prod == 5:
            tok_tipo = self.consumir("texto")
            tok_nome = self.consumir("id")
            self.consumir("ponto_virgula")
            return Declaracao(
                tok_tipo[1], tok_nome[1], tok_tipo[2], tok_tipo[3]
            )
        elif prod == 6:
            tok_nome = self.consumir("id")
            self.consumir("atribuicao")
            expr = self.parse_E()
            self.consumir("ponto_virgula")
            return Atribuicao(
                tok_nome[1], expr, tok_nome[2], tok_nome[3]
            )
        raise AssertionError(f"Producao inesperada para C: {prod}")

    def parse_E(self):
        prod = self.consultar_tabela("E")
        if prod == 7:
            t_node = self.parse_T()
            return self.parse_E1(t_node)
        raise AssertionError(f"Producao inesperada para E: {prod}")

    def parse_E1(self, esquerda):
        prod = self.consultar_tabela("E1")
        if prod == 8:
            tok_op = self.consumir("mais")
            t_node = self.parse_T()
            e1_node = self.parse_E1(t_node)
            return ExpressaoBinaria(
                tok_op[1], esquerda, e1_node,
                tok_op[2], tok_op[3],
            )
        elif prod == 9:
            tok_op = self.consumir("menos")
            t_node = self.parse_T()
            e1_node = self.parse_E1(t_node)
            return ExpressaoBinaria(
                tok_op[1], esquerda, e1_node,
                tok_op[2], tok_op[3],
            )
        elif prod == 10:
            return esquerda
        raise AssertionError(f"Producao inesperada para E1: {prod}")

    def parse_T(self):
        prod = self.consultar_tabela("T")
        if prod == 11:
            f_node = self.parse_F()
            return self.parse_T1(f_node)
        raise AssertionError(f"Producao inesperada para T: {prod}")

    def parse_T1(self, esquerda):
        prod = self.consultar_tabela("T1")
        if prod == 12:
            tok_op = self.consumir("multiplicacao")
            f_node = self.parse_F()
            t1_node = self.parse_T1(f_node)
            return ExpressaoBinaria(
                tok_op[1], esquerda, t1_node,
                tok_op[2], tok_op[3],
            )
        elif prod == 13:
            tok_op = self.consumir("divisao")
            f_node = self.parse_F()
            t1_node = self.parse_T1(f_node)
            return ExpressaoBinaria(
                tok_op[1], esquerda, t1_node,
                tok_op[2], tok_op[3],
            )
        elif prod == 14:
            tok_op = self.consumir("modulo")
            f_node = self.parse_F()
            t1_node = self.parse_T1(f_node)
            return ExpressaoBinaria(
                tok_op[1], esquerda, t1_node,
                tok_op[2], tok_op[3],
            )
        elif prod == 15:
            return esquerda
        raise AssertionError(f"Producao inesperada para T1: {prod}")

    def parse_F(self):
        prod = self.consultar_tabela("F")
        if prod == 16:
            self.consumir("abre_parenteses")
            expr = self.parse_E()
            self.consumir("fecha_parenteses")
            return expr
        elif prod == 17:
            tok = self.consumir("id")
            return Identificador(tok[1], tok[2], tok[3])
        elif prod == 18:
            tok = self.consumir("num_int")
            return Numero(int(tok[1]), "num_int", tok[2], tok[3])
        elif prod == 19:
            tok = self.consumir("num_real")
            return Numero(float(tok[1]), "num_real", tok[2], tok[3])
        raise AssertionError(f"Producao inesperada para F: {prod}")
