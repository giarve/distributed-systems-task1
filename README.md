## Compile proto code

```python
python3 -m grpc_tools.protoc -I . worker.proto  --python_out=. --grpc_python_out=.
python3 server.py
python3 client.py -h
```
