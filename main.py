from sistema import Sistema
from persistencia import guardar, cargar
from diagnostico import diagnostico, degradacion

def input_float(mensaje):
    """Solicita un número decimal al usuario, contemplando errores"""
    while True:
        valor = input(mensaje)
        if not valor:
            print("El valor no puede estar vacío. Intente nuevamente.")
            continue
        try:
            return float(valor)
        except ValueError:
            print("Error: Debe ingresar un número válido (use un punto para decimales). Ej: 10.5")

def input_texto(mensaje):
    """Solicita texto no vacío al usuario"""
    while True:
        valor = input(mensaje)
        if not valor.strip():
            print("El valor no puede estar vacío. Intente nuevamente.")
            continue
        return valor.strip()

def buscar_equipo(sistema, busqueda):
    """Busca equipo por código o por nombre (sin distinguir mayúsculas/minúsculas)"""
    # 1. Buscar por código exacto
    if busqueda in sistema.equipos:
        return busqueda, sistema.equipos[busqueda]
    
    # 2. Buscar por nombre (sin distinguir mayúsculas)
    for codigo, eq in sistema.equipos.items():
        if eq.nombre.lower() == busqueda.lower():
            return codigo, eq
    
    # 3. No encontrado
    return None, None

sistema = Sistema()
sistema.equipos = cargar()

