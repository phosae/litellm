# LiteLLM Proxy Debug Guide

This guide explains how to debug the LiteLLM proxy using VS Code.

## VS Code Debug Configurations

I've created several debug configurations in `.vscode/launch.json` that you can use:

### 1. Debug LiteLLM Proxy (admin.yaml)
- **Purpose**: Run the full LiteLLM proxy with your admin.yaml config
- **Use case**: Debug the complete proxy startup and operation
- **Command**: `litellm --config zenx/admin.yaml --debug --detailed_debug`

### 2. Debug LiteLLM Module (admin.yaml)
- **Purpose**: Run the LiteLLM module directly (better for debugging)
- **Use case**: Debug the proxy CLI module with better breakpoint support
- **Command**: `python -m litellm.proxy.proxy_cli --config zenx/admin.yaml --debug --detailed_debug`

### 3. Debug LiteLLM Proxy (admin.yaml) - Local
- **Purpose**: Run with local debugging flag
- **Use case**: Debug local development issues
- **Command**: `litellm --config zenx/admin.yaml --debug --detailed_debug --local`

### 4. Debug LiteLLM Proxy (admin.yaml) - Skip Server
- **Purpose**: Run setup without starting the server
- **Use case**: Debug configuration loading and database setup
- **Command**: `litellm --config zenx/admin.yaml --debug --detailed_debug --skip_server_startup`

### 5. Debug LiteLLM Proxy (admin.yaml) - Health Check
- **Purpose**: Test health of all models in config
- **Use case**: Debug model connectivity and configuration
- **Command**: `litellm --config zenx/admin.yaml --debug --detailed_debug --health`

### 6. Debug LiteLLM Components
- **Purpose**: Run the custom debug script
- **Use case**: Debug specific components (config loading, database, models)
- **Command**: `python zenx/debug_litellm.py`

## How to Use

1. **Open VS Code** in the project root directory
2. **Go to Run and Debug** (Ctrl+Shift+D or Cmd+Shift+D)
3. **Select a debug configuration** from the dropdown
4. **Set breakpoints** in the code you want to debug
5. **Press F5** or click the green play button to start debugging

## Setting Breakpoints

You can set breakpoints in these key files:
- `litellm/proxy/proxy_cli.py` - Main CLI entry point
- `litellm/proxy/proxy_server.py` - Server configuration and setup
- `litellm/proxy/db/prisma_client.py` - Database operations
- `zenx/debug_litellm.py` - Custom debug script

## Environment Variables

The debug configurations automatically set:
- `TZ=Asia/Shanghai` - Fixes timezone conflicts
- `PYTHONPATH=${workspaceFolder}` - Ensures proper module imports

## Common Issues and Solutions

### 1. Timezone Error
```
zoneinfo._common.ZoneInfoNotFoundError: Multiple conflicting time zone configurations found
```
**Solution**: The debug configurations automatically set `TZ=Asia/Shanghai`

### 2. Database Connection Error
```
Environment variable not found: DATABASE_URL
```
**Solution**: Make sure your `zenx/admin.yaml` has the correct `database_url` setting

### 3. Import Errors
```
ModuleNotFoundError: No module named 'litellm'
```
**Solution**: Make sure you're using the Poetry virtual environment and `PYTHONPATH` is set correctly

## Debug Tips

1. **Start with "Skip Server"** configuration to debug setup issues
2. **Use "Health Check"** to test model connectivity
3. **Use the custom debug script** to isolate specific components
4. **Set breakpoints** in the `run_server` function in `proxy_cli.py` for startup debugging
5. **Check the console output** for detailed debug information

## Configuration File

Your `zenx/admin.yaml` contains:
- 2 models: `cd-st-4-20250514-conf` and `429-conf`
- Database URL: `postgresql://postgres:root@host.orb.internal:5432/litellm`
- Master key: `sk-1234`

Make sure the database is accessible and the models are properly configured. 