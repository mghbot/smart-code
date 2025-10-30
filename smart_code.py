import functools
import inspect
import logging
import time
import json
import os
import threading
from typing import Any, Callable, Dict, List, Optional, Tuple
from strategies import Strategy, SequentialStrategy, ThreadedStrategy, BatchedStrategy
from profiler import Profiler
from learner import Learner
from storage import Storage
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("smart_code")
class SmartCodeError(Exception):
    pass
def smart_code(*, strategies: Optional[List[Strategy]] = None, storage_path: str = ".smart_code.json", min_calls: int = 3, alpha: float = 0.9) -> Callable[[Callable], Callable]:
    if strategies is None:
        strategies = [SequentialStrategy(), ThreadedStrategy(), BatchedStrategy()]
    storage = Storage(storage_path)
    learner = Learner(storage, min_calls=min_calls, alpha=alpha)
    def decorator(func: Callable) -> Callable:
        func_id = f"{func.__module__}.{func.__qualname__}"
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            call_args = dict(bound.arguments)
            try:
                chosen_strategy = learner.select_strategy(func_id, strategies)
                logger.info(f"Selected strategy: {chosen_strategy.__class__.__name__} for {func_id}")
            except Exception as e:
                logger.warning(f"Strategy selection failed for {func_id}: {e}. Falling back to SequentialStrategy.")
                chosen_strategy = SequentialStrategy()
            profiler = Profiler()
            profiler.start()
            try:
                result = chosen_strategy.execute(func, call_args)
            except Exception as exec_err:
                logger.error(f"Strategy {chosen_strategy.__class__.__name__} failed for {func_id}: {exec_err}")
                raise SmartCodeError(f"Strategy execution failed: {exec_err}") from exec_err
            finally:
                elapsed = profiler.stop()
                learner.record_call(func_id, chosen_strategy.__class__.__name__, elapsed)
                logger.info(f"Recorded {elapsed:.4f}s for {func_id} with {chosen_strategy.__class__.__name__}")
            return result
        wrapper._smart_code_strategies = strategies
        wrapper._smart_code_learner = learner
        return wrapper
    return decorator
