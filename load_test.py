import redis
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "redis-14124.c44.us-east-1-2.ec2.redns.redis-cloud.com")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 14124))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", None)
REDIS_SSL = os.environ.get("REDIS_SSL", "false").lower() in ("true", "1", "t")

TOTAL_REQUESTS = 10000
MAX_WORKERS = 20

redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, ssl=REDIS_SSL, decode_responses=True
)


def random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def send_request_to_redis():
    try:
        name = random_string(8)
        description = random_string(20)

        key = f"item:{name}"
        value = description

        redis_client.set(key, value)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    success_count = 0
    fail_count = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(send_request_to_redis) for _ in range(TOTAL_REQUESTS)]

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
    assert success_rate > 99.9999
