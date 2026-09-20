import math
import random
import time


# ============================================================
# GENERADOR CONGRUENCIAL LINEAL (LCG)
# ============================================================

class LCG:
    """
    Generador congruencial lineal propio.

    Fórmula:

        X_(n+1) = (a * X_n + c) mod m

    Luego se transforma el valor entero a:

        U = X_n / m

    para obtener un número pseudoaleatorio en [0, 1).
    """

    def __init__(
        self,
        semilla=42,
        a=1664525,
        c=1013904223,
        m=2**32
    ):
        self.estado = semilla
        self.a = a
        self.c = c
        self.m = m

    def random(self):
        """
        Retorna un número pseudoaleatorio uniforme
        en el intervalo [0, 1).
        """

        self.estado = (
            self.a * self.estado + self.c
        ) % self.m

        return self.estado / self.m


# ============================================================
# MÉTODO 1:
# GEOMÉTRICA POR TRANSFORMADA INVERSA
# ============================================================

def geometrica_transformada_inversa(p, rng):
    """
    Genera:

        X ~ Geométrica(p)

    mediante Transformada Inversa.

    X representa el número de días hasta
    el primer día lluvioso.

    Fórmula:

        X = floor(
                ln(1 - U)
                /
                ln(1 - p)
            ) + 1

    con U en [0, 1).
    """

    if p <= 0 or p > 1:
        raise ValueError(
            "La probabilidad p debe cumplir 0 < p <= 1."
        )

    if p == 1:
        return 1

    u = rng.random()

    x = (
        math.floor(
            math.log(1 - u)
            /
            math.log(1 - p)
        )
        + 1
    )

    return x


def generar_muestra_transformada_inversa(
    p,
    cantidad,
    semilla=42
):
    """
    Genera una muestra geométrica utilizando
    Transformada Inversa.

    Para este método se utiliza el generador
    pseudoaleatorio estándar de Python.
    """

    rng = random.Random(semilla)

    muestra = []

    for _ in range(cantidad):

        x = geometrica_transformada_inversa(
            p,
            rng
        )

        muestra.append(x)

    return muestra


# ============================================================
# MÉTODO 2:
# LCG + ENSAYOS DIARIOS
# ============================================================

def geometrica_lcg(p, lcg):
    """
    Genera:

        X ~ Geométrica(p)

    utilizando un LCG propio.

    Se simula cada día individualmente:

        U < p     -> lluvia
        U >= p    -> no lluvia

    El proceso termina al obtener el primer
    día lluvioso.

    Retorna el número de días necesarios.
    """

    if p <= 0 or p > 1:
        raise ValueError(
            "La probabilidad p debe cumplir 0 < p <= 1."
        )

    intentos = 1

    while True:

        u = lcg.random()

        if u < p:
            return intentos

        intentos += 1


def generar_muestra_lcg(
    p,
    cantidad,
    semilla=42
):
    """
    Genera una muestra geométrica mediante
    LCG + ensayos sucesivos.
    """

    lcg = LCG(
        semilla=semilla
    )

    muestra = []

    for _ in range(cantidad):

        x = geometrica_lcg(
            p,
            lcg
        )

        muestra.append(x)

    return muestra


# ============================================================
# ESTADÍSTICAS AUXILIARES
# ============================================================

def calcular_media(valores):

    if not valores:
        return 0.0

    return sum(valores) / len(valores)


def calcular_varianza(valores):

    if not valores:
        return 0.0

    media = calcular_media(
        valores
    )

    suma = sum(
        (valor - media) ** 2
        for valor in valores
    )

    return suma / len(valores)


def obtener_frecuencias(valores):

    frecuencias = {}

    for valor in valores:

        frecuencias[valor] = (
            frecuencias.get(valor, 0) + 1
        )

    return dict(
        sorted(frecuencias.items())
    )


# ============================================================
# PRUEBA DE LOS DOS MÉTODOS
# ============================================================

