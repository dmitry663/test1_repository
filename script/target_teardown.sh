#!/bin/bash

NQN="nqn.2024-07.io.example:nvme-oF-target"

echo "==== NVMe-oF 타겟 설정 해제 ===="

# 1. 심볼릭 링크 제거 (포트와 서브시스템 연결 해제)
if [ -L "/sys/kernel/config/nvmet/ports/1/subsystems/$NQN" ]; then
    echo "서브시스템과 포트 연결 해제 중..."
    sudo unlink /sys/kernel/config/nvmet/ports/1/subsystems/$NQN
fi

# 2. 포트 제거
if [ -d "/sys/kernel/config/nvmet/ports/1" ]; then
    echo "포트 제거 중..."
    sudo rmdir /sys/kernel/config/nvmet/ports/1
fi

# 3. 네임스페이스 제거
if [ -d "/sys/kernel/config/nvmet/subsystems/$NQN/namespaces/1" ]; then
    echo "네임스페이스 제거 중..."
    sudo rmdir /sys/kernel/config/nvmet/subsystems/$NQN/namespaces/1
fi

# 4. 서브시스템 제거
if [ -d "/sys/kernel/config/nvmet/subsystems/$NQN" ]; then
    echo "서브시스템 제거 중..."
    sudo rmdir /sys/kernel/config/nvmet/subsystems/$NQN
fi

# 5. 모듈 언로드
echo "커널 모듈 언로드 중..."
sudo modprobe -r nvmet-rdma 2>/dev/null
sudo modprobe -r nvmet 2>/dev/null

echo "==== NVMe-oF 타겟 설정이 모두 해제되었습니다 ===="
