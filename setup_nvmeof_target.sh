#!/bin/bash

# NVMe-oF 설정 스크립트
# Author: [Your Name]
# Date: [Date]

# 타겟 IP와 포트 설정
TARGET_IP="192.168.1.7"
PORT="4420"
NQN="nqn.2024-07.io.example:nvme-oF-target"
NVME_DEVICE="/dev/nvme0n1p4"

echo "==== NVMe-oF 타겟 설정 스크립트 시작 ===="

# 1. 커널 모듈 로드
echo "1. 커널 모듈 로드 중..."
sudo modprobe nvmet || { echo "nvmet 모듈 로드 실패"; exit 1; }
sudo modprobe nvmet-tcp || { echo "nvmet-tcp 모듈 로드 실패"; exit 1; }
echo "커널 모듈 로드 완료."

# 2. 서브시스템 설정
echo "2. 서브시스템 생성 중..."
SUBSYS_PATH="/sys/kernel/config/nvmet/subsystems/$NQN"
if [ ! -d "$SUBSYS_PATH" ]; then
    sudo mkdir -p "$SUBSYS_PATH"
    sudo sh -c 'echo 1 > '"$SUBSYS_PATH"'/attr_allow_any_host'
    echo "서브시스템 생성 완료: $SUBSYS_PATH"
else
    echo "서브시스템 이미 존재: $SUBSYS_PATH"
fi

# 3. 네임스페이스 설정
echo "3. 네임스페이스 생성 중..."
NAMESPACE_PATH="$SUBSYS_PATH/namespaces/1"
if [ ! -d "$NAMESPACE_PATH" ]; then
    sudo mkdir -p "$NAMESPACE_PATH"
    sudo sh -c 'echo -n '"$NVME_DEVICE"' > '"$NAMESPACE_PATH"'/device_path'
    sudo sh -c 'echo 1 > '"$NAMESPACE_PATH"'/enable'
    echo "네임스페이스 생성 완료: $NAMESPACE_PATH"
else
    echo "네임스페이스 이미 존재: $NAMESPACE_PATH"
fi

# 4. 포트 설정
echo "4. 포트 설정 중..."
PORT_PATH="/sys/kernel/config/nvmet/ports/1"
if [ ! -d "$PORT_PATH" ]; then
    sudo mkdir -p "$PORT_PATH"
    sudo sh -c 'echo '"$TARGET_IP"' > '"$PORT_PATH"'/addr_traddr'
    sudo sh -c 'echo '"$PORT"' > '"$PORT_PATH"'/addr_trsvcid'
    sudo sh -c 'echo "tcp" > '"$PORT_PATH"'/addr_trtype'
    sudo sh -c 'echo "ipv4" > '"$PORT_PATH"'/addr_adrfam'
    sudo ln -s "$SUBSYS_PATH" "$PORT_PATH/subsystems/$NQN"
    echo "포트 설정 완료: $PORT_PATH"
else
    echo "포트 이미 설정됨: $PORT_PATH"
fi

# 5. 설정 확인
echo "5. 설정 확인:"
cat "$PORT_PATH/addr_traddr"
cat "$PORT_PATH/addr_trsvcid"
cat "$PORT_PATH/addr_trtype"
cat "$PORT_PATH/addr_adrfam"

echo "==== NVMe-oF 타겟 설정 스크립트 완료 ===="
