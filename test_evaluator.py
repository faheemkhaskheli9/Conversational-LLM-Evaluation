import unittest
from evaluator import EndpointContract, Message, evaluate

class EvaluationTests(unittest.TestCase):
    def test_custom_contract(self):
        c = EndpointContract("input", "previous", "profile", ("data", "answer"))
        self.assertEqual(c.build("hi", [Message("user", "hello")], {"tier": "basic"}),
                         {"input": "hi", "previous": [{"role": "user", "content": "hello"}], "profile": {"tier": "basic"}})
        self.assertEqual(c.parse({"data": {"answer": "ok"}}), "ok")

    def test_invalid_response(self):
        with self.assertRaises(ValueError):
            EndpointContract().parse({"response": 1})

    def test_collision(self):
        with self.assertRaises(ValueError):
            EndpointContract("history").build("hi", [], {})

    def test_metrics(self):
        self.assertEqual(evaluate([Message("assistant", "HELLO"), Message("assistant", "")], ("hello", "bye")),
                         {"assistant_turns": 2, "nonempty_ratio": 0.5, "required_term_ratio": 0.5})
        self.assertIsNone(evaluate([])["nonempty_ratio"])

if __name__ == "__main__":
    unittest.main()
