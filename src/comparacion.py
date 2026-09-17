import time
from statistics import mean

from generadores import (
    generar_muestra_transformada_inversa,
    generar_muestra_lcg,
    calcular_media,
    calcular_varianza,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

CANTIDAD_OBSERVACIONES = 100000
CANTIDAD_REPETICIONES = 30

# Utilizamos julio por ser el escenario con mayor
# variabilidad entre los tres meses principales.
P = 183 / 341


# ============================================================
# EJECUCIÓN DE UN MÉTODO
# ============================================================

def ejecutar_prueba(
    generador,
    p,
    cantidad,
    semilla
):
    """
    Ejecuta un método de generación y obtiene:

    - tiempo de ejecución
    - media
    - varianza
    """

    inicio = time.perf_counter()

    muestra = generador(
        p=p,
        cantidad=cantidad,
        semilla=semilla
    )

    tiempo = (
        time.perf_counter()
        - inicio
    )

    media_muestra = calcular_media(
        muestra
    )

    varianza_muestra = calcular_varianza(
        muestra
    )

    return {
        "tiempo": tiempo,
        "media": media_muestra,
        "varianza": varianza_muestra,
    }


# ============================================================
# COMPARACIÓN DE MÉTODOS
# ============================================================

def comparar_metodos():

    media_teorica = 1 / P

    varianza_teorica = (
        (1 - P)
        /
        (P ** 2)
    )

    resultados_inversa = []
    resultados_lcg = []

    print("=" * 78)
    print("COMPARACIÓN DE MÉTODOS DE GENERACIÓN")
    print("TRANSFORMADA INVERSA VS LCG")
    print("=" * 78)

    print()
    print("CONFIGURACIÓN")
    print("-" * 78)

    print(
        f"Probabilidad p: "
        f"{P:.6f}"
    )

    print(
        f"Observaciones por ejecución: "
        f"{CANTIDAD_OBSERVACIONES}"
    )

    print(
        f"Número de repeticiones: "
        f"{CANTIDAD_REPETICIONES}"
    )

    print()
    print("VALORES TEÓRICOS")
    print("-" * 78)

    print(
        f"Media teórica: "
        f"{media_teorica:.6f}"
    )

    print(
        f"Varianza teórica: "
        f"{varianza_teorica:.6f}"
    )

    # ========================================================
    # REPETICIONES
    # ========================================================

    for semilla in range(
        1,
        CANTIDAD_REPETICIONES + 1
    ):

        resultado_inversa = ejecutar_prueba(
            generar_muestra_transformada_inversa,
            P,
            CANTIDAD_OBSERVACIONES,
            semilla
        )

        resultado_lcg = ejecutar_prueba(
            generar_muestra_lcg,
            P,
            CANTIDAD_OBSERVACIONES,
            semilla
        )

        resultados_inversa.append(
            resultado_inversa
        )

        resultados_lcg.append(
            resultado_lcg
        )

    # ========================================================
    # MÉTRICAS AGREGADAS
    # ========================================================

    tiempos_inversa = [
        resultado["tiempo"]
        for resultado in resultados_inversa
    ]

    tiempos_lcg = [
        resultado["tiempo"]
        for resultado in resultados_lcg
    ]

    errores_media_inversa = [
        abs(
            resultado["media"]
            - media_teorica
        )
        for resultado in resultados_inversa
    ]

    errores_media_lcg = [
        abs(
            resultado["media"]
            - media_teorica
        )
        for resultado in resultados_lcg
    ]

    errores_varianza_inversa = [
        abs(
            resultado["varianza"]
            - varianza_teorica
        )
        for resultado in resultados_inversa
    ]

    errores_varianza_lcg = [
        abs(
            resultado["varianza"]
            - varianza_teorica
        )
        for resultado in resultados_lcg
    ]

    # ========================================================
    # RESULTADOS
    # ========================================================

    print()
    print("=" * 78)
    print("RESULTADOS PROMEDIO DE LAS REPETICIONES")
    print("=" * 78)

    print()
    print(
        f"{'Métrica':<32}"
        f"{'Inversa':>20}"
        f"{'LCG':>20}"
    )

    print("-" * 72)

    print(
        f"{'Tiempo promedio (s)':<32}"
        f"{mean(tiempos_inversa):>20.6f}"
        f"{mean(tiempos_lcg):>20.6f}"
    )

    print(
        f"{'Error promedio media':<32}"
        f"{mean(errores_media_inversa):>20.6f}"
        f"{mean(errores_media_lcg):>20.6f}"
    )

    print(
        f"{'Error promedio varianza':<32}"
        f"{mean(errores_varianza_inversa):>20.6f}"
        f"{mean(errores_varianza_lcg):>20.6f}"
    )

    # ========================================================
    # VALORES MÍNIMOS Y MÁXIMOS
    # ========================================================

    print()
    print("=" * 78)
    print("VARIACIÓN ENTRE EJECUCIONES")
    print("=" * 78)

    print()
    print("TRANSFORMADA INVERSA")
    print("-" * 78)

    print(
        f"Tiempo mínimo: "
        f"{min(tiempos_inversa):.6f} s"
    )

    print(
        f"Tiempo máximo: "
        f"{max(tiempos_inversa):.6f} s"
    )

    print(
        f"Error mínimo de media: "
        f"{min(errores_media_inversa):.6f}"
    )

    print(
        f"Error máximo de media: "
        f"{max(errores_media_inversa):.6f}"
    )

    print()
    print("LCG + ENSAYOS")
    print("-" * 78)

    print(
        f"Tiempo mínimo: "
        f"{min(tiempos_lcg):.6f} s"
    )

    print(
        f"Tiempo máximo: "
        f"{max(tiempos_lcg):.6f} s"
    )

    print(
        f"Error mínimo de media: "
        f"{min(errores_media_lcg):.6f}"
    )

    print(
        f"Error máximo de media: "
        f"{max(errores_media_lcg):.6f}"
    )

    # ========================================================
    # DIFERENCIA DE VELOCIDAD
    # ========================================================

    tiempo_promedio_inversa = mean(
        tiempos_inversa
    )

    tiempo_promedio_lcg = mean(
        tiempos_lcg
    )

    relacion_tiempo = (
        tiempo_promedio_lcg
        /
        tiempo_promedio_inversa
    )

    print()
    print("=" * 78)
    print("COMPARACIÓN DE RENDIMIENTO")
    print("=" * 78)

    print()

    print(
        f"LCG tarda aproximadamente "
        f"{relacion_tiempo:.2f} veces "
        f"el tiempo de Transformada Inversa."
    )

    print()
    print("=" * 78)
    print("COMPARACIÓN FINALIZADA")
    print("=" * 78)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    comparar_metodos()