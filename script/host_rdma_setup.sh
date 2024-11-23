#!/bin/bash

# NVMe-oF RDMA 호스트 설정
TARGET_IP="192.168.1.1"
PORT="4420"
NQN="nqn.2024-07.io.example:nvme-oF-target"

echo "==== NVMe-oF RDMA 호스트 설정 ===="

# 디스커버리
sudo nvme discover -t rdma -a $TARGET_IP -s $PORT

# 연결
sudo nvme connect -t rdma -n $NQN -a $TARGET_IP -s $PORT

# 연결된 디바이스 확인
sudo nvme list

echo "==== NVMe-oF RDMA 호스트 설정 완료 ===="
