import pandas as pd
import numpy as np

def _convert_numpy_types(obj):
    """Recursively convert numpy types to native Python types for JSON serialization."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _convert_numpy_types(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_convert_numpy_types(v) for v in obj]
    return obj

def _truncate_text(text: str, max_width: int) -> str:
    """Helper function to truncate text if it exceeds max_width."""
    if not isinstance(text, str) or max_width <= 0 or len(text) <= max_width:
        return text

    # For very large widths, truncate from the middle
    if max_width > 200:
        return text[:100] + ".." + text[-100:]
    
    # Otherwise, truncate at the end
    return text[:max_width - 2] + ".."

def get_summary(path: str, preview_rows: int = 2, max_col_width: int = 200) -> dict:
    """
    Get a summary of a Parquet file.

    Args:
        path: The path to the Parquet file.
        preview_rows: The number of rows to include in the preview.
        max_col_width: The maximum character width for text columns in the preview.
                       If a string exceeds this, it will be truncated.
                       Set to 0 for no truncation.

    Returns:
        A summary of the file, including columns, types, number of rows, and file size.
    """
    df = pd.read_parquet(path)
    
    preview_df = df.head(preview_rows)
    preview_records = preview_df.to_dict(orient="records")

    # Apply truncation logic if max_col_width is set
    if max_col_width > 0:
        for row in preview_records:
            for key, value in row.items():
                row[key] = _truncate_text(value, max_col_width)

    summary = {
        "columns": df.columns.tolist(),
        "types": {col: str(df[col].dtype) for col in df.columns},
        "rows": len(df),
        "file_size": f"{df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB",
        "preview": preview_records,
    }
    
    return _convert_numpy_types(summary)

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
    item = df.iloc[index].to_dict()
    return _convert_numpy_types(item)
