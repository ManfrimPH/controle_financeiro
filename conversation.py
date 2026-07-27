from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Optional


@dataclass
class ConversationState:
    handler: str
    data: dict = field(default_factory=dict)
    last_activity: datetime = field(default_factory=datetime.now)


class ConversationManager:
    def __init__(self, timeout_minutes: int = 30):
        self._states: dict[int, ConversationState] = {}
        self.timeout = timedelta(minutes=timeout_minutes)

    def get(self, chat_id: int) -> Optional[ConversationState]:
        state = self._states.get(chat_id)
        if state is None:
            return None
        if datetime.now() - state.last_activity > self.timeout:
            del self._states[chat_id]
            return None
        return state

    def create(self, chat_id: int, handler: str) -> ConversationState:
        state = ConversationState(handler=handler)
        self._states[chat_id] = state
        return state

    def touch(self, chat_id: int):
        state = self._states.get(chat_id)
        if state:
            state.last_activity = datetime.now()

    def cleanup(self, chat_id: int):
        self._states.pop(chat_id, None)

    def is_active(self, chat_id: int) -> bool:
        return self.get(chat_id) is not None
# Default shared instance
conv_manager = ConversationManager()
