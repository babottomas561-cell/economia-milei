# Análisis descriptivo de las variables

**La economía argentina bajo tres gobiernos: Macri (2015-2019), Fernández (2019-2023) y Milei (desde diciembre de 2023)**

> Este documento se genera con `uv run python estudio/descriptivo/descriptivo.py` a partir de `estudio/descriptivo/plantilla.md`, y el mismo script lo copia al final del `README.md`. Las tablas y los números entre llaves de la plantilla los calcula el script con los datos congelados en `data/` (último dato: inflación de {{ultimo_ipc}}, actividad de julio de 2026, cuentas nacionales del segundo trimestre de 2026, cuentas fiscales de agosto de 2026, EPH del primer trimestre de 2026 y mercados al 30/10/2026). El texto interpretativo se escribió sobre esos datos: si se actualizan, las tablas y las figuras cambian solas, pero conviene releer el texto.

## 1. Objetivo, organización y criterios

Este análisis describe, una por una, las variables con las que el estudio evalúa el desempeño económico del gobierno de Javier Milei, y las compara con los dos gobiernos anteriores. No estima ningún modelo causal: su objetivo es conocer los datos antes de modelarlos, es decir, saber qué forma tiene cada distribución, cuánto cambia de un gobierno a otro, qué valores extremos la dominan, cómo se relacionan las variables entre sí y qué propiedades estadísticas (estacionariedad, autocorrelación, estacionalidad, quiebres) van a condicionar el modelo econométrico que se propone al final (sección 7.5).

El documento se organiza así. La sección 2 resume en una tabla todas las variables, su fuente y su frecuencia. La sección 3 muestra las series largas para tener una primera imagen de los diez años. La sección 4, el núcleo del documento, trata cada variable por separado con el mismo esquema: una **ficha** (qué es y cómo se mide, fuente, por qué se eligió y cuáles son sus limitaciones), una **figura de cuatro paneles** (serie de tiempo con los gobiernos sombreados, histograma superpuesto por gobierno, diagrama de caja y barras de media y mediana), la **tabla de estadística descriptiva**, la **tabla de distribución de frecuencias** y una **interpretación** con el contexto económico de cada período. La sección 5 compara los gobiernos con todas las variables a la vez, la 6 presenta el análisis bivariado (correlaciones y diagramas de dispersión), la 7 las pruebas que preparan el modelo y la 8 las limitaciones.

**Criterios comunes a todo el análisis**

- **Períodos de gobierno.** Macri asumió el 10/12/2015, Fernández el 10/12/2019 y Milei el 10/12/2023. Cada observación se asigna al gobierno que estaba en el cargo en el **punto medio** del período que describe. Así, diciembre de 2023 es de Milei (asumió el día 10 y el mes incluye la devaluación del 13), pero el cuarto trimestre de 2023 y el segundo semestre de 2023 son de Fernández.
- **Muestra.** La mayoría de las series oficiales de datos.gob.ar que usa el estudio arrancan en enero de 2016. El IPC del INDEC se volvió a publicar en mayo de 2016 (después de la emergencia estadística declarada en enero de ese año), así que la inflación del gobierno de Macri empieza en mayo de 2016 y faltan sus primeros cinco meses, que incluyeron la salida del cepo de diciembre de 2015. **Las estadísticas de Macri son de un período incompleto y probablemente subestiman la inflación y la caída salarial de su primer año.**
- **Deflactor.** Las variables "reales" se deflactan mes a mes por el IPC nacional del INDEC (diciembre de 2016 = 100), extendido hacia atrás hasta abril de 2016 con las variaciones del IPC-GBA. La base de los índices reales es noviembre de 2023 = 100, el último mes completo del gobierno anterior.
- **Qué serie se describe.** Cuando una variable tiene tendencia (un índice de salario real, el nivel de reservas), su media por gobierno depende sobre todo de dónde empezó cada período, y su histograma mezcla niveles de años distintos. Por eso, para esas variables, la figura muestra el nivel en el tiempo pero el histograma, el boxplot y la tabla de frecuencias describen su **tasa de variación** (mensual o interanual), que es la que tiene una distribución comparable entre gobiernos. La tabla descriptiva del nivel se agrega aparte.
- **Estadísticos.** N, media, mediana, desvío estándar, mínimo, primer y tercer cuartil (Q1, Q3), máximo, coeficiente de variación, asimetría y curtosis. Se usan los estimadores muestrales corregidos de pandas. La curtosis es *en exceso*: 0 corresponde a una distribución normal y valores positivos indican colas más pesadas que la normal. El coeficiente de variación (CV = desvío / media × 100) solo se informa cuando la variable es estrictamente positiva: en tasas que cambian de signo la media puede estar cerca de cero y el CV se vuelve arbitrariamente grande y no tiene interpretación.
- **Tablas de frecuencias.** Los intervalos son **comunes a los tres gobiernos**, para que las frecuencias relativas se puedan comparar fila por fila, y son cerrados a izquierda y abiertos a derecha, [a; b). El número de intervalos sigue la regla de Sturges, k = 1 + 3,322 · log₁₀ N, con N el total de observaciones de los tres gobiernos, y el ancho se redondea a un valor "limpio" (1, 2, 2,5 o 5 por una potencia de 10). Como casi todas las series tienen colas pesadas, los intervalos cubren el rango entre los percentiles 2,5 y 97,5 y lo que queda afuera se agrupa en dos **clases abiertas** en los extremos ("menos de a", "b o más"); si no, un único mes extremo, como diciembre de 2023, obligaría a usar intervalos tan anchos que toda la distribución caería en uno o dos. Para cada gobierno se informan la frecuencia absoluta (fa), la relativa (fr, %) y la relativa acumulada (Fr, %). La inflación mensual es la única variable con intervalos de distinto ancho, elegidos a mano (ver 4.1).
- **Lectura de las figuras.** En las series de tiempo el fondo marca el gobierno (amarillo Macri, verde Fernández, azul Milei) y las líneas punteadas numeradas, los eventos: 1 PASO de 2019, 2 vuelta del cepo, 3 cuarentena, 4 legislativas de 2021, 5 balotaje de 2023, 6 devaluación de diciembre de 2023, 7 salida del cepo, 8 elección en la provincia de Buenos Aires y 9 legislativas de 2025. Los histogramas están superpuestos (contorno de cada gobierno) y en porcentaje de las observaciones de cada uno, de modo que gobiernos con distinto N se comparan bien. En los boxplots la caja va de Q1 a Q3, la línea es la mediana, los bigotes llegan hasta 1,5 rangos intercuartiles y los puntos son atípicos; cuando un único valor extremo aplastaría las cajas, el eje se recorta y los valores fuera de escala se informan al pie.

## 2. Variables del estudio

| Dimensión | Variable | Fuente | Id / origen | Frecuencia | Unidad | Período |
|:---|:---|:---|:---|:---|:---|:---|
| Precios | Inflación mensual | INDEC (IPC) | ArgentinaDatos `finanzas/indices/inflacion` | Mensual | % mensual | may-16 a sep-26 |
| Precios | Nivel del IPC, núcleo y regulados | INDEC | `148.3_INIVELNAL_DICI_M_26`, `148.3_INUCLEONAL_DICI_M_19`, `148.3_IREGULANAL_DICI_M_22` | Mensual | Índice dic-16 = 100 | dic-16 a sep-26 |
| Ingresos | Salario privado registrado | INDEC (índice de salarios) | `149.1_SOR_PRIADO_OCTU_0_25` | Mensual | Índice oct-16 = 100, deflactado | abr-16 a jul-26 |
| Ingresos | Salario público | INDEC | `149.1_SOR_PUBICO_OCTU_0_14` | Mensual | Ídem | abr-16 a jul-26 |
| Ingresos | Salario no registrado | INDEC | `149.1_SOR_PRIADO_OCTU_0_28` (corrido −5 meses) | Mensual | Ídem | may-16 a feb-26 |
| Ingresos | Salario mínimo, vital y móvil | Ministerio de Trabajo | `57.1_SMVMM_0_M_34` | Mensual | $ por mes, deflactado | abr-16 a sep-26 |
| Ingresos | Salario en blanco y en negro, tasa de no registro | INDEC, microdatos de la EPH (cálculo propio) | `data/eph_salarios.csv` (`P21`, `PP07H`, `PONDIIO`) | Trimestral | $ por mes; % | T1-17 a T1-26 |
| Actividad | EMAE desestacionalizado | INDEC | `143.3_NO_PR_2004_A_31` | Mensual | Índice 2004 = 100 | ene-16 a jul-26 |
| Actividad | PBI, consumo privado y público, inversión, exportaciones, importaciones | INDEC (cuentas nacionales) | `4.2_OGP_2004_T_17`, `4.2_MGCP_2004_T_25`, `4.2_DGCP_2004_T_30`, `4.2_DGIT_2004_T_25`, `4.2_DGE_2004_T_26`, `4.2_OGI_2004_T_25` | Trimestral | Millones de $ de 2004, tasa anual | T1-16 a T2-26 |
| Actividad | PBI y componentes nominales | INDEC | `4.4_OGP_2004_T_17`, `4.4_DGCP_2004_T_27`, `4.4_DGCP_2004_T_30`, `4.4_DGI_2004_T_19`, `4.4_OGI_2004_T_25`, `4.4_DGT_2004_T_20`, `4.4_DE_2004_T_24`, `4.4_VE_2004_T_21` | Trimestral | Millones de $ corrientes, tasa anual | T1-16 a T2-26 |
| Actividad | Valor agregado por sector (13 sectores) | INDEC | `11.2_ISOT_2004_T_39`, `11.2_VMASD_2004_T_23`, `11.2_VMATC_2004_T_12`, etc. (ver `SECTORES` en el script) | Trimestral | Millones de $ de 2004 | T1-16 a T2-26 |
| Fiscal | Resultado primario | Secretaría de Hacienda (IMIG) | `452.3_RESULTADO_RIO_0_M_18_54` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Intereses de la deuda | Hacienda | `452.3_INTERESES_TOS_0_M_15_62` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Ingresos primarios | Hacienda | `379.9_ING_PRIMAR017__36_12` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Gasto primario | Hacienda | `379.9_ING_PRIMAR017__36_12` − `379.9_SUPERAVIT_017__23_94` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Jubilaciones y pensiones | Hacienda | `452.2_JUBILACIONVAS_0_T_36_18` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Gasto por rubro | Hacienda | ids `452.2_*` y `452.3_CAPITAL_*` (ver `estudio/run.py`, `FISCAL`) | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Subsidios a la energía | Hacienda | `452.2_ENERGIAGIA_0_T_7_79` | Trimestral | Millones de $ | T1-16 a T2-26 |
| Cambio | Dólar oficial mayorista | BCRA (Com. A 3500) | API BCRA v4, variable 5 | Diaria | $ por US$ | dic-15 a oct-26 |
| Cambio | Contado con liquidación | ArgentinaDatos | `cotizaciones/dolares/contadoconliqui` | Diaria | $ por US$ | 2016 a oct-26 |
| Cambio | Reservas brutas | BCRA | API BCRA v4, variable 1 | Diaria | Millones de US$ | 2016 a oct-26 |
| Mercados | Riesgo país | JP Morgan (EMBI) vía ArgentinaDatos | `finanzas/indices/riesgo-pais` | Diaria | Puntos básicos | dic-15 a oct-26 |
| Mercados | Acciones (13 ADRs) | Yahoo Finance | GGAL, BMA, BBAR, SUPV, YPF, PAM, TGS, CEPU, EDN, TEO, CRESY, LOMA, IRS | Diaria | US$, ajustado | ene-19 a oct-26 |
| Mercados | Bonos soberanos | BYMA vía data912 | GD30D, GD35D, GD41D | Diaria | US$ MEP por 100 VN | oct-21 a oct-26 |
| Social | Pobreza | INDEC (EPH, 31 aglomerados) | Comunicados semestrales | Semestral | % de personas | S2-16 a S1-26 |
| Social | Desocupación | INDEC (EPH) | `42.3_EPH_PUNTUATAL_0_M_30` | Trimestral | % de la PEA | T2-16 a T2-26 |

Todas las series de datos.gob.ar se descargan con `load_series` (`src/quantkit/data.py`), pidiendo por separado las mensuales y las trimestrales: si se mezclan frecuencias en una misma consulta, la API agrega en silencio todas las series a la frecuencia más baja. El PBI trimestral del INDEC está **a tasa anual**: el PBI de un año es el promedio de sus cuatro trimestres, no la suma, y los flujos fiscales de 12 meses se dividen por ese promedio.

## 3. Panorama: las series largas

Antes de tratar cada variable conviene mirarlas juntas en el tiempo, porque buena parte de lo que después aparece en las tablas (asimetrías, colas pesadas, cambios de media) se explica por unos pocos episodios que se ven a simple vista.

![Precios y salarios](figuras/D01_series_precios_salarios.png)

**Figura #.** La inflación mensual tiene tres tramos nítidos: un nivel de 1% a 4% con Macri (con saltos en 2018 y después de las PASO de 2019), una aceleración casi continua con Fernández hasta 12,8% en octubre-noviembre de 2023, y con Milei un pico de 25,5% en diciembre de 2023 seguido de una desinflación muy rápida que se detiene en torno a 2% mensual desde mediados de 2025. La interanual, en escala logarítmica, muestra lo mismo sin el ruido mensual: 289% en abril de 2024 y alrededor de 31-33% desde entonces. Los salarios reales del panel inferior cuentan otra historia: la caída es de larga data (el privado registrado venía de 120-127 en 2017), con un escalón abrupto en diciembre de 2023 que el sector privado recuperó a lo largo de 2024 y el sector público no. El salario no registrado es la serie más volátil y la única que con Milei supera su nivel de 2023. El salario mínimo real cae en cada gobierno y se desploma en el actual; el tipo de cambio real salta con la devaluación y vuelve a la zona de 100 en 2025-2026: la apreciación real borró la devaluación.

![Actividad, fiscal y social](figuras/D02_series_actividad_fiscal_social.png)

**Figura #.** La actividad mensual (EMAE) no tiene tendencia de largo plazo: oscila alrededor de 100 durante diez años, con la caída de la cuarentena (marzo-abril de 2020) como único valor extremo. La inversión amplifica los ciclos del PBI: cae y sube entre dos y cuatro veces más que el producto en cada episodio. El resultado fiscal es la serie con el cambio de nivel más claro de todo el estudio: del rango −2% a −6% del PBI a un superávit primario de 1% a 2% sostenido desde 2024. La pobreza tiene un pico en el primer semestre de 2024 y cae a mínimos de la serie en el segundo de 2025; la desocupación se mueve en un rango más estrecho.

![Mercados](figuras/D03_series_mercados.png)

**Figura #.** Las variables de mercado reaccionan a los eventos políticos con más claridad que las macroeconómicas: el riesgo país salta con las PASO de 2019 (evento 1) y vuelve a subir antes de la elección de Buenos Aires de septiembre de 2025 (evento 8); la canasta de ADRs pierde la mitad de su valor en un día después de esas PASO y casi se triplica entre la asunción de Milei y enero de 2025. La brecha cambiaria, cero mientras no hay cepo, llega a 150% en 2023 y se cierra con la salida del cepo (evento 7), el mismo mes del salto de reservas por el desembolso del FMI.

## 4. Análisis por variable

### 4.1 Precios

#### Inflación mensual

*Qué es y cómo se mide.* La variación porcentual del nivel general del Índice de Precios al Consumidor (IPC) del INDEC respecto del mes anterior. El IPC mide el costo de una canasta fija de bienes y servicios de consumo de los hogares de las seis regiones del país (GBA, Pampeana, Noreste, Noroeste, Cuyo y Patagonia), con ponderaciones de la Encuesta Nacional de Gasto de los Hogares 2004/05. Los precios se relevan en comercios durante todo el mes, así que la variación mensual compara promedios de mes contra promedios de mes.

*Fuente y período.* INDEC, vía ArgentinaDatos (`finanzas/indices/inflacion`), mayo de 2016 a {{ultimo_ipc}}. Mensual, en % mensual.

*Por qué se eligió.* La estabilización de precios fue el objetivo central y explícito del programa económico de Milei y es la variable que condiciona a todas las demás: el poder de compra del salario, el tipo de cambio real y el valor real del gasto público dependen de ella. La frecuencia mensual da además la mayor cantidad de observaciones del estudio para comparar gobiernos.

*Limitaciones.* La canasta tiene más de veinte años y pondera poco los servicios y las tarifas, que fueron los precios que más subieron desde 2024: con ponderaciones actuales la inflación de 2024-2025 sería algo mayor. Entre enero y abril de 2016 no hay IPC del INDEC (ArgentinaDatos usa ahí el IPC de CABA, que acá se descarta), de modo que faltan los primeros meses de Macri.

![Inflación mensual](figuras/{{fig_infl_m}})

**Figura #. Inflación mensual por gobierno: serie, histograma, boxplot y media contra mediana.**

**Tabla #. Estadística descriptiva de la inflación mensual (%)**

{{desc_infl_m}}

**Tabla #. Distribución de frecuencias de la inflación mensual (%)**

{{frec_infl_m}}

Los intervalos de esta tabla no son los de Sturges, que con 125 meses daría 8 intervalos de igual ancho: como la cola de Milei recorre un rango diez veces mayor que el cuerpo de la distribución, todo el gobierno de Macri caería en uno o dos. Se usan intervalos de 1 punto hasta 5% y luego de 2,5, 2,5, 5 y 15 puntos, y por eso el histograma de la figura grafica la **densidad** (frecuencia relativa dividida por el ancho del intervalo): así el área de cada barra, y no su altura, es proporcional a la cantidad de meses.

La media de la inflación mensual con Milei ({{infl_m_Milei_media}}%) es casi igual a la de Fernández ({{infl_m_Fernández_media}}%), pero la comparación de medias es engañosa: la **mediana** de Milei ({{infl_m_Milei_mediana}}%) está mucho más cerca de la de Macri ({{infl_m_Macri_mediana}}%) que de la de Fernández ({{infl_m_Fernández_mediana}}%). La diferencia entre media y mediana, la asimetría de {{infl_m_Milei_asim}} y la curtosis de {{infl_m_Milei_curt}} dicen lo mismo: la distribución de Milei es una masa de meses de 1,5% a 4% más una cola de muy pocos meses extremos (diciembre de 2023 a marzo de 2024). Es el caso típico en el que la mediana describe mejor el "mes típico" que la media, y el panel de barras de la figura lo muestra: Milei es el único gobierno en el que la media casi duplica a la mediana.

La tabla de frecuencias permite leer la forma de cada distribución sin pasar por los momentos. La clase modal de Macri y de Milei es la misma, {{infl_m_Milei_moda}}, pero con pesos muy distintos: {{infl_m_Macri_moda_fr}}% de los meses de Macri y {{infl_m_Milei_moda_fr}}% de los de Milei. La de Fernández es {{infl_m_Fernández_moda}}, con {{infl_m_Fernández_moda_fr}}%. Con Macri el {{menos2_Macri}}% de los meses tuvo una inflación menor a 2%; con Fernández, el {{menos2_Fernández}}%; con Milei, el {{menos2_Milei}}%. En el otro extremo, los meses con 5% o más fueron {{mas5_Macri}}% del total con Macri, {{mas5_Fernández}}% con Fernández y {{mas5_Milei}}% con Milei. La distribución de Fernández es la más corrida a la derecha y la más dispersa en el cuerpo (su caja va de {{infl_m_Fernández_q1}}% a {{infl_m_Fernández_q3}}%); la de Milei es la más concentrada en el centro (rango intercuartil de {{infl_m_Milei_q1}}% a {{infl_m_Milei_q3}}%) y, a la vez, la única con valores por encima de 15%.

