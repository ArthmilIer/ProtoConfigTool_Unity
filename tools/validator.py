def is_empty(v):
    return v is None or v == ""

def validate_sheet(sheet):
    keys = {}

    for row_num, row in enumerate(sheet["rows"], start=3):
        key_value = row[0] if row else None
        if is_empty(key_value):
            raise Exception(
                f"{sheet['excel']}.{sheet['sheet']} 第{row_num}行 第1列 主键不能为空"
            )

        try:
            key = int(key_value)
        except (TypeError, ValueError):
            continue

        if key in keys:
            raise Exception(
                f"{sheet['excel']}.{sheet['sheet']} 第{row_num}行 第1列 "
                f"键'{key_value}'重复，已在第{keys[key]}行出现"
            )

        keys[key] = row_num
