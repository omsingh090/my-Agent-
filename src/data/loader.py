"""
Data Loader Module
Loads data from various formats: CSV, JSON, Excel.
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load data from various formats."""

    SUPPORTED_FORMATS = [".csv", ".json", ".xlsx", ".xls"]
    MAX_FILE_SIZE_MB = 500

    @staticmethod
    def load(file_path: str) -> tuple:
        """
        Load data from file with validation.

        Args:
            file_path: Path to data file

        Returns:
            Tuple of (dataframe, metadata)

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If format not supported or file too large

        Example:
            >>> df, meta = DataLoader.load("data.csv")
            >>> print(meta['rows'], meta['columns'])
            1000 15
        """
        path = Path(file_path)

        # Validation
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in DataLoader.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {path.suffix}. "
                f"Supported: {DataLoader.SUPPORTED_FORMATS}"
            )

        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > DataLoader.MAX_FILE_SIZE_MB:
            raise ValueError(
                f"File too large: {file_size_mb:.1f}MB "
                f"(max: {DataLoader.MAX_FILE_SIZE_MB}MB)"
            )

        # Load based on format
        if path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
        elif path.suffix.lower() == ".json":
            df = pd.read_json(file_path)
        elif path.suffix.lower() in [".xlsx", ".xls"]:
            df = pd.read_excel(file_path)

        # Generate metadata
        metadata = {
            "file_name": path.name,
            "file_size_mb": round(file_size_mb, 2),
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": list(df.columns),
            "dtypes": {col: str(df[col].dtype) for col in df.columns},
        }

        logger.info(f"✓ Loaded {metadata['rows']} rows, {metadata['columns']} columns")
        return df, metadata

    @staticmethod
    def validate_schema(df: pd.DataFrame, required_columns: list = None) -> bool:
        """
        Validate dataframe schema.

        Args:
            df: Dataframe to validate
            required_columns: List of required column names

        Returns:
            True if valid, False otherwise

        Example:
            >>> is_valid = DataLoader.validate_schema(df, ["revenue", "date"])
        """
        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                logger.error(f"Missing required columns: {missing}")
                return False

        if len(df) == 0:
            logger.error("Empty dataframe")
            return False

        return True

    @staticmethod
    def infer_types(df: pd.DataFrame) -> pd.DataFrame:
        """
        Infer and convert data types.

        Args:
            df: Input dataframe

        Returns:
            Dataframe with inferred types

        Example:
            >>> df = DataLoader.infer_types(df)
        """
        for col in df.columns:
            # Try numeric
            try:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                if df[col].isna().sum() == 0:
                    continue
            except:
                pass

            # Try datetime
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                if df[col].isna().sum() == 0:
                    continue
            except:
                pass

            # Default to string
            df[col] = df[col].astype(str)

        logger.info("✓ Types inferred")
        return df
