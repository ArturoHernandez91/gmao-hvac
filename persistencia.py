import json
import os
import csv
from equipo import Equipo
from diagnostico import diagnostico, degradacion

def guardar(equipos):
    try:
        os.makedirs("datos", exist_ok=True)
        data = {}
        for nombre, eq in equipos.items():
            data[nombre] = {
                "nombre": eq.nombre,
                "marca": eq.marca,
                "tipo": eq.tipo,
                "ubicacion": eq.ubicacion,
                "historial": eq.historial
            }
        # Guardar en archivo 
        with open("datos/gmao.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"Guardados {len(equipos)} equipos")
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

def cargar():
    try:
        with open("datos/gmao.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        equipos = {}
        for nombre, d in data.items():
            eq = Equipo(d["nombre"], d["marca"], d["tipo"], d["ubicacion"])
            eq.historial = d["historial"]
            equipos[nombre] = eq
        
        print(f"Cargados {len(equipos)} equipos")
        return equipos
    except FileNotFoundError:
        print("Archivo no encontrado. Creando nueva base de datos.")
        return {}
    except Exception as e:
        print(f"Error al cargar: {e}")
        return {}

def exportar_csv(equipos, nombre_archivo="reporte_gmao.csv"):
    """Exporta todas las mediciones a CSV (compatible con Excel español)"""
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')  # Cambiado a punto y coma
            
            # Cabecera
            writer.writerow([
                "Equipo", "Marca", "Tipo", "Ubicación",
                "Fecha", "SH", "SC", "COP", "Diagnóstico"
            ])
            
            # Datos
            for nombre, eq in equipos.items():
                for medicion in eq.historial:
                    diag = diagnostico(medicion["SH"], medicion["SC"])
                    writer.writerow([
                        eq.nombre,
                        eq.marca,
                        eq.tipo,
                        eq.ubicacion,
                        medicion["fecha"],
                        medicion["SH"],
                        medicion["SC"],
                        medicion["COP"],
                        diag
                    ])
        
        print(f"✅ Exportado: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def exportar_resumen_csv(equipos, nombre_archivo="resumen_gmao.csv"):
    """Exporta resumen por equipo a CSV (compatible con Excel español)"""
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')  # Cambiado a punto y coma
            
            writer.writerow([
                "Equipo", "Marca", "Tipo", "Ubicación",
                "Mediciones", "Último SH", "Último SC", 
                "Último COP", "Diagnóstico", "Tendencia"
            ])
            
            for nombre, eq in equipos.items():
                if eq.historial:
                    ultima = eq.historial[-1]
                    diag = diagnostico(ultima["SH"], ultima["SC"])
                    tendencia = degradacion(eq.historial)
                else:
                    ultima = {"SH": "-", "SC": "-", "COP": "-"}
                    diag = "Sin mediciones"
                    tendencia = "Sin datos"
                
                writer.writerow([
                    eq.nombre,
                    eq.marca,
                    eq.tipo,
                    eq.ubicacion,
                    len(eq.historial),
                    ultima["SH"],
                    ultima["SC"],
                    ultima["COP"],
                    diag,
                    tendencia
                ])
        
        print(f"✅ Resumen exportado: {nombre_archivo}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False