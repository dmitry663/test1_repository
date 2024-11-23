#!/bin/bash

# 마운트할 NVMe 디바이스와 마운트 지점 설정
NVME_DEVICE="/dev/nvme0n1p1" # 마운트할 NVMe 디바이스
MOUNT_POINT="/mnt/nvme"      # 마운트 지점

echo "==== NVMe 디바이스 마운트 스크립트 ===="

# 1. NVMe 디바이스 확인
echo "1. NVMe 디바이스 확인 중..."
if lsblk | grep -q $(basename $NVME_DEVICE); then
    echo "디바이스 확인됨: $NVME_DEVICE"
else
    echo "디바이스를 찾을 수 없습니다: $NVME_DEVICE"
    exit 1
fi

# 2. 마운트 지점 생성
echo "2. 마운트 지점 확인 및 생성 중..."
if [ ! -d "$MOUNT_POINT" ]; then
    echo "마운트 지점이 존재하지 않습니다. 생성 중: $MOUNT_POINT"
    sudo mkdir -p "$MOUNT_POINT"
else
    echo "마운트 지점이 이미 존재합니다: $MOUNT_POINT"
fi

# 3. 파일 시스템 확인 및 생성 (필요시)
echo "3. 파일 시스템 확인 중..."
if sudo blkid $NVME_DEVICE | grep -q "ext4"; then
    echo "디바이스에 ext4 파일 시스템이 이미 존재합니다."
else
    echo "ext4 파일 시스템이 존재하지 않습니다. 생성 중..."
    sudo mkfs.ext4 $NVME_DEVICE
    if [ $? -ne 0 ]; then
        echo "파일 시스템 생성 실패."
        exit 1
    fi
    echo "ext4 파일 시스템 생성 완료."
fi

# 4. NVMe 디바이스 마운트
echo "4. 디바이스 마운트 중..."
sudo mount $NVME_DEVICE $MOUNT_POINT
if [ $? -eq 0 ]; then
    echo "디바이스 마운트 성공: $NVME_DEVICE -> $MOUNT_POINT"
else
    echo "디바이스 마운트 실패."
    exit 1
fi

# 5. 마운트 확인
echo "5. 마운트 상태 확인:"
df -h | grep $MOUNT_POINT

echo "==== NVMe 디바이스 마운트 스크립트 완료 ===="
