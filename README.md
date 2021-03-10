## Install dependencies

To install the required dependencies:

```pip install -r requirements.txt```

## Compile proto code

```python
python3 -m grpc_tools.protoc -I . server.proto  --python_out=. --grpc_python_out=.
```

## Getting started

Run the server:

```python3 server.py```

Use the client to create a worker:

```python3 client.py worker create```

Submit a task to the cluster:

```python3 client.py job run-wordcount http://localhost:8000/file1.txt http://localhost:8000/file2.txt```