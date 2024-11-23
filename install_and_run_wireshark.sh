#!/bin/bash

echo "==== Wireshark 설치 및 실행 스크립트 ===="

# 1. 시스템 업데이트
echo "1. 시스템 업데이트 중..."
sudo apt-get update -y
if [ $? -ne 0 ]; then
    echo "시스템 업데이트 실패. 스크립트를 종료합니다."
    exit 1
fi

# 2. Wireshark 설치
echo "2. Wireshark 설치 중..."
sudo apt-get install -y wireshark
if [ $? -ne 0 ]; then
    echo "Wireshark 설치 실패. 스크립트를 종료합니다."
    exit 1
fi

# 3. 비루트 사용자를 위한 권한 설정
echo "3. 비루트 사용자 권한 설정..."
sudo dpkg-reconfigure wireshark-common
sudo usermod -aG wireshark $USER

echo "Wireshark 설치 완료. 권한 적용을 위해 로그아웃 후 다시 로그인하세요."

# 4. Wireshark 실행
read -p "Wireshark를 지금 실행하시겠습니까? (y/n): " RUN_NOW
if [ "$RUN_NOW" == "y" ]; then
    echo "Wireshark 실행 중..."
    wireshark &
else
    echo "Wireshark 실행을 건너뜁니다."
fi

echo "==== Wireshark 설치 및 실행 스크립트 완료 ===="
