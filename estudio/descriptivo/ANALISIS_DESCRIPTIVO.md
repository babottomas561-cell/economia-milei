# Capítulo 2. Análisis descriptivo de las variables

**La economía argentina bajo tres gobiernos: Macri (2015-2019), Fernández (2019-2023) y Milei (desde diciembre de 2023)**

> Este documento se genera con `uv run python estudio/descriptivo/descriptivo.py` a partir de `estudio/descriptivo/plantilla.md`. Las tablas y los números entre llaves de la plantilla los calcula el script con los datos congelados en `data/` (último dato: inflación de sep-26, actividad de julio de 2026, cuentas nacionales del segundo trimestre de 2026, cuentas fiscales de agosto de 2026 y mercados al 30/10/2026). El texto interpretativo se escribió sobre esos datos: si se actualizan, las tablas cambian solas pero conviene releer el texto.

## 2.1 Objetivo y criterios

Este capítulo describe, una por una, las variables con las que el estudio evalúa el desempeño económico del gobierno de Javier Milei. Para cada una se presenta qué mide, de dónde sale, por qué se eligió y qué limitaciones tiene. Después se resume su distribución con estadística descriptiva y gráficos, comparando a Milei con los dos gobiernos anteriores. El capítulo termina con las pruebas que preparan el modelo econométrico del capítulo siguiente: estacionariedad, autocorrelación, estacionalidad y quiebres estructurales. Acá no se estima ningún modelo causal: el objetivo es conocer los datos antes de modelarlos.

**Criterios comunes a todo el capítulo**

- **Períodos de gobierno.** Macri asumió el 10/12/2015, Fernández el 10/12/2019 y Milei el 10/12/2023. Cada observación se asigna al gobierno que estaba en el cargo en el **punto medio** del período que describe. Así, diciembre de 2023 es de Milei (asumió el día 10 y el mes incluye la devaluación del 13), pero el cuarto trimestre de 2023 y el segundo semestre de 2023 son de Fernández.
- **Muestra.** La mayoría de las series oficiales de datos.gob.ar que usa el estudio arrancan en enero de 2016. El IPC del INDEC se volvió a publicar en mayo de 2016 (después de la emergencia estadística declarada en enero de ese año), así que la inflación del gobierno de Macri empieza en mayo de 2016 y faltan sus primeros cinco meses, que incluyeron la salida del cepo de diciembre de 2015. **Las estadísticas de Macri son de un período incompleto y probablemente subestiman la inflación y la caída salarial de su primer año.**
- **Deflactor.** Las variables "reales" se deflactan mes a mes por el IPC nacional del INDEC (diciembre de 2016 = 100), extendido hacia atrás hasta abril de 2016 con las variaciones del IPC-GBA. La base de los índices reales es noviembre de 2023 = 100, el último mes completo del gobierno anterior.
- **Asimetría y curtosis.** Se reportan los estimadores muestrales corregidos de pandas. La curtosis es *en exceso*: 0 corresponde a una distribución normal, valores positivos indican colas más pesadas que la normal.
- **Coeficiente de variación.** CV = desvío / media × 100. Solo se informa cuando la variable es estrictamente positiva: en tasas de variación que cambian de signo (crecimiento del PBI, resultado fiscal) la media puede estar cerca de cero y el CV se vuelve arbitrariamente grande y no tiene interpretación.

## 2.2 Fichas técnicas de las variables

### Tabla resumen

| Dimensión | Variable | Fuente | Id / origen | Frecuencia | Unidad | Período |
|:---|:---|:---|:---|:---|:---|:---|
| Precios | Inflación mensual | INDEC (IPC) | ArgentinaDatos `finanzas/indices/inflacion` | Mensual | % mensual | may-16 a sep-26 |
| Precios | Nivel del IPC (y núcleo, regulados) | INDEC | `148.3_INIVELNAL_DICI_M_26`, `148.3_INUCLEONAL_DICI_M_19`, `148.3_IREGULANAL_DICI_M_22` | Mensual | Índice dic-16 = 100 | dic-16 a sep-26 |
| Ingresos | Salario privado registrado | INDEC (índice de salarios) | `149.1_SOR_PRIADO_OCTU_0_25` | Mensual | Índice oct-16 = 100, deflactado | abr-16 a jul-26 |
| Ingresos | Salario público | INDEC | `149.1_SOR_PUBICO_OCTU_0_14` | Mensual | Ídem | abr-16 a jul-26 |
| Ingresos | Salario no registrado | INDEC | `149.1_SOR_PRIADO_OCTU_0_28` (corrido −5 meses) | Mensual | Ídem | may-16 a feb-26 |
| Ingresos | Salario mínimo, vital y móvil | Ministerio de Trabajo | `57.1_SMVMM_0_M_34` | Mensual | $ por mes, deflactado | abr-16 a sep-26 |
| Actividad | EMAE desestacionalizado | INDEC | `143.3_NO_PR_2004_A_31` | Mensual | Índice 2004 = 100 | ene-16 a jul-26 |
| Actividad | PBI real | INDEC (cuentas nacionales) | `4.2_OGP_2004_T_17` | Trimestral | Millones de $ de 2004, tasa anual | T1-16 a T2-26 |
| Actividad | Inversión (IBIF) real | INDEC | `4.2_DGIT_2004_T_25` | Trimestral | Ídem | T1-16 a T2-26 |
| Actividad | PBI y componentes nominales | INDEC | `4.4_OGP_2004_T_17`, `4.4_DGCP_2004_T_27`, `4.4_DGCP_2004_T_30`, `4.4_DGI_2004_T_19`, `4.4_OGI_2004_T_25`, `4.4_DGT_2004_T_20`, `4.4_DE_2004_T_24`, `4.4_VE_2004_T_21` | Trimestral | Millones de $ corrientes, tasa anual | T1-16 a T2-26 |
| Fiscal | Resultado primario | Secretaría de Hacienda (IMIG) | `452.3_RESULTADO_RIO_0_M_18_54` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Intereses de la deuda | Hacienda | `452.3_INTERESES_TOS_0_M_15_62` | Mensual | Millones de $ | ene-16 a ago-26 |
| Fiscal | Gasto primario | Hacienda | `379.9_ING_PRIMAR017__36_12` − `379.9_SUPERAVIT_017__23_94` | Mensual | Millones de $ | ene-16 a ago-26 |
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

Todas las series de datos.gob.ar se descargan con `load_series` (`src/quantkit/data.py`), pidiendo por separado las mensuales y las trimestrales: si se mezclan frecuencias en una misma consulta, la API agrega en silencio todas las series a la frecuencia más baja.

### Precios

**Inflación mensual y nivel del IPC.** El Índice de Precios al Consumidor del INDEC mide la variación del costo de una canasta fija de bienes y servicios para los hogares de las seis regiones del país, con ponderaciones de la Encuesta de Gasto de los Hogares 2004/05. Se usa la variación mensual del nivel general y, para el deflactor, el índice en nivel; la inflación interanual se calcula como la variación del índice contra el mismo mes del año anterior.

- *Por qué se eligió.* La estabilización de precios fue el objetivo central y explícito del programa económico de Milei. Es también la variable que condiciona a todas las demás: el poder de compra del salario, el tipo de cambio real y el valor real del gasto público dependen de ella.
- *Limitaciones.* La canasta tiene más de veinte años y pondera poco los servicios y las tarifas, que fueron los precios que más subieron desde 2024: con ponderaciones actuales la inflación de 2024-2025 sería algo mayor. Entre enero y abril de 2016 no hay IPC del INDEC (la serie de ArgentinaDatos usa ahí el IPC de CABA, que este capítulo descarta). El dato de octubre de 2026 todavía no se publicó.

### Ingresos

**Salario real privado registrado, público y no registrado.** El Índice de Salarios del INDEC mide la evolución de los salarios de puestos de trabajo fijos (no del salario promedio), separando el sector privado registrado (asalariados con aportes, a partir de los registros del SIPA), el sector público y el sector privado no registrado (a partir de la EPH). Se deflacta por el IPC para obtener el salario real; en la sección 2.4.3 se usa además sin deflactar (salario nominal), para separar cuánto subieron los sueldos en pesos de cuánto subieron los precios.

- *Por qué se eligió.* Es la medida más directa del costo distributivo de la estabilización: la devaluación de diciembre de 2023 y la aceleración inflacionaria posterior se trasladan primero a salarios. Separar los tres sectores muestra quién pagó el ajuste: el empleo público es una variable de política fiscal, el privado registrado depende de paritarias y el no registrado del mercado.
- *Limitaciones.* El índice del sector no registrado se publica con cinco meses de rezago: el dato de cada mes describe salarios de cinco meses antes, por lo que acá se corre −5 meses para ubicarlo en el mes que corresponde (por eso termina en febrero de 2026). Esa serie surge de una muestra chica de la EPH y es mucho más volátil. El índice no capta cambios de composición del empleo (si se pierden puestos de salarios bajos, el promedio sube aunque nadie cobre más).

**Salario mínimo, vital y móvil (SMVM).** Monto mensual fijado por el Consejo del Salario; se deflacta por el IPC.

- *Por qué se eligió.* Es un precio que fija directamente el gobierno y funciona como referencia para planes sociales y para el salario informal más bajo. Mide una decisión de política, no un resultado de mercado.
- *Limitaciones.* Pocos asalariados registrados cobran exactamente el mínimo; su efecto sobre el salario efectivo es indirecto.

### Actividad e inversión

**EMAE.** El Estimador Mensual de Actividad Económica del INDEC aproxima mensualmente la evolución del PBI. Se usa la serie desestacionalizada (base 2004 = 100).

- *Por qué se eligió.* Es la única medida de actividad mensual, lo que da suficientes observaciones para comparar tres gobiernos y fechar el piso de la recesión (abril de 2024) y la desaceleración de 2026.
- *Limitaciones.* Se revisa con cada publicación; la desestacionalización del INDEC puede trasladar parte de los shocks (por ejemplo, la cuarentena de 2020) a los meses vecinos.

**PBI real e inversión (IBIF).** Producto interno bruto e inversión bruta interna fija trimestrales de las cuentas nacionales, a precios de 2004, sin desestacionalizar. Se usa la variación interanual del trimestre (que elimina la estacionalidad) y la tasa de inversión (IBIF / PBI a precios corrientes, suma de cuatro trimestres).

- *Por qué se eligió.* El PBI es la medida estándar del desempeño agregado; la inversión es el componente que anticipa el crecimiento futuro y el más sensible a la confianza en el programa.
- *Limitaciones.* El INDEC publica cada trimestre **a tasa anual**: el valor anual es el promedio de los cuatro trimestres, no su suma. Con 42 trimestres en total y 10 de Milei, las pruebas estadísticas trimestrales tienen poca potencia. Los ponderadores de 2004 sobrestiman el peso de los bienes de inversión importados, cuyo precio relativo cayó mucho desde entonces: la tasa de inversión a precios de 2004 y a precios corrientes cuentan historias distintas (ver 2.4.4).

### Fiscal

