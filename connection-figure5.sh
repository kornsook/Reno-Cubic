mn -c
rm -r 'fig5'
mkdir 'fig5'
python3 experiment.py './fig5' 10 'figure5'
chmod -R 0777 './fig5'
su <Your SUDO USER> -c "tshark -2 -r ./fig5/connection_bbr.pcapng -R 'tcp.stream eq 1 && tcp.analysis.ack_rtt'  -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > ./fig5/bbr"
su <Your SUDO USER> -c "tshark -2 -r ./fig5/connection_cubic.pcapng -R 'tcp.stream eq 1 && tcp.analysis.ack_rtt'  -e frame.time_relative -e tcp.analysis.ack_rtt -Tfields -E separator=, > ./fig5/cubic"
python3 plot_figure5.py ./fig5/bbr ./fig5/cubic 8 ./fig5/figure5_mininet.png
