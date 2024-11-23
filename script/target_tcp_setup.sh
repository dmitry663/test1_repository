#!/bin/bash

# NVMe-oF TCP 타겟 설정
NQN="nqn.2024-07.io.example:nvme-oF-target"
NVME_DEVICE="/dev/nvme0n1p4"
TARGET_IP="192.168.1.7"
PORT="4420"

echo "==== NVMe-oF TCP 타겟 설정 ===="

# 커널 모듈 로드
sudo modprobe nvmet
sudo modprobe nvmet-tcp

# 서브시스템 설정
sudo mkdir /sys/kernel/config/nvmet/subsystems/$NQN
sudo sh -c 'echo 1 > /sys/kernel/config/nvmet/subsystems/$NQN/attr_allow_any_host'

# 네임스페이스 연결
sudo mkdir /sys/kernel/config/nvmet/subsystems/$NQN/namespaces/1
sudo sh -c "echo -n $NVME_DEVICE > /sys/kernel/config/nvmet/subsystems/$NQN/namespaces/1/device_path"
sudo sh -c "echo 1 > /sys/kernel/config/nvmet/subsystems/$NQN/namespaces/1/enable"

# 포트 설정
sudo mkdir /sys/kernel/config/nvmet/ports/1
sudo sh -c "echo $TARGET_IP > /sys/kernel/config/nvmet/ports/1/addr_traddr"
sudo sh -c "echo $PORT > /sys/kernel/config/nvmet/ports/1/addr_trsvcid"
sudo sh -c 'echo "tcp" > /sys/kernel/config/nvmet/ports/1/addr_trtype'
sudo sh -c 'echo "ipv4" > /sys/kernel/config/nvmet/ports/1/addr_adrfam'

# 서브시스템 연결
sudo ln -s /sys/kernel/config/nvmet/subsystems/$NQN /sys/kernel/config/nvmet/ports/1/subsystems/$NQN

echo "==== NVMe-oF TCP 타겟 설정 완료 ===="
