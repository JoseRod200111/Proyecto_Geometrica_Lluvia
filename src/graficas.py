from pathlib import Path
import time

import matplotlib.pyplot as plt

from datos import (
    cargar_datos,
    calcular_probabilidades_mensuales,
    MESES_PRINCIPALES,
)

from simulacion import simular_mes

from generadores import (
    generar_muestra_transformada_inversa,
    generar_muestra_lcg,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

CANTIDAD_SIMULACIONES = 10000
SEMILLA = 42

RUTA_PROYECTO = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

RUTA_GRAFICAS = (
    RUTA_PROYECTO
    / "resultados"
    / "graficas"
)

RUTA_GRAFICAS.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def guardar_grafica(nombre_archivo):
    """
    Guarda la gráfica actual en la carpeta
    resultados/graficas.
    """

    ruta = RUTA_GRAFICAS / nombre_archivo

    plt.tight_layout()

    plt.savefig(
        ruta,
        dpi=180,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Generada: "
        f"{ruta}"
    )


def frecuencias_agrupadas(
    valores,
    limite=8
):
    """
    Calcula frecuencias relativas para:

        X = 1
        X = 2
        ...
        X = limite
        X >= limite + 1

    Para limite=8:

        1, 2, ..., 8, 9+
    """

    conteos = [
        0
        for _ in range(limite + 1)
    ]

    for valor in valores:

        if valor <= limite:
            conteos[valor - 1] += 1

        else:
            conteos[limite] += 1

    total = len(valores)

    if total == 0:
        return [
            0.0
            for _ in conteos
        ]

    return [
        conteo / total
        for conteo in conteos
    ]


def probabilidades_teoricas(
    p,
    limite=8
):
    """
    Probabilidades de la distribución geométrica
    agrupadas como:

        X = 1,...,8
        X >= 9
    """

    probabilidades = []

    for x in range(
        1,
        limite + 1
    ):

        probabilidad = (
            ((1 - p) ** (x - 1))
            * p
        )

        probabilidades.append(
            probabilidad
        )

    # P(X >= limite + 1)
    probabilidad_cola = (
        (1 - p) ** limite
    )

    probabilidades.append(
        probabilidad_cola
    )

    return probabilidades


# ============================================================
# GRÁFICA 1
# PROBABILIDAD DE LLUVIA POR MES
# ============================================================

def grafica_probabilidad_mensual(
    datos
):

    resultados = (
        calcular_probabilidades_mensuales(
            datos
        )
    )

    nombres = []
    probabilidades = []

    for mes in range(1, 13):

        nombres.append(
            resultados[mes]["mes"]
        )

        probabilidades.append(
            resultados[mes]["p"]
        )

    plt.figure(
        figsize=(11, 6)
    )

    plt.bar(
        nombres,
        probabilidades
    )

    plt.title(
        "Probabilidad histórica de día lluvioso por mes"
    )

    plt.xlabel(
        "Mes"
    )

    plt.ylabel(
        "Probabilidad estimada p"
    )

    plt.ylim(
        0,
        1
    )

    plt.xticks(
        rotation=45,
        ha="right"
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    guardar_grafica(
        "01_probabilidad_lluvia_por_mes.png"
    )


# ============================================================
# GRÁFICAS 2, 3 Y 4
# DISTRIBUCIÓN HISTÓRICA VS MODELO
# ============================================================

def grafica_distribucion_mes(
    resultado,
    numero
):

    limite = 8

    categorias = [
        str(x)
        for x in range(1, limite + 1)
    ]

    categorias.append(
        "9+"
    )

    historica = frecuencias_agrupadas(
        resultado["intervalos_reales"],
        limite
    )

    inversa = frecuencias_agrupadas(
        resultado["muestra_inversa"],
        limite
    )

    lcg = frecuencias_agrupadas(
        resultado["muestra_lcg"],
        limite
    )

    teorica = probabilidades_teoricas(
        resultado["p"],
        limite
    )

    posiciones = list(
        range(len(categorias))
    )

    ancho = 0.2

    plt.figure(
        figsize=(11, 6)
    )

    plt.bar(
        [
            x - 1.5 * ancho
            for x in posiciones
        ],
        historica,
        width=ancho,
        label="Datos históricos"
    )

    plt.bar(
        [
            x - 0.5 * ancho
            for x in posiciones
        ],
        teorica,
        width=ancho,
        label="Geométrica teórica"
    )

    plt.bar(
        [
            x + 0.5 * ancho
            for x in posiciones
        ],
        inversa,
        width=ancho,
        label="Transformada inversa"
    )

    plt.bar(
        [
            x + 1.5 * ancho
            for x in posiciones
        ],
        lcg,
        width=ancho,
        label="LCG + ensayos"
    )

    plt.xticks(
        posiciones,
        categorias
    )

    plt.title(
        f"Distribución de intervalos - "
        f"{resultado['mes']}"
    )

    plt.xlabel(
        "Días hasta el siguiente día lluvioso (X)"
    )

    plt.ylabel(
        "Frecuencia relativa"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    nombre = (
        f"{numero:02d}_distribucion_"
        f"{resultado['mes'].lower()}.png"
    )

    guardar_grafica(
        nombre
    )


# ============================================================
# GRÁFICA 5
# COMPARACIÓN DE MEDIAS
# ============================================================

def grafica_medias(
    resultados
):

    meses = [
        resultado["mes"]
        for resultado in resultados
    ]

    historicas = [
        resultado["media_real"]
        for resultado in resultados
    ]

    teoricas = [
        resultado["media_teorica"]
        for resultado in resultados
    ]

    inversas = [
        resultado["media_inversa"]
        for resultado in resultados
    ]

    lcgs = [
        resultado["media_lcg"]
        for resultado in resultados
    ]

    posiciones = list(
        range(len(meses))
    )

    ancho = 0.2

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        [
            x - 1.5 * ancho
            for x in posiciones
        ],
        historicas,
        width=ancho,
        label="Datos históricos"
    )

    plt.bar(
        [
            x - 0.5 * ancho
            for x in posiciones
        ],
        teoricas,
        width=ancho,
        label="Teórica"
    )

    plt.bar(
        [
            x + 0.5 * ancho
            for x in posiciones
        ],
        inversas,
        width=ancho,
        label="Transformada inversa"
    )

    plt.bar(
        [
            x + 1.5 * ancho
            for x in posiciones
        ],
        lcgs,
        width=ancho,
        label="LCG + ensayos"
    )

    plt.xticks(
        posiciones,
        meses
    )

    plt.title(
        "Comparación de medias"
    )

    plt.ylabel(
        "Media de días"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    guardar_grafica(
        "05_comparacion_medias.png"
    )


# ============================================================
# GRÁFICA 6
# COMPARACIÓN DE VARIANZAS
# ============================================================

def grafica_varianzas(
    resultados
):

    meses = [
        resultado["mes"]
        for resultado in resultados
    ]

    historicas = [
        resultado["varianza_real"]
        for resultado in resultados
    ]

    teoricas = [
        resultado["varianza_teorica"]
        for resultado in resultados
    ]

    inversas = [
        resultado["varianza_inversa"]
        for resultado in resultados
    ]

    lcgs = [
        resultado["varianza_lcg"]
        for resultado in resultados
    ]

    posiciones = list(
        range(len(meses))
    )

    ancho = 0.2

    plt.figure(
        figsize=(10, 6)
    )

    plt.bar(
        [
            x - 1.5 * ancho
            for x in posiciones
        ],
        historicas,
        width=ancho,
        label="Datos históricos"
    )

    plt.bar(
        [
            x - 0.5 * ancho
            for x in posiciones
        ],
        teoricas,
        width=ancho,
        label="Teórica"
    )

    plt.bar(
        [
            x + 0.5 * ancho
            for x in posiciones
        ],
        inversas,
        width=ancho,
        label="Transformada inversa"
    )

    plt.bar(
        [
            x + 1.5 * ancho
            for x in posiciones
        ],
        lcgs,
        width=ancho,
        label="LCG + ensayos"
    )

    plt.xticks(
        posiciones,
        meses
    )

    plt.title(
        "Comparación de varianzas"
    )

    plt.ylabel(
        "Varianza"
    )

    plt.legend()

    plt.grid(
        axis="y",
        alpha=0.3
    )

    guardar_grafica(
        "06_comparacion_varianzas.png"
    )


# ============================================================
# GRÁFICA 7
# COMPARACIÓN DE TIEMPO DE EJECUCIÓN
# ============================================================

def grafica_rendimiento_metodos():
    """
    Compara únicamente el tiempo de ejecución de
    Transformada Inversa y LCG + ensayos.

    Se realizan 30 ejecuciones de 100000 observaciones
    para julio y se grafica el tiempo promedio de cada
    método.

    Los errores de media y varianza se reportan en las
    tablas y en el análisis estadístico, pero no se mezclan
    con los tiempos en esta gráfica porque representan
    magnitudes diferentes.
    """

    p = 183 / 341

    cantidad = 100000
    repeticiones = 30

    tiempos_inversa = []
    tiempos_lcg = []

    print()
    print(
        "Ejecutando comparación de rendimiento "
        "para la gráfica 07..."
    )

    for semilla in range(
        1,
        repeticiones + 1
    ):

        # ----------------------------------------------------
        # Transformada Inversa
        # ----------------------------------------------------

        inicio = time.perf_counter()

        generar_muestra_transformada_inversa(
            p=p,
            cantidad=cantidad,
            semilla=semilla
        )

        tiempo = (
            time.perf_counter()
            - inicio
        )

        tiempos_inversa.append(
            tiempo
        )

        # ----------------------------------------------------
        # LCG + ENSAYOS
        # ----------------------------------------------------

        inicio = time.perf_counter()

        generar_muestra_lcg(
            p=p,
            cantidad=cantidad,
            semilla=semilla
        )

        tiempo = (
            time.perf_counter()
            - inicio
        )

        tiempos_lcg.append(
            tiempo
        )

    # --------------------------------------------------------
    # Promedios
    # --------------------------------------------------------

    tiempo_inversa = (
        sum(tiempos_inversa)
        / len(tiempos_inversa)
    )

    tiempo_lcg = (
        sum(tiempos_lcg)
        / len(tiempos_lcg)
    )

    # ========================================================
    # GRÁFICA
    # ========================================================

    metodos = [
        "Transformada inversa",
        "LCG + ensayos",
    ]

    tiempos = [
        tiempo_inversa,
        tiempo_lcg,
    ]

    plt.figure(
        figsize=(8, 6)
    )

    barras = plt.bar(
        metodos,
        tiempos
    )

    plt.title(
        "Tiempo promedio de ejecución "
        "(30 ejecuciones)"
    )

    plt.ylabel(
        "Tiempo promedio (s)"
    )

    plt.grid(
        axis="y",
        alpha=0.3
    )

    for barra in barras:

        altura = barra.get_height()

        plt.text(
            barra.get_x()
            + barra.get_width() / 2,
            altura,
            f"{altura:.4f} s",
            ha="center",
            va="bottom"
        )

    guardar_grafica(
        "07_comparacion_rendimiento.png"
    )

    print()
    print(
        f"Tiempo promedio Inversa: "
        f"{tiempo_inversa:.6f} s"
    )

    print(
        f"Tiempo promedio LCG: "
        f"{tiempo_lcg:.6f} s"
    )

    print(
        f"LCG / Inversa: "
        f"{tiempo_lcg / tiempo_inversa:.2f} veces"
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def generar_todas_las_graficas():

    print("=" * 70)
    print("GENERACIÓN DE GRÁFICAS DEL PROYECTO")
    print("=" * 70)

    print()
    print(
        "Carpeta de salida:"
    )

    print(
        RUTA_GRAFICAS
    )

    # --------------------------------------------------------
    # Cargar datos
    # --------------------------------------------------------

    datos = cargar_datos()

    # --------------------------------------------------------
    # Gráfica mensual
    # --------------------------------------------------------

    grafica_probabilidad_mensual(
        datos
    )

    # --------------------------------------------------------
    # Ejecutar simulaciones
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Distribuciones individuales
    # --------------------------------------------------------

    for numero, resultado in enumerate(
        resultados,
        start=2
    ):

        grafica_distribucion_mes(
            resultado,
            numero
        )

    # --------------------------------------------------------
    # Comparaciones globales
    # --------------------------------------------------------

    grafica_medias(
        resultados
    )

    grafica_varianzas(
        resultados
    )

    grafica_rendimiento_metodos()

    print()
    print("=" * 70)
    print("GRÁFICAS GENERADAS CORRECTAMENTE")
    print("=" * 70)


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    generar_todas_las_graficas()