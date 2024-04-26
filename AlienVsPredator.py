import random
import time

class Node:
    __slots__ = 'value', 'next', 'prev'

    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __str__(self):
        return str(self.value)

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, value):
        new_node = Node(value)
        if self.head == None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.length += 1

    def __iter__(self):
        curr_node = self.head
        while curr_node is not None:
            yield curr_node
            curr_node = curr_node.next

    def __str__(self):
        result = [str(x.prev) + '<--' + str(x.value) + '-->' + str(x.next) for x in self]
        # result = [str(x.value) for x in self]
        return '  '.join(result)

class Alien:
    def __init__(self):
        self.vida = 50
        self.simbolo = "👽 "
        self.coordenadas = None

class Depredador:
    def __init__(self):
        self.vida = 50
        self.simbolo = "🤖 "
        self.coordenadas = None

class Tablero:
    def __init__(self, n):
        self.n = n
        self.matriz = DoubleLinkedList()

    def crear_tablero(self, alien, depredador, nivel_dificultad):
        simbolos = ['+', '-']
        depredador_coord = [(random.randint(0, self.n - 1), random.randint(0, self.n - 1))]
        depredador.coordenadas = depredador_coord
        print("El depredador saldrá en la posición:", depredador.coordenadas)
        alien_coord = []
        while True:
            coordenadas = str(input("Ingrese las coordenadas en las que desea aparecer al alien: "))
            coordenadas = coordenadas.strip()
            coordenadas = coordenadas.split(",")
            if len(coordenadas) != 2 or not coordenadas[0].isdigit() or not coordenadas[1].isdigit() or int(
                    coordenadas[0]) < 0 or int(coordenadas[0]) > self.n - 1 or int(coordenadas[1]) < 0 or int(
                    coordenadas[1]) > self.n - 1:
                print("Posición inválida")
            else:
                fila_alien_coord = int(coordenadas[0])
                columna_alien_coord = int(coordenadas[1])
                alien_coord.append(fila_alien_coord)
                alien_coord.append(columna_alien_coord)
                alien_coord = [tuple(alien_coord)]
                alien.coordenadas = alien_coord
                break
        while alien_coord == depredador_coord:
            depredador_coord = [(random.randint(0, self.n - 1), random.randint(0, self.n - 1))]
            depredador.coordenadas = depredador_coord

        for i in range(self.n):
            fila = DoubleLinkedList()
            for j in range(self.n):
                if (i, j) in depredador_coord:
                    fila.append(depredador)
                elif (i, j) in alien_coord:
                    fila.append(alien)
                else:
                    if random.random() > nivel_dificultad / 100:
                        fila.append(' . ')
                    else:
                        simbolo = random.choice(simbolos)
                        if simbolo == '+':
                            fila.append(' + ')
                        else:
                            fila.append(' - ')
                            if depredador_coord is None:
                                depredador_coord = (i, j)
            self.matriz.append(fila)

    def imprimir_tablero(self):
        current = self.matriz.head
        print(" 0  ", end="")
        for i in range(1, self.n):
            print(i, end="  ")
        print()
        while current != None:
            fila = current.value
            node = fila.head
            while node != None:
                value = node.value
                if isinstance(value, Alien):
                    print(value.simbolo, end='')
                elif isinstance(value, Depredador):
                    print(value.simbolo, end='')
                else:
                    print(value, end='')
                node = node.next
            print()
            current = current.next

