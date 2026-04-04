import datetime as dt

class Equipo:
    _contador = 0  # Contador global para códigos únicos
    
    def __init__(self, nombre, marca, tipo, ubicacion):
        Equipo._contador += 1
        self.codigo = f"EQ-{Equipo._contador:04d}" 
        self.nombre = nombre
        self.marca = marca
        self.tipo = tipo
        self.ubicacion = ubicacion
        self.historial = []
    
    def registrar_medicion(self, SH, SC, COP):
        self.historial.append({
            "fecha": dt.datetime.now().isoformat(),
            "SH": SH,
            "SC": SC,
            "COP": COP
        })