# DeePTB Recipes 📚

This repository contains tutorials and examples for [DeePTB](https://github.com/deepmodeling/DeePTB) - a deep learning package for accelerating *ab initio* electronic structure simulations.

## 🚀 Quick Start

All tutorials are available in two versions:
- **Standard Jupyter Notebooks**: For local execution
- **Google Colab Notebooks**: For online execution (no installation required!)

## 📖 DeePTB Tutorials (v2.2)

### Tutorial 1: DeePTB-SK Baseline Model
Learn how to use built-in base models to plot band structures for given crystal structures.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DeePTB-Lab/Recipes/blob/main/deeptb_tutorials/v2.2/DeePTB_Tutorial_1_Colab.ipynb)
[![Local Notebook](https://img.shields.io/badge/Jupyter-Local-orange?logo=jupyter)](deeptb_tutorials/v2.2/DeePTB_Tutorial_1.ipynb)

---

### Tutorial 2: Training DeePTB-SK Model
Learn how to train a DeePTB-SK model from scratch using first-principles data.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DeePTB-Lab/Recipes/blob/main/deeptb_tutorials/v2.2/DeePTB_Tutorial_2_Colab.ipynb)
[![Local Notebook](https://img.shields.io/badge/Jupyter-Local-orange?logo=jupyter)](deeptb_tutorials/v2.2/DeePTB_Tutorial_2.ipynb)

---

### Tutorial 2.1: Advanced DeePTB-SK Training
Advanced training techniques and optimization strategies for DeePTB-SK models.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DeePTB-Lab/Recipes/blob/main/deeptb_tutorials/v2.2/DeePTB_Tutorial_2_1_Colab.ipynb)
[![Local Notebook](https://img.shields.io/badge/Jupyter-Local-orange?logo=jupyter)](deeptb_tutorials/v2.2/DeePTB_Tutorial_2_1.ipynb)

---

### Tutorial 3: DeePTB-E3 Model
Learn how to use E3-equivariant neural networks for representing quantum operators.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DeePTB-Lab/Recipes/blob/main/deeptb_tutorials/v2.2/DeePTB_Tutorial_3_Colab.ipynb)
[![Local Notebook](https://img.shields.io/badge/Jupyter-Local-orange?logo=jupyter)](deeptb_tutorials/v2.2/DeePTB_Tutorial_3.ipynb)

---

### Tutorial 4: Advanced Applications
Advanced applications and use cases of DeePTB models.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DeePTB-Lab/Recipes/blob/main/deeptb_tutorials/v2.2/DeePTB_Tutorial_4_Colab.ipynb)
[![Local Notebook](https://img.shields.io/badge/Jupyter-Local-orange?logo=jupyter)](deeptb_tutorials/v2.2/DeePTB_Tutorial_4.ipynb)

---

## 💻 Running Locally

### Prerequisites
- Python 3.10+
- [UV package manager](https://github.com/astral-sh/uv) (recommended)

### Installation

```bash
# Clone DeePTB repository
git clone https://github.com/deepmodeling/DeePTB.git
cd DeePTB

# Install using UV
uv sync

# Or install using pip
pip install -e .
```

### Run Tutorials

```bash
# Clone this repository
git clone https://github.com/DeePTB-Lab/Recipes.git
cd Recipes/deeptb_tutorials/v2.2

# Launch Jupyter
jupyter notebook
```

## ☁️ Running on Google Colab

Simply click the "Open in Colab" badge above any tutorial! The Colab version will:
- ✅ Automatically detect your environment (GPU/CPU)
- ✅ Install DeePTB and all dependencies
- ✅ Download required data files
- ✅ Ready to run in 5-7 minutes

> **💡 Tip**: First-time setup takes 5-7 minutes. Subsequent runs will be faster if you keep the runtime alive.

## 📦 What's Included

- **Tutorials**: Step-by-step guides for using DeePTB
- **Data**: Example datasets for training and testing
- **Scripts**: Utility scripts for data processing and conversion

## 🔧 Technical Details

### Colab Setup Features
- Automatic environment detection (Colab/Binder/Local)
- Smart CUDA version detection (nvidia-smi → torch → default)
- Fallback installation methods (UV → pip)
- Progress indicators and detailed logging
- Support for repeated execution

### Installation Flow
1. Environment detection
2. UV package manager installation
3. DeePTB repository cloning
4. Dependency installation (PyTorch, torch_scatter, etc.)
5. Tutorial data download
6. Installation verification

## 📚 Documentation

- [DeePTB Documentation](https://deeptb.readthedocs.io/)
- [DeePTB GitHub](https://github.com/deepmodeling/DeePTB)
- [Installation Guide](COLAB_SETUP_GUIDE.md)
- [Troubleshooting](TEST_COLAB.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the LGPL-3.0 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- DeePTB development team
- DeepModeling community
- All contributors to this repository

---

**Author**: Gu, Qiangqiang (顾强强)  
**Email**: guqq@ustc.edu.cn  
**Date**: 2025-11-21  
**Version**: v2.2
