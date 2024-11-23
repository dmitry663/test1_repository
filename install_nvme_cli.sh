#!/bin/bash

echo "==== NVMe CLI 설치 스크립트 ===="

# 1. 시스템 업데이트
echo "1. 시스템 업데이트 중..."
sudo apt-get update -y
if [ $? -ne 0 ]; then
    echo "시스템 업데이트 실패. 스크립트를 종료합니다."
    exit 1
fi

# 2. NVMe CLI 설치
echo "2. NVMe CLI 설치 중..."
sudo apt-get install -y nvme-cli
if [ $? -ne 0 ]; then
    echo "NVMe CLI 설치 실패. 스크립트를 종료합니다."
    exit 1
fi

# 3. 설치 확인
echo "3. NVMe CLI 설치 확인 중..."
if nvme version > /dev/null 2>&1; then
    echo "NVMe CLI 설치 성공!"
    nvme version
else
    echo "NVMe CLI 설치 실패!"
    exit 1
fi

# 4. 기본 명령어 테스트
echo "4. NVMe 디바이스 목록 확인 중..."
sudo nvme list
if [ $? -eq 0 ]; then
    echo "NVMe 디바이스 확인 완료."
else
    echo "NVMe 디바이스 확인 실패. NVMe 디바이스가 연결되지 않았을 수 있습니다."
fi

echo "==== NVMe CLI 설치 스크립트 완료 ===="
