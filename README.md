# Crypto Data Converter

This web application allows you to convert crypto order history and transaction history from one platform's format to a standardized format.

## Features

- Upload CSV files for order history and transaction history
- Preview uploaded data
- Modify column mappings
- Process data according to specified mappings
- Store processed data in a local SQLite database

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/crypto-converter.git
   cd crypto-converter
   ```

2. Build and run the Docker container:
   ```
   docker-compose up --build
   ```

3. Access the application at `http://localhost:5000`

## Usage

1. Upload your order history and transaction history CSV files.
2. Review the preview of your data.
3. Modify the column mappings if necessary.
4. Click "Process Files" to convert your data.
5. View the processed results.

## Development

To run tests:
```
docker-compose run web pytest
```

To apply database migrations:
```
docker-compose run web flask db upgrade
```

## License

This project is licensed under the MIT License.