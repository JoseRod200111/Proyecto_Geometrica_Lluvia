# Simulación del número de días hasta el siguiente día lluvioso

Proyecto de Modelación y Simulación basado en el uso de la distribución geométrica para representar el número de días que transcurren hasta observar el siguiente día lluvioso en Ciudad de Guatemala.

El proyecto utiliza datos históricos diarios de precipitación del período 2015-2025 y compara dos métodos de generación de variables aleatorias geométricas:

- Transformada Inversa.
- Generador Congruencial Lineal (LCG) propio con ensayos sucesivos.

## Descripción del problema

La precipitación presenta un comportamiento aleatorio que puede analizarse mediante modelos probabilísticos.

En este proyecto se define como día lluvioso cualquier día cuya precipitación acumulada sea mayor o igual a 1 mm.

La variable aleatoria de interés es:

X = número de días hasta el siguiente día lluvioso.

Para cada mes analizado se utiliza una distribución geométrica:

P(X = k) = (1 - p)^(k - 1) * p

donde:

- X toma los valores 1, 2, 3, ...
- p representa la probabilidad estimada de que un día sea lluvioso.
- k representa el número de días necesarios hasta observar lluvia.

La probabilidad p se estima directamente a partir de los datos históricos:

p = días lluviosos / total de días observados

## Datos utilizados

Se utilizaron datos históricos diarios de precipitación obtenidos mediante Open-Meteo Historical Weather API.

Características principales:

- Período: 2015-2025.
- Resolución: diaria.
- Variable: precipitación acumulada diaria.
- Unidad: milímetros.
- Zona horaria: America/Guatemala.
- Modelo meteorológico utilizado: ERA5.
- Umbral para considerar un día lluvioso: precipitación >= 1 mm.

El archivo original se encuentra en:

```text
data/raw/precipitacion_guatemala_2015_2025.csv
```

El archivo contiene 4018 registros diarios.

## Probabilidades históricas de lluvia

Las probabilidades estimadas para cada mes fueron:

| Mes | Días lluviosos | Días analizados | p |
|---|---:|---:|---:|
| Enero | 16 | 341 | 0.0469 |
| Febrero | 27 | 311 | 0.0868 |
| Marzo | 66 | 341 | 0.1935 |
| Abril | 157 | 330 | 0.4758 |
| Mayo | 263 | 341 | 0.7713 |
| Junio | 287 | 330 | 0.8697 |
| Julio | 183 | 341 | 0.5367 |
| Agosto | 235 | 341 | 0.6891 |
| Septiembre | 289 | 330 | 0.8758 |
| Octubre | 243 | 341 | 0.7126 |
| Noviembre | 99 | 330 | 0.3000 |
| Diciembre | 34 | 341 | 0.0997 |

La variación entre meses muestra que no resulta apropiado utilizar una única probabilidad de lluvia para todo el año.

Por esta razón, el modelo se trabaja de manera mensual.

## Meses principales analizados

Para el análisis detallado se seleccionaron:

- Junio.
- Julio.
- Septiembre.

Estos meses permiten estudiar diferentes comportamientos durante la época lluviosa.

Las probabilidades utilizadas fueron:

```text
Junio:       p = 0.869697
Julio:       p = 0.536657
Septiembre:  p = 0.875758
```

Julio presenta una probabilidad considerablemente menor que junio y septiembre, por lo que produce una distribución de tiempos de espera más amplia.

## Modelo geométrico

Para una variable aleatoria geométrica:

```text
P(X = k) = (1 - p)^(k - 1) * p
```

La media teórica es:

```text
E[X] = 1 / p
```

y la varianza teórica es:

```text
Var(X) = (1 - p) / p²
```

El modelo supone que:

- Cada día puede clasificarse como lluvioso o no lluvioso.
- La probabilidad p permanece constante dentro del mes analizado.
- Los días se consideran ensayos independientes.
- El proceso termina cuando se observa el primer día lluvioso.

La independencia entre días constituye una simplificación del comportamiento meteorológico real.

## Métodos de generación

### 1. Transformada Inversa

Se genera inicialmente:

```text
U ~ Uniforme(0,1)
```

y posteriormente se transforma U para obtener una variable geométrica.

