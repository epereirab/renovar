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
- Para iterar sobre un rango de precios en la oferta de un generador se debe ejecutar `./itera_precios.sh ncorridas nprocesos generador precio_ini precio_fin precio_paso`.
