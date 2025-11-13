import pandas as pd
from fastmcp import FastMCP
from pydantic import BaseModel
mcp = FastMCP(name="DataViewer")
class ParquetViewer:
    @staticmethod
    @mcp.tool()
    def get_summary(path: str) -> dict:
        """
        Get a summary of a Parquet file.

        Args:
            path: The path to the Parquet file.

        Returns:
            A summary of the file, including columns, types, number of rows, and file size.
        """
        df = pd.read_parquet(path)
        return {
            "columns": df.columns.tolist(),
            "types": {col: str(df[col].dtype) for col in df.columns},
            "rows": len(df),
            "file_size": f"{df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB",
            "preview": df.head(3).to_dict(orient="records"),
        }

    @staticmethod
    @mcp.tool()
    def get_item(path: str, index: int) -> dict:
        """
        Get a specific item from a Parquet file.

        Args:
            path: The path to the Parquet file.
            index: The index of the item to retrieve.

        Returns:
            The item at the specified index.
        """
        df = pd.read_parquet(path)
        return df.iloc[index].to_dict()

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
