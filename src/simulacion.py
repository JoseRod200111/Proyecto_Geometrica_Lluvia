from datos import (
    cargar_datos,
    obtener_resumen_mes,
    MESES_PRINCIPALES,
)

from generadores import (
    generar_muestra_transformada_inversa,
    generar_muestra_lcg,
    calcular_media,
    calcular_varianza,
    obtener_frecuencias,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

CANTIDAD_SIMULACIONES = 10000
SEMILLA = 42


# ============================================================
# DISTANCIA ENTRE DISTRIBUCIONES
# ============================================================

def calcular_error_frecuencias(
    reales,
    simulados
):
    """
    Calcula el error absoluto medio entre:

        frecuencia empírica real
        frecuencia simulada

    para todos los valores X observados.

    Las frecuencias se comparan como proporciones.
    """

    frecuencias_reales = obtener_frecuencias(
        reales
    )

    frecuencias_simuladas = obtener_frecuencias(
        simulados
    )

    valores = sorted(
        set(frecuencias_reales.keys())
        |
        set(frecuencias_simuladas.keys())
    )

    total_real = len(reales)
    total_simulado = len(simulados)

    errores = []

    for x in valores:

        prob_real = (
            frecuencias_reales.get(x, 0)
            / total_real
        )

        prob_simulada = (
            frecuencias_simuladas.get(x, 0)
            / total_simulado
        )

        errores.append(
            abs(
                prob_real
                - prob_simulada
            )
        )

    if not errores:
        return 0.0

    return sum(errores) / len(errores)


# ============================================================
# SIMULACIÓN DE UN MES
# ============================================================

def simular_mes(
    datos,
    mes,
    cantidad=CANTIDAD_SIMULACIONES,
    semilla=SEMILLA
):
    """
    Ejecuta ambos métodos para un mes específico
    utilizando el p estimado con los datos reales.
    """

    resumen_real = obtener_resumen_mes(
        datos,
        mes
    )

    p = resumen_real["p"]

    intervalos_reales = (
        resumen_real["intervalos"]
    )

    # --------------------------------------------------------
    # Método 1:
    # Transformada Inversa
    # --------------------------------------------------------

    muestra_inversa = (
        generar_muestra_transformada_inversa(
            p=p,
            cantidad=cantidad,
            semilla=semilla
        )
    )

    # --------------------------------------------------------
    # Método 2:
    # LCG + ensayos
    # --------------------------------------------------------

    muestra_lcg = generar_muestra_lcg(
        p=p,
        cantidad=cantidad,
        semilla=semilla
    )

    # --------------------------------------------------------
    # Estadísticas
    # --------------------------------------------------------

    resultado = {

        "mes": resumen_real["mes"],

        "numero_mes": mes,

        "p": p,

        "cantidad_real": (
            len(intervalos_reales)
        ),

        "cantidad_simulada": cantidad,

        # Datos reales
        "media_real": (
            resumen_real["media_real"]
        ),

        "varianza_real": (
            resumen_real["varianza_real"]
        ),

        # Valores teóricos
        "media_teorica": (
            resumen_real["media_teorica"]
        ),

        "varianza_teorica": (
            resumen_real["varianza_teorica"]
        ),

        # Transformada inversa
        "media_inversa": calcular_media(
            muestra_inversa
        ),

        "varianza_inversa": calcular_varianza(
            muestra_inversa
        ),

        "error_frecuencias_inversa":
            calcular_error_frecuencias(
                intervalos_reales,
                muestra_inversa
            ),

        # LCG
        "media_lcg": calcular_media(
            muestra_lcg
        ),

        "varianza_lcg": calcular_varianza(
            muestra_lcg
        ),

        "error_frecuencias_lcg":
            calcular_error_frecuencias(
                intervalos_reales,
                muestra_lcg
            ),

        # Guardamos muestras para uso posterior
        "intervalos_reales":
            intervalos_reales,

        "muestra_inversa":
            muestra_inversa,

        "muestra_lcg":
            muestra_lcg,
    }

    return resultado


# ============================================================
# IMPRESIÓN DE RESULTADOS
# ============================================================

def imprimir_resultado(resultado):

    print()
    print("=" * 78)
    print(
        f"SIMULACIÓN: "
        f"{resultado['mes'].upper()}"
    )
    print("=" * 78)

    print()
    print("PARÁMETROS")
    print("-" * 78)

    print(
        f"p estimada: "
        f"{resultado['p']:.6f}"
    )

    print(
        f"Intervalos reales: "
        f"{resultado['cantidad_real']}"
    )

    print(
        f"Intervalos simulados por método: "
        f"{resultado['cantidad_simulada']}"
    )

    print()
    print("MEDIA")
    print("-" * 78)

    print(
        f"{'Real':<28}"
        f"{resultado['media_real']:>12.6f}"
    )

    print(
        f"{'Geométrica teórica':<28}"
        f"{resultado['media_teorica']:>12.6f}"
    )

    print(
        f"{'Transformada inversa':<28}"
        f"{resultado['media_inversa']:>12.6f}"
    )

    print(
        f"{'LCG + ensayos':<28}"
        f"{resultado['media_lcg']:>12.6f}"
    )

    print()
    print("VARIANZA")
    print("-" * 78)

    print(
        f"{'Real':<28}"
        f"{resultado['varianza_real']:>12.6f}"
    )

    print(
        f"{'Geométrica teórica':<28}"
        f"{resultado['varianza_teorica']:>12.6f}"
    )

    print(
        f"{'Transformada inversa':<28}"
        f"{resultado['varianza_inversa']:>12.6f}"
    )

    print(
        f"{'LCG + ensayos':<28}"
        f"{resultado['varianza_lcg']:>12.6f}"
    )

    print()
    print("ERROR DE DISTRIBUCIÓN CONTRA DATOS REALES")
    print("-" * 78)

    print(
        f"Transformada inversa: "
        f"{resultado['error_frecuencias_inversa']:.6f}"
    )

    print(
        f"LCG + ensayos:        "
        f"{resultado['error_frecuencias_lcg']:.6f}"
    )


# ============================================================
# SIMULACIÓN COMPLETA
# ============================================================

def ejecutar_simulacion():

    print("=" * 78)
    print("SIMULACIÓN DE INTERVALOS ENTRE DÍAS LLUVIOSOS")
    print("CIUDAD DE GUATEMALA - DATOS 2015 A 2025")
    print("=" * 78)

    datos = cargar_datos()

    resultados = []

    for mes in MESES_PRINCIPALES:

        resultado = simular_mes(
            datos=datos,
            mes=mes,
            cantidad=CANTIDAD_SIMULACIONES,
            semilla=SEMILLA
        )

        resultados.append(
            resultado
        )

        imprimir_resultado(
            resultado
        )

    # --------------------------------------------------------
    # Resumen global
    # --------------------------------------------------------

    print()
    print("=" * 78)
    print("RESUMEN DE LOS TRES MESES")
    print("=" * 78)

    print(
        f"{'Mes':<14}"
        f"{'p':>10}"
        f"{'Real':>12}"
        f"{'Inversa':>12}"
        f"{'LCG':>12}"
    )

    for resultado in resultados:

        print(
            f"{resultado['mes']:<14}"
            f"{resultado['p']:>10.4f}"
            f"{resultado['media_real']:>12.4f}"
            f"{resultado['media_inversa']:>12.4f}"
            f"{resultado['media_lcg']:>12.4f}"
        )

    print()
    print("=" * 78)
    print("SIMULACIÓN FINALIZADA")
    print("=" * 78)

    return resultados


# ============================================================
# EJECUCIÓN DIRECTA
# ============================================================

if __name__ == "__main__":
    ejecutar_simulacion()