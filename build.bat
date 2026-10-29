@echo off

chcp 65001

setlocal enabledelayedexpansion

::Excel 目录
set EXCEL_DIR=E:\Project\ConfigTool\excel
::proto 目录
set PROTO_OUT=E:\Project\ConfigTool\proto
::bytes 目录
set BYTES_OUT=E:\Project\ConfigTool\bytes
::C# 目录
set CSHARP_OUT=E:\Project\ConfigTool\cs
::C# partial类目录
set PARTIAL_OUT=E:\Project\ConfigTool\partial

echo Excel 目录: %EXCEL_DIR%
echo Proto 输出: %PROTO_OUT%
echo Bytes 输出: %BYTES_OUT%
echo C# 目录: %CSHARP_OUT%
echo Partial 目录: %PARTIAL_OUT%
echo.

echo 开始清理缓存文件

echo 清理Proto输出目录

del /q "%PROTO_OUT%\*"

echo 清理Bytes输出目录

del /q "%BYTES_OUT%\*"

echo 清理 C# 输出目录

del /q "%CSHARP_OUT%\*"

echo 清理Partial输出目录

del /q "%PARTIAL_OUT%\*"

echo 清理完毕

python build.py ^
  --excel_dir "%EXCEL_DIR%" ^
  --proto_out "%PROTO_OUT%" ^
  --bytes_out "%BYTES_OUT%" ^
  --partial_out "%PARTIAL_OUT%"

if errorlevel 1 (
    echo [ERROR] Python build failed. Stop.
    pause
    exit /b 1
)

echo 生成完毕，开始解析
echo.

for %%f in (%PROTO_OUT%\*.proto) do (
    echo 生成 C#: %%~nxf
    protoc -I"%PROTO_OUT%" --csharp_out="%CSHARP_OUT%" "%%f"
    if errorlevel 1 (
        echo [ERROR] C# generation failed: %%~nxf
        pause
        exit /b 1
    )
)

echo 生成完毕
echo.

pause
