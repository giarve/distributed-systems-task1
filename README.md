## Install dependencies

To install the required dependencies:

```pip install -r requirements.txt```

## Compile proto code

```python
python3 -m grpc_tools.protoc -I . server.proto  --python_out=. --grpc_python_out=.
```

## Getting started

Run the server (an instance of Redis must be running on your local machine):

```python3 server.py```

Use the client to create a worker:

```python3 client.py worker create```

Submit a task to the cluster:

```python3 client.py job run word_count_frequencies http://localhost:8000/file1.txt http://localhost:8000/file2.txt```

## Using the WebUI

Start the WebUI:

```python3 client.py serve```

To submit a new job, you can upload a .py file that has two functions, map_func and reduce_func. You can provide multiple arguments by separating them with spaces.

See `example_jobs/count_words.py` for an example.
