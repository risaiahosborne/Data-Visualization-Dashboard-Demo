import logging
from pathlib import Path

import pandas as pd

DATA_RAW_DIR = Path("data_raw")
DATA_CLEAN_DIR = Path("data_clean")
RAW_FILE_NAME = "Meteorite_Landings.csv"
CLEAN_FILE_NAME = "Meteorite_Landings_CLEAN.csv"

def setup_logger() -> logging.Logger:
    """
    Sets up a logger for the application.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("meteorite_dashboard")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Create console handler with a higher log level        
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # Create formatter and add it to the handlers        
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        
        # Add the handlers to the logger
        logger.addHandler(ch) 
        
    return logger

def load_raw_meteorite_data(logger: logging.Logger) -> pd.DataFrame:
    """
    Loads the raw meteorite data from a CSV file.
    """
    raw_file_path = DATA_RAW_DIR / RAW_FILE_NAME
    
    #Check if the file exists before attempting to read it
    if not raw_file_path.exists():
        logger.error(f"Raw data file not found: {raw_file_path}")
        raise FileNotFoundError(f"Raw data file not found: {raw_file_path}")
    
    logger.info(f"Loading raw meteorite data from {raw_file_path}")
    df = pd.read_csv(raw_file_path)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    
    return df

def clean_numeric_data(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Cleans the numeric data
    """
    
    numeric_columns = ["mass (g)", "year", "reclat", "reclong", ]
    
    for col in numeric_columns:
        if col in df.columns:
            # Convert to numeric, coercing errors to NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
            logger.info(f"Cleaned numeric data for column: {col}")
        else:
            logger.warning(f"Column {col} not found in DataFrame")
            
    return df

def clean_text_fields(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Cleans the text fields in the DataFrame.
    """
    
    text_columns = ["name", "nametype", "recclass", "fall", "GeoLocation"]
    
    for col in text_columns:
        if col in df.columns:
            # Strip whitespace and convert to string
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].str.strip().str.lower()
            logger.info(f"Cleaned text data for column: {col}")
        else:
            logger.warning(f"Column {col} not found in DataFrame")
            
    return df

def clean_geolocation(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Cleans the GeoLocation field in the DataFrame.
    """
    
    if "GeoLocation" in df.columns:
        # Remove parentheses and split into latitude and longitude
        df["GeoLocation"] = df["GeoLocation"].str.replace(r"[()]", "", regex=True)
        df[["latitude", "longitude"]] = df["GeoLocation"].str.split(",", expand=True)
        
        # Convert to numeric, coercing errors to NaN
        df["latitude"] = pd.to_numeric(df["latitude"], errors='coerce')
        df["longitude"] = pd.to_numeric(df["longitude"], errors='coerce')
        
        logger.info("Cleaned GeoLocation data")
    else:
        logger.warning("Column GeoLocation not found in DataFrame")
        
    return df

def save_cleaned_data(df: pd.DataFrame, logger: logging.Logger) -> None:
    """
    Saves the cleaned DataFrame to a CSV file.
    """
    clean_file_path = DATA_CLEAN_DIR / CLEAN_FILE_NAME
    
    # Ensure the clean data directory exists
    DATA_CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    
    df.to_csv(clean_file_path, index=False)
    logger.info(f"Saved cleaned data to {clean_file_path}")

def main() -> None:
    logger = setup_logger()

    try:
        df = load_raw_meteorite_data(logger)
        df = clean_numeric_data(df, logger)
        df = clean_text_fields(df, logger)
        df = clean_geolocation(df, logger)

        save_cleaned_data(df, logger)

        logger.info("Data cleaning completed successfully.")

    except Exception as exc:
        logger.exception(f"Cleaning failed: {exc}")
        raise


if __name__ == "__main__":
    main()

    