# Documentación
En el presente documento se describe el funcionamiento del modelo de simulación implementado para el proceso renovAr 2.
## Datos de entrada/ Archivos de parámetros
Los datos de entrada se manejan a través de archivos *.csv*. Los archivos necesarios son los que se detallan a continuación con sus respectivos parámetros.
### Data Config
|           config           | config value |                       Descripción                      |
|:--------------------------:|:------------:|:------------------------------------------------------:|
|          debugging         | true/false |           generar archivos LP para debuggear           |
|      restriccion_nodal     | true/false |             considerar restricción por pdi             |
| restriccion_por_tecnologia | true/false |     considerar restricción de mínimo por tecnología    |
|    restriccion_por_zona    | true/false |             considerar restricción por zona            |
|      precio_aleatorio      | true/false | considerar parámetro de precio aleatorio por generador |
|     restriccion_minimo     | true/false |  considerar parámetro de potencia mínima por generador |
|     restriccion_gbm        | true/false |  considerar restricción de garantía banco mundial      |
|          solver            | cplex/glpk |  elegir solver para realizar la optimización           |

### Generadores
|                 parámetro                 |    valor   |                    descripción                    |
|:-----------------------------------------:|:----------:|:-------------------------------------------------:|
|                   nombre                  |   string   |                  nombre proyecto                  |
|                 disponible                | true/false |                considerar o no en modelo          |
|                    pdi                    |   string   |               punto de interconexión              |
|                    zona                   |   string   |                     zona                          |
|                 tecnología                |   string   |                     tecnologia                    |
|                    pmax [MW]              |    float   |               potencia ofertada                   |
|                    pmin [MW]              |    float   |   potencia mínima de adjudicación parcial         |
|            tiempo de ejecución [dias]     |    float   |       tiempo de ejecución proyecto (días)         |
|                    gbm [$/MW]             |    float   |       tiempo de ejecución proyecto (días)         |
|               precio oferta [$/MWh]       |    float   |                      precio ofertado              |
|                 precio_a                  |    float   |    parámetro *a* de la distribución respectiva    |
|                 precio_b                  |    float   |    parámetro *b* de la distribución respectiva    |
|              precio aleatorio             | true/false | considerar variación de precio según distribución |
| Distribución de probabilidad de la oferta |   string*  |                tipo de distribución               |

Los valores asignados a los pdi, zona y tecnología de cada generador deben ser consistentes con los pdi, zona y tecnología existentes en sus archivos respectivos.

*Los valores de distribución de probabilidad utilizables son los siguientes:
 
| Distribución | Parámetro a | Parámetro b |
|:------------:|:-----------:|:-----------:|
| normal       | mean        |     sd      |
| pareto       | shape       |     -       |
| triangular   | low bound   | high bound  |
| uniforme     | low bound   | high bound  |
 
### Tecnologias
| Parámetro | Valor | Descripción |
|:---------:|:-----:|:-----------:|
|  nombre   |string |      nombre tecnología       |
|     min [MW]  | float |      potencia mínima restricción por tecnología       |
|  tejecucionmax [dias]   | float |      tiempo de ejecución máximo por tecnología       |
|  preciomax [$/MWh]  | float |      precio máximo de oferta por tecnología      |
| gbm [$] | float | gbm total por tecnología |

### Zonas
| Parámetro | Valor | Descripción |
|:---------:|:-----:|:-----------:|
|  nombre   |string |      nombre zona       |
|  max [MW]  | float |  potencia máxima restricción por zona   |
|  tecnologias  |[string1,..] |   lista de tecnologias involucradas en la restricción por zona      |
|  pdi's   |[string1,..] |  lista de pdi pertenecientes a la zona |

### Pdi
| Parámetro | Valor | Descripción |
|:---------:|:-----:|:-----------:|
|  nombre   |string |      nombre pdi     |
| max [MW]  | float |   Potencia máxima de inyección de pdi |
|     fp    | float |       Factor de pérdidas asociado al pdi   |

## Modelo matemático
### Función objetivo
![f1]

Donde:
+ POA(g)	: precio ofertado considerando factor pérdida PDI y el tiempo de construcción.
+ U(g)	: variable binaria de adjudicación

el POA de cada proyecto se calcula como sigue:

POA(g) = Precio(g) * Fp(pdi(g)) - 0.005 * (tmaxtecn(tecn(g))-tej(g))

### Restricciones
+ Potencia máxima adjudicable por tecnología.
+ Potencia máxima adjudicable por zona/tecnología
+ Potencia máxima adjudicable por PDI
+ Potencia máxima y mínima de adjudicación por proyecto.

[f1]: http://chart.apis.google.com/chart?cht=tx&chl=min_{z}=\sum{}{POA(g)*P(g)}

