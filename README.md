# Modelo de Subasta Renovar 2
Este es la guia de configuración del modelo de subasta del proceso RenovAr 2 desarrollado por SPEC Energy Consulting.

## Instalación
Estos son los pasos que se requieren hacer para su instalación en máquina Unix:
- Instalar python 2.7
- Descargar get-pip: `curl https://bootstrap.pypa.io/get-pip.py > get-pip.py`
- Instalar pip: `sudo python get-pip.py` 
- Instalar pyomo: `sudo -H python -m pip install pyomo`
- Instalar pyomo.extras: `sudo -H python -m pip install pyomo.extras`
- Descargar un solver y configurarlo
- Instalar git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- Descargar repositorio: `git clone https://github.com/epereirab/renovar.git`

## Configuración
En cuanto a la configuración:
- Añadir variables de entorno de optimizador
- Editar archivos en carpeta <b>/datos</b>

## Ejecución
Descripción de principales pasos de ejecución

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
  
    
