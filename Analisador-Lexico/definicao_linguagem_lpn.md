# PARTE 1 - DEFINICAO DA LINGUAGEM LPN

Este arquivo documenta, de forma organizada, os elementos que o analisador lexico reconhece.

## Palavras-chave

- `inteiro`
- `real`
- `texto`
- `se`
- `senao`
- `enquanto`
- `para`
- `funcao`
- `procedimento`
- `retorne`
- `escolha`
- `caso`
- `padrao`
- `pare`
- `continue`

## Identificadores

Regex reconhecida:

```text
[a-zA-Z_][a-zA-Z0-9_]*
```

## Numeros

Regex reconhecidas:

```text
\d+
\d+\.\d+
```

## Strings

Textos entre aspas duplas:

```text
"exemplo"
```

## Operadores aritmeticos

- `+`
- `-`
- `*`
- `/`
- `%`

## Operadores logicos

- `&&`
- `||`
- `!`

## Operadores de comparacao

- `>`
- `<`
- `>=`
- `<=`
- `==`
- `!=`
- `=`

## Delimitadores

- `;`
- `,`
- `:`
- `(`
- `)`
- `{`
- `}`

## Comentarios ignorados pelo lexer

- Linha: `// comentario`
- Bloco: `/* comentario */`

## Resumo tecnico do reconhecimento

O lexer implementado no projeto segue estas regras gerais:

- palavras-chave sao reconhecidas a partir de identificadores validos;
- numeros inteiros e reais possuem tokens distintos;
- comentarios e espacos em branco sao ignorados durante a tokenizacao;
- simbolos nao reconhecidos geram erro lexico;
- a posicao do erro e informada com linha e coluna.

## Organizacao do projeto

Os arquivos principais deste projeto sao:

- `definicao_linguagem_lpn.md`: documenta a linguagem reconhecida.
- `entrada/codigo_exemplo.lpn`: arquivo onde o codigo de entrada pode ser escrito ou alterado.
- `entrada/exemplos_validos/`: colecao de exemplos com entrada lexicamente valida.
- `entrada/exemplos_invalidos/`: colecao de exemplos com erros lexicos para teste.
- `src/lexer_lpn.py`: implementa a analise lexica e controla a execucao principal.
- `src/html_saida.py`: gera o HTML final com tabela de simbolos ou mensagem de erro.
- `saida/resultado_analise_lexica.html`: saida gerada apos a execucao.

## Observacao

Este arquivo descreve a linguagem e a organizacao geral do projeto. A implementacao do lexer e da geracao de HTML esta separada em modulos diferentes para deixar o codigo mais claro e facil de manter.
