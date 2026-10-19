from main import has_relevant_result


class Test_relevant_result:
    def test_has_relevant_result_true(self):
        result = [(None, 0.8)]

        assert has_relevant_result(result) is True

    def test_has_relevant_result_false(self):
        result = [(None, 0.3)]

        assert has_relevant_result(result) is False

    def test_has_relevant_result_none(self):
        result = []

        assert has_relevant_result(result) is False



    #---------------------------------------

