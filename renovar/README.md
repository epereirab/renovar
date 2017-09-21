# Documentación

## Datos de entrada/ Archivos de parámetros

### Data Config
+ Debugging (genera archivos LP)
+ Restriccion_nodal (considerar restricción por pdi)
+ Restriccion_por_tecnologia (considerar restricción de minimo por tecnologia)
+ Restriccion_por_zona (cosiderar restricción por zona)
+ Precio_aleatorio (considerar parámetro de precio aleatorio por generador)
+ Restriccion_minimo (cosiderar parámetro de minimo por generador)

### Generadores
+ Nombre
+ Disponible (true o false)
+ Pdi (punto de interconexión)
+ Región o zona
+ Tecnología 
+ Pmax
+ Pmin
+ Precio oferta
+ Tiempo de ejecución
+ Precio_a (parametro a)
+ Precio_b (parámetro b)
+ Precio aleatorio (true o false)
+ Distribución de probabilidad de la oferta

<center>
 
| Distribución | Parámetro a | Parámetro b |
|--------------|-------------|-------------|
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

asdf
