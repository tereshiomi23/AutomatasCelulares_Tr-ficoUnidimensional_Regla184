import numpy as np
import matplotlib.pyplot as plt

def simular_trafico(n_celdas=100, pasos=100, densidad=0.4):
    # Inicialización del carril con la densidad de coches especificada
    # 1 representa un "coche", 0 representa un espacio "vacío"
    carril = (np.random.rand(n_celdas) < densidad).astype(int)
    
    # Matriz para registrar la evolución temporal
    historial = np.zeros((pasos, n_celdas))
    historial[0] = carril

    for t in range(1, pasos):
        nuevo_carril = np.zeros(n_celdas, dtype=int)
        for i in range(n_celdas):
            # Identificamos el estado de la celda actual y sus vecinas
            # Se usan condiciones periódicas (anillo) para conservar la densidad
            actual = carril[i]
            atras = carril[(i - 1) % n_celdas]
            adelante = carril[(i + 1) % n_celdas]
            
            # Aplicación de la Regla 184:
            # Un coche se mueve si la celda de adelante está vacía (image_1e7836.png)
            if actual == 1:
                if adelante == 0:
                    nuevo_carril[i] = 0  # El coche avanza, deja la celda vacía
                else:
                    nuevo_carril[i] = 1  # Bloqueado por el coche de adelante
            else: # Si la celda actual está vacía (0)
                if atras == 1:
                    nuevo_carril[i] = 1  # El coche de atrás entra en esta celda
                else:
                    nuevo_carril[i] = 0  # Sigue vacía
        
        carril = nuevo_carril
        historial[t] = carril
        
    return historial

# Ejecución y Visualización
resultados = simular_trafico(densidad=0.6) # Densidad alta para ver atascos

plt.figure(figsize=(12, 8))
plt.imshow(resultados, cmap='binary', interpolation='nearest')
plt.title("Simulación de Flujo de Coches (Regla 184)")
plt.xlabel("Posición en el carril")
plt.ylabel("Tiempo (Pasos)")
plt.show()