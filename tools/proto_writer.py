import os
from tools.utils import snake

TYPE_MAP = {
    "uint32": "uint32",
    "int": "int32",
    "float": "float",
    "string": "string",
    "bool": "bool",
    "time": "int64",
}

def generate_proto(excel, proto_out):
    proto_path = os.path.join(proto_out, f"{excel['name']}.proto")

    with open(proto_path, "w", encoding="utf-8") as f:
        f.write('syntax = "proto3";\n\n')

        for sheet in excel["sheets"]:
            item = f"{sheet['sheet']}Item"
            config = f"{sheet['sheet']}Config"

            f.write(f"message {item} {{\n")
            idx = 1
            for field in sheet["fields"]:
                if field["type"] not in TYPE_MAP:
                    raise Exception(
                        f"{excel['name']}.{sheet['sheet']} 字段'{field['name']}'"
                        f"类型'{field['type']}'不支持"
                    )
                t = TYPE_MAP[field["type"]]
                name = snake(field["name"])
                if field["array"]:
                    f.write(f"  repeated {t} {name} = {idx};\n")
                else:
                    f.write(f"  {t} {name} = {idx};\n")
                idx += 1
            f.write("}\n\n")

            f.write(f"message {config} {{\n")
            f.write(f"  repeated {item} items = 1;\n")
            f.write("}\n\n")

    print(f"[PROTO] 生成 {proto_path}")
