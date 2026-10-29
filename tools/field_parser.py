import re

FIELD_RE = re.compile(r"^(\w+)\(([\w\.]+)\)$")
ALLOWED_TYPES = {"uint32", "int", "float", "string", "bool", "time"}

def parse_fields(header_row):
    fields = []

    for cell in header_row:
        if not cell.value:
            continue

        value = str(cell.value)
        m = FIELD_RE.match(value)
        if not m:
            raise Exception(
                f"{cell.parent.title} 第{cell.row}行 第{cell.column}列 字段定义错误: {value}"
            )

        name, type_str = m.groups()
        if type_str.lower() == "none":
            continue

        is_array = type_str.startswith("array.")
        base_type = type_str.replace("array.", "", 1)
        if base_type not in ALLOWED_TYPES:
            raise Exception(
                f"{cell.parent.title} 第{cell.row}行 第{cell.column}列 "
                f"字段'{name}'类型'{type_str}'不支持"
            )

        fields.append({
            "name": name,
            "type": base_type,
            "array": is_array,
            "column": cell.column - 1
        })

    return fields
