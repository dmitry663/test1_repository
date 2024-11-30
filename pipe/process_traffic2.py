import sys
from tensorflow.keras.models import load_model

def process_line(line):
    # 각 라인을 처리하는 함수
    print(f"Processed: {line.strip()}")  # 예: 데이터를 가공하여 출력

def main():
    MODEL_PATH = "model/lstm_autoencoder_model.keras"  # 저장된 모델 경로

    # 모델 로드
    model_path = "model/lstm_autoencoder_model.keras"
    model = load_model(model_path)
    print(f"Model loaded from: {model_path}")

    
    # stdin에서 실시간으로 데이터 읽기
    for line in sys.stdin:
        if line.strip():  # 빈 줄이 아닌 경우만 처리
            process_line(line)

if __name__ == "__main__":
    main()
