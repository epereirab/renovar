# from coopr.pyomo import *
# from coopr.opt import SolverFactory

from pyomo.environ import *
from pyomo.opt import SolverFactory

from modelo import model as model
# from SlaveModel import _model as slave_model
import cStringIO
import sys
import exporter
import os
import csv
import argparse

parser = argparse.ArgumentParser(description='PARSER para corrida')
parser.add_argument('-ncaso', default=1)
args = parser.parse_args()

#  - - - - - - LEER RUTAS DE DATOS Y RESULTADOS  - - - - - - #

config_rutas = open('config_rutas.txt', 'r')
path_datos = ''
path_resultados = ''
tmp_line = ''

for line in config_rutas:

     if tmp_line == '[datos]':
         path_datos = line.split()[0]
     elif tmp_line == '[resultados]':
         path_resultados = line.split()[0]

     tmp_line = line.split()[0]

if not os.path.exists(path_resultados):
     print "el directorio output: " + path_resultados + " no existe, creando..."
     os.mkdir(path_resultados)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#  - - - - - - CARGAR DATOS AL MODELO  - - - - - - ##
#  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

print ("--- Leyendo data ---")
print ("path input:" + path_datos)
data_modelo = DataPortal()

nombre_archivo = path_datos+'data_config.csv'
print "importando: " + nombre_archivo
data_modelo.load(filename=nombre_archivo,
                 param=model.config_value,
                 index=model.CONFIG)

nombre_archivo = path_datos+'data_pdi.csv'
print "importando: " + nombre_archivo
data_modelo.load(filename=nombre_archivo,
                 param=(model.pdi_max, model.pdi_fp),
                 index=model.PDI)
print 'importacion OK'

nombre_archivo = path_datos+'data_limitacion.csv'
print "importando: " + nombre_archivo
data_modelo.load(filename=nombre_archivo,
                 param=(model.limitacion_max, model.limitacion_pdi),
                 index=model.LIMITACION)
print 'importacion OK'

nombre_archivo = path_datos+'data_generadores.csv'
print "importando: " + nombre_archivo
data_modelo.load(filename=nombre_archivo,
                 param=(model.gen_disponible, model.gen_pdi, model.gen_zona, model.gen_tecnologia,
                        model.gen_pmax, model.gen_pmin, model.gen_tejecucion, model.gen_gbm,
                        model.gen_precio, model.gen_precio_a, model.gen_precio_b, model.gen_precio_aleatorio,
                        model.gen_precio_distribucion, model.gen_alternativo),
                 index=model.GENERADORES)
print 'importacion OK'

nombre_archivo = path_datos+'data_tecnologias.csv'
print "importando: " + nombre_archivo
data_modelo.load(filename=nombre_archivo,
                 param=(model.tecnologia_min, model.tecnologia_tejecucionmax, model.tecnologia_preciomax,
                        model.tecnologia_gbm),
                 index=model.TECNOLOGIAS)
print 'importacion OK'

nombre_archivo = path_datos+'data_zonas.csv'
print "importando: " + nombre_archivo
data_modelo.load(filename=nombre_archivo,
                 param=(model.zona_max, model.zona_tecnologias, model.zona_zonas),
                 index=model.ZONAS)
print 'importacion OK'

###########################################################################
# CREANDO MODELO Y RESOLVIENDO OPTIMIZACION
###########################################################################
print ("--- Creando Modelo ---")
instancia_modelo = model.create_instance(data_modelo)

if instancia_modelo.config_value['solver'] == 'glpk':
    opt = SolverFactory("glpk")
elif instancia_modelo.config_value['solver'] == 'cplex':
    opt = SolverFactory("cplex")

print ("--- Resolviendo la optimizacion ---")
results_master = opt.solve(instancia_modelo, tee=True)

print ("Modelo Resuelto")
instancia_modelo.solutions.load_from(results_master)

###########################################################################
# EXPORTANDO RESULTADOS
###########################################################################

# debugging options
if instancia_modelo.config_value['debugging']:
    exporter.exportar_modelo(instancia_modelo, path_resultados, 'model_after')

exporter.exportar_gen(instancia_modelo, path_resultados, 'generadores_' + str(args.ncaso).zfill(6) + '.csv',args.ncaso)
