# Installing Claude Code

## Prerequisites
- macOS, Linux, or Windows
- Node.js 18 or higher

## Installation Steps

### 1. Install via npm
```bash
npm install -g @anthropic/claude-code
```

### 2. Authenticate
```bash
claude login
```
This will open your browser to authenticate with your Anthropic account.

### 3. Verify Installation
```bash
claude --version
```

## Basic Usage

### Start Claude Code
```bash
claude
```

### Open a specific directory
```bash
claude /path/to/your/project
```

### Use with specific model
```bash
claude --model claude-3-opus-20240229
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