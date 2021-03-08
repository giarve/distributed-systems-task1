## Compile proto code

```python
cd examples/python/helloworld
python -m grpc_tools.protoc -I . worker.proto  --python_out=. --grpc_python_out=.
```
