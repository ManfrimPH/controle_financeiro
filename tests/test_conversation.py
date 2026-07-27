import sys
sys.path.insert(0, "/home/manfrim/projetos/controle_financeiro")

from conversation import ConversationManager


def test_create_and_get():
    mgr = ConversationManager(timeout_minutes=30)
    state = mgr.create(12345, "add")
    assert state.handler == "add"
    assert mgr.get(12345) is state


def test_cleanup():
    mgr = ConversationManager()
    mgr.create(12345, "add")
    mgr.cleanup(12345)
    assert mgr.get(12345) is None


def test_is_active():
    mgr = ConversationManager()
    assert not mgr.is_active(12345)
    mgr.create(12345, "add")
    assert mgr.is_active(12345)


def test_touch_updates_activity():
    mgr = ConversationManager()
    state = mgr.create(12345, "add")
    old = state.last_activity
    mgr.touch(12345)
    assert state.last_activity >= old


def test_multiple_users():
    mgr = ConversationManager()
    s1 = mgr.create(1, "add")
    s2 = mgr.create(2, "del")
    assert mgr.get(1) is s1
    assert mgr.get(2) is s2
    mgr.cleanup(1)
    assert mgr.get(1) is None
    assert mgr.get(2) is s2
