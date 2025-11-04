#!/usr/bin/env bash
set -euo pipefail

# Script to create the `arab-ocr` conda environment and install the latest PyTorch+CUDA
# Usage: bash setup_env.sh
# Note: this script assumes `conda` is installed and available in PATH.

ENV_FILE="environment.yml"
ENV_NAME="arab-ocr"

if ! command -v conda >/dev/null 2>&1; then
  echo "conda not found in PATH. Install Miniconda/Anaconda first: https://docs.conda.io/en/latest/miniconda.html"
  exit 1
fi

# Create environment from YAML (will overwrite if exists)
conda env create -f "$ENV_FILE" || true

# Activate conda in this script (works for most installations)
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME"

# Install the latest PyTorch + CUDA packages (versionless to get the newest available)
# This will pick the newest pytorch-cuda available in the channels.
conda install -y -c pytorch -c nvidia pytorch torchvision torchaudio pytorch-cuda

# Ensure pip-side packages are installed/updated
pip install --upgrade pip
pip install --upgrade transformers openai arabic-reshaper python-bidi accelerate safetensors sentencepiece

# Quick verification
python - <<'PY'
import sys
try:
    import torch
    print('torch', torch.__version__)
    print('CUDA available:', torch.cuda.is_available())
except Exception as e:
    print('Verification failed:', e, file=sys.stderr)
    sys.exit(2)
PY

echo "Environment '$ENV_NAME' created and PyTorch installed (latest pytorch-cuda)."