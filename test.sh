echo $1 $2
for i in `seq $1 $2`
do
    mpirun -host $3 -ppn 36 python count.py -f db$i.1 -p 1
    mpirun -host $3 -ppn 36 python count.py -f db$i.2 -p 2
    mpirun -host $3 -ppn 36 python count.py -f db$i.3 -p 3
    mpirun -host $3 -ppn 36 python count.py -f db$i.4 -p 4
    mpirun -host $3 -ppn 36 python count.py -f db$i.5 -p 5
done
for i in db*
do
    python pic.py -f $i | python -m json.tool | tee p.$i
done

