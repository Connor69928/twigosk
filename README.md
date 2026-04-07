# 🌿 TWIG Browser
TWIG is the open‑source browser core used inside ConSurf (and now Sneakon too).  
It’s lightweight, readable, and designed so anyone can build on top of it without fighting the codebase.

TWIG is intentionally minimal — no plugins, no custom protocol, no extra layers.  
Just a clean PyQt5 + QtWebEngine browser that you can run, fork, or turn into your own flavour.

---

## 📦 Requirements

TWIG uses Python and PyQt5.  
To build or run it, you’ll need the following modules:

- PyQt5  
- PyQtWebEngine  
- PyInstaller (for building)

After 1.3, you can install everything with:

```
pip install -r requirements.txt
```

For now, you need:

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

## 🖼️ Icon Notice

The current `icon.ico` is **just a placeholder**.  
Right now it uses the **ConSurf logo**, because TWIG doesn’t have its own branding yet.

TWIG will get its own proper logo in **version 1.3** (matching ConSurf’s version numbering).

---

## 🌱 About the User‑Agent

TWIG adds a simple identifier to the User‑Agent:

```
TWIG/<version>
```

This keeps the engine honest and lets downstream browsers (like Sneakon or ConSurf) add their own tags on top.

---

## 🤝 Contributing

TWIG is open‑source and easy to fork.  
Feel free to experiment, port it to other languages, or build your own edition.

The main repo only accepts changes from the core devs, but forks and pull requests are always welcome for discussion.

---

## 📄 License

TWIG is open‑source under the MIT License.