**Resultado primario y financiero.** Resultado del Sector Público Nacional no financiero en base caja (Informe Mensual de Ingresos y Gastos de la Secretaría de Hacienda). El primario excluye los intereses de la deuda; el financiero los incluye. Se expresan como suma de 12 meses sobre el PBI nominal de los cuatro trimestres correspondientes (en agosto de 2026, el último PBI disponible, el del segundo trimestre).

- *Por qué se eligió.* El equilibrio fiscal ("déficit cero") fue el ancla del programa: es lo que permitió dejar de financiar al Tesoro con emisión.
- *Limitaciones.* Es base caja: los intereses capitalizados de las Lecaps se pagan junto con el capital al vencimiento y no aparecen como intereses, así que el resultado financiero luce mejor que el devengado. Abarca solo la Nación, no las provincias. Los primeros once meses de la suma móvil de Milei incluyen meses del gobierno anterior.

**Gasto primario y su composición por rubro.** Gasto primario total (ingresos primarios menos resultado primario) y sus principales rubros: jubilaciones y pensiones, asignaciones familiares y AUH, pensiones no contributivas, salarios, subsidios a la energía y al transporte, transferencias corrientes a provincias y gasto de capital (obra pública). Se mide como % del PBI (12 meses), como variación real interanual y como estructura porcentual del gasto de cada año.

- *Por qué se eligió.* El ajuste fiscal se hizo por el lado del gasto. La composición muestra dónde cayó (obra pública, subsidios) y qué rubros ganaron peso.
- *Limitaciones.* El rubro "Resto" es un residuo e incluye gastos de funcionamiento, otras transferencias y gastos no clasificados. Los subsidios al transporte tienen serie solo desde julio de 2022.

**Subsidios a la energía.** Transferencias corrientes al sector energético (CAMMESA, ENARSA y otros), que solo existen con frecuencia trimestral en datos.gob.ar. Se miden como % del PBI del trimestre.

- *Por qué se eligió.* Es el rubro donde la "corrección de precios relativos" (suba de tarifas) se traduce directamente en menor gasto.
- *Limitaciones.* Muy estacional (los subsidios suben en invierno por la importación de gas) y con pagos atrasados que se mueven de un trimestre a otro.

### Tipo de cambio

**Dólar oficial, depreciación mensual, tipo de cambio real y brecha.** Dólar mayorista de la Comunicación A 3500 del BCRA (promedio mensual), su variación mensual, el tipo de cambio real bilateral (oficial / IPC, nov-23 = 100) y la brecha con el contado con liquidación.

- *Por qué se eligió.* La devaluación de diciembre de 2023 (118% en un día) y la salida del cepo de abril de 2025 son los dos eventos cambiarios del período; el tipo de cambio es además el principal canal de traspaso a precios.
- *Limitaciones.* El tipo de cambio real no descuenta la inflación de Estados Unidos (alrededor de 3% anual) y es bilateral, no multilateral. El promedio mensual reparte un salto discreto (como el del 13/12/2023) entre dos meses.

### Mercados

**Riesgo país.** Spread del índice EMBI de JP Morgan para Argentina: diferencia de rendimiento entre los bonos soberanos argentinos en dólares y los del Tesoro de EEUU, en puntos básicos.

- *Por qué se eligió.* Resume en un número la probabilidad de default que asignan los inversores y determina el costo al que el país podría volver a financiarse en los mercados.
- *Limitaciones.* Depende también de la tasa de EEUU y del apetito global por riesgo emergente; no es solo una calificación del gobierno.

**Acciones (13 ADRs) y bonos soberanos (GD30, GD35, GD41).** Canasta equiponderada de las acciones argentinas que cotizan en Nueva York (precio ajustado por dividendos) y una cartera equiponderada de los tres Globales más líquidos de la reestructuración de 2020, medida por retorno total (precio + cupones + amortizaciones). Para la estadística descriptiva se usa el retorno logarítmico diario en %.

- *Por qué se eligió.* Los precios de mercado son la evaluación en tiempo real de las expectativas sobre el programa económico y, a diferencia de las estadísticas oficiales, no tienen rezago.
- *Limitaciones.* La canasta de ADRs está sesgada a bancos y energía. Los bonos de data912 empiezan en septiembre de 2021, así que la comparación con Fernández cubre solo su segunda mitad, y no hay datos de Macri.

### Social

**Pobreza.** Porcentaje de personas bajo la línea de pobreza (ingreso del hogar menor que la Canasta Básica Total), EPH de 31 aglomerados urbanos, por semestre. Los valores se toman de los comunicados semestrales del INDEC; los de S2-2025 (28,2%) y S1-2026 (32,3%) del comunicado del 24/9/2026.

- *Por qué se eligió.* Es el indicador social más seguido y el que mejor refleja el efecto combinado de inflación, salarios y transferencias sobre los hogares.
- *Limitaciones.* Solo 20 observaciones en diez años; cubre solo población urbana; la EPH subdeclara ingresos.

**Desocupación.** Desocupados sobre población económicamente activa, EPH, por trimestre.

- *Por qué se eligió.* Completa la lectura del mercado de trabajo: el salario real puede subir porque se pierden los empleos peor pagos.
- *Limitaciones.* Es estacional (más alta en el primer trimestre), por lo que conviene comparar trimestres iguales. No capta la precarización (empleo no registrado, monotributo).

## 2.3 Panorama: las series largas

Antes de resumir cada variable en una tabla conviene mirarlas en el tiempo. En los tres gráficos siguientes el fondo marca el gobierno (amarillo Macri, verde Fernández, azul Milei) y las líneas punteadas numeradas, los eventos: 1 PASO de 2019, 2 vuelta del cepo, 3 cuarentena, 4 legislativas de 2021, 5 balotaje de 2023, 6 devaluación de diciembre de 2023, 7 salida del cepo, 8 elección en la provincia de Buenos Aires y 9 legislativas de 2025.

![Precios y salarios](figuras/D01_series_precios_salarios.png)

**Figura 2.1.** La inflación mensual tiene tres tramos nítidos: un nivel de 1% a 4% con Macri (con saltos en 2018 y después de las PASO de 2019), una aceleración casi continua con Fernández hasta 12,8% en octubre de 2023, y con Milei un pico de 25,5% en diciembre de 2023 seguido de una desinflación muy rápida que se detiene en torno a 2% mensual desde mediados de 2025. La interanual, en escala logarítmica, muestra lo mismo sin el ruido mensual: 289% en abril de 2024 y alrededor de 31-33% desde entonces. Los salarios reales del panel inferior cuentan otra historia: la caída es de larga data (el privado registrado venía de 120-127 en 2017), con un escalón abrupto en diciembre de 2023 que el sector privado recuperó a lo largo de 2024 y el sector público no. El salario no registrado es la serie más volátil y la única que con Milei supera su nivel de 2023. El salario mínimo real cae en cada gobierno y se desploma en el actual; el tipo de cambio real salta con la devaluación y vuelve a la zona de 100 en 2025-2026: la apreciación real borró la devaluación.

![Actividad, fiscal y social](figuras/D02_series_actividad_fiscal_social.png)

**Figura 2.2.** La actividad mensual (EMAE) no tiene tendencia de largo plazo: oscila alrededor de 100 durante diez años, con la caída de la cuarentena (marzo-abril de 2020) como único valor extremo. La inversión amplifica los ciclos del PBI: cae y sube entre dos y cuatro veces más que el producto en cada episodio. El resultado fiscal es la serie con el cambio de nivel más claro de todo el estudio: del rango −2% a −6% del PBI a un superávit primario de 1% a 2% sostenido desde 2024. La pobreza tiene un pico en el primer semestre de 2024 y cae a mínimos de la serie en el segundo de 2025; la desocupación se mueve en un rango más estrecho.

![Mercados](figuras/D03_series_mercados.png)

**Figura 2.3.** Las variables de mercado reaccionan a los eventos políticos con más claridad que las macroeconómicas: el riesgo país salta con las PASO de 2019 (evento 1) y vuelve a subir antes de la elección de Buenos Aires de septiembre de 2025 (evento 8); la canasta de ADRs pierde la mitad de su valor en un día después de esas PASO y se multiplica por cuatro entre fines de 2023 y enero de 2025. La brecha cambiaria, cero mientras no hay cepo, llega a 150% en 2023 y se cierra con la salida del cepo (evento 7), el mismo mes del salto de reservas por el desembolso del FMI.

## 2.4 Estadística descriptiva por variable

Cada tabla resume la variable para cada gobierno y para toda la muestra. Las columnas son: número de observaciones (N), media, mediana, desvío estándar, mínimo, máximo, coeficiente de variación, asimetría y curtosis en exceso.

### 2.4.1 Inflación

**Tabla 2.1. Inflación mensual (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | 2,75 | 2,60 | 1,34 | 0,20 | 6,50 | 48,69 | 0,80 | 0,74 |
| Fernández | dic-19 a nov-23 | 48 | 5,01 | 4,05 | 2,72 | 1,50 | 12,80 | 54,35 | 1,32 | 1,84 |
| Milei | dic-23 a sep-26 | 34 | 4,61 | 2,70 | 5,37 | 1,50 | 25,50 | 116,68 | 2,88 | 8,22 |
| Toda la muestra | may-16 a sep-26 | 125 | 4,12 | 3,10 | 3,48 | 0,20 | 25,50 | 84,50 | 3,32 | 14,84 |

La media de la inflación mensual con Milei (4,61%) es casi igual a la de Fernández (5,01%), pero la comparación de medias es engañosa: la **mediana** de Milei (2,70%) está mucho más cerca de la de Macri (2,60%) que de la de Fernández (4,05%). La diferencia entre media y mediana, la asimetría de 2,88 y la curtosis de 8,22 dicen lo mismo: la distribución de Milei es una masa de meses de 1,5% a 4% más una cola de muy pocos meses extremos (diciembre de 2023 a marzo de 2024). Es el caso típico en el que la mediana describe mejor el "mes típico" que la media. El CV de Milei (116,68%) duplica el de los gobiernos anteriores: es el período con la inflación menos estable, aunque esa inestabilidad se concentra al principio. Para toda la muestra la curtosis de 14,8 indica colas mucho más pesadas que una normal, algo a tener en cuenta en el modelo (errores no normales).

**Tabla 2.2. Inflación interanual (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | abr-17 a nov-19 | 32 | 37,7 | 32,8 | 13,7 | 21,4 | 57,3 | 36,4 | 0,17 | -1,84 |
| Fernández | dic-19 a nov-23 | 48 | 69,1 | 52,4 | 32,6 | 35,8 | 160,9 | 47,3 | 1,13 | 0,27 |
| Milei | dic-23 a sep-26 | 34 | 114,2 | 45,4 | 102,0 | 31,3 | 289,4 | 89,2 | 0,72 | -1,31 |
| Toda la muestra | abr-17 a sep-26 | 114 | 73,7 | 50,4 | 66,4 | 21,4 | 289,4 | 90,0 | 2,06 | 3,41 |

La interanual "arrastra" doce meses, así que el gobierno de Milei hereda en sus primeros meses la inflación acumulada de 2023 y su media (114,2%) es la más alta de los tres. De nuevo, la mediana (45,4%) es menor que la de Fernández. La curtosis negativa de Macri y Milei (distribuciones "achatadas" o bimodales) refleja que en ambos períodos la inflación interanual pasó por dos niveles distintos: la media resume mal una serie con tendencia.

**Distribución de frecuencias de la inflación mensual.** Para comparar la forma de la distribución se agrupan los meses en intervalos comunes a los tres gobiernos, cerrados a izquierda y abiertos a derecha. Por la regla de Sturges (k = 1 + 3,322 log₁₀ N) corresponderían unos 6 intervalos por gobierno (Macri 6,4, Fernández 6,6, Milei 6,1); se usan 9 porque la cola de Milei recorre un rango diez veces mayor que el cuerpo de la distribución y con intervalos de igual ancho todo el gobierno de Macri caería en uno o dos. Por eso los intervalos se ensanchan en la cola (de 1 punto hasta 5%, luego 2,5, 5 y 15 puntos).

**Tabla 2.3. Macri (may-16 a nov-19)**

| Inflación mensual (%) | Marca de clase | Frec. absoluta | Frec. relativa (%) | Frec. abs. acumulada | Frec. rel. acumulada (%) |
|:---|---:|---:|---:|---:|---:|
| [0; 1) | 0,50 | 1 | 2,3 | 1 | 2,3 |
| [1; 2) | 1,50 | 12 | 27,9 | 13 | 30,2 |
| [2; 3) | 2,50 | 13 | 30,2 | 26 | 60,5 |
| [3; 4) | 3,50 | 10 | 23,3 | 36 | 83,7 |
| [4; 5) | 4,50 | 4 | 9,3 | 40 | 93,0 |
| [5; 7,5) | 6,25 | 3 | 7,0 | 43 | 100,0 |
| [7,5; 10) | 8,75 | 0 | 0,0 | 43 | 100,0 |
| [10; 15) | 12,50 | 0 | 0,0 | 43 | 100,0 |
| [15; 30) | 22,50 | 0 | 0,0 | 43 | 100,0 |
| **Total** |  | 43 | 100,0 |  |  |

**Tabla 2.4. Fernández (dic-19 a nov-23)**

| Inflación mensual (%) | Marca de clase | Frec. absoluta | Frec. relativa (%) | Frec. abs. acumulada | Frec. rel. acumulada (%) |
|:---|---:|---:|---:|---:|---:|
| [0; 1) | 0,50 | 0 | 0,0 | 0 | 0,0 |
| [1; 2) | 1,50 | 3 | 6,2 | 3 | 6,2 |
| [2; 3) | 2,50 | 7 | 14,6 | 10 | 20,8 |
| [3; 4) | 3,50 | 12 | 25,0 | 22 | 45,8 |
| [4; 5) | 4,50 | 6 | 12,5 | 28 | 58,3 |
| [5; 7,5) | 6,25 | 13 | 27,1 | 41 | 85,4 |
| [7,5; 10) | 8,75 | 4 | 8,3 | 45 | 93,8 |
| [10; 15) | 12,50 | 3 | 6,2 | 48 | 100,0 |
| [15; 30) | 22,50 | 0 | 0,0 | 48 | 100,0 |
| **Total** |  | 48 | 100,0 |  |  |

**Tabla 2.5. Milei (dic-23 en adelante)**

| Inflación mensual (%) | Marca de clase | Frec. absoluta | Frec. relativa (%) | Frec. abs. acumulada | Frec. rel. acumulada (%) |
|:---|---:|---:|---:|---:|---:|
| [0; 1) | 0,50 | 0 | 0,0 | 0 | 0,0 |
| [1; 2) | 1,50 | 7 | 20,6 | 7 | 20,6 |
| [2; 3) | 2,50 | 15 | 44,1 | 22 | 64,7 |
| [3; 4) | 3,50 | 3 | 8,8 | 25 | 73,5 |
| [4; 5) | 4,50 | 4 | 11,8 | 29 | 85,3 |
| [5; 7,5) | 6,25 | 0 | 0,0 | 29 | 85,3 |
| [7,5; 10) | 8,75 | 1 | 2,9 | 30 | 88,2 |
| [10; 15) | 12,50 | 2 | 5,9 | 32 | 94,1 |
| [15; 30) | 22,50 | 2 | 5,9 | 34 | 100,0 |
| **Total** |  | 34 | 100,0 |  |  |

![Histogramas](figuras/D04_histogramas_inflacion.png)

**Figura 2.4.** Como los intervalos tienen anchos distintos, el histograma grafica la **densidad** (frecuencia relativa dividida por el ancho del intervalo): así el área de cada barra, y no su altura, es proporcional a la cantidad de meses. Las tablas de frecuencias acumuladas permiten leer los percentiles directamente: con Macri el 30% de los meses tuvo una inflación menor a 2%; con Fernández, el 6%; con Milei, el 21%. En el otro extremo, los meses con 5% o más fueron 7% del total con Macri, 42% con Fernández y 15% con Milei. La distribución de Fernández es la más "corrida a la derecha" y la más dispersa en el cuerpo; la de Milei es la más concentrada en el centro (el 44% de los meses entre 2% y 3%) y a la vez la única con valores por encima de 15%. Una media sola no puede describir esa forma.

### 2.4.2 Salarios

**Tabla 2.6. Salario real privado registrado (nov-23 = 100)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | abr-16 a nov-19 | 44 | 117,4 | 119,4 | 6,9 | 104,9 | 127,4 | 5,9 | -0,35 | -1,26 |
| Fernández | dic-19 a nov-23 | 48 | 103,8 | 103,1 | 2,4 | 100,0 | 111,8 | 2,3 | 1,62 | 2,99 |
| Milei | dic-23 a jul-26 | 32 | 96,7 | 98,3 | 3,9 | 87,9 | 100,7 | 4,1 | -1,31 | 0,59 |
| Toda la muestra | abr-16 a jul-26 | 124 | 106,8 | 104,1 | 9,6 | 87,9 | 127,4 | 9,0 | 0,56 | -0,45 |

**Tabla 2.7. Variación mensual del salario real privado registrado (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | -0,27 | -0,13 | 1,35 | -3,93 | 2,97 | – | -0,20 | 0,65 |
| Fernández | dic-19 a nov-23 | 48 | -0,08 | -0,28 | 1,77 | -3,65 | 6,15 | – | 1,06 | 2,45 |
| Milei | dic-23 a jul-26 | 32 | -0,08 | 0,09 | 2,37 | -11,50 | 3,36 | – | -3,62 | 18,09 |
| Toda la muestra | may-16 a jul-26 | 123 | -0,15 | -0,09 | 1,81 | -11,50 | 6,15 | – | -1,57 | 12,75 |

En niveles, cada gobierno tuvo un salario real privado más bajo que el anterior: 117,4 con Macri, 103,8 con Fernández y 96,7 con Milei (nov-23 = 100). La tabla de variaciones mensuales muestra que la media de los tres gobiernos es negativa o casi cero; lo que distingue a Milei es la forma: asimetría de -3,62 y curtosis de 18,09, por un único mes de caída extrema (−11,5% en diciembre de 2023) seguido de muchos meses de recuperación (la mediana, 0,09%, es la única positiva). Es un patrón de "shock y recomposición", distinto de la erosión gradual de los dos gobiernos anteriores.

**Tabla 2.8. Salario real público (nov-23 = 100)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | abr-16 a nov-19 | 44 | 121,4 | 123,4 | 8,0 | 106,0 | 132,1 | 6,6 | -0,35 | -1,29 |
| Fernández | dic-19 a nov-23 | 48 | 102,4 | 102,6 | 3,3 | 96,3 | 111,9 | 3,2 | 0,18 | 0,28 |
| Milei | dic-23 a jul-26 | 32 | 83,4 | 83,7 | 2,3 | 78,1 | 86,8 | 2,7 | -0,83 | 0,07 |
| Toda la muestra | abr-16 a jul-26 | 124 | 104,3 | 103,8 | 15,7 | 78,1 | 132,1 | 15,1 | 0,11 | -0,99 |

**Tabla 2.9. Variación mensual del salario real público (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | -0,34 | -0,47 | 1,61 | -2,85 | 4,09 | – | 1,18 | 1,82 |
| Fernández | dic-19 a nov-23 | 48 | -0,09 | -0,39 | 2,56 | -5,72 | 8,02 | – | 0,90 | 2,04 |
| Milei | dic-23 a jul-26 | 32 | -0,48 | -0,29 | 3,36 | -15,92 | 3,92 | – | -3,43 | 14,89 |
| Toda la muestra | may-16 a jul-26 | 123 | -0,28 | -0,37 | 2,51 | -15,92 | 8,02 | – | -1,56 | 12,81 |

El salario público tuvo el mismo shock inicial que el privado (−15,9% en un mes) pero sin la recuperación posterior: su nivel promedio con Milei (83,4) es el más bajo de la serie y su desvío (2,3) es chico, es decir, quedó estable en un nivel bajo. Es la variable que mejor muestra que el ajuste fiscal pasó en parte por la masa salarial del Estado.

**Tabla 2.10. Salario real no registrado (nov-23 = 100)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | 141,8 | 145,5 | 11,2 | 119,2 | 155,2 | 7,9 | -0,70 | -0,95 |
| Fernández | dic-19 a nov-23 | 48 | 114,1 | 113,8 | 5,5 | 100,0 | 124,1 | 4,8 | -0,10 | -0,16 |
| Milei | dic-23 a feb-26 | 27 | 111,1 | 116,4 | 21,0 | 80,7 | 141,6 | 18,9 | -0,11 | -1,52 |
| Toda la muestra | may-16 a feb-26 | 118 | 123,5 | 120,9 | 18,7 | 80,7 | 155,2 | 15,2 | -0,09 | -0,51 |

**Tabla 2.11. Variación mensual del salario real no registrado (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | jun-16 a nov-19 | 42 | -0,47 | -0,40 | 1,82 | -3,90 | 3,07 | – | -0,04 | -0,84 |
| Fernández | dic-19 a nov-23 | 48 | -0,34 | -0,14 | 2,33 | -6,39 | 5,07 | – | -0,42 | 0,83 |
| Milei | dic-23 a feb-26 | 27 | 1,37 | 2,32 | 3,73 | -10,89 | 6,54 | – | -2,30 | 5,99 |
| Toda la muestra | jun-16 a feb-26 | 117 | 0,01 | 0,22 | 2,66 | -10,89 | 6,54 | – | -0,96 | 2,87 |

El salario no registrado es la excepción: con Milei su variación mensual media es positiva (1,37% por mes, mediana 2,32%), contra caídas promedio en los dos gobiernos anteriores. Es también la serie más volátil (desvío de 3,73 puntos con Milei) y su CV en niveles (18,9%) cuadruplica el de los gobiernos previos, porque recorre todo el camino de 81 a 142 dentro del mismo período. La lectura económica es que el salario informal, sin paritarias, es el que más cae con la inflación alta y el que más rápido se recompone con la desinflación; la estadística, de muestra chica, pide cautela con cada dato aislado.

**Tabla 2.12. Salario mínimo real (nov-23 = 100)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | abr-16 a nov-19 | 44 | 132,3 | 136,8 | 14,2 | 104,6 | 153,5 | 10,7 | -0,34 | -1,19 |
| Fernández | dic-19 a nov-23 | 48 | 103,0 | 102,1 | 5,1 | 93,9 | 114,8 | 5,0 | 0,52 | -0,14 |
| Milei | dic-23 a sep-26 | 34 | 67,8 | 68,2 | 5,7 | 59,2 | 85,2 | 8,5 | 0,49 | 0,96 |
| Toda la muestra | abr-16 a sep-26 | 126 | 103,8 | 103,4 | 27,0 | 59,2 | 153,5 | 26,0 | 0,01 | -0,92 |

El salario mínimo real promedio con Milei (67,8) es la mitad del de Macri (132,3). A diferencia de los salarios de mercado, el mínimo no se recuperó después del shock de diciembre de 2023: cae de manera casi monótona hasta su mínimo de la serie (59,2) en el último dato.

### 2.4.3 Salario nominal contra salario real

El salario real es un cociente: lo que se cobra en pesos (salario nominal) dividido por lo que cuestan las cosas (IPC). Mirar el numerador por separado muestra *cómo* se llegó a cada resultado real: si el salario real cae porque los aumentos fueron chicos o porque la inflación fue grande. La relación exacta es

  (1 + variación real) = (1 + variación nominal) / (1 + inflación),

y por eso con inflación alta las dos tasas pueden ser enormes y el resultado real, chico: un aumento nominal de 300% puede ser una pérdida real si la inflación fue de 330%. Las series nominales son los mismos índices de la sección anterior sin deflactar, en la misma ventana de tiempo.

**Tabla 2.13. Variación mensual del salario nominal privado registrado (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | 2,45 | 2,45 | 1,03 | 0,75 | 4,75 | 42,10 | 0,29 | -0,87 |
| Fernández | dic-19 a nov-23 | 48 | 4,91 | 4,69 | 2,88 | -0,24 | 13,23 | – | 0,48 | 0,41 |
| Milei | dic-23 a jul-26 | 32 | 4,62 | 2,42 | 4,36 | 1,37 | 19,99 | 94,34 | 2,07 | 4,25 |
| Toda la muestra | may-16 a jul-26 | 123 | 3,98 | 3,28 | 3,11 | -0,24 | 19,99 | – | 2,07 | 6,08 |

**Tabla 2.14. Variación mensual del salario nominal público (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | 2,39 | 2,43 | 1,47 | 0,30 | 6,23 | 61,49 | 0,83 | 0,57 |
| Fernández | dic-19 a nov-23 | 48 | 4,91 | 3,87 | 3,44 | 0,52 | 16,31 | 70,15 | 1,30 | 1,80 |
| Milei | dic-23 a jul-26 | 32 | 4,15 | 3,12 | 3,40 | 0,93 | 15,11 | 82,13 | 1,78 | 3,02 |
| Toda la muestra | may-16 a jul-26 | 123 | 3,83 | 2,91 | 3,08 | 0,30 | 16,31 | 80,38 | 1,78 | 3,57 |

**Tabla 2.15. Variación mensual del salario nominal no registrado (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | jun-16 a nov-19 | 42 | 2,22 | 2,51 | 1,69 | -1,20 | 5,34 | – | -0,15 | -0,48 |
| Fernández | dic-19 a nov-23 | 48 | 4,63 | 4,47 | 2,73 | -0,50 | 11,24 | – | 0,23 | -0,70 |
| Milei | dic-23 a feb-26 | 27 | 6,48 | 5,73 | 3,25 | 0,14 | 15,08 | 50,06 | 0,58 | 0,70 |
| Toda la muestra | jun-16 a feb-26 | 117 | 4,19 | 3,73 | 3,01 | -1,20 | 15,08 | – | 0,74 | 0,65 |

**Tabla 2.16. Variación mensual del salario mínimo nominal (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | may-16 a nov-19 | 43 | 2,49 | 0,00 | 4,28 | 0,00 | 13,00 | – | 1,35 | 0,24 |
| Fernández | dic-19 a nov-23 | 48 | 4,73 | 3,54 | 5,37 | 0,00 | 19,90 | – | 1,19 | 0,82 |
| Milei | dic-23 a sep-26 | 34 | 2,94 | 1,78 | 3,57 | 0,00 | 15,38 | – | 2,23 | 4,76 |
| Toda la muestra | may-16 a sep-26 | 125 | 3,47 | 1,50 | 4,64 | 0,00 | 19,90 | – | 1,47 | 1,55 |

Los aumentos nominales mensuales siguen de cerca a la inflación de cada gobierno: el salario privado registrado subió en promedio 2,45% por mes con Macri, 4,91% con Fernández y 4,62% con Milei, contra una inflación media de 2,75%, 5,01% y 4,61%. Con Milei la media y la mediana (2,42%) se separan mucho, igual que en la inflación: los aumentos nominales más grandes de toda la serie (hasta 19,99% en un mes) llegaron en los meses posteriores a la devaluación, para recomponer lo perdido, y después se desaceleraron junto con los precios. El salario no registrado es el único con aumentos nominales mensuales mayores con Milei (6,48%) que con Fernández (4,63%), aun con menos inflación: es la contracara nominal de su recuperación real. El salario mínimo tiene una distribución particular: su mediana es baja (0% con Macri) porque se ajusta por decreto pocas veces al año y la mayoría de los meses no cambia; desde mediados de 2024 se ajusta casi todos los meses, pero por debajo de la inflación.

**Tabla 2.17. Descomposición de la variación de cada salario: nominal, inflación y real**

| Salario | Gobierno | Desde | Hasta | Nominal acum. (%) | Inflación acum. (%) | Real acum. (%) | Nominal anual (%) | Inflación anual (%) | Real anual (%) |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Privado registrado * | Macri | abr-16 | nov-19 | 182,6 | 219,3 | -11,5 | 33,6 | 38,3 | -3,3 |
| Privado registrado | Fernández | nov-19 | nov-23 | 882,3 | 930,7 | -4,7 | 77,0 | 79,2 | -1,2 |
| Privado registrado | Milei | nov-23 | jul-26 | 314,2 | 328,8 | -3,4 | 70,5 | 72,7 | -1,3 |
| Público * | Macri | abr-16 | nov-19 | 174,6 | 219,3 | -14,0 | 32,6 | 38,3 | -4,1 |
| Público | Fernández | nov-19 | nov-23 | 872,5 | 930,7 | -5,6 | 76,6 | 79,2 | -1,4 |
| Público | Milei | nov-23 | jul-26 | 261,0 | 328,8 | -15,8 | 61,9 | 72,7 | -6,3 |
| No registrado * | Macri | may-16 | nov-19 | 150,2 | 206,4 | -18,3 | 29,9 | 37,7 | -5,6 |
| No registrado | Fernández | nov-19 | nov-23 | 764,7 | 930,7 | -16,1 | 71,5 | 79,2 | -4,3 |
| No registrado | Milei | nov-23 | feb-26 | 438,7 | 280,5 | 41,6 | 111,1 | 80,9 | 16,7 |
| Salario mínimo * | Macri | abr-16 | nov-19 | 178,5 | 219,3 | -12,8 | 33,1 | 38,3 | -3,7 |
| Salario mínimo | Fernández | nov-19 | nov-23 | 765,2 | 930,7 | -16,1 | 71,5 | 79,2 | -4,3 |
| Salario mínimo | Milei | nov-23 | sep-26 | 162,9 | 344,2 | -40,8 | 40,6 | 69,3 | -16,9 |

![Salario nominal contra real](figuras/D13_salario_nominal_vs_real.png)

**Figura 2.5.** El panel izquierdo compara mes a mes los aumentos nominales con la inflación desde 2022: cuando la línea del salario queda debajo de la barra de inflación, el salario real cae ese mes. En diciembre de 2023 la brecha es máxima: precios +25,5% contra aumentos de 11,0% en el privado registrado y 5,5% en el público. Desde febrero de 2024 la relación se invierte y el salario privado supera a la inflación en 18 de los 31 meses siguientes, lo que explica su recuperación real a lo largo de 2024. El público también le gana a la inflación en la mitad de esos meses, pero por márgenes más chicos, y nunca recupera el escalón inicial. (El salario mínimo no se grafica en este panel porque se ajusta por escalones y tiene muchos meses con 0%.) El panel derecho resume cada gobierno en términos anualizados. Con Fernández los cuatro salarios subieron entre 71% y 77% nominal por año contra una inflación de 79%: perdieron poco por año pero de manera constante. Con Milei la dispersión entre salarios es mucho mayor que en los gobiernos anteriores: con una inflación de alrededor de 70-80% anual en la ventana de cada serie, el privado registrado subió 70,5% nominal por año (real -1,3%), el público 61,9% (real -6,3%), el no registrado 111,1% (real +16,7%) y el mínimo solo 40,6% (real -16,9%). Que el salario mínimo y el público, los dos que fija o negocia directamente el Estado, sean los que más quedaron atrás de la inflación es consistente con que la política salarial del sector público fue parte del ancla antiinflacionaria y del ajuste fiscal. La lección metodológica es que en una economía con inflación de tres dígitos una suba nominal "récord" no dice nada por sí sola: hay que compararla siempre con la inflación de la misma ventana.

### 2.4.4 Actividad e inversión

**Tabla 2.18. EMAE desestacionalizado (nov-23 = 100)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | ene-16 a nov-19 | 47 | 99,8 | 99,4 | 2,3 | 95,9 | 104,3 | 2,3 | 0,43 | -0,71 |
| Fernández | dic-19 a nov-23 | 48 | 97,2 | 99,4 | 6,9 | 72,5 | 105,4 | 7,1 | -1,57 | 2,80 |
| Milei | dic-23 a jul-26 | 32 | 102,5 | 103,5 | 3,1 | 96,4 | 107,1 | 3,0 | -0,63 | -0,76 |
| Toda la muestra | ene-16 a jul-26 | 127 | 99,5 | 100,3 | 5,1 | 72,5 | 107,1 | 5,1 | -2,14 | 7,36 |

**Tabla 2.19. Variación mensual del EMAE (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | feb-16 a nov-19 | 46 | -0,10 | 0,01 | 1,18 | -3,16 | 2,38 | – | -0,48 | 0,98 |
| Fernández | dic-19 a nov-23 | 48 | 0,14 | 0,38 | 3,45 | -15,64 | 10,55 | – | -1,94 | 11,35 |
| Milei | dic-23 a jul-26 | 32 | 0,08 | 0,11 | 1,40 | -2,90 | 2,73 | – | -0,25 | 0,09 |
| Toda la muestra | feb-16 a jul-26 | 126 | 0,04 | 0,08 | 2,34 | -15,64 | 10,55 | – | -2,22 | 20,63 |

El nivel medio de actividad con Milei (102,5) es el más alto de los tres gobiernos, aunque la diferencia es de pocos puntos: en diez años el EMAE se movió casi siempre entre 95 y 107. La variación mensual promedio es prácticamente cero en los tres casos (entre −0,1% y +0,1%); lo que cambia es la volatilidad, dominada en el gobierno de Fernández por la cuarentena de 2020 (mínimo de −15,6% y curtosis de 11,4). Sin la cuarentena, la actividad con Milei es tan volátil como con Macri: desvíos de 1,40 y 1,18 puntos.

**Tabla 2.20. PBI real, variación interanual del trimestre (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | T1-17 a T4-19 | 12 | -0,6 | -0,3 | 3,8 | -6,3 | 4,5 | – | -0,15 | -1,31 |
| Fernández | T1-20 a T4-23 | 16 | 1,3 | 1,7 | 9,1 | -18,9 | 18,7 | – | -0,31 | 0,61 |
| Milei | T1-24 a T2-26 | 10 | 1,7 | 2,3 | 3,6 | -5,1 | 6,5 | – | -0,55 | 0,12 |
| Toda la muestra | T1-17 a T2-26 | 38 | 0,8 | 1,4 | 6,5 | -18,9 | 18,7 | – | -0,20 | 2,23 |

**Tabla 2.21. Inversión (IBIF) real, variación interanual del trimestre (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | T1-17 a T4-19 | 12 | -2,3 | -2,9 | 16,3 | -25,1 | 20,2 | – | -0,06 | -1,47 |
| Fernández | T1-20 a T4-23 | 16 | 8,6 | 5,8 | 25,9 | -38,3 | 78,6 | – | 1,06 | 3,08 |
| Milei | T1-24 a T2-26 | 10 | -2,0 | -6,9 | 21,3 | -29,4 | 32,4 | – | 0,62 | -0,63 |
| Toda la muestra | T1-17 a T2-26 | 38 | 2,4 | 0,5 | 22,1 | -38,3 | 78,6 | – | 0,99 | 2,52 |

**Tabla 2.22. Tasa de inversión (IBIF / PBI, precios corrientes, 4 trimestres, %)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | T4-16 a T4-19 | 13 | 14,8 | 14,8 | 0,6 | 14,2 | 15,7 | 3,7 | 0,42 | -1,50 |
| Fernández | T1-20 a T4-23 | 16 | 16,5 | 17,2 | 1,9 | 13,0 | 18,5 | 11,2 | -0,91 | -0,65 |
| Milei | T1-24 a T2-26 | 10 | 16,4 | 16,4 | 0,5 | 15,5 | 17,3 | 2,8 | -0,22 | 1,09 |
| Toda la muestra | T4-16 a T2-26 | 39 | 15,9 | 16,0 | 1,5 | 13,0 | 18,5 | 9,1 | -0,09 | -0,92 |

La media del crecimiento interanual del PBI con Milei (1,7%) es la más alta, pero con 10 trimestres y un desvío de 3,6 puntos la diferencia con Fernández (1,3%, con el rebote de la pandemia adentro) no es estadísticamente distinguible. La inversión es entre tres y seis veces más volátil que el PBI en todos los gobiernos y con Milei su crecimiento interanual mediano es negativo (-6,9%). La tasa de inversión a precios corrientes es parecida con Fernández y con Milei (alrededor de 16,4%), mientras que a precios de 2004 cae de 20,8% a 18,1% (ver `estudio/results.md`): la diferencia es el precio relativo de los bienes de inversión, que con el dólar apreciado y la apertura importadora se abarataron frente al resto de la economía. La misma inversión física cuesta menos pesos, y la tasa nominal sube aunque la cantidad baje.

### 2.4.5 Cuentas fiscales

**Tabla 2.23. Gasto primario (% del PBI, 12 meses)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | dic-16 a nov-19 | 36 | 20,5 | 20,1 | 2,2 | 17,7 | 23,6 | 10,8 | 0,20 | -1,62 |
| Fernández | dic-19 a nov-23 | 48 | 20,1 | 20,1 | 1,7 | 17,7 | 23,6 | 8,3 | 0,62 | -0,47 |
| Milei | dic-23 a ago-26 | 33 | 14,6 | 14,4 | 1,0 | 13,6 | 18,3 | 6,9 | 2,22 | 5,60 |
| Toda la muestra | dic-16 a ago-26 | 117 | 18,7 | 18,9 | 3,1 | 13,6 | 23,6 | 16,5 | -0,14 | -1,02 |

**Tabla 2.24. Gasto primario real, variación interanual (%)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | abr-17 a nov-19 | 32 | -8,9 | -11,0 | 6,6 | -18,5 | 8,4 | – | 0,68 | -0,06 |
| Fernández | dic-19 a nov-23 | 48 | 3,4 | 1,6 | 14,6 | -24,3 | 42,5 | – | 0,62 | 0,64 |
| Milei | dic-23 a ago-26 | 33 | -9,8 | -6,8 | 15,9 | -41,2 | 24,9 | – | -0,14 | -0,44 |
| Toda la muestra | abr-17 a ago-26 | 113 | -3,9 | -4,7 | 14,7 | -41,2 | 42,5 | – | 0,41 | 1,11 |

**Tabla 2.25. Resultado primario (% del PBI, 12 meses)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | dic-16 a nov-19 | 36 | -2,73 | -2,98 | 1,14 | -4,17 | -0,53 | – | 0,52 | -1,01 |
| Fernández | dic-19 a nov-23 | 48 | -2,87 | -2,26 | 1,55 | -6,43 | -0,44 | – | -0,98 | 0,02 |
| Milei | dic-23 a ago-26 | 33 | 1,09 | 1,42 | 0,99 | -2,66 | 1,78 | – | -2,53 | 6,56 |
| Toda la muestra | dic-16 a ago-26 | 117 | -1,71 | -2,15 | 2,18 | -6,43 | 1,78 | – | 0,11 | -0,75 |

**Tabla 2.26. Resultado financiero (% del PBI, 12 meses)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | dic-16 a nov-19 | 36 | -5,11 | -5,15 | 0,63 | -5,94 | -3,77 | – | 0,46 | -0,84 |
| Fernández | dic-19 a nov-23 | 48 | -4,87 | -4,16 | 1,65 | -8,43 | -2,93 | – | -1,17 | -0,18 |
| Milei | dic-23 a ago-26 | 33 | -0,37 | 0,17 | 1,18 | -4,34 | 0,40 | – | -2,12 | 3,98 |
| Toda la muestra | dic-16 a ago-26 | 117 | -3,67 | -4,13 | 2,44 | -8,43 | 0,40 | – | 0,36 | -0,66 |

**Tabla 2.27. Subsidios a la energía (% del PBI del trimestre)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | T1-16 a T4-19 | 16 | 1,43 | 1,17 | 0,93 | 0,24 | 4,16 | 64,96 | 1,83 | 4,37 |
| Fernández | T1-20 a T4-23 | 16 | 1,90 | 1,99 | 0,60 | 1,06 | 3,08 | 31,35 | 0,24 | -0,87 |
| Milei | T1-24 a T2-26 | 10 | 0,82 | 0,79 | 0,37 | 0,28 | 1,41 | 45,72 | 0,43 | -0,60 |
| Toda la muestra | T1-16 a T2-26 | 42 | 1,47 | 1,31 | 0,81 | 0,24 | 4,16 | 55,23 | 1,07 | 1,67 |

Estas son las tablas con diferencias más grandes entre gobiernos. El gasto primario promedio pasa de alrededor de 20% del PBI con Macri y Fernández a 14,6% con Milei: más de cinco puntos del producto. El resultado primario medio cambia de signo (-2,73% con Macri, -2,87% con Fernández, 1,09% con Milei) y la mediana de Milei (1,42%) es más representativa que la media, porque el mínimo (-2,66%, en diciembre de 2023) es una suma de 12 meses que contiene once meses del gobierno anterior; eso explica también su asimetría negativa (-2,53). El resultado financiero promedio de Milei es levemente negativo por el mismo motivo, pero su mediana (0,17%) es positiva: es el único gobierno de la muestra con superávit financiero. Los subsidios energéticos son el rubro con la caída más clara: de 1,90% del PBI por trimestre con Fernández a 0,82% con Milei.

**Estructura del gasto (tortas).** Para ver la composición se usa el gasto de cada año completo en pesos corrientes: las participaciones no necesitan deflactarse, porque numerador y denominador están en la misma moneda del mismo año.

**Tabla 2.28. Estructura del gasto primario, 2023 y 2025 (% del total)**

| Rubro (% del gasto primario) | 2023 | 2025 | Cambio (pp) |
|:---|---:|---:|---:|
| Jubilaciones y pensiones | 33,3 | 44,1 | +10,8 |
| Asignaciones (AUH y familiares) | 4,4 | 7,4 | +3,1 |
| Pensiones no contributivas | 3,0 | 3,7 | +0,6 |
| Salarios del Estado nacional | 14,2 | 13,8 | -0,4 |
| Subsidios a la energía | 8,3 | 4,8 | -3,5 |
| Subsidios al transporte | 2,6 | 2,3 | -0,3 |
| Transferencias a provincias | 2,0 | 1,1 | -0,9 |
| Obra pública (gasto de capital) | 6,1 | 1,6 | -4,5 |
| Resto del gasto primario | 26,1 | 21,2 | -4,9 |

![Tortas del gasto](figuras/D07_tortas_gasto.png)

**Figura 2.6.** La composición del gasto cambió más que en cualquier otro momento de la serie. Las jubilaciones pasaron de un tercio a 44% del gasto primario y las asignaciones (AUH y familiares) de 4,4% a 7,4%. Esto **no** significa que se gastara más en jubilaciones: su gasto real cayó 4% entre 2023 y 2025 (ver `estudio/results.md`), pero el total cayó 26% y los rubros que más se recortaron (obra pública, de 6,1% a 1,6% del gasto; subsidios a la energía, de 8,3% a 4,8%) dejaron más espacio relativo a las prestaciones sociales. Es un buen ejemplo de por qué una torta debe leerse junto con el tamaño del total: una porción más grande de una torta más chica puede ser un monto menor.

**Composición de la demanda.** Para el PBI por componente se usan las cuentas nacionales a precios corrientes. Una torta necesita partes positivas que sumen el total, y el PBI no cumple eso por el lado de la demanda (las importaciones restan); por eso se grafica la composición de la demanda final, C + G + I + X, y las importaciones se informan aparte. Las exportaciones a precios corrientes se obtienen por identidad (demanda global menos el resto de sus componentes), porque esa serie viene vacía en la API.

**Tabla 2.29. Componentes de la demanda (% del PBI, precios corrientes)**

| Componente (% del PBI, precios corrientes) | 2017 | 2019 | 2023 | 2025 |
|:---|---:|---:|---:|---:|
| Consumo privado | 66,7 | 66,1 | 65,8 | 70,8 |
| Consumo público | 17,7 | 16,4 | 16,2 | 15,3 |
| Inversión (IBIF) | 15,2 | 14,2 | 18,4 | 16,6 |
| Exportaciones | 11,3 | 17,9 | 12,7 | 15,5 |
| Importaciones | 14,0 | 14,7 | 13,7 | 14,8 |
| Existencias y discrepancia | 3,1 | 0,0 | 0,6 | -3,4 |

![Tortas de la demanda](figuras/D08_tortas_demanda.png)

**Figura 2.7.** Entre 2023 y 2025 crece el peso del consumo privado (de 65,8% a 70,8% del PBI) y de las exportaciones (de 12,7% a 15,5%, por la normalización de la cosecha después de la sequía de 2023 y por Vaca Muerta), y bajan el consumo público (de 16,2% a 15,3%) y la inversión (de 18,4% a 16,6%). Las importaciones también suben (de 13,7% a 14,8%), en línea con la apertura comercial. La caída del consumo público en el PBI es la contraparte, en las cuentas nacionales, del ajuste fiscal de la Tabla 2.23.

### 2.4.6 Tipo de cambio

**Tabla 2.30. Depreciación mensual del dólar oficial (%, promedio mensual)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | dic-15 a nov-19 | 48 | 4,09 | 2,03 | 7,03 | -3,81 | 28,10 | – | 1,80 | 3,17 |
| Fernández | dic-19 a nov-23 | 48 | 3,82 | 3,02 | 3,33 | 0,01 | 20,89 | 87,01 | 2,98 | 13,96 |
| Milei | dic-23 a oct-26 | 35 | 4,92 | 2,05 | 14,12 | -2,74 | 81,44 | – | 5,07 | 27,24 |
| Toda la muestra | dic-15 a oct-26 | 131 | 4,22 | 2,24 | 8,61 | -3,81 | 81,44 | – | 6,16 | 50,47 |

**Tabla 2.31. Tipo de cambio real oficial (nov-23 = 100)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | abr-16 a nov-19 | 44 | 138,2 | 126,4 | 22,4 | 112,2 | 185,9 | 16,2 | 0,59 | -1,11 |
| Fernández | dic-19 a nov-23 | 48 | 142,4 | 140,8 | 23,4 | 100,0 | 173,3 | 16,4 | 0,03 | -1,65 |
| Milei | dic-23 a sep-26 | 34 | 111,0 | 107,1 | 13,2 | 95,8 | 152,8 | 11,9 | 1,60 | 2,86 |
| Toda la muestra | abr-16 a sep-26 | 126 | 132,5 | 123,4 | 24,5 | 95,8 | 185,9 | 18,5 | 0,49 | -1,10 |

La depreciación mensual mediana es casi igual con Macri y con Milei (alrededor de 2%) y más alta con Fernández (3%), pero Milei tiene la distribución más extrema de todo el capítulo: asimetría de 5,07 y curtosis de 27,24, por un único salto (la devaluación del 13/12/2023) seguido del "crawling peg" de 2% mensual y de la flotación entre bandas desde abril de 2025. Es el tipo de variable donde la media y el desvío describen mal el proceso: lo que hay es un régimen con un salto discreto. El tipo de cambio real promedio con Milei (111,0) es el más bajo de los tres gobiernos, es decir, el peso más apreciado en términos reales.

### 2.4.7 Mercados

**Tabla 2.32. Riesgo país (puntos básicos, diario)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | 10/12/15 a 09/12/19 | 1.132 | 723 | 513 | 518 | 342 | 2.532 | 72 | 2,26 | 3,97 |
| Fernández | 10/12/19 a 09/12/23 | 1.453 | 2.053 | 1.967 | 545 | 1.101 | 4.362 | 27 | 1,25 | 2,37 |
| Milei | 10/12/23 a 30/10/26 | 859 | 987 | 755 | 465 | 402 | 2.102 | 47 | 0,65 | -0,91 |
| Toda la muestra | 10/12/15 a 30/10/26 | 3.444 | 1.350 | 1.382 | 799 | 342 | 4.362 | 59 | 0,58 | -0,23 |

**Tabla 2.33. Retorno diario de la canasta de ADRs argentinos (%, logarítmico)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | 03/01/19 a 09/12/19 | 242 | -0,28 | 0,06 | 5,14 | -68,41 | 8,08 | – | -9,70 | 128,31 |
| Fernández | 10/12/19 a 08/12/23 | 1.030 | 0,05 | 0,00 | 2,87 | -17,69 | 19,36 | – | -0,01 | 5,65 |
| Milei | 11/12/23 a 30/10/26 | 744 | 0,08 | 0,00 | 3,01 | -19,69 | 29,16 | – | 1,16 | 14,37 |
| Toda la muestra | 03/01/19 a 30/10/26 | 2.016 | 0,02 | 0,00 | 3,27 | -68,41 | 29,16 | – | -4,19 | 99,31 |

**Tabla 2.34. Retorno diario total de la cartera GD30/GD35/GD41 (%, logarítmico)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fernández | 01/10/21 a 07/12/23 | 533 | 0,01 | -0,05 | 2,54 | -17,37 | 18,52 | – | 0,18 | 11,37 |
| Milei | 11/12/23 a 30/10/26 | 707 | 0,12 | 0,04 | 1,69 | -9,03 | 16,38 | – | 2,25 | 25,47 |
| Toda la muestra | 01/10/21 a 30/10/26 | 1.240 | 0,08 | 0,01 | 2,10 | -17,37 | 18,52 | – | 0,78 | 17,04 |

El riesgo país promedio con Milei (987 pb) es menos de la mitad del de Fernández (2.053 pb) y más alto que el de Macri (723 pb), cuya media está inflada por los meses posteriores a las PASO de 2019 (la mediana de Macri es 513 pb). Los retornos diarios tienen las colas más pesadas del capítulo: la curtosis de 128 de los ADRs en 2019 la produce un solo día, el 12/8/2019 (−68% logarítmico, la reacción a las PASO), y aun sin él las curtosis de 5 a 25 están lejos de la normal (0). Es la evidencia descriptiva de por qué los modelos de riesgo de mercado para activos argentinos usan distribuciones t de Student o volatilidad condicional (GARCH) en lugar de la normal. El retorno medio diario de los bonos con Milei (0,12% por día) es el más alto, con un desvío menor que con Fernández.

### 2.4.8 Indicadores sociales

**Tabla 2.35. Pobreza (% de personas, semestral)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | S2-16 a S2-19 | 7 | 30,7 | 30,3 | 3,8 | 25,7 | 35,5 | 12,5 | 0,19 | -1,49 |
| Fernández | S1-20 a S2-23 | 8 | 39,8 | 40,4 | 2,0 | 36,5 | 42,0 | 5,0 | -0,75 | -0,70 |
| Milei | S1-24 a S1-26 | 5 | 36,6 | 32,3 | 9,8 | 28,2 | 52,9 | 26,7 | 1,57 | 2,45 |
| Toda la muestra | S2-16 a S1-26 | 20 | 35,8 | 36,0 | 6,5 | 25,7 | 52,9 | 18,2 | 0,63 | 0,94 |

**Tabla 2.36. Desocupación (% de la PEA, trimestral)**

| Gobierno | Período | N | Media | Mediana | Desvío | Mín | Máx | CV (%) | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Macri | T2-16 a T4-19 | 15 | 9,0 | 9,1 | 0,9 | 7,2 | 10,6 | 9,8 | -0,34 | 0,46 |
| Fernández | T1-20 a T4-23 | 16 | 8,3 | 7,1 | 2,3 | 5,7 | 13,1 | 28,2 | 0,72 | -0,76 |
| Milei | T1-24 a T2-26 | 10 | 7,4 | 7,6 | 0,5 | 6,4 | 7,9 | 7,4 | -0,97 | -0,58 |
| Toda la muestra | T2-16 a T2-26 | 41 | 8,3 | 7,9 | 1,7 | 5,7 | 13,1 | 20,0 | 0,68 | 0,34 |

La pobreza media con Milei (36,6%) está entre la de Macri y la de Fernández, pero con solo 5 semestres y un recorrido de 52,9% a 28,2% la media no es un buen resumen: la mediana (32,3%) y el CV de 26,7%, el más alto de los tres, dicen que es el período con la pobreza más cambiante, con el pico y el mínimo de la década dentro del mismo gobierno. La desocupación media con Milei (7,4%) es la más baja de los tres gobiernos, pero conviene leerla con cuidado: la de Fernández incluye el pico de la pandemia (13,1% en el segundo trimestre de 2020), la serie es estacional y la comparación de medias no corrige cambios en la tasa de actividad ni en la calidad del empleo. Comparando trimestres iguales, la desocupación subió de 6,2% (T2-23) a 7,9% (T2-26).

## 2.5 Comparación entre gobiernos

### 2.5.1 Promedios por gobierno

![Barras de promedios](figuras/D05_barras_promedios.png)

**Figura 2.8.** Cada barra es la media del período y el segmento vertical, ± un error estándar (desvío / √N). Las barras resumen lo que ya mostraron las tablas: la mayor diferencia entre gobiernos está en el resultado fiscal; en la variación mensual del salario real privado los intervalos se superponen por completo; en el crecimiento del PBI los intervalos también se superponen. **Advertencia metodológica:** el error estándar así calculado supone observaciones independientes, y estas series son muy persistentes (ver la sección 2.6): los intervalos verdaderos son más anchos. Un test formal de diferencia de medias debería usar errores estándar robustos a autocorrelación (Newey-West), lo que se deja para el capítulo econométrico.

### 2.5.2 Variación acumulada y anualizada

La variación acumulada compara el último dato del gobierno anterior con el último dato del propio. Como los períodos tienen distinto largo (Milei lleva menos de tres años), se anualiza: (1 + variación acumulada)^(1/años) − 1. Las filas con asterisco no empiezan en el último dato del gobierno anterior porque la serie no existe antes (Macri).

**Tabla 2.37. Variación acumulada y anualizada por gobierno**

| Variable | Gobierno | Desde | Hasta | Años | Acumulada (%) | Anualizada (%) |
|:---|---:|---:|---:|---:|---:|---:|
| IPC (inflación) * | Macri | abr-16 | nov-19 | 3,6 | 219,3 | 38,3 |
| IPC (inflación) | Fernández | nov-19 | nov-23 | 4,0 | 930,7 | 79,2 |
| IPC (inflación) | Milei | nov-23 | sep-26 | 2,8 | 344,2 | 69,3 |
| Salario real privado registrado * | Macri | abr-16 | nov-19 | 3,6 | -11,5 | -3,3 |
| Salario real privado registrado | Fernández | nov-19 | nov-23 | 4,0 | -4,7 | -1,2 |
| Salario real privado registrado | Milei | nov-23 | jul-26 | 2,7 | -3,4 | -1,3 |
| Salario real público * | Macri | abr-16 | nov-19 | 3,6 | -14,0 | -4,1 |
| Salario real público | Fernández | nov-19 | nov-23 | 4,0 | -5,6 | -1,4 |
| Salario real público | Milei | nov-23 | jul-26 | 2,7 | -15,8 | -6,3 |
| Salario real no registrado * | Macri | may-16 | nov-19 | 3,5 | -18,3 | -5,6 |
| Salario real no registrado | Fernández | nov-19 | nov-23 | 4,0 | -16,1 | -4,3 |
| Salario real no registrado | Milei | nov-23 | feb-26 | 2,3 | 41,6 | 16,7 |
| Salario mínimo real * | Macri | abr-16 | nov-19 | 3,6 | -12,8 | -3,7 |
| Salario mínimo real | Fernández | nov-19 | nov-23 | 4,0 | -16,1 | -4,3 |
| Salario mínimo real | Milei | nov-23 | sep-26 | 2,8 | -40,8 | -16,9 |
| Actividad (EMAE) * | Macri | ene-16 | nov-19 | 3,8 | -4,7 | -1,3 |
| Actividad (EMAE) | Fernández | nov-19 | nov-23 | 4,0 | 3,9 | 1,0 |
| Actividad (EMAE) | Milei | nov-23 | jul-26 | 2,7 | 2,2 | 0,8 |
| PBI (4 trimestres) * | Macri | T4-16 | T4-19 | 3,0 | -1,9 | -0,6 |
| PBI (4 trimestres) | Fernández | T4-19 | T4-23 | 4,0 | 3,5 | 0,9 |
| PBI (4 trimestres) | Milei | T4-23 | T2-26 | 2,5 | 4,2 | 1,7 |
| Inversión (4 trimestres) * | Macri | T4-16 | T4-19 | 3,0 | -10,2 | -3,5 |
| Inversión (4 trimestres) | Fernández | T4-19 | T4-23 | 4,0 | 25,5 | 5,8 |
| Inversión (4 trimestres) | Milei | T4-23 | T2-26 | 2,5 | -9,7 | -4,0 |
| Dólar oficial real * | Macri | abr-16 | nov-19 | 3,6 | 29,8 | 7,6 |
| Dólar oficial real | Fernández | nov-19 | nov-23 | 4,0 | -42,5 | -12,9 |
| Dólar oficial real | Milei | nov-23 | sep-26 | 2,8 | -3,7 | -1,3 |
| Riesgo país | Macri | 09/12/15 | 09/12/19 | 4,0 | 340,4 | 44,9 |
| Riesgo país | Fernández | 09/12/19 | 09/12/23 | 4,0 | -11,9 | -3,1 |
| Riesgo país | Milei | 09/12/23 | 30/10/26 | 2,9 | -59,0 | -26,5 |

![Barras de variación](figuras/D06_barras_variacion_por_gobierno.png)

**Figura 2.9.** La inflación anualizada de Milei (69%) es menor que la de Fernández (79%) y mayor que la de Macri (38%, con sus primeros cinco meses fuera de la muestra), y está dominada por los primeros cuatro meses: anualizada, la inflación fue de 62% entre abril y diciembre de 2024, 31,5% en 2025 y 33% en los nueve meses de 2026. En términos reales, el patrón de Milei es el más heterogéneo: el salario no registrado sube 16,7% por año y el mínimo cae 16,9% por año; el salario público cae 6,3% anual, el privado registrado 1,3% (igual que con Fernández); el PBI crece 1,7% por año (el mejor de los tres) y la inversión cae 4% por año. El tipo de cambio real termina casi donde empezó (−1,3% anual) después de recorrer un salto de 50% y su reversión.

### 2.5.3 Boxplots

![Boxplots](figuras/D09_boxplots.png)

**Figura 2.10.** Los diagramas de caja permiten comparar posición, dispersión y valores atípicos al mismo tiempo. En la inflación, la caja de Milei (rango intercuartil) es la más angosta y está a la altura de la de Macri, y los meses de diciembre de 2023 a marzo de 2024 aparecen como **atípicos** (más de 1,5 rangos intercuartiles por encima del tercer cuartil). En el resultado primario la caja de Milei no se superpone con ninguna de las anteriores: es la única variable donde el cambio de régimen es visible incluso en la distribución completa. El riesgo país de Macri tiene una caja baja con muchos atípicos (los meses posteriores a las PASO); el de Milei tiene una caja muy alta, porque en su período el riesgo país bajó de 2.000 a 400 puntos y volvió a subir: una distribución con tendencia, no un nivel estable.

## 2.6 Preparación para el modelo econométrico

Esta sección no estima el modelo: describe las propiedades de las series que van a condicionar su especificación.

### 2.6.1 Estacionariedad: pruebas ADF y KPSS

Se usan dos pruebas con hipótesis nulas opuestas. La de Dickey-Fuller aumentada (ADF) tiene como nula que la serie tiene **raíz unitaria** (no es estacionaria); la KPSS tiene como nula que la serie **es estacionaria**. Usarlas juntas evita leer la falta de rechazo de una sola como prueba de lo contrario: una serie es I(0) si el ADF rechaza (p < 0,05) y el KPSS no rechaza (p > 0,05); tiene raíz unitaria si pasa lo inverso; y el resultado es ambiguo si ambas rechazan o ninguna. Los rezagos del ADF se eligen por el criterio de Akaike. "Det." indica los componentes deterministas (c: constante; ct: constante y tendencia). El p-valor del KPSS que informa statsmodels está acotado entre 0,01 y 0,10 porque se interpola en la tabla de Kwiatkowski et al. (1992).

**Tabla 2.38. Pruebas de raíz unitaria, niveles y primeras diferencias**

| Variable | Det. | N | ADF nivel (p) | KPSS nivel (p) | ADF dif. (p) | KPSS dif. (p) | Nivel | Diferencia |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|
| Inflación mensual (%) | c | 125 | -2,81 (0,056) | 0,37 (0,090) | -6,67 (0,000) | 0,09 (≥0,10) | ambiguo | I(0) |
| Inflación interanual (%) | c | 114 | -2,35 (0,156) | 0,46 (0,053) | -2,19 (0,209) | 0,12 (≥0,10) | ambiguo | ambiguo |
| log IPC | ct | 126 | -2,06 (0,566) | 0,38 (≤0,01) | -2,77 (0,063) | 0,38 (0,086) | raíz unitaria | ambiguo |
| log salario real privado registrado | c | 124 | -1,33 (0,614) | 1,55 (≤0,01) | -4,80 (0,000) | 0,05 (≥0,10) | raíz unitaria | I(0) |
| log salario real público | c | 124 | -1,15 (0,696) | 1,63 (≤0,01) | -5,59 (0,000) | 0,05 (≥0,10) | raíz unitaria | I(0) |
| log salario real no registrado | c | 118 | -1,81 (0,377) | 1,00 (≤0,01) | -4,16 (0,001) | 0,27 (≥0,10) | raíz unitaria | I(0) |
| log EMAE | c | 122 | -2,24 (0,191) | 0,39 (0,082) | -8,91 (0,000) | 0,05 (≥0,10) | ambiguo | I(0) |
| Depreciación mensual oficial (%) | c | 125 | -8,62 (0,000) | 0,17 (≥0,10) | -8,15 (0,000) | 0,12 (≥0,10) | I(0) | I(0) |
| log tipo de cambio real | c | 126 | -0,87 (0,799) | 0,77 (≤0,01) | -9,61 (0,000) | 0,16 (≥0,10) | raíz unitaria | I(0) |
| Resultado primario 12m (% PBI) | c | 117 | -1,97 (0,300) | 1,02 (≤0,01) | -4,30 (0,000) | 0,06 (≥0,10) | raíz unitaria | I(0) |
| log riesgo país (prom. mensual) | c | 130 | -1,49 (0,539) | 0,62 (0,021) | -8,25 (0,000) | 0,30 (≥0,10) | raíz unitaria | I(0) |
| log PBI real (trimestral) | ct | 42 | -2,77 (0,207) | 0,16 (0,040) | -2,72 (0,070) | 0,10 (≥0,10) | raíz unitaria | ambiguo |
| log IBIF real (trimestral) | ct | 42 | -3,28 (0,069) | 0,08 (≥0,10) | -5,86 (0,000) | 0,07 (≥0,10) | ambiguo | I(0) |

- **Los niveles de las variables reales son no estacionarios.** El logaritmo del salario real (los tres), del tipo de cambio real y del riesgo país, y el resultado primario como % del PBI tienen raíz unitaria en niveles y son estacionarios en primeras diferencias: son I(1). Cualquier regresión entre ellas en niveles corre riesgo de ser espuria salvo que estén cointegradas.
- **La inflación mensual está en el límite.** El ADF casi rechaza (p = 0,056) y el KPSS casi rechaza (p = 0,09): es el resultado "ambiguo" típico de una serie estacionaria con cambios de nivel. Perron (1989) mostró que un quiebre estructural no modelado sesga el ADF hacia no rechazar la raíz unitaria, así que la evidencia es compatible con una inflación I(0) alrededor de una media que cambió de régimen (ver 2.6.4). En primera diferencia es claramente I(0).
- **El log del IPC** tiene raíz unitaria en niveles y su diferencia (la inflación) es ambigua: con inflación alta y persistente el nivel de precios puede comportarse como I(2). Modelar la inflación y no el nivel de precios evita ese problema.
- **La depreciación mensual es I(0)** en niveles: es una tasa de variación sin tendencia.
- **Las series trimestrales (PBI e IBIF)** dan resultados débiles: con 42 observaciones y estacionalidad, las pruebas tienen poca potencia. El logaritmo del PBI es I(1); para el modelo conviene usar su variación interanual o la serie desestacionalizada.

### 2.6.2 Autocorrelación de la inflación mensual: ACF y PACF

![ACF y PACF](figuras/D10_acf_pacf_inflacion.png)

**Tabla 2.39. Prueba de Ljung-Box de la inflación mensual (H0: no hay autocorrelación hasta el rezago indicado)**

| Rezagos | Q nivel | p nivel | Q diferencia | p diferencia |
|:---|---:|---:|---:|---:|
| 6 | 288,4 | 0,0000 | 37,9 | 0,0000 |
| 12 | 333,1 | 0,0000 | 38,5 | 0,0001 |
| 24 | 343,7 | 0,0000 | 41,6 | 0,0144 |

**Figura 2.11.** En niveles, la función de autocorrelación (ACF) decae lentamente y en forma monótona (0,85 en el primer rezago, significativa hasta el quinto), mientras que la autocorrelación parcial (PACF) se corta después de pocos rezagos: es significativa en los rezagos 1 (0,85), 2 (−0,17), 3 (0,38) y 4 (−0,25) y luego queda dentro de la banda. Ese patrón (ACF que decae, PACF que se corta) es la firma de un **proceso autorregresivo de orden bajo, AR(3) o AR(4)**. La Ljung-Box rechaza con holgura la ausencia de autocorrelación: la inflación de un mes predice la del siguiente (inercia inflacionaria). En primera diferencia aparece una autocorrelación negativa grande en el rezago 2 (−0,43), señal de que diferenciar una serie que es casi estacionaria introduce estructura artificial (sobrediferenciación): es otro argumento para modelar la inflación en niveles con quiebres, y no en diferencias.

### 2.6.3 Estacionalidad

Se estima un factor estacional por mes (o trimestre) como el promedio de la serie sin tendencia (la tendencia es una media móvil centrada de 12 meses o 4 trimestres), y se prueba con Kruskal-Wallis si todos los meses tienen la misma distribución. Kruskal-Wallis es la versión no paramétrica del ANOVA: compara rangos y no medias, lo que lo hace robusto a los valores extremos. Para la inflación se excluye la ventana de noviembre de 2023 a marzo de 2024: con ella adentro, diciembre aparece como el mes más inflacionario del año solo por la devaluación.

**Tabla 2.40. Estacionalidad**

| Serie | Kruskal-Wallis H | p-valor | Mes/trimestre de mayor factor | Factor máximo |
|:---|---:|---:|---:|---:|
| Inflación mensual | 30,5 | 0,0013 | mar | 1,06 pp |
| Gasto primario real | 77,9 | 0,0000 | dic | 32,99 % |
| PBI real (sin desestacionalizar) | 20,3 | 0,0001 | T2 | 4,73 % |
| EMAE desestacionalizado (var. mensual) | 14,2 | 0,2225 | may | 1,08 pp |

![Estacionalidad](figuras/D11_estacionalidad.png)

**Figura 2.12.** La inflación mensual tiene una estacionalidad moderada pero estadísticamente significativa (p = 0,001): marzo (inicio de clases, cambio de temporada de ropa) está 1,1 puntos por encima de la tendencia y mayo a julio entre 0,7 y 0,85 por debajo. El gasto primario real tiene una estacionalidad enorme (+33,0% en diciembre y +17% en junio por el aguinaldo), que justifica trabajar con sumas de 12 meses o variaciones interanuales como en este capítulo. El PBI sin desestacionalizar sube 4,7% en el segundo trimestre (cosecha gruesa) y cae -2,9% en el primero. Como control, el EMAE desestacionalizado no muestra estacionalidad residual (p = 0,22): la desestacionalización del INDEC funciona. Consecuencia para el modelo: la inflación mensual necesita dummies estacionales (al menos para marzo y el bloque mayo-julio) o un componente SARIMA.

### 2.6.4 Quiebres estructurales

Se usan tres pruebas complementarias.

1. **Test de Quandt-Andrews (QLR o sup-F).** Para cada fecha candidata, entre el 15% y el 85% de la muestra, se calcula el estadístico F de Chow de un cambio en los dos coeficientes de un AR(1) de la inflación (constante y persistencia). Como la fecha se elige donde el F es máximo, los valores críticos no son los de la F habitual sino los de Andrews (1993): 5,00 (10%), 5,86 (5%) y 7,78 (1%) para q = 2.
2. **Test de Chow en fechas elegidas a priori** (diciembre de 2023, devaluación y cambio de gobierno; abril de 2025, salida del cepo). Como las fechas no se eligen mirando los datos, valen los valores críticos F habituales.
3. **Test de Zivot-Andrews**: raíz unitaria con un quiebre en la constante en una fecha desconocida, que corrige el sesgo de Perron del ADF.

![Quiebres](figuras/D12_quiebres_inflacion.png)

**Tabla 2.41. Test de Chow en fechas conocidas**

| Serie | Fecha del quiebre | F | p |
|:---|---:|---:|---:|
| Inflación mensual, AR(1) | dic-23 | 0,46 | 0,6313 |
| Inflación mensual, AR(1) | abr-25 | 0,45 | 0,6360 |
| Var. mensual del EMAE (media) | dic-23 | 0,00 | 0,9561 |
| Var. mensual del EMAE (media) | abr-25 | 0,01 | 0,9425 |
| Var. mensual salario real privado (media) | dic-23 | 0,06 | 0,8009 |
| Var. mensual salario real privado (media) | abr-25 | 0,00 | 0,9861 |
| Depreciación mensual oficial, AR(1) | dic-23 | 0,16 | 0,8486 |
| Depreciación mensual oficial, AR(1) | abr-25 | 0,55 | 0,5770 |

**Tabla 2.42. Test de Zivot-Andrews (H0: raíz unitaria sin quiebre)**

| Serie | ZA | p | VC 5% | Quiebre |
|:---|---:|---:|---:|---:|
| Inflación mensual | -4,47 | 0,127 | -4,81 | feb-24 |
| log salario real privado registrado | -4,07 | 0,309 | -4,81 | ago-18 |
| log EMAE | -3,20 | 0,839 | -4,81 | mar-18 |
| log tipo de cambio real | -4,82 | 0,049 | -4,81 | abr-18 |

**Figura 2.13 y lectura de las pruebas.**

- El QLR encuentra un quiebre muy significativo en la dinámica de la inflación con máximo en **ene-24** (F = 13,5, por encima del valor crítico de 1%). La fecha es la que separa el shock de la devaluación (diciembre de 2023, que queda en el primer tramo) del proceso de desinflación (desde enero de 2024): el cambio de régimen no es tanto el salto de precios como la velocidad de convergencia posterior.
- El test de Chow **en diciembre de 2023 no rechaza** (p = 0,63) para el AR(1) de la inflación. No contradice al QLR: si diciembre de 2023 se asigna al segundo tramo, ese dato extremo (25,5% después de 12,8%) queda como un residuo enorme dentro del tramo nuevo y los coeficientes estimados de ambos tramos se parecen. Un mes desplazado cambia por completo la conclusión, lo que indica que el quiebre debe modelarse con una **dummy de impulso** para los meses de la devaluación más una **dummy de régimen** desde enero de 2024, y no solo con un corte de muestra.
- La salida del cepo (abril de 2025) no produce un quiebre detectable en la inflación ni en la depreciación mensual: en el gráfico se ve como un cambio de media (de 4,61% promedio de todo el gobierno a alrededor de 2,3% desde abril de 2025), pero esa baja ya venía ocurriendo antes.
- Las **medias** de la variación mensual del EMAE y del salario real privado no cambian en ninguna de las dos fechas (p > 0,8): lo que cambió con Milei en esas variables es su volatilidad y la forma de la distribución (un shock inicial y una recuperación), no su tendencia de largo plazo.
- Zivot-Andrews no rechaza la raíz unitaria para la inflación, el salario real ni el EMAE aun permitiendo un quiebre, y la rechaza en el límite (p = 0,049) para el tipo de cambio real con quiebre en la crisis de abril de 2018.

### 2.6.5 Qué modelo sugieren los datos

Resumiendo la evidencia de este capítulo:

| Hallazgo descriptivo | Implicancia para el modelo |
|:---|:---|
| Inflación mensual persistente (PACF significativa en los rezagos 1 a 4), ADF/KPSS en el límite, quiebre en ene-24 | Modelo autorregresivo en niveles, AR(3)-AR(4), con dummy de impulso (dic-23 a feb-24) y dummy de régimen (desde ene-24) |
| Estacionalidad significativa de la inflación (marzo, mayo-julio) | Dummies mensuales o componente SARIMA(p,0,q)(1,0,0)₁₂ |
| Salarios reales, tipo de cambio real, riesgo país y resultado fiscal son I(1) | Trabajar en diferencias, o probar cointegración (Johansen) antes de usar niveles |
| Depreciación mensual I(0) con un salto discreto | Puede entrar como regresor de la inflación (traspaso a precios) |
| Colas pesadas (curtosis de 5 a 128) en inflación, depreciación y retornos | Errores robustos; en mercados, distribución t o GARCH |
| Errores estándar ingenuos subestiman la incertidumbre de las diferencias entre gobiernos | Regresiones con dummies de gobierno y errores Newey-West (HAC) |

**Propuesta para el capítulo econométrico.** El modelo más adecuado a los datos es un **ARIMAX para la inflación mensual**: un AR(3) o AR(4) en niveles con dummies estacionales, una dummy de impulso para la devaluación y una dummy de régimen desde enero de 2024, más la depreciación mensual del oficial (contemporánea y rezagada) como regresor exógeno. Permite responder dos preguntas concretas: cuánto bajó la "inflación inercial" con el cambio de régimen y cuánto del salto de 2023-2024 fue traspaso del tipo de cambio. Como extensión, un **VAR en tasas de variación** (depreciación, inflación, variación del salario nominal y del EMAE, todas I(0)), identificado con un orden de Cholesky que va de lo más exógeno (tipo de cambio) a lo más endógeno (actividad), permitiría estimar el traspaso a precios y a salarios con funciones de impulso-respuesta. Con 125 observaciones mensuales un VAR de cuatro variables y dos o tres rezagos es estimable, pero no uno más grande. Para las comparaciones simples entre gobiernos alcanza una **regresión de cada variable sobre dummies de gobierno con errores HAC**, que formaliza las diferencias de medias de las tablas de este capítulo. Un modelo de cambio de régimen de Markov (Hamilton, 1989) sería la alternativa si se quisiera que los datos fechen los regímenes en lugar de imponerlos.

## 2.7 Limitaciones del análisis descriptivo

- **Períodos desiguales.** Milei lleva menos de tres años, contra cuatro de sus antecesores, y su período incluye a la vez el costo de la estabilización (2024) y el rebote (2025). Las estadísticas de cada gobierno resumen ciclos distintos.
- **Herencia y contexto.** La asignación por gobierno es contable, no causal: la inflación de diciembre de 2023 se registra en el período de Milei aunque refleje precios reprimidos heredados, y la sequía de 2023 y la pandemia de 2020 no son decisiones de política. Separar efecto gobierno de efecto contexto es tarea del modelo, no de la estadística descriptiva.
- **Macri incompleto.** Faltan los primeros meses del gobierno de Macri en las series de precios y salarios, que fueron de inflación alta.
- **Pocas observaciones en las series trimestrales y semestrales.** Con 10 trimestres o 5 semestres por gobierno, asimetría y curtosis son muy inestables y deben leerse solo como descripción.
- **Revisiones.** El INDEC revisa el EMAE y las cuentas nacionales con cada publicación; los datos están congelados a octubre de 2026.

## Referencias

- Andrews, D. W. K. (1993). Tests for parameter instability and structural change with unknown change point. *Econometrica*, 61(4), 821-856.
- Dickey, D. A. y Fuller, W. A. (1979). Distribution of the estimators for autoregressive time series with a unit root. *Journal of the American Statistical Association*, 74(366), 427-431.
- Hamilton, J. D. (1989). A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357-384.
- Kwiatkowski, D., Phillips, P. C. B., Schmidt, P. y Shin, Y. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root. *Journal of Econometrics*, 54(1-3), 159-178.
- Ljung, G. M. y Box, G. E. P. (1978). On a measure of lack of fit in time series models. *Biometrika*, 65(2), 297-303.
- Perron, P. (1989). The great crash, the oil price shock, and the unit root hypothesis. *Econometrica*, 57(6), 1361-1401.
- Stock, J. H. y Watson, M. W. (2019). *Introduction to Econometrics* (4.ª ed.). Pearson. Tabla 14.5 (valores críticos del QLR).
- Zivot, E. y Andrews, D. W. K. (1992). Further evidence on the great crash, the oil-price shock, and the unit-root hypothesis. *Journal of Business & Economic Statistics*, 10(3), 251-270.
- INDEC: Índice de Precios al Consumidor, Índice de Salarios, EMAE, Informe de Avance del Nivel de Actividad, Encuesta Permanente de Hogares (informes de pobreza y de mercado de trabajo).
- Secretaría de Hacienda: Informe Mensual de Ingresos y Gastos (IMIG) del Sector Público Nacional no financiero, base caja.
- BCRA: API de Estadísticas Monetarias v4.0. Datos abiertos: [datos.gob.ar](https://datos.gob.ar), [ArgentinaDatos](https://argentinadatos.com), [data912](https://data912.com).
