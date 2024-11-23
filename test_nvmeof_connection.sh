#!/bin/bash

# NVMe-oF 테스트 스크립트
TARGET_IP="192.168.1.7"
PORT="4420"
NQN="nqn.2024-07.io.example:nvme-oF-target"

echo "==== NVMe-oF 타겟 연결 테스트 시작 ===="

# 1. 디스커버리
echo "1. 디스커버리 실행 중..."
sudo nvme discover -t tcp -a $TARGET_IP -s $PORT
if [ $? -eq 0 ]; then
    echo "디스커버리 성공: $TARGET_IP:$PORT"
else
    echo "디스커버리 실패: $TARGET_IP:$PORT"
    exit 1
fi

# 2. 타겟 연결
echo "2. 타겟 연결 중..."
sudo nvme connect -t tcp -n $NQN -a $TARGET_IP -s $PORT
if [ $? -eq 0 ]; then
    echo "타겟 연결 성공: $NQN at $TARGET_IP:$PORT"
else
    echo "타겟 연결 실패: $NQN at $TARGET_IP:$PORT"
    exit 1
fi

# 3. 연결된 디바이스 확인
echo "3. 연결된 NVMe 디바이스 목록 확인:"
sudo nvme list
if [ $? -eq 0 ]; then
    echo "디바이스 확인 완료."
else
    echo "디바이스 목록 확인 실패."
    exit 1
fi

echo "==== NVMe-oF 타겟 연결 테스트 완료 ===="
