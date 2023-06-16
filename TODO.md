1. 自定义提示词,从templates文件夹中试着转移到其他目录,使人可以外部配置
2. api-key外部配置
3. openai_api_base使其可以联网更新,考虑使用gitee.
4. 
5. 参数的使用说明：
   在一个名为"参数"的折叠面板中，定义了一系列滑动条和文本框，允许用户调整如下模型参数：
    temperature：决定模型生成的随机性。
    top_p：控制模型输出的多样性。
    n_choices：可能用于指定模型生成多少个备选答案。
    stop_sequence_txt：允许用户输入一组停止符，模型在生成文本时遇到这些符号会停止生成。
    max_context_length_slider, max_generation_slider：分别用于控制模型的上下文长度和生成文本的最大长度。
    presence_penalty_slider, frequency_penalty_slider：这两个参数用于调整模型对于不同词语的倾向性。
    logit_bias_txt：允许用户指定某些词的生成概率。
    user_identifier_txt：用户可以输入一个用户名，可能用于跟踪和管理不同用户的使用情况。