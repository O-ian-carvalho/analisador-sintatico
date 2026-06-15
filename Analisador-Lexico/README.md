# Analisador Lexico da LPN

Este projeto implementa um analisador lexico em Python para a linguagem **LPN (Linguagem Procedural Nobre)**.

O programa le um codigo-fonte em LPN, reconhece tokens com expressoes regulares e gera um arquivo HTML com o resultado da analise. Quando ocorre erro lexico, o HTML apresenta a mensagem correspondente com linha e coluna.

## Objetivo

O projeto foi desenvolvido para:

- reconhecer lexemas validos da linguagem LPN;
- transformar a entrada em tokens no formato `(TIPO_TOKEN, valor)`;
- ignorar espacos em branco e comentarios;
- detectar erros lexicos;
- gerar uma saida HTML com sucesso ou erro.

## Estrutura do projeto

Os arquivos principais sao:

- `definicao_linguagem_lpn.md`: documentacao da linguagem reconhecida pelo analisador.
- `entrada/codigo_exemplo.lpn`: arquivo de entrada usado para os testes.
- `entrada/exemplos_validos/`: exemplos de codigo que devem ser aceitos pelo lexer.
- `entrada/exemplos_invalidos/`: exemplos de codigo que devem gerar erro lexico.
- `src/lexer_lpn.py`: modulo principal com a logica do lexer e o fluxo de execucao.
- `src/html_saida.py`: modulo responsavel pela geracao do HTML de resultado.
- `saida/resultado_analise_lexica.html`: arquivo gerado apos a execucao.
- `.vscode/launch.json`: configuracao para executar o projeto pelo VS Code.

## Requisitos

Para executar o projeto, voce precisa de:

- Python 3;
- VS Code;
- extensao `Python` da Microsoft no VS Code.

## Como executar no VS Code

1. Abra o VS Code.
2. Escolha `File > Open Folder`.
3. Abra a pasta do projeto.
4. Edite o arquivo `entrada/codigo_exemplo.lpn` com o codigo que deseja analisar.
5. Se necessario, selecione o interpretador Python em `Ctrl + Shift + P` > `Python: Select Interpreter`.
6. Abra o arquivo `src/lexer_lpn.py`.
7. Pressione `F5`.
8. Se o VS Code solicitar a configuracao de execucao, selecione `Executar Lexer LPN`.
9. Ao final, abra `saida/resultado_analise_lexica.html`.

## Fluxo de funcionamento

O funcionamento do projeto acontece assim:

1. `src/lexer_lpn.py` le o conteudo de `entrada/codigo_exemplo.lpn`.
2. O lexer reconhece os tokens com base nas expressoes regulares definidas na implementacao.
3. Se nao houver erro lexico, `src/html_saida.py` gera a tabela de simbolos em HTML.
4. Se houver erro lexico, `src/html_saida.py` gera um HTML com a mensagem de erro.

## Onde editar a entrada

O codigo que sera analisado deve ser escrito em:

```text
entrada/codigo_exemplo.lpn
```

Tambem ha arquivos prontos para teste em:

```text
entrada/exemplos_validos/
entrada/exemplos_invalidos/
```

## Onde ver o resultado

O resultado da analise aparece em:

```text
saida/resultado_analise_lexica.html
```

Esse arquivo pode apresentar dois cenarios:

- sucesso: mostra o status da analise e a tabela de simbolos;
- erro lexico: mostra a mensagem de erro com linha e coluna.

## Exemplo de uso

Exemplo de codigo valido em `entrada/codigo_exemplo.lpn`:

```text
inteiro x;
x = 10;
```

Saida esperada de tokens no terminal:

```text
('INTEIRO', 'inteiro')
('ID', 'x')
('PONTO_VIRGULA', ';')
('ID', 'x')
('ATRIBUICAO', '=')
('NUM_INT', '10')
('PONTO_VIRGULA', ';')
```

## Como testar erro lexico

Para verificar o tratamento de erro, escreva um simbolo invalido em `entrada/codigo_exemplo.lpn`, por exemplo:

```text
inteiro x;
@
```

Depois execute novamente com `F5`.

O HTML gerado deve exibir uma mensagem semelhante a:

```text
Simbolo invalido encontrado: '@' (linha 2, coluna 1)
```

## Arquivos de exemplo

O projeto agora inclui exemplos separados para facilitar demonstracoes e testes:

- `entrada/exemplos_validos/exemplo_basico.lpn`
- `entrada/exemplos_validos/exemplo_com_texto_e_real.lpn`
- `entrada/exemplos_validos/exemplo_com_comentarios.lpn`
- `entrada/exemplos_invalidos/exemplo_simbolo_invalido.lpn`
- `entrada/exemplos_invalidos/exemplo_comentario_nao_fechado.lpn`
- `entrada/exemplos_invalidos/exemplo_string_nao_fechada.lpn`

## Resumo das responsabilidades

- `src/lexer_lpn.py` concentra a analise lexica, a leitura do arquivo de entrada e a execucao principal.
- `src/html_saida.py` concentra a geracao da saida HTML.
- `definicao_linguagem_lpn.md` descreve os elementos reconhecidos pela linguagem.

## Observacoes

- Nao e necessario editar o codigo Python para testar novas entradas.
- Basta alterar `entrada/codigo_exemplo.lpn`, executar `src/lexer_lpn.py` e abrir o HTML gerado em `saida/`.
- A separacao entre lexer e geracao de HTML deixa o projeto mais organizado e mais facil de manter.
