

import numpy as np
import matplotlib.pyplot as plt

def simulacion_regla_184(celdas=50, pasos=30, densidad=0.4):
    # 1. Inicialización
    carril = (np.random.rand(celdas) < densidad).astype(int)
    historia = np.zeros((pasos, celdas))
    historia[0] = carril

    # 2. Evolución temporal
    for t in range(1, pasos):
        nuevo_carril = np.zeros(celdas, dtype=int)
        for i in range(celdas):
            # Lógica local: Un 1 se mueve si el frente (i+1) es 0
            # Se usa % celdas para el carril circular
            actual = carril[i]
            atras = carril[(i - 1) % celdas]
            adelante = carril[(i + 1) % celdas]
            
            if actual == 1:
                # Si hay coche y adelante está vacío, se mueve (deja un 0)
                nuevo_carril[i] = 1 if adelante == 1 else 0
            else:
                # Si está vacío y atrás viene un coche, lo recibe (se vuelve 1)
                nuevo_carril[i] = 1 if atras == 1 else 0
        
        carril = nuevo_carril
        historia[t] = carril
        
    return historia

# --- EJECUCIÓN Y SALIDA ---
data = simulacion_regla_184(densidad=0.6)

# Opción 1: Imprimir en consola (para verificar datos crudos)
print("Matriz de tráfico (1=Coche, 0=Vacío):")
print(data.astype(int))

# Opción 2: Gráfica interactiva
plt.figure(figsize=(10, 6))
plt.imshow(data, cmap='binary', interpolation='nearest')
plt.title("Flujo de Tráfico - Regla 184")
plt.xlabel("Posición (Carril)")
plt.ylabel("Tiempo (Pasos)")
plt.grid(False)
plt.show(block=True)  # 'block=True' fuerza a la ventana a quedarse abierta