import csv
from datetime import datetime
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

UMBRAL_LLUVIA_MM = 1.0

# Ruta del proyecto:
# Proyecto_Geometrica_Lluvia/
# ├── data/
# └── src/
RUTA_PROYECTO = Path(__file__).resolve().parent.parent

RUTA_CSV = (
    RUTA_PROYECTO
    / "data"
    / "raw"
    / "precipitacion_guatemala_2015_2025.csv"
)

MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}

MESES_PRINCIPALES = [6, 7, 9]


# ============================================================
# LECTURA DEL CSV
# ============================================================

def cargar_datos(ruta_csv=RUTA_CSV):
    """
    Lee el CSV descargado de Open-Meteo.

    Retorna una lista de diccionarios con:
        fecha
        precipitacion
        lluvioso
    """

    datos = []

    if not ruta_csv.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo:\n{ruta_csv}"
        )

    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        # El archivo de Open-Meteo contiene:
        #
        # línea 1: nombres de metadatos
        # línea 2: valores de metadatos
        # línea 3: línea vacía
        # línea 4: encabezado real de datos

        next(archivo)
        next(archivo)
        next(archivo)

        lector = csv.DictReader(archivo)

        for fila in lector:
            fecha = datetime.strptime(
                fila["time"],
                "%Y-%m-%d"
            ).date()

            precipitacion = float(
                fila["precipitation_sum (mm)"]
            )

            lluvioso = precipitacion >= UMBRAL_LLUVIA_MM

            datos.append(
                {
                    "fecha": fecha,
                    "precipitacion": precipitacion,
                    "lluvioso": lluvioso,
                }
            )

    return datos


# ============================================================
# PROBABILIDAD DE LLUVIA
# ============================================================

def calcular_probabilidad_mes(datos, mes):
    """
    Calcula:

        p = días lluviosos / total de días

    para un mes específico utilizando todos los años disponibles.
    """

    registros_mes = [
        registro
        for registro in datos
        if registro["fecha"].month == mes
    ]

    total_dias = len(registros_mes)

    dias_lluviosos = sum(
        1
        for registro in registros_mes
        if registro["lluvioso"]
    )

    if total_dias == 0:
        return 0.0, 0, 0

    p = dias_lluviosos / total_dias

    return p, dias_lluviosos, total_dias


def calcular_probabilidades_mensuales(datos):
    """
    Calcula p para los 12 meses.

    Retorna un diccionario:
        mes -> datos estadísticos
    """

    resultados = {}

    for mes in range(1, 13):
        p, lluviosos, total = calcular_probabilidad_mes(
            datos,
            mes
        )

        resultados[mes] = {
            "mes": MESES[mes],
            "p": p,
            "dias_lluviosos": lluviosos,
            "total_dias": total,
        }

    return resultados


# ============================================================
# INTERVALOS ENTRE DÍAS LLUVIOSOS
# ============================================================

def obtener_intervalos_mes(datos, mes):
    """
    Obtiene los intervalos X entre días lluviosos.

    IMPORTANTE:
    Los intervalos solamente se calculan dentro del mismo
    mes y del mismo año.

    Ejemplo:

        3 de julio  -> lluvia
        6 de julio  -> lluvia

        X = 3

    No se calcula un intervalo entre:
        31 de julio -> 1 de agosto
    """

    intervalos = []

    # Obtener los años presentes en los datos
    anios = sorted(
        set(
            registro["fecha"].year
            for registro in datos
        )
    )

    for anio in anios:

        fechas_lluviosas = [
            registro["fecha"]
            for registro in datos
            if (
                registro["fecha"].year == anio
                and registro["fecha"].month == mes
                and registro["lluvioso"]
            )
        ]

        fechas_lluviosas.sort()

        for i in range(1, len(fechas_lluviosas)):

            fecha_anterior = fechas_lluviosas[i - 1]
            fecha_actual = fechas_lluviosas[i]

            diferencia = (
                fecha_actual - fecha_anterior
            ).days

            intervalos.append(diferencia)

    return intervalos


# ============================================================
# ESTADÍSTICAS BÁSICAS
# ============================================================

def calcular_media(valores):
    if not valores:
        return 0.0

    return sum(valores) / len(valores)


def calcular_varianza(valores):
    """
    Varianza poblacional.
    """

    if not valores:
        return 0.0

    media = calcular_media(valores)

    suma = sum(
        (valor - media) ** 2
        for valor in valores
    )

    return suma / len(valores)