El contexto económico explica esas formas. Con Macri, la inflación bajó en 2017 bajo un esquema de metas de inflación y volvió a subir con las crisis cambiarias de 2018 y de agosto de 2019; nunca superó el 6,5% mensual. Con Fernández, la combinación de emisión para financiar el déficit (en especial en 2020), controles de precios y cepo cambiario con brecha creciente produjo una aceleración casi monótona: cada año la inflación mensual típica fue más alta que el anterior, hasta 12,8% en noviembre de 2023, después de la devaluación posterior a las PASO de ese año. Con Milei, la devaluación del 13 de diciembre de 2023 (de 366 a 800 pesos por dólar) y la liberación de precios regulados llevaron la inflación a 25,5% en diciembre; desde ahí bajó en forma muy rápida, con un tipo de cambio que se movió al 2% mensual (crawling peg), superávit fiscal y fin del financiamiento monetario al Tesoro. Desde mediados de 2025 la desinflación se estanca entre 1,5% y 3% mensual.

Para toda la muestra la curtosis de {{infl_m_Total_curt}} indica colas mucho más pesadas que una normal, y el CV de Milei ({{infl_m_Milei_cv}}%) duplica el de los gobiernos anteriores: es el período con la inflación menos estable, aunque esa inestabilidad se concentra en los primeros cuatro meses. Para el modelo, esto implica errores no normales y la necesidad de tratar explícitamente los meses de la devaluación (sección 7).

#### Inflación interanual

*Qué es y cómo se mide.* La variación porcentual del IPC nacional contra el mismo mes del año anterior. Se calcula con el índice en nivel extendido hacia atrás con el IPC-GBA, por eso arranca en abril de 2017.

*Fuente y período.* INDEC (`148.3_INIVELNAL_DICI_M_26`), abril de 2017 a {{ultimo_ipc}}. Mensual, en %.

*Por qué se eligió.* Es la medida de inflación que se usa en el debate público, en los contratos y en las paritarias, y la que elimina la estacionalidad sin necesidad de desestacionalizar.

*Limitaciones.* Cada dato contiene doce meses: la interanual "arrastra" la inflación del gobierno anterior durante el primer año del siguiente y sus observaciones consecutivas comparten once de esos doce meses, de modo que están fuertemente autocorrelacionadas y la cantidad efectiva de información es mucho menor que N.

![Inflación interanual](figuras/{{fig_infl_a}})

**Figura #. Inflación interanual por gobierno.**

**Tabla #. Estadística descriptiva de la inflación interanual (%)**

{{desc_infl_a}}

**Tabla #. Distribución de frecuencias de la inflación interanual (%)**

{{frec_infl_a}}

La media de Milei ({{infl_a_Milei_media}}%) es la más alta de los tres gobiernos, el doble de la de Fernández ({{infl_a_Fernández_media}}%) y el triple de la de Macri ({{infl_a_Macri_media}}%). Es el efecto del arrastre: los primeros once meses de Milei acumulan la inflación de 2023 y la de la devaluación, y la interanual llega a su máximo de la serie (289,4%) en abril de 2024, cuatro meses después de que la mensual ya había empezado a bajar. La mediana ({{infl_a_Milei_mediana}}%) es menor que la de Fernández ({{infl_a_Fernández_mediana}}%), y la tabla de frecuencias muestra la bimodalidad: el {{infl_a_Milei_moda_fr}}% de los meses de Milei están en la clase más baja, {{infl_a_Milei_moda}}, y casi un tercio (diciembre de 2023 a septiembre de 2024) por encima de 200%, con muy pocos meses en el medio.

La curtosis negativa de Macri ({{infl_a_Macri_curt}}) y de Milei ({{infl_a_Milei_curt}}) indica distribuciones "achatadas" o bimodales: en ambos períodos la inflación interanual pasó por dos niveles distintos (con Macri, alrededor de 25% en 2017 y alrededor de 50% en 2019; con Milei, más de 200% en 2024 y 31-33% desde 2025). En una serie con tendencia, la media es un mal resumen y el boxplot lo muestra con claridad: la caja de Milei es la más alta y la más larga, aunque el gobierno termina con la inflación interanual más baja de la década ({{infl_a_Milei_min}}% en octubre de 2025).

Económicamente, la interanual es la variable que el público "siente", y explica por qué la percepción de la desinflación llegó con rezago: en abril de 2024 la mensual ya estaba en 8,8%, pero los precios eran casi cuatro veces los de un año antes. Para el modelo, la interanual no es una buena variable dependiente (sus errores están solapados por construcción); conviene modelar la mensual y reconstruir la interanual.

#### Inflación núcleo

*Qué es y cómo se mide.* La variación mensual del IPC núcleo del INDEC, que excluye los bienes y servicios con comportamiento estacional (frutas, verduras, ropa, turismo) y los regulados (tarifas, combustibles, transporte, prepagas, cigarrillos, educación formal). Representa el 70% de la canasta.

*Fuente y período.* INDEC (`148.3_INUCLEONAL_DICI_M_19`), enero de 2017 a agosto de 2026. Mensual, en % mensual.

*Por qué se eligió.* Separa la inflación "de fondo", que responde a la demanda, a las expectativas y al tipo de cambio, de los cambios de precios que decide el Estado. Es la que miran los bancos centrales para evaluar si una desinflación es genuina.

*Limitaciones.* Sigue usando las ponderaciones de 2004/05. No es una medida de "inflación subyacente" en sentido estadístico (no recorta extremos), sino una clasificación fija de productos.

![Inflación núcleo](figuras/{{fig_infl_nucleo}})

**Figura #. Inflación núcleo por gobierno.**

**Tabla #. Estadística descriptiva de la inflación núcleo (% mensual)**

{{desc_infl_nucleo}}

**Tabla #. Distribución de frecuencias de la inflación núcleo (% mensual)**

{{frec_infl_nucleo}}

La núcleo reproduce casi exactamente la forma de la inflación general: medias de {{infl_nucleo_Macri_media}}%, {{infl_nucleo_Fernández_media}}% y {{infl_nucleo_Milei_media}}%, medianas de {{infl_nucleo_Macri_mediana}}%, {{infl_nucleo_Fernández_mediana}}% y {{infl_nucleo_Milei_mediana}}%. Con Milei la asimetría ({{infl_nucleo_Milei_asim}}) y la curtosis ({{infl_nucleo_Milei_curt}}) son todavía mayores que en la general, porque el salto de diciembre de 2023 fue más grande en la núcleo (28,3%) que en el nivel general: los bienes con precio de mercado, muchos de ellos transables, reaccionaron de inmediato a la devaluación, mientras que parte de los regulados se ajustó en los meses siguientes.

La tabla de frecuencias muestra que la clase modal es la misma para los tres gobiernos, {{infl_nucleo_Milei_moda}}, pero que concentra el {{infl_nucleo_Milei_moda_fr}}% de los meses de Milei contra el {{infl_nucleo_Macri_moda_fr}}% de Macri y el {{infl_nucleo_Fernández_moda_fr}}% de Fernández. Es la señal más clara de que, salvo el shock inicial, la inflación de fondo con Milei volvió a valores parecidos a los de 2017: su mínimo ({{infl_nucleo_Milei_min}}% en julio de 2025) es apenas superior al de Macri ({{infl_nucleo_Macri_min}}%).

La diferencia con la inflación general está en el tiempo: la núcleo bajó primero y más rápido, porque respondió a la estabilización del tipo de cambio y a la contracción de la demanda de 2024, mientras que la general quedó más alta por la recomposición de tarifas. Esa brecha entre ambas es justamente la variable siguiente.

#### Inflación de precios regulados

*Qué es y cómo se mide.* La variación mensual del componente "regulados" del IPC: bienes y servicios cuyos precios fija o autoriza el Estado (electricidad, gas, agua, combustibles, transporte público, prepagas, telefonía, educación formal, cigarrillos). En la serie de tiempo de la figura se muestra el **precio relativo** regulados / núcleo (noviembre de 2023 = 100), que indica si las tarifas subieron más o menos que el resto de la economía.

*Fuente y período.* INDEC (`148.3_IREGULANAL_DICI_M_22`), enero de 2017 a agosto de 2026. Mensual.

*Por qué se eligió.* Es la variable de política más directa del IPC: mide la "corrección de precios relativos" que el gobierno de Milei planteó como condición de la estabilización y que es la contracara de la baja de subsidios de las cuentas fiscales (sección 4.4).

*Limitaciones.* El peso de los regulados en el IPC es de alrededor del 20% con ponderaciones de 2004: probablemente subestima el peso actual de las tarifas en el gasto de los hogares.

![Regulados](figuras/{{fig_infl_regulados}})

**Figura #. Inflación de regulados por gobierno; arriba, precio relativo regulados / núcleo.**

**Tabla #. Estadística descriptiva de la inflación de regulados (% mensual)**

{{desc_infl_regulados}}

**Tabla #. Estadística descriptiva del precio relativo regulados / núcleo (nov-2023 = 100)**

{{desc_regulados_vs_nucleo}}

**Tabla #. Distribución de frecuencias de la inflación de regulados (% mensual)**

{{frec_infl_regulados}}

La serie del precio relativo es, probablemente, el gráfico que mejor resume la política de precios de cada gobierno. Con Macri los regulados se encarecen fuerte respecto de la núcleo (el "tarifazo" de 2016-2018): el relativo sube de 146 a 177 y su media en el período es {{regulados_vs_nucleo_Macri_media}}. Con Fernández ocurre lo contrario: las tarifas se congelan o se ajustan por debajo de la inflación y el relativo cae de 164 a 100, su mínimo. Con Milei se revierte de nuevo: pasa de 94 en diciembre de 2023 a {{regulados_vs_nucleo_Milei_max}} en agosto de 2026, una suba de 60% en términos reales en menos de tres años.

En las tasas mensuales, eso se ve como una media de regulados con Milei ({{infl_regulados_Milei_media}}%) mucho más alta que su mediana ({{infl_regulados_Milei_mediana}}%), con un máximo de {{infl_regulados_Milei_max}}% en enero de 2024 (un mes después del pico de la núcleo: las tarifas se ajustaron con rezago). Fernández tiene el único mes con regulados negativos (abril de 2020, en plena cuarentena) y la única curtosis negativa ({{infl_regulados_Fernández_curt}}), señal de una distribución plana: los regulados se movían por decisiones discretas, sin un valor "típico". La clase modal de Fernández es {{infl_regulados_Fernández_moda}}, la más baja de los tres.

La lectura económica es que una parte de la inflación de 2024 fue el pago de precios reprimidos durante el gobierno anterior, y que esa corrección siguió hasta 2026 con aumentos mensuales de regulados mayores que los de la núcleo en la mayoría de los meses. Para el análisis distributivo es un dato central: los hogares de ingresos bajos gastan una proporción mayor en tarifas y transporte, de modo que su inflación efectiva fue más alta que la del promedio.

### 4.2 Ingresos

Las cuatro series de salario de esta sección son índices, con tendencia, así que la figura muestra el nivel real (noviembre de 2023 = 100) y el histograma, el boxplot y la tabla de frecuencias describen la **variación mensual del salario real**, en %. La tabla descriptiva del nivel se agrega a continuación de la de variaciones.

#### Salario real privado registrado

*Qué es y cómo se mide.* El Índice de Salarios del INDEC para el sector privado registrado: asalariados con aportes a la seguridad social, a partir de los registros del SIPA. El índice sigue la remuneración de **puestos de trabajo fijos** (no el salario promedio de los que están ocupados en cada momento), así que no se mueve por cambios de composición del empleo. Se deflacta mes a mes por el IPC nacional.

*Fuente y período.* INDEC (`149.1_SOR_PRIADO_OCTU_0_25`), abril de 2016 a julio de 2026. Mensual, índice octubre de 2016 = 100, reexpresado en términos reales con base noviembre de 2023 = 100.

*Por qué se eligió.* Es el salario de referencia de la economía formal, fijado en paritarias. Mide el costo distributivo de la estabilización para el núcleo del mercado de trabajo: la devaluación de diciembre de 2023 y la aceleración inflacionaria posterior se trasladan primero a salarios.

*Limitaciones.* Mide salarios de convenio y de puestos fijos: no capta horas extra, bonos por fuera del convenio ni la pérdida de puestos. El IPC con ponderaciones viejas subestima el aumento de las tarifas, de modo que el salario real de 2024-2026 podría ser algo más bajo que el que muestra la serie.

![Salario privado registrado](figuras/{{fig_sal_priv_reg}})

**Figura #. Salario real privado registrado: nivel (arriba) y distribución de su variación mensual por gobierno.**

**Tabla #. Estadística descriptiva de la variación mensual del salario real privado registrado (%)**

{{desc_d_sal_priv_reg}}

**Tabla #. Estadística descriptiva del nivel del salario real privado registrado (nov-2023 = 100)**

{{desc_sal_priv_reg}}

**Tabla #. Distribución de frecuencias de la variación mensual del salario real privado registrado (%)**

{{frec_sal_priv_reg}}

En niveles, cada gobierno tuvo un salario real privado más bajo que el anterior: {{sal_priv_reg_Macri_media}} con Macri, {{sal_priv_reg_Fernández_media}} con Fernández y {{sal_priv_reg_Milei_media}} con Milei. La serie de la figura muestra que esa caída no es un escalón por gobierno sino una tendencia larga con dos crisis: el máximo es de agosto de 2017 ({{sal_priv_reg_Macri_max}}), la caída más importante ocurre en 2018 y 2019 con las dos devaluaciones de Macri, el período de Fernández es una meseta con leve deterioro (de 111,8 en febrero de 2020 a 100 en noviembre de 2023), y el de Milei arranca con el piso de la serie ({{sal_priv_reg_Milei_min}} en marzo de 2024), recupera hasta 100,7 en enero de 2025 y desde ahí vuelve a bajar levemente, hasta 96,6 en julio de 2026.

En variaciones mensuales, la media de los tres gobiernos es negativa o casi cero ({{d_sal_priv_reg_Macri_media}}%, {{d_sal_priv_reg_Fernández_media}}% y {{d_sal_priv_reg_Milei_media}}%). Lo que distingue a Milei es la forma: asimetría de {{d_sal_priv_reg_Milei_asim}} y curtosis de {{d_sal_priv_reg_Milei_curt}}, las más extremas de los salarios, por un único mes de caída (−11,5% en diciembre de 2023) seguido de muchos meses de recuperación. Su mediana ({{d_sal_priv_reg_Milei_mediana}}%) es la única positiva y la tabla de frecuencias lo confirma: la clase modal de Milei es {{sal_priv_reg_Milei_moda}} ({{sal_priv_reg_Milei_moda_fr}}% de los meses), mientras que la de Macri y la de Fernández es {{sal_priv_reg_Macri_moda}}. Desde febrero de 2024, el salario privado le ganó a la inflación en 18 de 30 meses.

Es un patrón de **"shock y recomposición"**, distinto de la erosión gradual de los dos gobiernos anteriores. La explicación económica es la indexación de las paritarias: en 2024 los convenios se renegociaban cada uno a tres meses con cláusulas de revisión, y cuando la inflación mensual bajó de 25% a 4% en cuatro meses, los aumentos pactados sobre la inflación pasada quedaron por encima de la inflación presente. Desde 2025, con la inflación estabilizada y el gobierno presionando para que las paritarias no superen un tope de alrededor de 1% a 2% mensual, la recuperación se detuvo. El resultado neto es que el salario privado registrado de mediados de 2026 está casi en el mismo nivel que en noviembre de 2023 y unos 20 puntos debajo del máximo de 2017.

#### Salario real público

*Qué es y cómo se mide.* El Índice de Salarios del INDEC para el sector público (nacional, provincial y municipal), deflactado por el IPC. Igual que el privado, sigue puestos fijos.

*Fuente y período.* INDEC (`149.1_SOR_PUBICO_OCTU_0_14`), abril de 2016 a julio de 2026. Mensual.

*Por qué se eligió.* Es un precio que fija el propio Estado como empleador, y por eso mide una decisión de política fiscal: una parte del ajuste del gasto pasa por la masa salarial pública.

*Limitaciones.* Mezcla jurisdicciones: el salario nacional, que decide el gobierno de Milei, pesa menos que el de las provincias, que tienen sus propias paritarias. No distingue entre sectores (docentes, salud, administración).

![Salario público](figuras/{{fig_sal_publico}})

**Figura #. Salario real público: nivel y distribución de su variación mensual por gobierno.**

**Tabla #. Estadística descriptiva de la variación mensual del salario real público (%)**

{{desc_d_sal_publico}}

**Tabla #. Estadística descriptiva del nivel del salario real público (nov-2023 = 100)**

{{desc_sal_publico}}

**Tabla #. Distribución de frecuencias de la variación mensual del salario real público (%)**

{{frec_sal_publico}}

El salario público tuvo el mismo shock inicial que el privado, pero más grande (−15,9% en diciembre de 2023, el mínimo de toda la serie) y sin la recuperación posterior. Su nivel promedio con Milei ({{sal_publico_Milei_media}}) es el más bajo de la serie, casi 20 puntos debajo del de Fernández ({{sal_publico_Fernández_media}}) y casi 40 debajo del de Macri ({{sal_publico_Macri_media}}). El desvío del nivel con Milei ({{sal_publico_Milei_desvio}}) es el menor de los tres gobiernos y el CV ({{sal_publico_Milei_cv}}%) también: el salario público quedó **estable en un nivel bajo**, entre {{sal_publico_Milei_min}} y {{sal_publico_Milei_max}}.

La distribución de las variaciones mensuales tiene la misma clase modal en los tres gobiernos ({{sal_publico_Milei_moda}}), con el {{sal_publico_Milei_moda_fr}}% de los meses de Milei, y la diferencia la hace el primer mes: la media de Milei ({{d_sal_publico_Milei_media}}%) es la más negativa por el −15,9% de diciembre de 2023, y la mediana ({{d_sal_publico_Milei_mediana}}%) es parecida a la de los otros gobiernos. Desde febrero de 2024 el salario público le ganó a la inflación en la mitad de los meses (15 de 30), pero por márgenes chicos que no alcanzaron para recuperar el escalón.

La comparación con el privado es la evidencia más directa de que la política salarial del sector público fue una herramienta del ajuste fiscal y del ancla antiinflacionaria: el Estado nacional otorgó aumentos por debajo de la inflación en 2024 y las provincias, con menos transferencias de la Nación, hicieron lo mismo. Es también la variable donde la "herencia" pesa menos: el salario público de noviembre de 2023 ya estaba unos 30 puntos debajo del de 2017, y con Milei bajó otros 16.

#### Salario real no registrado

*Qué es y cómo se mide.* El Índice de Salarios del INDEC para el sector privado no registrado (asalariados sin aportes), que se construye con datos de la Encuesta Permanente de Hogares. Se deflacta por el IPC.

*Fuente y período.* INDEC (`149.1_SOR_PRIADO_OCTU_0_28`), mayo de 2016 a febrero de 2026. Mensual.

*Por qué se eligió.* Más de un tercio de los asalariados no está registrado (ver la tasa de no registro más abajo). Es el ingreso laboral de los hogares más pobres y el que se ajusta sin paritarias ni decretos, por oferta y demanda.

