import os

import openai
import gradio as gr

openai.api_key = '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'
#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

def clean_textbox(*args):
    n = len(args)
    return [""] * n


class ChatGPT:
    def __init__(self):
        self.messages = [{'role': 'system', 'content': "You are now a very useful maid assistant! If you have a question you can't answer, please reply with As a classy girl, I can't answer this question"}]

    def reset(self, *args):
        self.messages = [{'role': 'system', 'content': "You are now a very useful maid assistant! If you have a question you can't answer, please reply with As a classy girl, I can't answer this question"}]
        return clean_textbox(*args)

    def chat(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages,
            temperature=0.7
        )
        res_msg = completion.choices[0].message["content"].strip()
        self.messages.append({"role": "assistant", "content": res_msg})
        return res_msg


if __name__ == '__main__':
    my_chatgpt = ChatGPT()
    with gr.Blocks(title="ChatGPT") as demo:
        gr.Markdown('''
        # ChatGPT
                ''')
        with gr.Row():
            with gr.Column(scale=9):
                prompt = gr.Text(label='ChatGPT_Prompt', show_label=False, lines=3,
                                 placeholder='ChatGPT Prompt')
                res = gr.Text(label='ChatGPT_result', show_label=False, lines=3,
                              placeholder='chatgpt results')

            with gr.Column(scale=1):
                btn_gen = gr.Button(value="send", variant='primary')
                btn_clear = gr.Button(value="restart chat")

        gr.Examples([
            ["How to Become a My channel Grow more Pyresearch youtube channel"],
            ["Suppose there is a pond with an infinite amount of water in it. There are currently 2 empty jugs with volumes of 5 liters and 6 liters respectively. The problem is how to get 3 liters of water from the pond with only these 2 jugs."],
            ["Please help me with C++Write quick sort code."]],
            inputs=[prompt],
            outputs=[res],
            fn=my_chatgpt.chat,
            cache_examples=False)

        btn_gen.click(fn=my_chatgpt.chat, inputs=prompt,
                      outputs=res)
        btn_clear.click(fn=my_chatgpt.reset,
                        inputs=[prompt, res],
                        outputs=[prompt, res])

    demo.queue()
    demo.launch()
