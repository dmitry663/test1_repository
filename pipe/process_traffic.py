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
        row.append(data[header.index('frame.time_epoch')])
        row.append(-1 if prev_line is None or data[header.index('frame.time_epoch')] - prev_line[transform_header.index('timestamp')]>5 else 0 if tump > 0 else data[header.index('frame.time_epoch')] - prev_line[transform_header.index('timestamp')])
        row.append(data[header.index('frame.len')])         
        if data[header.index('tcp.dstport')] == 4420:
            row.append(0)
        elif data[header.index('tcp.srcport')] == 4420:
            row.append(1)
        else:
            row.append(-1)
        row.append(data[header.index('tcp.seq_raw')])
        row.append(data[header.index('tcp.len')])
        row.append(data[header.index('tcp.ack_raw')])
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
    if not len(data)-data_size+1>0:
        return None
    
    sequences = []
    for i in range(len(data)-data_size,len(data)):
        seq = data.iloc[i-window_size:i][features].values
        sequences.append(seq)
    return np.array(sequences)

def main(model_path, features, window_size, THRESHOLD):
    # main 함수 내부
    df = pd.DataFrame(columns=features)  # 빈 데이터프레임으로 초기화
    anomaly_scores=[]

    # 모델 로드
    model = load_model(model_path)
    print(f"Model loaded from: {model_path}")

    # 실시간 데이터 읽기
    # stdin에서 실시간으로 데이터 읽기
    for line in sys.stdin:
        if line.strip():  # 빈 줄이 아닌 경우만 처리
            # 데이터 변환
            header, data = transform_data(line)
            print(f"transform data:{len(data)}")

            # 리스트에 데이터 추가
            _,new_df= scaler_data(pd.DataFrame(data, columns=header))
            df = pd.concat([df, new_df], axis=0)

            # 윈도우 생성(추가된 만큼)
            sequences = prepare_sequences(df, features, window_size, len(data))
            
            if sequences is None or len(sequences) == 0:
                print("Insufficient data for sequences. Skipping...")
                continue  # 다음 데이터로 이동
            # 생성된 원도우 mse 구하기
            if sequences is not None and len(sequences) > 0:
                reconstructed = model.predict(sequences)
                mse = np.mean(np.power(sequences - reconstructed, 2), axis=(1, 2))# 재구성 오차 계산
            
                # mse 알림 또는 그래프에 추가
                anomaly_scores.extend(mse)
                for fild in mse:
                    print(fild)


if __name__ == "__main__":
    # 설정
    MODEL_PATH = "model/lstm_autoencoder_model.keras"  # 저장된 모델 경로
    FEATURES = ['packet_size', 'time_diff', 'packet_direct', 'tcp_size', 'tcp_seq',
                'tcp_ack', 'nvme_packet_type', 'nvme_packet_pdo', 'nvme_packet_plen',
                'nvme_cid', 'nvme_opc', 'remain_data']  # 모델 학습에 사용된 피처
    WINDOW_SIZE = 10  # 슬라이딩 윈도우 크기
    THRESHOLD = 0.005  # 재구성 오차 임계값 (적절히 조정)

    # 테스트 실행
    # anomaly_detection_pipe(TEST_FILE, MODEL_PATH, FEATURES, WINDOW_SIZE, THRESHOLD)
    main(MODEL_PATH, FEATURES, WINDOW_SIZE, THRESHOLD)
