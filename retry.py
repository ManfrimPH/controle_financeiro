import random
import time
import logging
from functools import wraps

logger = logging.getLogger("finance_bot.retry")


class RetryError(Exception):
    pass


def with_retry(func, max_retries=5, base_delay=1, max_delay=30):
    @wraps(func)
    def wrapper(*args, **kwargs):
        last_exc = None
        for attempt in range(1, max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exc = e
                if attempt == max_retries:
                    break
                delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                jitter = random.uniform(0, delay * 0.3)
                logger.warning(
                    "%s falhou (tentativa %d/%d): %s. Nova tentativa em %.1fs...",
                    func.__name__, attempt, max_retries, e, delay + jitter,
                )
                time.sleep(delay + jitter)
        raise RetryError(f"{func.__name__} falhou após {max_retries} tentativas: {last_exc}")
    return wrapper


def retry_methods(bot):
    for method in ("send_message", "edit_message_text", "answer_callback_query"):
        if hasattr(bot, method):
            setattr(bot, method, with_retry(getattr(bot, method)))
    return bot
