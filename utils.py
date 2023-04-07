import openai
import os
import json
from datetime import datetime

class Terminal3(object):
    def __init__(self, OPENAI_API_KEY='', model_selection='default', verbose=False):
        if OPENAI_API_KEY == '':
            openai.api_key = os.getenv("OPENAI_API_KEY")
        else:
            openai.api_key = OPENAI_API_KEY

        self.default_prompt_root = "fine-tune/default.json"
        self.test_prompt_path = "fine-tune/test.json"
        self.model_selection = model_selection
        self.verbose = verbose
        self.history = self.load_history()
        self.init_chatgpt()

    def load_history(self):
        if self.model_selection == 'default':
            his_path = self.default_prompt_root
        elif self.model_selection == 'test':
            his_path = self.test_prompt_path
        else:
            his_path = ""

        if os.path.exists(his_path):
            with open(his_path, "r") as f:
                history = json.load(f)
                return history
        else:
            raise FileNotFoundError()

    def init_chatgpt(self):
        verbose = self.verbose
        verbose = True
        self.history.append({"role": "user", "content": "Reply Ready when you are ready"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            # max_tokens=500,
            temperature=0.1,
            # top_p=0.9,
            # stop=["\n"],
        )

        if verbose:
            response_id = response["id"]
            response_prompt_tokens = response["usage"]["prompt_tokens"]
            response_completion_tokens = response["usage"]["completion_tokens"]
            response_total_tokens = response["usage"]["total_tokens"]

            print(f"CHAT id:{response_id}, Input TOKENS: {response_prompt_tokens}, ",
                  f"Output TOKENS: {response_completion_tokens}, ",
                  f"All TOKENS: {response_total_tokens}")

        answer = response["choices"][0]["message"]["content"]

        if verbose:
            print("Terminal3:\n" + answer)
        self.history.append({"role": "assistant", "content": answer})

        return answer

    def start_new_chat(self, wallet_addr, question):
        if self.verbose:
            print(wallet_addr)
            print(question)

        self.history.append({"role": "user", "content": question})
        wallet_addr = wallet_addr
        customized_addr = 'fine-tune/%s' % wallet_addr

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            # max_tokens=500,
            temperature=0.1,
            # top_p=0.9,
            # stop=["\n"],
        )

        response_id = response["id"]
        # print("response_id: " + response_id)
        response_prompt_tokens = response["usage"]["prompt_tokens"]
        # print(f"response_prompt_tokens: {response_prompt_tokens}")
        response_completion_tokens = response["usage"]["completion_tokens"]
        # print(f"response_completion_tokens: {response_completion_tokens}")
        response_total_tokens = response["usage"]["total_tokens"]
        # print(f"response_total_tokens: {response_total_tokens}")

        print(f"CHAT id:{response_id}, Input TOKENS: {response_prompt_tokens}, ",
              f"Output TOKENS: {response_completion_tokens}, ",
              f"All TOKENS: {response_total_tokens}")
        answer = response["choices"][0]["message"]["content"]
        print("Terminal3:\n" + answer)
        self.history.append({"role": "assistant", "content": answer})

        return answer


    def save_history(self):
        pass

    def parse_answer(self, answer):
        pass
