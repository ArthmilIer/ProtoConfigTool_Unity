import os
import sys
import subprocess
from datetime import datetime
from importlib import import_module
from tools.utils import snake
from tools.csharp_partial_generator import generate_partial

def parse_time(v):
    if isinstance(v, datetime):
        return int(v.timestamp())
    return int(datetime.strptime(str(v), "%Y-%m-%d %H:%M:%S").timestamp())

def is_empty(v):
    return v is None or v == ""

def default_value(t, is_array):
    if is_array:
        return []
    if t == "uint32" or t == "int":
        return 0
    if t == "float":
        return 0
    if t == "bool":
        return False
    if t == "string":
        return ""
    return None

def convert_value(v, t, is_array, allow_empty=False):
    if allow_empty and is_empty(v):
        default = default_value(t, is_array)
        if default is not None:
            return default

    if is_array:
        if is_empty(v):
            return []
        return [convert_value(x, t, False) for x in str(v).split("|")]

    if t == "uint32" or t == "int":
        return int(v)
    if t == "float":
        return float(v)
    if t == "bool":
        return bool(int(v))
    if t == "string":
        return str(v)
    if t == "time":
        return parse_time(v)

    raise Exception(f"未知类型: {t}")

def format_cell_error(sheet, row_num, col_num, field, val, error):
    return (
        f"{sheet['excel']}.{sheet['sheet']} "
        f"第{row_num}行 第{col_num}列 字段'{field['name']}' "
        f"值'{val}'转换失败: {error}"
    )

def build_bytes(sheet, proto_out, bytes_out, partial_out):
    proto = os.path.join(proto_out, f"{sheet['excel']}.proto")
    proto_dir = os.path.abspath(os.path.dirname(proto))
    proto_file = os.path.basename(proto)

    subprocess.run([
        "protoc",
        f"-I{proto_dir}",
        f"--python_out={proto_dir}",
        proto_file
    ], cwd=proto_dir, check=True)

    if proto_dir not in sys.path:
        sys.path.insert(0, proto_dir)

    mod = import_module(f"{sheet['excel']}_pb2")
    cfg_cls = getattr(mod, f"{sheet['sheet']}Config")
    generate_partial(sheet["sheet"], partial_out)
    msg = cfg_cls()

    for row_num, row in enumerate(sheet["rows"], start=3):
        item = msg.items.add()
        for field in sheet["fields"]:
            col_idx = field["column"]
            val = row[col_idx] if col_idx < len(row) else None
            field_name = snake(field["name"])
            try:
                value = convert_value(
                    val,
                    field["type"],
                    field["array"],
                    allow_empty=col_idx != 0
                )
            except Exception as e:
                raise Exception(
                    format_cell_error(sheet, row_num, col_idx + 1, field, val, e)
                ) from None

            if field["array"]:
                getattr(item, field_name).extend(value)
            else:
                setattr(item, field_name, value)

    out_path = os.path.join(bytes_out, f"{sheet['sheet']}.bytes")
    os.makedirs(bytes_out, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(msg.SerializeToString())

    print(f"[BYTES] 生成 {out_path}")
