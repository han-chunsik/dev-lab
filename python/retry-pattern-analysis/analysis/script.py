import pandas as pd
import matplotlib.pyplot as plt
import os

# 🔧 분석할 CSV 파일 목록
CSV_PATHS = [
    "./analysis/result/simple_retry.csv",
    "./analysis/result/backoff.csv",
    "./analysis/result/full_jitter_backoff.csv",
]

# 🔧 출력 폴더
OUTPUT_DIR = "./analysis/graph"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def plot_request_density(csv_path: str, output_dir: str):
    """ts_ms 기준 요청 빈도(ms 단위)를 상대 시간 기준으로 시각화"""
    filename = os.path.splitext(os.path.basename(csv_path))[0]
    df = pd.read_csv(csv_path)

    # ✅ ts_ms를 0부터 시작하는 상대 시간으로 정규화
    min_ts = df['ts_ms'].min()
    df['relative_ms'] = df['ts_ms'] - min_ts

    # ✅ ms별 요청 수 (빈도) 계산
    ms_density = df['relative_ms'].value_counts().sort_index()

    # ✅ 시각화
    plt.figure(figsize=(12, 5))
    plt.plot(ms_density.index, ms_density.values, marker='o', linestyle='-')
    plt.title(f"Request Density per ms - {filename}")
    plt.xlabel("Elapsed Time (ms from start)")
    plt.ylabel("Number of Requests")
    plt.grid(True)

    # ✅ 저장
    output_path = os.path.join(output_dir, f"{filename}_density_per_ms.png")
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"✅ 저장 완료: {output_path}")

# 🔁 모든 파일 반복 처리
for path in CSV_PATHS:
    plot_request_density(path, OUTPUT_DIR)