# Analisador Sintático LL(1) - LPN

Este projeto implementa um analisador sintático LL(1) preditivo dirigido por tabela para um subconjunto da LPN (Linguagem Procedural Nobre). A análise sintática consome os tokens gerados pelo analisador léxico, aplica as produções definidas na tabela LL(1), constrói uma Árvore Sintática Abstrata (AST) e serializa essa árvore no arquivo `ast.json`.

O escopo do projeto é exclusivamente sintático. Não há análise semântica, verificação de tipos, tabela de símbolos, recuperação de erros, geração de código, otimizações ou execução de programas.

---

## 1. Escopo e limitações

O lexer reconhece um conjunto maior de tokens da linguagem LPN. O parser, porém, utiliza apenas os terminais presentes na gramática LL(1) e em sua tabela de análise. Portanto, uma sequência de tokens válida para o lexer não é necessariamente válida para o parser.

O analisador sintático reconhece exclusivamente as cadeias geradas pela gramática LL(1) e utiliza apenas os terminais presentes em sua tabela de análise. Tokens reconhecidos pelo lexer, mas ausentes da tabela LL(1), estão fora do escopo deste trabalho e provocam erro sintático.

Todo programa aceito pertence à linguagem gerada pela gramática LL(1). Qualquer token ou sequência de tokens sem produção correspondente na tabela LL(1) deve gerar `ErroSintatico`. O parser reconhece exclusivamente cadeias deriváveis da gramática LL(1) definida neste documento.

Um programa é considerado sintaticamente válido se, e somente se, toda a sequência de tokens puder ser consumida pelas produções indicadas pela tabela LL(1), terminando com o símbolo de fim de entrada `$`.

---

## 2. Estrutura do projeto

```text
analisador-sintatico/
├── main.py
├── README.md
├── tabela LL.md
├── ast.json
├── Analisador-Lexico/
│   └── src/
│       ├── lexer_lpn.py
│       └── html_saida.py
├── src/
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── ast_serializer.py
│   └── exceptions.py
├── exemplos/
│   ├── entrada_valida.lpn
│   ├── ast_exemplo.json
│   └── exemplos_invalidos/
└── tests/
    └── test_parser.py
```

Arquivos principais:

- `Analisador-Lexico/src/lexer_lpn.py`: implementa o analisador léxico.
- `src/parser.py`: implementa o parser LL(1), o mapeamento de tokens e a tabela de análise.
- `src/ast_nodes.py`: define os nós da AST.
- `src/ast_serializer.py`: serializa a AST para JSON.
- `src/exceptions.py`: define `ErroSintatico`.
- `main.py`: executa a análise completa, combinando lexer, parser e serialização da AST.
- `tests/test_parser.py`: executa a suíte de testes automatizados.

---

## 3. Gramática LL(1)

### Símbolo inicial

`P` (Programa)

### Símbolos não-terminais

```text
P, L, C, E, E1, T, T1, F
```

### Símbolos terminais

```text
inteiro, real, texto, id, num_int, num_real,
mais, menos, multiplicacao, divisao, modulo,
atribuicao, ponto_virgula, abre_parenteses, fecha_parenteses, $
```

O símbolo `$` representa o fim da entrada e é acrescentado pelo programa principal após a tokenização.

### Produções

| # | Produção |
|---|----------|
| 0 | P -> L |
| 1 | L -> C L |
| 2 | L -> ε |
| 3 | C -> inteiro id ponto_virgula |
| 4 | C -> real id ponto_virgula |
| 5 | C -> texto id ponto_virgula |
| 6 | C -> id atribuicao E ponto_virgula |
| 7 | E -> T E1 |
| 8 | E1 -> mais T E1 |
| 9 | E1 -> menos T E1 |
| 10 | E1 -> ε |
| 11 | T -> F T1 |
| 12 | T1 -> multiplicacao F T1 |
| 13 | T1 -> divisao F T1 |
| 14 | T1 -> modulo F T1 |
| 15 | T1 -> ε |
| 16 | F -> abre_parenteses E fecha_parenteses |
| 17 | F -> id |
| 18 | F -> num_int |
| 19 | F -> num_real |

### Uso de ε

A produção vazia está presente em:

- `L -> ε`, permitindo programa vazio ou fim da lista de comandos;
- `E1 -> ε`, finalizando expressões aditivas;
- `T1 -> ε`, finalizando expressões multiplicativas.

---

## 4. Tabela LL(1)

A tabela LL(1) é organizada como uma matriz de não-terminal por terminal. Cada célula contém o número da produção aplicada pelo parser.

