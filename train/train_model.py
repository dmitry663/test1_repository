import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector, TimeDistributed
from tensorflow.keras.models import load_model

def transform_data(file_path = "data/output", sep="\t"):
    df = pd.read_csv(file_path, sep=sep)

    # 헤더와 데이터 분리
    header = list(df.columns)  # 헤더를 리스트로 추출
    data = df.values.tolist()  # 데이터를 2차원 리스트로 변환

    transform_header = ['num','timestamp','time_diff','packet_size','packet_direct','tcp_seq','tcp_size','tcp_ack','nvme_packet_type','nvme_packet_pdo','nvme_packet_plen','nvme_cid','nvme_opc','remain_data']
    transform_data = []

    for i in range(len(data)):
        # 데이터 중복 정리
        data[i][header.index('nvme-tcp.type')] = [] if type(data[i][header.index('nvme-tcp.type')]) is not type("") else [int(i) for i in data[i][header.index('nvme-tcp.type')].split(',') if len(i)>0]
        data[i][header.index('nvme-tcp.pdo')] = [] if type(data[i][header.index('nvme-tcp.pdo')]) is not type("") else [int(i) for i in data[i][header.index('nvme-tcp.pdo')].split(',') if len(i)>0]
        data[i][header.index('nvme-tcp.plen')] = [] if type(data[i][header.index('nvme-tcp.plen')]) is not type("") else [int(i) for i in data[i][header.index('nvme-tcp.plen')].split(',') if len(i)>0]
        data[i][header.index('nvme.cmd.cid')] = [] if type(data[i][header.index('nvme.cmd.cid')]) is not type("") else [int(i,16) for i in data[i][header.index('nvme.cmd.cid')].split(',') if len(i)>0]
        data[i][header.index('nvme.cqe.cid')] = [] if type(data[i][header.index('nvme.cqe.cid')]) is not type("") else [int(i,16) for i in data[i][header.index('nvme.cqe.cid')].split(',') if len(i)>0]
        data[i][header.index('nvme-tcp.cmd.cid')] = [] if type(data[i][header.index('nvme-tcp.cmd.cid')]) is not type("") else [int(i,16) for i in data[i][header.index('nvme-tcp.cmd.cid')].split(',') if len(i)>0]
        data[i][header.index('nvme.cmd.opc')] = [] if type(data[i][header.index('nvme.cmd.opc')]) is not type("") else [int(i,16) for i in data[i][header.index('nvme.cmd.opc')].split(',') if len(i)>0]

        
        for tump in range(1 if len(data[i][header.index('nvme-tcp.type')])==0 else  len(data[i][header.index('nvme-tcp.type')])):

            # 데이터 정리    
            row = []

            row.append(i)
            row.append(data[i][header.index('frame.time_epoch')])
            row.append(-1 if i==0 or data[i][header.index('frame.time_epoch')] - data[i-1][header.index('frame.time_epoch')]>5 else 0 if tump > 0 else data[i][header.index('frame.time_epoch')] - data[i-1][header.index('frame.time_epoch')])
            row.append(data[i][header.index('frame.len')])         
            if data[i][header.index('tcp.dstport')] == 4420:
                row.append(0)
            elif data[i][header.index('tcp.srcport')] == 4420:
                row.append(1)
            else:
                row.append(-1)
            row.append(data[i][header.index('tcp.seq_raw')])
            row.append(data[i][header.index('tcp.len')])
            row.append(data[i][header.index('tcp.ack_raw')])
            row.append(data[i][header.index('nvme-tcp.type')][0] if len(data[i][header.index('nvme-tcp.type')]) else -1)
            row.append(data[i][header.index('nvme-tcp.pdo')][0] if len(data[i][header.index('nvme-tcp.pdo')]) else -1)
            row.append(data[i][header.index('nvme-tcp.plen')][0] if len(data[i][header.index('nvme-tcp.plen')]) else -1)
            if len(data[i][header.index('nvme.cmd.cid')]) > 0 and data[i][header.index('nvme-tcp.type')][0] == 4:
                row.append(data[i][header.index('nvme.cmd.cid')].pop(0))
            elif len(data[i][header.index('nvme.cqe.cid')]) > 0 and data[i][header.index('nvme-tcp.type')][0] == 5:
                row.append(data[i][header.index('nvme.cqe.cid')].pop(0))
            elif len(data[i][header.index('nvme-tcp.cmd.cid')]) > 0 and data[i][header.index('nvme-tcp.type')][0] == 7:
                row.append(data[i][header.index('nvme-tcp.cmd.cid')].pop(0))
            else:
                row.append(-1)
            row.append(data[i][header.index('nvme.cmd.opc')].pop(0) if len(data[i][header.index('nvme.cmd.opc')])>0 and data[i][header.index('nvme-tcp.type')][0] == 4 else -1)
            if len(data[i][header.index('nvme-tcp.type')])>0:
                data[i][header.index('nvme-tcp.type')].pop(0)
                data[i][header.index('nvme-tcp.pdo')].pop(0)
                data[i][header.index('nvme-tcp.plen')].pop(0)
            row.append(1 if len(data[i][header.index('nvme-tcp.type')]) > 0 else 0)
            transform_data.append(row)

    print("transform_data:")
    return transform_header, transform_data

