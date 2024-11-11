# -*- coding: UTF-8 -*-
import os
from openai import OpenAI


## code io, txt
def read_code(file_path):
    if file_path.endswith('.txt'):
        with open(file_path, 'r') as f:
            code = f.readlines()
        return code
    else:
        raise ValueError('Unsupported file type')


########################################################################################################################
## uml statement generate, gpt api interaction, json
## api request, web severce limis, data analysis
## DASHSCOPE_API_KEY, ali severce free for 30 days  "sk-70551c38004b404e9f1876a26b42b8ba"
file_path = './code2uml/'
input_file = 'resample.txt'
out_file = input_file.split('.')[0] + '.puml'
code = read_code(file_path+input_file)
try:
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models  llama3-8b-instruct
        messages=[
            {'role': 'system', 'content': '问题陈述：你是一个专业的Python代码分析师，给你一段darts库源码，将其转换为PlantUML活动图代码。'
                                          '解决步骤：1.接收输入信息，分析代码片段的逻辑。'
                                          '2.根据分析结果，将其转换为PlantUML活动图代码。'
                                          '3.现在请你输出能直接绘制PlantUML图的内容，不需要代码分析结果和其他任何的额外内容。'},
            {'role': 'user', 'content': f'代码片段：{code}'}
            ]
    )
    print(completion.choices[0].message.content)
    with open(file_path + out_file, 'w') as f:
        # f.write(completion.choices[0].message.content)
        content = completion.choices[0].message.content
        lines = content.split('\n')[1:-1]
        f.write('\n'.join(lines))
except Exception as e:
    print(f"错误信息：{e}")
    print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

## plot view, plantUML api interaction, json
########################################################################################################################

#----------------------------------------------------------------------------------------------------------------------#
# from plantuml import PlantUML
# URL = ('https://www.plantuml.com/plantuml/duml/RL3BIiDG4DtVhyYoNVW32MX_HJ35GgrYupvepKr8XEAZY4bZQ_5XqJIWQDfhzMTcvZP_uQZK'
#        'XJYhmvm7XrDhE-kxpjvMKtm3OM9s0TD0nnaD9CevdUMMC4iteF0U3_ro7A7lON70J_JxU1jYrAF1AoKFbbXPDIdje9g16kckHtT3JCDVTobb6'
#        'NlBo2zjy8vo1aK8XGl5c7aEqljJTYmc7NZB_vIW-9bwEMCwol0uMiOtwaQ5HYvTNclbq-CLzOUWNjQgXhDfjvWwdrI5mMSkFaunJYbnOVwar'
#        'GcbYINiPjisAjYz-T5mg__AsgsDHfq7sjuHDSQyrYS0')
# text = """
# title Authentication Sequence
#
# Alice->Bob: Authentication Request
# note right of Bob: Bob thinks about it
# Bob->Alice: Authentication Response
# commandline"""
#
# # puml = PlantUML(url=URL).processes_file('sample.txt')
# puml = PlantUML(url=URL).processes(text)
# # out = open(path.join(directory, outfile), 'wb')
# # out.write(content)
# # out.close()
# print(f'generate UML image with raw png format: {puml}')
# # print(list(map(lambda filename: {'filename': filename, 'gen_success':
# #     puml.processes_file('D:/PycharmProjects/tools/sample.txt', directory='D:/PycharmProjects/tools')}, 'sample.svg')))
#
#
# import cv2
# image = cv2.imread('sample.png', cv2.IMREAD_UNCHANGED)
#
# # 检查图片是否成功加载
# if image is None:
#     print("无法加载图片")
# else:
#     # 显示图片
#     cv2.imshow('Raw PNG Image', image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#
# # plantuml implementation error: send request format error, received response content analyze error
#----------------------------------------------------------------------------------------------------------------------#