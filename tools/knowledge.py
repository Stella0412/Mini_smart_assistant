from langchain_core.tools import tool

@tool
def search_knowledge(query: str) -> str:
    """搜索知识库，根据关键词查询相关知识的说明信息。

    Args:
        query: 要查询的问题或关键词，例如"什么是LangChain"、"介绍一下机器学习"
    """
    knowledge = {
        "LangChain": "LangChain是一个用于开发LLM应用的框架，支持工具、代理、内存管理等功能。",
        "机器学习": "机器学习是AI的子集，让系统能从数据中自动学习和改进。",
    }
    for key, value in knowledge.items():
        if key in query:
            return value
    return f"未找到关于'{query}'的信息"
