"""Generate the Phase 1 Superstore MySQL warehouse from the exported CSV files."""

from __future__ import annotations

import csv
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PHASE_DIR = Path(__file__).resolve().parents[1]
CSV_DIR = PHASE_DIR / "data" / "csv"
OUTPUT_FILE = PHASE_DIR / "sql" / "Superstore_DataWarehouse.sql"


TABLE_COLUMNS = {
    "DimProduct": [
        "ProductKey",
        "Product ID",
        "Product Name",
        "Category",
        "Sub-Category",
    ],
    "DimCustomer": [
        "CustomerKey",
        "Segment",
        "Customer Name",
        "Customer ID",
    ],
    "DimGeography": [
        "GeographyKey",
        "GeographyBusinessKey",
        "City",
        "State",
        "Country",
        "Region",
        "Market",
    ],
    "DimShipMode": [
        "ShipModeKey",
        "Ship Mode",
    ],
    "DimOrderPriority": [
        "PriorityKey",
        "Order Priority",
    ],
    "DimDate": [
        "DateKey",
        "GregorianDate",
        "GregorianYearInt",
        "GregorianMonthNo",
        "GregorianDayInMonth",
        "GregorianMonthDayInt",
        "GregorianDayOfWeekInt",
        "GregorianMonthName",
        "GregorianStr",
        "GregorianYearMonthSort",
        "GregorianYearMonthStr",
        "GregorianDayOfWeekName",
        "GrgorianWeekOfYearName",
        "GregorianWeekOfYearNo",
        "PersianInt",
        "PersianYearInt",
        "PersianMonthNo",
        "PersianDayInMonth",
        "PersianMonthDayInt",
        "PersianDayOfWeekInt",
        "PersianMonthName",
        "PersianStr",
        "PersianYearMonthInt",
        "PersianYearMonthStr",
        "PersianDayOfWeekName",
        "PersianWeekOfYearName",
        "PersianWeekOfYearNo",
        "PersianFullName",
        "SeasonCode",
        "SeasonName",
        "IsGregorianLeap",
        "IsPersianLeap",
        "PersianYearMonthSort",
    ],
    "FactSales": [
        "SalesRowKey",
        "OrderID",
        "ProductKey",
        "CustomerKey",
        "GeographyKey",
        "ShipModeKey",
        "PriorityKey",
        "OrderDateKey",
        "ShipDateKey",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
        "ShippingCost",
        "IsReturned",
        "DeliverDays",
    ],
}


PRIMARY_KEYS = {
    "DimProduct": "ProductKey",
    "DimCustomer": "CustomerKey",
    "DimGeography": "GeographyKey",
    "DimShipMode": "ShipModeKey",
    "DimOrderPriority": "PriorityKey",
    "DimDate": "DateKey",
    "FactSales": "SalesRowKey",
}


EXPECTED_ROW_COUNTS = {
    "DimProduct": 10246,
    "DimCustomer": 1589,
    "DimGeography": 3772,
    "DimShipMode": 4,
    "DimOrderPriority": 4,
    "DimDate": 1468,
    "FactSales": 49670,
}


TABLE_ORDER = [
    "DimProduct",
    "DimCustomer",
    "DimGeography",
    "DimShipMode",
    "DimOrderPriority",
    "DimDate",
    "FactSales",
]


INTEGER_COLUMNS = {
    "ProductKey",
    "CustomerKey",
    "GeographyKey",
    "ShipModeKey",
    "PriorityKey",
    "DateKey",
    "GregorianYearInt",
    "GregorianMonthNo",
    "GregorianDayInMonth",
    "GregorianMonthDayInt",
    "GregorianDayOfWeekInt",
    "GregorianYearMonthSort",
    "GregorianWeekOfYearNo",
    "PersianInt",
    "PersianYearInt",
    "PersianMonthNo",
    "PersianDayInMonth",
    "PersianMonthDayInt",
    "PersianDayOfWeekInt",
    "PersianYearMonthInt",
    "PersianWeekOfYearNo",
    "SeasonCode",
    "IsGregorianLeap",
    "IsPersianLeap",
    "PersianYearMonthSort",
    "SalesRowKey",
    "OrderDateKey",
    "ShipDateKey",
    "Quantity",
    "DeliverDays",
}