*Limitaciones.* El INDEC lo publica con **cinco meses de rezago**: el dato de cada mes describe salarios de cinco meses antes, por lo que acá se corre −5 meses para ubicarlo en el mes que corresponde (por eso termina en febrero de 2026). Surge de una muestra chica de la EPH, es mucho más volátil que los otros índices y conviene leer sus movimientos en promedios de varios meses.

![Salario no registrado](figuras/{{fig_sal_no_reg}})

**Figura #. Salario real no registrado: nivel y distribución de su variación mensual por gobierno.**

**Tabla #. Estadística descriptiva de la variación mensual del salario real no registrado (%)**

{{desc_d_sal_no_reg}}

**Tabla #. Estadística descriptiva del nivel del salario real no registrado (nov-2023 = 100)**

{{desc_sal_no_reg}}

**Tabla #. Distribución de frecuencias de la variación mensual del salario real no registrado (%)**

{{frec_sal_no_reg}}

El salario no registrado es la excepción de todo el análisis: con Milei su variación mensual media es positiva ({{d_sal_no_reg_Milei_media}}% por mes, mediana {{d_sal_no_reg_Milei_mediana}}%), contra caídas promedio en los dos gobiernos anteriores ({{d_sal_no_reg_Macri_media}}% y {{d_sal_no_reg_Fernández_media}}%). La tabla de frecuencias muestra un corrimiento de toda la distribución: la clase modal de Milei es {{sal_no_reg_Milei_moda}} ({{sal_no_reg_Milei_moda_fr}}% de los meses), dos clases por encima de la de Fernández ({{sal_no_reg_Fernández_moda}}), y desde febrero de 2024 el salario informal le ganó a la inflación en 23 de 25 meses.

En niveles, recorre todo el camino de {{sal_no_reg_Milei_min}} (enero de 2024) a {{sal_no_reg_Milei_max}} (febrero de 2026) dentro del mismo gobierno, por eso su CV en niveles ({{sal_no_reg_Milei_cv}}%) es el mayor de todos los salarios y su desvío ({{sal_no_reg_Milei_desvio}}) cuadruplica el de Fernández. Termina el período por encima del nivel de 2019, aunque todavía debajo del máximo de 2017.

La lectura económica es que el salario informal, sin paritarias que lo protejan, es el que más cae cuando la inflación se acelera y el que más rápido se recompone cuando se frena, porque se fija en cada changa o trabajo y no por contratos de varios meses. A eso se sumó la recuperación de la actividad desde mediados de 2024, concentrada en servicios con alta informalidad. La serie es de muestra chica y pide cautela con cada dato aislado, pero su dirección coincide con la de la EPH (más abajo), que es una fuente independiente.

#### Salario mínimo real

*Qué es y cómo se mide.* El monto mensual del salario mínimo, vital y móvil (SMVM) para una jornada completa, fijado por el Consejo del Salario o, sin acuerdo, por decreto. Se deflacta por el IPC.

*Fuente y período.* Ministerio de Trabajo (`57.1_SMVMM_0_M_34`), abril de 2016 a septiembre de 2026. Mensual, nov-2023 = 100.

*Por qué se eligió.* Es un precio que fija directamente el gobierno y funciona como referencia para el salario informal más bajo, para planes sociales y para algunas prestaciones. Mide una decisión de política, no un resultado de mercado.

*Limitaciones.* Pocos asalariados registrados cobran exactamente el mínimo, así que su efecto sobre el salario efectivo es indirecto. Como se ajusta por escalones, su variación mensual tiene muchos ceros y por eso acá se describe el **nivel** real, no la variación.

![Salario mínimo](figuras/{{fig_smvm}})

**Figura #. Salario mínimo real por gobierno (nivel, nov-2023 = 100).**

**Tabla #. Estadística descriptiva del salario mínimo real (nov-2023 = 100)**

{{desc_smvm}}

**Tabla #. Distribución de frecuencias del salario mínimo real (nov-2023 = 100)**

{{frec_smvm}}

El salario mínimo real promedio con Milei ({{smvm_Milei_media}}) es la mitad del de Macri ({{smvm_Macri_media}}) y dos tercios del de Fernández ({{smvm_Fernández_media}}). La tabla de frecuencias es la más contundente de todo el análisis: las tres distribuciones casi no se superponen. El {{smvm_Macri_moda_fr}}% de los meses de Macri está en {{smvm_Macri_moda}}; el {{smvm_Fernández_moda_fr}}% de los de Fernández en {{smvm_Fernández_moda}}; y el {{smvm_Milei_moda_fr}}% de los de Milei en {{smvm_Milei_moda}}. El boxplot muestra tres cajas escalonadas, sin solapamiento entre ellas.

A diferencia de los salarios de mercado, el mínimo no se recuperó después del shock de diciembre de 2023: pasó de 100 a 70,6 en dos meses (diciembre y enero) y desde ahí cae de manera casi monótona hasta su mínimo de la serie ({{smvm_Milei_min}}) en el último dato. Desde mediados de 2024 se ajusta casi todos los meses, pero siempre por debajo de la inflación. La asimetría positiva de Milei ({{smvm_Milei_asim}}) la produce el primer mes (85,2 en diciembre de 2023), que todavía tenía el nivel heredado.

El salario mínimo es, junto con el público, la variable de ingreso que el gobierno controla directamente, y las dos muestran el mismo comportamiento: ajuste por debajo de la inflación como parte del ancla nominal. La diferencia es que el mínimo venía cayendo desde 2016 en todos los gobiernos: en diez años perdió más del 60% de su poder de compra (de 153,5 en septiembre de 2016 a {{smvm_Milei_min}}).

#### Salario nominal contra salario real

El salario real es un cociente: lo que se cobra en pesos (salario nominal) dividido por lo que cuestan las cosas (IPC). Mirar el numerador por separado muestra *cómo* se llegó a cada resultado real: si el salario real cae porque los aumentos fueron chicos o porque la inflación fue grande. La relación exacta es

  (1 + variación real) = (1 + variación nominal) / (1 + inflación),

y por eso con inflación alta las dos tasas pueden ser enormes y el resultado real, chico: un aumento nominal de 300% puede ser una pérdida real si la inflación fue de 330%. Las series nominales son los mismos índices de las secciones anteriores sin deflactar, en la misma ventana de tiempo.

**Tabla #. Variación mensual del salario nominal privado registrado (%)**

{{desc_dn_sal_priv_reg}}

**Tabla #. Variación mensual del salario nominal público (%)**

{{desc_dn_sal_publico}}

**Tabla #. Variación mensual del salario nominal no registrado (%)**

{{desc_dn_sal_no_reg}}

**Tabla #. Variación mensual del salario mínimo nominal (%)**

{{desc_dn_smvm}}

Los aumentos nominales mensuales siguen de cerca a la inflación de cada gobierno: el salario privado registrado subió en promedio {{dn_sal_priv_reg_Macri_media}}% por mes con Macri, {{dn_sal_priv_reg_Fernández_media}}% con Fernández y {{dn_sal_priv_reg_Milei_media}}% con Milei, contra una inflación media de {{infl_m_Macri_media}}%, {{infl_m_Fernández_media}}% y {{infl_m_Milei_media}}%. Con Milei la media y la mediana ({{dn_sal_priv_reg_Milei_mediana}}%) se separan mucho, igual que en la inflación: los aumentos nominales más grandes de toda la serie (hasta {{dn_sal_priv_reg_Milei_max}}% en un mes) llegaron en los meses posteriores a la devaluación, para recomponer lo perdido, y después se desaceleraron junto con los precios. El salario no registrado es el único con aumentos nominales mensuales mayores con Milei ({{dn_sal_no_reg_Milei_media}}%) que con Fernández ({{dn_sal_no_reg_Fernández_media}}%), aun con menos inflación: es la contracara nominal de su recuperación real. El salario mínimo tiene una distribución particular: su mediana es baja (0% con Macri) porque se ajustaba por decreto pocas veces al año y la mayoría de los meses no cambiaba.

**Tabla #. Descomposición de la variación de cada salario: nominal, inflación y real**

{{tabla_nominal_real}}

![Salario nominal contra real](figuras/D13_salario_nominal_vs_real.png)

**Figura #.** El panel izquierdo compara mes a mes los aumentos nominales con la inflación desde 2022: cuando la línea del salario queda debajo de la barra de inflación, el salario real cae ese mes. En diciembre de 2023 la brecha es máxima: precios +25,5% contra aumentos de 11,0% en el privado registrado y 5,5% en el público. Desde febrero de 2024 la relación se invierte y el salario privado supera a la inflación en 18 de los 30 meses siguientes, lo que explica su recuperación real a lo largo de 2024. El público también le gana a la inflación en la mitad de esos meses, pero por márgenes más chicos, y nunca recupera el escalón inicial. El panel derecho resume cada gobierno en términos anualizados. Con Fernández los cuatro salarios subieron entre 71% y 77% nominal por año contra una inflación de 79%: perdieron poco por año pero de manera constante. Con Milei la dispersión entre salarios es mucho mayor: con una inflación de alrededor de 70-80% anual en la ventana de cada serie, el privado registrado subió {{nr_sal_priv_reg_Milei_nom}}% nominal por año (real {{nr_sal_priv_reg_Milei_real}}%), el público {{nr_sal_publico_Milei_nom}}% (real {{nr_sal_publico_Milei_real}}%), el no registrado {{nr_sal_no_reg_Milei_nom}}% (real +{{nr_sal_no_reg_Milei_real}}%) y el mínimo solo {{nr_smvm_Milei_nom}}% (real {{nr_smvm_Milei_real}}%). Que el salario mínimo y el público, los dos que fija o negocia directamente el Estado, sean los que más quedaron atrás de la inflación es consistente con que la política salarial del sector público fue parte del ancla antiinflacionaria y del ajuste fiscal. La lección metodológica es que en una economía con inflación de tres dígitos una suba nominal "récord" no dice nada por sí sola: hay que compararla siempre con la inflación de la misma ventana.

#### Salario en blanco contra salario en negro (EPH)

*Qué es y cómo se mide.* A partir de los microdatos de la Encuesta Permanente de Hogares, el ingreso de la ocupación principal (`P21`) de los asalariados que declaran ingreso, separados en registrados y no registrados según si les hacen descuentos jubilatorios (`PP07H`), y expandidos con el ponderador de ingresos (`PONDIIO`). La variable es el cociente entre el ingreso medio de los no registrados y el de los registrados, × 100: **cuántos pesos cobra un asalariado en negro por cada $100 que cobra uno en blanco**.

*Fuente y período.* INDEC, microdatos de la EPH (cálculo propio, resumen trimestral en `data/eph_salarios.csv`), primer trimestre de 2017 al primer trimestre de 2026. Trimestral, en %.

*Por qué se eligió.* Es una medida independiente del Índice de Salarios para la brecha entre el empleo formal y el informal, con la misma pregunta de la misma encuesta para los dos grupos. Al ser un cociente, no necesita deflactor.

*Limitaciones.* Es un cociente de ingresos mensuales, no por hora: los no registrados trabajan menos horas (alrededor de 33 por semana contra 39 de los registrados). Mezcla cambios de salario con cambios de composición (quién está en cada grupo). La EPH subdeclara ingresos, sobre todo en los extremos.

![Salario en negro sobre salario en blanco](figuras/{{fig_eph_ratio}})

**Figura #. Salario medio de los asalariados no registrados por cada $100 de los registrados (EPH).**

**Tabla #. Estadística descriptiva del salario en negro por cada $100 en blanco (%)**

{{desc_eph_ratio}}

**Tabla #. Distribución de frecuencias del salario en negro por cada $100 en blanco (%)**

{{frec_eph_ratio}}

Durante ocho años el cociente se movió en un rango estrecho, de 41,5 a 47,6: en promedio, un asalariado en negro cobró {{eph_ratio_Macri_media}} pesos por cada 100 de uno en blanco con Macri y {{eph_ratio_Fernández_media}} con Fernández. Con Milei la media sube a {{eph_ratio_Milei_media}} y, sobre todo, la serie recorre un rango mucho mayor: cae a {{eph_ratio_Milei_min}} en el segundo trimestre de 2024, el mínimo de la serie, y sube sin pausa hasta {{eph_ratio_Milei_max}} en el primer trimestre de 2026, el máximo. El CV de Milei ({{eph_ratio_Milei_cv}}%) casi triplica el de los gobiernos anteriores.

La tabla de frecuencias lo muestra como un desplazamiento: la clase modal de Fernández es {{eph_ratio_Fernández_moda}} ({{eph_ratio_Fernández_moda_fr}}% de los trimestres) y la de Milei {{eph_ratio_Milei_moda}}; el último dato de Milei, {{eph_ratio_Milei_max}}, es el primero de toda la serie por encima de 50. Con solo nueve trimestres, la media y la curtosis de Milei son inestables, pero la dirección es inequívoca.

La forma en V coincide con la del índice de salarios no registrados, aunque viene de otra fuente: el salario en negro cayó más que el en blanco con el shock de la devaluación (no tenía paritaria que lo actualizara) y después creció mucho más rápido. En términos reales, el ingreso medio de los no registrados de la EPH está en el primer trimestre de 2026 alrededor de 26% por encima del cuarto trimestre de 2023, y el de los registrados, 2% por encima. Una parte puede ser efecto composición (si los informales peor pagos dejaron de trabajar o pasaron a cuentapropistas, el promedio sube), pero la brecha condicional, que controla por sexo, edad, educación, región y horas, también se achicó: de alrededor de −40% en 2017 a alrededor de −33% en 2026.

#### Tasa de asalariados no registrados (EPH)

*Qué es y cómo se mide.* El porcentaje de los asalariados que no tienen descuento jubilatorio, según la EPH, expandido con el ponderador de ingresos.

*Fuente y período.* INDEC, microdatos de la EPH (cálculo propio), T1-2017 a T1-2026. Trimestral, en % de los asalariados.

*Por qué se eligió.* Completa la lectura de la variable anterior: si el salario informal mejora pero la informalidad crece, la mejora tiene otro significado. Es también un indicador de calidad del empleo que la tasa de desocupación no capta.

*Limitaciones.* Solo cubre asalariados: los monotributistas y cuentapropistas, que crecieron en el período, no entran. En 2020 la cuarentena produjo una caída artificial (los informales perdieron el empleo, no se formalizaron).

![Tasa de no registro](figuras/{{fig_eph_tasa}})

**Figura #. Asalariados no registrados como % del total de asalariados (EPH).**

**Tabla #. Estadística descriptiva de la tasa de asalariados no registrados (%)**

{{desc_eph_tasa}}

**Tabla #. Distribución de frecuencias de la tasa de asalariados no registrados (%)**

{{frec_eph_tasa}}

La tasa de no registro con Milei es la más alta de los tres gobiernos: media de {{eph_tasa_Milei_media}}%, contra {{eph_tasa_Macri_media}}% con Macri y {{eph_tasa_Fernández_media}}% con Fernández, y el {{eph_tasa_Milei_moda_fr}}% de sus trimestres en la clase {{eph_tasa_Milei_moda}}. El máximo de la serie ({{eph_tasa_Milei_max}}%) es el último dato, el primer trimestre de 2026.

La distribución de Fernández es la más asimétrica ({{eph_tasa_Fernández_asim}}) por la cuarentena: en el segundo trimestre de 2020 la tasa cayó a {{eph_tasa_Fernández_min}}%, no porque los informales se formalizaran sino porque fueron los primeros en perder el trabajo; a medida que volvieron, la tasa subió a 37-38% en 2022. Con Milei se mantiene en ese nivel alto y con poca dispersión (desvío de {{eph_tasa_Milei_desvio}} puntos).

Leída junto con la anterior, la conclusión es que con Milei el salario informal mejoró en relación con el formal, pero dentro de un mercado de trabajo en el que más de un tercio de los asalariados sigue sin registrar y la proporción no bajó. La mejora del ingreso informal no vino de una formalización.

### 4.3 Actividad e inversión

#### Actividad económica mensual (EMAE)

*Qué es y cómo se mide.* El Estimador Mensual de Actividad Económica del INDEC aproxima mes a mes la evolución del PBI a precios de 2004, a partir de indicadores sectoriales. Se usa la serie desestacionalizada, reexpresada con noviembre de 2023 = 100; el histograma y la tabla de frecuencias describen su variación mensual (%).

*Fuente y período.* INDEC (`143.3_NO_PR_2004_A_31`), enero de 2016 a julio de 2026. Mensual.

*Por qué se eligió.* Es la única medida de actividad mensual, lo que da suficientes observaciones para comparar tres gobiernos y fechar con precisión el piso de la recesión de 2024 y la desaceleración de 2026.

*Limitaciones.* Se revisa con cada publicación; la desestacionalización del INDEC puede trasladar parte de los shocks (por ejemplo, la cuarentena de 2020) a los meses vecinos, y el último dato es el más provisorio.

![EMAE](figuras/{{fig_emae}})

**Figura #. EMAE desestacionalizado (nivel) y distribución de su variación mensual por gobierno.**

**Tabla #. Estadística descriptiva de la variación mensual del EMAE (%)**

{{desc_d_emae}}

**Tabla #. Estadística descriptiva del nivel del EMAE (nov-2023 = 100)**

{{desc_emae}}

**Tabla #. Distribución de frecuencias de la variación mensual del EMAE (%)**

{{frec_emae}}

El hecho más llamativo del EMAE es que **en diez años casi no se movió**: el nivel medio es {{emae_Macri_media}} con Macri, {{emae_Fernández_media}} con Fernández y {{emae_Milei_media}} con Milei, y salvo la cuarentena la serie siempre estuvo entre 95 y 107. La variación mensual promedio es prácticamente cero en los tres casos ({{d_emae_Macri_media}}%, {{d_emae_Fernández_media}}% y {{d_emae_Milei_media}}%). Es el estancamiento de largo plazo de la economía argentina, que precede a los tres gobiernos.

Lo que cambia entre gobiernos es la volatilidad. La de Fernández está dominada por la cuarentena: −15,6% en abril de 2020 y +10,6% en mayo, con una curtosis de {{d_emae_Fernández_curt}} y una asimetría de {{d_emae_Fernández_asim}}. Sin esos meses, la actividad con Milei es tan volátil como con Macri: desvíos de {{d_emae_Milei_desvio}} y {{d_emae_Macri_desvio}} puntos, la misma clase modal ({{emae_Milei_moda}}, con el {{emae_Milei_moda_fr}}% de los meses de Milei) y una distribución casi normal (curtosis de {{d_emae_Milei_curt}}).

En niveles, el período de Milei tiene una forma de "pozo y rebote": el EMAE cae hasta {{emae_Milei_min}} en abril de 2024 por el efecto combinado de la devaluación, la caída del salario real y el recorte del gasto, se recupera hasta el máximo de la serie ({{emae_Milei_max}}) en marzo de 2026 y vuelve a caer en los últimos meses (−2,9% en julio de 2026, el peor mes de todo el gobierno, peor incluso que diciembre de 2023). El nivel medio más alto de Milei se explica sobre todo por el rebote de 2025 y por el aporte de sectores como el agro, la minería y la energía, que se ven más abajo.

#### PBI real

*Qué es y cómo se mide.* El producto interno bruto trimestral a precios de 2004 de las cuentas nacionales del INDEC, sin desestacionalizar. Se usa la variación interanual del trimestre, que elimina la estacionalidad comparando cada trimestre con el mismo del año anterior.

