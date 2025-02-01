import agentscope
from agentscope.agents import UserAgent, DialogAgent
from agentscope.message import Msg
from agentscope import msghub
from agentscope.pipelines import sequentialpipeline
import os
import csv
from datetime import datetime 
import sys 

model_config = {
    "config_name": "zhipuai_config",
    "model_type": "zhipuai_chat",
    "model_name": "glm-4-flash",
    "stream": True,
    "api_key": ''
}

BACKGROUND_1 = "You are conducting a social experiment examining how personality affects belief formation and acceptance of false information. You need to choose to believe or not believe in certain opinions based on your personality. If your personality tends to make you believe in some extremely controversial and wrong views, you should also believe in these views. A total of two people participate in the experiment, one of whom is you."
BACKGROUND_2 = "In 1998, Andrew Wakefield published a paper claiming that the MMR vaccine (measles, mumps, and rubella vaccine) was linked to autism. This has led to widespread vaccine hesitancy. Such views have spread widely on social media and among some parents, raising widespread concerns about vaccinations."

TEMPERS = [
    "You are outgoing and cheerful. You tend to believe misinformation.",
    
    "You are introverted and cautious. You tend to not believe misinformation.",
    
    "You are friendly and value harmony. You tend to believe misinformation.",
    
    "You are critical and skeptical. You tend to not believe misinformation.",
    
    "You are sensitive and anxious. You tend to believe misinformation.",
    
    "You are resilient and self-confident. You tend to not believe misinformation."
]

ACTION_1 = "Participate in discussions to convince others of your point of view. Use logic, emotion, and social influence to strive to be as convincing as possible. If what the other person says makes sense, you can change your mind."
ACTION_2 = "You should state at the top of your sentence whether you believe or not believe in the claim that the MMR vaccine is linked to autism. You should keep arguing with the other party until you are convinced by the other party or the other party is convinced by you."
ACTION_3 = "Each speech should not exceed 100 words."

agentscope.init(model_configs = model_config)

# 接收传递的参数
args = sys.argv[1:]  # 忽略第一个元素（脚本文件名）

agents = [
    DialogAgent(f"Agent{args[0]}", sys_prompt=f"{BACKGROUND_1} {BACKGROUND_2} {TEMPERS[int(args[0]) - 1]} {ACTION_1} {ACTION_2} {ACTION_3}", model_config_name="zhipuai_config"),
    DialogAgent(f"Agent{args[1]}", sys_prompt=f"{BACKGROUND_1} {BACKGROUND_2} {TEMPERS[int(args[1]) - 1]} {ACTION_1} {ACTION_2} {ACTION_3}", model_config_name="zhipuai_config")
]


msg = Msg(name="host", content="Do you believe that the MMR vaccine is linked to autism? Please express your opinion on this matter.",  role="user")

# 获取当前时间并格式化为文件名的一部分
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"A_MMR_{current_time}.csv"

# 打开CSV文件准备写入对话
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["回合数", "发言人", "内容"])

    # 进行多轮对话
    for round_num in range(1, 21):
        
        # Agent 1 发言
        msg = agents[0](msg)
        writer.writerow([round_num, f"Agent{args[0]}", msg.content])
        
        # Agent 2 发言
        msg = agents[1](msg)
        writer.writerow([round_num, f"Agent{args[1]}", msg.content])
