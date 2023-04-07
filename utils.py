import openai
import os
import json
from datetime import datetime


class Terminal3(object):
    def __init__(self, OPENAI_API_KEY='',
                 wallet_address='0x2Cb9F791d68ea5bDc8Aab1aAEA61ED84D876e67F',
                 model_selection='default',
                 verbose=False):
        if OPENAI_API_KEY == '':
            openai.api_key = os.getenv("OPENAI_API_KEY")
        else:
            openai.api_key = OPENAI_API_KEY

        self.default_prompt_root = "fine-tune/default.json"
        self.test_prompt_path = "fine-tune/test.json"
        # self.wallet_address = wallet_address
        self.model_selection = model_selection

        if self.model_selection == 'default':
            his_path = self.default_prompt_root
        elif self.model_selection == 'test':
            his_path = self.test_prompt_path
        else:
            his_path = ''
        self.his_path = his_path

        self.verbose = verbose
        self.history = self.load_history()
        # self.init_chatgpt(wallet_address)

    def load_history(self):
        if os.path.exists(self.his_path):
            with open(self.his_path, "r") as f:
                history = json.load(f)
                return history
        else:
            raise FileNotFoundError()

    def init_chatgpt(self, wallet_address):  # TODO: Add Parallel Support
        self.history = self.load_history()

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

        print("Init Done.")
        answer = self.start_chat(wallet_address, "Hello")

        return answer

    def start_chat(self, wallet_addr, question):
        if self.verbose:
            print(wallet_addr)
            print(question)

        if question.lower() == "save":
            json_data = json.dumps(self.history)
            with open(self.his_path, "w") as history_file:
                history_file.write(json_data)
                return ({"Action": "Save History"})

        self.history.append({"role": "user", "content": question})

        # TODO: ADD Multi-Wallet Support
        # wallet_addr = wallet_addr
        # customized_addr = 'fine-tune/%s' % wallet_addr

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

        if self.verbose:
            print("Terminal3:\n" + answer)

        if int(response_total_tokens) > 4000:
            self.history = self.history[:10] + self.history[-100:]  # Cut Length

        self.history.append({"role": "assistant", "content": answer})

        return answer
