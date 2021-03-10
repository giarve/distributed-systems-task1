## Compile proto code

```python
python3 -m grpc_tools.protoc -I . server.proto  --python_out=. --grpc_python_out=.
python3 server.py
python3 client.py -h
```

Tested with rq@dcbbd067f0e94637f475839eca0ae805d0b2a323

To install:
python3 -m pip install --upgrade git+https://github.com/rq/rq.git@dcbbd067f0e94637f475839eca0ae805d0b2a323

pip install -r requirements.txt