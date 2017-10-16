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

- Para ejecutar una iteración única se debe ejecutar el siguiente comando `python main.py`.
- Para realizar varias corridas se debe ejecutar `./corre.sh ncorridas nprocesos`.
- Para iterar sobre un rango de precios en la oferta de solo un generador se debe ejecutar `./itera_precios.sh ncorridas nprocesos generador precio_ini precio_fin precio_paso`.
- Para iterar sobre un rango de precios en la oferta de 3 generadores con el mismo nombre se debe ejecutar `./itera_precios2.sh ncorridas nprocesos generador delta_precio1 delta_precio2 precio_ini precio_fin precio_paso`.

Ejemplo:
- Para ejecutar 1 corrida con 1 proceso paralelo sobre el proyecto EOL-M1 entre el precio 41 y 49 con un paso de 1 se debe ejecutar:  $ ./itera_precios.sh 1 1 EOL-M1 41 49 1
- Para ejecutar 1 corrida con 1 proceso paralelo sobre los proyectos EOL-M1, EOL-M2 (precio +1) y EOL-M3 (precio +2) entre el precio 41 y 49 con un paso de 1 se debe ejecutar:  $ ./itera_precios2.sh 1 1 EOL-M 1 2 41 49 1
