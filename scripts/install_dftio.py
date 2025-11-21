#!/usr/bin/env python3
"""
DFTIO Colab Installation Script
自动安装DFTIO库
"""

import sys
import os
from pathlib import Path


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def check_dftio_installed():
    """检查DFTIO是否已安装"""
    try:
        import dftio
        print(f"\n✅ DFTIO 已安装 (版本: {dftio.__version__})")
        return True
    except ImportError:
        print("\n⚠️  DFTIO 未安装,开始安装流程...")
        return False


def install_dftio():
    """安装DFTIO"""
    print_section("📦 开始安装 DFTIO")
    
    # 步骤1: 克隆DFTIO仓库
    print("\n[1/2] 克隆 DFTIO 仓库...")
    if not Path('dftio').exists():
        os.system("git clone -q https://github.com/deepmodeling/dftio.git")
        print("✅ 仓库克隆完成")
    else:
        print("✅ DFTIO 仓库已存在")
    
    # 步骤2: 安装DFTIO
    print("\n[2/2] 安装 DFTIO...")
    original_dir = os.getcwd()
    os.chdir('dftio')
    
    try:
        ret = os.system("pip install -q -e .")
        if ret != 0:
            raise Exception("pip install failed")
        print("✅ DFTIO 安装完成")
    except Exception as e:
        print(f"❌ DFTIO 安装失败: {e}")
        sys.exit(1)
    finally:
        os.chdir(original_dir)
    
    # 步骤3: 验证安装
    print("\n[3/3] 验证安装...")
    try:
        import dftio
        print(f"✅ Python 导入验证成功: {dftio.__version__}")
    except ImportError:
        print("⚠️  Python 导入失败")
        print("   请尝试重启 Runtime")
    
    print_section("🎉 DFTIO 安装完成!")


def main():
    """主函数"""
    # 检查是否已安装
    if not check_dftio_installed():
        install_dftio()
    else:
        print("✅ DFTIO 已安装,跳过安装步骤")


if __name__ == "__main__":
    main()
