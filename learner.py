import logging
import statistics
from typing import Dict, List, Optional
from storage import Storage
from strategies import Strategy
logger = logging.getLogger("learner")
class Learner:
    def __init__(self, storage: Storage, min_calls: int = 3, alpha: float = 0.9):
        self.storage = storage
        self.min_calls = min_calls
        self.alpha = alpha
    def select_strategy(self, func_id: str, strategies: List[Strategy]) -> Strategy:
        data = self.storage.load()
        key = f"func:{func_id}"
        if key not in data or not data[key]:
            logger.info(f"No historical data for {func_id}; defaulting to first strategy")
            return strategies[0]
        strategy_times = data[key]
        for strategy in strategies:
            name = strategy.__class__.__name__
            times = strategy_times.get(name, [])
            if len(times) < self.min_calls:
                logger.info(f"EXPLORING: {name} needs more data ({len(times)}/{self.min_calls})")
                return strategy
        best_strategy = None
        best_score = float('inf')
        for strategy in strategies:
            name = strategy.__class__.__name__
            times = strategy_times.get(name, [])
            score = statistics.median(times)
            logger.info(f"Strategy {name} median time: {score:.6f}s")
            if score < best_score:
                best_score = score
                best_strategy = strategy
        return best_strategy if best_strategy else strategies[0]
    def record_call(self, func_id: str, strategy_name: str, elapsed: float):
        data = self.storage.load()
        key = f"func:{func_id}"
        if key not in data:
            data[key] = {}
        if strategy_name not in data[key]:
            data[key][strategy_name] = []
        data[key][strategy_name].append(elapsed)
        self.storage.save(data)
        logger.debug(f"Recorded {elapsed:.6f}s for {func_id}:{strategy_name}")
