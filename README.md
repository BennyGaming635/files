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
At the moment, the only recommended changes you should make are changes to the icons (which are 48x48px). These icons were sourced via Icons8 but they can easily be changed out.
You can also change the folder that files are shared via, which is currently /SHARED/. You can also change the port if you want too.



>[!CAUTION]
> please dont professionally use this, actually dont use this at all