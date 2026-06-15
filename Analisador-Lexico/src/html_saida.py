import html
from pathlib import Path


def gerar_tabela_html(tokens, caminho_saida: str):
    """Gera um arquivo HTML com a tabela de simbolos."""
    linhas_tabela = []
    for tipo, valor, *_ in tokens:
        linhas_tabela.append(
            "        <tr>"
            f"<td>{html.escape(tipo)}</td>"
            f"<td>{html.escape(valor)}</td>"
            "</tr>"
        )

    conteudo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabela de Simbolos - LPN</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f4f6f8;
            color: #1f2933;
        }}
        .secao {{
            margin-bottom: 28px;
            padding: 20px;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        h1 {{
            margin-bottom: 20px;
        }}
        h2 {{
            margin-top: 0;
        }}
        .sucesso {{
            color: #166534;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #d9e2ec;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background: #102a43;
            color: #ffffff;
        }}
        tr:nth-child(even) {{
            background: #f8fbff;
        }}
    </style>
</head>
<body>
    <h1>Resultado da Analise Lexica da LPN</h1>

    <section class="secao">
        <h2>Status da Analise</h2>
        <p class="sucesso">Analise concluida com sucesso. Nenhum erro lexico foi encontrado.</p>
    </section>

    <section class="secao">
        <h2>Tabela de Simbolos</h2>
        <table>
            <thead>
                <tr>
                    <th>Tipo do Token</th>
                    <th>Valor</th>
                </tr>
            </thead>
            <tbody>
{chr(10).join(linhas_tabela)}
            </tbody>
        </table>
    </section>
</body>
</html>
"""

    Path(caminho_saida).write_text(conteudo, encoding="utf-8")


def gerar_erro_html(caminho_saida: str, mensagem_erro: str):
    """Gera um arquivo HTML informando o erro lexico encontrado."""
    conteudo = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erro Lexico - LPN</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #fef2f2;
            color: #7f1d1d;
        }}
        .secao {{
            padding: 20px;
            background: #ffffff;
            border-left: 6px solid #dc2626;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }}
        code {{
            font-size: 1rem;
        }}
    </style>
</head>
<body>
    <h1>Resultado da Analise Lexica da LPN</h1>
    <section class="secao">
        <h2>Erro Lexico Encontrado</h2>
        <p>O codigo exemplo possui um erro lexico e nao foi possivel gerar a tabela de simbolos.</p>
        <p><code>{html.escape(mensagem_erro)}</code></p>
    </section>
</body>
</html>
"""

    Path(caminho_saida).write_text(conteudo, encoding="utf-8")
