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

### Generadores
|                 parámetro                 |    valor   |                    descripción                    |
|:-----------------------------------------:|:----------:|:-------------------------------------------------:|
|                   nombre                  |   string   |                                                   |
|                 disponible                | true/false |                                                   |
|                    pdi                    |   string   |               punto de interconexión              |
|                    zona                   |   string   |                                                   |
|                 tecnología                |   string   |                                                   |
|                    pmax                   |    float   |               potencia ofertada                   |
|                    pmin                   |    float   |   potencia mínima de adjudicación parcial         |
|               precio oferta               |    float   |                      precio ofertado              |
|            tiempo de ejecución            |    float   |       tiempo de ejecución proyecto (días)         |
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
- Tipo (ej: eólica, solar)
- potencia mínima restricción por tecnología
- tiempo de ejecución máximo por tecnología
- precio máximo de oferta por tecnología

### Zonas
- Nombre 
- potencia máxima restricción por zona
- tecnologías que involucra la zona (puede ser más de una)
- puntos de interconexión pertenecientes a la zona

### Pdi
- Nombre
- Potencia máxima de inyección en pdi
- Factor de pérdidas asociado al pdi

## Modelo matemático

### Función objetivo
min z = suma(POA(g) x P(g)).

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


