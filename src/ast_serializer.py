import json

from src.ast_nodes import (
    Programa, Declaracao, Atribuicao,
    ExpressaoBinaria, Identificador, Numero,
)


def serializar(no):
    if isinstance(no, Programa):
        return {
            "tipo": "Programa",
            "comandos": [serializar(c) for c in no.comandos],
        }
    elif isinstance(no, Declaracao):
        return {
            "tipo": "Declaracao",
            "tipo_variavel": no.tipo_variavel,
            "nome": no.nome,
            "linha": no.linha,
            "coluna": no.coluna,
        }
    elif isinstance(no, Atribuicao):
        return {
            "tipo": "Atribuicao",
            "nome": no.nome,
            "expressao": serializar(no.expressao),
            "linha": no.linha,
            "coluna": no.coluna,
        }
    elif isinstance(no, ExpressaoBinaria):
        return {
            "tipo": "ExpressaoBinaria",
            "operador": no.operador,
            "esquerda": serializar(no.esquerda),
            "direita": serializar(no.direita) if no.direita is not None else None,
            "linha": no.linha,
            "coluna": no.coluna,
        }
    elif isinstance(no, Identificador):
        return {
            "tipo": "Identificador",
            "nome": no.nome,
            "linha": no.linha,
            "coluna": no.coluna,
        }
    elif isinstance(no, Numero):
        return {
            "tipo": "Numero",
            "valor": no.valor,
            "tipo_valor": no.tipo_valor,
            "linha": no.linha,
            "coluna": no.coluna,
        }
    raise ValueError(f"Tipo de no desconhecido: {type(no).__name__}")


def serializar_para_json(no, caminho_saida: str):
    dados = serializar(no)
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