*Fuente y período.* INDEC (`4.2_OGP_2004_T_17`), primer trimestre de 2017 (primera variación interanual) al segundo trimestre de 2026. Trimestral, en % interanual.

*Por qué se eligió.* Es la medida estándar del desempeño agregado y la base de las comparaciones internacionales y del crecimiento por habitante que muestra la primera parte de este README.

*Limitaciones.* El INDEC publica cada trimestre **a tasa anual**. Con 10 trimestres de Milei, cualquier diferencia de medias tiene muy poca potencia estadística. Los ponderadores de 2004 están desactualizados.

![PBI](figuras/{{fig_pib}})

**Figura #. PBI real: variación interanual del trimestre por gobierno.**

**Tabla #. Estadística descriptiva del crecimiento interanual del PBI (%)**

{{desc_g_pib}}

**Tabla #. Distribución de frecuencias del crecimiento interanual del PBI (%)**

{{frec_pib}}

La media del crecimiento interanual con Milei ({{g_pib_Milei_media}}%) es la más alta de los tres gobiernos, seguida por la de Fernández ({{g_pib_Fernández_media}}%) y la de Macri ({{g_pib_Macri_media}}%). Pero con 10 trimestres y un desvío de {{g_pib_Milei_desvio}} puntos, el error estándar de la media de Milei es de más de un punto, y la diferencia con Fernández no es estadísticamente distinguible. La tabla de frecuencias muestra que Macri y Milei comparten la clase modal, {{pib_Milei_moda}}, con la mitad de sus trimestres, mientras que Fernández tiene la distribución más dispersa (desvío de {{g_pib_Fernández_desvio}}) por la caída de 18,9% del segundo trimestre de 2020 y el rebote de 18,7% un año después: dos valores que, en la media, se cancelan casi exactamente.

El perfil de Milei es el de una recesión corta y una recuperación: −5,1% en el primer trimestre de 2024, el piso, y luego cuatro trimestres de crecimiento alto, con un máximo de 6,5% en el segundo trimestre de 2025, en buena parte por comparación con una base muy baja. Desde fines de 2025 el crecimiento se estabiliza en torno a 2%. La mediana de Milei ({{g_pib_Milei_mediana}}%) es más alta que su media, porque el período empieza con tres trimestres negativos que tiran el promedio hacia abajo.

En perspectiva, el crecimiento interanual promedio de toda la muestra ({{g_pib_Total_media}}%) no alcanza a cubrir el crecimiento de la población (alrededor de 1% anual), de modo que el producto por habitante cayó en la década: es la contracara trimestral del estancamiento que se veía en el EMAE.

#### Inversión bruta interna fija

*Qué es y cómo se mide.* La inversión en construcción, maquinaria y equipo y material de transporte, a precios de 2004, de las cuentas nacionales trimestrales. Se usa la variación interanual del trimestre.

*Fuente y período.* INDEC (`4.2_DGIT_2004_T_25`), T1-2017 a T2-2026. Trimestral, % interanual.

*Por qué se eligió.* Es el componente que anticipa el crecimiento futuro y el más sensible a la confianza en el programa económico y a la estabilidad de las reglas.

*Limitaciones.* Muy volátil y con fuerte peso de la maquinaria importada, cuyo precio relativo depende del tipo de cambio. A precios de 2004 sobrestima el peso de los bienes de capital importados.

![Inversión](figuras/{{fig_ibif}})

**Figura #. Inversión: variación interanual del trimestre por gobierno.**

**Tabla #. Estadística descriptiva del crecimiento interanual de la inversión (%)**

{{desc_g_ibif}}

**Tabla #. Distribución de frecuencias del crecimiento interanual de la inversión (%)**

{{frec_ibif}}

La inversión es entre tres y seis veces más volátil que el PBI en todos los gobiernos (desvíos de {{g_ibif_Macri_desvio}}, {{g_ibif_Fernández_desvio}} y {{g_ibif_Milei_desvio}} puntos, contra {{g_pib_Macri_desvio}}, {{g_pib_Fernández_desvio}} y {{g_pib_Milei_desvio}} del PBI). Es el patrón clásico del "acelerador": las empresas ajustan la inversión mucho más que la producción ante cambios en la demanda esperada, y en una economía con crisis recurrentes ese ajuste es extremo.

Con Milei, la media ({{g_ibif_Milei_media}}%) es parecida a la de Macri ({{g_ibif_Macri_media}}%) y la mediana ({{g_ibif_Milei_mediana}}%) es la más baja de los tres gobiernos; su clase modal es {{ibif_Milei_moda}}, con el {{ibif_Milei_moda_fr}}% de los trimestres, una clase por debajo de la de los otros dos gobiernos ({{ibif_Macri_moda}}). El perfil temporal es de montaña rusa: caídas de 24% y 29% en la primera mitad de 2024, subas de 31% y 32% en la primera mitad de 2025 (rebote sobre una base deprimida y boom de importación de bienes de capital con el dólar barato) y nuevas caídas de 11% y 12% en el primer semestre de 2026.

La lectura económica es que la estabilización no se tradujo todavía en un aumento sostenido de la inversión, que es la condición para que el crecimiento de 2025 sea duradero. La incertidumbre electoral de 2025 y las tasas de interés reales altas de ese año son dos explicaciones habituales; el Régimen de Incentivo para Grandes Inversiones (RIGI) apunta a proyectos de largo plazo cuya ejecución todavía no se refleja en estos datos.

#### Tasa de inversión

*Qué es y cómo se mide.* La inversión bruta interna fija como porcentaje del PBI, ambos a precios corrientes, suma de los últimos cuatro trimestres.

*Fuente y período.* INDEC, cuentas nacionales a precios corrientes (`4.4_DGI_2004_T_19` sobre `4.4_OGP_2004_T_17`), T4-2016 a T2-2026. Trimestral, % del PBI.

*Por qué se eligió.* Mide el esfuerzo de inversión en relación con el tamaño de la economía, que es lo que determina la acumulación de capital.

*Limitaciones.* A precios corrientes depende del precio relativo de los bienes de inversión: si la maquinaria se abarata respecto del resto de la economía, la tasa nominal baja aunque se invierta la misma cantidad física.

![Tasa de inversión](figuras/{{fig_tasa_inv}})

**Figura #. Tasa de inversión (% del PBI, precios corrientes) por gobierno.**

**Tabla #. Estadística descriptiva de la tasa de inversión (% del PBI)**

{{desc_tasa_inv}}

**Tabla #. Distribución de frecuencias de la tasa de inversión (% del PBI)**

{{frec_tasa_inv}}

La tasa de inversión a precios corrientes es parecida con Fernández ({{tasa_inv_Fernández_media}}%) y con Milei ({{tasa_inv_Milei_media}}%), y más baja con Macri ({{tasa_inv_Macri_media}}%). Pero las formas son muy distintas: la de Fernández tiene el mayor desvío ({{tasa_inv_Fernández_desvio}}) porque recorre todo el camino del mínimo de la serie (13,0% en la cuarentena) al máximo (18,5% en el tercer trimestre de 2023); la de Milei es la más concentrada, con el {{tasa_inv_Milei_moda_fr}}% de sus trimestres en {{tasa_inv_Milei_moda}}, pero con una tendencia decreciente, de {{tasa_inv_Milei_max}}% a {{tasa_inv_Milei_min}}%, el valor más bajo desde 2020.

La tasa alta de fines del gobierno de Fernández está inflada por el precio relativo: con el dólar oficial atrasado y brecha de más de 100%, los bienes de capital importados (valuados al oficial) eran caros en pesos respecto del resto de la economía. Con Milei pasa lo contrario: la apreciación real y la apertura importadora abarataron la maquinaria y la tasa a precios corrientes cae aunque la cantidad física no lo haga en la misma medida. Por eso conviene leer esta tabla junto con la anterior: en volumen, la inversión con Milei cayó; en pesos corrientes, su peso en el PBI se mantuvo en el promedio de la década.

#### Consumo privado

*Qué es y cómo se mide.* El gasto de consumo final de los hogares a precios de 2004, cuentas nacionales trimestrales; variación interanual del trimestre.

*Fuente y período.* INDEC (`4.2_MGCP_2004_T_25`), T1-2017 a T2-2026. Trimestral, % interanual.

*Por qué se eligió.* Es el 70% de la demanda y el componente más ligado al salario real y al empleo: une la sección de ingresos con la de actividad.

*Limitaciones.* En las cuentas nacionales se obtiene en parte como residuo, de modo que absorbe errores de medición de los otros componentes.

![Consumo privado](figuras/{{fig_consumo}})

**Figura #. Consumo privado: variación interanual del trimestre por gobierno.**

**Tabla #. Estadística descriptiva del crecimiento interanual del consumo privado (%)**

{{desc_g_consumo_privado}}

**Tabla #. Distribución de frecuencias del crecimiento interanual del consumo privado (%)**

{{frec_consumo}}

El consumo privado reproduce la forma del PBI pero con más amplitud: media de {{g_consumo_privado_Milei_media}}% con Milei, {{g_consumo_privado_Fernández_media}}% con Fernández y {{g_consumo_privado_Macri_media}}% con Macri, y desvíos mayores que los del producto en los tres gobiernos. Con Milei cae 5% y 8% interanual en la primera mitad de 2024, cuando el salario real tocó su piso, y crece 11,5% y 11,7% en la primera mitad de 2025, de la mano de la recuperación salarial, la vuelta del crédito al consumo y el abaratamiento de los bienes durables importados.

La distribución de Macri es la única con media negativa ({{g_consumo_privado_Macri_media}}%): la crisis de 2018-2019 se tradujo en caídas del consumo de hasta 11%, en línea con la caída del salario real de esos años. La clase modal de Milei ({{consumo_Milei_moda}}) es la misma que la de Macri. En el último dato (segundo trimestre de 2026) el consumo crece apenas 0,4% interanual: la desaceleración que mostraba el EMAE llega también al gasto de los hogares, en sintonía con el estancamiento del salario privado registrado desde 2025.

#### Consumo público

*Qué es y cómo se mide.* El gasto de consumo final del gobierno general (Nación, provincias y municipios) a precios de 2004: esencialmente salarios públicos y compras de bienes y servicios. Variación interanual del trimestre.

*Fuente y período.* INDEC (`4.2_DGCP_2004_T_30`), T1-2017 a T2-2026. Trimestral.

*Por qué se eligió.* Es la medida del ajuste fiscal desde las cuentas nacionales, y cubre también a las provincias.

*Limitaciones.* No incluye transferencias (jubilaciones, subsidios), que son la mayor parte del gasto nacional; por eso un ajuste fiscal fuerte puede verse poco en esta serie.

![Consumo público](figuras/{{fig_cpub}})

**Figura #. Consumo público: variación interanual del trimestre por gobierno.**

**Tabla #. Estadística descriptiva del crecimiento interanual del consumo público (%)**

{{desc_g_consumo_publico}}

**Tabla #. Distribución de frecuencias del crecimiento interanual del consumo público (%)**

{{frec_cpub}}

El consumo público cae en promedio con Macri ({{g_consumo_publico_Macri_media}}%) y con Milei ({{g_consumo_publico_Milei_media}}%) y crece con Fernández ({{g_consumo_publico_Fernández_media}}%): es la variable de cuentas nacionales que mejor separa a los gobiernos con programas de ajuste de los expansivos. Con Milei la distribución es la más compacta (desvío de {{g_consumo_publico_Milei_desvio}}, curtosis de {{g_consumo_publico_Milei_curt}}): caídas de 4% a 5% en la primera mitad de 2024, estabilidad en 2025 y una nueva caída de 4,1% en el segundo trimestre de 2026.

Que la caída del consumo público sea moderada comparada con la del gasto primario nacional (que cae alrededor de 26% real entre 2023 y 2025, ver 4.4) tiene una explicación de composición: el consumo público incluye a las provincias, que mantuvieron buena parte de su gasto, y no incluye las transferencias, que fueron el centro del ajuste nacional (obra pública, subsidios energéticos, transferencias a provincias).

#### Exportaciones

*Qué es y cómo se mide.* Exportaciones de bienes y servicios a precios de 2004, cuentas nacionales trimestrales; variación interanual del trimestre.

*Fuente y período.* INDEC (`4.2_DGE_2004_T_26`), T1-2017 a T2-2026. Trimestral.

*Por qué se eligió.* Son la fuente genuina de dólares de la economía y la variable que define si el crecimiento puede sostenerse sin crisis de balanza de pagos.

*Limitaciones.* Muy dependientes del clima (la cosecha) y de los precios internacionales, que no son decisiones de política.

![Exportaciones](figuras/{{fig_expo}})

**Figura #. Exportaciones: variación interanual del trimestre por gobierno.**

**Tabla #. Estadística descriptiva del crecimiento interanual de las exportaciones (%)**

{{desc_g_exportaciones}}

**Tabla #. Distribución de frecuencias del crecimiento interanual de las exportaciones (%)**

{{frec_expo}}

Las exportaciones son la variable de actividad con la diferencia más grande a favor de Milei: crecimiento interanual medio de {{g_exportaciones_Milei_media}}%, contra {{g_exportaciones_Macri_media}}% con Macri y {{g_exportaciones_Fernández_media}}% con Fernández. Todos los trimestres de Milei tienen crecimiento positivo (mínimo de {{g_exportaciones_Milei_min}}%) y el {{expo_Milei_moda_fr}}% está en la clase {{expo_Milei_moda}}, mientras que la clase modal de Fernández es {{expo_Fernández_moda}}. El boxplot de Milei no se superpone con la caja de Fernández.

Dos factores explican la mayor parte de esa diferencia y ninguno es enteramente de política. El primero es la **sequía de 2023**, la peor en décadas, que deprimió las exportaciones agrícolas del último año de Fernández y dejó una base muy baja: buena parte del crecimiento de 2024 es la cosecha que volvió a la normalidad. El segundo es la maduración de la **producción de petróleo y gas de Vaca Muerta**, con inversiones que empezaron en gobiernos anteriores y que convirtieron a la Argentina en exportadora neta de energía. Sobre esos dos factores actuaron medidas propias del gobierno, como la baja de retenciones y la unificación cambiaria, cuyo efecto aislado no se puede medir con estadística descriptiva.

#### Importaciones

*Qué es y cómo se mide.* Importaciones de bienes y servicios a precios de 2004, variación interanual del trimestre.

*Fuente y período.* INDEC (`4.2_OGI_2004_T_25`), T1-2017 a T2-2026. Trimestral.

*Por qué se eligió.* Son el componente que más responde al tipo de cambio real, a los controles cambiarios y a la apertura comercial, y su evolución muestra cómo se repartió la demanda interna entre producción local e importada.

*Limitaciones.* Mezcla bienes de consumo, insumos y bienes de capital, que responden a cosas distintas.

![Importaciones](figuras/{{fig_impo}})

**Figura #. Importaciones: variación interanual del trimestre por gobierno.**

**Tabla #. Estadística descriptiva del crecimiento interanual de las importaciones (%)**

{{desc_g_importaciones}}

**Tabla #. Distribución de frecuencias del crecimiento interanual de las importaciones (%)**

{{frec_impo}}

Las importaciones son la variable más volátil de la demanda (desvíos de {{g_importaciones_Macri_desvio}}, {{g_importaciones_Fernández_desvio}} y {{g_importaciones_Milei_desvio}} puntos) y la que tiene la distribución más "plana" en los tres gobiernos: ninguna clase concentra más de un tercio de los trimestres y las curtosis son negativas. Con Milei, la media ({{g_importaciones_Milei_media}}%) y la mediana ({{g_importaciones_Milei_mediana}}%) están muy separadas, señal de una distribución bimodal: caídas de 12% a 23% en los tres primeros trimestres de 2024, cuando la recesión y la devaluación las frenaron, y subas de 11% a 41% en 2025, con el tipo de cambio apreciado, la eliminación de licencias previas y la salida del cepo.

Las importaciones amplifican el ciclo del PBI en ambas direcciones, como la inversión, y son en buena medida su contracara: el boom de inversión de 2025 fue en gran parte maquinaria importada. En 2026 vuelven a caer (−7,5% y −8,6%), en línea con la desaceleración de la actividad y de la inversión.

#### Valor agregado por sector

El EMAE y el PBI esconden comportamientos sectoriales muy distintos. La tabla y la figura siguientes resumen el crecimiento interanual promedio de cada sector por gobierno (promedio de las variaciones interanuales trimestrales) y, para Milei, cuánto cambió el nivel de los últimos cuatro trimestres disponibles respecto de 2023, que compara años completos y por lo tanto no tiene problemas de estacionalidad.

*Fuente.* INDEC, valor agregado bruto por sector a precios de 2004, cuentas nacionales trimestrales (13 sectores, ids `11.2_*` en el script).

**Tabla #. Crecimiento por sector y gobierno**

{{tabla_sectores}}

![Sectores](figuras/B04_sectores.png)

**Figura #.** El crecimiento de Milei es **angosto**: se concentra en cinco sectores. El agro está {{sec_agro}}% por encima de 2023 (con un crecimiento interanual promedio de {{sec_agro_Milei}}%), la minería y el petróleo {{sec_mineria_y_petroleo}}%, la intermediación financiera {{sec_intermediacion_financiera}}%, hoteles y restaurantes {{sec_hoteles_y_restaurantes}}% y la pesca {{sec_pesca}}%. En el otro extremo, la construcción cambia {{sec_construccion}}% respecto de 2023, la industria {{sec_industria}}%, el comercio {{sec_comercio}}% y la administración pública {{sec_administracion_publica}}%.

Cada número tiene una explicación distinta. El agro compara con la sequía de 2023, de modo que su salto es más recuperación que crecimiento. La minería y el petróleo reflejan Vaca Muerta. La intermediación financiera crece por la remonetización y la vuelta del crédito con la desinflación, desde niveles muy bajos. La construcción cae por el fin de la obra pública (ver la composición del gasto) y la industria por la combinación de recesión de 2024, apertura importadora y dólar apreciado, que golpeó a los sectores que compiten con importaciones. Los sectores que más crecen son intensivos en capital y en recursos naturales y emplean relativamente poca gente; los que caen (construcción, industria, comercio) son los grandes empleadores. Esa es una de las razones por las que el crecimiento del PBI no se tradujo en una baja de la desocupación (sección 4.7).

Con Macri, los sectores ganadores eran los mismos recursos naturales (agro y pesca) y la construcción, con la obra pública de 2017; con Fernández, después de la pandemia, crecieron sobre todo los servicios (hoteles y restaurantes, comercio) y la construcción, mientras que el agro cayó por la sequía.

### 4.4 Cuentas fiscales

Todas las variables fiscales son del Sector Público Nacional no financiero, en base caja, del Informe Mensual de Ingresos y Gastos (IMIG) de la Secretaría de Hacienda. Los flujos se expresan como **suma de 12 meses sobre el PBI nominal** de los cuatro trimestres correspondientes (en los dos últimos meses, sin PBI publicado, se usa el último disponible), lo que elimina la fuerte estacionalidad mensual (aguinaldos en junio y diciembre) y permite comparar años con inflaciones muy distintas. Una consecuencia de esa suma móvil es que **los primeros once meses de Milei contienen meses del gobierno anterior**: el resultado de diciembre de 2023 es, en realidad, el de todo 2023.

#### Gasto primario