| NT | int | real | txt | id | ni | nr | + | - | * | / | % | = | ; | ( | ) | $ |
|----|-----|------|-----|----|----|----|---|---|---|---|---|---|---|---|---|---|
| P  | 0   | 0    | 0   | 0  |    |    |   |   |   |   |   |   |   |   |   | 0 |
| L  | 1   | 1    | 1   | 1  |    |    |   |   |   |   |   |   |   |   |   | 2 |
| C  | 3   | 4    | 5   | 6  |    |    |   |   |   |   |   |   |   |   |   |   |
| E  |     |      |     | 7  | 7  | 7  |   |   |   |   |   |   |   | 7 |   |   |
| E1 |     |      |     |    |    |    | 8 | 9 |   |   |   |   | 10|   | 10|   |
| T  |     |      |     | 11 | 11 | 11 |   |   |   |   |   |   |   | 11|   |   |
| T1 |     |      |     |    |    |    | 15| 15| 12| 13| 14|   | 15|   | 15|   |
| F  |     |      |     | 17 | 18 | 19 |   |   |   |   |   |   |   | 16|   |   |

Legenda:

- `int` = `inteiro`
- `txt` = `texto`
- `ni` = `num_int`
- `nr` = `num_real`
- `+` = `mais`
- `-` = `menos`
- `*` = `multiplicacao`
- `/` = `divisao`
- `%` = `modulo`
- `=` = `atribuicao`
- `;` = `ponto_virgula`
- `(` = `abre_parenteses`
- `)` = `fecha_parenteses`

Quando a célula correspondente ao par `(não-terminal, token_atual)` está vazia, não existe produção aplicável, e o parser deve interromper a análise com `ErroSintatico`.

---

## 5. Funcionamento do lexer

O lexer (`Analisador-Lexico/src/lexer_lpn.py`) utiliza expressões regulares combinadas em uma regex master para tokenizar o código-fonte. O método `tokenizar(codigo_fonte)` percorre a entrada com `re.finditer()`, identifica cada token pelo grupo nomeado da expressão regular e retorna uma lista de tuplas.

### Representação de token

```python
(tipo, valor, linha, coluna)
```

Atributos:

- `tipo`: nome do token produzido pelo lexer, como `INTEIRO`, `ID` ou `MAIS`;
- `valor`: lexema original encontrado no código-fonte;
- `linha`: linha do token, indexada a partir de 1;
- `coluna`: coluna do token, indexada a partir de 1.

### Tokens reconhecidos pelo lexer

Palavras-chave:

```text
INTEIRO, REAL, TEXTO, SE, SENAO, ENQUANTO, PARA, FUNCAO,
PROCEDIMENTO, RETORNE, ESCOLHA, CASO, PADRAO, PARE, CONTINUE
```

Literais e identificadores:

```text
NUM_INT, NUM_REAL, STRING, ID
```

Operadores aritméticos:

```text
MAIS, MENOS, MULT, DIV, MOD
```

Operadores lógicos:

```text
E_LOGICO, OU_LOGICO, NEGACAO
```

Operadores de comparação e atribuição:

```text
MAIOR_IGUAL, MENOR_IGUAL, IGUAL, DIFERENTE, MAIOR, MENOR, ATRIBUICAO
```

Delimitadores:

```text
PONTO_VIRGULA, VIRGULA, DOIS_PONTOS, ABRE_PAREN, FECHA_PAREN,
ABRE_CHAVE, FECHA_CHAVE
```

Tokens especiais:

```text
COMENTARIO_BLOCO, COMENTARIO_LINHA, ESPACO, INVALIDO
```

`COMENTARIO_BLOCO`, `COMENTARIO_LINHA` e `ESPACO` são reconhecidos pelo lexer, mas não são enviados ao parser. O token `INVALIDO` gera `ErroLexico`.

### Funções públicas do lexer utilizadas

- `AnalisadorLexicoLPN.tokenizar(codigo_fonte)` retorna a lista de tokens no formato `(tipo, valor, linha, coluna)`.
- `carregar_codigo_fonte()` retorna o caminho do arquivo de entrada e o conteúdo textual a ser analisado.

### Erros léxicos

A classe `ErroLexico` é levantada quando ocorre uma das seguintes situações:

- símbolo inválido encontrado na entrada;
- comentário de bloco não encerrado.

---

## 6. Relação entre lexer e parser

O reconhecimento léxico não implica reconhecimento sintático. Executar apenas o lexer verifica se o texto pode ser dividido em tokens, mas não verifica se a sequência de tokens é derivável pela gramática LL(1).

