import pytest

from retry import with_retry, retry_methods, RetryError


class FakeBot:
    def __init__(self):
        self.send_message_calls = 0

    def send_message(self, chat_id, text, **kwargs):
        self.send_message_calls += 1
        if self.send_message_calls < 3:
            raise ConnectionError("network is unreachable")
        return {"ok": True, "text": text}


def test_with_retry_succeeds_after_failures():
    fake = FakeBot()
    wrapped = with_retry(fake.send_message, max_retries=5, base_delay=0)
    result = wrapped(1, "oi")
    assert result == {"ok": True, "text": "oi"}
    assert fake.send_message_calls == 3


def test_with_retry_raises_after_max_retries():
    def always_fail():
        raise ConnectionError("boom")

    wrapped = with_retry(always_fail, max_retries=3, base_delay=0)
    with pytest.raises(RetryError):
        wrapped()


def test_with_retry_succeeds_first_try():
    calls = []

    def ok():
        calls.append(1)
        return "done"

    wrapped = with_retry(ok, max_retries=3, base_delay=0)
    assert wrapped() == "done"
    assert len(calls) == 1


def test_retry_methods_wraps_telegram_methods():
    class MiniBot:
        def send_message(self, *a, **k):
            return 1

        def edit_message_text(self, *a, **k):
            return 2

        def answer_callback_query(self, *a, **k):
            return 3

    bot = MiniBot()
    retry_methods(bot)
    assert bot.send_message(1) == 1
    assert bot.edit_message_text(2) == 2
    assert bot.answer_callback_query(3) == 3
