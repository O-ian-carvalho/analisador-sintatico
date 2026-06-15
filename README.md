# Analisador Sintático LL(1) — LPN

Implementação de um analisador sintático LL(1) preditivo dirigido por tabela para um subconjunto da linguagem LPN (Linguagem Procedural Nobre), com construção de Árvore Sintática Abstrata (AST) e serialização para JSON.

---

## 1. Gramática LL(1)

### Símbolo inicial

`P` (Programa)

### Símbolos não-terminais

P, L, C, E, E1, T, T1, F

### Símbolos terminais (19)

inteiro, real, texto, id, num_int, num_real, mais, menos, multiplicacao, divisao, modulo, atribuicao, ponto_virgula, abre_parenteses, fecha_parenteses, $

### ε (epsilon)

Presente em L (L → ε), E1 (E1 → ε) e T1 (T1 → ε).

### Fim de arquivo

`$`

### Produções

| # | Produção |
|---|----------|
| 0 | P → L |
| 1 | L → C L |
| 2 | L → ε |
| 3 | C → inteiro id ponto_virgula |
| 4 | C → real id ponto_virgula |
| 5 | C → texto id ponto_virgula |
| 6 | C → id atribuicao E ponto_virgula |
| 7 | E → T E1 |
| 8 | E1 → mais T E1 |
| 9 | E1 → menos T E1 |
| 10 | E1 → ε |
| 11 | T → F T1 |
| 12 | T1 → multiplicacao F T1 |
| 13 | T1 → divisao F T1 |
| 14 | T1 → modulo F T1 |
| 15 | T1 → ε |
| 16 | F → abre_parenteses E fecha_parenteses |
| 17 | F → id |
| 18 | F → num_int |
| 19 | F → num_real |

---

## 2. Tabela LL(1)

Organizada como matriz (não-terminal × terminal). Cada célula contém o número da produção a ser aplicada.

| NT | int | real | txt | id | ni | nr | + | - | * | / | % | = | ; | ( | ) | $ |
|----|-----|------|-----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| P  | 0   | 0    | 0   | 0  |    |    |    |    |    |    |    |    |    |    |    | 0 |
| L  | 1   | 1    | 1   | 1  |    |    |    |    |    |    |    |    |    |    |    | 2 |
| C  | 3   | 4    | 5   | 6  |    |    |    |    |    |    |    |    |    |    |    |   |
| E  |     |      |     | 7  | 7  | 7  |    |    |    |    |    |    |    | 7 |    |   |
| E1 |     |      |     |    |    |    | 8  | 9  |    |    |    |    | 10 |    | 10 |   |
| T  |     |      |     | 11 | 11 | 11 |    |    |    |    |    |    |    | 11 |    |   |
| T1 |     |      |     |    |    |    | 15 | 15 | 12 | 13 | 14 |    | 15 |    | 15 |   |
| F  |     |      |     | 17 | 18 | 19 |    |    |    |    |    |    |    | 16 |    |   |

Legenda: int=inteiro, ni=num_int, nr=num_real, txt=texto

---

## 3. Funcionamento do Lexer

O lexer (`Analisador-Lexico/src/lexer_lpn.py`) utiliza expressões regulares combinadas em uma regex master para tokenizar o código-fonte.

### Como os tokens são produzidos

O método `tokenizar(codigo_fonte)` percorre o código com `re.finditer()`, identificando cada token por grupo nomeado na regex.

### Tipos de tokens existentes (41 tipos)

Palavras-chave: INTEIRO, REAL, TEXTO, SE, SENAO, ENQUANTO, PARA, FUNCAO, PROCEDIMENTO, RETORNE, ESCOLHA, CASO, PADRAO, PARE, CONTINUE

Literais: NUM_INT, NUM_REAL, STRING, ID

Operadores aritméticos: MAIS, MENOS, MULT, DIV, MOD

Operadores lógicos: E_LOGICO, OU_LOGICO, NEGACAO

Operadores de comparação: MAIOR_IGUAL, MENOR_IGUAL, IGUAL, DIFERENTE, MAIOR, MENOR, ATRIBUICAO

Delimitadores: PONTO_VIRGULA, VIRGULA, DOIS_PONTOS, ABRE_PAREN, FECHA_PAREN, ABRE_CHAVE, FECHA_CHAVE

Especiais: COMENTARIO_BLOCO, COMENTARIO_LINHA, ESPACO, INVALIDO

### Classe que representa um token

Tupla `(tipo: str, valor: str, linha: int, coluna: int)`.

### Atributos de cada token

- `tipo`: string com o nome do token (ex: "INTEIRO", "ID", "MAIS")
- `valor`: lexema correspondente no código fonte (ex: "x", "10", "+")
- `linha`: número da linha (1-indexed)
- `coluna`: número da coluna (1-indexed)

### Tratamento de erros léxicos

A classe `ErroLexico` é levantada quando um caractere inválido é encontrado ou um comentário de bloco não é fechado.

### Fim da entrada

Representado pelo token `("$", "$", linha, coluna)` adicionado pelo parser ao final da lista de tokens.

### Funções públicas do lexer utilizadas pelo parser

- `AnalisadorLexicoLPN.tokenizar(codigo_fonte)` → `list[tuple]`
- `carregar_codigo_fonte()` → `(Path, str)`

---

## 4. Tokens suportados pelo parser

O parser implementa **apenas** o subconjunto LL(1) definido pela gramática. Os tokens a seguir são aceitos:

| Token lexer | Terminal gramática |
|-------------|-------------------|
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

