import numpy as np
import matplotlib.pyplot as plt

# =========================================================================
# 1. CONFIGURACIÓN DE IDENTIDAD Y REPRODUCIBILIDAD
# =========================================================================
CEDULA_SEED = 55044 

def configurar_entorno(semilla):
    np.random.seed(semilla)
    print(f"--- Simulación Iniciada ---")
    print(f"Semilla Aleatoria Activa (Cédula): {semilla}")

# =========================================================================
# 2. IMPLEMENTACIÓN DEL AUTÓMATA (Regla 184)
# =========================================================================

def inicializar_ca(n_celdas, densidad):
    return (np.random.rand(n_celdas) < densidad).astype(int)

def aplicar_regla_184(carril_actual):
    izq = np.roll(carril_actual, 1)  
    der = np.roll(carril_actual, -1) 
    nuevo_estado = ((izq == 1) & (carril_actual == 0)) | \
                   ((carril_actual == 1) & (der == 1))
    return nuevo_estado.astype(int)

def analizar_flujo(matriz):
    pasos = matriz.shape[0]
    n_celdas = matriz.shape[1]
    flujos = []
    for t in range(pasos - 1):
        movimientos = np.sum((matriz[t] == 1) & (matriz[t+1] == 0))
        flujos.append(movimientos / n_celdas)
    return flujos

# =========================================================================
# 3. VISUALIZACIÓN CORREGIDA (Sin solapamientos)
# =========================================================================

def ejecutar_simulacion_final(n_celdas=250, pasos=200, densidad=0.65):
    configurar_entorno(CEDULA_SEED)
    
    # Evolución del sistema
    historia = np.zeros((pasos, n_celdas))
    estado = inicializar_ca(n_celdas, densidad)
    historia[0] = estado
    for t in range(1, pasos):
        estado = aplicar_regla_184(estado)
        historia[t] = estado
        
    datos_flujo = analizar_flujo(historia)
    
    # --- SOLUCIÓN AL SOLAPAMIENTO DE TEXTO ---
    # Usamos un layout de 2 filas y 1 columna con GridSpec para control total
    fig = plt.figure(figsize=(12, 14))
    gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.4) # hspace añade el espacio necesario

    # Gráfico Superior: Simulación Espacio-Tiempo
    ax1 = fig.add_subplot(gs[0])
    img = ax1.imshow(historia, cmap='binary', interpolation='nearest', aspect='auto')
    ax1.set_title(f"Simulación de Tráfico - Regla 184 (Densidad: {densidad})", fontsize=16, pad=20)
    ax1.set_ylabel("Tiempo (Pasos)", fontsize=12)
    ax1.set_xlabel("Posición en el Carril (Celdas)", fontsize=12)
    
    # Barra de color integrada correctamente
    cbar = fig.colorbar(img, ax=ax1, ticks=[0, 1], shrink=0.7, pad=0.02)
    cbar.ax.set_yticklabels(['Vacío (0)', 'Coche (1)'])

    # Gráfico Inferior: Cuantificación de Flujo
    ax2 = fig.add_subplot(gs[1])
    ax2.plot(datos_flujo, color='blue', linewidth=2, label='Flujo Instantáneo')
    media = np.mean(datos_flujo)
    ax2.axhline(y=media, color='red', linestyle='--', label=f'Media: {media:.2f}')
    
    ax2.set_title("Análisis Numérico: Convergencia del Flujo Vehicular", fontsize=16, pad=15)
    ax2.set_ylabel("Flujo (Coches/Celda)", fontsize=12)
    ax2.set_xlabel("Paso de Tiempo", fontsize=12)
    ax2.legend(loc='lower right')
    ax2.grid(True, linestyle=':', alpha=0.6)

    # Ajuste final automático de márgenes internos
    plt.tight_layout()
    
    # Guardado de alta calidad
    plt.savefig("simulacion_limpia.png", dpi=300, bbox_inches='tight')
    print("Archivo 'simulacion_limpia.png' generado sin solapamientos.")
    
    plt.show()

if __name__ == "__main__":
    ejecutar_simulacion_final()