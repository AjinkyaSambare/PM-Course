# Python Installation Guide

This guide will help you install Python on Windows and macOS.

## macOS Installation

### Method 1: Using Homebrew (Recommended)

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**:
   ```bash
   brew install python3
   ```

3. **Verify Installation**:
   ```bash
   python3 --version
   pip3 --version
   ```

### Method 2: Download from Python.org

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Click on the latest Python release for macOS
3. Download the macOS installer (.pkg file)
4. Double-click the downloaded file and follow the installation wizard
5. **Important**: During installation, make sure to check "Add Python to PATH"

### Method 3: Using pyenv (For Multiple Python Versions)

1. **Install pyenv**:
   ```bash
   brew install pyenv
   ```

2. **Add pyenv to your shell**:
   ```bash
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```

3. **Restart your terminal or run**:
   ```bash
   source ~/.zshrc
   ```

4. **Install Python**:
   ```bash
   pyenv install 3.12.0  # Replace with desired version
   pyenv global 3.12.0
   ```

## Windows Installation

### Method 1: Microsoft Store (Windows 10/11 - Easiest)

1. Open Microsoft Store
2. Search for "Python"
3. Select the latest Python version (e.g., Python 3.12)
4. Click "Get" or "Install"
5. Python will be automatically added to PATH

### Method 2: Download from Python.org (Recommended for Full Control)

1. Visit [python.org/downloads](https://www.python.org/downloads/)
2. Click on the latest Python release for Windows
3. Download the Windows installer (64-bit recommended):
   - For 64-bit systems: "Windows installer (64-bit)"
   - For 32-bit systems: "Windows installer (32-bit)"
4. Run the downloaded installer
5. **IMPORTANT**: Check the box "Add Python to PATH" at the bottom of the first screen
6. Click "Install Now" for default installation or "Customize installation" for advanced options
7. Wait for installation to complete



## Post-Installation Verification

### For Both macOS and Windows:

1. **Open a new terminal/command prompt**

2. **Check Python version**:
   - macOS: `python3 --version`
   - Windows: `python --version`

3. **Check pip (Python package manager)**:
   - macOS: `pip3 --version`
   - Windows: `pip --version`

4. **Test Python**:
   ```python
   python3  # or just 'python' on Windows
   >>> print("Hello, Python!")
   >>> exit()
   ```


## Troubleshooting

### macOS Issues:

1. **"python" command not found**: Use `python3` instead
2. **SSL Certificate errors**: Run `pip3 install --upgrade certifi`
3. **Permission errors**: Use `pip3 install --user <package>`

### Windows Issues:

1. **"python" not recognized**: 
   - Ensure Python was added to PATH during installation
   - Manually add Python to PATH through System Environment Variables

2. **pip not working**:
   ```powershell
   python -m ensurepip --upgrade
   ```

3. **Scripts not running**: 
   - Run PowerShell as Administrator
   - Execute: `Set-ExecutionPolicy RemoteSigned`

## Recommended IDE/Editors

1. **Visual Studio Code**: Free, lightweight, excellent Python support
2. **PyCharm**: Professional IDE with free Community Edition
3. **Jupyter Notebook**: Great for data science and learning
   ```bash
   pip install notebook
   jupyter notebook
   ```

## Next Steps

1. Install essential packages:
   ```bash
   pip install numpy pandas matplotlib requests
   ```

2. Learn Python basics with interactive tutorials:
   - [Python.org Tutorial](https://docs.python.org/3/tutorial/)
   - [W3Schools Python](https://www.w3schools.com/python/)
   - [Real Python](https://realpython.com/)

3. Practice with coding challenges:
   - [LeetCode](https://leetcode.com/)
   - [HackerRank](https://www.hackerrank.com/domains/python)
   - [Codewars](https://www.codewars.com/)