*Qué es y cómo se mide.* El gasto total excluidos los intereses de la deuda, obtenido como ingresos primarios menos resultado primario. Se mide como % del PBI (nivel, en la figura) y como **variación real interanual** del gasto del mes, deflactado por el IPC (histograma, boxplot y frecuencias).

*Fuente y período.* Secretaría de Hacienda (`379.9_ING_PRIMAR017__36_12` − `379.9_SUPERAVIT_017__23_94`), enero de 2016 a agosto de 2026; % del PBI desde diciembre de 2016, variación real desde enero de 2017.

*Por qué se eligió.* El ajuste fiscal de Milei se hizo por el lado del gasto, y su tamaño es la diferencia más grande entre gobiernos de todo el estudio.

*Limitaciones.* Es base caja: los gastos devengados y no pagados (deuda flotante) no aparecen hasta que se pagan. La variación interanual de un mes puede estar distorsionada por cambios en el calendario de pagos (por ejemplo, un aguinaldo adelantado).

![Gasto primario](figuras/{{fig_gasto}})

**Figura #. Gasto primario: % del PBI (arriba) y distribución de su variación real interanual por gobierno.**

**Tabla #. Estadística descriptiva de la variación real interanual del gasto primario (%)**

{{desc_d_gasto_real}}

**Tabla #. Estadística descriptiva del gasto primario (% del PBI, 12 meses)**

{{desc_gasto_pib}}

**Tabla #. Distribución de frecuencias de la variación real interanual del gasto primario (%)**

{{frec_gasto}}

El gasto primario promedio pasa de alrededor de 20% del PBI con Macri ({{gasto_pib_Macri_media}}%) y Fernández ({{gasto_pib_Fernández_media}}%) a {{gasto_pib_Milei_media}}% con Milei: más de cinco puntos del producto, el cambio de nivel más grande de todo el análisis. Las tres distribuciones del nivel prácticamente no se superponen: el máximo de Milei ({{gasto_pib_Milei_max}}%, que es diciembre de 2023 y por lo tanto el gasto de todo 2023) apenas toca los mínimos de los gobiernos anteriores, y desde mediados de 2024 la serie oscila entre 13,6% y 14,7%, los valores más bajos de la década. La asimetría ({{gasto_pib_Milei_asim}}) y la curtosis ({{gasto_pib_Milei_curt}}) de Milei las produce justamente ese primer tramo de transición.

En variaciones reales, las medias de Macri ({{d_gasto_real_Macri_media}}%) y de Milei ({{d_gasto_real_Milei_media}}%) son parecidas: los dos son gobiernos de ajuste del gasto. La diferencia está en la forma y la intensidad. Con Macri el ajuste fue gradual y sostenido (desvío de {{d_gasto_real_Macri_desvio}} puntos, el {{gasto_Macri_moda_fr}}% de los meses en {{gasto_Macri_moda}}); con Milei fue un shock concentrado: variaciones de hasta {{d_gasto_real_Milei_min}}% interanual en enero de 2024 y luego, por efecto base, subas de hasta {{d_gasto_real_Milei_max}}% en 2025 contra los meses más bajos de 2024. Por eso Milei tiene el mayor desvío ({{d_gasto_real_Milei_desvio}}) y una mediana ({{d_gasto_real_Milei_mediana}}%) más alta que la media. Fernández es el único gobierno con gasto real creciente en promedio ({{d_gasto_real_Fernández_media}}%), con un máximo de {{d_gasto_real_Fernández_max}}% en mayo de 2020 por los programas de la pandemia (IFE, ATP).

La comparación en % del PBI es más informativa que la de tasas, porque el PBI también cambió: el gasto cayó alrededor de 26% en términos reales entre 2023 y 2025 mientras el producto crecía, de modo que su peso en la economía bajó todavía más. La composición de esa caída se analiza al final de esta sección.

#### Ingresos primarios

*Qué es y cómo se mide.* Los ingresos totales del Sector Público Nacional excluidas las rentas de la propiedad financieras: impuestos, contribuciones a la seguridad social y otros ingresos corrientes y de capital. Como % del PBI (12 meses) y como variación real interanual.

*Fuente y período.* Secretaría de Hacienda (`379.9_ING_PRIMAR017__36_12`), enero de 2016 a agosto de 2026.

*Por qué se eligió.* El resultado fiscal es ingresos menos gastos: sin los ingresos no se puede saber si el superávit vino de gastar menos o de recaudar más.

*Limitaciones.* Incluye ingresos extraordinarios (moratorias, blanqueos, aportes únicos) que distorsionan las comparaciones interanuales de meses puntuales.

![Ingresos](figuras/{{fig_ingresos}})

**Figura #. Ingresos primarios: % del PBI (arriba) y distribución de su variación real interanual por gobierno.**

**Tabla #. Estadística descriptiva de la variación real interanual de los ingresos primarios (%)**

{{desc_d_ing_real}}

**Tabla #. Estadística descriptiva de los ingresos primarios (% del PBI, 12 meses)**

{{desc_ing_pib}}

**Tabla #. Distribución de frecuencias de la variación real interanual de los ingresos primarios (%)**

{{frec_ingresos}}

Los ingresos cuentan una historia que suele quedar oculta detrás del superávit: **la recaudación también bajó**. Su peso en el PBI cae en cada gobierno: {{ing_pib_Macri_media}}% con Macri, {{ing_pib_Fernández_media}}% con Fernández y {{ing_pib_Milei_media}}% con Milei, con un mínimo de la serie ({{ing_pib_Milei_min}}%) en junio de 2026. Con Milei la recaudación se sostuvo en 2024 con el impuesto PAIS y la suba de las retenciones, y bajó desde 2025 con la eliminación del impuesto PAIS, la baja de retenciones a las exportaciones agropecuarias y la caída de la recaudación ligada al comercio exterior.

En variaciones reales, las medias de Macri ({{d_ing_real_Macri_media}}%) y de Milei ({{d_ing_real_Milei_media}}%) son casi iguales y negativas, y la distribución de Milei es la más concentrada: el {{ingresos_Milei_moda_fr}}% de sus meses está en {{ingresos_Milei_moda}}, con un desvío de {{d_ing_real_Milei_desvio}} puntos contra {{d_ing_real_Fernández_desvio}} de Fernández. Los valores extremos de los gobiernos anteriores son ingresos extraordinarios: el mínimo de Macri ({{d_ing_real_Macri_min}}% en diciembre de 2017) compara contra diciembre de 2016, inflado por el impuesto especial del sinceramiento fiscal (blanqueo), y el máximo de Fernández ({{d_ing_real_Fernández_max}}% en septiembre de 2021) contra la recaudación deprimida de la pandemia y un ingreso extraordinario de ese mes.

Que el superávit se haya logrado con ingresos en baja confirma que el ajuste fue enteramente por el gasto, y es un dato relevante para su sostenibilidad: con una recaudación de alrededor de 15% del PBI, el margen para bajar más impuestos depende de seguir recortando gastos.

#### Resultado primario

*Qué es y cómo se mide.* Ingresos primarios menos gasto primario: el resultado antes del pago de intereses de la deuda. Suma de 12 meses sobre el PBI.

*Fuente y período.* Secretaría de Hacienda (`452.3_RESULTADO_RIO_0_M_18_54`), diciembre de 2016 a agosto de 2026. Mensual, % del PBI.

*Por qué se eligió.* El equilibrio fiscal ("déficit cero") fue el ancla del programa de Milei: es lo que permitió dejar de financiar al Tesoro con emisión monetaria, la causa de fondo de la inflación de los años anteriores.

*Limitaciones.* Abarca solo la Nación, no las provincias. Es base caja.

![Resultado primario](figuras/{{fig_res_primario}})

**Figura #. Resultado primario (% del PBI, 12 meses) por gobierno.**

**Tabla #. Estadística descriptiva del resultado primario (% del PBI)**

{{desc_res_primario}}

**Tabla #. Distribución de frecuencias del resultado primario (% del PBI)**

{{frec_res_primario}}

El resultado primario medio cambia de signo: {{res_primario_Macri_media}}% con Macri, {{res_primario_Fernández_media}}% con Fernández y {{res_primario_Milei_media}}% con Milei. La tabla de frecuencias es la más nítida del estudio: el {{res_primario_Milei_moda_fr}}% de los meses de Milei está en la clase {{res_primario_Milei_moda}}, una clase en la que no hay **ningún** mes de los gobiernos anteriores, y el boxplot de Milei no se superpone con los otros dos. La mediana de Milei ({{res_primario_Milei_mediana}}%) es más representativa que la media, porque el mínimo ({{res_primario_Milei_min}}%, diciembre de 2023) es el resultado de todo 2023; eso explica también su asimetría negativa ({{res_primario_Milei_asim}}) y su curtosis ({{res_primario_Milei_curt}}).

Las trayectorias dentro de cada gobierno también son distintas. Con Macri el déficit primario se achica de manera continua (de {{res_primario_Macri_min}}% a {{res_primario_Macri_max}}%), con el acuerdo con el FMI de 2018 como acelerador. Con Fernández el déficit salta a {{res_primario_Fernández_min}}% en la pandemia (diciembre de 2020) y luego se estabiliza alrededor de −2% a −3%. Con Milei el resultado pasa de −2,7% a superávit en mayo de 2024 (el primer valor positivo de la serie, en términos de 12 meses), llega a {{res_primario_Milei_max}}% en diciembre de 2024 y se mantiene entre 1,1% y 1,8% desde entonces.

Es el resultado más claro del programa y el que, según el propio gobierno, explica la desinflación: sin déficit que financiar, el Tesoro dejó de pedirle pesos al Banco Central. La correlación entre resultado primario e inflación del análisis bivariado (sección 6) es negativa con Milei, aunque, como se discute allí, en parte es el reflejo de dos tendencias simultáneas.

#### Resultado financiero

*Qué es y cómo se mide.* Resultado primario menos intereses de la deuda: el resultado fiscal "completo". Suma de 12 meses sobre el PBI.

*Fuente y período.* Secretaría de Hacienda (resultado primario menos `452.3_INTERESES_TOS_0_M_15_62`), diciembre de 2016 a agosto de 2026.

*Por qué se eligió.* Es el resultado que determina si el Estado necesita endeudarse o emitir: un superávit primario con déficit financiero sigue requiriendo financiamiento.

*Limitaciones.* En base caja, los intereses capitalizados de las Letras del Tesoro capitalizables (Lecaps), que se pagan al vencimiento junto con el capital, no se registran como intereses: el resultado financiero de 2024-2026 es algo más favorable que el devengado.

![Resultado financiero](figuras/{{fig_res_financiero}})

**Figura #. Resultado financiero (% del PBI, 12 meses) por gobierno.**

**Tabla #. Estadística descriptiva del resultado financiero (% del PBI)**

{{desc_res_financiero}}

**Tabla #. Distribución de frecuencias del resultado financiero (% del PBI)**

{{frec_res_financiero}}

Con Macri el déficit financiero fue muy estable ({{res_financiero_Macri_media}}% de media, desvío de {{res_financiero_Macri_desvio}}) y el {{res_financiero_Macri_moda_fr}}% de sus meses cae en una sola clase, {{res_financiero_Macri_moda}}: el déficit primario bajaba, pero los intereses de la deuda que se tomaba para financiarlo subían en la misma proporción. Con Fernández el déficit financiero promedio ({{res_financiero_Fernández_media}}%) es parecido pero más disperso, que llega a {{res_financiero_Fernández_min}}% en la pandemia.

Milei es el único gobierno de la muestra con meses de superávit financiero: el {{res_financiero_Milei_moda_fr}}% de sus meses está en {{res_financiero_Milei_moda}}, la mediana es positiva ({{res_financiero_Milei_mediana}}%) y el máximo es {{res_financiero_Milei_max}}% (agosto de 2025). La media es levemente negativa ({{res_financiero_Milei_media}}%) solo por los primeros meses de la suma móvil, que arrastran el déficit de 2023. En el último dato el superávit financiero es casi nulo (0,05%), lo que muestra que el margen sobre el equilibrio es estrecho.

#### Intereses de la deuda

*Qué es y cómo se mide.* Los intereses pagados de la deuda pública nacional en base caja, suma de 12 meses sobre el PBI.

*Fuente y período.* Secretaría de Hacienda (`452.3_INTERESES_TOS_0_M_15_62`), diciembre de 2016 a agosto de 2026.

*Por qué se eligió.* Es el puente entre el resultado primario y el financiero, y refleja el costo de la deuda acumulada y de las decisiones de reestructuración.

*Limitaciones.* La misma de la variable anterior: en base caja no capta los intereses capitalizados de las Lecaps ni los que se pagan con nueva deuda dentro del mismo instrumento.

![Intereses](figuras/{{fig_intereses}})

**Figura #. Intereses de la deuda (% del PBI, 12 meses) por gobierno.**

**Tabla #. Estadística descriptiva de los intereses de la deuda (% del PBI)**

{{desc_intereses_pib}}

**Tabla #. Distribución de frecuencias de los intereses de la deuda (% del PBI)**

{{frec_intereses}}

Los intereses tienen tres regímenes claros. Con Macri suben de manera continua, de {{intereses_pib_Macri_min}}% a {{intereses_pib_Macri_max}}% del PBI, por el endeudamiento en moneda extranjera y la devaluación de 2018, que multiplicó en pesos el costo de la deuda en dólares. Con Fernández caen después de la reestructuración de la deuda con acreedores privados de 2020, que redujo los cupones de los bonos en dólares, hasta un mínimo de {{intereses_pib_Fernández_min}}%. Con Milei bajan todavía más: media de {{intereses_pib_Milei_media}}%, el {{intereses_Milei_moda_fr}}% de los meses en la clase más baja ({{intereses_Milei_moda}}) y un mínimo de la serie de {{intereses_pib_Milei_min}}% en junio de 2026.

Parte de esa baja es contable: la deuda en pesos se refinanció con Lecaps cuyos intereses no aparecen como tales en la base caja. Otra parte es real: el crecimiento del PBI en dólares, con un tipo de cambio apreciado, reduce el peso de la deuda en moneda extranjera. La comparación de los CV (todos entre 19% y 30%) muestra que los intereses son la variable fiscal con más tendencia dentro de cada gobierno.

#### Jubilaciones y pensiones

*Qué es y cómo se mide.* El gasto en prestaciones de la seguridad social (jubilaciones y pensiones contributivas). Como % del PBI (12 meses) y como variación real interanual.

*Fuente y período.* Secretaría de Hacienda (`452.2_JUBILACIONVAS_0_T_36_18`), enero de 2016 a agosto de 2026.

*Por qué se eligió.* Es el rubro más grande del gasto (un tercio en 2023, 44% en 2025) y el que más debate generó: su evolución depende de la fórmula de movilidad, que cambió en cada gobierno.

*Limitaciones.* Mide el gasto total, no el haber de cada jubilado: incluye el efecto del aumento de la cantidad de beneficiarios. No distingue entre el haber mínimo y los haberes más altos, que siguieron trayectorias distintas.

![Jubilaciones](figuras/{{fig_jubilaciones}})

**Figura #. Gasto en jubilaciones: % del PBI (arriba) y distribución de su variación real interanual por gobierno.**

**Tabla #. Estadística descriptiva de la variación real interanual del gasto en jubilaciones (%)**

{{desc_d_jub_real}}

**Tabla #. Estadística descriptiva del gasto en jubilaciones (% del PBI, 12 meses)**

{{desc_jub_pib}}

**Tabla #. Distribución de frecuencias de la variación real interanual del gasto en jubilaciones (%)**

{{frec_jubilaciones}}

El gasto en jubilaciones cae como % del PBI en cada gobierno: {{jub_pib_Macri_media}}% con Macri, {{jub_pib_Fernández_media}}% con Fernández y {{jub_pib_Milei_media}}% con Milei. Con Fernández la caída es la más fuerte dentro del período (de 8,7% en 2020 a {{jub_pib_Fernández_min}}% en noviembre de 2023): la fórmula de movilidad de 2021 ajustaba con rezago de varios meses y con inflación en aceleración los haberes quedaban cada vez más atrás. Con Milei el piso es {{jub_pib_Milei_min}}% en mayo de 2024 y desde ahí el gasto **sube** hasta {{jub_pib_Milei_max}}% en el último dato.

Las variaciones reales lo muestran con precisión. Con Milei la distribución es la más dispersa (desvío de {{d_jub_real_Milei_desvio}} puntos): una variación de {{d_jub_real_Milei_min}}% interanual en enero de 2024, cuando la fórmula heredada actualizó los haberes muy por debajo de la inflación de la devaluación, y subas de hasta {{d_jub_real_Milei_max}}% en 2025 contra esa base deprimida. En el medio, un decreto de marzo de 2024 (DNU 274/2024) cambió la fórmula, desde abril, a una indexación mensual por la inflación pasada, que desde entonces preservó el valor real de los haberes. La mediana de Milei ({{d_jub_real_Milei_mediana}}%) es la más alta de los tres gobiernos; la media ({{d_jub_real_Milei_media}}%) es casi cero.

La paradoja aparente es que las jubilaciones pasaron de un tercio a 44% del gasto primario (ver las tortas más abajo) mientras su gasto real caía en 2024. No hay contradicción: el total cayó mucho más que las jubilaciones, así que su participación subió. El haber mínimo con el bono previsional, congelado en términos nominales desde 2024, sí perdió valor real; esta serie, que es el gasto total, no permite verlo.

#### Subsidios a la energía

*Qué es y cómo se mide.* Transferencias corrientes al sector energético (CAMMESA, ENARSA y otros) que cubren la diferencia entre el costo de la energía y las tarifas. Solo existen con frecuencia trimestral en datos.gob.ar; se miden como % del PBI del trimestre.

*Fuente y período.* Secretaría de Hacienda (`452.2_ENERGIAGIA_0_T_7_79`), T1-2016 a T2-2026. Trimestral.

*Por qué se eligió.* Es el rubro donde la "corrección de precios relativos" (la suba de tarifas de la sección de precios) se traduce directamente en menor gasto.

*Limitaciones.* Muy estacional (suben en invierno por la importación de gas) y con pagos atrasados que se mueven de un trimestre a otro.

![Subsidios a la energía](figuras/{{fig_sub_energia}})

**Figura #. Subsidios a la energía (% del PBI del trimestre) por gobierno.**

**Tabla #. Estadística descriptiva de los subsidios a la energía (% del PBI del trimestre)**

{{desc_sub_energia_pib}}

**Tabla #. Distribución de frecuencias de los subsidios a la energía (% del PBI del trimestre)**

{{frec_sub_energia}}

Los subsidios energéticos son el rubro con la caída más clara: de {{sub_energia_pib_Fernández_media}}% del PBI por trimestre con Fernández a {{sub_energia_pib_Milei_media}}% con Milei, menos de la mitad. La clase modal de Milei ({{sub_energia_Milei_moda}}) está una clase por debajo de la de los otros dos gobiernos ({{sub_energia_Fernández_moda}}), y su máximo ({{sub_energia_pib_Milei_max}}%) es apenas superior a la mediana de Macri.

Macri tiene la distribución más asimétrica ({{sub_energia_pib_Macri_asim}}) porque arranca con los subsidios heredados de 2015 (hasta {{sub_energia_pib_Macri_max}}% en el cuarto trimestre de 2016) y los reduce con los aumentos de tarifas de 2016-2018: un proceso muy parecido al de Milei, que se revirtió con Fernández, cuando el congelamiento de tarifas y la suba del precio internacional del gas en 2022 los llevaron de nuevo a 2% a 3% del PBI trimestral. La comparación con el precio relativo de los regulados (sección 4.1) cierra el círculo: los dos gobiernos que subieron tarifas por encima de la inflación bajaron subsidios, y el que las congeló los subió.

