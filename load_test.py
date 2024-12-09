import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

URL = "http://localhost:8080/testitems"
TOTAL_REQUESTS = 10000
MAX_WORKERS = 100

def random_string(length=10):

    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_request():
    try:

        name = random_string(8)
        description = random_string(20)
        data = {
            'name': name,
            'description': description
        }
        response = requests.post(URL, data=data, timeout=5)

        if response.status_code in [200, 302]:
            return True
        else:
            return False
    except Exception:
        return False

if __name__ == "__main__":
    success_count = 0
    fail_count = 0

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
