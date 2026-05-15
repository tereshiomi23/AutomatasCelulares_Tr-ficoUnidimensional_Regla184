import numpy as np
import time
import os

N_CELDAS = 40        # Reducido para que quepa perfectamente en la pantalla de la consola
DENSIDAD = 0.80      # 35% de vehículos
SEMILLA = 55044
ITERACIONES = 100

VACIO = 0
COCHE = 1

# Iconos visuales
ICONO_COCHE = "🚗"
ICONO_VACIO = " . "

np.random.seed(SEMILLA)
carril = (np.random.rand(N_CELDAS) < DENSIDAD).astype(int)

def aplicar_regla_184(carril_actual):
    nuevo = np.zeros(N_CELDAS, dtype=int)
    for i in range(N_CELDAS):
        L = carril_actual[(i - 1) % N_CELDAS]
        C = carril_actual[i]
        R = carril_actual[(i + 1) % N_CELDAS]
        
        if C == COCHE and R == VACIO:
            nuevo[i] = VACIO
        elif C == VACIO and L == COCHE:
            nuevo[i] = COCHE
        elif C == COCHE and R == COCHE:
            nuevo[i] = COCHE
        else:
            nuevo[i] = VACIO
    return nuevo

# Bucle de animación
for t in range(ITERACIONES):
    # Limpia la consola en cada paso para generar el efecto de video fluido
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Construye la carretera convirtiendo los 1s en coches y los 0s en asfalto
    pista_visual = "".join([ICONO_COCHE if celda == COCHE else ICONO_VACIO for celda in carril])
    
    print("=" * 60)
    print(f" SIMULACIÓN DE TRÁFICO EN VIVO (REGLA 184) | Paso: {t}")
    print("=" * 60)
    print(pista_visual)
    print("=" * 60)
    print(f"Semilla Académica: {SEMILLA} | Densidad de carril: {DENSIDAD*100}%")
    
    # Avanza el estado físico
    carril = aplicar_regla_184(carril)
    
    # Control de velocidad de la animación (0.15 segundos por cuadro)
    time.sleep(0.15)
