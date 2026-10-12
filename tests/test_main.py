from main import has_relevant_result

def test_has_relevant_result_true():
    result = [(None, 0.8)]

    assert has_relevant_result(result) is True

def test_has_relevant_result_false():
    result = [(None, 0.3)]

    assert has_relevant_result(result) is False

def test_has_relevant_result_none():
    result = []

    assert has_relevant_result(result) is False



