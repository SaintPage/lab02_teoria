# lab02_teoria
## Autor
- 23661 Ángel de Jesús Mérida Jiménez 

# Problema 2 — Balanceo de expresiones infix

Programa que verifica si los símbolos `( )`, `[ ]` y `{ }` de una expresión
están balanceados, usando una **pila**.

## Por qué una pila

Balancear no se puede resolver contando aperturas y cierres: el orden del
anidamiento también importa (`{[(])}` tiene 3 y 3, pero está mal anidado).
Solo una pila lo detecta, porque el tope siempre debe ser la apertura más
reciente.

## Ejecución


python3 balanceador.py expresiones.txt
python3 balanceador.py expresiones.txt --todos   # muestra todos los caracteres


Una expresión por línea en el archivo. Las líneas vacías o que empiezan con
`#` se ignoran.

## Errores detectados

| Error | Ejemplo |
|---|---|
| Cierre sin apertura | `...b]` |
| Anidamiento cruzado | `{[(])}` |
| Apertura sin cerrar | `((((` |


# Problema 3 — Algoritmo de Shunting Yard

Convierte expresiones regulares de notación **infix** a **postfix**, usando
una pila.

## Qué es

Lo publicó Edsger Dijkstra en 1961. El nombre viene de las estaciones de
maniobras de tren: los vagones se desvían a una vía muerta y se reincorporan
en otro orden — esa vía muerta es la pila.

Se recorre la entrada una sola vez: los operandos van directo a la salida;
al llegar un operador, mientras el tope de la pila tenga precedencia mayor o
igual, se saca ese tope hacia la salida antes de apilar el operador nuevo.

## Tabla de precedencias

| Prioridad | Operador |
|---|---|
| 4 (alta) | `*` `+` `?` |
| 3 | concatenación (`·`, insertada por el programa) |
| 2 | `\|` |
| — | `( )`, actúan como barrera |

## Adaptaciones para regex

- **Concatenación implícita**: se inserta un `·` entre operandos consecutivos.
- **El punto es literal**: se reserva `·` para la concatenación, así el `.`
  de una regex (ej. dominios) no se confunde con el operador.
- **Escapados**: `\(`, `\)`, etc. se leen como literales.
- **Clases de caracteres**: `[ae]` se lee como un solo operando.

## Extensiones `+` y `?`

Se expanden sobre el postfix (pila de fragmentos):

```
A+  ->  A A*
A?  ->  A | ε
```

## Ejecución


python3 shunting_yard.py regex.txt


Una expresión por línea. Líneas vacías o que empiezan con `//` se ignoran.

- Link al primer vídeo: https://youtu.be/XnEgIjlt2cw (Segundo problema).
- Link al segundo vídeo https://youtu.be/bpVJA5jBvd4 (tercer problema).


