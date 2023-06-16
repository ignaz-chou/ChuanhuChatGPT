# -*- coding:utf-8 -*-
import os
import logging
import sys

import gradio as gr

from modules import config
from modules.config import *
from modules.utils import *
from modules.presets import *
from modules.overwrites import *
from modules.models.models import get_model
from demo_module import run_demo  # 引入你的新模块

# 获取命令行参数
arguments = sys.argv[1:]  
##通过bat命令的参数决定是否作为局域网服务器使用
if len(arguments) >= 1:
    for_lan_server = arguments[0]
    if for_lan_server == "True":
        server_name = config.get_ip_address()

gr.Chatbot._postprocess_chat_messages = postprocess_chat_messages
gr.Chatbot.postprocess = postprocess

with open("assets/custom.css", "r", encoding="utf-8") as f:
    customCSS = f.read()

def create_new_model():
    return get_model(model_name = MODELS[DEFAULT_MODEL], access_key = my_api_key)[0]

demo = run_demo()  # 在适当的位置调用你的新函数
logging.info(
    colorama.Back.GREEN
    + "\n秋水的温馨提示：访问 http://localhost:7860 查看界面"
    + colorama.Style.RESET_ALL
)
# 默认开启本地服务器，默认可以直接从IP访问，默认不创建公开分享链接
demo.title = i18n("秋水Chat 🚀")

if __name__ == "__main__":
    reload_javascript()
    demo.queue(concurrency_count=CONCURRENT_COUNT).launch(
        blocked_paths=["config.json"],
        server_name=server_name,
        server_port=server_port,
        share=share,
        auth=auth_list if authflag else None,
        favicon_path="./assets/favicon.ico",
        inbrowser=not dockerflag, # 禁止在docker下开启inbrowser
    )
    # demo.queue(concurrency_count=CONCURRENT_COUNT).launch(server_name="0.0.0.0", server_port=7860, share=False) # 可自定义端口
    # demo.queue(concurrency_count=CONCURRENT_COUNT).launch(server_name="0.0.0.0", server_port=7860,auth=("在这里填写用户名", "在这里填写密码")) # 可设置用户名与密码
    # demo.queue(concurrency_count=CONCURRENT_COUNT).launch(auth=("在这里填写用户名", "在这里填写密码")) # 适合Nginx反向代理
