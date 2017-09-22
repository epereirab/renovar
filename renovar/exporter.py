import csv
import cStringIO
import sys

def exportar_modelo(model, path, nombre_archivo):
    stdout_ = sys.stdout  # Keep track of the previous value.
    stream = cStringIO.StringIO()
    sys.stdout = stream
    print model.pprint()  # Here you can do whatever you want, import module1, call test
    sys.stdout = stdout_  # restore the previous stdout.
    variable = stream.getvalue()  # This will get the "hello" string inside the variable

    output = open(path + nombre_archivo + '.txt', 'w')
    output.write(variable)
    model.write(filename=path + nombre_archivo + '_LP.lp', io_options={'symbolic_solver_labels': True})
    # sys.stdout.write(instance.pprint())
    output.close()


def exportar_gen(model, path, nombre_archivo, ncaso):
    """ Resultados de Generadores """
    gen = model.GENERADORES
    ofile = open(path + nombre_archivo, "wb")
    writer = csv.writer(ofile, delimiter=',', quoting=csv.QUOTE_NONE)

    # header
    header = ['ncaso','Generador', 'tecnologia','zona','pdi', 'pmax','pmin', 'gbm', 'poa','precio','PC','UC']

    writer.writerow(header)

    for g in gen:
        tmprow = []
        tmprow.append(ncaso)
        tmprow.append(g)
        tmprow.append(model.gen_tecnologia[g])
        tmprow.append(model.gen_zona[g])
        tmprow.append(model.gen_pdi[g])
        tmprow.append(model.gen_pmax[g])
        tmprow.append(model.gen_pmin[g])
        tmprow.append(model.gen_gbm[g])
        tmprow.append(model.gen_poa[g])
        tmprow.append(model.gen_precio[g])
        tmprow.append(model.GEN_PC[g].value)
        tmprow.append(model.GEN_UC[g].value)


        writer.writerow(tmprow)

    ofile.close()