DECIMAL_SCALES = {
    "Sales": 4,
    "Discount": 3,
    "Profit": 4,
    "ShippingCost": 4,
}


CREATE_TABLES_SQL = """
CREATE TABLE `DimProduct` (
  `ProductKey` INT UNSIGNED NOT NULL,
  `Product ID` VARCHAR(20) NOT NULL,
  `Product Name` VARCHAR(255) NOT NULL,
  `Category` VARCHAR(32) NOT NULL,
  `Sub-Category` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`ProductKey`),
  UNIQUE KEY `uq_dimproduct_product_id` (`Product ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `DimCustomer` (
  `CustomerKey` INT UNSIGNED NOT NULL,
  `Segment` VARCHAR(32) NOT NULL,
  `Customer Name` VARCHAR(100) NOT NULL,
  `Customer ID` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`CustomerKey`),
  UNIQUE KEY `uq_dimcustomer_customer_id` (`Customer ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `DimGeography` (
  `GeographyKey` INT UNSIGNED NOT NULL,
  `GeographyBusinessKey` VARCHAR(128) NOT NULL,
  `City` VARCHAR(100) NOT NULL,
  `State` VARCHAR(100) NOT NULL,
  `Country` VARCHAR(100) NOT NULL,
  `Region` VARCHAR(50) NOT NULL,
  `Market` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`GeographyKey`),
  UNIQUE KEY `uq_dimgeography_business_key` (`GeographyBusinessKey`),
  KEY `idx_dimgeography_country` (`Country`),
  KEY `idx_dimgeography_market_region` (`Market`, `Region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `DimShipMode` (
  `ShipModeKey` TINYINT UNSIGNED NOT NULL,
  `Ship Mode` VARCHAR(32) NOT NULL,
  PRIMARY KEY (`ShipModeKey`),
  UNIQUE KEY `uq_dimshipmode_name` (`Ship Mode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `DimOrderPriority` (
  `PriorityKey` TINYINT UNSIGNED NOT NULL,
  `Order Priority` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`PriorityKey`),
  UNIQUE KEY `uq_dimorderpriority_name` (`Order Priority`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `DimDate` (
  `DateKey` INT UNSIGNED NOT NULL,
  `GregorianDate` DATE NOT NULL,
  `GregorianYearInt` SMALLINT UNSIGNED NOT NULL,
  `GregorianMonthNo` TINYINT UNSIGNED NOT NULL,
  `GregorianDayInMonth` TINYINT UNSIGNED NOT NULL,
  `GregorianMonthDayInt` SMALLINT UNSIGNED NOT NULL,
  `GregorianDayOfWeekInt` TINYINT UNSIGNED NOT NULL,
  `GregorianMonthName` VARCHAR(20) NOT NULL,
  `GregorianStr` VARCHAR(10) NOT NULL,
  `GregorianYearMonthSort` INT UNSIGNED NOT NULL,
  `GregorianYearMonthStr` VARCHAR(10) NOT NULL,
  `GregorianDayOfWeekName` VARCHAR(20) NOT NULL,
  `GrgorianWeekOfYearName` VARCHAR(16) NOT NULL,
  `GregorianWeekOfYearNo` TINYINT UNSIGNED NOT NULL,
  `PersianInt` INT UNSIGNED NOT NULL,
  `PersianYearInt` SMALLINT UNSIGNED NOT NULL,
  `PersianMonthNo` TINYINT UNSIGNED NOT NULL,
  `PersianDayInMonth` TINYINT UNSIGNED NOT NULL,
  `PersianMonthDayInt` SMALLINT UNSIGNED NOT NULL,
  `PersianDayOfWeekInt` TINYINT UNSIGNED NOT NULL,
  `PersianMonthName` VARCHAR(20) NOT NULL,
  `PersianStr` VARCHAR(10) NOT NULL,
  `PersianYearMonthInt` INT UNSIGNED NOT NULL,
  `PersianYearMonthStr` VARCHAR(7) NOT NULL,
  `PersianDayOfWeekName` VARCHAR(20) NOT NULL,
  `PersianWeekOfYearName` VARCHAR(16) NOT NULL,
  `PersianWeekOfYearNo` TINYINT UNSIGNED NOT NULL,
  `PersianFullName` VARCHAR(64) NOT NULL,
  `SeasonCode` TINYINT UNSIGNED NOT NULL,
  `SeasonName` VARCHAR(20) NOT NULL,
  `IsGregorianLeap` BOOLEAN NOT NULL,
  `IsPersianLeap` BOOLEAN NOT NULL,
  `PersianYearMonthSort` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`DateKey`),
  UNIQUE KEY `uq_dimdate_gregorian_date` (`GregorianDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `FactSales` (
  `SalesRowKey` INT UNSIGNED NOT NULL,
  `OrderID` VARCHAR(20) NOT NULL,
  `ProductKey` INT UNSIGNED NOT NULL,
  `CustomerKey` INT UNSIGNED NOT NULL,
  `GeographyKey` INT UNSIGNED NOT NULL,
  `ShipModeKey` TINYINT UNSIGNED NOT NULL,
  `PriorityKey` TINYINT UNSIGNED NOT NULL,
  `OrderDateKey` INT UNSIGNED NOT NULL,
  `ShipDateKey` INT UNSIGNED NOT NULL,
  `Sales` DECIMAL(18,4) NOT NULL,
  `Quantity` SMALLINT UNSIGNED NOT NULL,
  `Discount` DECIMAL(6,3) NOT NULL,
  `Profit` DECIMAL(18,4) NOT NULL,
  `ShippingCost` DECIMAL(18,4) NOT NULL,
  `IsReturned` BOOLEAN NOT NULL,
  `DeliverDays` TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (`SalesRowKey`),
  KEY `idx_factsales_order_id` (`OrderID`),
  KEY `idx_factsales_product` (`ProductKey`),
  KEY `idx_factsales_customer` (`CustomerKey`),
  KEY `idx_factsales_geography` (`GeographyKey`),
  KEY `idx_factsales_ship_mode` (`ShipModeKey`),
  KEY `idx_factsales_priority` (`PriorityKey`),
  KEY `idx_factsales_order_date` (`OrderDateKey`),
  KEY `idx_factsales_ship_date` (`ShipDateKey`),
  CONSTRAINT `fk_factsales_product`
    FOREIGN KEY (`ProductKey`) REFERENCES `DimProduct` (`ProductKey`),
  CONSTRAINT `fk_factsales_customer`
    FOREIGN KEY (`CustomerKey`) REFERENCES `DimCustomer` (`CustomerKey`),
  CONSTRAINT `fk_factsales_geography`
    FOREIGN KEY (`GeographyKey`) REFERENCES `DimGeography` (`GeographyKey`),
  CONSTRAINT `fk_factsales_ship_mode`
    FOREIGN KEY (`ShipModeKey`) REFERENCES `DimShipMode` (`ShipModeKey`),
  CONSTRAINT `fk_factsales_priority`
    FOREIGN KEY (`PriorityKey`) REFERENCES `DimOrderPriority` (`PriorityKey`),
  CONSTRAINT `fk_factsales_order_date`
    FOREIGN KEY (`OrderDateKey`) REFERENCES `DimDate` (`DateKey`),
  CONSTRAINT `fk_factsales_ship_date`
    FOREIGN KEY (`ShipDateKey`) REFERENCES `DimDate` (`DateKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
""".strip()


