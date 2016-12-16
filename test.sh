for i in `seq 5 6`
do
    mpirun -host node1,node2,node3 -ppn 36 python count.py -f db$i.1 -p 1
    mpirun -host node1,node2,node3 -ppn 36 python count.py -f db$i.2 -p 2
    mpirun -host node1,node2,node3 -ppn 36 python count.py -f db$i.3 -p 3
    mpirun -host node1,node2,node3 -ppn 36 python count.py -f db$i.4 -p 4
    mpirun -host node1,node2,node3 -ppn 36 python count.py -f db$i.5 -p 5
done
for i in db*
do
    python pic.py -f $i | python -m json.tool | tee p.$i
done

