import logging
from pathlib import Path 

import pandas as pd

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

DATA_RAW_DIR = Path("data_raw")
RAW_FILE_NAME = "Meteorite_Landings.csv"

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

def validate_schema(df: pd.DataFrame, logger: logging.Logger) -> bool:
    """
    Validates the schema of the DataFrame against expected columns.

    Args:
        df (pd.DataFrame): DataFrame to validate.
        logger (logging.Logger): Logger instance for logging.

    Returns:
        bool: True if schema is valid, False otherwise.
    """
    expected_columns = {
        "name", "id", "nametype", "recclass", "mass (g)", 
        "fall", "year", "reclat", "reclong", "GeoLocation"
    }
    
    actual_columns = set(df.columns)
    missing = expected_columns - actual_columns
    
    if missing:
        logger.error(f"Schema validation failed. Missing columns: {missing}")
        return False
    
    logger.info("Schema validation passed.")
    return True

def main() -> None:
    """
    Main function to load and validate raw meteorite data.
    """
    logger = setup_logger()
    
    try:
        df = load_raw_meteorite_data(logger)
        
        if not validate_schema(df, logger):
            logger.error("Data schema validation failed. Exiting.")
            return
        
        logger.info("Data ingestion completed successfully.")
    
    except Exception as e:
        logger.exception(f"An error occurred during data ingestion: {e}")
        
if __name__ == "__main__":
    main()