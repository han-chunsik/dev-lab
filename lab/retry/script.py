import random
import time
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# 설정 값
SUCCESS_RATE = 0.7
TOTAL_REQUESTS = 100
MAX_RETRIES = 3
MAX_WORKERS = 100
BASE_BACKOFF_SEC = 0.1

# 결과 저장 경로
BASE_DIR = Path(__file__).resolve().parent
RESULT_DIR = BASE_DIR / "../../analysis/retry/result"
RESULT_DIR.mkdir(parents=True, exist_ok=True)


def now_ms():
    return int(time.time() * 1000)


def send_request(req_id):
    return random.random() < SUCCESS_RATE


def simple_retry_thread(req_id):
    logs = []
    for attempt in range(1, MAX_RETRIES + 1):
        ts = now_ms()
        success = send_request(req_id)
        logs.append((req_id, attempt, success, ts))
        if success:
            break
    return logs


def backoff_retry_thread(req_id):
    logs = []
    for attempt in range(1, MAX_RETRIES + 1):
        ts = now_ms()
        success = send_request(req_id)
        logs.append((req_id, attempt, success, ts))
        if success:
            break
        time.sleep(BASE_BACKOFF_SEC * (2 ** (attempt - 1)))
    return logs


def jitter_retry_thread(req_id):
    logs = []
    for attempt in range(1, MAX_RETRIES + 1):
        ts = now_ms()
        success = send_request(req_id)
        logs.append((req_id, attempt, success, ts))
        if success:
            break
        max_delay = BASE_BACKOFF_SEC * (2 ** (attempt - 1))
        time.sleep(random.uniform(0, max_delay))
    return logs


def save_attempt_logs_to_csv(attempt_logs, strategy_name):
    filename = f"{strategy_name.lower().replace(' ', '_')}.csv"
    filepath = RESULT_DIR / filename

    with open(filepath, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["req_id", "attempt", "success", "ts_ms"])
        for log in attempt_logs:
            writer.writerow(log)

    print(f"재시도 단위 로그 저장됨 → {filepath.resolve()}")


def run_simulation(thread_fn, strategy_name):
    print(f"재시도 전략: {strategy_name}")
    all_logs = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(thread_fn, req_id) for req_id in range(TOTAL_REQUESTS)]
        for future in futures:
            all_logs.extend(future.result())

    # 성공률 계산
    success_count = sum(1 for log in all_logs if log[2] and log[1] == 1)
    total_success = len(set(log[0] for log in all_logs if log[2])) 
    success_rate = 100 * total_success / TOTAL_REQUESTS
    avg_attempts = len(all_logs) / TOTAL_REQUESTS

    print(f"✅ 요청 기준 성공률: {success_rate:.2f}%")
    print(f"🔁 평균 재시도 횟수: {avg_attempts:.2f}회")

    save_attempt_logs_to_csv(all_logs, strategy_name)


if __name__ == "__main__":
    run_simulation(simple_retry_thread, "Simple Retry")
    run_simulation(backoff_retry_thread, "Backoff")
    run_simulation(jitter_retry_thread, "Full Jitter Backoff")
