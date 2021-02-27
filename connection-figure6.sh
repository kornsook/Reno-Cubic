mn -c
rm -r 'fig6'
mkdir 'fig6'
python2 experiment.py './fig6' 55 'figure6'
chmod -R 0777 './fig6'
cd './fig6'
echo "processing flows..."
for i in 0 1 2 3 4; do
captcp throughput -u Mbit --stdio connection$i.pcapng > captcp$i.txt
awk "{print (\$1+$i*2-1)(\",\")(\$2) }" < captcp$i.txt > captcp-csv$i.txt
done
cd '../'
python3 plot_figure6.py -f ./fig6/captcp-csv* --duration 50 -o ./fig6/figure6_mininet.png