SQL_HEADER = """-- Superstore Final Project - Phase 1
-- This script creates the final MySQL data warehouse.
-- The tables and records were generated from the final Power BI CSV exports.

SET NAMES utf8mb4;

CREATE DATABASE IF NOT EXISTS `superstore_dw`
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE `superstore_dw`;

DROP TABLE IF EXISTS `FactSales`;
DROP TABLE IF EXISTS `DimDate`;
DROP TABLE IF EXISTS `DimOrderPriority`;
DROP TABLE IF EXISTS `DimShipMode`;
DROP TABLE IF EXISTS `DimGeography`;
DROP TABLE IF EXISTS `DimCustomer`;
DROP TABLE IF EXISTS `DimProduct`;

"""


SQL_FOOTER = """

COMMIT;

SELECT 'DimProduct' AS `TableName`, COUNT(*) AS `ActualRows`, 10246 AS `ExpectedRows`,
       IF(COUNT(*) = 10246, 'PASS', 'FAIL') AS `Status` FROM `DimProduct`
UNION ALL
SELECT 'DimCustomer', COUNT(*), 1589, IF(COUNT(*) = 1589, 'PASS', 'FAIL') FROM `DimCustomer`
UNION ALL
SELECT 'DimGeography', COUNT(*), 3772, IF(COUNT(*) = 3772, 'PASS', 'FAIL') FROM `DimGeography`
UNION ALL
SELECT 'DimShipMode', COUNT(*), 4, IF(COUNT(*) = 4, 'PASS', 'FAIL') FROM `DimShipMode`
UNION ALL
SELECT 'DimOrderPriority', COUNT(*), 4, IF(COUNT(*) = 4, 'PASS', 'FAIL') FROM `DimOrderPriority`
UNION ALL
SELECT 'DimDate', COUNT(*), 1468, IF(COUNT(*) = 1468, 'PASS', 'FAIL') FROM `DimDate`
UNION ALL
SELECT 'FactSales', COUNT(*), 49670, IF(COUNT(*) = 49670, 'PASS', 'FAIL') FROM `FactSales`;

SELECT
  COUNT(*) AS `FactRows`,
  COUNT(DISTINCT `OrderID`) AS `DistinctOrders`,
  SUM(`Sales`) AS `TotalSales`,
  SUM(`Profit`) AS `TotalProfit`,
  SUM(`Quantity`) AS `TotalQuantity`,
  SUM(`ShippingCost`) AS `TotalShippingCost`,
  COUNT(DISTINCT CASE WHEN `IsReturned` = 1 THEN `OrderID` END) AS `ReturnedOrders`,
  ROUND(
    100.0 * COUNT(DISTINCT CASE WHEN `IsReturned` = 1 THEN `OrderID` END)
    / COUNT(DISTINCT `OrderID`),
    2
  ) AS `ReturnRatePercent`,
  MIN(`DeliverDays`) AS `MinimumDeliveryDays`,
  MAX(`DeliverDays`) AS `MaximumDeliveryDays`
FROM `FactSales`;

SELECT
  MIN(`GregorianDate`) AS `StartDate`,
  MAX(`GregorianDate`) AS `EndDate`,
  COUNT(*) AS `DateRows`
FROM `DimDate`;
"""


