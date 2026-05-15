import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros del simulador interactivo
N_CELDAS = 100       # Reducido a 100 para que los coches se vean más grandes y claros
DENSIDAD = 0.40      # 40% de tráfico: ideal para ver movimiento y atascos locales
SEMILLA = 55044      # Tu semilla académica
VACIO = 0
COCHE = 1

# Inicialización del carril
np.random.seed(SEMILLA)
carril = (np.random.rand(N_CELDAS) < DENSIDAD).astype(int)

# Configuración de la ventana gráfica
fig, ax = plt.subplots(figsize=(12, 2))
# Inicializamos el carril visualmente (matriz 1xN)
im = ax.imshow(carril.reshape(1, -1), cmap='binary', aspect='auto', interpolation='nearest')
ax.axis('off')

def aplicar_regla_184(carril_actual):
    """Aplica la micro-física de la Regla 184."""
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

def actualizar(frame):
    """Función que refresca la pantalla en cada cuadro del video."""
    global carril
    carril = aplicar_regla_184(carril)
    im.set_array(carril.reshape(1, -1))
    ax.set_title(f"Simulación de Tráfico en Vivo (Regla 184) - Paso: {frame} | Semilla: {SEMILLA}")
    return [im]

# Crear la animación: cambia cada 100 milisegundos (0.1 segundos)
ani = animation.FuncAnimation(fig, actualizar, frames=200, interval=100, blit=True)

print("Abriendo ventana interactiva... Mira tu barra de tareas.")
plt.show()
