from datos import main as ejecutar_datos

from generadores import main as ejecutar_generadores

from estadisticas import main as ejecutar_estadisticas

from simulacion import ejecutar_simulacion

from comparacion import comparar_metodos

from graficas import generar_todas_las_graficas


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def mostrar_titulo():
    print()
    print("=" * 78)
    print("SIMULACIÓN DE INTERVALOS ENTRE DÍAS LLUVIOSOS")
    print("DISTRIBUCIÓN GEOMÉTRICA")
    print("=" * 78)

    print()
    print(
        "Datos históricos de precipitación:"
    )

    print(
        "Ciudad de Guatemala, 2015-2025"
    )

    print(
        "Definición de día lluvioso: "
        "precipitación >= 1 mm"
    )

    print()
    print(
        "Métodos de generación:"
    )

    print(
        "1. Transformada Inversa"
    )

    print(
        "2. LCG propio + ensayos sucesivos"
    )


def mostrar_menu():
    print()
    print("=" * 78)
    print("MENÚ PRINCIPAL")
    print("=" * 78)

    print()
    print(
        "1. Analizar datos históricos"
    )

    print(
        "2. Probar generadores geométricos"
    )

    print(
        "3. Ejecutar validación estadística"
    )

    print(
        "4. Ejecutar simulación completa"
    )

    print(
        "5. Comparar métodos de generación"
    )

    print(
        "6. Generar gráficas"
    )

    print(
        "7. Ejecutar todo"
    )

    print(
        "0. Salir"
    )

    print()


def esperar():
    print()

    input(
        "Presione Enter para volver al menú..."
    )


# ============================================================
# EJECUCIÓN COMPLETA
# ============================================================

def ejecutar_todo():
    """
    Ejecuta todas las etapas del proyecto
    de manera secuencial.
    """

    print()
    print("=" * 78)
    print("EJECUCIÓN COMPLETA DEL PROYECTO")
    print("=" * 78)

    # --------------------------------------------------------
    # 1. Datos históricos
    # --------------------------------------------------------

    print()
    print()
    print("#" * 78)
    print("ETAPA 1: ANÁLISIS DE DATOS HISTÓRICOS")
    print("#" * 78)
    print()

    ejecutar_datos()

    # --------------------------------------------------------
    # 2. Generadores
    # --------------------------------------------------------

    print()
    print()
    print("#" * 78)
    print("ETAPA 2: GENERADORES GEOMÉTRICOS")
    print("#" * 78)
    print()

    ejecutar_generadores()

    # --------------------------------------------------------
    # 3. Validación
    # --------------------------------------------------------

    print()
    print()
    print("#" * 78)
    print("ETAPA 3: VALIDACIÓN ESTADÍSTICA")
    print("#" * 78)
    print()

    ejecutar_estadisticas()

    # --------------------------------------------------------
    # 4. Simulación
    # --------------------------------------------------------

    print()
    print()
    print("#" * 78)
    print("ETAPA 4: SIMULACIÓN")
    print("#" * 78)
    print()

    ejecutar_simulacion()

    # --------------------------------------------------------
    # 5. Comparación
    # --------------------------------------------------------

    print()
    print()
    print("#" * 78)
    print("ETAPA 5: COMPARACIÓN DE MÉTODOS")
    print("#" * 78)
    print()

    comparar_metodos()

    # --------------------------------------------------------
    # 6. Gráficas
    # --------------------------------------------------------

    print()
    print()
    print("#" * 78)
    print("ETAPA 6: GENERACIÓN DE GRÁFICAS")
    print("#" * 78)
    print()

    generar_todas_las_graficas()

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    print()
    print()
    print("=" * 78)
    print("PROYECTO EJECUTADO CORRECTAMENTE")
    print("=" * 78)

    print()
    print(
        "Las gráficas se encuentran en:"
    )

    print(
        "resultados/graficas/"
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    mostrar_titulo()

    while True:

        mostrar_menu()

        opcion = input(
            "Seleccione una opción: "
        ).strip()

        # ====================================================
        # OPCIÓN 1
        # ====================================================

        if opcion == "1":

            print()
            ejecutar_datos()
            esperar()

        # ====================================================
        # OPCIÓN 2
        # ====================================================

        elif opcion == "2":

            print()
            ejecutar_generadores()
            esperar()

        # ====================================================
        # OPCIÓN 3
        # ====================================================

        elif opcion == "3":

            print()
            ejecutar_estadisticas()
            esperar()

        # ====================================================
        # OPCIÓN 4
        # ====================================================

        elif opcion == "4":

            print()
            ejecutar_simulacion()
            esperar()

        # ====================================================
        # OPCIÓN 5
        # ====================================================

        elif opcion == "5":

            print()
            comparar_metodos()
            esperar()

        # ====================================================
        # OPCIÓN 6
        # ====================================================

        elif opcion == "6":

            print()
            generar_todas_las_graficas()
            esperar()

        # ====================================================
        # OPCIÓN 7
        # ====================================================

        elif opcion == "7":

            print()
            ejecutar_todo()
            esperar()

        # ====================================================
        # SALIR
        # ====================================================

        elif opcion == "0":

            print()
            print("=" * 78)
            print("PROGRAMA FINALIZADO")
            print("=" * 78)
            print()

            break

        # ====================================================
        # OPCIÓN INCORRECTA
        # ====================================================

        else:

            print()
            print(
                "Opción inválida. "
                "Seleccione un número entre 0 y 7."
            )


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()