# web-arabic-ocr

Simple AI-generated web interface for Arabic OCR using a vision-to-sequence model.

This repository provides a small Flask app that accepts pasted or uploaded images
and returns OCR results for Arabic text.

Requirements
------------
- Python 3.10 or 3.11
- Conda (Miniconda or Anaconda)

Setup
-----
1. Open a terminal in the `arab-ocr-flask` directory.

2. Create the conda environment defined in `environment.yml` and activate it:

```bash
conda env create -f environment.yml
conda activate arab-ocr
```

3. Install PyTorch with CUDA support. The provided `setup_env.sh` installs the
	 latest available `pytorch-cuda` via conda. Run it with:

```bash
bash setup_env.sh
```

Running the app
---------------
Start the Flask app from the project folder:

```bash
python app.py
```

By default the server runs in debug mode on `http://127.0.0.1:5000/`.

Notes and troubleshooting
-------------------------
- Model download: the first run may download large model files. Ensure you have
	sufficient disk space and a reliable connection.
- GPU drivers: installing the latest `pytorch-cuda` via conda usually selects
	a recent CUDA build. If CUDA is not compatible with your system drivers,
	install a specific `pytorch-cuda` version (for example `pytorch-cuda=11.8`).
- Memory: running large models requires significant RAM and GPU memory. If
	you run out of memory, use a smaller model or run on CPU.
