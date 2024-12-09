import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://localhost:8080/testitems"
TOTAL_REQUESTS = 10000
MAX_WORKERS = 100  # 可根据机器性能进行调整

def random_string(length=10):
    # 生成指定长度的随机字符串
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_request():
    try:
        # 为每一次请求生成随机的name和description
        name = random_string(8)
        description = random_string(20)
        data = {
            'name': name,
            'description': description
        }
        response = requests.post(URL, data=data, timeout=5)
        # 根据后端逻辑，成功创建item应重定向至index并返回200-3xx状态码
        # 假设一切正常，status_code应为302(redirect)或200
        if response.status_code in [200, 302]:
            return True
        else:
            return False
    except Exception:
        return False

if __name__ == "__main__":
    success_count = 0
    fail_count = 0

    # 使用多线程并发发送请求
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(send_request) for _ in range(TOTAL_REQUESTS)]

        for future in as_completed(futures):
            result = future.result()
            if result:
                success_count += 1
            else:
                fail_count += 1

    print(f"Total requests: {TOTAL_REQUESTS}")
    print(f"Success: {success_count}")
    print(f"Fail: {fail_count}")
    success_rate = (success_count / TOTAL_REQUESTS) * 100
    print(f"Success rate: {success_rate:.2f}%")
