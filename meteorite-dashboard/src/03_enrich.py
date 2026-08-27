import logging
from pathlib import Path

import numpy as np
import pandas as pd

DATA_CLEAN_DIR = Path("data_clean")
DATA_ENRICHED_DIR = Path("data_enriched")
CLEAN_FILE_NAME = "Meteorite_Landings_CLEAN.csv"
ENRICHED_FILE_NAME = "Meteorite_Landings_ENRICHED.csv"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("meteorite_dashboard")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger


def load_clean_meteorite_data(logger: logging.Logger) -> pd.DataFrame:
    clean_file_path = DATA_CLEAN_DIR / CLEAN_FILE_NAME

    if not clean_file_path.exists():
        logger.error(f"Clean data file not found: {clean_file_path}")
        raise FileNotFoundError(f"Clean data file not found: {clean_file_path}")

    logger.info(f"Loading cleaned meteorite data from {clean_file_path}")
    df = pd.read_csv(clean_file_path)
    logger.info(f"Loaded {len(df)} rows and {len(df.columns)} columns")

    return df


def add_severity_score(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Adds a severity score based on mass (g).
    """
    logger.info("Adding severity_score based on mass (g)")

    bins = [0, 100, 1000, 10000, 100000, np.inf]
    labels = [1, 2, 3, 4, 5]

    df["severity_score"] = pd.cut(
        df["mass (g)"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return df


def add_date_fields(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Adds year_valid, decade, and century fields.
    """
    logger.info("Adding date dimension fields")

    df["year_valid"] = df["year"].between(800, 2100)

    df.loc[df["year_valid"], "decade"] = (df["year"] // 10) * 10
    df.loc[df["year_valid"], "century"] = (df["year"] // 100) + 1

    return df


def add_mass_category(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Adds mass_category based on mass (g).
    """
    logger.info("Adding mass_category based on mass (g)")

    bins = [0, 10, 100, 1000, 10000, np.inf]
    labels = ["tiny", "small", "medium", "large", "massive"]

    df["mass_category"] = pd.cut(
        df["mass (g)"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return df


def add_fall_found_flag(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Adds a fall_found_flag based on the normalized fall column.
    """
    logger.info("Adding fall_found_flag")

    fall_norm = df["fall"].str.lower()

    df["fall_found_flag"] = np.where(
        fall_norm == "fell",
        "fell",
        np.where(fall_norm == "found", "found", "unknown")
    )

    return df


def add_hemisphere_flags(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Adds hemisphere_ns and hemisphere_ew based on latitude/longitude.
    Assumes latitude and longitude were created in 02_clean.py.
    """
    logger.info("Adding hemisphere flags")

    df["hemisphere_ns"] = np.where(df["latitude"] >= 0, "north", "south")
    df["hemisphere_ew"] = np.where(df["longitude"] >= 0, "east", "west")

    return df


def add_location_quality(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """
    Adds location_quality flag based on coordinate validity.
    """
    logger.info("Adding location_quality flag")

    cond_missing = df["latitude"].isna() | df["longitude"].isna()
    cond_invalid = ~cond_missing & (
        (df["latitude"] < -90) | (df["latitude"] > 90) |
        (df["longitude"] < -180) | (df["longitude"] > 180)
    )

    df["location_quality"] = "valid"
    df.loc[cond_missing, "location_quality"] = "missing"
    df.loc[cond_invalid, "location_quality"] = "invalid"

    return df


def save_enriched_data(df: pd.DataFrame, logger: logging.Logger) -> None:
    enriched_file_path = DATA_ENRICHED_DIR / ENRICHED_FILE_NAME

    DATA_ENRICHED_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Saving enriched meteorite data to {enriched_file_path}")
    df.to_csv(enriched_file_path, index=False)
    logger.info("Enriched data saved successfully")


def main() -> None:
    logger = setup_logger()

    try:
        df = load_clean_meteorite_data(logger)
        df = add_severity_score(df, logger)
        df = add_date_fields(df, logger)
        df = add_mass_category(df, logger)
        df = add_fall_found_flag(df, logger)
        df = add_hemisphere_flags(df, logger)
        df = add_location_quality(df, logger)

        save_enriched_data(df, logger)

        logger.info("Data enrichment completed successfully.")
    except Exception as exc:
        logger.exception(f"Enrichment failed: {exc}")
        raise


if __name__ == "__main__":
    main()
