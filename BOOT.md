# Boot Arguments

When running Simple Files, there are several arguments you can use to change how your file server works.

## Arguments

### Change the Port

To change the port the server runs on, use:

```bash
python files.py --port <port>
```

The default port is `8000`.

Example:

```bash
python files.py --port 9000
```

---

### Change the Root Folder

To change the folder the server uses to store files, use:

```bash
python files.py --folder <folder>
```

Example:

```bash
python files.py --folder UPLOADS
```

The default folder is `SHARED/`.

If the folder does not exist, it will be created automatically.

---

### Change the Host IP

To change the host IP address the server runs on, use:

```bash
python files.py --host <host>
```

Example:

```bash
python files.py --host 127.0.0.1 --port 3000
```

This example changes the server address from:

```text
0.0.0.0:8000
```

to:

```text
127.0.0.1:3000
```

---

### Change the Server Name

To change the displayed server name, use:

```bash
python files.py --name "<server name>"
```

Example:

```bash
python files.py --name "Dev Server Store 1"
```
> [!NOTE]
> Your custom server name must be wrapped in quotation marks.
