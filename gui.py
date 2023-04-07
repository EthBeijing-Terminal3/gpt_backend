from tkinter import *
import random

import openai

# import api_key
openai.api_key = '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'


class api_key:
    def toChat2(self):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self}
            ]
        )
        print(completion.choices[0].message)
        return completion.choices[0].message


class ChatBot:
    def __init__(self, master):
        self.master = master
        master.title("Chat Bot")
        # master.iconbitmap('bot.ico')
        master.geometry('400x450')
        master.resizable(width=False, height=False)

        # Create widgets
        self.chatlog = Text(master, bd=0, bg="#f2f2f2", height="8", width="50", font=("Arial", 11), )
        self.chatlog.config(state=DISABLED)

        self.scrollbar = Scrollbar(master, command=self.chatlog.yview, cursor="heart", bg="#ccc")
        self.chatlog['yscrollcommand'] = self.scrollbar.set

        self.entrybox = Entry(master, bd=0, bg="white", width="37", font=("Arial", 12))
        self.entrybox.bind("<Return>", self.enter_pressed)

        self.send_button = Button(master, text="Send", width="12", height=2, bd=0, bg="#4CAF50",
                                  activebackground="#3e8e41", font=("Arial", 12), command=self.clicked)

        # Set layout
        self.chatlog.place(x=10, y=50, height=340, width=380)
        self.scrollbar.place(x=386, y=50, height=340)
        self.entrybox.place(x=10, y=410, height=30, width=320)
        self.send_button.place(x=335, y=410, height=30, width=50)

        # Initialize conversation
        self.init_conversation()

    def init_conversation(self):
        messages = ["你好呀，我在这儿!", "我是智能机器人，我能帮你做什么呢?"]
        for message in messages:
            self.chatbot_response(message)

    def enter_pressed(self, event):
        self.clicked()

    def clicked(self):
        user_input = self.entrybox.get()
        if (user_input != ""):
            self.chatlog.config(state=NORMAL)
            self.chatlog.insert(END, "You: " + user_input + "\n\n")
            self.chatlog.config(foreground="#333", font=("Arial", 11))

            response = self.generate_response(user_input)
            print(response.content)
            self.chatbot_response(response.content.strip())

    def generate_response(self, user_input):
        if user_input != "":
            responses = api_key.toChat2(user_input)
            return responses
        else:
            return

    def chatbot_response(self, response):
        self.chatlog.config(state=NORMAL)
        self.chatlog.insert(END, "AI >>> " + response + "\n\n")
        self.chatlog.config(foreground="#442265", font=("Arial", 11))
        self.entrybox.delete(0, END)
        self.chatlog.config(state=DISABLED)
        self.chatlog.yview(END)

root = Tk()
bot = ChatBot(root)
root.mainloop()