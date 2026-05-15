import numpy as np
import matplotlib.pyplot as plt
import csv
import os

# =========================================================================
# 1. PARÁMETROS E IDENTIDAD (Ítem 3.2)
# =========================================================================
N_CELDAS = 200
ITERACIONES = 150
SEMILLA = 55044  # Semilla basada en la cédula de identidad

VACIO = 0
COCHE = 1

# =========================================================================
# 2. FUNCIONES MODULARES (Ítem 3.1)
# =========================================================================
def inicializar_carril(densidad):
    """Crea el estado inicial aleatorio basado en la densidad."""
    np.random.seed(SEMILLA)
    return (np.random.rand(N_CELDAS) < densidad).astype(int)

def aplicar_regla_184(carril):
    """Lógica micro-física: Movimiento local de vehículos."""
    nuevo = np.zeros(N_CELDAS, dtype=int)
    for i in range(N_CELDAS):
        L = carril[(i - 1) % N_CELDAS]
        C = carril[i]
        R = carril[(i + 1) % N_CELDAS]
        
        if C == COCHE and R == VACIO:
            nuevo[i] = VACIO
        elif C == VACIO and L == COCHE:
            nuevo[i] = COCHE
        elif C == COCHE and R == COCHE:
            nuevo[i] = COCHE
        else:
            nuevo[i] = VACIO
    return nuevo

def guardar_captura_momento(estado, escenario_id, t, ruta_carpeta):
    """Genera y guarda una evidencia fotográfica aislada dentro de su carpeta."""
    plt.figure(figsize=(15, 1.2))
    plt.imshow(estado.reshape(1, -1), cmap='binary', aspect='auto', interpolation='nearest')
    plt.title(f"Evidencia Fotográfica Escenario {escenario_id} - Tiempo t={t} (Semilla: {SEMILLA})")
    plt.axis('off')  # Remueve bordes y números de ejes para una captura limpia
    plt.savefig(os.path.join(ruta_carpeta, f"captura_{escenario_id}_t{t}.png"), bbox_inches='tight', dpi=150)
    plt.close()

# =========================================================================
# 3. EJECUCIÓN Y GENERACIÓN DE MÉTRICAS (Ítem 3.6 y 3.7)
# =========================================================================
escenarios = [
    {"id": "A", "densidad": 0.05, "nombre": "Muerte_Rapida"},
    {"id": "B", "densidad": 0.90, "nombre": "Caos_Congestion"},
    {"id": "C", "densidad": 0.50, "nombre": "Sensibilidad"}
]

# Momentos clave indispensables requeridos por la rúbrica
momentos_clave = [0, 5, 35, 75, 149]

# Crear una figura para mostrar los 3 mapas espacio-temporales juntos
fig, axes = plt.subplots(1, 3, figsize=(18, 8))
plt.subplots_adjust(bottom=0.2, wspace=0.3)

for idx, esc in enumerate(escenarios):
    print(f"Simulando Escenario {esc['id']}: {esc['nombre']}...")
    
    # Crear la carpeta específica para el escenario si no existe
    carpeta_destino = f"Evidencias_Escenario_{esc['id']}"
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Inicialización limpia de la matriz bidimensional
    historia = np.zeros((ITERACIONES, N_CELDAS))
    estado = inicializar_carril(esc['densidad'])
    historia[0] = estado.copy() # Asignación correcta a la primera fila
    
    # Registro en archivo CSV con las 4 columnas exactas de Excel
    csv_file = os.path.join(carpeta_destino, f"metricas_escenario_{esc['id']}.csv")
    tiempos, n_vacias, n_coches = [], [], []
    
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["SEMILLA_USADA", SEMILLA])  # Requisito indispensable de trazabilidad
        writer.writerow(["Tiempo (t)", "Celdas Totales", "Vacías", "Vehículos Activos"])
        
        for t in range(ITERACIONES):
            v = np.sum(estado == VACIO)
            c = np.sum(estado == COCHE)
            
            # Guardar captura fotográfica individual si corresponde al momento clave
            if t in momentos_clave:
                guardar_captura_momento(estado, esc['id'], t, carpeta_destino)
            
            # Registro de métricas estructuradas cada 5 pasos de tiempo
            if t % 5 == 0:
                writer.writerow([t, N_CELDAS, v, c])
                
            tiempos.append(t)
            n_vacias.append(v)
            n_coches.append(c)
            
            if t < ITERACIONES - 1:
                estado = aplicar_regla_184(estado)
                historia[t+1] = estado.copy()

    # Dibujar Visualización Espacio-Temporal en el panel compartido
    axes[idx].imshow(historia, cmap='binary', aspect='auto', interpolation='nearest')
    axes[idx].set_title(f"Escenario {esc['id']}\nDensidad: {esc['densidad']}")
    axes[idx].set_xlabel("Celdas (Espacio)")
    axes[idx].set_ylabel("Tiempo (t)")

    # Generar Gráfico de Población de Líneas dentro de su carpeta respectiva
    plt.figure(figsize=(8, 4))
    plt.plot(tiempos, n_vacias, label='Vacías', color='blue')
    plt.plot(tiempos, n_coches, label='Coches', color='red')
    plt.title(f"Población Escenario {esc['id']} - Semilla: {SEMILLA}")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Cantidad de Celdas")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(carpeta_destino, f"grafico_poblacion_{esc['id']}.png"))
    plt.close()

# Configurar y guardar la visualización final de los tres tableros juntos
plt.figure(fig.number)
plt.suptitle(f"Portafolio IA: Regla 184 - Josmary Pulgar (Semilla: {SEMILLA})", fontsize=16)
plt.savefig("visualizacion_espacial_unificada.png", dpi=300)

print("\n--- ¡PROCESO CONCLUIDO CON ÉXITO! ---")
print("Se han estructurado y guardado los siguientes componentes en tu directorio:")
print("📂 Evidencias_Escenario_A/ -> CSV (4 columnas de Excel), Gráfico de población y 5 Capturas PNG")
print("📂 Evidencias_Escenario_B/ -> CSV (4 columnas de Excel), Gráfico de población y 5 Capturas PNG")
print("📂 Evidencias_Escenario_C/ -> CSV (4 columnas de Excel), Gráfico de población y 5 Capturas PNG")
print("🖼️ 'visualizacion_espacial_unificada.png' guardada en la raíz para la portada de tu informe.")

plt.show()
