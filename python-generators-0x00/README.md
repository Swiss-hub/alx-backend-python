# Python Generators 0x00 - MySQL Seeder

This module contains a Python script `seed.py` that connects to a MySQL server, creates a database and table, and populates it using data from `user_data.csv`.

## Features

- Connects to MySQL server
- Creates `ALX_prodev` database
- Creates `user_data` table with fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR)
  - `email` (VARCHAR)
  - `age` (DECIMAL)
- Inserts unique users from CSV file

## Usage

Run the main script:

```bash
./0-main.py
