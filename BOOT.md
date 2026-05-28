# Boot Arguments
When running Simple Files, there are many arguments you can run to change certain functions on your file server.

## Arguments
To change the port the server is deployed on, use
```python
python files.py --port
```
The default port is 8000.

For example:
```python
python files.py --port 9000
```
---
To change the folder the server will use to store files (as a root folder), use
```python
python files.py --folder
```

For example:
```python
python.files.py --folder UPLOADS
```

The default folder is SHARED/ (folder will automatically be created).
---
To change the host IP, of which the server is deployed on, use
```python
python files.py --host
```

For example:
```python
python files.py --host 127.0.0.1 --port 3000
```

(This examples shows a change from 0.0.0.0:8000 to 127.0.0.1:3000)
---
To change the name displayed on your server, use
```python
python files.py --name
```

For example:
```python
python files.py --name "Dev Server Store 1"
```
**Note: Your new name *must* be in brackets**

