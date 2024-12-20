import sys
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

def transform_data(next_line, prev_line = None, num=0):

    header = ['frame.number','frame.len','frame.time_relative','frame.time_epoch','frame.protocols','ip.src','ip.dst','tcp.srcport','tcp.dstport','tcp.seq_raw','tcp.len','tcp.ack_raw','nvme-tcp.type','nvme-tcp.pdo','nvme-tcp.plen','nvme.cmd.cid','nvme.cqe.cid','nvme-tcp.cmd.cid','nvme.cmd.opc']
    data = next_line.split("\t")

    transform_header = ['num','timestamp','time_diff','packet_size','packet_direct','tcp_seq','tcp_size','tcp_ack','nvme_packet_type','nvme_packet_pdo','nvme_packet_plen','nvme_cid','nvme_opc','remain_data']
    transform_data = []

    
    # 데이터 중복 정리
    data[header.index('nvme-tcp.type')] = [] if type(data[header.index('nvme-tcp.type')]) is not type("") else [int(i) for i in data[header.index('nvme-tcp.type')].split(',') if len(i)>0]
    data[header.index('nvme-tcp.pdo')] = [] if type(data[header.index('nvme-tcp.pdo')]) is not type("") else [int(i) for i in data[header.index('nvme-tcp.pdo')].split(',') if len(i)>0]
    data[header.index('nvme-tcp.plen')] = [] if type(data[header.index('nvme-tcp.plen')]) is not type("") else [int(i) for i in data[header.index('nvme-tcp.plen')].split(',') if len(i)>0]
    data[header.index('nvme.cmd.cid')] = [] if type(data[header.index('nvme.cmd.cid')]) is not type("") else [int(i,16) for i in data[header.index('nvme.cmd.cid')].split(',') if len(i)>0]
    data[header.index('nvme.cqe.cid')] = [] if type(data[header.index('nvme.cqe.cid')]) is not type("") else [int(i,16) for i in data[header.index('nvme.cqe.cid')].split(',') if len(i)>0]
    data[header.index('nvme-tcp.cmd.cid')] = [] if type(data[header.index('nvme-tcp.cmd.cid')]) is not type("") else [int(i,16) for i in data[header.index('nvme-tcp.cmd.cid')].split(',') if len(i)>0]
    data[header.index('nvme.cmd.opc')] = [] if type(data[header.index('nvme.cmd.opc')]) is not type("") else [int(i,16) for i in data[header.index('nvme.cmd.opc')].split(',') if len(i)>0]


    for tump in range(1 if len(data[header.index('nvme-tcp.type')])==0 else  len(data[header.index('nvme-tcp.type')])):
        # 데이터 정리    
        row = []

        row.append(num)
        row.append(float(data[header.index('frame.time_epoch')]))
        row.append(-1 if prev_line is None or data[header.index('frame.time_epoch')] - prev_line[transform_header.index('timestamp')]>5 else 0 if tump > 0 else data[header.index('frame.time_epoch')] - prev_line[transform_header.index('timestamp')])
        row.append(int(data[header.index('frame.len')]))         
        if data[header.index('tcp.dstport')] == 4420:
            row.append(0)
        elif data[header.index('tcp.srcport')] == 4420:
            row.append(1)
        else:
            row.append(-1)
        row.append(int(data[header.index('tcp.seq_raw')]))
        row.append(int(data[header.index('tcp.len')]))
        row.append(int(data[header.index('tcp.ack_raw')]))
        row.append(data[header.index('nvme-tcp.type')][0] if len(data[header.index('nvme-tcp.type')]) else -1)
        row.append(data[header.index('nvme-tcp.pdo')][0] if len(data[header.index('nvme-tcp.pdo')]) else -1)
        row.append(data[header.index('nvme-tcp.plen')][0] if len(data[header.index('nvme-tcp.plen')]) else -1)
        if len(data[header.index('nvme.cmd.cid')]) > 0 and data[header.index('nvme-tcp.type')][0] == 4:
            row.append(data[header.index('nvme.cmd.cid')].pop(0))
        elif len(data[header.index('nvme.cqe.cid')]) > 0 and data[header.index('nvme-tcp.type')][0] == 5:
            row.append(data[header.index('nvme.cqe.cid')].pop(0))
        elif len(data[header.index('nvme-tcp.cmd.cid')]) > 0 and data[header.index('nvme-tcp.type')][0] == 7:
            row.append(data[header.index('nvme-tcp.cmd.cid')].pop(0))
        else:
            row.append(-1)
        row.append(data[header.index('nvme.cmd.opc')].pop(0) if len(data[header.index('nvme.cmd.opc')])>0 and data[header.index('nvme-tcp.type')][0] == 4 else -1)
        if len(data[header.index('nvme-tcp.type')])>0:
            data[header.index('nvme-tcp.type')].pop(0)
            data[header.index('nvme-tcp.pdo')].pop(0)
            data[header.index('nvme-tcp.plen')].pop(0)
        row.append(1 if len(data[header.index('nvme-tcp.type')]) > 0 else 0)
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

