#!/usr/bin/env python3
"""
DeePTB Colab Installation Script
自动检测环境并安装DeePTB及其依赖
"""

import sys
import os
from pathlib import Path
import subprocess


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def detect_environment():
    """检测运行环境"""
    in_colab = 'google.colab' in sys.modules
    in_binder = 'BINDER_SERVICE_HOST' in os.environ
    in_local = not (in_colab or in_binder)
    
    print_section("🔍 环境检测")
    if in_colab:
        print("✅ 检测到 Google Colab 环境")
    elif in_binder:
        print("✅ 检测到 Binder 环境")
    else:
        print("✅ 检测到本地环境")
    
    return in_colab, in_binder, in_local


def check_deeptb_installed():
    """检查DeePTB是否已安装"""
    deeptb_installed = False
    deeptb_dir_exists = Path('DeePTB').exists()
    
    try:
        import dptb
        print(f"\n✅ DeePTB 已安装 (版本: {dptb.__version__})")
        deeptb_installed = True
    except ImportError:
        if deeptb_dir_exists:
            print("\n⚠️  DeePTB目录存在但未安装,将重新安装...")
        else:
            print("\n⚠️  DeePTB 未安装,开始安装流程...")
    
    return deeptb_installed, deeptb_dir_exists


def detect_cuda_version(in_colab):
    """检测CUDA版本"""
    cuda_version = "cpu"  # 默认使用CPU版本
    
    if in_colab:
        # 方法1: 尝试使用nvidia-smi检测(最可靠)
        try:
            result = subprocess.run(['nvidia-smi'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                cuda_version = "cu121"
                print("🎮 检测到GPU环境(nvidia-smi),使用 CUDA 12.1")
            else:
                print("💻 未检测到GPU,使用 CPU 版本")
        except:
            # 方法2: 如果nvidia-smi失败,尝试检查torch(Colab预装)
            print("⚠️  nvidia-smi 检测失败,尝试通过PyTorch检测...")
            try:
                import torch
                if torch.cuda.is_available():
                    cuda_ver = torch.version.cuda
                    if cuda_ver:
                        cuda_version = f"cu{cuda_ver.replace('.', '')}"
                        print(f"🎮 检测到GPU环境(PyTorch),使用 CUDA {cuda_version}")
                    else:
                        cuda_version = "cu121"
                        print("🎮 PyTorch可用,使用默认 CUDA 12.1")
                else:
                    print("💻 PyTorch未检测到GPU,使用 CPU 版本")
            except ImportError:
                cuda_version = "cu121"
                print("⚠️  PyTorch未安装,使用Colab默认 CUDA 12.1")
            except Exception as e:
                cuda_version = "cu121"
                print(f"⚠️  CUDA检测异常: {e},使用默认 CUDA 12.1")
    else:
        print("💻 非Colab环境,使用 CPU 版本")
    
    return cuda_version


def create_dptb_wrapper():
    """创建 dptb 命令包装器"""
    try:
        wrapper_path = "/usr/local/bin/dptb"
        
        # 确保使用绝对路径
        deeptb_root = os.path.abspath((os.getcwd()))
        venv_bin = os.path.join(deeptb_root, ".venv", "bin")
        dptb_exec = os.path.join(venv_bin, "dptb")
        
        # 验证路径是绝对路径
        if not os.path.isabs(dptb_exec):
            raise ValueError(f"路径不是绝对路径: {dptb_exec}")
        
        print(f"🔍 DeePTB 根目录: {deeptb_root}")
        print(f"🔍 Venv 可执行路径: {dptb_exec}")
        
        # 检查可执行文件是否存在
        if not os.path.exists(dptb_exec):
            print(f"⚠️  未找到可执行文件: {dptb_exec}")
            print("   尝试使用 python -m dptb 替代...")
            python_exec = os.path.join(venv_bin, "python")
            if not os.path.exists(python_exec):
                raise FileNotFoundError(f"Python 解释器也不存在: {python_exec}")
            dptb_exec = f'{python_exec} -m dptb'
            
        # 关键修复: 直接执行 venv 中的二进制文件，保留当前工作目录 (CWD)
        # 这样用户在任意目录下运行 !dptb 都能正确找到相对路径的文件
        script_content = f"""#!/bin/bash
exec {dptb_exec} "$@"
"""
        with open("dptb_wrapper", "w") as f:
            f.write(script_content)
            
        os.system(f"chmod +x dptb_wrapper")
        ret = os.system(f"mv dptb_wrapper {wrapper_path}")
        
        if ret != 0:
            print(f"⚠️  移动 wrapper 到 {wrapper_path} 失败，可能需要 sudo 权限")
            return False
            
        print(f"✅ 创建命令包装器: {wrapper_path} -> {dptb_exec}")
        return True
    except Exception as e:
        print(f"⚠️  创建命令包装器失败: {e}")
        return False

def inject_venv_path():
    """将 venv 的包路径注入到系统环境"""
    try:
        # 获取 venv 的 site-packages 路径
        # 我们通过运行 venv 里的 python 来获取
        result = subprocess.run(
            ["uv", "run", "python", "-c", "import site; print(site.getsitepackages()[0])"], 
            capture_output=True, text=True, cwd="DeePTB"
        )
        
        if result.returncode == 0:
            venv_site_packages = result.stdout.strip()
            print(f"🔍 Venv 库路径: {venv_site_packages}")
            
            # 1. 立即添加到当前进程 (用于验证)
            if venv_site_packages not in sys.path:
                sys.path.insert(0, venv_site_packages)
            
            # 2. 添加到系统 site-packages (通过 .pth 文件持久化)
            # 找到系统 site-packages
            import site
            system_site = site.getsitepackages()[0]
            pth_file = Path(system_site) / "deeptb_venv.pth"
            
            with open(pth_file, "w") as f:
                f.write(venv_site_packages + "\n")
                
            print(f"✅ 注入路径到系统: {pth_file}")
            return True
        else:
            print(f"⚠️  获取 venv 路径失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"⚠️  路径注入失败: {e}")
        return False

def install_deeptb(cuda_version):
    """安装DeePTB"""
    print_section("📦 开始安装 DeePTB")
    
    # 步骤1: 安装UV
    print("\n[1/5] 安装 UV 包管理器...")
    os.system("pip install -q uv")
    print("✅ UV 安装完成")
    
    # 步骤2: 克隆DeePTB仓库
    print("\n[2/5] 克隆 DeePTB 仓库...")
    if not Path('DeePTB').exists():
        os.system("git clone -q https://github.com/deepmodeling/DeePTB.git")
        print("✅ 仓库克隆完成")
    else:
        print("✅ DeePTB 仓库已存在")
    
    # 步骤3: 使用UV安装DeePTB (纯 uv sync 模式)
    print("\n[3/5] 使用 UV 安装 DeePTB 及依赖...")
    print("⏳ 这可能需要几分钟,请耐心等待...")
    print("   正在安装:")
    print("   - PyTorch")
    print("   - torch_scatter")
    print("   - torch_geometric")
    print("   - e3nn")
    print("   - 其他依赖")
    
    # 构建find-links URL
    find_links_url = f"https://data.pyg.org/whl/torch-2.5.0+{cuda_version}.html"
    print(f"📦 使用 PyG wheel: {find_links_url}")
    
    # 切换到DeePTB目录并安装
    original_dir = os.getcwd()
    os.chdir('DeePTB')
    
    try:
        # 使用标准的 uv sync
        print("🚀 执行 uv sync...")
        ret = os.system(f"uv sync --find-links {find_links_url}")
        
        if ret != 0:
            raise Exception("uv sync failed")
            
        print("✅ DeePTB 依赖安装完成 (Virtual Environment)")
        
        # 关键步骤: 桥接 venv 和 系统环境
        print("\n[3.5/5] 配置环境桥接...")
        create_dptb_wrapper()
        inject_venv_path()
        
    except Exception as e:
        print(f"❌ UV安装失败: {e}")
        print("\n尝试备用安装方法 (Standard PIP)...")
        os.system(f"pip install torch-scatter -f {find_links_url}")
        os.system("pip install -e .")
    
    # 步骤4: 验证安装
    print("\n[4/5] 验证安装...")
    
    # 刷新导入缓存
    import site
    import importlib
    site.main()
    importlib.invalidate_caches()
    
    # 验证命令
    ret = os.system("dptb --version")
    if ret != 0:
        print("⚠️  'dptb' 命令验证失败 (Wrapper可能未生效)")
        # 尝试直接调用
        os.system("uv run dptb --version")
    else:
        print("✅ 命令行工具验证成功")
        
    # 验证导入
    try:
        import dptb
        print(f"✅ Python 导入验证成功: {dptb.__version__}")
    except ImportError:
        print("⚠️  Python 导入失败 (路径注入可能未生效)")
        print("   请尝试重启 Runtime")
    
    # 返回原目录
    os.chdir(original_dir)
    
    print_section("🎉 安装完成!")


def download_tutorial_data(in_colab, in_binder):
    """下载教程数据"""
    if in_colab or in_binder:
        print("\n📥 下载教程数据文件...")
        
        if not Path('Recipes').exists():
            os.system("git clone -q https://github.com/DeePTB-Lab/Recipes.git")
            print("✅ 数据文件下载完成")
        else:
            print("✅ Recipes 仓库已存在")
        
        # 切换到tutorial目录
        target_dir = '/content/Recipes/deeptb_tutorials/v2.2' if in_colab else 'Recipes/deeptb_tutorials/v2.2'
        if not os.getcwd().endswith('v2.2'):
            os.chdir(target_dir)
        print(f"📂 当前工作目录: {os.getcwd()}")
    else:
        print("\n💻 本地环境,使用现有数据文件")
        print(f"📂 当前工作目录: {os.getcwd()}")


def main():
    """主函数"""
    # 检测环境
    in_colab, in_binder, in_local = detect_environment()
    
    # 检查是否已安装
    deeptb_installed, deeptb_dir_exists = check_deeptb_installed()
    
    # 在线环境需要安装
    if (in_colab or in_binder) and not deeptb_installed:
        # 尝试设置缓存 (仅Colab)          
        # 检测CUDA版本
        cuda_version = detect_cuda_version(in_colab)
        # 安装DeePTB
        install_deeptb(cuda_version)
        
        # 下载数据
        download_tutorial_data(in_colab, in_binder)
        
    elif in_local and not deeptb_installed:
        print_section("⚠️  本地环境检测")
        print("请在本地环境中手动安装 DeePTB:")
        print("")
        print("  git clone https://github.com/deepmodeling/DeePTB.git")
        print("  cd DeePTB")
        print("  uv sync")
        print("")
        print("详细安装说明: https://github.com/deepmodeling/DeePTB#installation")
        print("=" * 60)
    else:
        # 已安装,只下载数据
        download_tutorial_data(in_colab, in_binder)


if __name__ == "__main__":
    main()
