import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ_PROJETO / "Analisador-Lexico" / "src"))

from lexer_lpn import AnalisadorLexicoLPN, ErroLexico, carregar_codigo_fonte
from src.parser import Parser
from src.exceptions import ErroSintatico
from src.ast_serializer import serializar_para_json


def main():
    analisador = AnalisadorLexicoLPN()

    try:
        caminho_entrada, codigo_fonte = carregar_codigo_fonte()
    except FileNotFoundError as erro:
        print(f"Arquivo de entrada nao encontrado: {erro.filename}")
        return

    try:
        tokens_lexer = analisador.tokenizar(codigo_fonte)
    except ErroLexico as erro:
        print(f"Erro lexico: {erro}")
        return

    ultimo = tokens_lexer[-1] if tokens_lexer else ("$", "$", 1, 1)
    tokens = list(tokens_lexer) + [("$", "$", ultimo[2], ultimo[3] + 1)]

    print("Tokens reconhecidos pelo lexer:")
    for t in tokens:
        print(f"  {t}")

    try:
        parser = Parser(tokens)
        ast = parser.parse()
        print("\nAnalise sintatica concluida com sucesso!")
        print(f"AST: {ast.tipo} com {len(ast.comandos)} comando(s)")

        caminho_json = RAIZ_PROJETO / "ast.json"
        serializar_para_json(ast, str(caminho_json))
        print(f"AST serializada em: {caminho_json}")

    except ErroSintatico as erro:
        print(f"\nErro sintatico: {erro}")


if __name__ == "__main__":
    main()