def read_csv_table(table_name: str) -> list[dict[str, str]]:
    """Read one CSV and validate its columns, rows, and primary key."""

    csv_path = CSV_DIR / f"{table_name}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing CSV file: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)

        expected_columns = TABLE_COLUMNS[table_name]
        if reader.fieldnames != expected_columns:
            raise ValueError(
                f"Unexpected columns in {csv_path.name}.\n"
                f"Expected: {expected_columns}\n"
                f"Found:    {reader.fieldnames}"
            )

        rows = list(reader)

    expected_count = EXPECTED_ROW_COUNTS[table_name]
    if len(rows) != expected_count:
        raise ValueError(
            f"Unexpected row count in {csv_path.name}: "
            f"{len(rows):,} instead of {expected_count:,}"
        )

    for row_number, row in enumerate(rows, start=2):
        if any(value == "" for value in row.values()):
            raise ValueError(
                f"Blank value found in {csv_path.name}, row {row_number}"
            )

    primary_key = PRIMARY_KEYS[table_name]
    key_values = [row[primary_key] for row in rows]
    if len(key_values) != len(set(key_values)):
        raise ValueError(f"Duplicate {primary_key} found in {csv_path.name}")

    return sorted(rows, key=lambda row: int(row[primary_key]))


def read_all_tables() -> dict[str, list[dict[str, str]]]:
    """Read and validate all seven CSV files."""

    return {table_name: read_csv_table(table_name) for table_name in TABLE_ORDER}


