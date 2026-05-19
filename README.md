# 🌿 TWIGOsk
Twigosk is based on TWIG, the open‑source browser core used inside ConSurf (and now Sneakon too).  

Unlike TWIG, this has tabs, window controls and browser controls removed.
## 📦 Requirements

TWIG uses Python and PyQt5.  
To build or run it, you’ll need the following modules:

- PyQt5  
- PyQtWebEngine  
- PyInstaller (for building)

```
pip install PyQt5 PyQtWebEngine pyinstaller
```

---

## 🧪 Running TWIG From Source

If you just want to test TWIG without building anything:

```
python Browser.py
```

---

## 🛠️ Building TWIG

TWIG ships with a `Twig.spec` file so you don’t have to deal with PyInstaller arguments manually.

To build a standalone executable:

```
pyinstaller Twig.spec
```

After the build finishes, your compiled browser will be inside:

```
dist/TWIG/
```

That folder contains everything needed to run TWIG.

---


## 🌱 About the User‑Agent

TWIG adds a simple identifier to the User‑Agent:

```
TWIG/<version>
```

---

## 🤝 Contributing

TWIGOsk is open‑source and easy to fork.  
Feel free to experiment, port it to other languages, or build your own edition.

The main repo only accepts changes from the core devs, but forks and pull requests are always welcome for discussion.

---

## 🐍 Python Version Notice

TWIGOsk currently requires a specific Python version for building.  
PyInstaller (the tool that bundles TWIGOsk into an executable) only supports certain Python releases, and newer versions tend to break compatibility until PyInstaller catches up.

For now, TWIGOsk builds correctly on:

```
Python 3.10 – 3.12
```

Python 3.13 and 3.14 are **not supported** by PyInstaller yet, so building TWIG/Twigosk on those versions will fail.

Running from source is usually fine on newer versions, but if you want to compile Twigosk into an executable, make sure you're using a supported Python version.

---

## 📄 License

Twigosk is open‑source under the MIT License.
