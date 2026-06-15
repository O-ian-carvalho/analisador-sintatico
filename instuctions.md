# Implementação do Analisador Sintático LL(1), AST e Geração de JSON em Python

Você é um desenvolvedor sênior especialista em compiladores, gramáticas formais, análise léxica e sintática, construção de AST e implementação em Python.

Sua tarefa é implementar a etapa de análise sintática de um compilador em Python com base EXCLUSIVAMENTE nos arquivos e diretórios fornecidos pelo projeto.

---

# Arquivos e diretórios que DEVEM ser analisados

Antes de iniciar qualquer implementação, analise completamente os seguintes recursos:

* `documentação gramática.txt`
* `tabela LL.md`
* Diretório do analisador léxico localizado em:

```
<INSIRA_AQUI_O_PATH_DO_ANALISADOR_LEXICO>
```

Esses recursos constituem a especificação oficial do projeto.

Não implemente nenhuma solução antes de analisar integralmente todos eles.

---

# Processo obrigatório antes da implementação

Antes de gerar qualquer código, faça uma análise detalhada dos arquivos.

Explique:

* quais produções foram encontradas na gramática;
* quais são os símbolos terminais;
* quais são os símbolos não-terminais;
* qual é o símbolo inicial;
* quais símbolos representam ε (epsilon), caso existam;
* quais símbolos representam fim de arquivo, caso existam;
* como a tabela LL(1) está organizada;
* como o analisador léxico gera os tokens;
* quais informações cada token possui;
* quais estruturas existentes devem ser reutilizadas.

Somente após concluir essa análise inicie a implementação.

---

# Análise obrigatória do analisador léxico

Analise todos os arquivos presentes no diretório do analisador léxico.

Identifique e documente:

* como os tokens são produzidos;
* quais tipos de tokens existem;
* qual classe representa um token;
* quais atributos cada token possui;
* se existem linha e coluna;
* como erros léxicos são tratados;
* como o fim da entrada é representado;
* quais funções públicas do lexer devem ser utilizadas pelo parser.

O parser deve integrar-se ao lexer reutilizando sua interface atual.

Não altere o comportamento do analisador léxico sem necessidade.

Caso alguma alteração seja inevitável, explique detalhadamente:

* a implementação original;
* a alteração proposta;
* o motivo técnico;
* os impactos gerados.

---

# Escopo do parser (REGRA OBRIGATÓRIA)

Implemente o analisador sintático EXCLUSIVAMENTE para o subconjunto da linguagem definido pela gramática LL(1) presente em:

* `documentação gramática.txt`
* `tabela LL.md`

O fato de o analisador léxico reconhecer determinados tokens NÃO significa que esses tokens façam parte do subconjunto sintático que deve ser implementado.

O parser NÃO deve inferir funcionalidades extras.

---

# Tokens adicionais reconhecidos pelo lexer

O analisador léxico pode reconhecer tokens adicionais devido a:

* evolução futura da linguagem;
* reutilização do lexer;
* funcionalidades experimentais;
* implementações incompletas.

Esses tokens NÃO devem ampliar automaticamente o escopo do parser.

Portanto:

* implemente apenas as produções explicitamente presentes na gramática;
* utilize apenas os terminais presentes na tabela LL;
* não deduza novas produções;
* não crie regras sintáticas para suportar tokens extras;
* não implemente funcionalidades ausentes da gramática.

---

# Divergência entre lexer e gramática

Caso o lexer reconheça tokens que não pertençam ao subconjunto LL(1):

* documente esses tokens;
* informe que eles ficaram fora do escopo sintático;
* trate sua ocorrência como erro sintático;
* não os incorpore à AST;
* não implemente suporte para eles.

Em caso de conflito entre:

1. comportamento do lexer;
2. gramática;
3. tabela LL(1);

a prioridade obrigatória é:

1. tabela LL(1);
2. gramática;
3. lexer.

Explique toda divergência encontrada.

---

# Implementação do parser

Implemente um analisador sintático LL(1) em Python.

O parser deverá:

* receber a sequência de tokens produzida pelo lexer;
* utilizar a tabela LL(1) fornecida;
* validar toda a entrada;
* consumir corretamente todos os tokens;
* aplicar as produções adequadas;
* utilizar o símbolo inicial correto;
* verificar o marcador de fim da entrada;
* detectar erros sintáticos;
* permitir manutenção futura.

Não utilize:

* expressões regulares para substituir a análise;
* parsing ad hoc;
* heurísticas não justificadas;
* parser recursivo que ignore a tabela LL.

A implementação deve efetivamente utilizar a tabela LL(1).

---

# Funcionamento esperado do parser

O parser deve realizar análise preditiva dirigida por tabela.

