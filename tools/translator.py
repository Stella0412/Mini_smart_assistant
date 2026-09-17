from langchain_core.tools import tool
from deep_translator import GoogleTranslator

# 语言名称 -> Google Translator 语言代码
LANG_MAP = {
    "英文": "en", "英语": "en",
    "日文": "ja", "日语": "ja",
    "韩文": "ko", "韩语": "ko",
    "法文": "fr", "法语": "fr",
    "德文": "de", "德语": "de",
    "西班牙文": "es", "西班牙语": "es",
    "俄文": "ru", "俄语": "ru",
    "中文": "zh-CN",
}


@tool
def translate(text: str, target_language: str = "英文") -> str:
    """将中文文本翻译成目标语言（使用在线翻译引擎，支持任意文本）。

    Args:
        text: 要翻译的中文文本
        target_language: 目标语言，如：英文、日文、韩文、法文、德文、西班牙文、俄文
    """
    lang_code = LANG_MAP.get(target_language.strip())
    if lang_code is None:
        return f"不支持目标语言'{target_language}'，当前支持：英文、日文、韩文、法文、德文、西班牙文、俄文"

    try:
        result = GoogleTranslator(source="zh-CN", target=lang_code).translate(text)
        return f"翻译结果：'{text}' -> [{target_language}] {result}"
    except Exception as e:
        return f"翻译失败：{e}"
