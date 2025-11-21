#!/usr/bin/env python3
"""
DeePTB Tutorial to Colab Converter (Clean Version)
使用外部安装脚本,使notebook更简洁
"""

import json
import sys
from pathlib import Path
from typing import Dict, List

# 简洁的安装单元格模板 - 只需调用安装脚本
INSTALL_CELLS_TEMPLATE = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 🚀 Installation & Setup\n",
            "\n",
            "This cell will automatically:\n",
            "- Detect your environment (Colab/Binder/Local)\n",
            "- Install DeePTB and all dependencies\n",
            "- Download tutorial data files\n",
            "\n",
            "> **💡 First-time setup takes 5-7 minutes. Please be patient!**"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Download and run the installation script\n",
            "import os\n",
            "from pathlib import Path\n",
            "\n",
            "# Check if we're in Colab/Binder\n",
            "IN_COLAB = 'google.colab' in __import__('sys').modules\n",
            "IN_BINDER = 'BINDER_SERVICE_HOST' in os.environ\n",
            "\n",
            "if IN_COLAB or IN_BINDER:\n",
            "    # Download the installation script\n",
            "    if not Path('install_deeptb.py').exists():\n",
            "        !wget -q https://raw.githubusercontent.com/DeePTB-Lab/Recipes/main/scripts/install_deeptb.py\n",
            "    \n",
            "    # Run the installation script\n",
            "    %run install_deeptb.py\n",
            "else:\n",
            "    print(\"💻 Running locally - please ensure DeePTB is installed\")\n",
            "    print(\"See: https://github.com/deepmodeling/DeePTB#installation\")"
        ]
    }
]


def create_badge_cell(notebook_name: str) -> Dict:
    """创建Colab徽章单元格"""
    colab_url = f"https://colab.research.google.com/github/DeePTB-Lab/Recipes/blob/main/deeptb_tutorials/v2.2/{notebook_name}"
    
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab_url})\n",
            "[![GitHub](https://img.shields.io/badge/GitHub-DeePTB-blue)](https://github.com/deepmodeling/DeePTB)\n",
            "\n",
            "---"
        ]
    }


def convert_notebook(input_path: Path, output_path: Path) -> bool:
    """
    转换notebook为Colab版本
    
    Args:
        input_path: 输入notebook路径
        output_path: 输出notebook路径
    
    Returns:
        bool: 转换是否成功
    """
    try:
        # 读取原始notebook
        print(f"📖 读取: {input_path.name}")
        with open(input_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # 创建徽章单元格
        badge_cell = create_badge_cell(output_path.name)
        
        # 组合所有单元格
        new_cells = [badge_cell] + INSTALL_CELLS_TEMPLATE + nb['cells']
        
        # 更新notebook
        nb['cells'] = new_cells
        
        # 保存新notebook
        print(f"💾 保存: {output_path.name}")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
        
        print(f"✅ 转换成功: {output_path.name}")
        return True
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("🔄 DeePTB Tutorial to Colab Converter (Clean Version)")
    print("=" * 70)
    print()
    
    # 定义要转换的tutorials
    tutorials_dir = Path("deeptb_tutorials/v2.2")
    
    tutorials = [
        "DeePTB_Tutorial_1.ipynb",
        "DeePTB_Tutorial_2.ipynb",
        "DeePTB_Tutorial_2_1.ipynb",
        "DeePTB_Tutorial_3.ipynb",
        "DeePTB_Tutorial_4.ipynb",
    ]
    
    # 检查目录是否存在
    if not tutorials_dir.exists():
        print(f"❌ 错误: 目录不存在 {tutorials_dir}")
        print("请在Recipes仓库根目录运行此脚本")
        sys.exit(1)
    
    # 转换每个tutorial
    success_count = 0
    for tutorial in tutorials:
        print(f"\n{'─' * 70}")
        input_path = tutorials_dir / tutorial
        output_name = tutorial.replace('.ipynb', '_Colab.ipynb')
        output_path = tutorials_dir / output_name
        
        if not input_path.exists():
            print(f"⚠️  跳过: {tutorial} (文件不存在)")
            continue
        
        if output_path.exists():
            response = input(f"⚠️  {output_name} 已存在,是否覆盖? (y/N): ")
            if response.lower() != 'y':
                print(f"⏭️  跳过: {tutorial}")
                continue
        
        if convert_notebook(input_path, output_path):
            success_count += 1
    
    # 总结
    print(f"\n{'=' * 70}")
    print(f"✅ 转换完成: {success_count}/{len(tutorials)} 个tutorials")
    print("=" * 70)
    print()
    print("📋 下一步:")
    print("1. 提交 scripts/install_deeptb.py 到 GitHub")
    print("2. 检查生成的 *_Colab.ipynb 文件")
    print("3. 在Colab中测试每个notebook")
    print()


if __name__ == "__main__":
    main()
