import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

def prepare_sequences(data, features, window_size):
    """
    데이터에서 슬라이딩 윈도우 시퀀스를 준비
    """
    sequences = []
    for i in range(len(data) - window_size + 1):
        seq = data.iloc[i:i+window_size][features].values
        sequences.append(seq)
    return np.array(sequences)

def test_model(test_file, model_path, features, window_size, threshold):
    """
    저장된 모델을 이용해 테스트 데이터를 처리하고 이상치 탐지
    """
    # 테스트 데이터 로드
    df = pd.read_csv(test_file)
    
    # 슬라이딩 윈도우 준비
    test_sequences = prepare_sequences(df, features, window_size)

    # 모델 불러오기
    print(f"Loading model from: {model_path}")
    model = load_model(model_path)

    # 예측
    print("Predicting on test data...")
    reconstructed = model.predict(test_sequences)

    # 재구성 오차 계산
    mse = np.mean(np.power(test_sequences - reconstructed, 2), axis=(1, 2))

    # 이상치 탐지
    anomalies = mse > threshold

    # 결과 저장
    anomaly_scores = np.zeros(len(df))
    anomaly_labels = np.zeros(len(df))
    anomaly_scores[window_size - 1:] = mse
    anomaly_labels[window_size - 1:] = anomalies

    df['anomaly_score'] = anomaly_scores
    df['anomaly_label'] = anomaly_labels

    # 결과 CSV로 저장
    output_file = "data/test_result_with_anomalies_lstm.csv"
    df.to_csv(output_file, index=False)
    print(f"Anomaly detection completed. Results saved to '{output_file}'.")

if __name__ == "__main__":
    # 설정
    TEST_FILE = "data/test_data.csv"  # 테스트 데이터 파일
    MODEL_PATH = "model/lstm_autoencoder_model.keras"  # 저장된 모델 경로
    FEATURES = ['packet_size', 'time_diff', 'packet_direct', 'tcp_size', 'tcp_seq',
                'tcp_ack', 'nvme_packet_type', 'nvme_packet_pdo', 'nvme_packet_plen',
                'nvme_cid', 'nvme_opc', 'remain_data']  # 모델 학습에 사용된 피처
    WINDOW_SIZE = 10  # 슬라이딩 윈도우 크기
    THRESHOLD = 0.005  # 재구성 오차 임계값 (적절히 조정)

    # 테스트 실행
    test_model(TEST_FILE, MODEL_PATH, FEATURES, WINDOW_SIZE, THRESHOLD)
