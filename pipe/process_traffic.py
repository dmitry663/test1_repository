import sys

def process_line(line):
    # 각 라인을 처리하는 함수
    print(f"Processed: {line.strip()}")  # 예: 데이터를 가공하여 출력

def main():
    # stdin에서 실시간으로 데이터 읽기
    for line in sys.stdin:
        if line.strip():  # 빈 줄이 아닌 경우만 처리
            process_line(line)

if __name__ == "__main__":
    main()
