# ConfigTool 配置表规则

ConfigTool 用于把 Excel 配置表生成 `proto`、`bytes`、C# 协议代码和动态 partial 脚本。

## Excel 目录

- 默认读取 `./excel` 目录。
- 只处理 `.xlsx` 文件。
- 会忽略 Excel 临时文件，例如 `~$xxx.xlsx`。
- 每个 Excel 文件会生成一个同名 `.proto` 文件。
- 每个 Sheet 会生成一个同名 `.bytes` 文件。

## Sheet 结构

每个 Sheet 使用固定行规则：

| 行号 | 用途 |
| --- | --- |
| 第 1 行 | 字段定义 |
| 第 2 行 | 字段说明，工具不解析 |
| 第 3 行开始 | 配置数据 |

尾部全空行会被忽略，避免 Excel 格式残留导致误报。

## 字段定义

字段定义格式：

```text
字段名(类型)
```

示例：

```text
ID(uint32)
Name(string)
IsView(bool)
OpenTime(time)
Cost(float)
Param(array.string)
Remark(None)
```

字段名只能使用字母、数字、下划线，且需要符合正则：

```text
\w+
```

字段定义必须完整匹配 `字段名(类型)`，否则构建失败并输出 Sheet、行、列和错误字段。

备注列可以使用：

```text
字段名(None)
```

`None` 不区分大小写，例如 `None`、`none`、`NONE` 都有效。备注列只用于在 Excel 中保留说明或辅助信息，不会生成 proto 字段，也不会写入 bytes。备注列可以放在数据列中间，后续字段仍会按原始 Excel 列读取。

## 支持类型

| Excel 类型 | Proto 类型 | 配置值规则 |
| --- | --- | --- |
| `uint32` | `uint32` | 非负整数 |
| `int` | `int32` | 整数 |
| `float` | `float` | 浮点数 |
| `string` | `string` | 字符串 |
| `bool` | `bool` | `0` 或 `1` |
| `time` | `int64` | `yyyy-MM-dd HH:mm:ss` |

数组类型使用：

```text
array.基础类型
```

例如：

```text
array.string
array.uint32
array.float
```

数组值使用 `|` 分隔：

```text
1|2|3
hello|world
```

## 主键规则

- 每个 Sheet 的第一列是主键列。
- 主键不能为空。
- 主键值必须能转换为 `uint32`。
- 同一个 Sheet 内主键不能重复。
- 如果主键重复，构建会失败，并输出当前行和首次出现的行。

示例错误：

```text
Test.Sub 第5行 第1列 键'1'重复，已在第3行出现
```

## 空值规则

第一列主键不允许为空。

非主键字段允许为空，默认值如下：

| 类型 | 空值默认 |
| --- | --- |
| `uint32` | `0` |
| `int` | `0` |
| `float` | `0` |
| `bool` | `false`，等价配置值 `0` |
| `string` | `""` |
| `array.*` | 空数组 |

`time` 不允许为空。空 `time` 会构建失败，并输出具体表、行、列、字段和值。

## 错误输出

构建失败时会输出 `[ERROR]`，并尽量带上：

- Excel 文件名
- Sheet 名
- 行号
- 列号
- 字段名
- 原始值
- 具体错误原因

示例：

```text
[ERROR] Building.Sheet1 第3行 第4列 字段'OpenTime' 值''转换失败: time data '' does not match format '%Y-%m-%d %H:%M:%S'
```

未知字段类型会直接报错：

```text
Sheet 第1行 第1列 字段'Bad'类型'uint'不支持
```

## 生成内容

Python 构建会生成：

- `.proto`
- `.bytes`
- 动态 partial 脚本

bat 脚本还会调用 `protoc` 生成 C# 协议代码。

默认输出目录由命令行参数或 bat 脚本指定：

```text
--excel_dir
--proto_out
--bytes_out
--partial_out
```

## bat 构建规则

bat 脚本会先清理输出目录，再重新生成。

会清理的目录包括：

- proto 输出目录
- bytes 输出目录
- C# 输出目录
- partial 输出目录

partial 是动态生成脚本，构建时会被清理。需要额外逻辑时，应在项目中手动编写独立扩展脚本，不要写在生成目录内。

如果 Python 构建失败，bat 会立即停止。

如果 C# 生成失败，bat 也会立即停止，并输出失败的 proto 文件名。

## 注意事项

- Sheet 名会用于生成 Proto message、bytes 文件名和 partial 类名。
- 多个 Excel 或 Sheet 同名时，可能出现输出覆盖或 C# 类型冲突，需要通过命名设计规避。
- `bool` 当前只支持 `0` 和 `1`。
- `time` 当前只支持 `yyyy-MM-dd HH:mm:ss` 格式，或 Excel 日期时间单元格。
- 默认生成的 partial 索引逻辑使用 `Get(uint id)`；如果项目需要自定义索引或扩展逻辑，应在生成目录外自行维护。
