import sys

#  1. ESTRUCTURA DE DATOS: LA PILA (STACK)
class Pila:

    def __init__(self):
    # almacenamiento interno (privado)
        self._items = []          

    def push(self, item):
        """Coloca un elemento en el tope de la pila. Costo O(1)."""
        self._items.append(item)

    def pop(self):
        """Retira y devuelve el elemento del tope. Costo O(1)."""
        if self.esta_vacia():
            raise IndexError("pop() sobre una pila vacia")
        return self._items.pop()

    def peek(self):
        """Consulta el tope SIN retirarlo. Devuelve None si esta vacia."""
        if self.esta_vacia():
            return None
        return self._items[-1]

    def esta_vacia(self):
        """True si no quedan elementos pendientes."""
        return len(self._items) == 0

    def tamano(self):
        return len(self._items)

    def pendientes(self):
        """Devuelve una copia de los elementos que quedaron sin cerrar."""
        return list(self._items)

    def contenido(self):
        """Representacion visual de la pila: base a la izquierda, tope a la derecha."""
        if self.esta_vacia():
            return "(vacia)"
        simbolos = "".join(simbolo for simbolo, _ in self._items)
        return f"[ {' '.join(simbolos)} ]  <- tope"


#  2. TABLA DE SIMBOLOS DE INTERES
# Cada simbolo de cierre se mapea a su correspondiente simbolo de apertura.
# Cambiar esta tabla es lo unico necesario para soportar mas simbolos.
PAREJAS = {
    ')': '(',
    ']': '[',
    '}': '{',
}

APERTURAS = set(PAREJAS.values())   # {'(', '[', '{'}
CIERRES = set(PAREJAS.keys())       # {')', ']', '}'}

ESCAPE = '\\'                       # caracter de escape


#  3. ALGORITMO DE BALANCEO
def balancear(expresion):

    pila = Pila()
    pasos = []
    # bandera: el caracter anterior fue una '\'
    escapado = False       

    for posicion, caracter in enumerate(expresion):

        # CASO 0: el caracter anterior fue '\' -> este es literal 
        if escapado:
            pasos.append(_paso(posicion, caracter,
                               "Caracter escapado con '\\': se trata como "
                               "literal, NO se apila", pila))
            escapado = False
            continue

        # CASO 1: caracter de escape 
        if caracter == ESCAPE:
            escapado = True
            pasos.append(_paso(posicion, caracter,
                               "Inicia escape: el siguiente caracter sera literal",
                               pila))
            continue

        #  CASO 2: simbolo de APERTURA -> PUSH 
        if caracter in APERTURAS:
            pila.push((caracter, posicion))
            pasos.append(_paso(posicion, caracter,
                               f"PUSH '{caracter}'", pila))
            continue

        #  CASO 3: simbolo de CIERRE -> POP 
        if caracter in CIERRES:
            esperado = PAREJAS[caracter]

            # 3a. No hay ninguna apertura pendiente -> error
            if pila.esta_vacia():
                pasos.append(_paso(posicion, caracter,
                                   f"ERROR: '{caracter}' sin apertura previa "
                                   f"(pila vacia)", pila))
                return (False, pasos,
                        f"Cierre '{caracter}' en la posicion {posicion} "
                        f"no tiene apertura correspondiente.")

            tope, pos_tope = pila.pop()

            # 3b. El tope no es la pareja correcta -> error de anidamiento
            if tope != esperado:
                pasos.append(_paso(posicion, caracter,
                                   f"ERROR: se esperaba cerrar '{tope}' "
                                   f"(abierto en pos {pos_tope}), "
                                   f"pero llego '{caracter}'", pila))
                return (False, pasos,
                        f"Anidamiento incorrecto en la posicion {posicion}: "
                        f"'{caracter}' intenta cerrar '{tope}' "
                        f"(abierto en la posicion {pos_tope}).")

            # 3c. Emparejamiento correcto
            pasos.append(_paso(posicion, caracter,
                               f"POP  '{tope}'  ->  pareja '{tope}{caracter}' "
                               f"correcta (apertura en pos {pos_tope})", pila))
            continue

        #  CASO 4: cualquier otro caracter -> se ignora 
        pasos.append(_paso(posicion, caracter,
                           "No es simbolo de interes: se ignora", pila,
                           relevante=False))

    #  Escape colgante al final de la linea 
    if escapado:
        return (False, pasos,
                "La expresion termina con un '\\' sin caracter que escapar.")

    #  Al terminar la pila DEBE estar vacia 
    if not pila.esta_vacia():
        pendientes = ", ".join(f"'{s}' (pos {p})" for s, p in pila.pendientes())
        return (False, pasos,
                f"Quedaron {pila.tamano()} apertura(s) sin cerrar: {pendientes}.")

    return (True, pasos, "Expresion correctamente balanceada.")


def _paso(posicion, caracter, accion, pila, relevante=True):
    """Construye el registro de un paso de la traza."""
    return {
        "posicion": posicion,
        "caracter": caracter,
        "accion": accion,
        "pila": pila.contenido(),
        "relevante": relevante,
    }


#  4. IMPRESION DE RESULTADOS

def imprimir_traza(numero_linea, expresion, balanceada, pasos, mensaje,
                   mostrar_todos=False):
    print(f"LINEA {numero_linea}: {expresion}")
   

    visibles = pasos if mostrar_todos else [p for p in pasos if p["relevante"]]

    if not visibles:
        print("  (la linea no contiene simbolos de agrupacion)")
    else:
        print(f"  {'#':>3}  {'Pos':>4}  {'Car':^5}  {'Accion':<66}  Pila")
        print(f"  {'-'*3}  {'-'*4}  {'-'*5}  {'-'*66}  {'-'*20}")
        for i, p in enumerate(visibles, start=1):
            print(f"  {i:>3}  {p['posicion']:>4}  {p['caracter']:^5}  "
                  f"{p['accion']:<66}  {p['pila']}")

    print()
    estado = "BALANCEADA" if balanceada else "NO BALANCEADA"
    marca = "[OK]" if balanceada else "[X]"
    print(f"  RESULTADO: {marca} {estado}")
    print(f"  Detalle:   {mensaje}")
    print()


#  5. PROGRAMA PRINCIPAL
def main():
    if len(sys.argv) < 2:
        print("archivo utilizado: Expresiones.txt")
        sys.exit(1)

    ruta = sys.argv[1]
    mostrar_todos = "--todos" in sys.argv

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"ERROR: no se encontro el archivo '{ruta}'")
        sys.exit(1)

    print()
    print(f"#  BALANCEADOR DE EXPRESIONES INFIX  -  archivo: {ruta}")
    print()

    total = 0
    correctas = 0

    for numero, linea in enumerate(lineas, start=1):
        expresion = linea.rstrip("\n").rstrip("\r")

        # Se omiten lineas vacias y comentarios que inicien con '#'
        if expresion.strip() == "" or expresion.lstrip().startswith("#"):
            continue

        total += 1
        balanceada, pasos, mensaje = balancear(expresion)
        if balanceada:
            correctas += 1
        imprimir_traza(numero, expresion, balanceada, pasos, mensaje,
                       mostrar_todos)

    print(f"#  RESUMEN: {correctas} de {total} expresiones estan balanceadas")
    
if __name__ == "__main__":
    main()