Exemplo conceitual:

* consultar o topo da pilha;
* comparar com o token atual;
* consumir terminais;
* expandir não-terminais conforme a tabela;
* reconhecer produções vazias;
* validar o fim da entrada.

A implementação deve refletir o algoritmo LL(1).

---

# Tratamento de erros sintáticos

Implemente mensagens claras e detalhadas.

Sempre que possível, informe:

* token encontrado;
* lexema encontrado;
* token esperado;
* não-terminal sendo processado;
* linha;
* coluna;
* contexto do erro.

Exemplo:

"Erro sintático na linha 12, coluna 8. Encontrado ';', esperado IDENTIFIER durante a expansão de Declaracao."

Caso existam mecanismos de recuperação de erro na tabela LL, implemente-os.

Caso não existam, realize interrupção controlada da análise.

---

# Construção da AST

Durante a análise sintática, construa uma Árvore Sintática Abstrata (AST).

A AST deve representar a estrutura lógica do programa.

Evite construir uma árvore sintática concreta desnecessariamente detalhada.

Remova elementos puramente sintáticos quando apropriado.

---

# Requisitos da AST

Cada nó deve possuir, quando aplicável:

* tipo do nó;
* valor associado;
* filhos;
* linha;
* coluna;
* demais metadados úteis.

Utilize classes Python apropriadas.

Empregue boas práticas de orientação a objetos.

A AST deve representar SOMENTE construções pertencentes ao subconjunto LL(1).

Não crie nós para funcionalidades não definidas na gramática.

---

# Serialização da AST

Implemente a conversão completa da AST para JSON.

A serialização deve:

* preservar toda a hierarquia da árvore;
* converter objetos para estruturas serializáveis;
* utilizar indentação adequada;
* gerar JSON legível.

---

# Geração automática do arquivo JSON

Após uma análise bem-sucedida:

gere automaticamente um arquivo:

```text
ast.json
```

contendo a AST completa.

A geração do JSON deve ocorrer ao final do processamento do programa.

O usuário não deve precisar montar manualmente o JSON.

---

# Estrutura sugerida

Caso o projeto não possua organização definida, utilize:

```text
parser.py
ast_nodes.py
ast_serializer.py
exceptions.py
main.py
```

Caso já exista uma estrutura no projeto:

* adapte-se a ela;
* reutilize arquivos existentes;
* evite reorganizações desnecessárias.

---

# Integração com o projeto existente

Reutilize ao máximo:

* classes existentes;
* modelos de tokens;
* exceções;
* padrões adotados;
* convenções de nomenclatura.

Não reescreva componentes já funcionais sem justificativa técnica.

---

# Testes obrigatórios

Implemente testes cobrindo:

## Casos válidos

* programa mínimo;
* declarações simples;
* comandos isolados;
* programas completos;
* combinações das principais produções.

## Casos inválidos

* token inesperado;
* ausência de símbolos obrigatórios;
* produções inválidas;
* fechamento incorreto;
* fim inesperado do arquivo;
* uso de tokens fora do subconjunto LL(1).

Explique o comportamento esperado de cada teste.

---

# Exemplos

Forneça exemplos completos contendo:

* código-fonte de entrada;
* sequência de tokens produzida pelo lexer;
* etapas relevantes do parser;
* AST construída;
* conteúdo do JSON gerado.

---

# Entregáveis obrigatórios

Forneça:

1. resumo da gramática identificada;
2. resumo da tabela LL(1);
3. resumo do funcionamento do lexer;
4. lista dos tokens reconhecidos;
5. lista dos tokens efetivamente suportados pelo parser;
6. divergências encontradas;
7. justificativas adotadas;
8. implementação completa do parser;
9. implementação completa da AST;
10. implementação completa da serialização;
11. geração automática do arquivo `ast.json`;
12. código Python funcional;
13. instruções de execução;
14. instruções de teste;
15. exemplos válidos;
16. exemplos inválidos;
17. exemplos do JSON produzido.

---

# Restrições obrigatórias

* Não invente regras da linguagem.
* Não faça suposições sem justificativa.
* Não ignore produções da gramática.
* Não ignore a tabela LL(1).
* Não implemente funcionalidades fora do subconjunto especificado.
* Não trate tokens extras do lexer como válidos automaticamente.
* Não gere apenas pseudocódigo.
* Não entregue implementações parciais.
* Não substitua o algoritmo LL(1) por outra abordagem.
* Não modifique o lexer sem necessidade.
* Caso alguma informação esteja ausente ou inconsistente, interrompa a implementação e descreva explicitamente o problema antes de prosseguir.

Somente após concluir toda a análise dos arquivos fornecidos, implemente a solução completa em Python.
