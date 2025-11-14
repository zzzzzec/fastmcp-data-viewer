import os
import sys

# Add the 'src' directory to the path to allow absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastmcp import FastMCP
from fastmcp_data_viewer.data_source.parquet_viewer import get_summary, get_item

mcp = FastMCP(
    name="data-viewer",
    tools=[get_summary, get_item],
)
