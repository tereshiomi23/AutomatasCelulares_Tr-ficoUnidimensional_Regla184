import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==========================================
# CONFIGURACIÓN INDISPENSABLE (Ítem 3.2)
# ==========================================
CEDULA = "55044"  # <--- SUSTITUYE POR TUS ÚLTIMOS 5 DÍGITOS
SEMILLA = int(CEDULA)
np.random.seed(SEMILLA)





def inicializar_carretera(N, densidad):
    """
    Crea una carretera circular de tamaño N.
    Representación (Ítem 3.4): 1 = Coche, 0 = Espacio vacío.
    """
    # Esta es la línea corregida que soluciona el ValueError y el SyntaxError
    return np.random.choice([0,1], size=N, p=[1-densidad, densidad])


def aplicar_regla_184(actual):
    """
    Aplica la micro-física de la Regla 184 (Ítem 3.1).
    Un coche avanza si hay un espacio (0) adelante.
    """
    N = len(actual)
    siguiente = np.zeros(N, dtype=int)
    
    for i in range(N):
        # Índices con módulo N para que la carretera sea CIRCULAR
        izquierda = actual[(i - 1) % N]
        centro = actual[i]
        derecha = actual[(i + 1) % N]
        
        # LÓGICA DE TRANSICIÓN (Basada en tu diagrama de flujo)
        if centro == 1:
            if derecha == 0:
                siguiente[i] = 0  # El coche avanza, deja la celda vacía
            else:
                siguiente[i] = 1  # Bloqueado por otro coche (Atasco)
        else: # centro == 0
            if izquierda == 1:
                siguiente[i] = 1  # Un coche entra en este espacio
            else:
                siguiente[i] = 0  # El espacio sigue vacío
                
    return siguiente

def ejecutar_simulacion(N, pasos, densidad, nombre_escenario):
    carretera = inicializar_carretera(N, densidad)
    datos_log = []
    historial_visual = [carretera.copy()]

    for t in range(pasos):
        # EXTRACCIÓN DE DATOS CADA 5 ITERACIONES (Ítem 3.7)
        if t % 5 == 0:
            activas = np.sum(carretera)
            vacias = N - activas
            datos_log.append([t, N, vacias, activas, SEMILLA])
        
        carretera = aplicar_regla_184(carretera)
        historial_visual.append(carretera.copy())

    # GUARDAR DATOS EN CSV (Ítem 3.7)
    df = pd.DataFrame(datos_log, columns=["Iteracion", "Total", "Vacias", "Activas", "Semilla"])
    df.to_csv(f"datos_{nombre_escenario}.csv", index=False)
    
    return np.array(historial_visual)

# ==========================================
# EJECUCIÓN DE ESCENARIOS (Ítem 3.6)
# ==========================================
# Escenario C: Comparación de Densidad (20% vs 80%)
N_CELDAS = 100
PASOS = 50

print(f"Simulando con semilla: {SEMILLA}...")
evolucion = ejecutar_simulacion(N_CELDAS, PASOS, 0.3, "Escenario_B_Caos")

# Visualización rápida (Genera la salida gráfica para el informe)
plt.figure(figsize=(10, 6))
plt.imshow(evolucion, cmap='Greys', interpolation='nearest')
plt.title(f"Evolución Regla 184 - Semilla {SEMILLA}")
plt.xlabel("Posición en la carretera")
plt.ylabel("Tiempo (Iteraciones)")
plt.show()