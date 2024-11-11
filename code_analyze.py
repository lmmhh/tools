# -*- coding: UTF-8 -*-

import os
from openai import OpenAI

INPUT_DIR = 'D:/Python311/Lib/site-packages/darts/models/forecasting/'
OUTPUT_DIR = './code2uml/'
API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# input_file = 'resample.txt'
# out_file = input_file.split('.')[0] + '.puml'
# code = read_code(file_path+input_file)
# 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models  llama3-8b-instruct


def read_code(file_path):
    if file_path.endswith('.py'):
        with open(file_path, 'r') as f:
            code = f.readlines()
        return code
    else:
        raise ValueError('Unsupported file type')


class CodeAnalyze:
    def __init__(self, file):
        self.file_name = file
        self.file_path = INPUT_DIR + file

    def code2uml(self):
        if os.path.exists(self.file_path):
            code = read_code(self.file_path)
        out_file = OUTPUT_DIR + os.path.splitext(self.file_name)[1] + '.puml'
        try:
            client = OpenAI(
                api_key=API_KEY,
                base_url=BASE_URL,
            )

            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {'role': 'system', 'content': '问题陈述：你是一个专业的Python代码分析师，给你一段darts库源码，将其转换为PlantUML活动图代码。'
                                                  '解决步骤：1.接收输入信息，分析代码片段的逻辑。'
                                                  '2.根据分析结果，将其转换为PlantUML活动图代码。'
                                                  '3.现在请你输出能直接绘制PlantUML图的内容，不需要代码分析结果和其他任何的额外内容。'},
                    {'role': 'user', 'content': f'代码片段：{code}'}
                    ]
            )
            # print(completion.choices[0].message.content) # check + content error process
            with open(out_file, 'w') as f:
                content = completion.choices[0].message.content
                lines = content.split('\n')[1:-1]
                f.write('\n'.join(lines))
        except Exception as e:
            print(f"错误信息：{e}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

    def model2parm(self):
        if os.path.exists(self.file_path):
            code = read_code(self.file_path)
        # out_file = OUTPUT_DIR + os.path.splitext(self.file_name)[1] + '.puml'
        try:
            client = OpenAI(
                api_key=API_KEY,
                base_url=BASE_URL,
            )

            completion = client.chat.completions.create(
                model="qwen-plus",
                messages=[
                    {'role': 'system', 'content': '问题陈述：你是一个专业的Python代码分析师，给你一段darts库的预测模型实现源码，'
                                                  '分析预测模型函数的输入参数设置方式、给出必要参数范围及使用示例。'
                                                  '步骤：1.分析模型实现的逻辑。2.根据分析结果，列举所有参数。3.输出必要参数范围及使用示例。'
                                                  '注意：分别以list形式对应输出参数、示例、取值范围，并通过参数使用示例说明模型实现逻辑，不包含其他任何的额外内容。'},
                    {'role': 'user', 'content': f'代码片段：{code}'}
                    ]
            )
            print(completion.choices[0].message.content)  # check + content error process, output to config file
            # with open(out_file, 'w') as f:
            #     content = completion.choices[0].message.content
            #     lines = content.split('\n')[1:-1]
            #     f.write('\n'.join(lines))
        except Exception as e:
            print(f"错误信息：{e}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


if __name__ == '__main__':
    model = 'arima.py'
    code = CodeAnalyze(model)
    code.model2parm()
