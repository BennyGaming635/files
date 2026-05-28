# Simple Files
Simple Files is a simple to use network web server for storing things. At the moment it supports file uploads, image and video previews and folders. Downloading media is kind of bugged at the moment but will soon be fixed once an update is pushed (or when i can be bothered (always wants to download as html but you can right click save as for now)).

If you have any feature ideas make an issue and I'll add em, otherwise enjoy :-)

## Setup

1. First run pip to install the requirements.
```python
pip install -r requirements.txt
```

2. Now create a folder (default we recommend is SHARED) where your script is stored.
**Windows**
```console
mkdir SHARED
```
**MacOS**
```console
mkdir SHARED
```
**Linux**
```console
mkdir SHARED
```
pssp - i now realise that they all have/had the same command...

3. Now simply run files.py, you should be prompted with an IP you can visit in your browser.
```python
python files.py
```
```console
========================================
SIMPLE FILES (UPLOADS ENABLED)
========================================
Folder: SHARED
URL: http://IP_ADDRESS:8000
========================================
```

## What can I change?
If you would like, you can use special args when running *files.py* with arguments like --host or --name. If you want to learn about these, please [read this](BOOT.md).
Our *amazing* icons were selected via Icons8, but you can still replace icons which are stored in *icons/* but the server folder can only be changed by [boot args](BOOT.md).


>[!CAUTION]
> please dont professionally use this, actually dont use this at all

## Plans to add next
Please [read here](TODO.md)