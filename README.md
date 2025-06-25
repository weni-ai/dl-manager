# Datalake Manager

Manage access to the data lake.

## Overview

This project provides a gRPC service for sending data to a data lake. The service receives data through its gRPC endpoints and forwards it to a data lake backend, abstracting the direct interaction with the data source.

The main components are:
- **gRPC Server**: Exposes methods to insert different types of data (traces, events, messages, etc.).
- **RedshiftManager**: A manager class responsible for handling the business logic and sending data to the data lake.
- **RedshiftClient**: A client to communicate with an external API that presumably ingests the data into Redshift.

## Features

- gRPC interface for high-performance communication.
- Rate limiting on gRPC endpoints to prevent abuse.
- Structured way to send different kinds of data to the data lake.
- Decoupled architecture using managers and clients.

## Getting Started

### Prerequisites

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/weni-ai/dl-manager.git
   cd datalake-manager
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

### Running the server

To start the gRPC server, run the following command:

```bash
poetry run python -m datalake_manager.server.server
```

The server will start on port `50051`.

## gRPC Services

The server exposes multiple services for different data types. Here are the proto definitions:

- `datalake_manager/server/proto/traces/traces.proto`
- `datalake_manager/server/proto/events/events.proto`
- `datalake_manager/server/proto/msgs/msgs.proto`
- `datalake_manager/server/proto/message_template/message_templates.proto`

You can use a gRPC client like `grpcurl` or `postman` to interact with the services.

## Running Tests

To run the test suite, use:

```bash
poetry run pytest
```

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us. 