def diagnostico(SH, SC):
    if SH > 12 and SC <3:
        return "Falta de refrigerante"
    elif SH < 5 and SC > 8:
        return "Sobrecarga"
    else:
        return "Funcionamiento normal"

def degradacion(historial):
    if len(historial) < 3:
        return "Sin datos suficientes en el historial"
    
    cop_vals = [m["COP"] for m in historial[-3:]]
    if cop_vals [-1] < cop_vals[0]:
        return "Rendimiento en descenso"
    return "Estable"