#### Composición del gasto y de la demanda (tortas)

Para ver la composición del gasto se usa el gasto de cada año completo en pesos corrientes: las participaciones no necesitan deflactarse, porque numerador y denominador están en la misma moneda del mismo año.

**Tabla #. Estructura del gasto primario, 2023 y 2025 (% del total)**

{{tabla_gasto}}

![Tortas del gasto](figuras/D07_tortas_gasto.png)

**Figura #.** La composición del gasto cambió más que en cualquier otro momento de la serie. Las jubilaciones pasaron de un tercio a 44% del gasto primario y las asignaciones (AUH y familiares) de 4,4% a 7,4%. Esto **no** significa que se gastara más en jubilaciones: su gasto real cayó 4% entre 2023 y 2025 (ver `estudio/results.md`), pero el total cayó 26% y los rubros que más se recortaron (obra pública, de 6,1% a 1,6% del gasto; subsidios a la energía, de 8,3% a 4,8%) dejaron más espacio relativo a las prestaciones sociales. Es un buen ejemplo de por qué una torta debe leerse junto con el tamaño del total: una porción más grande de una torta más chica puede ser un monto menor.

Para el PBI por componente se usan las cuentas nacionales a precios corrientes. Una torta necesita partes positivas que sumen el total, y el PBI no cumple eso por el lado de la demanda (las importaciones restan); por eso se grafica la composición de la demanda final, C + G + I + X, y las importaciones se informan aparte. Las exportaciones a precios corrientes se obtienen por identidad (demanda global menos el resto de sus componentes), porque esa serie viene vacía en la API.

**Tabla #. Componentes de la demanda (% del PBI, precios corrientes)**

{{tabla_demanda}}

![Tortas de la demanda](figuras/D08_tortas_demanda.png)

**Figura #.** Entre 2023 y 2025 crece el peso del consumo privado (de 65,8% a 70,8% del PBI) y de las exportaciones (de 12,7% a 15,5%, por la normalización de la cosecha después de la sequía y por Vaca Muerta), y bajan el consumo público (de 16,2% a 15,3%) y la inversión (de 18,4% a 16,6%). Las importaciones también suben (de 13,7% a 14,8%), en línea con la apertura comercial. La caída del consumo público en el PBI es la contraparte, en las cuentas nacionales, del ajuste fiscal de esta sección.

### 4.5 Tipo de cambio y reservas

#### Dólar oficial: depreciación mensual y tipo de cambio real

*Qué es y cómo se mide.* El tipo de cambio mayorista de referencia de la Comunicación A 3500 del BCRA, en pesos por dólar, promediado por mes. La distribución describe su **depreciación mensual** (variación % del promedio mensual); la serie de la figura muestra el **tipo de cambio real** bilateral (oficial / IPC, noviembre de 2023 = 100), que indica cuán caro o barato está el dólar en relación con los precios internos.

*Fuente y período.* BCRA (API de Estadísticas Monetarias v4, variable 5), diciembre de 2015 a octubre de 2026; IPC del INDEC para el tipo de cambio real. Mensual.

*Por qué se eligió.* La devaluación del 13/12/2023 (118% en un día) y la salida del cepo del 14/4/2025 son los dos eventos cambiarios centrales del período; el tipo de cambio es además el principal canal de traspaso a precios (sección 6) y el precio que define la competitividad de los sectores transables.

*Limitaciones.* El tipo de cambio real no descuenta la inflación de Estados Unidos (alrededor de 3% anual) y es bilateral, no multilateral. El promedio mensual reparte un salto discreto entre dos meses: la devaluación de diciembre de 2023 aparece como +81% en diciembre y el resto en enero.

![Dólar oficial](figuras/{{fig_dolar}})

**Figura #. Tipo de cambio real oficial (arriba) y distribución de la depreciación mensual por gobierno.**

**Tabla #. Estadística descriptiva de la depreciación mensual del dólar oficial (%)**

{{desc_dep_oficial}}

**Tabla #. Estadística descriptiva del tipo de cambio real oficial (nov-2023 = 100)**

{{desc_tcr}}

**Tabla #. Distribución de frecuencias de la depreciación mensual del dólar oficial (%)**

{{frec_dolar}}

La depreciación mensual mediana es casi igual con Macri ({{dep_oficial_Macri_mediana}}%) y con Milei ({{dep_oficial_Milei_mediana}}%) y más alta con Fernández ({{dep_oficial_Fernández_mediana}}%), pero Milei tiene la distribución más extrema de todo el análisis: asimetría de {{dep_oficial_Milei_asim}} y curtosis de {{dep_oficial_Milei_curt}}, por un único salto ({{dep_oficial_Milei_max}}% en diciembre de 2023) seguido de un crawling peg de 2% mensual hasta abril de 2025 y de una flotación entre bandas desde entonces. La tabla de frecuencias muestra que el {{dolar_Milei_moda_fr}}% de los meses de Milei está en {{dolar_Milei_moda}}, la concentración más alta de los tres gobiernos. Es el tipo de variable donde la media y el desvío describen mal el proceso: lo que hay es un régimen con un salto discreto.

Los regímenes cambiarios de los gobiernos anteriores dejan huellas igual de nítidas. Con Macri, que tuvo tipo de cambio flotante, el {{dolar_Macri_moda_fr}}% de los meses cae en la clase modal y más de un cuarto de los meses tiene depreciación **negativa** (el peso se apreció): es la distribución más dispersa en el cuerpo, con las crisis de 2018 (+28,1% en septiembre) y 2019 en la cola. Con Fernández no hay ningún mes negativo: con cepo y un crawling peg administrado, el oficial subió todos los meses, con un salto de {{dep_oficial_Fernández_max}}% después de las PASO de agosto de 2023.

En tipo de cambio real, el promedio de Milei ({{tcr_Milei_media}}) es el más bajo de los tres gobiernos, es decir, el peso más apreciado. La serie lo explica: la devaluación lleva el tipo de cambio real a {{tcr_Milei_max}} en enero de 2024, pero como la inflación de los meses siguientes fue muy superior al 2% del crawling peg, la ganancia se erosiona en un año y medio. Después de un repunte en la previa electoral de 2025, el tipo de cambio real cae a {{tcr_Milei_min}} en mayo de 2026, por debajo del nivel de noviembre de 2023. Es el costo del ancla cambiaria: ayuda a bajar la inflación, pero encarece la producción local en dólares y explica parte del mal desempeño de la industria y del boom de importaciones.

#### Brecha cambiaria

*Qué es y cómo se mide.* La diferencia porcentual entre el dólar contado con liquidación (CCL), que se obtiene comprando un activo en pesos y vendiéndolo en dólares en el exterior, y el dólar oficial mayorista. Promedio mensual de datos diarios.

*Fuente y período.* BCRA (oficial) y ArgentinaDatos (`cotizaciones/dolares/contadoconliqui`), enero de 2016 a octubre de 2026. Mensual, en %.

*Por qué se eligió.* Es el termómetro de los controles cambiarios: sin cepo la brecha es casi cero, y su tamaño mide cuánto se desvía el precio oficial del que surge del mercado. Una brecha alta anticipa devaluaciones y alimenta expectativas de inflación.

*Limitaciones.* El CCL es un mercado chico y su precio puede ser afectado por intervenciones del BCRA. Después de abril de 2025, con restricciones para empresas que todavía siguen, la brecha no es exactamente cero.

![Brecha](figuras/{{fig_brecha}})

**Figura #. Brecha cambiaria (CCL sobre oficial, %) por gobierno.**

**Tabla #. Estadística descriptiva de la brecha cambiaria (%)**

{{desc_brecha}}

**Tabla #. Distribución de frecuencias de la brecha cambiaria (%)**

{{frec_brecha}}

La brecha separa a los tres gobiernos como pocas variables. Con Macri, sin cepo hasta septiembre de 2019, la mediana es {{brecha_Macri_mediana}}% y el {{brecha_Macri_moda_fr}}% de los meses está en {{brecha_Macri_moda}}; la media ({{brecha_Macri_media}}%) y la curtosis ({{brecha_Macri_curt}}) las producen los tres últimos meses, con el cepo de vuelta. Con Fernández la brecha es estructural: media de {{brecha_Fernández_media}}%, nunca baja de 25% y llega a {{brecha_Fernández_max}}% en octubre de 2023, en la previa del balotaje. Su clase modal es {{brecha_Fernández_moda}}.

Con Milei la brecha cae de {{brecha_Milei_max}}% en diciembre de 2023 (con el oficial ya devaluado) a menos de 20% en pocos meses, se mantiene en un rango de 10% a 50% durante 2024 mientras rige el cepo con el "dólar blend" (que liquidaba el 20% de las exportaciones al CCL), y prácticamente desaparece con la salida del cepo de abril de 2025 (mínimo de {{brecha_Milei_min}}% en agosto de 2025). La media ({{brecha_Milei_media}}%) y la mediana ({{brecha_Milei_mediana}}%) están muy separadas porque la distribución mezcla los dos regímenes.

La correlación entre brecha e inflación es alta con Fernández y con Milei (sección 6), lo que es coherente con la idea de que la brecha anticipa la devaluación del oficial y, con ella, la inflación; pero con Milei la brecha y la inflación también bajaron juntas por motivos comunes (estabilización, superávit fiscal), así que la correlación no prueba una causalidad.

#### Reservas internacionales

*Qué es y cómo se mide.* Las reservas internacionales brutas del BCRA en miles de millones de dólares, dato de fin de mes. La distribución describe su variación mensual (%).

*Fuente y período.* BCRA (API de Estadísticas Monetarias v4, variable 1), enero de 2016 a octubre de 2026. Mensual.

*Por qué se eligió.* Son el respaldo de la moneda y la capacidad del BCRA de defender el tipo de cambio y pagar deuda; su caída precedió a las crisis de 2018-2019 y 2023.

*Limitaciones.* Las reservas brutas incluyen pasivos: el swap con China, encajes de los depósitos en dólares, préstamos de organismos internacionales y repos con bancos. Las reservas **netas**, que descuentan esos pasivos, son mucho menores y, en algunos períodos, negativas; no hay una serie oficial de reservas netas.

![Reservas](figuras/{{fig_reservas}})

**Figura #. Reservas brutas del BCRA (arriba) y distribución de su variación mensual por gobierno.**

**Tabla #. Estadística descriptiva de la variación mensual de las reservas (%)**

{{desc_d_reservas}}

**Tabla #. Estadística descriptiva de las reservas brutas (miles de millones de US$)**

{{desc_reservas_m}}

**Tabla #. Distribución de frecuencias de la variación mensual de las reservas (%)**

{{frec_reservas}}

En niveles, las reservas promedio son las más altas con Macri ({{reservas_m_Macri_media}} mil millones, con un máximo de {{reservas_m_Macri_max}} en abril de 2019 por los desembolsos del FMI) y las más bajas con Milei ({{reservas_m_Milei_media}}), pero las trayectorias son opuestas: Macri y Fernández terminan con menos reservas de las que tenían en su mejor momento (Fernández deja el mínimo de la serie, {{reservas_m_Fernández_min}} mil millones en noviembre de 2023), mientras que Milei empieza en ese piso y termina en el máximo de su período ({{reservas_m_Milei_max}} mil millones en octubre de 2026).

La variación mensual media es positiva con Macri ({{d_reservas_Macri_media}}%) y con Milei ({{d_reservas_Milei_media}}%) y negativa con Fernández ({{d_reservas_Fernández_media}}%), cuya clase modal es {{reservas_Fernández_moda}}. Con Milei la distribución es muy asimétrica ({{d_reservas_Milei_asim}}) y con una curtosis de {{d_reservas_Milei_curt}}, por un solo mes: abril de 2025, con +{{d_reservas_Milei_max}}% por el primer desembolso del nuevo acuerdo con el FMI (alrededor de US$ 12.000 millones) al salir del cepo. Sin ese mes, la mediana ({{d_reservas_Milei_mediana}}%) muestra una acumulación moderada pero sostenida.

Es importante no leer el aumento de las reservas brutas como una mejora equivalente de la solvencia externa: buena parte del aumento de 2025-2026 es deuda (FMI, repos, colocaciones del Tesoro), no compras de divisas del BCRA en el mercado.

### 4.6 Mercados

#### Riesgo país

*Qué es y cómo se mide.* El spread del índice EMBI de JP Morgan para Argentina: la diferencia de rendimiento entre los bonos soberanos argentinos en dólares y los bonos del Tesoro de Estados Unidos de plazo similar, en puntos básicos (100 pb = 1 punto porcentual). Dato diario.

*Fuente y período.* JP Morgan vía ArgentinaDatos (`finanzas/indices/riesgo-pais`), diciembre de 2015 a octubre de 2026. Diario.

*Por qué se eligió.* Resume en un número la probabilidad de default que asignan los inversores y determina el costo al que el país podría volver a financiarse en los mercados internacionales. Es una evaluación del programa económico en tiempo real.

*Limitaciones.* Depende también de la tasa de Estados Unidos y del apetito global por riesgo emergente: no es solo una calificación del gobierno. Las observaciones diarias están muy autocorrelacionadas, de modo que el N de la tabla sobrestima mucho la información disponible.

![Riesgo país](figuras/{{fig_riesgo_pais}})

**Figura #. Riesgo país (puntos básicos, escala logarítmica) por gobierno.**

**Tabla #. Estadística descriptiva del riesgo país (puntos básicos)**

{{desc_riesgo_pais}}

**Tabla #. Distribución de frecuencias del riesgo país (puntos básicos)**

{{frec_riesgo_pais}}

El riesgo país promedio con Milei ({{riesgo_pais_Milei_media}} pb) es menos de la mitad del de Fernández ({{riesgo_pais_Fernández_media}} pb) y más alto que el de Macri ({{riesgo_pais_Macri_media}} pb). Las medianas son más informativas: {{riesgo_pais_Macri_mediana}} pb con Macri, {{riesgo_pais_Fernández_mediana}} con Fernández y {{riesgo_pais_Milei_mediana}} con Milei. La media de Macri está inflada por los meses posteriores a las PASO de 2019 (hasta {{riesgo_pais_Macri_max}} pb el 30/8/2019), y por eso su asimetría ({{riesgo_pais_Macri_asim}}) es la más alta. La de Fernández, por el pico de la pandemia (4.362 pb el 23/3/2020) y por el default técnico previo a la reestructuración.

La tabla de frecuencias muestra tres distribuciones casi separadas: la clase modal de Macri es {{riesgo_pais_Macri_moda}} ({{riesgo_pais_Macri_moda_fr}}% de los días), la de Milei {{riesgo_pais_Milei_moda}} ({{riesgo_pais_Milei_moda_fr}}%) y la de Fernández {{riesgo_pais_Fernández_moda}}, con una distribución mucho más plana (solo {{riesgo_pais_Fernández_moda_fr}}% de los días en la clase modal). El boxplot de Milei es el más alto en relación con su mediana: su caja va de {{riesgo_pais_Milei_q1}} a {{riesgo_pais_Milei_q3}} pb porque el período tiene una tendencia fuerte, no un nivel estable.

La trayectoria con Milei: de alrededor de 1.900 pb al asumir a un mínimo de {{riesgo_pais_Milei_min}} pb en julio de 2026, con dos interrupciones. La primera, en 2025, con la incertidumbre electoral: el riesgo país subió a más de 1.400 pb antes y después de la derrota oficialista en la provincia de Buenos Aires (evento 8) y cayó bruscamente después de las legislativas de octubre (evento 9). La segunda, en los últimos meses de la muestra, con una suba hasta 787 pb a fines de octubre de 2026. Que el riesgo país no haya bajado de 400 pb, a pesar del superávit fiscal, indica que los mercados todavía no consideran a la Argentina un emisor de riesgo normal: el acceso al financiamiento voluntario sigue siendo caro.

#### Acciones argentinas (13 ADRs)

*Qué es y cómo se mide.* Una canasta equiponderada de las 13 acciones argentinas más líquidas que cotizan en Nueva York (GGAL, BMA, BBAR, SUPV, YPF, PAM, TGS, CEPU, EDN, TEO, CRESY, LOMA, IRS), con precios ajustados por dividendos, en dólares. La distribución describe el **retorno logarítmico diario** en %, 100 · ln(P_t / P_t−1); la serie muestra el nivel de la canasta (2/1/2019 = 1).

*Fuente y período.* Yahoo Finance, enero de 2019 a octubre de 2026. Diario.

*Por qué se eligió.* Los precios de mercado son la evaluación en tiempo real de las expectativas sobre la economía y la política, y a diferencia de las estadísticas oficiales no tienen rezago.

*Limitaciones.* La canasta está sesgada a bancos y energía, y no representa a la economía en su conjunto. Empieza en 2019: el período de Macri cubre solo su último año, que incluye las PASO.

![ADRs](figuras/{{fig_adr}})

**Figura #. Canasta de ADRs argentinos (arriba, escala logarítmica) y distribución del retorno diario por gobierno.**

**Tabla #. Estadística descriptiva del retorno diario de la canasta de ADRs (%, logarítmico)**

{{desc_r_adr}}

**Tabla #. Estadística descriptiva del nivel de la canasta de ADRs (2/1/2019 = 1)**

{{desc_adr_canasta}}

**Tabla #. Distribución de frecuencias del retorno diario de la canasta de ADRs (%)**

{{frec_adr}}

Los retornos diarios tienen las colas más pesadas de todo el análisis. La curtosis de {{r_adr_Macri_curt}} de Macri la produce un solo día, el 12/8/2019, con −68,4% logarítmico (la canasta perdió la mitad de su valor en una sesión, la reacción a las PASO). Sin él, las curtosis de Fernández ({{r_adr_Fernández_curt}}) y de Milei ({{r_adr_Milei_curt}}) siguen lejos de la normal: con Milei, el peor día fue el 8/9/2025, después de la elección bonaerense ({{r_adr_Milei_min}}%), y el mejor el 27/10/2025, después de las legislativas (+{{r_adr_Milei_max}}%). Es la evidencia descriptiva de por qué los modelos de riesgo de mercado para activos argentinos usan distribuciones t de Student o volatilidad condicional (GARCH) en lugar de la normal.

La tabla de frecuencias muestra que, a diferencia de las variables macroeconómicas, las distribuciones de los tres gobiernos son muy parecidas en el cuerpo: la clase modal es {{adr_Milei_moda}} en los tres, con alrededor del 19% al 23% de los días, y la mediana diaria es prácticamente cero. Las diferencias de rendimiento acumulado entre gobiernos, enormes en niveles, surgen de diferencias de media diarias muy chicas ({{r_adr_Fernández_media}}% contra {{r_adr_Milei_media}}%) acumuladas durante cientos de días.

En niveles, la canasta promedia {{adr_canasta_Fernández_media}} con Fernández (con un piso de {{adr_canasta_Fernández_min}} en abril de 2020) y {{adr_canasta_Milei_media}} con Milei, con un máximo de {{adr_canasta_Milei_max}} en enero de 2025: las acciones argentinas se multiplicaron por casi tres entre la asunción y ese máximo, en una de las subas más grandes del mundo en ese período, y desde ahí oscilaron con la política.

#### Bonos soberanos (GD30, GD35, GD41)

