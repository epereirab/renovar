# Modelo de Subasta Renovar 2
Este es la guia de configuración del modelo de subasta del proceso RenovAr 2 desarrollado por SPEC Energy Consulting.

## Instalación
Estos son los pasos que se requieren hacer para su instalación en máquina Unix:
- Instalar python 2.7
- Descargar get-pip: `curl https://bootstrap.pypa.io/get-pip.py > get-pip.py`
- Instalar pip: `sudo python get-pip.py` 
- Instalar pyomo: `sudo -H python -m pip install pyomo`
- Descargar un solver y configurarlo
- Instalar git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- Descargar repositorio: `git clone https://github.com/epereirab/renovar.git`

## Configuración
En cuanto a la configuración:
- Añadir variables de entorno de optimizador
- Editar archivos en carpeta <b>/datos</b>

## Ejecución
Descripción de principales pasos de ejecución
