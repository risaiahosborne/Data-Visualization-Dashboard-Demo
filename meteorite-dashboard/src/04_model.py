import logging 
from pathlib import Path

import pandas as pd

DATA_ENRICHED_DIR = Path("data_enriched")
DATA_MODEL_DIR = Path("data_model")
ENRICHED_FILE_NAME = "Meteorite_Landings_ENRICHED.csv"

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

def load_enriched_meteorite_data(logger: logging.Logger) -> pd.DataFrame:
    """
    Loads the enriched meteorite data from a CSV file.
    """
    enriched_file_path = DATA_ENRICHED_DIR / ENRICHED_FILE_NAME
    
    # Check if the file exists before attempting to read it
    if not enriched_file_path.exists():
        logger.error(f"Enriched data file not found: {enriched_file_path}")
        raise FileNotFoundError(f"Enriched data file not found: {enriched_file_path}")
    
    logger.info(f"Loading enriched meteorite data from {enriched_file_path}")
    df = pd.read_csv(enriched_file_path)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")
    
    return df

def build_dim_meteorite(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    dim = df[["id", "name", "mass (g)", "severity_score"]].drop_duplicates()
    dim = dim.rename(columns={"id": "meteorite_id", "mass (g)": "mass_g"})
    logger.info(f"Built dim_meteorite with {len(dim)} rows")
    return dim


def build_dim_location(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    dim = df[["latitude", "longitude", "hemisphere_ns", "hemisphere_ew", "location_quality"]].drop_duplicates()
    dim = dim.reset_index(drop=True)
    dim["location_key"] = dim.index + 1
    logger.info(f"Built dim_location with {len(dim)} rows")
    return dim


def build_dim_time(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    dim = df[["year", "decade", "century", "year_valid"]].drop_duplicates()
    dim = dim.reset_index(drop=True)
    dim["time_key"] = dim.index + 1
    logger.info(f"Built dim_time with {len(dim)} rows")
    return dim


def build_dim_classification(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    dim = df[["recclass", "nametype", "fall", "fall_found_flag"]].drop_duplicates()
    dim = dim.reset_index(drop=True)
    dim["classification_key"] = dim.index + 1
    logger.info(f"Built dim_classification with {len(dim)} rows")
    return dim

def build_fact_meteorite(
    df: pd.DataFrame,
    dim_meteorite: pd.DataFrame,
    dim_location: pd.DataFrame,
    dim_time: pd.DataFrame,
    dim_classification: pd.DataFrame,
    logger: logging.Logger,
) -> pd.DataFrame:

    # join location_key
    fact = df.merge(
        dim_location,
        on=["latitude", "longitude", "hemisphere_ns", "hemisphere_ew", "location_quality"],
        how="left",
    )

    # join time_key
    fact = fact.merge(
        dim_time,
        on=["year", "decade", "century", "year_valid"],
        how="left",
    )

    # join classification_key
    fact = fact.merge(
        dim_classification,
        on=["recclass", "nametype", "fall", "fall_found_flag"],
        how="left",
    )

    # select fact columns
    fact = fact[
        [
            "id",
            "location_key",
            "time_key",
            "classification_key",
            "mass (g)",
            "severity_score",
            "mass_category",
            "fall_found_flag",
            "location_quality",
        ]
    ].rename(columns={"id": "meteorite_id", "mass (g)": "mass_g"})

    logger.info(f"Built fact_meteorite_events with {len(fact)} rows")
    return fact

def save_model_tables(
    dim_meteorite: pd.DataFrame,
    dim_location: pd.DataFrame,
    dim_time: pd.DataFrame,
    dim_classification: pd.DataFrame,
    fact_meteorite_events: pd.DataFrame,
    logger: logging.Logger,
) -> None:
    DATA_MODEL_DIR.mkdir(parents=True, exist_ok=True)

    dim_meteorite.to_csv(DATA_MODEL_DIR / "dim_meteorite.csv", index=False)
    dim_location.to_csv(DATA_MODEL_DIR / "dim_location.csv", index=False)
    dim_time.to_csv(DATA_MODEL_DIR / "dim_time.csv", index=False)
    dim_classification.to_csv(DATA_MODEL_DIR / "dim_classification.csv", index=False)
    fact_meteorite_events.to_csv(DATA_MODEL_DIR / "fact_meteorite_events.csv", index=False)

    logger.info("Saved all model tables to data_model/")

def main() -> None:
    logger = setup_logger()

    try:
        df = load_enriched_meteorite_data(logger)

        dim_meteorite = build_dim_meteorite(df, logger)
        dim_location = build_dim_location(df, logger)
        dim_time = build_dim_time(df, logger)
        dim_classification = build_dim_classification(df, logger)

        fact_meteorite_events = build_fact_meteorite(
            df,
            dim_meteorite,
            dim_location,
            dim_time,
            dim_classification,
            logger,
        )

        save_model_tables(
            dim_meteorite,
            dim_location,
            dim_time,
            dim_classification,
            fact_meteorite_events,
            logger,
        )

        logger.info("Data modeling completed successfully.")
    except Exception as exc:
        logger.exception(f"Modeling failed: {exc}")
        raise


if __name__ == "__main__":
    main()