*Qué es y cómo se mide.* Una cartera equiponderada de los tres bonos Globales en dólares más líquidos de la reestructuración de 2020, medida por **retorno total** (variación de precio más cupones y amortizaciones cobrados), para que la amortización del GD30 no parezca una pérdida. La distribución describe el retorno diario en %; la serie, el índice de retorno total (1/10/2021 = 100).

*Fuente y período.* BYMA vía data912 (GD30D, GD35D, GD41D, en dólares MEP), octubre de 2021 a octubre de 2026. Diario.

*Por qué se eligió.* Es la medida directa de cuánto valía la deuda del país para sus tenedores, y la contracara del riesgo país en precios.

*Limitaciones.* Los datos empiezan en octubre de 2021: la comparación con Fernández cubre solo su segunda mitad y no hay datos de Macri. Algunos saltos diarios grandes de signo opuesto en días consecutivos (como el 3 y 4 de agosto de 2023) parecen problemas de registro de precios más que movimientos reales.

![Bonos](figuras/{{fig_bonos}})

**Figura #. Índice de retorno total de los Globales (arriba) y distribución del retorno diario por gobierno.**

**Tabla #. Estadística descriptiva del retorno diario total de la cartera GD30/GD35/GD41 (%)**

{{desc_r_bonos}}

**Tabla #. Estadística descriptiva del índice de retorno total (1/10/2021 = 100)**

{{desc_bonos_idx}}

**Tabla #. Distribución de frecuencias del retorno diario de los bonos (%)**

{{frec_bonos}}

El retorno medio diario de los bonos con Milei ({{r_bonos_Milei_media}}% por día) es el más alto de los dos gobiernos con datos, con un desvío ({{r_bonos_Milei_desvio}}) menor que con Fernández ({{r_bonos_Fernández_desvio}}): rindieron más y con menos volatilidad. La tabla de frecuencias muestra que el {{bonos_Milei_moda_fr}}% de los días de Milei cae en la clase {{bonos_Milei_moda}}, contra el {{bonos_Fernández_moda_fr}}% de Fernández: la distribución de Milei es mucho más concentrada en pequeñas ganancias diarias.

En niveles, el índice de retorno total pasa de alrededor de 104 en enero de 2024 a un máximo de {{bonos_idx_Milei_max}} en julio de 2026: un tenedor de Globales casi triplicó su inversión en dólares durante el gobierno, la contracara de la baja del riesgo país de 1.900 a 400 pb. Con Fernández el índice cae a {{bonos_idx_Fernández_min}} en julio de 2022 (la renuncia del ministro Guzmán), y termina el período algo por encima del valor con el que empezó ({{bonos_idx_Fernández_max}} en agosto de 2023 fue su máximo).

La curtosis de Milei ({{r_bonos_Milei_curt}}) y su asimetría positiva ({{r_bonos_Milei_asim}}) las producen los días alrededor de los eventos de 2025: −9,0% el 8/9/2025, tras la elección bonaerense, y +16,4% el 22/9/2025, con el anuncio de apoyo financiero del Tesoro de Estados Unidos.

### 4.7 Indicadores sociales

#### Pobreza

*Qué es y cómo se mide.* El porcentaje de personas que viven en hogares cuyo ingreso total no alcanza para comprar la Canasta Básica Total (alimentos y otros bienes y servicios esenciales), según la EPH de 31 aglomerados urbanos, por semestre.

*Fuente y período.* INDEC, comunicados semestrales de "Incidencia de la pobreza y la indigencia"; los valores de S2-2025 (28,2%) y S1-2026 (32,3%) son del comunicado del 24/9/2026. Segundo semestre de 2016 al primer semestre de 2026. Semestral.

*Por qué se eligió.* Es el indicador social más seguido y el que mejor refleja el efecto combinado de inflación, salarios, empleo y transferencias sobre los hogares.

*Limitaciones.* Solo 20 observaciones en diez años (5 de Milei), de modo que asimetría y curtosis son muy inestables. Cubre solo la población urbana; la EPH subdeclara ingresos; y la canasta se valoriza con el IPC, cuya canasta de 2004 subestima el peso de las tarifas.

![Pobreza](figuras/{{fig_pobreza}})

**Figura #. Pobreza (% de personas, semestral) por gobierno.**

**Tabla #. Estadística descriptiva de la pobreza (%)**

{{desc_pobreza}}

**Tabla #. Distribución de frecuencias de la pobreza (%)**

{{frec_pobreza}}

La pobreza media con Milei ({{pobreza_Milei_media}}%) está entre la de Macri ({{pobreza_Macri_media}}%) y la de Fernández ({{pobreza_Fernández_media}}%), pero con solo 5 semestres y un recorrido de 52,9% a 28,2% la media no es un buen resumen. La mediana ({{pobreza_Milei_mediana}}%) y el CV de {{pobreza_Milei_cv}}%, el más alto de los tres gobiernos, dicen que es el período con la pobreza más cambiante, con el pico de la década ({{pobreza_Milei_max}}%) y el valor más bajo desde 2018 ({{pobreza_Milei_min}}%) dentro del mismo gobierno. La tabla de frecuencias muestra que el {{pobreza_Fernández_moda_fr}}% de los semestres de Fernández está en {{pobreza_Fernández_moda}}, mientras que Milei tiene semestres en cuatro clases distintas.

El pico del primer semestre de 2024 es la consecuencia directa de la devaluación: la canasta básica subió con la inflación de 25% mensual mientras los ingresos quedaban atrás. La baja posterior es igual de rápida y tiene tres motores: la desinflación (que frenó la suba de la canasta), la recuperación del salario informal (el ingreso de los hogares de menores ingresos) y el aumento real de la AUH y de la Tarjeta Alimentar. La suba del primer semestre de 2026 (de 28,2% a 32,3%) es en parte estacional (el primer semestre suele ser peor que el segundo) y en parte refleja la desaceleración de la actividad y del salario formal.

#### Desocupación

*Qué es y cómo se mide.* Los desocupados (personas que no trabajan, buscaron trabajo y están disponibles) como porcentaje de la población económicamente activa, EPH, 31 aglomerados, por trimestre.

*Fuente y período.* INDEC (`42.3_EPH_PUNTUATAL_0_M_30`), segundo trimestre de 2016 al segundo trimestre de 2026. Trimestral.

*Por qué se eligió.* Completa la lectura del mercado de trabajo: el salario real puede subir porque se pierden los empleos peor pagos, y la pobreza depende tanto del salario como de tener trabajo.

*Limitaciones.* Es estacional (más alta en el primer trimestre), por lo que conviene comparar trimestres iguales. No capta la precarización (empleo no registrado, monotributo) ni el desaliento (quien deja de buscar trabajo deja de contar como desocupado).

![Desocupación](figuras/{{fig_desocupacion}})

**Figura #. Desocupación (% de la PEA, trimestral) por gobierno.**

**Tabla #. Estadística descriptiva de la desocupación (%)**

{{desc_desocupacion}}

**Tabla #. Distribución de frecuencias de la desocupación (%)**

{{frec_desocupacion}}

La desocupación media con Milei ({{desocupacion_Milei_media}}%) es la más baja de los tres gobiernos (contra {{desocupacion_Macri_media}}% y {{desocupacion_Fernández_media}}%) y la menos dispersa (desvío de {{desocupacion_Milei_desvio}}): el {{desocupacion_Milei_moda_fr}}% de sus trimestres está en {{desocupacion_Milei_moda}}. Pero conviene leerla con cuidado. La de Fernández incluye el pico de la pandemia (13,1% en el segundo trimestre de 2020) y termina con el mínimo de la serie (5,7% en el cuarto trimestre de 2023); por eso su mediana ({{desocupacion_Fernández_mediana}}%) es más baja que la de Milei ({{desocupacion_Milei_mediana}}%) y su distribución es la más asimétrica.

Comparando trimestres iguales, que es lo correcto para una serie estacional, la desocupación con Milei **subió**: de 6,2% en el segundo trimestre de 2023 a 7,6% en el de 2025 y 7,9% en el de 2026. Es coherente con la composición sectorial del crecimiento (sección 4.3): los sectores que crecieron emplean poca gente y los que cayeron, mucha.

La relación entre desocupación y crecimiento (ley de Okun) y entre desocupación e inflación (curva de Phillips) se analiza en la sección 6.

## 5. Comparación entre gobiernos

Esta sección junta las variables principales para comparar los tres gobiernos de un vistazo.

### 5.1 Promedios por gobierno

![Barras de promedios](figuras/D05_barras_promedios.png)

**Figura #.** Cada barra es la media del período y el segmento vertical, ± un error estándar (desvío / √N). Las barras resumen lo que ya mostraron las tablas: la mayor diferencia entre gobiernos está en el resultado fiscal; en la variación mensual del salario real privado los intervalos se superponen por completo; en el crecimiento del PBI los intervalos también se superponen. **Advertencia metodológica:** el error estándar así calculado supone observaciones independientes, y estas series son muy persistentes (ver la sección 7): los intervalos verdaderos son más anchos. Un test formal de diferencia de medias debería usar errores estándar robustos a autocorrelación (Newey-West), lo que se deja para el modelo econométrico.

### 5.2 Variación acumulada y anualizada

La variación acumulada compara el último dato del gobierno anterior con el último dato del propio. Como los períodos tienen distinto largo (Milei lleva menos de tres años), se anualiza: (1 + variación acumulada)^(1/años) − 1. Las filas con asterisco no empiezan en el último dato del gobierno anterior porque la serie no existe antes (Macri).

**Tabla #. Variación acumulada y anualizada por gobierno**

{{tabla_variacion}}

![Barras de variación](figuras/D06_barras_variacion_por_gobierno.png)

**Figura #.** La inflación anualizada de Milei (69%) es menor que la de Fernández (79%) y mayor que la de Macri (38%, con sus primeros cinco meses fuera de la muestra), y está dominada por los primeros cuatro meses: anualizada, la inflación fue de 62% entre abril y diciembre de 2024, 31,5% en 2025 y 33% en los nueve meses de 2026. En términos reales, el patrón de Milei es el más heterogéneo: el salario no registrado sube 16,7% por año y el mínimo cae 16,9% por año; el salario público cae 6,3% anual, el privado registrado 1,3% (igual que con Fernández); el PBI crece 1,7% por año (el mejor de los tres) y la inversión cae 4% por año. El tipo de cambio real termina casi donde empezó (−1,3% anual) después de recorrer un salto de 50% y su reversión.

### 5.3 Boxplots comparados

![Boxplots](figuras/D09_boxplots.png)

**Figura #.** Los diagramas de caja de las variables principales, uno al lado del otro, permiten comparar posición, dispersión y valores atípicos al mismo tiempo. En la inflación, la caja de Milei (rango intercuartil) es la más angosta y está a la altura de la de Macri, y los meses de diciembre de 2023 a marzo de 2024 aparecen como **atípicos** (más de 1,5 rangos intercuartiles por encima del tercer cuartil). En el resultado primario la caja de Milei no se superpone con ninguna de las anteriores: es la variable donde el cambio de régimen es visible incluso en la distribución completa. El riesgo país de Macri tiene una caja baja con muchos atípicos (los meses posteriores a las PASO); el de Milei tiene una caja alta, porque en su período el riesgo país bajó de 2.000 a 400 puntos y volvió a subir: una distribución con tendencia, no un nivel estable.

## 6. Análisis bivariado

Las secciones anteriores describieron cada variable por separado. Esta sección mira cómo se mueven de a pares, con tres herramientas: una matriz de correlaciones por gobierno, una tabla de pares seleccionados con su significatividad y diagramas de dispersión. Ninguna de ellas mide causalidad: una correlación puede deberse a que una variable afecta a la otra, a que ambas responden a una tercera o, en series con tendencia, a que simplemente se movieron en la misma dirección en el mismo período (correlación espuria). Este último problema es serio acá, porque la sección 7 muestra que varias de estas series son no estacionarias. Por eso la matriz usa **tasas de variación** siempre que es posible.

### 6.1 Matriz de correlaciones

Se usa la correlación de rangos de **Spearman** (ρ), que mide asociación monótona y no lineal y es robusta a valores extremos: con Pearson, los cuatro meses posteriores a la devaluación dominarían todas las correlaciones de Milei. Las variables son mensuales: inflación, depreciación del oficial, brecha cambiaria (nivel), variación del salario real y nominal privado registrado, variación del EMAE, variación de las reservas, variación del riesgo país (logarítmica, promedio mensual) y resultado primario (% del PBI, 12 meses).

![Matriz de correlaciones](figuras/B01_correlaciones.png)

**Figura #. Matriz de correlaciones de Spearman, toda la muestra y por gobierno.**

**Tabla #. Correlaciones de Spearman, gobierno de Milei**

{{corr_Milei}}

**Tabla #. Correlaciones de Spearman, toda la muestra (may-2016 a sep-2026)**

{{corr_Total}}

Tres resultados de la matriz son robustos en los tres gobiernos y en toda la muestra. El primero es la relación entre **inflación y salario nominal** (ρ de {{rho_Total_infl_m_dn_sal_priv_reg}} en toda la muestra, {{rho_Milei_infl_m_dn_sal_priv_reg}} con Milei): los salarios en pesos siguen a los precios, y cuanto más alta es la inflación más frecuentes y grandes son los aumentos. El segundo, la relación entre **inflación y brecha** ({{rho_Total_infl_m_brecha}} en toda la muestra), que se analiza abajo. El tercero, la correlación negativa entre **inflación y salario real** ({{rho_Total_infl_m_d_sal_priv_reg}}): los meses de inflación alta son meses de pérdida real.

Las diferencias entre gobiernos son tan informativas como las similitudes. Con Macri la correlación entre inflación y salario real es fuerte ({{rho_Macri_infl_m_d_sal_priv_reg}}) y entre inflación y salario nominal, débil ({{rho_Macri_infl_m_dn_sal_priv_reg}}): las paritarias eran anuales, de modo que un salto de inflación se trasladaba casi entero al salario real. Con Fernández y con Milei ocurre lo contrario (inflación y salario nominal con ρ de {{rho_Fernández_infl_m_dn_sal_priv_reg}} y {{rho_Milei_infl_m_dn_sal_priv_reg}}; inflación y salario real casi sin correlación): con inflación alta, los salarios se indexaron con revisiones cada pocos meses y absorbieron la inflación con menos pérdida mes a mes. Con Macri aparece además una correlación alta entre depreciación y riesgo país ({{rho_Macri_dep_oficial_d_log_rp}}), propia de las crisis cambiarias de 2018-2019, en las que el dólar y el riesgo país saltaban juntos.

Con Milei hay dos correlaciones nuevas. La **depreciación deja de correlacionarse con la inflación** (ρ de {{rho_Milei_infl_m_dep_oficial}}, contra {{rho_Fernández_infl_m_dep_oficial}} con Fernández): con un crawling peg fijo de 2% durante 2024 la depreciación casi no varió, mientras la inflación bajaba de 25% a 3%, y desde abril de 2025 el dólar se movió sin que la inflación lo acompañara. Y el **resultado primario se correlaciona negativamente con la inflación** ({{rho_Milei_infl_m_res_primario}}) y con la brecha ({{rho_Milei_brecha_res_primario}}): los meses de mayor superávit son los de menor inflación. Es la relación que predice la teoría fiscal de la inflación, pero también la que produciría una correlación espuria entre dos series con tendencia opuesta durante el mismo año y medio. Con Macri la misma correlación tiene signo contrario ({{rho_Macri_infl_m_res_primario}}): el déficit bajaba mientras la inflación subía. La matriz sola no puede distinguir entre ambas interpretaciones; esa es tarea del modelo.

### 6.2 Pares seleccionados

La tabla siguiente informa, para diez pares de variables con una relación económica conocida, la correlación lineal de Pearson (r), la de rangos de Spearman (ρ) y sus p-valores (H0: correlación nula), por gobierno y para toda la muestra. Comparar las dos columnas es en sí un diagnóstico: cuando r es alta y ρ baja, la correlación la producen unos pocos valores extremos.

**Tabla #. Correlaciones de pares seleccionados por gobierno**

{{tabla_pares}}

![Diagramas de dispersión](figuras/B02_dispersion.png)

**Figura #. Diagramas de dispersión de seis pares, con recta de mínimos cuadrados por gobierno.**

**Traspaso a precios (depreciación e inflación).** Con Fernández la correlación es alta y robusta (r = {{par_traspaso_a_precios_Fernández_r}}, ρ = {{par_traspaso_a_precios_Fernández_rho}}): en un régimen con cepo y brecha alta, cada aceleración del crawling peg o cada salto del oficial se trasladaba rápido a precios. Con Milei la r de Pearson es todavía más alta ({{par_traspaso_a_precios_Milei_r}}), pero la ρ de Spearman es {{par_traspaso_a_precios_Milei_rho}} (p = {{par_traspaso_a_precios_Milei_p}} para Pearson, no significativa para Spearman): **toda la correlación de Milei la producen diciembre de 2023 y enero de 2024**. Fuera de esos meses, depreciación e inflación no se movieron juntas: la inflación cayó con un dólar que subía 2% por mes y no repuntó con la flotación de 2025. Es el ejemplo más claro de todo el análisis de por qué hay que mirar ambas correlaciones. Con Macri la relación es débil (r = {{par_traspaso_a_precios_Macri_r}}, ρ = {{par_traspaso_a_precios_Macri_rho}}): con tipo de cambio flotante, sin brecha y con una inflación más baja, el traspaso fue menor y más lento.

**Inflación y salario.** Como se vio en la matriz, el salario real cae con la inflación con Macri (r = {{par_inflacion_y_salario_real_Macri_r}}) y casi no se relaciona con ella con Fernández ({{par_inflacion_y_salario_real_Fernández_r}}); con Milei, de nuevo, la r ({{par_inflacion_y_salario_real_Milei_r}}) la produce diciembre de 2023 y la ρ es casi cero ({{par_inflacion_y_salario_real_Milei_rho}}). El salario nominal, en cambio, acompaña a la inflación en los tres gobiernos y cada vez más: r de {{par_inflacion_y_salario_nominal_Macri_r}}, {{par_inflacion_y_salario_nominal_Fernández_r}} y {{par_inflacion_y_salario_nominal_Milei_r}}. Es la evidencia de la creciente indexación de la economía argentina, que hace más rápida la transmisión de la inflación a salarios en ambas direcciones: cuando la inflación sube, pero también cuando baja.

**Curva de Phillips (desocupación e inflación interanual, trimestral).** No hay una curva de Phillips estable: la correlación es positiva con Macri (r = {{par_curva_de_phillips_Macri_r}}, estanflación: en 2018-2019 subieron juntas la inflación y la desocupación), negativa con Fernández ({{par_curva_de_phillips_Fernández_r}}, la recuperación pospandemia bajó la desocupación mientras la inflación se aceleraba) y nula con Milei ({{par_curva_de_phillips_Milei_r}}, p = {{par_curva_de_phillips_Milei_p}}). Con Milei la inflación bajó de casi 300% a 31% interanual con una desocupación que se movió en un rango de un punto y medio: la desinflación no tuvo el costo en desempleo que sugiere una curva de Phillips tradicional, aunque sí lo tuvo en salario real y actividad durante 2024. Es coherente con un cambio de expectativas por el ancla fiscal más que con un enfriamiento de la demanda.

