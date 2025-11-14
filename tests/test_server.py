# tests/test_server.py

import pytest
import pandas as pd
from pathlib import Path

# 确保在运行测试前导入工具，以便它们被注册
from fastmcp_data_viewer.data_source import parquet_viewer

from fastmcp import Client
from fastmcp_data_viewer.app import mcp  # 导入你的 mcp 实例

# Fixture for simple data
@pytest.fixture
def simple_parquet_file(tmp_path: Path) -> str:
    """创建一个临时的、包含简单数据的 Parquet 文件"""
    file_path = tmp_path / "simple_data.parquet"
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'age': [25, 30, 35, 40],
    })
    df.to_parquet(file_path)
    return str(file_path)

# Fixture for data with long text
@pytest.fixture
def long_text_data() -> dict:
    """返回一个包含长文本字符串的字典，方便复用"""
    long_string = "start_" + ("x" * 300) + "_end"
    return {"id": [1], "description": [long_string]}

@pytest.fixture
def long_text_parquet_file(tmp_path: Path, long_text_data: dict) -> str:
    """创建一个临时的、包含长文本的 Parquet 文件"""
    file_path = tmp_path / "long_text_data.parquet"
    df = pd.DataFrame(long_text_data)
    df.to_parquet(file_path)
    return str(file_path)


@pytest.mark.asyncio
async def test_get_summary_defaults(simple_parquet_file: str):
    """测试 get_summary 的默认行为 (2行预览, 200字符截断)"""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_summary",
            arguments={"path": simple_parquet_file}
        )
        summary = result.structured_content
        assert summary is not None
        assert summary['rows'] == 4
        assert len(summary['preview']) == 2  # 默认预览行数应为 2
        assert summary['preview'][0]['name'] == 'Alice'
        assert summary['preview'][1]['name'] == 'Bob'

@pytest.mark.asyncio
async def test_get_summary_custom_preview_rows(simple_parquet_file: str):
    """测试自定义 preview_rows 参数"""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_summary",
            arguments={"path": simple_parquet_file, "preview_rows": 3}
        )
        summary = result.structured_content
        assert len(summary['preview']) == 3
        assert summary['preview'][2]['name'] == 'Charlie'

@pytest.mark.asyncio
async def test_get_summary_default_truncation(long_text_parquet_file: str):
    """测试默认的文本截断逻辑 (max_col_width=200)"""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_summary",
            arguments={"path": long_text_parquet_file}
        )
        summary = result.structured_content
        preview_text = summary['preview'][0]['description']
        assert len(preview_text) == 200 # 198 + ..
        assert preview_text.startswith("start_")
        assert not preview_text.endswith("_end")
        assert ".." in preview_text

@pytest.mark.asyncio
async def test_get_summary_no_truncation(long_text_parquet_file: str, long_text_data: dict):
    """测试 max_col_width=0 时不截断文本"""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_summary",
            arguments={"path": long_text_parquet_file, "max_col_width": 0}
        )
        summary = result.structured_content
        preview_text = summary['preview'][0]['description']
        original_text = long_text_data['description'][0]
        assert preview_text == original_text


@pytest.mark.asyncio
async def test_get_item_tool(simple_parquet_file: str):
    """测试 get_item 工具是否能正确返回指定索引的数据"""
    async with Client(mcp) as client:
        result = await client.call_tool(
            "get_item",
            arguments={"path": simple_parquet_file, "index": 1}
        )
        item = result.structured_content
        assert item is not None
        assert item['name'] == 'Bob'
        assert item['age'] == 30