import time

def retry(max_retries=3, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 1
            while attempt <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries:
                        raise
                    print(f"  ⚠️ Attempt {attempt} failed: {e} — retrying...")
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator