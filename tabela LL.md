## GRAMÁTICA UTILIZADA

- P -> L
- L -> C L
- L -> ε
- C -> inteiro id ponto_virgula
- C -> real id ponto_virgula
- C -> texto id ponto_virgula
- C -> id atribuicao E ponto_virgula
- E -> T E1
- E1 -> mais T E1
- E1 -> menos T E1
- E1 -> ε
- T -> F T1
- T1 -> multiplicacao F T1
- T1 -> divisao F T1
- T1 -> modulo F T1
- T1 -> ε
- F -> abre_parenteses E fecha_parenteses
- F -> id
- F -> num_int
- F -> num_real

## CONJUNTO FIRST

- FIRST(P) = { inteiro, real, texto, id, ε }
- FIRST(L) = { inteiro, real, texto, id, ε }
- FIRST(C) = { inteiro, real, texto, id }
- FIRST(E) = { abre_parenteses, id, num_int, num_real }
- FIRST(E1) = { mais, menos, ε }
- FIRST(T) = { abre_parenteses, id, num_int, num_real }
- FIRST(T1) = { multiplicacao, divisao, modulo, ε }
- FIRST(F) = { abre_parenteses, id, num_int, num_real }

## CONJUNTO FOLLOW

- FOLLOW(P) = { \$ }
- FOLLOW(L) = { \$ }
- FOLLOW(C) = { inteiro, real, texto, id, \$ }
- FOLLOW(E) = { ponto_virgula, fecha_parenteses }
- FOLLOW(E1) = { ponto_virgula, fecha_parenteses }
- FOLLOW(T) = { mais, menos, ponto_virgula, fecha_parenteses }
- FOLLOW(T1) = { mais, menos, ponto_virgula, fecha_parenteses }
- FOLLOW(F) = { multiplicacao, divisao, modulo,mais, menos, ponto_virgula,fecha_parenteses }

## REGRA DE CONSTRUÇÃO DA TABELA LL(1)

Para cada produção A → α:

• Para cada terminal a ∈ FIRST(α), adicione A→α em M\[A, a\]

• Se ε ∈ FIRST(α), para cada b ∈ FOLLOW(A), adicione A→α

em M\[A, b\]

Aplicando a regra à gramática:

P → L

• FIRST(L) = { inteiro, real, texto, id, ε }

M\[P, inteiro\] = P → L

M\[P, real\] = P → L

M\[P, texto\] = P → L

M\[P, id\] = P → L

M\[P, \$\] = P → L

L → C L

• FIRST(C L) = { inteiro, real, texto, id }

M\[L, inteiro\] = L → C L

M\[L, real\] = L → C L

M\[L, texto\] = L → C L

M\[L, id\] = L → C L

L → ε

• FOLLOW(L) = { \$ }

M\[L, \$\] = L → ε

C → inteiro id ponto_virgula

M\[C, inteiro\] = C → inteiro id ponto_virgula

C → real id ponto_virgula

M\[C, real\] = C → real id ponto_virgula

C → texto id ponto_virgula

M\[C, texto\] = C → texto id ponto_virgula

C → id atribuicao E ponto_virgula

M\[C, id\] = C → id atribuicao E ponto_virgula

E → T E1

• FIRST(T E1) = { abre_parenteses, id, num_int, num_real }

M\[E, abre_parenteses\] = E → T E1

M\[E, id\] = E → T E1

M\[E, num_int\] = E → T E1

M\[E, num_real\] = E → T E1

E1 → mais T E1

\[E1, mais\] = E1 → mais T E1

E1 → menos T E1

M\[E1, menos\] = E1 → menos T E1

E1 → ε

• FOLLOW(E1) = { ponto_virgula, fecha_parenteses }

M\[E1, ponto_virgula\] = E1 → ε

M\[E1, fecha_parenteses\] = E1 → ε

T → F T1

• FIRST(F T1) = { abre_parenteses, id, num_int, num_real }

M\[T, abre_parenteses\] = T → F T1

M\[T, id\] = T → F T1

M\[T, num_int\] = T → F T1

M\[T, num_real\] = T → F T1

T1 → multiplicacao F T1

M\[T1, multiplicacao\] = T1 → multiplicacao F T1

T1 → divisao F T1

M\[T1, divisao\] = T1 → divisao F T1

T1 → modulo F T1

M\[T1, modulo\] = T1 → modulo F T1

T1 → ε

• FOLLOW(T1) = { mais, menos, ponto_virgula, fecha_parenteses }

M\[T1, mais\] = T1 → ε

M\[T1, menos\] = T1 → ε

M\[T1, ponto_virgula\] = T1 → ε

M\[T1, fecha_parenteses\] = T1 → ε

F → abre_parenteses E fecha_parenteses

M\[F, abre_parenteses\] =

F → abre_parenteses E fecha_parentese

F → id

M\[F, id\] = F → id

F → num_int

M\[F, num_int\] = F → num_int

F → num_real

M\[F, num_real\] = F → num_real

## TABELA LL(1)

**Abreviações dos terminais:**

- int=inteiro real=real txt=texto id=id
- ni=num_int nr=num_real
- +=mais -=menos \*=(mult) /=(div) %=(mod)
- \==(attr)
- ;=(pv)
- (=(ap) )=(fp)
- \$=\$

| **NT** | **int** | **real** | **txt** | **id** | **ni** | **nr** | **+** | **\-** | **\*** | **/** | **%** | **\=** | **;** | **(** | **)** | **\$** |
| ------ | ------- | -------- | ------- | ------ | ------ | ------ | ----- | ------ | ------ | ----- | ----- | ------ | ----- | ----- | ----- | ------ |
| **P**  | 0       | 0        | 0       | 0      |        |        |       |        |        |       |       |        |       |       |       | 0      |
| **L**  | 1       | 1        | 1       | 1      |        |        |       |        |        |       |       |        |       |       |       | 2      |
| **C**  | 3       | 4        | 5       | 6      |        |        |       |        |        |       |       |        |       |       |       |        |
| **E**  |         |          |         | 7      | 7      | 7      |       |        |        |       |       |        |       | 7     |       |        |
| **E1** |         |          |         |        |        |        | 8     | 9      |        |       |       |        | 10    |       | 10    |        |
| **T**  |         |          |         | 11     | 11     | 11     |       |        |        |       |       |        |       | 11    |       |        |
| **T1** |         |          |         |        |        |        | 15    | 15     | 12     | 13    | 14    |        | 15    |       | 15    |        |
| **F**  |         |          |         | 17     | 18     | 19     |       |        |        |       |       |        |       | 16    |       |        |

## LEGENDAS DE PRODUÇÃO

- 0: P -> L
- 1: L -> C L
- 2: L -> ε
- 3: C -> inteiro id ponto_virgula
- 4: C -> real id ponto_virgula
- 5: C -> texto id ponto_virgula
- 6: C -> id atribuicao E ponto_virgula
- 7: E -> T E1
- 8: E1 -> mais T E1
- 9: E1 -> menos T E1
- 10: E1 -> ε
- 11: T -> F T1
- 12: T1 -> multiplicacao F T1
- 13: T1 -> divisao F T1
- 14: T1 -> modulo F T1
- 15: T1 -> ε
- 16: F -> abre_parenteses E fecha_parenteses
- 17: F -> id
- 18: F -> num_int
- 19: F -> num_real