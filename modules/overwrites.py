from __future__ import annotations
import logging

from typing import List, Tuple
import mdtex2html
from gradio_client import utils as client_utils

from modules.presets import *
from modules.index_func import *
from modules.config import render_latex

# postprocess函数是用来处理聊天机器人的输出的。它接收一个参数y，这个参数是一个包含机器人和用户之间的对话信息的列表。
# 这个函数的主要作用是对这个对话信息进行处理，处理完成后的信息包含HTML格式的字符串或包含媒体信息的字典。
def postprocess(
        self,
        y: List[List[str | Tuple[str] | Tuple[str, str] | None] | Tuple],
    ) -> List[List[str | Dict | None]]:
        """
        Parameters:
            y: List of lists representing the message and response pairs. Each message and response should be a string, which may be in Markdown format.  It can also be a tuple whose first element is a string filepath or URL to an image/video/audio, and second (optional) element is the alt text, in which case the media file is displayed. It can also be None, in which case that message is not displayed.
        Returns:
            List of lists representing the message and response. Each message and response will be a string of HTML, or a dictionary with media information. Or None if the message is not to be displayed.
        """
        if y is None:
            return []
        processed_messages = []
        for message_pair in y:
            assert isinstance(
                message_pair, (tuple, list)
            ), f"Expected a list of lists or list of tuples. Received: {message_pair}"
            assert (
                len(message_pair) == 2
            ), f"Expected a list of lists of length 2 or list of tuples of length 2. Received: {message_pair}"

            processed_messages.append(
                [
                    self._postprocess_chat_messages(message_pair[0], "user"),
                    self._postprocess_chat_messages(message_pair[1], "bot"),
                ]
            )
        return processed_messages


# postprocess_chat_messages函数是postprocess函数的辅助函数，它专门处理一条聊天信息。这个函数会检查聊天信息的类型，并根据类型进行相应的处理。
# 如果聊天信息是一个媒体文件的路径，那么它会把这个路径转换成一个包含文件名、MIME类型、备选文本和其他信息的字典。
# 如果聊天信息是一个字符串，那么它会把这个字符串转换成HTML格式。否则，它会抛出一个错误。
def postprocess_chat_messages(
        self, chat_message: str | Tuple | List | None, message_type: str
    ) -> str | Dict | None:
        if chat_message is None:
            return None
        elif isinstance(chat_message, (tuple, list)):
            filepath = chat_message[0]
            mime_type = client_utils.get_mimetype(filepath)
            filepath = self.make_temp_copy_if_needed(filepath)
            return {
                "name": filepath,
                "mime_type": mime_type,
                "alt_text": chat_message[1] if len(chat_message) > 1 else None,
                "data": None,  # These last two fields are filled in by the frontend
                "is_file": True,
            }
        elif isinstance(chat_message, str):
            if message_type == "bot":
                if not detect_converted_mark(chat_message):
                    chat_message = convert_mdtext(chat_message)
            elif message_type == "user":
                if not detect_converted_mark(chat_message):
                    chat_message = convert_asis(chat_message)
            return chat_message
        else:
            raise ValueError(f"Invalid message for Chatbot component: {chat_message}")

with open("./assets/custom.js", "r", encoding="utf-8") as f, \
    open("./assets/external-scripts.js", "r", encoding="utf-8") as f1:
    customJS = f.read()
    externalScripts = f1.read()


# reload_javascript函数是用来重新加载JavaScript代码的。这个函数首先会把customJS和externalScripts两个变量的内容拼接成一个HTML <script>标签。
# 然后，如果配置了需要渲染LaTeX公式，那么它还会添加MathJax库的代码。
# 最后，它会重写Gradio库的TemplateResponse类，把这些JavaScript代码插入到返回的HTML页面中。
# 这样，每当返回一个新的页面时，这些JavaScript代码都会被重新加载。
def reload_javascript():
    print("Reloading javascript...")
    js = f'<script>{customJS}</script><script async>{externalScripts}</script>'
    if render_latex:
        js += """\
            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML"></script>
            <script type="text/x-mathjax-config">MathJax.Hub.Config({skipStartupTypeset: false, tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']],displayMath: [['$$','$$'], ['\\[','\\]']]}});</script>
        """
    def template_response(*args, **kwargs):
        res = GradioTemplateResponseOriginal(*args, **kwargs)
        res.body = res.body.replace(b'</html>', f'{js}</html>'.encode("utf8"))
        res.init_headers()
        return res

    gr.routes.templates.TemplateResponse = template_response

GradioTemplateResponseOriginal = gr.routes.templates.TemplateResponse