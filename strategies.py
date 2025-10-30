import time
import threading
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List
import logging
logger = logging.getLogger("strategies")
class Strategy(ABC):
    @abstractmethod
    def execute(self, func: Callable, kwargs: Dict[str, Any]) -> Any:
        pass
class SequentialStrategy(Strategy):
    def execute(self, func: Callable, kwargs: Dict[str, Any]) -> Any:
        logger.debug("SequentialStrategy: executing function directly")
        return func(**kwargs)
class ThreadedStrategy(Strategy):
    def execute(self, func: Callable, kwargs: Dict[str, Any]) -> Any:
        logger.debug("ThreadedStrategy: executing function in a separate thread")
        result = [None]
        exception = [None]
        def target():
            try:
                result[0] = func(**kwargs)
            except Exception as e:
                exception[0] = e
        thread = threading.Thread(target=target)
        thread.start()
        thread.join()
        if exception[0]:
            raise exception[0]
        return result[0]
class BatchedStrategy(Strategy):
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
    def execute(self, func: Callable, kwargs: Dict[str, Any]) -> Any:
        logger.debug(f"BatchedStrategy: executing function with batch_size={self.batch_size}")
        iterable = kwargs.get('items', [])
        if not hasattr(iterable, '__iter__'):
            return func(**kwargs)
        results = []
        batch = []
        for item in iterable:
            batch.append(item)
            if len(batch) >= self.batch_size:
                batch_kwargs = kwargs.copy()
                batch_kwargs['items'] = batch
                results.append(func(**batch_kwargs))
                batch = []
        if batch:
            batch_kwargs = kwargs.copy()
            batch_kwargs['items'] = batch
            results.append(func(**batch_kwargs))
        return results
