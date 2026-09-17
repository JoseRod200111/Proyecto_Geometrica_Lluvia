from generadores import (
    LCG,
    generar_muestra_transformada_inversa,
    generar_muestra_lcg,
    calcular_media,
    calcular_varianza,
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

SEMILLA = 42

CANTIDAD_UNIFORMES = 100000
CANTIDAD_GEOMETRICAS = 100000

# Julio:
P_JULIO = 183 / 341

# Valor crítico chi-cuadrado para:
#
# alfa = 0.05
# grados de libertad = 9
#
# Se utilizará en la prueba de uniformidad
# con 10 intervalos.
CHI2_CRITICO_9_GL = 16.919

# Para la prueba geométrica tendremos:
#
# X = 1
# X = 2
# ...
# X = 8
# X >= 9
#
# Total: 9 categorías
#
# grados de libertad = 9 - 1 = 8
CHI2_CRITICO_8_GL = 15.507


# ============================================================
# PRUEBA DE UNIFORMIDAD DEL LCG
# ============================================================

def validar_lcg_uniforme(
    cantidad=CANTIDAD_UNIFORMES,
    semilla=SEMILLA
):
    """
    Evalúa los números U generados por el LCG.

    Para U ~ Uniforme(0,1):

        E[U] = 0.5
        Var(U) = 1/12 ≈ 0.083333
    """

    lcg = LCG(
        semilla=semilla
    )

    valores = []

    for _ in range(cantidad):
        valores.append(
            lcg.random()
        )

    media = calcular_media(
        valores
    )

    varianza = calcular_varianza(
        valores
    )

    minimo = min(valores)
    maximo = max(valores)

    return {
        "valores": valores,
        "media": media,
        "varianza": varianza,
        "minimo": minimo,
        "maximo": maximo,
    }


# ============================================================
# CHI-CUADRADO PARA UNIFORMIDAD
# ============================================================

def chi_cuadrado_uniforme(
    valores,
    numero_intervalos=10
):
    """
    Divide [0,1) en intervalos iguales.

    Para 10 intervalos:

        [0.0, 0.1)
        [0.1, 0.2)
        ...
        [0.9, 1.0)

    Si los valores son uniformes, cada intervalo
    debería contener aproximadamente N/10 datos.
    """

    observados = [
        0
        for _ in range(numero_intervalos)
    ]

    for valor in valores:

        indice = int(
            valor * numero_intervalos
        )

        if indice == numero_intervalos:
            indice -= 1

        observados[indice] += 1

    esperado = (
        len(valores)
        / numero_intervalos
    )

    chi2 = 0.0

    for observado in observados:

        chi2 += (
            (observado - esperado) ** 2
            / esperado
        )

    return chi2, observados, esperado


# ============================================================
# FRECUENCIAS GEOMÉTRICAS
# ============================================================

def contar_categorias_geometricas(
    muestra
):
    """
    Crea estas categorías:

        X = 1
        X = 2
        ...
        X = 8
        X >= 9

    Agrupar la cola evita frecuencias esperadas
    demasiado pequeñas.
    """

    categorias = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        "9+": 0,
    }

    for x in muestra:

        if x <= 8:
            categorias[x] += 1
        else:
            categorias["9+"] += 1

    return categorias


# ============================================================
# CHI-CUADRADO PARA DISTRIBUCIÓN GEOMÉTRICA
# ============================================================

def chi_cuadrado_geometrica(
    muestra,
    p
):
    """
    Compara una muestra simulada contra:

        X ~ Geométrica(p)

    utilizando las categorías:

        1, 2, ..., 8, 9+
    """

    observados = (
        contar_categorias_geometricas(
            muestra
        )
    )

    n = len(muestra)

    esperados = {}

    # Categorías 1 a 8
    for x in range(1, 9):

        probabilidad = (
            ((1 - p) ** (x - 1))
            * p
        )

        esperados[x] = (
            n * probabilidad
        )

    # Cola:
    #
    # P(X >= 9) = (1-p)^8

    probabilidad_cola = (
        (1 - p) ** 8
    )

    esperados["9+"] = (
        n * probabilidad_cola
    )

    chi2 = 0.0

    for categoria in observados:

        observado = (
            observados[categoria]
        )

        esperado = (
            esperados[categoria]
        )

        chi2 += (
            (observado - esperado) ** 2
            / esperado
        )

    return (
        chi2,
        observados,
        esperados
    )


# ============================================================
# IMPRESIÓN DE PRUEBA GEOMÉTRICA
# ============================================================

