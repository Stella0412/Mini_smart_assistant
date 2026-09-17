from pathlib import Path
import json

from langchain_core.tools import tool


# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 只允许读取 uploads 目录中的文件
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@tool
def read_user_file(file_path: str) -> str:
    """读取用户上传的文件内容。

    支持的文件类型包括：
    txt、md、csv、json、pdf、docx。

    文件必须位于项目的 uploads 目录中。

    Args:
        file_path: 用户上传文件的路径，例如 uploads/test.txt
    """
    try:
        file_path = file_path.strip()

        if not file_path:
            return "错误：文件路径不能为空"

        # 将用户输入的路径转换为绝对路径
        path = Path(file_path)

        if not path.is_absolute():
            path = BASE_DIR / path

        # 解析真实路径，防止 ../ 越权读取其他目录
        path = path.resolve()
        upload_dir = UPLOAD_DIR.resolve()

        try:
            path.relative_to(upload_dir)
        except ValueError:
            return "错误：为了安全，只允许读取 uploads 目录中的文件"

        # 检查文件是否存在
        if not path.exists():
            return f"错误：找不到文件：{file_path}"

        # 检查是否是普通文件
        if not path.is_file():
            return f"错误：'{file_path}' 不是一个普通文件"

        # 限制文件大小，例如最大 10 MB
        max_size = 10 * 1024 * 1024

        if path.stat().st_size > max_size:
            return "错误：文件太大，暂时只支持 10 MB 以内的文件"

        suffix = path.suffix.lower()

        # 读取文本类文件
        if suffix in [".txt", ".md", ".csv"]:
            return read_text_file(path)

        # 读取 JSON 文件
        if suffix == ".json":
            return read_json_file(path)

        # 读取 PDF 文件
        if suffix == ".pdf":
            return read_pdf_file(path)

        # 读取 Word 文件
        if suffix == ".docx":
            return read_docx_file(path)

        return (
            f"错误：暂不支持'{suffix}'文件类型。"
            "目前支持：txt、md、csv、json、pdf、docx"
        )

    except Exception as e:
        return f"读取文件时发生错误：{type(e).__name__}: {e}"


def read_text_file(path: Path) -> str:
    """读取文本文件，兼容常见编码。"""
    encodings = ["utf-8", "utf-8-sig", "gbk"]

    for encoding in encodings:
        try:
            content = path.read_text(encoding=encoding)
            return format_result(path, content)
        except UnicodeDecodeError:
            continue

    return "错误：无法识别该文本文件的编码格式"


def read_json_file(path: Path) -> str:
    """读取 JSON 文件并格式化输出。"""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        content = json.dumps(data, ensure_ascii=False, indent=2)
        return format_result(path, content)

    except json.JSONDecodeError as e:
        return f"错误：JSON 文件格式不正确：{e}"


def read_pdf_file(path: Path) -> str:
    """读取 PDF 文件内容。"""
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(f"\n--- 第 {page_number} 页 ---\n{text}")

        content = "".join(pages).strip()

        if not content:
            return "PDF 文件中没有提取到文本，可能是扫描版图片 PDF"

        return format_result(path, content)

    except ImportError:
        return "错误：读取 PDF 需要安装 pypdf：pip install pypdf"


def read_docx_file(path: Path) -> str:
    """读取 Word 文档内容。"""
    try:
        from docx import Document

        document = Document(str(path))
        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        content = "\n".join(paragraphs)

        if not content:
            return "Word 文件中没有读取到文本内容"

        return format_result(path, content)

    except ImportError:
        return "错误：读取 Word 文件需要安装 python-docx：pip install python-docx"


def format_result(path: Path, content: str) -> str:
    """统一格式化工具返回结果。"""
    max_chars = 30000

    if len(content) > max_chars:
        content = (
            content[:max_chars]
            + "\n\n【提示】文件内容过长，当前只返回前 30000 个字符。"
        )

    return f"【文件名】{path.name}\n【文件内容】\n{content}"