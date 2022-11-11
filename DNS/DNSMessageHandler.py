from DNS.Message.Answer import Answer
from DNS.Message.Header import Header
from DNS.Message.Question import Question
import pickle


class MessageHandler:
    def __init__(self, data):
        self.raw_data = data
        self.data = data.hex()
        self.header = Header(self.data[:24])
        self.question = Question(self.data[24:])

        if self.header.flags[0] == '1':
            self.answer = Answer(self.raw_data, self.data, self.question.offset, self.question.qtype)

    '''def __getstate__(self):
        state = {}
        state["header"] = self.header
        state["question"] = self.question
        state["answer"] = self.answer

        return state

    def __setstate__(self, state):
        self.header = state["header"]
        self.question = state["question"]
        state.answer = state["answer"] '''

# 00028180000100040000000006676f6f676c6503636f6d00001c0001c00c001c00010000012c0010 2a00145040100c0e0000000000000065c00c001c00010000012c00102a00145040100c0e000000000000008bc00c001c00010000012c00102a00145040100c0e0000000000000071c00c001c00010000012c00102a00145040100c0e0000000000000066