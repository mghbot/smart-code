import time
import logging
logger = logging.getLogger("profiler")
class Profiler:
    def __init__(self):
        self._start = None
        self._elapsed = None
    def start(self):
        self._start = time.perf_counter()
    def stop(self) -> float:
        if self._start is None:
            raise RuntimeError("Profiler was not started")
        self._elapsed = time.perf_counter() - self._start
        logger.debug(f"Profiling stopped: {self._elapsed:.6f}s")
        return self._elapsed
    @property
    def elapsed(self) -> float:
        if self._elapsed is None:
            raise RuntimeError("Profiler has not been stopped")
        return self._elapsed
