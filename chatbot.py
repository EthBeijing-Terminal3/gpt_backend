import openai
import os
import json
from datetime import datetime

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

openai.api_key = os.getenv("OPENAI_API_KEY")

# response_list = openai.Model.list()
# print(response_list)

# messages = []
# 定义文件路径
filename = "history/default.json"
history_global = []
# 如果文件存在，读取文件内容并将其反序列化为Python对象
if os.path.exists(filename):
    with open(filename, "r") as f:
        history_global = json.load(f)
# 如果文件不存在，将messages初始化为空数组
else:
    print("No Default Prompt")
highlight_his = [
        {"role": "user",
         "content": "You need to extract the user's action, parameters and comment.\n The user's action includes: 1. login, 2. token_query, 3. token_transfer, 4. token_show, 5. history_query, 6. token_swap, 7. token_freeze, 8. token_unfreeze, 9. borrow_token, 10. loan_status.\n The comments are your explanation to this action.\n Your answer should follow this format:\n Action:{text}\n Paramenters:{text}\n Comment:{text}."},
         {"role": "assistant",
        "content": "Understood! Just let me know what information you need me to provide in that format."}
    ]


def talk():
    global history_global
    # print("Chat History:")
    # print_history(history_global)

    while True:
        question = input("User: ")

        if question.strip() == "":
            continue

        if question.lower() == "help":
            print("Help List:")
            print(" help : call for help")
            print(" clear : clear chat history")
            print(" quit : exit Terminal3, and save the chat log into history/default.json")
            print(
                " save : save the chat log to typical file, e.g.  `save history/default.json`")
            print(" save now: save the file with current timestamp: history/<timestamp>.json")
            print(
                " load : load typical history `load history/test.json`")
            print(" list : list each history file")
            print(
                " show : show typical history, e.g.  `show history/test.json`")
            print(" del : delete the typical file e.g. `del history/test.json`")
            print(" del all: del every file except `history/default.json`")
            print(" Others: Ask Terminal3")
            print()
            continue

        if question.lower() == "clear":
            history_global = [{"role": "system", "content": "You are a helpful assistant."}]
            print_history(history_global)
            continue

        if question.lower() == "quit":
            # 将数据转换为JSON格式
            json_data = json.dumps(history_global)
            # 将JSON数据写入文件
            with open(filename, "w") as history_file:
                history_file.write(json_data)
            break

        if question.lower() == "save":
            # 将数据转换为JSON格式
            json_data = json.dumps(history_global)
            # 将JSON数据写入文件
            with open(filename, "w") as history_file:
                history_file.write(json_data)
            continue

        if question.lower() == "save now":
            save_file_path = "history/history_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".json"
            # 将数据转换为JSON格式
            json_data = json.dumps(history_global)
            # 将JSON数据写入文件
            with open(save_file_path, "w") as history_file:
                history_file.write(json_data)
            continue

        if question.lower().startswith("save"):
            save_file_path = question[5:]
            if len(save_file_path) == 0:
                print("请指定保存路径")
                continue
            # 将数据转换为JSON格式
            json_data = json.dumps(history_global)
            # 将JSON数据写入文件
            print(save_file_path)
            with open(save_file_path, "w") as history_file:
                history_file.write(json_data)
            continue

        if question.lower() == "load":
            if os.path.exists(filename):
                with open(filename, "r") as history_file:
                    history_global = json.load(history_file)
            # 如果文件不存在，将messages初始化为空数组
            else:
                history_global = [{"role": "system", "content": "You are a helpful assistant."}]
            print_history(history_global)
            continue

        if question.lower().startswith("load"):
            load_file_path = question[5:]
            if len(load_file_path) == 0:
                print("请指定导入文件路径")
                continue
            if os.path.exists(load_file_path):
                with open(load_file_path, "r") as history_file:
                    history_global = json.load(history_file)
            # 如果文件不存在，将messages初始化为空数组
            else:
                print("指定导入文件不存在: " + load_file_path)
            print_history(history_global)
            continue

        if question.lower() == "show":
            print_history(history_global)
            continue

        if question.lower().startswith("show"):
            show_file_path = question[5:]
            if len(show_file_path) == 0:
                print("请指定查看文件路径")
                continue
            if os.path.exists(show_file_path):
                with open(show_file_path, "r") as history_file:
                    history_read = json.load(history_file)
                    print_history(history_read)
            # 如果文件不存在，将messages初始化为空数组
            else:
                print("指定查看文件不存在: " + show_file_path)
            continue

        if question.lower() == "list":
            list_files("history")
            continue

        if question.lower() == "del all":
            for fn in os.listdir("history"):
                if fn != "default.json":
                    del_path = os.path.join("history", fn)
                    os.remove(del_path)
                    print("文件已删除: " + del_path)
            continue

        if question.lower().startswith("del"):
            del_file_path = question[4:].strip()
            if len(del_file_path) == 0:
                print("请指定删除文件路径")
                continue
            if os.path.exists(del_file_path):
                os.remove(del_file_path)
                print("文件已删除: " + del_file_path)
            else:
                print("指定删除文件不存在: " + del_file_path)
            continue

        # 控制记忆长度
        # messages = history_global[-6:]
        messages = history_global
        messages.append({"role": "user", "content": question})
        history_global.append({"role": "user", "content": question})

        # API调用
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            # max_tokens=500,
            temperature=0.1,
            # top_p=0.9,
            # stop=["\n"],
        )

        print()
        # print(response)
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
        print()

        answer = response["choices"][0]["message"]["content"]
        print("Terminal3:\n" + answer)
        history_global.append({"role": "assistant", "content": answer})
        history_global.append(highlight_his[0])
        history_global.append(highlight_his[1])
        print()


def print_history(h):
    for ele in h:
        print(f"[{ele['role']}]:{ele['content']}")
        print()


def list_files(directory):
    files = []
    for fn in os.listdir(directory):
        path = os.path.join(directory, fn)
        print(path)
        if os.path.isfile(path):
            files.append(path)
    return files

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    talk()