ARG1=${1:-1} #Numero de corridas
ARG2=${2:-1} #Procesos en paralelo

echo MONTE CARLO - PROCESO RENOVAR 2
echo Corridas          = $ARG1
echo Procesos paralelos= $ARG2
for i in `seq 1 $ARG1`; do
   echo Corriendo simulacion $i
   (python main.py -ncaso $i > salida.out) &
   if (( $i % $ARG2 == 0 ));
      then wait;
   fi
done