class Juego:
    def __init__(self, tablero, controlador):
        self.tablero = tablero
        tablero.imprimir_tablero()
        self.controlador_juego(controlador)

    def controlador_juego(self, controlador):
        if controlador == False:
            self.obtener_movimiento_alien()
        elif controlador == True:
            print()
            print("El juego ha finalizado")
            exit()

    def obtener_movimiento_alien(self):
        coordenadas = alien.coordenadas[0]
        movimiento_izquierda = (coordenadas[0], coordenadas[1] - 1)
        movimiento_derecha = (coordenadas[0], coordenadas[1] + 1)
        movimiento_arriba = (coordenadas[0] - 1, coordenadas[1])
        movimiento_abajo = (coordenadas[0] + 1, coordenadas[1])
        posibles_ataques = [movimiento_arriba, movimiento_abajo, movimiento_derecha, movimiento_izquierda]
        if depredador.coordenadas[0] in posibles_ataques:
            while True:
                atacar = input("El depredador se encuentra en su rango de ataque, desea atacarlo? (s/n) ").lower()
                if atacar == "s":
                    depredador.vida -= 10
                    print("La vida del depredador disminuyó a ", depredador.vida)
                    break
                elif atacar == "n":
                    break
        movimientos_disponibles = ["arriba", "abajo", "derecha", "izquierda"]
        if coordenadas[0] == 0:
            movimientos_disponibles.remove("arriba")
            if coordenadas[1] == 0:
                movimientos_disponibles.remove("izquierda")
            elif coordenadas[1] == tablero.n - 1:
                movimientos_disponibles.remove("derecha")
        if coordenadas[0] == tablero.n - 1:
            movimientos_disponibles.remove("abajo")
            if coordenadas[1] == 0:
                movimientos_disponibles.remove("izquierda")
            elif coordenadas[1] == tablero.n - 1:
                movimientos_disponibles.remove("derecha")
        if coordenadas[1] == 0:
            if "izquierda" in movimientos_disponibles:
                movimientos_disponibles.remove("izquierda")
        if coordenadas[1] == tablero.n - 1:
            if "derecha" in movimientos_disponibles:
                movimientos_disponibles.remove("derecha")
        print("Ingrese el movimiento que desea realizar: ", end="")
        for i, movimiento in enumerate(movimientos_disponibles):
            if i == len(movimientos_disponibles) - 1:
                print(movimiento, end="")
            else:
                print(movimiento, end=", ")
        print()
        while True:
            nuevo_mov = input().lower()
            if nuevo_mov not in movimientos_disponibles:
                print("Ingresa un valor valido, no puedes moverte en esa dirección")
            elif nuevo_mov == "arriba":
                direccion = movimiento_arriba
                break
            elif nuevo_mov == "abajo":
                direccion = movimiento_abajo
                break
            elif nuevo_mov == "derecha":
                direccion = movimiento_derecha
                break
            elif nuevo_mov == "izquierda":
                direccion = movimiento_izquierda
                break
        print("Tu direccion de movimiento es ", nuevo_mov, ", con coordenadas ", direccion)
        self.mover_alien(direccion, alien)

    def mover_alien(self, direccion, alien):
        direccion = [direccion]
        current = tablero.matriz.head
        fila = current.value
        node = fila.head
        for i in range(tablero.n):
            for j in range(tablero.n):
                if node is None:
                    current = current.next
                    fila = current.value
                    node = fila.head
                if (i, j) in direccion:
                    if node.value == " + ":
                        alien.vida += 10
                        print("Tu vida ha aumentado 10 puntos, ahora tienes: ", alien.vida, "de vida")
                    elif node.value == ' - ':
                        alien.vida -= 10
                        print("Tu vida ha disminuido 10 puntos, ahora tienes: ", alien.vida, "de vida")
                    elif isinstance(node.value, Depredador):
                        print("¿Enloquecimos?")
                        alien.vida -= 25
                        print("Tu vida ha disminuido a: ", alien.vida,
                              "por intentar estar en el mismo lugar que el depredador!")
                        tablero.imprimir_tablero()
                        self.obtener_movimiento_depredador()
                    node.value = alien
                node = node.next
        if (self.end_game()):
            self.estado_de_juego(True)
        self.borrar_alien(alien, direccion)

    def borrar_alien(self, alien, nuevas_coord):
        current = tablero.matriz.head
        fila = current.value
        node = fila.head
        for i in range(tablero.n):
            for j in range(tablero.n):
                if node is None:
                    current = current.next
                    fila = current.value
                    node = fila.head
                if (i, j) in alien.coordenadas:
                    node.value = ' . '
                node = node.next
        alien.coordenadas = nuevas_coord
        tablero.imprimir_tablero()
        self.obtener_movimiento_depredador()

    def obtener_movimiento_depredador(self):
        coordenadas = depredador.coordenadas[0]
        movimiento_izquierda = (coordenadas[0], coordenadas[1] - 1)
        movimiento_derecha = (coordenadas[0], coordenadas[1] + 1)
        movimiento_arriba = (coordenadas[0] - 1, coordenadas[1])
        movimiento_abajo = (coordenadas[0] + 1, coordenadas[1])

        movimientos_disponibles = [movimiento_abajo, movimiento_arriba, movimiento_derecha, movimiento_izquierda]
        movimientos_validos = []
        for movimiento in movimientos_disponibles:
            if not (-1 in movimiento or tablero.n in movimiento):
                movimientos_validos.append(movimiento)
        movimiento = random.choice(movimientos_validos)
        self.mover_depredador(movimiento)

    def mover_depredador(self, coordenadas):
        print()
        print("Es turno del depredador, preparando su movimiento...")
        time.sleep(3)
        print("El depredador se mueve a las coordenadas ", coordenadas)
        coordenadas = [coordenadas]
        current = tablero.matriz.head
        fila = current.value
        node = fila.head
        for i in range(tablero.n):
            for j in range(tablero.n):
                if node is None:
                    current = current.next
                    fila = current.value
                    node = fila.head
                if (i, j) in coordenadas:
                    if node.value == " + ":
                        depredador.vida += 10
                        print("La vida del depredador ha aumentado 10 puntos, ahora tiene: ", depredador.vida,
                              "de vida")
                    elif node.value == ' - ':
                        depredador.vida -= 10
                        print("La vida del depredador ha disminuido 10 puntos, ahora tiene: ", depredador.vida,
                              "de vida")
                    elif isinstance(node.value, Alien):
                        alien.vida -= 25
                        print("El depredador ha atacado al alien, la vida del alien ahora es ", alien.vida)
                        tablero.imprimir_tablero()
                        self.estado_de_juego(self.end_game())
                    node.value = depredador
                node = node.next
        if (self.end_game()):
            self.estado_de_juego(True)
        self.borrar_depredador(depredador, coordenadas)

    def borrar_depredador(self, depredador, nuevas_coord):
        current = tablero.matriz.head
        fila = current.value
        node = fila.head
        for i in range(tablero.n):
            for j in range(tablero.n):
                if node is None:
                    current = current.next
                    fila = current.value
                    node = fila.head
                if (i, j) in depredador.coordenadas:
                    node.value = ' . '
                node = node.next
        depredador.coordenadas = nuevas_coord
        tablero.imprimir_tablero()
        self.estado_de_juego(self.end_game())

    def end_game(self):
        if depredador.vida <= 0:
            print("¡El alien ha ganado!")
            return True
        elif alien.vida <= 0:
            print("¡El Depredador ha ganado!")
            return True
        else:
            return False

    def estado_de_juego(self, estado):
        if estado == True:
            self.controlador_juego(True)
        else:
            self.controlador_juego(False)

alien = Alien()
depredador = Depredador()
tablero = Tablero(4)
nivel_dificultad = int(input("Ingrese el nivel de dificultad (0-100): "))
tablero.crear_tablero(alien, depredador, nivel_dificultad)

Controlador = Juego(tablero, False)
tablero.imprimir_tablero()

"""
customll = DoubleLinkedList()
customll.append(1)
customll.append(2)
customll.append(3)
print(customll)
"""