def obtener_frecuencias(valores):
    """
    Cuenta cuántas veces aparece cada valor.

    Ejemplo:
        [1, 1, 1, 2, 3]

    retorna:
        {
            1: 3,
            2: 1,
            3: 1
        }
    """

    frecuencias = {}

    for valor in valores:
        frecuencias[valor] = (
            frecuencias.get(valor, 0) + 1
        )

    return dict(
        sorted(frecuencias.items())
    )


# ============================================================
# RESUMEN DE UN MES
# ============================================================

def obtener_resumen_mes(datos, mes):

    p, dias_lluviosos, total_dias = (
        calcular_probabilidad_mes(
            datos,
            mes
        )
    )

    intervalos = obtener_intervalos_mes(
        datos,
        mes
    )

    media_real = calcular_media(intervalos)
    varianza_real = calcular_varianza(intervalos)

    if p > 0:
        media_teorica = 1 / p

        varianza_teorica = (
            (1 - p) / (p ** 2)
        )
    else:
        media_teorica = 0.0
        varianza_teorica = 0.0

    return {
        "mes": MESES[mes],
        "numero_mes": mes,
        "p": p,
        "dias_lluviosos": dias_lluviosos,
        "total_dias": total_dias,
        "intervalos": intervalos,
        "cantidad_intervalos": len(intervalos),
        "media_real": media_real,
        "varianza_real": varianza_real,
        "media_teorica": media_teorica,
        "varianza_teorica": varianza_teorica,
        "frecuencias": obtener_frecuencias(
            intervalos
        ),
    }


# ============================================================
# IMPRESIÓN DE RESULTADOS
# ============================================================

def imprimir_probabilidades_mensuales(datos):

    print()
    print("=" * 70)
    print("PROBABILIDAD DE DÍA LLUVIOSO POR MES")
    print("=" * 70)

    resultados = calcular_probabilidades_mensuales(
        datos
    )

    for mes in range(1, 13):
        resultado = resultados[mes]

        print(
            f"{resultado['mes']:<12} | "
            f"{resultado['dias_lluviosos']:>3}/"
            f"{resultado['total_dias']:<3} días | "
            f"p = {resultado['p']:.4f}"
        )


def imprimir_resumen_mes(datos, mes):

    resumen = obtener_resumen_mes(
        datos,
        mes
    )

    print()
    print("=" * 70)
    print(
        f"RESUMEN: {resumen['mes'].upper()}"
    )
    print("=" * 70)

    print(
        f"Días analizados: "
        f"{resumen['total_dias']}"
    )

    print(
        f"Días lluviosos: "
        f"{resumen['dias_lluviosos']}"
    )

    print(
        f"Probabilidad p: "
        f"{resumen['p']:.6f}"
    )

    print(
        f"Intervalos observados: "
        f"{resumen['cantidad_intervalos']}"
    )

    print()
    print("VALORES REALES")
    print("-" * 70)

    print(
        f"Media real: "
        f"{resumen['media_real']:.6f}"
    )

    print(
        f"Varianza real: "
        f"{resumen['varianza_real']:.6f}"
    )

    print()
    print("VALORES GEOMÉTRICOS TEÓRICOS")
    print("-" * 70)

    print(
        f"E[X] = 1/p: "
        f"{resumen['media_teorica']:.6f}"
    )

    print(
        f"Var(X) = (1-p)/p²: "
        f"{resumen['varianza_teorica']:.6f}"
    )

    print()
    print("FRECUENCIAS DE INTERVALOS")
    print("-" * 70)

    for intervalo, cantidad in (
        resumen["frecuencias"].items()
    ):
        print(
            f"X = {intervalo:<2} -> "
            f"{cantidad} casos"
        )


# ============================================================
# PRUEBA DEL MÓDULO
# ============================================================

def main():

    print("=" * 70)
    print("ANÁLISIS DE DATOS HISTÓRICOS DE PRECIPITACIÓN")
    print("CIUDAD DE GUATEMALA - 2015 A 2025")
    print("=" * 70)

    print()
    print(f"Archivo:")
    print(RUTA_CSV)

    print()
    print(
        f"Umbral de día lluvioso: "
        f"{UMBRAL_LLUVIA_MM:.1f} mm"
    )

    datos = cargar_datos()

    print()
    print(
        f"Registros cargados: "
        f"{len(datos)}"
    )

    if datos:
        print(
            f"Primera fecha: "
            f"{datos[0]['fecha']}"
        )

        print(
            f"Última fecha: "
            f"{datos[-1]['fecha']}"
        )

    imprimir_probabilidades_mensuales(
        datos
    )

    for mes in MESES_PRINCIPALES:
        imprimir_resumen_mes(
            datos,
            mes
        )

    print()
    print("=" * 70)
    print("ANÁLISIS FINALIZADO")
    print("=" * 70)


if __name__ == "__main__":
    main()