from equipo import Equipo

class Sistema:
    def __init__(self):
        self.equipos = {}

    def agregar_equipo(self, nombre, marca, tipo, ubicacion):
        self.equipos[nombre] = Equipo(nombre, marca, tipo, ubicacion)

    def listar (self):
        for eq in self.equipos.values():
            print(f"{eq.nombre} - {eq.marca} ({eq.ubicacion})")