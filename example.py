import logging
import time
import random
from typing import List
from smart_code import smart_code
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("example")
def dummy_work(n: int) -> float:
    s = 0.0
    for _ in range(n * 1000):
        s += random.random()
    return s
@smart_code()
def process_items(items: List[int]) -> List[float]:
    logger.info(f"Processing {len(items)} items")
    results = []
    for item in items:
        results.append(dummy_work(item))
    return results
if __name__ == "__main__":
    for i in range(15):
        data = [random.randint(10, 50) for _ in range(20)]
        start = time.perf_counter()
        result = process_items(data)
        elapsed = time.perf_counter() - start
        logger.info(f"Run {i+1}: returned {len(result)} results in {elapsed:.4f}s")
