# Documentación
En el presente documento se describe el funcionamiento del modelo de simulación implementado para el proceso renovAr 2.
## Datos de entrada/ Archivos de parámetros
Los datos de entrada se manejan a través de archivos *.csv*. Los archivos necesarios son los que se detallan a continuación con sus respectivos parámetros.
### Data Config
| config                     | config value | descripción                                                   |
|:--------------------------:|:------------:|:-------------------------------------------------------------:|
| debugging                  | true/false   | Generar archivos LP para debuggear                            |
| restriccion_nodal          | true/false   | Considerar restricción por pdi                                |
| restriccion_limitación     | true/false   | Considerar restricción de limitaciones por agrupación de pdi  |
| restriccion_por_tecnologia | true/false   | Considerar restricción de mínimo por tecnología               |
| restriccion_por_zona       | true/false   | Considerar restricción por zona                               |
| precio_aleatorio           | true/false   | Considerar parámetro de precio aleatorio por generador        |
| restriccion_minimo         | true/false   | Considerar parámetro de potencia mínima por generador         |
| restriccion_gbm            | true/false   | Considerar restricción de garantía banco mundial              |
| solver                     | cplex/glpk   | Elegir solver para realizar la optimización                   |

*no se deben modificar los nombres de la columna config, solamente los valores de config value.

### Generadores
| parámetro                                 |    valor   |                    descripción                      |
|:-----------------------------------------:|:----------:|:---------------------------------------------------:|
| nombre                                    |   string   | Nombre proyecto                                     |
| disponible                                | true/false | Indica si optimización considera el proyecto o no   |
| pdi                                       |   string   | Código del Punto de Interconexión                   |
| zona                                      |   string   | Zona de interconexión                               |
| tecnología                                |   string   | Tecnología del generador                            |
| pmax [MW]                                 |    float   | Potencia máxima ofertada                            |
| pmin [MW]                                 |    float   | Potencia mínima para casación parcial               |
| tiempo de ejecución [dias]                |    float   | Tiempo de ejecución de proyecto                     |
| gbm [$/MW]                                |    float   | Monto de garantía del Banco Mundial solicitada      |
| precio oferta [$/MWh]                     |    float   | Precio ofertado                                     |
| precio_a                                  |    float   | Parámetro *a* de la distribución respectiva         |
| precio_b                                  |    float   | Parámetro *b* de la distribución respectiva         |
| precio aleatorio                          | true/false | Considerar variación de precio según distribución   |
| Distribución de probabilidad de la oferta |   string*  | Tipo de distribución                                |

Los valores asignados a los pdi, zona y tecnología de cada generador deben ser consistentes con los pdi, zona y tecnología existentes en sus archivos respectivos.

*Los valores de distribución de probabilidad utilizables son los siguientes (si se ingresa otro valor se toma por defecto distribución uniforme):
 
| Distribución | Parámetro a | Parámetro b |
|:------------:|:-----------:|:-----------:|
| normal       | mean        |     sd      |
| pareto       | shape       |     -       |
| triangular   | low bound   | high bound  |
| uniforme     | low bound   | high bound  |
 
### Tecnologias
| Parámetro              | Valor | Descripción                                 |
|:----------------------:|:-----:|:-------------------------------------------:|
| nombre                 |string | Nombre tecnología                           |
| min [MW]               | float | Potencia mínima restricción por tecnología  |
| tejecucionmax [dias]   | float | Tiempo de ejecución máximo por tecnología   |
| preciomax [$/MWh]      | float | Precio máximo de oferta por tecnología      |
| gbm [$]                | float | Gbm total por tecnología                    |

### Zonas
| Parámetro            | Valor        | Descripción                                                  |
|:--------------------:|:------------:|:------------------------------------------------------------:|
| nombre restricción   | string       | Nombre de la restricción zonal                               |
| max [MW]             | float        | Potencia máxima restricción por zona                         |
| tecnologias          | [string1,..] | Lista de tecnologias involucradas en la restricción por zona |
| zonas                | [string1,..] | Lista de zonas pertenecientes a la restricción               |

### Pdi
| Parámetro            | Valor | Descripción                         |
|:--------------------:|:-----:|:-----------------------------------:|
| nombre               |string | Nombre o código pdi                 |
| max [MW]             | float | Potencia máxima de inyección de pdi |
| fp                   | float | Factor de pérdidas asociado al pdi  |

### Limitación
| Parámetro | Valor        | Descripción                           |
|:---------:|:------------:|:-------------------------------------:|
| nombre    | string       | Nombre limitación                     |
| max [MW]  | float        | Potencia máxima por agrupación de pdi |
| pdi       | [string1,..] | pdi's asociados a la restricción        |

## Modelo matemático
### Función objetivo
![f1]

Donde:
+ POA(g)	: precio ofertado considerando factor pérdida PDI y el tiempo de construcción.
+ U(g)	: variable binaria de adjudicación

el POA de cada proyecto se calcula como sigue:

![f2]

### Restricciones
+ Potencia máxima adjudicable por tecnología.
+ Potencia máxima adjudicable por zona/tecnología
+ Potencia máxima adjudicable por PDI
+ Potencia máxima y mínima de adjudicación por proyecto.

[f1]: http://chart.apis.google.com/chart?cht=tx&chl={min%20\quad%20{z}=\sum{}{POA(g)\cdot%20P(g)}}
[f2]: http://chart.apis.google.com/chart?cht=tx&chl={POA_{g}=Precio_{g}\cdot%20Fp(pdi_{g})-0.005\cdot%20(tmaxtecn(tecn_{g})-tej_{g})}


