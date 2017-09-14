function ProgressBar {
# Process data
	let _progress=(${1}*100/${2}*100)/100
	let _done=(${_progress}*4)/10
	let _left=40-$_done
# Build progressbar string lengths
	_done=$(printf "%${_done}s")
	_left=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:
# 1.2.1.1 Progress : [########################################] 100%
printf "\rProgress : [${_done// /#}${_left// /-}] ${_progress}%%"

}
SECONDS=0 # empieza tiempo
ARG1=${1:-1} #Numero de corridas
ARG2=${2:-1} #Procesos en paralelo
echo "==========================================================="
echo "              MONTE CARLO - PROCESO RENOVAR 2      "
echo "==========================================================="
echo "Corridas           = " $ARG1
echo "Procesos paralelos = " $ARG2
for i in `seq 1 $ARG1`; do
   #echo Corriendo simulacion $i
   ProgressBar $i $ARG1
   (python main.py -ncaso $i > salida.out) &
   if (( $i % $ARG2 == 0 ));
      then wait;
   fi
done
wait;
echo ""
echo "==========================================================="
echo "PROCESO TERMINADO EXITOSAMENTE!"
echo "Procesando archivos de salida... "
line=$(sed -n 4p config_rutas.txt)
awk 'FNR==1 && NR!=1{next;}{print}' $line/g*.csv > $line/resultado.csv
rm $line/g*.csv

echo "Proceso terminado."
printf "Total runtime: $(($SECONDS / 3600))hrs $((($SECONDS / 60) % 60))min $(($SECONDS % 60))sec"
echo " "
echo " "