def main():

    print("=" * 70)
    print("GENERACIÓN DE VARIABLES GEOMÉTRICAS")
    print("TRANSFORMADA INVERSA VS LCG")
    print("=" * 70)

    # Julio
    p = 183 / 341

    cantidad = 10000
    semilla = 42

    # --------------------------------------------------------
    # Valores teóricos
    # --------------------------------------------------------

    media_teorica = 1 / p

    varianza_teorica = (
        (1 - p)
        /
        (p ** 2)
    )

    print()
    print("PARÁMETROS")
    print("-" * 70)

    print("Mes de referencia: Julio")
    print(f"p = {p:.6f}")
    print(f"Observaciones: {cantidad}")
    print(f"Semilla: {semilla}")

    print()
    print("VALORES TEÓRICOS")
    print("-" * 70)

    print(
        f"Media teórica: "
        f"{media_teorica:.6f}"
    )

    print(
        f"Varianza teórica: "
        f"{varianza_teorica:.6f}"
    )

    # ========================================================
    # MÉTODO 1
    # ========================================================

    inicio = time.perf_counter()

    muestra_inversa = (
        generar_muestra_transformada_inversa(
            p=p,
            cantidad=cantidad,
            semilla=semilla
        )
    )

    tiempo_inversa = (
        time.perf_counter() - inicio
    )

    media_inversa = calcular_media(
        muestra_inversa
    )

    varianza_inversa = calcular_varianza(
        muestra_inversa
    )

    # ========================================================
    # MÉTODO 2
    # ========================================================

    inicio = time.perf_counter()

    muestra_lcg = generar_muestra_lcg(
        p=p,
        cantidad=cantidad,
        semilla=semilla
    )

    tiempo_lcg = (
        time.perf_counter() - inicio
    )

    media_lcg = calcular_media(
        muestra_lcg
    )

    varianza_lcg = calcular_varianza(
        muestra_lcg
    )

    # ========================================================
    # RESULTADOS
    # ========================================================

    print()
    print("=" * 70)
    print("RESULTADOS: TRANSFORMADA INVERSA")
    print("=" * 70)

    print(
        f"Media simulada: "
        f"{media_inversa:.6f}"
    )

    print(
        f"Varianza simulada: "
        f"{varianza_inversa:.6f}"
    )

    print(
        f"Error media: "
        f"{abs(media_inversa - media_teorica):.6f}"
    )

    print(
        f"Error varianza: "
        f"{abs(varianza_inversa - varianza_teorica):.6f}"
    )

    print(
        f"Tiempo de ejecución: "
        f"{tiempo_inversa:.6f} s"
    )

    print()
    print("=" * 70)
    print("RESULTADOS: LCG + ENSAYOS")
    print("=" * 70)

    print(
        f"Media simulada: "
        f"{media_lcg:.6f}"
    )

    print(
        f"Varianza simulada: "
        f"{varianza_lcg:.6f}"
    )

    print(
        f"Error media: "
        f"{abs(media_lcg - media_teorica):.6f}"
    )

    print(
        f"Error varianza: "
        f"{abs(varianza_lcg - varianza_teorica):.6f}"
    )

    print(
        f"Tiempo de ejecución: "
        f"{tiempo_lcg:.6f} s"
    )

    # ========================================================
    # FRECUENCIAS
    # ========================================================

    frecuencias_inversa = obtener_frecuencias(
        muestra_inversa
    )

    frecuencias_lcg = obtener_frecuencias(
        muestra_lcg
    )

    print()
    print("=" * 70)
    print("COMPARACIÓN DE FRECUENCIAS")
    print("=" * 70)

    print(
        f"{'X':<5}"
        f"{'Teórica':>15}"
        f"{'Inversa':>15}"
        f"{'LCG':>15}"
    )

    for x in range(1, 9):

        teorica = (
            ((1 - p) ** (x - 1))
            * p
        )

        inversa = (
            frecuencias_inversa.get(x, 0)
            / cantidad
        )

        lcg = (
            frecuencias_lcg.get(x, 0)
            / cantidad
        )

        print(
            f"{x:<5}"
            f"{teorica:>15.6f}"
            f"{inversa:>15.6f}"
            f"{lcg:>15.6f}"
        )

    print()
    print("=" * 70)
    print("PRUEBA FINALIZADA")
    print("=" * 70)


if __name__ == "__main__":
    main()