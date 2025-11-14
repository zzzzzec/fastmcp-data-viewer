# FastMCP Data Viewer

A data viewer tool built with FastMCP that allows you to inspect the contents and summary of various data formats. This initial version supports Parquet files.

## Features

- View a summary of a Parquet file, including column names, types, row count, file size, and a preview of the first few rows.
- Retrieve a specific row (item) from a Parquet file by its index.

## Requirements

The project requires the following Python packages:
- `fastmcp`
- `pandas`
- `pyarrow`

You can install them using pip:
```bash
pip install -r requirements.txt
```

## Installation

This project is designed to be used as a Gemini CLI tool. An installation script is provided for convenience.

1. Make sure you have the Gemini CLI and its dependencies installed.
2. Run the installation script:
```bash
bash install.sh
```
This will install the tool with the name `data-viewer`.

## Usage

Once installed, you can interact with the data viewer through the Gemini CLI. The following tools are available:

### `get_summary`

Provides a summary of a Parquet file.

**Arguments:**
- `path` (str): The path to the Parquet file.
- `preview_rows` (int, optional): The number of rows to include in the preview. Defaults to `2`.
- `max_col_width` (int, optional): The maximum character width for text columns in the preview. Truncates long strings. Defaults to `200`. Set to `0` to disable truncation.

**Example:**
```
@data-viewer get_summary path='test.parquet'
```

### `get_item`

Retrieves a specific item (row) from a Parquet file by its index.

**Arguments:**
- `path` (str): The path to the Parquet file.
- `index` (int): The 0-based index of the item to retrieve.

**Example:**
```
@data-viewer get_item path='test.parquet' index=0
```