def validate_foreign_keys(tables: dict[str, list[dict[str, str]]]) -> None:
    """Make sure every FactSales foreign key exists in its dimension table."""

    fact_rows = tables["FactSales"]
    relationships = [
        ("ProductKey", "DimProduct"),
        ("CustomerKey", "DimCustomer"),
        ("GeographyKey", "DimGeography"),
        ("ShipModeKey", "DimShipMode"),
        ("PriorityKey", "DimOrderPriority"),
        ("OrderDateKey", "DimDate"),
        ("ShipDateKey", "DimDate"),
    ]

    for fact_column, dimension_table in relationships:
        dimension_key = PRIMARY_KEYS[dimension_table]
        valid_keys = {row[dimension_key] for row in tables[dimension_table]}
        missing_keys = {
            row[fact_column]
            for row in fact_rows
            if row[fact_column] not in valid_keys
        }

        if missing_keys:
            examples = sorted(missing_keys)[:5]
            raise ValueError(
                f"Invalid {fact_column} values in FactSales. Examples: {examples}"
            )


def quote_mysql_text(value: str) -> str:
    """Escape a text value and return a valid MySQL string literal."""

    escaped = (
        value.replace("\\", "\\\\")
        .replace("\x00", "\\0")
        .replace("'", "''")
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
        .replace("\x1a", "\\Z")
    )
    return f"'{escaped}'"


def format_decimal(value: str, scale: int) -> str:
    """Round a decimal value to the precision used by the warehouse."""

    step = Decimal(1).scaleb(-scale)
    rounded = Decimal(value).quantize(step, rounding=ROUND_HALF_UP)
    return format(rounded, f".{scale}f")


def format_sql_value(column: str, value: str) -> str:
    """Convert one CSV value to its SQL representation."""

    if column == "GregorianDate":
        return quote_mysql_text(value[:10])

    if column == "IsReturned":
        normalized = value.strip().casefold()
        if normalized == "true":
            return "1"
        if normalized == "false":
            return "0"
        raise ValueError(f"Unexpected IsReturned value: {value!r}")

    if column in INTEGER_COLUMNS:
        return str(int(value))

    if column in DECIMAL_SCALES:
        return format_decimal(value, DECIMAL_SCALES[column])

    return quote_mysql_text(value)


def write_table_data(
    sql_file,
    table_name: str,
    rows: list[dict[str, str]],
    batch_size: int = 500,
) -> None:
    """Write table records as multi-row INSERT statements."""

    columns = TABLE_COLUMNS[table_name]
    column_list = ", ".join(f"`{column}`" for column in columns)


    for start in range(0, len(rows), batch_size):
        batch = rows[start : start + batch_size]
        sql_file.write(f"INSERT INTO `{table_name}` ({column_list}) VALUES\n")

        sql_rows = []
        for row in batch:
            values = [format_sql_value(column, row[column]) for column in columns]
            sql_rows.append("(" + ", ".join(values) + ")")

        sql_file.write(",\n".join(sql_rows))
        sql_file.write(";\n")


def generate_sql_file(tables: dict[str, list[dict[str, str]]]) -> None:
    """Create the final self-contained MySQL file."""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8", newline="\n") as sql_file:
        sql_file.write(SQL_HEADER)
        sql_file.write(CREATE_TABLES_SQL)
        sql_file.write("\n\nSTART TRANSACTION;\n")

        for table_name in TABLE_ORDER:
            write_table_data(sql_file, table_name, tables[table_name])

        sql_file.write(SQL_FOOTER)


def main() -> None:
    print(f"Reading CSV files from: {CSV_DIR}")
    tables = read_all_tables()

    print("Checking primary and foreign keys...")
    validate_foreign_keys(tables)

    print("Creating the SQL data warehouse file...")
    generate_sql_file(tables)

    total_rows = sum(len(rows) for rows in tables.values())
    size_mb = OUTPUT_FILE.stat().st_size / (1024 * 1024)

    print(f"Done: {OUTPUT_FILE}")
    print(f"Tables: {len(tables)}")
    print(f"Rows: {total_rows:,}")
    print(f"File size: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()
