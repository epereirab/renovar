# Descripción del modelo y parámetros
## Parámetros modelo
Generadores:
- nombre
- disponible (true o false)
- pdi (punto de interconexión)
- región o zona
- tecnología 
- pmax
- pin
- precio oferta
- tiempo de ejecución
- precio_a (parametro a)
- precio_b (parámetro b)
- precio aleatorio (true o false)
- distribución de probabilidad de la oferta:
  - distribución normal -> normal 
    - parámetro a = mean, b = standard deviation
  - distribución de pareto -> pareto
    - parámetro a = shape
  - distribución triangular -> triangular
    - parámetro a = low bound, b = high bound, precio oferta = mode
  - distribucion por defecto: uniforme
    - parametro a = low bound, b = high bound
  
