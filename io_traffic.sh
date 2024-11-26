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

# 랜덤 작업 수행
random_io_operation() {
    local operation=$((RANDOM % 5))
    local random_file=${file_list[$((RANDOM % ${#file_list[@]}))]}

    case $operation in
        0) # 파일 생성
            local new_file="$MOUNT_PATH/$(generate_random_filename)"
            echo "Creating file: $new_file"
            echo "This is a test file." > "$new_file"
            file_list+=("$new_file")
            ;;
        1) # 파일 쓰기
            echo "Writing to file: $random_file"
            echo "Appending data at $(date)" >> "$random_file"
            ;;
        2) # 파일 읽기
            echo "Reading file: $random_file"
            cat "$random_file" > /dev/null
            ;;
        3) # 파일 삭제
            echo "Deleting file: $random_file"
            rm -f "$random_file"
            file_list=("${file_list[@]/$random_file}")
            ;;
        4) # 파일 정보 조회
            echo "File info for: $random_file"
            ls -lh "$random_file"
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