A validação sintática deve ser feita com o parser, por meio de `main.py` ou da suíte `tests/test_parser.py`.

O parser utiliza o dicionário `MAPA_TOKEN_LEXER_PARA_GRAMATICA`, definido em `src/parser.py`, para converter tokens do lexer em terminais da gramática.

| Token lexer | Terminal da gramática |
|-------------|------------------------|
| INTEIRO | inteiro |
| REAL | real |
| TEXTO | texto |
| ID | id |
| NUM_INT | num_int |
| NUM_REAL | num_real |
| MAIS | mais |
| MENOS | menos |
| MULT | multiplicacao |
| DIV | divisao |
| MOD | modulo |
| ATRIBUICAO | atribuicao |
| PONTO_VIRGULA | ponto_virgula |
| ABRE_PAREN | abre_parenteses |
| FECHA_PAREN | fecha_parenteses |

Tokens reconhecidos pelo lexer, mas não mapeados para terminais da gramática, não pertencem ao subconjunto sintático LL(1) implementado.

### Tokens fora do escopo sintático

| Token | Categoria |
|-------|-----------|
| SE, SENAO, ENQUANTO, PARA, FUNCAO, PROCEDIMENTO, RETORNE, ESCOLHA, CASO, PADRAO, PARE, CONTINUE | Palavras-chave |
| STRING | Literal |
| E_LOGICO, OU_LOGICO, NEGACAO | Operadores lógicos |
| MAIOR_IGUAL, MENOR_IGUAL, IGUAL, DIFERENTE, MAIOR, MENOR | Operadores de comparação |
| VIRGULA, DOIS_PONTOS, ABRE_CHAVE, FECHA_CHAVE | Delimitadores |

Esses tokens podem ser reconhecidos lexicalmente, mas provocam `ErroSintatico` quando aparecem em uma posição analisada pelo parser, pois não possuem entrada correspondente na tabela LL(1).

### Diferença entre reconhecimento léxico e sintático

| Código | Lexer | Parser |
|--------|-------|--------|
| `inteiro x;` | ✓ | ✓ |
| `x = 10 + 5;` | ✓ | ✓ |
| `se (x > 0)` | ✓ | ✗ |
| `x = 3 && y;` | ✓ | ✗ |
| `inteiro ;` | ✓ | ✗ |

---

## 7. Funcionamento do parser

O parser implementa um analisador preditivo recursivo com consulta explícita à tabela LL(1). A decisão de qual produção aplicar é tomada a partir do par formado pelo não-terminal em expansão e pelo token atual.

Fluxo geral:

1. `main.py` carrega o código-fonte.
2. `AnalisadorLexicoLPN.tokenizar()` produz a lista de tokens.
3. `main.py` acrescenta o token de fim de entrada `("$", "$", linha, coluna)`.
4. `Parser.parse()` inicia a análise pelo símbolo inicial `P`.
5. Cada método sintático consulta `TABELA_LL`.
6. Os tokens são consumidos quando correspondem ao terminal esperado.
7. A AST é construída durante o parsing.
8. Ao final, o parser exige que o token atual seja `$`.

Se um token não puder ser convertido em terminal gramatical, ou se não existir produção na tabela LL(1) para o par consultado, a análise é interrompida com `ErroSintatico`.

### Critério formal de aceitação

Uma entrada é aceita pelo analisador sintático se, e somente se:

- a tokenização termina sem `ErroLexico`;
- todos os tokens produzidos pelo lexer pertencem a uma sequência derivável pela gramática LL(1);
- cada expansão de não-terminal encontra uma produção definida em `TABELA_LL`;
- todos os terminais esperados são consumidos na ordem prevista pelas produções;
- após o consumo da cadeia, o token atual é `$`.

Caso qualquer uma dessas condições falhe, a entrada não é aceita pelo parser.

---

## 8. AST

A AST é construída simultaneamente à análise sintática. Ela representa apenas os elementos estruturais relevantes do subconjunto aceito pela gramática.

| Nó | Produção de origem | Atributos |
|----|--------------------|-----------|
| Programa | P -> L | tipo, comandos |
| Declaracao | C -> inteiro/real/texto id ponto_virgula | tipo_no, tipo_variavel, nome, linha, coluna |
| Atribuicao | C -> id atribuicao E ponto_virgula | tipo_no, nome, expressao, linha, coluna |
| ExpressaoBinaria | E1/T1 com operador | tipo_no, operador, esquerda, direita, linha, coluna |
| Identificador | F -> id | tipo_no, nome, linha, coluna |
| Numero | F -> num_int/num_real | tipo_no, valor, tipo_valor, linha, coluna |