**Ley de Okun (crecimiento del PBI y cambio de la desocupación, trimestral).** Es la relación más estable de todo el análisis: negativa y significativa en los tres gobiernos (r = {{par_ley_de_okun_Macri_r}}, {{par_ley_de_okun_Fernández_r}} y {{par_ley_de_okun_Milei_r}}) y en toda la muestra ({{par_ley_de_okun_Total_r}}). Los trimestres de crecimiento son trimestres de baja de la desocupación. En la figura, la recta de Milei está desplazada hacia arriba respecto de las otras: para un mismo crecimiento del PBI, la desocupación bajó menos o subió más. Es lo esperable si el crecimiento se concentra en sectores poco intensivos en empleo (agro, minería, energía, finanzas), como mostró la sección 4.3.

**Disciplina fiscal y riesgo país.** Con Milei la relación tiene el signo esperado y es fuerte en Pearson (r = {{par_disciplina_fiscal_y_riesgo_Milei_r}}): más superávit, menos riesgo país. Pero con Macri es positiva y todavía más fuerte ({{par_disciplina_fiscal_y_riesgo_Macri_r}}): el déficit primario bajaba mientras el riesgo país subía, porque la crisis de 2018-2019 fue de financiamiento externo y no de déficit primario. En toda la muestra la correlación es nula ({{par_disciplina_fiscal_y_riesgo_Total_r}}). Ambas series son I(1) (sección 7), así que estas correlaciones en niveles son exactamente el tipo de resultado que puede ser espurio; lo que muestran es que el resultado fiscal no alcanza, por sí solo, para explicar el riesgo país.

**Otros pares.** La brecha y la inflación están muy correlacionadas con Fernández (r = {{par_brecha_e_inflacion_Fernández_r}}) y con Milei ({{par_brecha_e_inflacion_Milei_r}}), y nada con Macri, que casi no tuvo brecha. Los precios regulados y la núcleo se mueven juntos con Fernández y Milei (r de {{par_regulados_y_nucleo_Fernández_r}} y {{par_regulados_y_nucleo_Milei_r}}), lo que indica que la política tarifaria acompañó a la inflación general en lugar de usarse como ancla independiente. La variación de las reservas y la del riesgo país no tienen correlación mensual en ningún gobierno, y la actividad y el salario real tienen una correlación positiva débil con Macri y con Milei (r de {{par_actividad_y_salario_real_Macri_r}} y {{par_actividad_y_salario_real_Milei_r}}).

### 6.3 Traspaso a precios con rezagos

La correlación contemporánea no capta que la depreciación puede trasladarse a precios con algunos meses de rezago. La correlación cruzada mide corr(inflación_t, depreciación_t−k) para rezagos k de 0 a 6 meses, por gobierno.

**Tabla #. Correlación cruzada entre la inflación y la depreciación rezagada k meses**

{{tabla_traspaso}}

![Traspaso](figuras/B03_traspaso.png)

**Figura #.** Con Fernández la correlación es alta y estable en todos los rezagos (Pearson entre {{ccp_Fernández_0}} y {{ccp_Fernández_3}}, Spearman entre {{ccs_Fernández_6}} y {{ccs_Fernández_2}}), con un máximo a los 2-3 meses: el traspaso era rápido y persistente, propio de una economía con indexación generalizada y expectativas de devaluación permanentes. Con Macri la correlación es máxima a 1 mes (Pearson {{ccp_Macri_1}}) y luego cae: traspaso rápido pero menos persistente. Con Milei, Pearson y Spearman cuentan historias opuestas en los primeros rezagos (Pearson {{ccp_Milei_0}} y Spearman {{ccs_Milei_0}} en el rezago 0): lo que Pearson ve es el shock de diciembre de 2023, que contamina todos los rezagos hasta 4 meses. Spearman, robusta a ese shock, muestra correlaciones nulas en los rezagos 0 a 2 y positivas a 5-6 meses ({{ccs_Milei_5}} y {{ccs_Milei_6}}), por encima de la banda de significatividad aproximada. Con 34 observaciones y tendencias comunes, esa correlación tardía no alcanza para afirmar un traspaso diferido; es una hipótesis para el modelo.

La conclusión práctica es que el traspaso del tipo de cambio a precios no es un parámetro fijo de la economía argentina: depende del régimen cambiario, de la brecha y de la credibilidad de la política. Un modelo que estime un único coeficiente de traspaso para toda la muestra estaría mezclando regímenes.

## 7. Preparación para el modelo econométrico

Esta sección no estima el modelo: describe las propiedades de las series que van a condicionar su especificación.

### 7.1 Estacionariedad: pruebas ADF y KPSS

Se usan dos pruebas con hipótesis nulas opuestas. La de Dickey-Fuller aumentada (ADF) tiene como nula que la serie tiene **raíz unitaria** (no es estacionaria); la KPSS tiene como nula que la serie **es estacionaria**. Usarlas juntas evita leer la falta de rechazo de una sola como prueba de lo contrario: una serie es I(0) si el ADF rechaza (p < 0,05) y el KPSS no rechaza (p > 0,05); tiene raíz unitaria si pasa lo inverso; y el resultado es ambiguo si ambas rechazan o ninguna. Los rezagos del ADF se eligen por el criterio de Akaike. "Det." indica los componentes deterministas (c: constante; ct: constante y tendencia). El p-valor del KPSS que informa statsmodels está acotado entre 0,01 y 0,10 porque se interpola en la tabla de Kwiatkowski et al. (1992).

**Tabla #. Pruebas de raíz unitaria, niveles y primeras diferencias**

{{tabla_raiz}}

- **Los niveles de las variables reales son no estacionarios.** El logaritmo del salario real (los tres), del tipo de cambio real y del riesgo país, y el resultado primario como % del PBI tienen raíz unitaria en niveles y son estacionarios en primeras diferencias: son I(1). Cualquier regresión entre ellas en niveles corre riesgo de ser espuria salvo que estén cointegradas; es lo que se advirtió en el análisis bivariado (resultado fiscal y riesgo país).
- **La inflación mensual está en el límite.** El ADF casi rechaza (p = 0,056) y el KPSS casi rechaza (p = 0,09): es el resultado "ambiguo" típico de una serie estacionaria con cambios de nivel. Perron (1989) mostró que un quiebre estructural no modelado sesga el ADF hacia no rechazar la raíz unitaria, así que la evidencia es compatible con una inflación I(0) alrededor de una media que cambió de régimen (ver 7.4). En primera diferencia es claramente I(0).
- **El log del IPC** tiene raíz unitaria en niveles y su diferencia (la inflación) es ambigua: con inflación alta y persistente el nivel de precios puede comportarse como I(2). Modelar la inflación y no el nivel de precios evita ese problema.
- **La depreciación mensual es I(0)** en niveles: es una tasa de variación sin tendencia.
- **Las series trimestrales (PBI e IBIF)** dan resultados débiles: con 42 observaciones y estacionalidad, las pruebas tienen poca potencia. El logaritmo del PBI es I(1); para el modelo conviene usar su variación interanual o la serie desestacionalizada.

### 7.2 Autocorrelación de la inflación mensual: ACF y PACF

![ACF y PACF](figuras/D10_acf_pacf_inflacion.png)

**Tabla #. Prueba de Ljung-Box de la inflación mensual (H0: no hay autocorrelación hasta el rezago indicado)**

{{tabla_ljungbox}}

**Figura #.** En niveles, la función de autocorrelación (ACF) decae lentamente y en forma monótona (0,85 en el primer rezago, significativa hasta el quinto), mientras que la autocorrelación parcial (PACF) se corta después de pocos rezagos: es significativa en los rezagos 1 (0,85), 2 (−0,17), 3 (0,38) y 4 (−0,25) y luego queda dentro de la banda. Ese patrón (ACF que decae, PACF que se corta) es la firma de un **proceso autorregresivo de orden bajo, AR(3) o AR(4)**. La Ljung-Box rechaza con holgura la ausencia de autocorrelación: la inflación de un mes predice la del siguiente (inercia inflacionaria). En primera diferencia aparece una autocorrelación negativa grande en el rezago 2 (−0,43), señal de que diferenciar una serie que es casi estacionaria introduce estructura artificial (sobrediferenciación): es otro argumento para modelar la inflación en niveles con quiebres, y no en diferencias.

### 7.3 Estacionalidad

Se estima un factor estacional por mes (o trimestre) como el promedio de la serie sin tendencia (la tendencia es una media móvil centrada de 12 meses o 4 trimestres), y se prueba con Kruskal-Wallis si todos los meses tienen la misma distribución. Kruskal-Wallis es la versión no paramétrica del ANOVA: compara rangos y no medias, lo que lo hace robusto a los valores extremos. Para la inflación se excluye la ventana de noviembre de 2023 a marzo de 2024: con ella adentro, diciembre aparece como el mes más inflacionario del año solo por la devaluación.

**Tabla #. Estacionalidad**

{{tabla_estacionalidad}}

![Estacionalidad](figuras/D11_estacionalidad.png)

**Figura #.** La inflación mensual tiene una estacionalidad moderada pero estadísticamente significativa (p = {{est_infl_p}}): marzo (inicio de clases, cambio de temporada de ropa) está {{est_infl_max}} puntos por encima de la tendencia y mayo a julio entre 0,7 y 0,85 por debajo. El gasto primario real tiene una estacionalidad enorme (+{{est_gasto_max}}% en diciembre y +17% en junio por el aguinaldo), que justifica trabajar con sumas de 12 meses o variaciones interanuales como en este análisis. El PBI sin desestacionalizar sube {{est_pib_max}}% en el segundo trimestre (cosecha gruesa) y cae {{est_pib_min}}% en el primero. Como control, el EMAE desestacionalizado no muestra estacionalidad residual (p = 0,22): la desestacionalización del INDEC funciona. Consecuencia para el modelo: la inflación mensual necesita dummies estacionales (al menos para marzo y el bloque mayo-julio) o un componente SARIMA.

### 7.4 Quiebres estructurales

Se usan tres pruebas complementarias.

1. **Test de Quandt-Andrews (QLR o sup-F).** Para cada fecha candidata, entre el 15% y el 85% de la muestra, se calcula el estadístico F de Chow de un cambio en los dos coeficientes de un AR(1) de la inflación (constante y persistencia). Como la fecha se elige donde el F es máximo, los valores críticos no son los de la F habitual sino los de Andrews (1993): 5,00 (10%), 5,86 (5%) y 7,78 (1%) para q = 2.
2. **Test de Chow en fechas elegidas a priori** (diciembre de 2023, devaluación y cambio de gobierno; abril de 2025, salida del cepo). Como las fechas no se eligen mirando los datos, valen los valores críticos F habituales.
3. **Test de Zivot-Andrews**: raíz unitaria con un quiebre en la constante en una fecha desconocida, que corrige el sesgo de Perron del ADF.

![Quiebres](figuras/D12_quiebres_inflacion.png)

**Tabla #. Test de Chow en fechas conocidas**

{{tabla_chow}}

**Tabla #. Test de Zivot-Andrews (H0: raíz unitaria sin quiebre)**

{{tabla_za}}

**Figura #. Estadístico F del QLR por fecha candidata y lectura de las pruebas.**

- El QLR encuentra un quiebre muy significativo en la dinámica de la inflación con máximo en **{{qlr_fecha}}** (F = {{qlr}}, por encima del valor crítico de 1%). La fecha es la que separa el shock de la devaluación (diciembre de 2023, que queda en el primer tramo) del proceso de desinflación (desde enero de 2024): el cambio de régimen no es tanto el salto de precios como la velocidad de convergencia posterior.
- El test de Chow **en diciembre de 2023 no rechaza** (p = 0,63) para el AR(1) de la inflación. No contradice al QLR: si diciembre de 2023 se asigna al segundo tramo, ese dato extremo (25,5% después de 12,8%) queda como un residuo enorme dentro del tramo nuevo y los coeficientes estimados de ambos tramos se parecen. Un mes desplazado cambia por completo la conclusión, lo que indica que el quiebre debe modelarse con una **dummy de impulso** para los meses de la devaluación más una **dummy de régimen** desde enero de 2024, y no solo con un corte de muestra.
- La salida del cepo (abril de 2025) no produce un quiebre detectable en la inflación ni en la depreciación mensual: en el gráfico se ve como un cambio de media (de {{infl_m_Milei_media}}% promedio de todo el gobierno a alrededor de 2,3% desde abril de 2025), pero esa baja ya venía ocurriendo antes.
- Las **medias** de la variación mensual del EMAE y del salario real privado no cambian en ninguna de las dos fechas (p > 0,8): lo que cambió con Milei en esas variables es su volatilidad y la forma de la distribución (un shock inicial y una recuperación), no su tendencia de largo plazo.
- Zivot-Andrews no rechaza la raíz unitaria para la inflación, el salario real ni el EMAE aun permitiendo un quiebre, y la rechaza en el límite (p = 0,049) para el tipo de cambio real con quiebre en la crisis de abril de 2018.

### 7.5 Qué modelo sugieren los datos

Resumiendo la evidencia de este análisis:

| Hallazgo descriptivo | Implicancia para el modelo |
|:---|:---|
| Inflación mensual persistente (PACF significativa en los rezagos 1 a 4), ADF/KPSS en el límite, quiebre en ene-24 | Modelo autorregresivo en niveles, AR(3)-AR(4), con dummy de impulso (dic-23 a feb-24) y dummy de régimen (desde ene-24) |
| Estacionalidad significativa de la inflación (marzo, mayo-julio) | Dummies mensuales o componente SARIMA(p,0,q)(1,0,0)₁₂ |
| Salarios reales, tipo de cambio real, riesgo país y resultado fiscal son I(1) | Trabajar en diferencias, o probar cointegración (Johansen) antes de usar niveles |
| Depreciación mensual I(0) con un salto discreto; traspaso a precios distinto en cada régimen (6.3) | Depreciación como regresor de la inflación, con coeficientes que cambian por régimen (interacción con dummies) y rezagos de 0 a 6 meses |
| Pearson y Spearman discrepan en los pares de Milei por los meses de la devaluación | Estimaciones robustas (excluir o modelar con dummies dic-23 a feb-24) y chequeos de sensibilidad |
| Ley de Okun estable, curva de Phillips inestable | La desocupación es más útil como variable de actividad que como determinante de la inflación |
| Colas pesadas (curtosis de 5 a 128) en inflación, depreciación y retornos | Errores robustos; en mercados, distribución t o GARCH |
| Errores estándar ingenuos subestiman la incertidumbre de las diferencias entre gobiernos | Regresiones con dummies de gobierno y errores Newey-West (HAC) |

**Propuesta para el modelo econométrico.** El modelo más adecuado a los datos es un **ARIMAX para la inflación mensual**: un AR(3) o AR(4) en niveles con dummies estacionales, una dummy de impulso para la devaluación y una dummy de régimen desde enero de 2024, más la depreciación mensual del oficial (contemporánea y rezagada, con coeficiente distinto por régimen cambiario) como regresor exógeno. Permite responder dos preguntas concretas: cuánto bajó la "inflación inercial" con el cambio de régimen y cuánto del salto de 2023-2024 fue traspaso del tipo de cambio. Como extensión, un **VAR en tasas de variación** (depreciación, inflación, variación del salario nominal y del EMAE, todas I(0)), identificado con un orden de Cholesky que va de lo más exógeno (tipo de cambio) a lo más endógeno (actividad), permitiría estimar el traspaso a precios y a salarios con funciones de impulso-respuesta. Con 125 observaciones mensuales un VAR de cuatro variables y dos o tres rezagos es estimable, pero no uno más grande. Para las comparaciones simples entre gobiernos alcanza una **regresión de cada variable sobre dummies de gobierno con errores HAC**, que formaliza las diferencias de medias de las tablas de este análisis. Un modelo de cambio de régimen de Markov (Hamilton, 1989) sería la alternativa si se quisiera que los datos fechen los regímenes en lugar de imponerlos.

## 8. Limitaciones del análisis descriptivo

- **Períodos desiguales.** Milei lleva menos de tres años, contra cuatro de sus antecesores, y su período incluye a la vez el costo de la estabilización (2024) y el rebote (2025). Las estadísticas de cada gobierno resumen ciclos distintos.
- **Herencia y contexto.** La asignación por gobierno es contable, no causal: la inflación de diciembre de 2023 se registra en el período de Milei aunque refleje precios reprimidos heredados, y la sequía de 2023 y la pandemia de 2020 no son decisiones de política. Separar efecto gobierno de efecto contexto es tarea del modelo, no de la estadística descriptiva.
- **Macri incompleto.** Faltan los primeros meses del gobierno de Macri en las series de precios y salarios, que fueron de inflación alta, y los ADRs y los bonos empiezan en 2019 y 2021.
- **Pocas observaciones en las series trimestrales y semestrales.** Con 10 trimestres o 5 semestres por gobierno, asimetría, curtosis y tablas de frecuencias son muy inestables y deben leerse solo como descripción.
- **Correlación no es causalidad.** Las correlaciones de la sección 6 describen co-movimientos; en series con tendencia pueden ser espurias, y ninguna permite atribuir un efecto a una política.
- **Revisiones.** El INDEC revisa el EMAE y las cuentas nacionales con cada publicación; los datos están congelados a octubre de 2026.

## Referencias

- Andrews, D. W. K. (1993). Tests for parameter instability and structural change with unknown change point. *Econometrica*, 61(4), 821-856.
- Dickey, D. A. y Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association*, 74(366), 427-431.
- Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357-384.
- Kruskal, W. H. y Wallis, W. A. (1952). Use of ranks in one-criterion variance analysis. *Journal of the American Statistical Association*, 47(260), 583-621.
- Kwiatkowski, D., Phillips, P. C. B., Schmidt, P. y Shin, Y. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root. *Journal of Econometrics*, 54(1-3), 159-178.
- Ljung, G. M. y Box, G. E. P. (1978). On a measure of lack of fit in time series models. *Biometrika*, 65(2), 297-303.
- Okun, A. M. (1962). Potential GNP: its measurement and significance. *Proceedings of the Business and Economic Statistics Section*, American Statistical Association, 98-104.
- Perron, P. (1989). The great crash, the oil price shock, and the unit root hypothesis. *Econometrica*, 57(6), 1361-1401.
- Phillips, A. W. (1958). The relation between unemployment and the rate of change of money wage rates in the United Kingdom, 1861-1957. *Economica*, 25(100), 283-299.
- Spearman, C. (1904). The proof and measurement of association between two things. *The American Journal of Psychology*, 15(1), 72-101.
- Stock, J. H. y Watson, M. W. (2019). *Introduction to Econometrics* (4.ª ed.). Pearson. Tabla 14.5 (valores críticos del QLR).
- Sturges, H. A. (1926). The choice of a class interval. *Journal of the American Statistical Association*, 21(153), 65-66.
- Yule, G. U. (1926). Why do we sometimes get nonsense-correlations between time-series? *Journal of the Royal Statistical Society*, 89(1), 1-63.
- Zivot, E. y Andrews, D. W. K. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. *Journal of Business & Economic Statistics*, 10(3), 251-270.
- INDEC: Índice de Precios al Consumidor, Índice de Salarios, EMAE, Informe de Avance del Nivel de Actividad, Encuesta Permanente de Hogares (microdatos e informes de pobreza y de mercado de trabajo).
- Secretaría de Hacienda: Informe Mensual de Ingresos y Gastos (IMIG) del Sector Público Nacional no financiero, base caja.
- BCRA: API de Estadísticas Monetarias v4.0. Datos abiertos: [datos.gob.ar](https://datos.gob.ar), [ArgentinaDatos](https://argentinadatos.com), [data912](https://data912.com).