while True:
    print("""
    ================================
    1. Añadir equipo
    2. Listar equipos
    3. Registrar medición
    4. Diagnosticar equipo
    5. Ver degradación
    6. Guardar datos
    7. Exportar a CSV
    8. Modificar equipo
    9. Eliminar equipo
    0. Salir
    ================================
    """)
    
    opcion = input("Opción: ").strip()
    
    if opcion == "1":
        print("\n--- NUEVO EQUIPO ---")
        nombre = input_texto("Nombre: ")
        marca = input_texto("Marca: ")
        tipo = input_texto("Tipo: ")
        ubicacion = input_texto("Ubicación: ")
        sistema.agregar_equipo(nombre, marca, tipo, ubicacion)
        print(f"Equipo '{nombre}' agregado correctamente")
    
    elif opcion == "2":
        sistema.listar()
    
    elif opcion == "3":
        print("\n--- REGISTRAR MEDICIÓN ---")
        busqueda = input("Código o nombre del equipo: ")
        codigo, equipo = buscar_equipo(sistema, busqueda)
    
        if equipo:
            print(f"Equipo: {equipo.nombre} ({codigo})")
            sh = input_float("SH (sobrecalentamiento): ")
            sc = input_float("SC (subenfriamiento): ")
            cop = input_float("COP (coeficiente de rendimiento): ")
            equipo.registrar_medicion(sh, sc, cop)
            print(f"Medición registrada en '{equipo.nombre}'")
        else:
            print(f"Equipo '{busqueda}' no encontrado")
            print("   Usa la opción 2 para ver los equipos disponibles")
    
    elif opcion == "4":
        print("\n--- DIAGNÓSTICO ---")
        busqueda = input("Código o nombre del equipo: ")
        codigo, equipo = buscar_equipo(sistema, busqueda)
    
        if equipo:
            historial = equipo.historial
            if len(historial) > 0:
                ult = historial[-1]
                resultado = diagnostico(ult["SH"], ult["SC"])
                print(f"\nEquipo: {equipo.nombre} ({codigo})")
                print(f"   Última medición:")
                print(f"   SH: {ult['SH']} | SC: {ult['SC']} | COP: {ult['COP']}")
                print(f"Diagnóstico: {resultado}")
            else:
                print(f"El equipo '{equipo.nombre}' no tiene mediciones registradas")
        else:
            print(f"Equipo '{busqueda}' no encontrado")
    
    elif opcion == "5":
        print("\n--- ANÁLISIS DE DEGRADACIÓN ---")
        busqueda = input("Código o nombre del equipo: ")
        codigo, equipo = buscar_equipo(sistema, busqueda)
        
        if equipo:
            historial = equipo.historial
            if len(historial) > 0:
                resultado = degradacion(historial)
                print(f"\nEquipo: {equipo.nombre} ({codigo})")
                print(f"   Historial: {len(historial)} registros")
                print(f"Análisis: {resultado}")
            else:
                print(f"El equipo '{equipo.nombre}' no tiene mediciones registradas")
        else:
            print(f"Equipo '{busqueda}' no encontrado")
        
    elif opcion == "6":
        guardar(sistema.equipos)
        print("Datos guardados correctamente")

    elif opcion == "7":
        print("\n--- EXPORTAR A CSV ---")
        print("1. Exportar detalle completo (todas las mediciones)")
        print("2. Exportar resumen (último estado por equipo)")
        
        sub_opcion = input("Opción: ")
        
        if sub_opcion == "1":
            from persistencia import exportar_csv
            exportar_csv(sistema.equipos)
        elif sub_opcion == "2":
            from persistencia import exportar_resumen_csv
            exportar_resumen_csv(sistema.equipos)
        else:
            print("Opción no válida")
    
    elif opcion == "8":
        print("\n--- MODIFICAR EQUIPO ---")
        busqueda = input("Código o nombre del equipo a modificar: ")
        codigo, equipo = buscar_equipo(sistema, busqueda)
        
        if equipo:
            print(f"\nDatos actuales de '{equipo.nombre}' ({codigo}):")
            print(f"  Marca: {equipo.marca}")
            print(f"  Tipo: {equipo.tipo}")
            print(f"  Ubicación: {equipo.ubicacion}")
            
            print("\n--- NUEVOS DATOS (dejar vacío para mantener) ---")
            
            nueva_marca = input(f"Nueva marca [{equipo.marca}]: ").strip()
            if nueva_marca:
                equipo.marca = nueva_marca
            
            nuevo_tipo = input(f"Nuevo tipo [{equipo.tipo}]: ").strip()
            if nuevo_tipo:
                equipo.tipo = nuevo_tipo
            
            nueva_ubicacion = input(f"Nueva ubicación [{equipo.ubicacion}]: ").strip()
            if nueva_ubicacion:
                equipo.ubicacion = nueva_ubicacion
            
            print(f"Equipo '{equipo.nombre}' modificado correctamente")
            
            guardar_cambios = input("¿Guardar cambios ahora? (s/n): ")
            if guardar_cambios.lower() == 's':
                guardar(sistema.equipos)
        else:
            print(f"Equipo '{busqueda}' no encontrado")

    elif opcion == "9":
        print("\n--- ELIMINAR EQUIPO ---")
        busqueda = input("Código o nombre del equipo a eliminar: ")
        codigo, equipo = buscar_equipo(sistema, busqueda)
        
        if equipo:
            print(f"\nEquipo a eliminar:")
            print(f"  Código: {codigo}")
            print(f"  Nombre: {equipo.nombre}")
            print(f"  Marca: {equipo.marca}")
            print(f"  Mediciones: {len(equipo.historial)}")
            
            confirmar = input(f"\n¿Eliminar permanentemente '{equipo.nombre}'? (s/n): ")
            if confirmar.lower() == 's':
                del sistema.equipos[codigo]
                print(f"Equipo '{equipo.nombre}' eliminado")
                
                guardar_cambios = input("¿Guardar cambios ahora? (s/n): ")
                if guardar_cambios.lower() == 's':
                    guardar(sistema.equipos)
            else:
                print("Eliminación cancelada")
        else:
            print(f"Equipo '{busqueda}' no encontrado")
    
    elif opcion == "0":
        guardar(sistema.equipos)
        print("\n¡Hasta luego!")
        print(f"   Se guardaron {len(sistema.equipos)} equipos con sus historiales")
        break
    
    else:
        print("Opción no válida. Elija un número del 0 al 6")