Os não-terminais `L`, `E`, `E1`, `T`, `T1` e `F` são mecanismos sintáticos utilizados para derivação e precedência, mas não aparecem diretamente como nós finais da AST. Parênteses em `F -> abre_parenteses E fecha_parenteses` também são eliminados da AST, mantendo apenas a expressão interna.

### JSON gerado

Quando a análise é concluída com sucesso, a AST é serializada em `ast.json`.

Exemplo simplificado:

```json
{
  "tipo": "Programa",
  "comandos": [
    {
      "tipo": "Declaracao",
      "tipo_variavel": "inteiro",
      "nome": "x"
    },
    {
      "tipo": "Atribuicao",
      "nome": "x",
      "expressao": {
        "tipo": "Numero",
        "valor": 10,
        "tipo_valor": "num_int"
      }
    }
  ]
}
```

---

## 9. Tratamento de erros

O projeto possui dois tipos principais de erro:

- `ErroLexico`: ocorre durante a tokenização, antes da análise sintática;
- `ErroSintatico`: ocorre durante a análise LL(1), quando a cadeia de tokens não pode ser derivada pela gramática.

As mensagens de erro incluem linha e coluna. Em erros sintáticos, a mensagem também indica o token encontrado, o tipo do token, os terminais esperados ou o não-terminal em expansão, conforme o ponto de falha.

A tabela LL(1) não possui mecanismo de recuperação de erros. Assim, ao encontrar o primeiro erro léxico ou sintático, a análise é interrompida.

---

## 10. Etapas de derivação

Exemplo para a entrada:

```lpn
x = 10;
```

Tokens relevantes:

```text
ID("x"), ATRIBUICAO("="), NUM_INT("10"), PONTO_VIRGULA(";"), $
```

Passos principais:

```text
1. P -> L
2. L -> C L
3. C -> id atribuicao E ponto_virgula
4. consumir ID("x")
5. consumir ATRIBUICAO("=")
6. E -> T E1
7. T -> F T1
8. F -> num_int
9. consumir NUM_INT("10")
10. T1 -> ε
11. E1 -> ε
12. consumir PONTO_VIRGULA(";")
13. L -> ε
14. consumir/verificar $
```

AST resultante, de forma simplificada:

```text
Programa([
  Atribuicao("x", Numero(10))
])
```

---

## 11. Instruções de execução

Os comandos devem ser executados a partir da raiz do projeto.

### Análise completa

```bash
python main.py arquivo.lpn
```

Se nenhum caminho for informado, o programa usa o arquivo padrão definido pelo carregador do lexer:

```text
Analisador-Lexico/entrada/codigo_exemplo.lpn
```

Exemplo com entrada válida:

```bash
python main.py exemplos/entrada_valida.lpn
```

Exemplo com entrada inválida:

```bash
python main.py exemplos/exemplos_invalidos/ponto_virgula_ausente.lpn
```

A execução de `main.py` realiza:

1. leitura do arquivo de entrada;
2. tokenização pelo lexer;
3. acréscimo do símbolo `$`;
4. análise sintática pelo parser LL(1);
5. construção da AST;
6. serialização da AST em `ast.json`, quando não há erro.

### Execução isolada do lexer

```bash
python Analisador-Lexico/src/lexer_lpn.py arquivo.lpn
```

Esse comando verifica somente a tokenização. Ele não constitui um teste completo do parser e não garante que a sequência formada pertença à gramática LL(1). Para validar sintaticamente uma entrada, deve-se executar `main.py` ou `tests/test_parser.py`.

---

## 12. Forma correta de testar o analisador sintático

Para testar o analisador sintático corretamente, os arquivos `.lpn` devem conter apenas cadeias pertencentes ao subconjunto definido pela gramática LL(1). Esse subconjunto é composto por:

- declarações simples;
- atribuições;
- expressões aritméticas;
- identificadores;
- números inteiros;
- números reais;
- parênteses;
- operadores `+`, `-`, `*`, `/` e `%`.

### Declarações válidas

```lpn
inteiro x;
real y;
texto nome;
```

### Atribuições válidas

```lpn
x = 10;
y = x + 3.5 * 2;
resultado = (x + y) % 2;
```

### Entrada válida completa

```lpn
inteiro x;
real y;
texto mensagem;
inteiro resultado;

x = 10;
y = 3.14;
resultado = x + y * 2;
resultado = (x + y) * 2;
```

### Comportamento esperado para entradas válidas

Uma entrada válida deve produzir:

