#!/bin/bash

# 변수 설정
NQN="nqn.2024-07.io.example:nvme-oF-target"

echo "==== NVMe-oF 타겟 설정 해제 ===="

# 서브시스템과 포트의 연결 해제
if [ -d "/sys/kernel/config/nvmet/ports/1" ]; then
    sudo unlink /sys/kernel/config/nvmet/ports/1/subsystems/$NQN
    sudo rmdir /sys/kernel/config/nvmet/ports/1
fi

if [ -d "/sys/kernel/config/nvmet/subsystems/$NQN" ]; then
    sudo rmdir /sys/kernel/config/nvmet/subsystems/$NQN
fi

# 커널 모듈 언로드
sudo modprobe -r nvmet-tcp
sudo modprobe -r nvmet-rdma
sudo modprobe -r nvmet

echo "NVMe-oF 타겟 설정이 모두 해제되었습니다."
