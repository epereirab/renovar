# Script para iterar precios de un proyecto en particular
ARG1=${1:-1} #Numero de experimientos por precio
ARG2=${2:-1} #Procesos en paralelo
ARG3=${3:-""} #Nombre generador a iterar
ARG4=${4:-1} #Delta precio gen 1
ARG5=${5:-1} #Delta precio gen 2
ARG6=${6:-40} #Precio inicial
ARG7=${7:-50} #Precio final
ARG8=${8:-1}  #Paso de barrido de precios

# Obtiene ruta datos
dirdata=$(sed -n 2p config_rutas.txt)
dirresu=$(sed -n 4p config_rutas.txt)
# Cambia nombre data_generadores
mv $dirdata/data_generadores.csv $dirdata/original_data_generadores.csv

# Nombre generadores
PRE1=$
GEN1=$ARG3
GEN1+=1
GEN2=$ARG3
GEN2+=2
GEN3=$ARG3
GEN3+=3

for precio in `seq $ARG6 $ARG8 $ARG7`; do
   precio1=`echo "$precio + $ARG4" | bc -l`
   precio2=`echo "$precio + $ARG5" | bc -l`
   echo $precio
   echo $precio1
   echo $precio2

   # Cambia precio de proyecto
   echo " -------------- SENSIBILIDAD PRECIO = " $precio "----------------"
   awk -F ',' -v gen1="$GEN1" -v gen2="$GEN2" -v gen3="$GEN3" -v pre="$precio" -v pre1="$precio1" -v pre2="$precio2" -v OFS=','\
   '$1 { if ($1==gen1) $10=pre; if ($1==gen2) $10=pre1; if ($1==gen3) $10=pre2;  print}' $dirdata/original_data_generadores.csv > $dirdata/data_generadores.csv
   # Corre simulacion
   ./corre.sh $ARG1 $ARG2
   # Guarda sensibilidad con precio
   mv $dirresu/resultado.csv $dirresu/resultado_$precio.csv
done

# Restaura data original
rm $dirdata/data_generadores.csv
mv $dirdata/original_data_generadores.csv $dirdata/data_generadores.csv
