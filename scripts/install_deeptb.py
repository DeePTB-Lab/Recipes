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


def setup_drive_cache():
    """设置Google Drive缓存"""
    try:
        # 检查是否在Colab
        if 'google.colab' not in sys.modules:
            return False, None

        print_section("💾 Google Drive 缓存设置")
        print("是否挂载 Google Drive 以缓存安装文件？(推荐)")
        print("这样可以显著加快下次运行速度 (5-7分钟 -> 30秒)")
        
        # 简单的超时输入或默认尝试挂载
        # 在Colab中,drive.mount会弹出授权窗口
        from google.colab import drive
        drive.mount('/content/drive')
        
        cache_root = Path('/content/drive/MyDrive/DeePTB_Colab_Cache')
        cache_root.mkdir(parents=True, exist_ok=True)
        
        # 1. 配置 UV Cache
        uv_cache = cache_root / 'uv_cache'
        uv_cache.mkdir(exist_ok=True)
        os.environ['UV_CACHE_DIR'] = str(uv_cache)
        print(f"✅ UV Cache 已配置: {uv_cache}")
        
        # 2. 配置 Repo Cache
        repo_cache = cache_root / 'DeePTB_Repo'
        
        return True, repo_cache
        
    except Exception as e:
        print(f"⚠️  Google Drive 挂载跳过或失败: {e}")
        print("   将使用临时环境运行 (无缓存)...")
        return False, None


def install_deeptb(cuda_version, repo_cache=None):
    """安装DeePTB"""
    print_section("📦 开始安装 DeePTB")
    
    # 步骤1: 安装UV
    print("\n[1/5] 安装 UV 包管理器...")
    os.system("pip install -q uv")
    print("✅ UV 安装完成")
    
    # 步骤2: 克隆DeePTB仓库
    print("\n[2/5] 克隆 DeePTB 仓库...")
    
    # 检查是否有缓存的Repo
    use_cached_repo = False
    if repo_cache and repo_cache.exists():
        print(f"📦 发现缓存的仓库: {repo_cache}")
        try:
            # 如果本地不存在,从缓存复制
            if not Path('DeePTB').exists():
                print("   正在从缓存恢复仓库...")
                import shutil
                shutil.copytree(repo_cache, 'DeePTB')
                print("✅ 从缓存恢复完成")
            use_cached_repo = True
        except Exception as e:
            print(f"⚠️  恢复缓存失败: {e}, 将重新克隆")
            
    if not Path('DeePTB').exists():
        os.system("git clone -q https://github.com/deepmodeling/DeePTB.git")
        print("✅ 仓库克隆完成")
    else:
        print("✅ DeePTB 仓库已存在")
        
    # 如果使用了缓存且成功安装,更新缓存
    if repo_cache and not use_cached_repo and Path('DeePTB').exists():
        try:
            print("💾 更新仓库缓存...")
            import shutil
            if repo_cache.exists():
                shutil.rmtree(repo_cache)
            shutil.copytree('DeePTB', repo_cache, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))
            print("✅ 仓库缓存已更新")
        except Exception as e:
            print(f"⚠️  更新缓存失败: {e}")
    
    # 步骤3: 使用UV安装DeePTB
    print("\n[3/5] 使用 UV 安装 DeePTB 及依赖...")
    if os.environ.get('UV_CACHE_DIR'):
        print(f"🚀 使用缓存加速: {os.environ['UV_CACHE_DIR']}")
    else:
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
        os.system(f"uv sync --find-links {find_links_url}")
        print("✅ DeePTB 依赖安装完成")
    except Exception as e:
        print(f"❌ UV安装失败: {e}")
        print("\n尝试备用安装方法...")
        os.system(f"pip install torch-scatter -f {find_links_url}")
        os.system("pip install -e .")
    
    # 步骤4: 安装DeePTB到系统环境
    print("\n[4/5] 安装 DeePTB 到系统环境...")
    try:
        os.system("uv pip install -e .")
        print("✅ DeePTB 已安装到系统环境")
    except:
        print("⚠️  使用 uv run 模式")
    
    # 步骤5: 验证安装
    print("\n[5/5] 验证安装...")
    ret = os.system("dptb --version 2>/dev/null")
    if ret != 0:
        ret = os.system("uv run dptb --version 2>/dev/null")
        if ret != 0:
            try:
                sys.path.insert(0, os.getcwd())
                import dptb
                print(f"✅ DeePTB 版本: {dptb.__version__}")
            except:
                print("⚠️  验证失败,但安装可能成功")
    
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
        repo_cache = None
        if in_colab:
            use_cache, repo_cache = setup_drive_cache()
            
        # 检测CUDA版本
        cuda_version = detect_cuda_version(in_colab)
        
        # 安装DeePTB
        install_deeptb(cuda_version, repo_cache)
        
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
