from main import has_relevant_result
from main import exit_question


class Test_relevant_result:
    def test_has_relevant_result_true():
        result = [(None, 0.8)]

        assert has_relevant_result(result) is True

    def test_has_relevant_result_false():
        result = [(None, 0.3)]

        assert has_relevant_result(result) is False

    def test_has_relevant_result_none():
        result = []

        assert has_relevant_result(result) is False



    #---------------------------------------

class Test_exit_question:
    def test_exit_question_true():
        result = "exit"

        assert exit_question(result) is True  

    def test_exit_question_false():
        result = "go out"

        assert exit_question (result) is False

    def test_exit_question_none():
        result = ""

        assert exit_question(result) is False