Este método permite obtener directamente el número de días hasta el primer éxito a partir de un número pseudoaleatorio uniforme.

### 2. LCG propio + ensayos sucesivos

Se implementó un Generador Congruencial Lineal propio mediante:

```text
Z(n+1) = (a * Z(n) + c) mod m
```

con:

```text
a = 1664525
c = 1013904223
m = 2^32
```

El número uniforme se calcula como:

```text
U = Z / m
```

Posteriormente se simulan días consecutivos:

```text
Si U < p:
    ocurre lluvia
Si U >= p:
    continúa la simulación
```

El número de ensayos necesarios hasta obtener lluvia corresponde a la variable geométrica X.

## Validación estadística

### Validación del LCG

Se generaron 100000 números pseudoaleatorios.

Resultados:

```text
Media obtenida:      0.501241
Media teórica:       0.500000

Varianza obtenida:   0.083046
Varianza teórica:    0.083333
```

También se aplicó una prueba chi-cuadrado de uniformidad:

```text
Chi-cuadrado calculado: 4.503
Chi-cuadrado crítico:  16.919
Nivel de significancia: 0.05
```

Como:

```text
4.503 < 16.919
```

no se rechaza la hipótesis de uniformidad.

### Validación de los generadores geométricos

Para julio se generaron 100000 observaciones con cada método.

Resultados:

```text
                         Media       Varianza

Teórica                 1.863388      1.608827
Transformada Inversa    1.866550      1.614901
LCG + ensayos           1.866170      1.623840
```

Prueba chi-cuadrado para Transformada Inversa:

```text
Chi-cuadrado calculado: 7.756248
Chi-cuadrado crítico:  15.507
```

Prueba chi-cuadrado para LCG + ensayos:

```text
Chi-cuadrado calculado: 1.285911
Chi-cuadrado crítico:  15.507
```

En ambos casos el valor calculado fue menor que el valor crítico, por lo que no se rechazó el ajuste a la distribución geométrica.

## Comparación con los datos reales

### Junio

```text
p = 0.869697

Media real:                 1.115942
Media geométrica teórica:   1.149826
Transformada Inversa:       1.144500
LCG + ensayos:              1.157800

Varianza real:              0.211195
Varianza teórica:           0.172274
```

### Julio

```text
p = 0.536657

Media real:                 1.773256
Media geométrica teórica:   1.863388
Transformada Inversa:       1.863900
LCG + ensayos:              1.879700

Varianza real:              1.826494
Varianza teórica:           1.608827
```

### Septiembre

```text
p = 0.875758

Media real:                 1.125899
Media geométrica teórica:   1.141869
Transformada Inversa:       1.137300
LCG + ensayos:              1.149600

Varianza real:              0.232351
Varianza teórica:           0.161995
```

Los generadores reproducen adecuadamente los valores esperados de la distribución geométrica.

Sin embargo, la varianza observada en los datos meteorológicos reales es mayor que la predicha por el modelo en los tres meses estudiados.

Esto indica que la distribución geométrica funciona como una aproximación útil, pero no reproduce completamente la dependencia temporal presente en la precipitación real.

## Comparación de métodos

Para realizar una comparación más estable se ejecutaron:

```text
30 repeticiones
100000 observaciones por repetición
```

para cada método.

En una de las ejecuciones experimentales se obtuvieron aproximadamente:

```text
Transformada Inversa: 0.0607 s
LCG + ensayos:        0.0830 s
```

El método LCG con ensayos sucesivos requirió más tiempo debido a que puede necesitar generar varios números uniformes antes de obtener el primer éxito.

En las pruebas realizadas, la Transformada Inversa presentó consistentemente un menor tiempo de ejecución.

En cuanto a precisión estadística, ambos métodos mostraron errores pequeños y resultados similares respecto a la distribución geométrica teórica.

## Visualizaciones

El proyecto genera automáticamente las siguientes gráficas:

```text
01_probabilidad_lluvia_por_mes.png
02_distribucion_junio.png
03_distribucion_julio.png
04_distribucion_septiembre.png
05_comparacion_medias.png
06_comparacion_varianzas.png
07_comparacion_rendimiento.png
```

Estas se almacenan en:

```text
resultados/graficas/
```

Las gráficas permiten comparar:

