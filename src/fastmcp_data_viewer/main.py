from .app import mcp
# Import the tools to register them
from .data_source import parquet_viewer

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
