from pypbbot.utils import Clips


def test_clips_add() -> None:
    a = Clips.fromStr('aA')
    b = Clips.fromStr('bB')
    assert str(a + b) == 'aAbB'
    assert str(123 + b) == '123bB'
    assert str(b + 0.0) == 'bB0.0'
    assert str('str' + a) == 'straA'
