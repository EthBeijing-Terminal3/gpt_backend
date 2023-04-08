import openai
import os
import json
from datetime import datetime


class Terminal3(object):
    def __init__(self, OPENAI_API_KEY='',
                 wallet_address='',
                 verbose=False):
        if OPENAI_API_KEY == '':
            openai.api_key = os.getenv("OPENAI_API_KEY")
        else:
            openai.api_key = OPENAI_API_KEY

        self.wallet_address = wallet_address
        self.default_path = "fine-tune/default.json"

        self.verbose = verbose
        self.history = self.load_history(mode='test')
        # self.init_chatgpt(wallet_address)

    def load_json(self, path):
        with open(path, "r") as f:
            history = json.load(f)
        self.history = history

    def load_history(self, mode='user'):
        path = "fine-tune/user/%s.json" % self.wallet_address
        if mode == 'default':
            self.load_json("fine-tune/default.json")
        elif mode == 'test':
            self.load_json("fine-tune/test.json")
        else:
            try:
                self.load_json(path)
            except:
                self.load_json("fine-tune/default.json")

    def init_chatgpt(self, wallet_address):  # TODO: Add Parallel Support
        self.wallet_address = wallet_address
        self.load_history(mode='test')
        # self.history.append(
        #     {
        #         "role": "system",
        #         "content": "My web3 ethernum wallet address is %s." % wallet_address,
        #     }
        # )
        # self.history.append(
        #     {
        #         "role": "system",
        #         "content": "Every response of your answer should strictly follow the json format: {\"Action\":{text}, "
        #                    "\"Parameters\":{text}, \"Comment\":{text}}. DO NOT output any extra words.",
        #     }
        # )
        answer = self.start_chat(wallet_address, "Hello, tell me about you.")

        return answer

    def start_chat(self, wallet_addr, question):
        self.wallet_address = wallet_addr
        if self.verbose:
            print(wallet_addr)
            print(question)

        if question.lower().strip() == "save" or question.lower().strip() == "save\n":
            json_data = json.dumps(self.history)
            with open("fine-tune/user/%s.json" % wallet_addr, "w") as history_file:
                history_file.write(json_data)
            return ({"Action": "save_history",
                         "Parameters": "none",
                         "Comment": "Save your chat history"
                         })

        if question.lower().strip() == "load" or question.lower().strip() == "load\n":
            self.load_history(mode='user')
            return ({"Action": "load_history",
                         "Parameters": "none",
                         "Comment": "Load your chat history"
                         })

        if question.lower().strip() == "load default" or question.lower().strip() == "load default\n":
            self.load_history(mode='test')
            return ({"Action": "load_history",
                         "Parameters": "none",
                         "Comment": "Load your chat history"
                         })

        if question.lower().strip() == "init" or question.lower().strip() == "init\n":
            self.load_history(mode='test')
            self.init_chatgpt(wallet_addr)

        elif question.lower().strip() == "history" or question.lower().strip() == "history\n":
            list = self.history[3:]
            print(self.history)
            _tmp = []
            for li in list:
                if li["role"] == "user":
                    _tmp.append(li)

            return ({"Action": "show_history",
                     "Parameters": _tmp,
                     "Comment": "Your chat history is list as follows:"
                     })

        self.history.append({"role": "user", "content": question})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.history,
            # max_tokens=4096,
            # temperature=0.1,
            # top_p=0.9,
            # stop=["\n"],
        )
        response_id = response["id"]
        response_prompt_tokens = response["usage"]["prompt_tokens"]
        response_completion_tokens = response["usage"]["completion_tokens"]
        response_total_tokens = response["usage"]["total_tokens"]

        if self.verbose:
            print(f"CHAT id:{response_id}, Input TOKENS: {response_prompt_tokens}, ",
                  f"Output TOKENS: {response_completion_tokens}, ",
                  f"All TOKENS: {response_total_tokens}")

        answer = response["choices"][0]["message"]["content"]

        if not answer.startswith('{') or not answer.endswith('}'):
            print("="*20)
            print(answer)
            self.load_history(mode='test')
            answer = self.start_chat(wallet_addr, question)

        if self.verbose:
            print("Terminal3:\n" + answer)

        if int(response_total_tokens) > 4000:
            self.history = self.history[:10] + self.history[-100:]  # Cut Length

        self.history.append({"role": "assistant", "content": answer})

        return answer
