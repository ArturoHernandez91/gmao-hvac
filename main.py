from sistema import Sistema
from persistencia import guardar, cargar
from diagnostico import diagnostico, degradacion

sistema = Sistema()
sistema.equipos = cargar()

while True:
    print("""
    1. Añadir equipo
    2. Listar
    3. Medición
    4. Diagnóstico
    5. Degradación
    6. Guardar
    0. Salir
    """)
    
    op = input("Opción: ")

    if op == "1":
        n = input("Nombre: ")
        m = input("Marca: ")
        t = input("Tipo: ")
        u = input("Ubicacion: ")
        sistema.agregar_equipo(n, m, t, u)

    elif op == "2":
        sistema.listar()

    elif op == "3":
        n = input("Equipo: ")
        SH = float(input("SH: "))
        SC = float(input("SC: "))
        COP = float(input("COP: "))

        sistema.equipos[n].registrar_medicion(SH, SC, COP)

    elif op =="4":
        n = input("Equipo: ")
        ult = sistema.equipos[n].historial[-1]
        print(diagnostico(ult["SH"], ult["SC"]))
    
    elif op =="5":
        n = input("Equipo: ")
    
        print(degradacion(sistema.equipos[n].historial))
    
    elif op =="6":
        guardar(sistema.equipos)

    elif op =="0":
        guardar(sistema.equipos)
        break