def imprimir_prueba_geometrica(
    nombre,
    muestra,
    p
):

    chi2, observados, esperados = (
        chi_cuadrado_geometrica(
            muestra,
            p
        )
    )

    print()
    print("=" * 70)
    print(nombre)
    print("=" * 70)

    print(
        f"{'Categoría':<12}"
        f"{'Observado':>15}"
        f"{'Esperado':>15}"
    )

    for categoria in observados:

        print(
            f"{str(categoria):<12}"
            f"{observados[categoria]:>15}"
            f"{esperados[categoria]:>15.2f}"
        )

    print()
    print(
        f"Chi-cuadrado calculado: "
        f"{chi2:.6f}"
    )

    print(
        f"Chi-cuadrado crítico "
        f"(α=0.05, gl=8): "
        f"{CHI2_CRITICO_8_GL:.3f}"
    )

    if chi2 < CHI2_CRITICO_8_GL:

        print(
            "Resultado: NO se rechaza "
            "el ajuste geométrico."
        )

    else:

        print(
            "Resultado: se rechaza "
            "el ajuste geométrico."
        )

    return chi2


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 70)
    print("VALIDACIÓN ESTADÍSTICA DE GENERADORES")
    print("=" * 70)

    # ========================================================
    # 1. VALIDACIÓN DEL LCG
    # ========================================================

    print()
    print("=" * 70)
    print("1. VALIDACIÓN DEL LCG")
    print("=" * 70)

    resultado_lcg = (
        validar_lcg_uniforme()
    )

    print()
    print("ESTADÍSTICAS DE U ~ Uniforme(0,1)")
    print("-" * 70)

    print(
        f"Cantidad: "
        f"{CANTIDAD_UNIFORMES}"
    )

    print(
        f"Media obtenida: "
        f"{resultado_lcg['media']:.6f}"
    )

    print(
        "Media teórica: "
        "0.500000"
    )

    print(
        f"Varianza obtenida: "
        f"{resultado_lcg['varianza']:.6f}"
    )

    print(
        "Varianza teórica: "
        "0.083333"
    )

    print(
        f"Mínimo: "
        f"{resultado_lcg['minimo']:.6f}"
    )

    print(
        f"Máximo: "
        f"{resultado_lcg['maximo']:.6f}"
    )

    # --------------------------------------------------------
    # Chi-cuadrado uniforme
    # --------------------------------------------------------

    (
        chi2_uniforme,
        observados_uniforme,
        esperado_uniforme
    ) = chi_cuadrado_uniforme(
        resultado_lcg["valores"]
    )

    print()
    print("PRUEBA CHI-CUADRADO DE UNIFORMIDAD")
    print("-" * 70)

    for i, observado in enumerate(
        observados_uniforme
    ):

        inferior = i / 10
        superior = (i + 1) / 10

        print(
            f"[{inferior:.1f}, {superior:.1f}) "
            f"-> {observado}"
        )

    print()

    print(
        f"Frecuencia esperada por intervalo: "
        f"{esperado_uniforme:.2f}"
    )

    print(
        f"Chi-cuadrado calculado: "
        f"{chi2_uniforme:.6f}"
    )

    print(
        f"Chi-cuadrado crítico "
        f"(α=0.05, gl=9): "
        f"{CHI2_CRITICO_9_GL:.3f}"
    )

    if (
        chi2_uniforme
        < CHI2_CRITICO_9_GL
    ):

        print(
            "Resultado: NO se rechaza "
            "la hipótesis de uniformidad."
        )

    else:

        print(
            "Resultado: se rechaza "
            "la hipótesis de uniformidad."
        )

    # ========================================================
    # 2. MUESTRAS GEOMÉTRICAS
    # ========================================================

    print()
    print("=" * 70)
    print("2. VALIDACIÓN GEOMÉTRICA")
    print("=" * 70)

    print()
    print(
        f"p de Julio: "
        f"{P_JULIO:.6f}"
    )

    print(
        f"Tamaño de cada muestra: "
        f"{CANTIDAD_GEOMETRICAS}"
    )

    muestra_inversa = (
        generar_muestra_transformada_inversa(
            p=P_JULIO,
            cantidad=CANTIDAD_GEOMETRICAS,
            semilla=SEMILLA
        )
    )

    muestra_lcg = (
        generar_muestra_lcg(
            p=P_JULIO,
            cantidad=CANTIDAD_GEOMETRICAS,
            semilla=SEMILLA
        )
    )

    # --------------------------------------------------------
    # Valores teóricos
    # --------------------------------------------------------

    media_teorica = (
        1 / P_JULIO
    )

    varianza_teorica = (
        (1 - P_JULIO)
        /
        (P_JULIO ** 2)
    )

    print()
    print("MEDIA Y VARIANZA")
    print("-" * 70)

    print(
        f"{'':<25}"
        f"{'Media':>15}"
        f"{'Varianza':>15}"
    )

    print(
        f"{'Teórica':<25}"
        f"{media_teorica:>15.6f}"
        f"{varianza_teorica:>15.6f}"
    )

    print(
        f"{'Transformada Inversa':<25}"
        f"{calcular_media(muestra_inversa):>15.6f}"
        f"{calcular_varianza(muestra_inversa):>15.6f}"
    )

    print(
        f"{'LCG + ensayos':<25}"
        f"{calcular_media(muestra_lcg):>15.6f}"
        f"{calcular_varianza(muestra_lcg):>15.6f}"
    )

    # ========================================================
    # 3. CHI-CUADRADO DE AMBOS MÉTODOS
    # ========================================================

    imprimir_prueba_geometrica(
        "TRANSFORMADA INVERSA",
        muestra_inversa,
        P_JULIO
    )

    imprimir_prueba_geometrica(
        "LCG + ENSAYOS",
        muestra_lcg,
        P_JULIO
    )

    print()
    print("=" * 70)
    print("VALIDACIÓN FINALIZADA")
    print("=" * 70)


if __name__ == "__main__":
    main()