def save_data(output_file = "data/transform_data.csv", header = [], data = []):
    df_transformed = pd.DataFrame(data, columns=header)# DataFrame 생성
    df_transformed.to_csv(output_file, index=False)# CSV로 저장
    print(f"Data saved to {output_file}")

# 정규화 함수
def scaler_data(df):
    
    features = ['packet_size', 'time_diff','packet_direct', 'tcp_size', 'tcp_seq', 'tcp_ack','nvme_packet_type','nvme_packet_pdo','nvme_packet_plen','nvme_cid','nvme_opc','remain_data']
    df['packet_size'] = df['packet_size'] / 65535
    df['time_diff'] = (df['time_diff']+1) / 6
    df['tcp_size'] = df['tcp_size'] / 65535
    df['tcp_seq'] = df['tcp_seq'] / 4294967295
    df['tcp_ack'] = df['tcp_ack'] / 4294967295
    df['nvme_packet_type'] = (df['nvme_packet_type']+1) / 16
    df['nvme_packet_pdo'] = (df['nvme_packet_pdo']+1) / 256
    df['nvme_packet_plen'] = (df['nvme_packet_plen']+1) / 65535
    df['nvme_cid'] = (df['nvme_cid']+1) / 65535
    df['nvme_opc'] = (df['nvme_opc']+1) / 32
    
    print("scaler_data:")
    return features,df

def prepare_sequences(data, features, window_size):
    sequences = []
    for i in range(len(data) - window_size + 1):
        seq = data.iloc[i:i+window_size][features].values
        sequences.append(seq)
    return np.array(sequences)

def build_lstm_autoencoder(input_shape):
    model = Sequential([
        LSTM(64, activation='relu', input_shape=(input_shape[1], input_shape[2]), return_sequences=True),
        LSTM(32, activation='relu', return_sequences=False),
        RepeatVector(input_shape[1]),
        LSTM(32, activation='relu', return_sequences=True),
        LSTM(64, activation='relu', return_sequences=True),
        TimeDistributed(Dense(input_shape[2]))
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

from sklearn.preprocessing import RobustScaler


if __name__== "__main__":
    
    # 시계열 윈도우 크기
    window_size = 10

    # 데이터 전처리
    header, data = transform_data(file_path = "data/output", sep="\t")
    save_data(output_file = "data/transform_data.csv", header = header, data = data)

    # DataFrame 생성
    df = pd.DataFrame(data, columns=header)

    # 데이터 정규화
    features, scaled_df = scaler_data(df)
    scaled_df.to_csv("data/scaler_data.csv", index=False)

    # 슬라이딩 윈도우 생성
    sequences = prepare_sequences(df, features, window_size)

    # LSTM Autoencoder 모델 정의
    input_shape = sequences.shape
    model = build_lstm_autoencoder(input_shape)

    # 모델 학습 (정상 데이터만 사용)
    print("Training LSTM Autoencoder...")
    model.fit(sequences, sequences, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

    # 모델 저장 (TensorFlow 형식, Keras 3 기준)
    model_save_path = "model/lstm_autoencoder_model.keras"  # .keras 확장자 사용
    model.save(model_save_path)
    print(f"Model saved to: {model_save_path}")

    # 테스트 데이터 준비
    test_sequences = prepare_sequences(df, features, window_size)
        
    # 모델 로드
    model_path = "model/lstm_autoencoder_model.keras"
    model = load_model(model_path)
    print(f"Model loaded from: {model_path}")

    # 테스트 데이터 예측
    print("Predicting on test data...")
    reconstructed = model.predict(test_sequences)
    
    # 재구성 오차 계산
    mse = np.mean(np.power(test_sequences - reconstructed, 2), axis=(1, 2))
    
    # 이상치 탐지 (재구성 오차 임계값)
    threshold = np.percentile(mse, 95)  # 상위 5%를 이상치로 간주
    anomalies = mse > threshold
    
    # 결과 저장
    anomaly_scores = np.zeros(len(df))
    anomaly_labels = np.zeros(len(df))
    anomaly_scores[window_size - 1:] = mse
    anomaly_labels[window_size - 1:] = anomalies
    
    df['anomaly_score'] = anomaly_scores
    df['anomaly_label'] = anomaly_labels
    
    df.to_csv("data/result_with_anomalies_lstm.csv", index=False)
    print("Anomaly detection completed. Results saved to 'data/result_with_anomalies_lstm.csv'.")