- consumo de todos os tokens da entrada;
- ausência de exceções;
- mensagem de conclusão da análise sintática;
- AST construída em memória;
- geração ou atualização do arquivo `ast.json`.

### Comportamento esperado para entradas inválidas

Uma entrada inválida deve produzir:

- interrupção da análise;
- lançamento de `ErroLexico` ou `ErroSintatico`;
- indicação de linha e coluna;
- indicação do token ou trecho responsável pelo erro, quando aplicável.

---

## 13. Testes automatizados

A suíte de testes deve ser executada a partir da raiz do projeto:

```bash
python tests/test_parser.py
```

O objetivo dos testes automatizados é verificar se o parser aceita as cadeias deriváveis pela gramática LL(1) e rejeita entradas que não possuem derivação válida na tabela de análise. Os testes também documentam o comportamento esperado em casos de erro.

Ao executar a suíte, cada caso imprime `[OK]` quando o resultado obtido corresponde ao resultado esperado.

### Casos cobertos pela suíte

Casos válidos:

- programa vazio;
- declarações com `inteiro`, `real` e `texto`;
- atribuições;
- números inteiros;
- números reais;
- parênteses;
- precedência dos operadores;
- operador de módulo;
- expressões com operadores combinados;
- múltiplos comandos.

Casos inválidos:

- ausência de ponto e vírgula;
- identificador ausente;
- expressão incompleta;
- parênteses não fechados;
- parênteses sem abertura correspondente;
- operador sem operando;
- fim inesperado de arquivo;
- sequências de tokens sem produção correspondente na tabela LL(1).

---

## 14. Exemplos

### Exemplos válidos

Declaração:

```lpn
inteiro x;
```

Atribuição simples:

```lpn
x = 10;
```

Expressão com precedência:

```lpn
resultado = a + b * c;
```

Expressão com parênteses:

```lpn
resultado = (a + b) * c;
```

Programa com múltiplos comandos:

```lpn
inteiro x;
real y;
x = 10;
y = x + 1;
```

### Exemplos inválidos

Ausência de ponto e vírgula:

```lpn
inteiro x
```

Erro esperado:

```text
Esperado 'ponto_virgula', encontrado '$'
```

Identificador ausente em declaração:

```lpn
inteiro ;
```

Expressão incompleta:

```lpn
x = a + ;
```

Token reconhecido pelo lexer, mas sem produção na tabela LL(1):

```lpn
se (x > 0)
```

Operador lógico fora do subconjunto sintático:

```lpn
x = 3 && y;
```

---

## 15. Decisões de implementação

### Integração entre lexer e parser

O lexer foi mantido como componente separado e fornece ao parser uma lista de tuplas no formato `(tipo, valor, linha, coluna)`. A inclusão de linha e coluna permite que o parser produza mensagens de erro mais informativas.

### Mapeamento de tokens

O parser não consome diretamente todos os tokens do lexer. Antes de consultar a tabela LL(1), ele converte o tipo léxico para o terminal gramatical correspondente por meio de `MAPA_TOKEN_LEXER_PARA_GRAMATICA`.

### Construção da AST

A construção da AST ocorre durante o parsing. As produções da gramática orientam a criação dos nós `Programa`, `Declaracao`, `Atribuicao`, `ExpressaoBinaria`, `Identificador` e `Numero`.

### Adaptação dos tokens

O lexer fornece tokens no formato `(tipo, valor, linha, coluna)`. A inclusão de linha e coluna permite que o parser emita mensagens de erro associadas à posição do token. O arquivo `html_saida.py` mantém compatibilidade por meio de desempacotamento flexível dos tokens.

### Critério de referência para inconsistências

Quando houver divergência entre o conjunto de tokens reconhecido pelo lexer e o subconjunto aceito pelo parser, a referência para aceitação sintática é a seguinte:

1. tabela LL(1);
2. gramática documentada;
3. comportamento do lexer.

### Ausência de análise semântica

O projeto não verifica declaração prévia de variáveis, compatibilidade de tipos, existência de identificadores, escopo ou valor das expressões. Entradas como atribuições a identificadores não declarados podem ser sintaticamente válidas se pertencerem à gramática LL(1).

---

## 16. Resumo do critério de validade

Uma entrada é aceita quando:

```text
lexer reconhece os lexemas
AND
parser consegue derivar toda a sequência pela tabela LL(1)
AND
o token final é $
```

Uma entrada é rejeitada quando:

```text
há erro léxico
OR
há token fora do subconjunto sintático
OR
não existe produção aplicável na tabela LL(1)
OR
há tokens restantes após o fim esperado do programa
```
