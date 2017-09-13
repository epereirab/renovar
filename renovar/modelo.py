# -*- encoding: utf-8 -*-
# import sys
# import os
# from os.path import abspath, dirname
# sys.path.insert(0, dirname(dirname(dirname(dirname(abspath(__file__))))))
#from coopr.pyomo import *
import math
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

# CORTES DE BENDERS
#model.BENDERS = Set(within=PositiveIntegers, ordered=True)

###########################################################################
# PARAMETERS
###########################################################################

model.config_value = Param(model.CONFIG)

# PDI
model.pdi_max = Param(model.PDI)

# GENERADORES

model.gen_disponible = Param(model.GENERADORES)
model.gen_pdi = Param(model.GENERADORES)
model.gen_tecnologia = Param(model.GENERADORES)
model.gen_pmax = Param(model.GENERADORES)
model.gen_pmin = Param(model.GENERADORES)
model.gen_poa = Param(model.GENERADORES)

# TECNOLOGIAS
model.tecnologia_min = Param(model.TECNOLOGIAS)
###########################################################################
# SETS FROM PARAMETERS
###########################################################################

###########################################################################
# PARAMETERS FROM PARAMETERS
###########################################################################

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

###########################################################################
# CONSTRAINTS
###########################################################################

# CONSTRAINT 1: Inyección maxima por cada PDI´
def nodal_balance_rule(model, pdi):

    lside = sum(model.GEN_PC[g] for g in model.GENERADORES if model.gen_pdi[g] == pdi)
    rside = (model.pdi_max[pdi])
    return lside <= rside

model.CT_nodal_balance = Constraint(model.PDI, rule=nodal_balance_rule)

# CONSTRAINT 2: potencia minima casada  pmin * UC <= PC
def gen_pmin_rule(model, g):

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

###########################################################################
# FUNCION OBJETIVO
###########################################################################

def system_cost_rule(model):
    costo_base = (sum(model.gen_poa[g] * model.GEN_PC[g] for g in model.GENERADORES))

    return costo_base


model.Objective_rule = Objective(rule=system_cost_rule, sense=minimize)
