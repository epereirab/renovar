# -*- encoding: utf-8 -*-
# import sys
# import os
# from os.path import abspath, dirname
# sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))
#from coopr.pyomo import *
import math
import random
from pyomo.environ import *
# from coopr.pyomo.base.sparse_indexed_component import *
# SparseIndexedComponent._DEFAULT_INDEX_CHECKING_ENABLED = False

model = AbstractModel()
model.dual = Suffix(direction=Suffix.IMPORT)

###########################################################################
# SETS
###########################################################################

model.CONFIG = Set()
# PDI
model.PDI = Set()
# GENERADORES
model.GENERADORES = Set()
# TECNOLOGIAS
model.TECNOLOGIAS = Set()
# ZONAS
model.ZONAS = Set()

# CORTES DE BENDERS
#model.BENDERS = Set(within=PositiveIntegers, ordered=True)

###########################################################################
# PARAMETERS
###########################################################################

model.config_value = Param(model.CONFIG)

# PDI
model.pdi_max = Param(model.PDI)
model.pdi_fp = Param(model.PDI)

# GENERADORES

model.gen_disponible = Param(model.GENERADORES)
model.gen_pdi = Param(model.GENERADORES)
model.gen_zona = Param(model.GENERADORES)
model.gen_tecnologia = Param(model.GENERADORES)
model.gen_pmax = Param(model.GENERADORES)
model.gen_pmin = Param(model.GENERADORES)
model.gen_tejecucion = Param(model.GENERADORES)
model.gen_gbm = Param(model.GENERADORES)
model.gen_precio = Param(model.GENERADORES)
model.gen_precio_a = Param(model.GENERADORES)
model.gen_precio_b = Param(model.GENERADORES)
model.gen_precio_aleatorio = Param(model.GENERADORES)
model.gen_precio_distribucion = Param(model.GENERADORES)

# TECNOLOGIAS
model.tecnologia_min = Param(model.TECNOLOGIAS)
model.tecnologia_tejecucionmax = Param(model.TECNOLOGIAS)
model.tecnologia_preciomax = Param(model.TECNOLOGIAS)
model.tecnologia_gbm = Param(model.TECNOLOGIAS)

# ZONAS
model.zona_max = Param(model.ZONAS)
model.zona_tecnologias = Param(model.ZONAS)
model.zona_barras = Param(model.ZONAS)

###########################################################################
# SETS FROM PARAMETERS
###########################################################################

###########################################################################
# PARAMETERS FROM PARAMETERS
###########################################################################

# gen_poa (gen_precio, gen_fppdi, gen_tejecucion, tecnologia_tejecucionmax)
def rule_gen_poa(model, g):
    dias_adelanto = (model.tecnologia_tejecucionmax[model.gen_tecnologia[g]]-model.gen_tejecucion[g])
    if model.config_value['precio_aleatorio']:
        if not model.gen_precio_aleatorio[g]:
            return model.gen_precio[g]*model.pdi_fp[model.gen_pdi[g]]-0.005 * dias_adelanto
        distribucion = model.gen_precio_distribucion[g]
        if distribucion == 'normal':
            precio_aleatorio = round(random.gauss(model.gen_precio_a[g], model.gen_precio_b[g]),2)
        elif distribucion == 'pareto':
            precio_aleatorio = model.gen_precio[g]+round(random.paretovariate(model.gen_precio_a[g]),2)
        elif distribucion == 'triangular':
            precio_aleatorio = round(random.triangular(model.gen_precio_a[g], model.gen_precio_b[g], model.gen_precio[g]),2)
        else:
            precio_aleatorio = round(random.uniform(model.gen_precio_a[g], model.gen_precio_b[g]),2)
        return precio_aleatorio*model.pdi_fp[model.gen_pdi[g]]-0.005 * dias_adelanto
    return model.gen_precio[g] * model.pdi_fp[model.gen_pdi[g]] - 0.005 * dias_adelanto

model.gen_poa = Param(model.GENERADORES,
                    initialize=rule_gen_poa)

###########################################################################
# VARIABLES
###########################################################################

# Unit commitment casacion
model.GEN_UC = Var(model.GENERADORES, within=Binary)

