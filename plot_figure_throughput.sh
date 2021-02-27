mn -c
rm -r 'fig_throughput'
mkdir 'fig_throughput'
python2 experiment.py './fig_throughput' 55 'figure_throughput'
chmod -R 0777 './fig_throughput'
cd './fig_throughput'
echo "processing flows..."
for i in 0 1; do
captcp throughput -u Mbit --stdio connection$i.pcapng > captcp$i.txt
awk "{print (\$1+$i*2-1)(\",\")(\$2) }" < captcp$i.txt > captcp-csv$i.txt
done
cd '../'
python3 plot_figure_throughput.py -f ./fig_throughput/captcp-csv* --duration 50 -o ./fig_throughput/figure6_mininet.png