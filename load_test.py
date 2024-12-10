import requests
import random
import string
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

# 配置
URL = "http://localhost:8080/testitems"
TOTAL_REQUESTS = 10000
MAX_WORKERS = 100

def random_string(length=10):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_request():
    """发送单个请求并记录延迟"""
    try:
        name = random_string(8)
        description = random_string(20)
        data = {
            'name': name,
            'description': description
        }

        start_time = time.time()
        response = requests.post(URL, data=data, timeout=5)
        latency = time.time() - start_time

        # 状态码 200 和 302 视为成功
        if response.status_code in [200, 302]:
            return True, latency
        else:
            return False, latency
    except Exception:
        return False, None

if __name__ == "__main__":
    success_count = 0
    fail_count = 0
    latencies = []

    # 开始测试
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(send_request) for _ in range(TOTAL_REQUESTS)]

        for future in as_completed(futures):
            result, latency = future.result()
            if result:
                success_count += 1
                if latency is not None:
                    latencies.append(latency)
            else:
                fail_count += 1

    end_time = time.time()

    # 计算性能指标
    total_time = end_time - start_time
    success_rate = (success_count / TOTAL_REQUESTS) * 100
    avg_latency = statistics.mean(latencies) if latencies else 0
    max_latency = max(latencies, default=0)
    min_latency = min(latencies, default=0)

    # 输出结果
    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Success: {success_count}")
    print(f"Fail: {fail_count}")
    print(f"Success rate: {success_rate:.2f}%")
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average latency: {avg_latency:.4f} seconds")
    print(f"Max latency: {max_latency:.4f} seconds")
    print(f"Min latency: {min_latency:.4f} seconds")
    print(f"Requests per second: {TOTAL_REQUESTS / total_time:.2f}")

    # 将结果保存为 CSV
    with open("performance_results.csv", "w") as file:
        file.write("Total requests,Success,Fail,Success rate,Total time,Average latency,Max latency,Min latency,Requests per second\n")
        file.write(f"{TOTAL_REQUESTS},{success_count},{fail_count},{success_rate:.2f},{total_time:.2f},{avg_latency:.4f},{max_latency:.4f},{min_latency:.4f},{TOTAL_REQUESTS / total_time:.2f}\n")

    print("Results saved to performance_results.csv")
