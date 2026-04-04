from equipo import Equipo

class Sistema:
    def __init__(self):
        self.equipos = {}  # clave: código, valor: equipo
        self.proximo_codigo = 1

    def agregar_equipo(self, nombre, marca, tipo, ubicacion):
        equipo = Equipo(nombre, marca, tipo, ubicacion)
        self.equipos[equipo.codigo] = equipo
        return equipo.codigo

    def listar(self):
        if not self.equipos:
            print("No hay equipos registrados")
        else:
            print(f"\n{'='*80}")
            print(f"{'CÓDIGO':<12} {'EQUIPO':<25} {'MARCA':<12} {'UBICACIÓN':<25}")
            print(f"{'='*80}")
        
            for codigo, eq in self.equipos.items():
                print(f"{codigo:<12} {eq.nombre:<25} {eq.marca:<12} {eq.ubicacion:<25}")
        
            print(f"{'='*80}")
            print(f"Total: {len(self.equipos)} equipos\n")
    
    def buscar_por_codigo(self, codigo):
        return self.equipos.get(codigo)
    
    def buscar_por_nombre(self, nombre):
        for codigo, eq in self.equipos.items():
            if eq.nombre.lower() == nombre.lower():
                return codigo, eq
        return None, None