# Potencia casada del generador g
def bounds_gen_pg(model, g):
    ub = round(model.gen_pmax[g], 2)
    if model.gen_disponible[g]:
        return 0, ub
    return 0,0

model.GEN_PC = Var(model.GENERADORES, within=NonNegativeReals, bounds=bounds_gen_pg)

# Variable de holgura casación por tecnologia
def bounds_vh_tech(model, tecnologia):
    ub = (model.tecnologia_min[tecnologia])
    return 0, ub

model.VH_TECH = Var(model.TECNOLOGIAS, within=NonNegativeReals, bounds=bounds_vh_tech)

###########################################################################
# CONSTRAINTS
###########################################################################

# CONSTRAINT 1: Inyección maxima por cada PDI´
def nodal_balance_rule(model, pdi):

    if not model.config_value['restriccion_nodal']:
        return Constraint.Skip
    formular = False
    lside = 0
    # lside = sum(model.GEN_PC[g] for g in model.GENERADORES if model.gen_pdi[g] == pdi)
    for g in model.GENERADORES:
        if model.gen_pdi[g] == pdi:
            lside += model.GEN_PC[g]
            formular = True
    rside = (model.pdi_max[pdi])
    if not formular:
        return Constraint.Skip
    return lside <= rside

model.CT_nodal_balance = Constraint(model.PDI, rule=nodal_balance_rule)

# CONSTRAINT 2: potencia minima casada  pmin * UC <= PC
def gen_pmin_rule(model, g):
    if not model.config_value['restriccion_minimo']:
        return Constraint.Skip
    rside = model.GEN_PC[g]
    lside = model.gen_pmin[g] * model.GEN_UC[g]
    return lside <= rside

model.CT_potencia_minima = Constraint(model.GENERADORES, rule=gen_pmin_rule)

# CONSTRAINT 3: potencia maxima casada  pmax * UC >= PC
def gen_pmax_rule(model, g):

    rside = model.GEN_PC[g]
    lside = model.gen_pmax[g] * model.GEN_UC[g]
    return lside >= rside

model.CT_potencia_maxima = Constraint(model.GENERADORES, rule=gen_pmax_rule)

# CONSTRAINT 4: minimo por tecnologia

def tecnologia_balance_rule(model, tecnologia):

    if not model.config_value['restriccion_por_tecnologia']:
        return Constraint.Skip
    rside = (model.tecnologia_min[tecnologia] - model.VH_TECH[tecnologia])
    lside = sum(model.GEN_PC[g] for g in model.GENERADORES if model.gen_tecnologia[g] in tecnologia)

    return lside == rside

model.CT_tecnologia_balance = Constraint(model.TECNOLOGIAS, rule=tecnologia_balance_rule)

# CONSTRAINT 4: maximo por zonas
def zona_max_rule(model, zona):

    if not model.config_value['restriccion_por_zona']:
        return Constraint.Skip
    lside = 0
    formular = False
    for g in model.GENERADORES:
        if (model.gen_zona[g] == zona) and (model.gen_tecnologia[g] in model.zona_tecnologias[zona]):
            lside += model.GEN_PC[g]
            formular= True
    rside = model.zona_max[zona]
    if not formular:
        return Constraint.Skip
    return lside <= rside

model.CT_zona_max = Constraint(model.ZONAS, rule=zona_max_rule)

# CONSTRAINT 5: garantia del banco mundial
def gbm_rule(model, tecnologia):

    if not model.config_value['restriccion_gbm']:
        return Constraint.Skip
    
    return sum(model.gen_gbm[g]*model.gen_pmax[g]*model.GEN_UC[g] for g in model.GENERADORES if tecnologia == model.gen_tecnologia[g]) <= model.tecnologia_gbm[tecnologia]

model.CT_gbm = Constraint(model.TECNOLOGIAS, rule=gbm_rule)

###########################################################################
# FUNCION OBJETIVO
###########################################################################

def system_cost_rule(model):
    costo_base = (sum(model.gen_poa[g] * model.GEN_PC[g] for g in model.GENERADORES))
    costo_base += sum(model.tecnologia_preciomax[tecnologia]*model.VH_TECH[tecnologia] for tecnologia in model.TECNOLOGIAS)
    return costo_base

model.Objective_rule = Objective(rule=system_cost_rule, sense=minimize)