---

## 5. Divergências encontradas

### Tokens do lexer fora do escopo sintático

Os seguintes tokens são reconhecidos pelo lexer mas **não** pertencem ao subconjunto LL(1) e disparam erro sintático:

| Token | Categoria |
|-------|-----------|
| SE, SENAO, ENQUANTO, PARA, FUNCAO, PROCEDIMENTO, RETORNE, ESCOLHA, CASO, PADRAO, PARE, CONTINUE | Palavras-chave |
| STRING | Literal |
| E_LOGICO, OU_LOGICO, NEGACAO | Operadores lógicos |
| MAIOR_IGUAL, MENOR_IGUAL, IGUAL, DIFERENTE, MAIOR, MENOR | Operadores de comparação |
| VIRGULA, DOIS_PONTOS, ABRE_CHAVE, FECHA_CHAVE | Delimitadores |

### Prioridade de resolução de conflitos

1. Tabela LL(1)
2. Gramática (documentação gramática.txt)
3. Comportamento do lexer

---

## 6. Nós da AST

| Nó | Produção origem | Atributos |
|----|----------------|-----------|
| Programa | P → L | tipo, comandos |
| Declaracao | C → inteiro/real/texto id ; | tipo_no, tipo_variavel, nome, linha, coluna |
| Atribuicao | C → id = E ; | tipo_no, nome, expressao, linha, coluna |
| ExpressaoBinaria | E1/T1 com operador | tipo_no, operador, esquerda, direita, linha, coluna |
| Identificador | F → id | tipo_no, nome, linha, coluna |
| Numero | F → num_int/num_real | tipo_no, valor, tipo_valor, linha, coluna |

### Nós sintáticos eliminados

L, E, E1, T, T1, F — são mecanismos gramaticais absorvidos durante a construção da AST. Parênteses em F → ( E ) também são eliminados.

---

## 7. Justificativas das decisões

### Modificação do lexer

**Alteração**: token passou de `(tipo, valor)` para `(tipo, valor, linha, coluna)`.

**Motivo técnico**: o parser necessita de linha e coluna para mensagens de erro (exigência do escopo). As variáveis já eram computadas internamente no lexer (linhas 91-92) e descartadas (linha 104).

**Impactos**: `html_saida.py` ajustado para desempacotamento flexível (`for tipo, valor, *_ in tokens`). API pública `tokenizar()` inalterada.

### Algoritmo de parsing

Parser preditivo recursivo com consulta explícita à tabela LL(1). Cada método consulta `self.tabela[non_terminal][token_atual]` para decidir a produção. A construção da AST é simultânea ao parsing, eliminando nós sintáticos intermediários.

### Tratamento de erros

Interrupção controlada (a tabela LL(1) não possui mecanismos de recuperação de erro). Mensagens incluem token, lexema, esperado, não-terminal, linha e coluna.

---

## 8. Etapas do parser (derivação)

Exemplo para entrada `x = 10;`:

```
Tokens: [ID("x"), ATRIBUICAO("="), NUM_INT("10"), PONTO_VIRGULA(";"), $]

Passos do parser:
1. P -> L                        [expandir P]
2. L -> C L                      [expandir L com ID]
3. C -> id = E ;                  [expandir C com ID]
4. consumir(ID "x")              [casa terminal id]
5. consumir(ATRIBUICAO "=")      [casa terminal =]
6. E -> T E1                      [expandir E]
7. T -> F T1                      [expandir T]
8. F -> num_int                   [expandir F com NUM_INT]
9. consumir(NUM_INT "10")        [casa terminal num_int]
10. T1 -> ε                       [T1 vazio]
11. E1 -> ε                       [E1 vazio]
12. consumir(PONTO_VIRGULA ";")  [casa terminal ;]
13. L -> ε                        [fim da lista]

AST construida:
Atribuicao("x", Numero(10))
```

---

## 9. Instruções de execução

```bash
# Executar analise completa (lexer + parser + JSON)
python main.py <caminho_do_arquivo>
# Se omitido, usa: Analisador-Lexico/entrada/codigo_exemplo.lpn

# Exemplo com arquivo valido
python main.py exemplos/entrada_valida.lpn

# Exemplo com arquivo invalido
python main.py exemplos/exemplos_invalidos/ponto_virgula_ausente.lpn

# Executar apenas o lexer (funcionalidade original)
python Analisador-Lexico/src/lexer_lpn.py <caminho_do_arquivo>
```

## 10. Instruções de teste

```bash
python tests/test_parser.py
```

Os testes cobrem:
- **Casos válidos**: programa vazio, declarações (inteiro, real, texto), atribuições, expressões com todos os operadores, parênteses, programas completos
- **Casos inválidos**: tokens fora do subconjunto, ponto e vírgula ausente, identificador ausente, parênteses não fechados, expressões incompletas, EOF inesperado

---

## 11. Exemplos

### Válido: `exemplos/entrada_valida.lpn`

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

### Inválido: `exemplos/exemplos_invalidos/ponto_virgula_ausente.lpn`

```lpn
inteiro x
```
Erro: `Esperado 'ponto_virgula', encontrado '$' (linha 1, coluna 10)`

### JSON gerado: `exemplos/ast_exemplo.json`

```json
{
  "tipo": "Programa",
  "comandos": [
    { "tipo": "Declaracao", "tipo_variavel": "inteiro", "nome": "x" },
    { "tipo": "Atribuicao", "nome": "x", "expressao": { ... } }
  ]
}
```
