sudo tshark -i any -l -f "tcp port 4420" -T fields\
    -e frame.number\
    -e frame.len\
    -e frame.time_relative\
    -e frame.time_epoch\
    -e frame.protocols\
    -e ip.src\
    -e ip.dst\
    -e tcp.srcport\
    -e tcp.dstport\
    -e tcp.seq_raw\
    -e tcp.len\
    -e tcp.ack_raw\
    -e nvme-tcp.type\
    -e nvme-tcp.pdo\
    -e nvme-tcp.plen\
    -e nvme.cmd.cid\
    -e nvme.cqe.cid\
    -e nvme-tcp.cmd.cid\
    -e nvme.cmd.opc