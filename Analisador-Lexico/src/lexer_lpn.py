import re
import sys
from pathlib import Path

from html_saida import gerar_erro_html, gerar_tabela_html


# ============================================================================
# ANALISADOR LEXICO DA LPN
# Este arquivo contem toda a implementacao do lexer.
# O codigo que sera analisado deve ser escrito em "entrada/codigo_exemplo.lpn".
# A definicao resumida da linguagem esta em "definicao_linguagem_lpn.md".
# ============================================================================


class ErroLexico(Exception):
    """Erro levantado quando um lexema invalido e encontrado."""

    def __init__(self, mensagem: str, linha: int, coluna: int):
        super().__init__(f"{mensagem} (linha {linha}, coluna {coluna})")
        self.linha = linha
        self.coluna = coluna


class AnalisadorLexicoLPN:
    """Lexer da Linguagem Procedural Nobre (LPN)."""

    PALAVRAS_CHAVE = {
        "inteiro": "INTEIRO",
        "real": "REAL",
        "texto": "TEXTO",
        "se": "SE",
        "senao": "SENAO",
        "enquanto": "ENQUANTO",
        "para": "PARA",
        "funcao": "FUNCAO",
        "procedimento": "PROCEDIMENTO",
        "retorne": "RETORNE",
        "escolha": "ESCOLHA",
        "caso": "CASO",
        "padrao": "PADRAO",
        "pare": "PARE",
        "continue": "CONTINUE",
    }

    ESPECIFICACAO_TOKENS = [
        ("COMENTARIO_BLOCO", r"/\*[\s\S]*?\*/"),
        ("COMENTARIO_LINHA", r"//[^\n]*"),
        ("STRING", r'"(?:\\.|[^"\\])*"'),
        ("NUM_REAL", r"\d+\.\d+"),
        ("NUM_INT", r"\d+"),
        ("E_LOGICO", r"&&"),
        ("OU_LOGICO", r"\|\|"),
        ("MAIOR_IGUAL", r">="),
        ("MENOR_IGUAL", r"<="),
        ("IGUAL", r"=="),
        ("DIFERENTE", r"!="),
        ("ATRIBUICAO", r"="),
        ("MAIOR", r">"),
        ("MENOR", r"<"),
        ("NEGACAO", r"!"),
        ("MAIS", r"\+"),
        ("MENOS", r"-"),
        ("MULT", r"\*"),
        ("DIV", r"/"),
        ("MOD", r"%"),
        ("PONTO_VIRGULA", r";"),
        ("VIRGULA", r","),
        ("DOIS_PONTOS", r":"),
        ("ABRE_PAREN", r"\("),
        ("FECHA_PAREN", r"\)"),
        ("ABRE_CHAVE", r"\{"),
        ("FECHA_CHAVE", r"\}"),
        ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("ESPACO", r"[ \t\r\n]+"),
        ("INVALIDO", r"."),
    ]

    def __init__(self):
        partes = [f"(?P<{nome}>{padrao})" for nome, padrao in self.ESPECIFICACAO_TOKENS]
        self.regex_master = re.compile("|".join(partes))

    def tokenizar(self, codigo_fonte: str):
        tokens = []
        linha = 1
        coluna = 1

        for correspondencia in self.regex_master.finditer(codigo_fonte):
            tipo = correspondencia.lastgroup
            valor = correspondencia.group(tipo)
            linha_atual = linha
            coluna_atual = coluna

            if tipo == "INVALIDO":
                raise ErroLexico(
                    f"Simbolo invalido encontrado: {valor!r}",
                    linha_atual,
                    coluna_atual,
                )

            if tipo not in {"ESPACO", "COMENTARIO_LINHA", "COMENTARIO_BLOCO"}:
                if tipo == "ID" and valor in self.PALAVRAS_CHAVE:
                    tipo = self.PALAVRAS_CHAVE[valor]
                tokens.append((tipo, valor, linha_atual, coluna_atual))

            qtd_quebras = valor.count("\n")
            if qtd_quebras:
                linha += qtd_quebras
                coluna = len(valor.rsplit("\n", 1)[-1]) + 1
            else:
                coluna += len(valor)

        self._validar_trechos_nao_reconhecidos(codigo_fonte)
        return tokens

    def _validar_trechos_nao_reconhecidos(self, codigo_fonte: str):
        """Detecta comentario de bloco nao encerrado."""
        abertura = codigo_fonte.find("/*")
        while abertura != -1:
            fechamento = codigo_fonte.find("*/", abertura + 2)
            if fechamento == -1:
                trecho = codigo_fonte[:abertura]
                linha = trecho.count("\n") + 1
                coluna = len(trecho.rsplit("\n", 1)[-1]) + 1
                raise ErroLexico("Comentario de bloco nao encerrado", linha, coluna)
            abertura = codigo_fonte.find("/*", fechamento + 2)


def carregar_codigo_fonte():
    """
    Carrega o codigo LPN a partir de um arquivo.
    Se nenhum caminho for informado, usa o arquivo entrada/codigo_exemplo.lpn.
    """
    projeto_dir = Path(__file__).resolve().parent.parent
    caminho_entrada = Path(sys.argv[1]) if len(sys.argv) > 1 else projeto_dir / "entrada" / "codigo_exemplo.lpn"
    return caminho_entrada.resolve(), caminho_entrada.read_text(encoding="utf-8")


def main():
    analisador = AnalisadorLexicoLPN()
    projeto_dir = Path(__file__).resolve().parent.parent
    arquivo_saida = projeto_dir / "saida" / "resultado_analise_lexica.html"

    try:
        caminho_entrada, codigo_fonte = carregar_codigo_fonte()
        tokens = analisador.tokenizar(codigo_fonte)
        print("Tokens reconhecidos:")
        for token in tokens:
            print(token)

        gerar_tabela_html(tokens, str(arquivo_saida))
        print(f"\nArquivo analisado: {caminho_entrada}")
        print(f"Resultado HTML gerado em: {arquivo_saida}")
    except FileNotFoundError as erro:
        print(f"Arquivo de entrada nao encontrado: {erro.filename}")
    except ErroLexico as erro:
        gerar_erro_html(str(arquivo_saida), str(erro))
        print(f"Erro lexico: {erro}")
        print(f"Resultado HTML gerado em: {arquivo_saida}")


if __name__ == "__main__":
    main()
