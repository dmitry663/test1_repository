#!/bin/bash

# 설정
MOUNT_PATH="/mnt/nvme"
FILE_PREFIX="testfile"
MAX_FILES=100
MAX_ITERATIONS=1000

# 파일 리스트
declare -a file_list

# 랜덤 파일 이름 생성
generate_random_filename() {
    echo "${FILE_PREFIX}_$(date +%s%N | sha256sum | head -c 8).txt"
}

# 메모리 캐시 초기화 함수
clear_memory_cache() {
    echo "Clearing memory cache..."
    sudo sync
    sudo sysctl -w vm.drop_caches=3
    echo "Memory cache cleared."
}

# 랜덤 작업 수행
random_io_operation() {
    local operation=$((RANDOM % 8))
    local random_file=${file_list[$((RANDOM % ${#file_list[@]}))]}

    case $operation in
        0) # 파일 생성
            local new_file="$MOUNT_PATH/$(generate_random_filename)"
            echo "Creating file: $new_file"
            file_list+=("$new_file")
            ;;
        1) # 파일 생성 후 파일 쓰기
            local new_file="$MOUNT_PATH/$(generate_random_filename)"
            echo "Creating file: $new_file"
            
            # 무작위 길이 (10 ~ 100)와 무작위 문자열 생성
            random_length=$((RANDOM % 262144))
            random_string=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $random_length | head -n 1)
            
            # 무작위 문자열을 파일에 추가
            echo "$random_string" > "$new_file"
            file_list+=("$new_file")
            echo "Writing $random_length to file: $new_file"
            ;;
        2) # 파일 쓰기
            echo "Writing to file: $random_file"
            
            # 무작위 길이 (10 ~ 100)와 무작위 문자열 생성
            random_length=$((RANDOM % 262144))
            random_string=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $random_length | head -n 1)
            
            # 무작위 문자열을 파일에 추가
            echo "$random_string" > "$random_file"
            echo "Writing $random_length to file: $random_file"
            ;;
        3) # 파일 추가 쓰기
            echo "Writing to file: $random_file"
            
            # 무작위 길이 (10 ~ 100)와 무작위 문자열 생성
            random_length=$((RANDOM % 262144))
            random_string=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $random_length | head -n 1)
            
            # 무작위 문자열을 파일에 추가
            echo "$random_string" >> "$random_file"
            echo "Writing $random_length to file: $random_file"
            ;;
        4) # 파일 읽기
            echo "Reading file: $random_file"
            cat "$random_file" > /dev/null
            ;;
        5) # 파일 삭제
            echo "Deleting file: $random_file"
            rm -f "$random_file"
            # 배열에서 $random_file 제거
            file_list=("${file_list[@]/$random_file}")  # 기존 방식 대신 아래 방식 사용
            file_list=($(for f in "${file_list[@]}"; do [ "$f" != "$random_file" ] && echo "$f"; done))
            ;;
        6) # 파일 삭제
            echo "Deleting file: $random_file"
            rm -f "$random_file"
            # 배열에서 $random_file 제거
            file_list=("${file_list[@]/$random_file}")  # 기존 방식 대신 아래 방식 사용
            file_list=($(for f in "${file_list[@]}"; do [ "$f" != "$random_file" ] && echo "$f"; done))
            ;;
        7) # 메모리 캐시 초기화
            echo "Deleting file: $random_file"
            clear_memory_cache
            ;;
            
    esac
}

# 파일 리스트 초기화
initialize_file_list() {
    file_list=()
    for file in "$MOUNT_PATH"/*; do
        [ -f "$file" ] && file_list+=("$file")
    done
    echo "Initialized file list with ${#file_list[@]} files."
}

# 메인 실행
main() {
    echo "Starting I/O traffic generation..."
    initialize_file_list
    for ((i = 0; i < MAX_ITERATIONS; i++)); do
        echo "Iteration $((i + 1)) of $MAX_ITERATIONS"
        random_io_operation
        sleep 0.1  # 작업 간격 (초 단위)
    done
    echo "I/O traffic generation completed."
}

main