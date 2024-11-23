#!/bin/bash

echo "==== NVMe-oF 호스트 설정 해제 ===="

# NVMe 디바이스 연결 해제
sudo nvme disconnect-all

echo "NVMe-oF 호스트 설정이 모두 해제되었습니다."