def prepare_sequences(data, features, window_size, data_size=1):
    if not len(data) - data_size + 1 > 0:
        return None

    # 데이터 타입 강제 변환
    data[features] = data[features].apply(pd.to_numeric, errors='coerce').fillna(0)

    sequences = []
    for i in range(len(data) - data_size, len(data)):
        seq = data.iloc[i - window_size:i][features].values.astype('float32')  # float32로 변환
        sequences.append(seq)
    return np.array(sequences)


import sys
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from collections import deque

def update_plot(ax, line, mse_window, threshold):
    """실시간 그래프 업데이트"""
    line.set_ydata(mse_window)
    line.set_xdata(range(len(mse_window)))
    ax.relim()  # 축 한계 재조정
    ax.autoscale_view()  # 축 크기 자동 조정
    ax.axhline(threshold, color="red", linestyle="--", label="Threshold")
    plt.draw()
    plt.pause(0.1)  # 짧은 지연으로 업데이트

def main(model_path, features, window_size, THRESHOLD):
    # DataFrame 초기화
    df = pd.DataFrame(columns=features)
    mse_window = deque(maxlen=50)  # 최근 50개의 MSE 값을 저장

    # 그래프 초기화
    plt.ion()  # 인터랙티브 모드 활성화
    fig, ax = plt.subplots(figsize=(10, 6))
    line, = ax.plot([], [], label="MSE", color="blue")
    ax.set_title("Real-Time Anomaly Detection")
    ax.set_xlabel("Sequence")
    ax.set_ylabel("MSE")
    ax.grid(True)
    ax.legend()

    # 모델 로드
    model = load_model(model_path)
    print(f"Model loaded from: {model_path}")

    try:
        # 실시간 데이터 읽기
        for line in sys.stdin:
            if line.strip():  # 빈 줄 무시
                # 데이터 변환
                header, data = transform_data(line.strip())
                print(f"Data received: {len(data)}")

                # DataFrame으로 변환 및 정규화
                new_df = pd.DataFrame(data, columns=header)
                _, new_df = scaler_data(new_df)

                # 빈 데이터프레임 체크
                if not new_df.empty:
                    df = pd.concat([df, new_df], axis=0)
                else:
                    print("Warning: new_df is empty. Skipping...")
                    continue

                # 데이터 충분성 체크
                if len(df) < window_size:
                    print("Not enough data to create sequences. Skipping...")
                    continue

                # 윈도우 생성
                sequences = prepare_sequences(df, features, window_size, len(data))

                if sequences is None or sequences.shape[1] == 0:
                    print("Invalid sequences generated. Skipping...")
                    continue

                # 모델 예측
                reconstructed = model.predict(sequences)
                mse = np.mean(np.power(sequences - reconstructed, 2), axis=(1, 2))  # 재구성 오차 계산

                # 최근 MSE 값을 저장하고 그래프 업데이트
                mse_window.extend(mse)
                update_plot(ax, line, mse_window, THRESHOLD)

                # 결과 출력
                for score in mse:
                    print(f"Anomaly score: {score}")

    except KeyboardInterrupt:
        # Ctrl+C 발생 시
        print("\nKeyboardInterrupt detected. Exiting gracefully...")

    finally:
        # 그래프 표시
        plt.ioff()  # 인터랙티브 모드 종료
        plt.show()


if __name__ == "__main__":
    # 설정
    MODEL_PATH = "model/lstm_autoencoder_model.keras"  # 저장된 모델 경로
    FEATURES = ['packet_size', 'time_diff', 'packet_direct', 'tcp_size', 'tcp_seq',
                'tcp_ack', 'nvme_packet_type', 'nvme_packet_pdo', 'nvme_packet_plen',
                'nvme_cid', 'nvme_opc', 'remain_data']  # 모델 학습에 사용된 피처
    WINDOW_SIZE = 10  # 슬라이딩 윈도우 크기
    THRESHOLD = 0.005  # 재구성 오차 임계값 (적절히 조정)

    # 실행
    main(MODEL_PATH, FEATURES, WINDOW_SIZE, THRESHOLD)
