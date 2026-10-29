import os
import sys
import argparse
from tools.excel_loader import load_excels
from tools.proto_writer import generate_proto
from tools.validator import validate_sheet
from tools.data_converter import build_bytes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--excel_dir", default="./excel")
    parser.add_argument("--proto_out", default="./output/proto")
    parser.add_argument("--bytes_out", default="./output/bytes")
    parser.add_argument("--partial_out", default="./output/csharp_partial")
    args = parser.parse_args()

    os.makedirs(args.proto_out, exist_ok=True)
    os.makedirs(args.bytes_out, exist_ok=True)

    print(f"Excel目录: {args.excel_dir}")
    print(f"Proto输出: {args.proto_out}")
    print(f"Bytes输出: {args.bytes_out}")

    excel_infos = load_excels(args.excel_dir)

    for excel in excel_infos:
        generate_proto(excel, args.proto_out)

    for excel in excel_infos:
        for sheet in excel["sheets"]:
            validate_sheet(sheet)
            build_bytes(sheet, args.proto_out, args.bytes_out, args.partial_out)

    print("\n===== 全部配置生成完成 =====")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
