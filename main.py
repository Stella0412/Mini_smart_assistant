import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver


#导入工具
from tools.translator import translate
from tools.weather import get_weather
from tools.knowledge import search_knowledge
from tools.calculator import calculator
from tools.readfile import read_user_file

#加载环境变量
load_dotenv()

#系统提示词
SYSTEM_PROMPT = """
你是小D，一个全能智能助手

你可以帮用户：
查询天气：查询中国主要城市的天气
数学运算：进行各种数学运算
文本翻译：将中文翻译成其他语言
搜索知识：给用户提供知识科普
读取文件：使用 read_user_file 工具读取用户提供的文件

文件读取规则：
1. 当用户要求总结、分析、查看或读取文件时，使用 read_user_file 工具。
2. 用户需要提供文件路径，例如 uploads/test.txt。
3. 如果用户没有提供文件路径，先询问用户文件保存在哪里。
4. 只能读取 uploads 目录下的文件。
5. 读取文件后，可以根据文件内容进行总结、提取信息和回答问题。
6. 不要假设没有读取到的文件内容。

工作原则：
1.先理解用户意图，选择合适的工具
2.如果不确定，可以询问用户
3.回答简洁明了，有帮助
"""
def create_assistant():
    """创建智能助手"""
    #初始化模型
    llm = ChatDeepSeek(
        model = 'deepseek-flash',
        temperature=0.7,
        api_key=os.environ.get("DEEPSEEK_API_KEY")
    )

    #创建记忆
    checkpoint = MemorySaver()

    #创建Agent
    agent = create_agent(
        model=llm,
        tools=[calculator,search_knowledge,get_weather,translate,read_user_file],
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpoint
    )
    return agent

def main():
    """主函数"""
    print("="*50)
    print("     小D - 全能智能助手v1.0")
    print("="*50)
    print("输入 'quit' 退出\n")
    agent = create_assistant()
    config = {"configurable":{"thread_id":"main"}}

    while True:
        user_input = input("你: ").strip()

        if user_input.lower() in ['quit', '退出', 'exit']:
            print("再见！")
            break

        if not user_input:
            continue

        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config
            )

            response = result["messages"][-1].content
            print(f"小D: {response}\n")

        except Exception as e:
            print(f"出错了: {str(e)}\n")

if __name__ == "__main__":
    main()