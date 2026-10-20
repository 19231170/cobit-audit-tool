import os
import subprocess
import sys

def build():
    print("Mempersiapkan build COBIT Audit Tool (.exe)...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "COBIT-Audit-Tool",
        "--add-data", "app;app",
        "main.py"
    ]
    print(f"Menjalankan perintah: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("\n=======================================================")
        print("Build berhasil! File aplikasi berada di folder:")
        print(os.path.abspath("dist/COBIT-Audit-Tool/COBIT-Audit-Tool.exe"))
        print("=======================================================")
    else:
        print("Build gagal dengan kode error:", result.returncode)

if __name__ == "__main__":
    build()
