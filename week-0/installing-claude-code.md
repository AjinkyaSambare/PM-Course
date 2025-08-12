# Installing Claude Code

## Prerequisites
- macOS, Linux, or Windows
- Node.js 18 or higher

## Step 1: Install Node.js

### macOS
1. **Using Homebrew (recommended):**
   ```bash
   brew install node
   ```
   
2. **Using the official installer:**
   - Download from [nodejs.org](https://nodejs.org/)
   - Choose the LTS version
   - Run the .pkg installer

### Windows
1. **Using the official installer:**
   - Download from [nodejs.org](https://nodejs.org/)
   - Choose the LTS version (.msi installer)
   - Run the installer (it will automatically add Node.js to PATH)
   
2. **Using Chocolatey (if installed):**
   ```powershell
   choco install nodejs
   ```

### Verify Node.js Installation
```bash
node --version
npm --version
```

## Step 2: Install Claude Code

### macOS / Linux

1. **Install Claude Code globally:**
   ```bash
   npm install -g @anthropic/claude-code
   ```

   If you encounter permission issues, try:
   ```powershell
   sudo npm install -g @anthropic/claude-code --force
   ```
2. **Authenticate:**
   ```bash
   claude login
   ```
   This will open your browser to authenticate with your Anthropic account.

3. **Verify Installation:**
   ```bash
   claude --version
   ```

### Windows

1. **Open PowerShell or Command Prompt as Administrator**

2. **Install Claude Code globally:**
   ```powershell
   npm install -g @anthropic/claude-code
   ```
   
   If you encounter permission issues, try:
   ```powershell
   npm install -g @anthropic/claude-code --force
   ```

3. **Authenticate:**
   ```powershell
   claude login
   ```
   This will open your browser to authenticate with your Anthropic account.

4. **Verify Installation:**
   ```powershell
   claude --version
   ```

### Troubleshooting Windows Installation
- If `claude` command is not recognized, add npm global directory to PATH:
  1. Run `npm config get prefix` to find the npm directory
  2. Add `<npm-directory>\bin` to your system PATH
  3. Restart your terminal

## Basic Usage

### Start Claude Code
```bash
claude
```


### Common Commands
- `claude help` - Show help information
- `claude logout` - Log out of your account
- `claude config` - Configure settings

## Keyboard Shortcuts
- `Ctrl+C` - Cancel current operation
- `Ctrl+D` - Exit Claude Code
- `Tab` - Autocomplete commands

## Getting Help
- Documentation: https://docs.anthropic.com/en/docs/claude-code
- Report issues: https://github.com/anthropics/claude-code/issues