# Script para iterar precios de un proyecto en particular
ARG1=${1:-1} #Numero de experimientos por precio
ARG2=${2:-1} #Procesos en paralelo
ARG3=${3:-""} #Nombre generador a iterar
ARG4=${4:-50} #Precio inicial
ARG5=${5:-60} #Precio final
ARG6=${6:-1}  #Paso de barrido de precios

# Obtiene ruta datos
dirdata=$(sed -n 2p config_rutas.txt)
dirresu=$(sed -n 4p config_rutas.txt)
# Cambia nombre data_generadores
mv $dirdata/data_generadores.csv $dirdata/original_data_generadores.csv

for precio in `seq $ARG4 $ARG6 $ARG5`; do
   # Cambia precio de proyecto
   echo " -------------- SENSIBILIDAD PRECIO = " $precio "----------------"
   awk -F ',' -v gen="$ARG3" -v pre="$precio" -v OFS=',' '$1 { if ($1==gen) $10=pre; print}' $dirdata/original_data_generadores.csv > $dirdata/data_generadores.csv
   # Corre simulacion
   ./corre.sh $ARG1 $ARG2
   # Guarda sensibilidad con precio
   mv $dirresu/resultado.csv $dirresu/resultado_$precio.csv
done

# Restaura data original
rm $dirdata/data_generadores.csv
mv $dirdata/original_data_generadores.csv $dirdata/data_generadores.csv