- Datos meteorológicos reales.
- Distribución geométrica teórica.
- Transformada Inversa.
- LCG + ensayos sucesivos.
- Medias y varianzas.
- Rendimiento computacional.

## Estructura del proyecto

```text
Proyecto_Geometrica_Lluvia/
│
├── data/
│   ├── processed/
│   └── raw/
│       └── precipitacion_guatemala_2015_2025.csv
│
├── resultados/
│   └── graficas/
│       ├── 01_probabilidad_lluvia_por_mes.png
│       ├── 02_distribucion_junio.png
│       ├── 03_distribucion_julio.png
│       ├── 04_distribucion_septiembre.png
│       ├── 05_comparacion_medias.png
│       ├── 06_comparacion_varianzas.png
│       └── 07_comparacion_rendimiento.png
│
├── src/
│   ├── comparacion.py
│   ├── datos.py
│   ├── estadisticas.py
│   ├── generadores.py
│   ├── graficas.py
│   ├── main.py
│   └── simulacion.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Función de cada archivo

### `datos.py`

Lee y procesa los datos históricos de precipitación.

Calcula:

- Probabilidad mensual de lluvia.
- Intervalos reales entre días lluviosos.
- Media y varianza observadas.

### `generadores.py`

Implementa:

- Transformada Inversa.
- LCG propio.
- Generación geométrica mediante ensayos sucesivos.

### `estadisticas.py`

Realiza:

- Validación del LCG.
- Prueba chi-cuadrado de uniformidad.
- Validación de los generadores geométricos.
- Comparación de media y varianza.

### `simulacion.py`

Ejecuta la simulación completa para:

- Junio.
- Julio.
- Septiembre.

Compara datos reales, modelo teórico y simulaciones.

### `comparacion.py`

Ejecuta múltiples repeticiones para comparar:

- Tiempo de ejecución.
- Error de la media.
- Error de la varianza.

### `graficas.py`

Genera automáticamente todas las visualizaciones del proyecto.

### `main.py`

Proporciona un menú principal desde el cual se pueden ejecutar todos los componentes del proyecto.

## Instalación

Se recomienda utilizar un entorno virtual.

En Windows PowerShell:

```powershell
python -m venv .venv
```

Activar el entorno:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```powershell
python src\main.py
```

El menú principal permite seleccionar:

```text
1. Analizar datos históricos
2. Probar generadores geométricos
3. Ejecutar validación estadística
4. Ejecutar simulación completa
5. Comparar métodos de generación
6. Generar gráficas
7. Ejecutar todo
0. Salir
```

También es posible ejecutar cada módulo individualmente:

```powershell
python src\datos.py
python src\generadores.py
python src\estadisticas.py
python src\simulacion.py
python src\comparacion.py
python src\graficas.py
```

## Resultados principales

Los resultados obtenidos muestran que:

- Ambos métodos implementados generan adecuadamente variables aleatorias con distribución geométrica.
- El LCG propio superó la prueba de uniformidad utilizada.
- Ambos generadores superaron la prueba de bondad de ajuste chi-cuadrado utilizada.
- Las medias simuladas se aproximan a las medias teóricas.
- La Transformada Inversa mostró menor tiempo de ejecución en las pruebas realizadas.
- Los datos reales presentan una varianza mayor que la predicha por la distribución geométrica.
- El modelo geométrico constituye una aproximación útil, aunque simplifica la dependencia temporal existente entre días lluviosos.

## Limitaciones

El modelo supone independencia entre días consecutivos y una probabilidad constante dentro de cada mes.

En condiciones meteorológicas reales pueden existir períodos consecutivos de lluvia o de ausencia de lluvia debido a sistemas atmosféricos persistentes.

Por esta razón, el modelo geométrico no pretende realizar un pronóstico meteorológico, sino estudiar probabilísticamente el tiempo de espera entre días lluviosos y comparar métodos de generación de variables aleatorias.

## Autor

José Roberto Rodríguez Reyes
Alejandro Rivera Rodríguez 
Juan Marcos Cruz Melara 
José Pablo Ordoñez Barrios 
Carlos Daniel Estrada Vega 

Universidad del Valle de Guatemala  
Ciencias de la Computación y Tecnologías de la Información  
Modelación y Simulación