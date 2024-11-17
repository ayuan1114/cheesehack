import random

class CodedSet:
    def __init__(self):
        self.dig_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.user_dict = {}

    def add_new_entry(self, user):
        new_code = self.gen_code()
        self.user_dict[user] = new_code
        return new_code

    def gen_code(self):
        dig_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        code_str = ""
        for i in range(19):
            if i % 5 == 4:
                code_str += "-"
            else:
                code_str += random.choice(dig_str)
        if code_str in self.user_dict.keys():
            return self.gen_code()
        return code_str

    def get_code(self, user):
        return self.user_dict[user]
    
    def is_valid(self, token):
        return token in self.user_dict.values()

def gen_code():
    dig_str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    code_str = ""
    for i in range(19):
        if i % 5 == 4:
            code_str += "-"
        else:
            code_str += random.choice(dig_str)
    return code_str