from langchain_core.tools import tool
from langchain_tavily import TavilySearch

@tool
def get_weather(city:str) -> str:
    """查询指定城市的实时天气情况。

    Args:
        city: 城市名称，例如"北京"、"上海"
    """
    # 创建 Tavily 搜索工具（默认自动读取环境变量 TAVILY_API_KEY）
    search = TavilySearch(max_results=3, topic="general")

    try:
        results = search.invoke({"query": f"{city} 今天实时天气预报 气温"})
    except Exception as e:
        return f"错误:调用Tavily搜索时出现问题 - {e}"

    if not results.get("results"):
        return f"未找到关于'{city}'的天气信息，请确认城市名称是否正确"

    # 整理搜索结果为易读的自然语言摘要
    lines = [f"【{city}天气查询结果】"]
    for i, item in enumerate(results["results"], 1):
        title = item.get("title", "")
        content = (item.get("content", "") or "").strip()[:200]
        url = item.get("url", "")
        lines.append(f"\n{i}. {title}")
        if content:
            lines.append(f"   {content}")
        if url:
            lines.append(f"   来源: {url}")

    return "\n".join(lines)