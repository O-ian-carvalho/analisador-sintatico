"""
Testes do analisador sintatico LL(1).

Cada teste documenta o comportamento esperado:
- Casos validos: produzem AST sem erros
- Casos invalidos: disparam ErroSintatico ou ErroLexico
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "Analisador-Lexico" / "src"))

from lexer_lpn import AnalisadorLexicoLPN, ErroLexico
from src.parser import Parser
from src.exceptions import ErroSintatico


analisador = AnalisadorLexicoLPN()


def tokenizar(codigo):
    toks = analisador.tokenizar(codigo)
    ultimo = toks[-1] if toks else ("$", "$", 1, 1)
    return list(toks) + [("$", "$", ultimo[2], ultimo[3] + 1)]


def analisar(codigo):
    tokens = tokenizar(codigo)
    parser = Parser(tokens)
    return parser.parse()


def testar(nome, codigo, esperado_sucesso=True, explicacao=""):
    try:
        ast = analisar(codigo)
        if esperado_sucesso:
            print(f"[OK]   {nome}")
            if explicacao:
                print(f"       -> {explicacao}")
            return True
        else:
            print(f"[FALHOU] {nome} — deveria ter falhado")
            return False
    except (ErroSintatico, ErroLexico) as e:
        if not esperado_sucesso:
            print(f"[OK]   {nome}")
            print(f"       -> {explicacao}")
            print(f"       -> Erro gerado: {e}")
            return True
        else:
            print(f"[FALHOU] {nome} — erro inesperado: {e}")
            return False


print("=" * 60)
print("TESTES - CASOS VALIDOS")
print("=" * 60)

# Programa vazio: verifica se L -> epsilon eh reconhecida sem tokens
testar("Programa vazio", "", True,
       "L -> epsilon: programa sem comandos deve ser aceito")

# Declaracao inteiro: C -> inteiro id ponto_virgula
testar("Declaracao inteiro", "inteiro x;", True,
       "C -> inteiro id ;: declaracao de variavel inteira")

# Declaracao real: C -> real id ponto_virgula
testar("Declaracao real", "real y;", True,
       "C -> real id ;: declaracao de variavel real")

# Declaracao texto: C -> texto id ponto_virgula
testar("Declaracao texto", "texto msg;", True,
       "C -> texto id ;: declaracao de variavel texto")

# Atribuicao simples: C -> id = E ; com E -> T -> F -> num_int
testar("Atribuicao simples", "x = 10;", True,
       "C -> id = E ;: atribuicao de literal inteiro")

# Declaracao + Atribuicao: duas producoes de C em sequencia (L -> C L)
testar("Declaracao + Atribuicao", "inteiro x;\nx = 10;", True,
       "L -> C L: sequencia de declaracao seguida de atribuicao")

# Multiplas declaracoes: tres tipos diferentes em sequencia
testar("Multiplas declaracoes", "inteiro a;\nreal b;\ntexto c;", True,
       "L -> C L (multiplas): tres declaracoes de tipos diferentes")

# Expressao com adicao: E1 -> mais T E1
testar("Expressao com adicao", "x = a + 1;", True,
       "E1 -> + T E1: expressao com operador de adicao")

# Expressao com subtracao: E1 -> menos T E1
testar("Expressao com subtracao", "x = a - 1;", True,
       "E1 -> - T E1: expressao com operador de subtracao")

# Expressao com multiplicacao: T1 -> multiplicacao F T1
testar("Expressao com multiplicacao", "x = a * 2;", True,
       "T1 -> * F T1: expressao com operador de multiplicacao")

# Expressao com divisao: T1 -> divisao F T1
testar("Expressao com divisao", "x = a / 2;", True,
       "T1 -> / F T1: expressao com operador de divisao")

# Expressao com operadores combinados: precedencia * sobre +
testar("Expressao com operadores combinados", "x = a + b * c;", True,
       "Precedencia: * liga mais forte que + (T1 antes de E1)")

# Expressao com parenteses: F -> ( E ) sobrepoe precedencia
testar("Expressao com parenteses", "x = (a + b) * c;", True,
       "F -> ( E ): parenteses alteram precedencia padrao")

# Expressao com parenteses aninhados: F -> ( E ) com E -> ( E )
testar("Expressao com parenteses aninhados", "x = ((a + b));", True,
       "F -> ( E ) recursivo: parenteses aninhados sao eliminados na AST")

# Expressao com num_real: F -> num_real
testar("Expressao com num_real", "x = 3.14 * 2;", True,
       "F -> num_real: literal real em expressao")

# Programa completo: todas as producoes principais combinadas
testar("Programa completo",
       "inteiro x;\nreal y;\nx = 10;\ny = x + 1;", True,
       "Combinacao de P -> L, L -> C L, C -> declaracao/atribuicao, E com operadores")

# Operador modulo: T1 -> modulo F T1
testar("Operador modulo", "x = a % 2;", True,
       "T1 -> % F T1: expressao com operador de modulo")

# Atribuicao encadeada: todos os operadores aritmeticos combinados
testar("Atribuicao encadeada por expressao",
       "resultado = a + b - c * d / e;", True,
       "Multiplos operadores na mesma expressao (+ - * /)")

print()
print("=" * 60)
print("TESTES - CASOS INVALIDOS")
print("=" * 60)

# Token SE fora do subconjunto LL(1) -> erro em P
testar("Token fora do subconjunto LL(1) (se)", "se (x) {}", False,
       "Token 'se' (SE) nao faz parte do subconjunto LL(1): erro ao expandir P")

# Token FUNCAO fora do subconjunto LL(1)
testar("Token fora do subconjunto LL(1) (funcao)", "funcao f() {}", False,
       "Token 'funcao' (FUNCAO) nao faz parte do subconjunto LL(1): erro ao expandir P")

# Token STRING fora do subconjunto LL(1)
testar("Token fora do subconjunto LL(1) (string)", 'x = "texto";', False,
       "Token STRING nao pertence ao subconjunto LL(1): erro ao expandir E")

# Ausencia de ponto e virgula: C -> inteiro id ; mas ; nao encontrado
testar("Ponto e virgula ausente", "inteiro x", False,
       "C -> inteiro id ; espera ';' mas encontra EOF")

# Identificador ausente: C -> inteiro id ; mas id nao encontrado
testar("Identificador ausente na declaracao", "inteiro ;", False,
       "C -> inteiro id ; espera 'id' mas encontra ';'")

# Atribuicao sem expressao: C -> id = E ; mas E nao encontrada
testar("Atribuicao sem expressao", "x = ;", False,
       "C -> id = E ; espera expressao mas encontra ';'")

# Parentese nao fechado: F -> ( E ) espera ) mas encontra ;
testar("Parentese nao fechado", "x = (a + b;", False,
       "F -> ( E ) espera ')' mas encontra ';'")

# Parentese extra sem abertura: ) nao esperado na expressao
testar("Parentese nao aberto", "x = a + b);", False,
       "Token ')' nao esperado em E1 ou T1: producao nao prevê ) neste ponto")

# Operador + sem operando direito: falha em E1
testar("Operador sem operando direito", "x = + 1;", False,
       "E1 -> + T E1: '+' exige T a direita, mas E nao comeca com operador")

# Operador * sem operando esquerdo na expressao
testar("Operador sem operando esquerdo na expressao", "x = a + * 1;", False,
       "T1 -> * F T1: '*' exige F a direita, mas T nao comeca com operador")

# Identificador 'booleano' interpretado como ID (nao e palavra-chave)
# C -> id = E ; falha porque = nao encontrado, 'x' vira expressao
testar("Tipo inexistente na gramatica", "booleano x;", False,
       "'booleano' e token ID, parser tenta C -> id = E ; mas ';' nao e '='")

# EOF no meio de declaracao: C -> inteiro id ; falta id e ;
testar("Fim inesperado (declaracao incompleta)", "inteiro ", False,
       "C -> inteiro id ;: EOF encontrado antes de 'id'")

# EOF no meio de expressao: E1 -> + T E1 falta T
testar("Fim inesperado (expressao incompleta)", "x = a + ", False,
       "E1 -> + T E1: EOF encontrado antes de T (expressao incompleta)")
