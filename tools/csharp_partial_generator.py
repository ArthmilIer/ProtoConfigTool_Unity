import os

TEMPLATE = """using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public partial class {sheet}Config
{{
    private Dictionary<uint, {sheet}Item> _byId;

    public void BuildIndex()
    {{
        _byId = new Dictionary<uint, {sheet}Item>(Items.Count);
        foreach (var item in Items)
        {{
            _byId[item.Id] = item;
        }}
    }}

    public {sheet}Item Get(uint id)
    {{
        _byId.TryGetValue(id, out var val);
        return val;
    }}
}}
"""

def generate_partial(sheet_name: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)

    file_path = os.path.join(out_dir, f"{sheet_name}Config.cs")

    # 已存在就不覆盖（非常重要）
    if os.path.exists(file_path):
        print(f"[SKIP] 已存在 partial: {file_path}")
        return

    code = TEMPLATE.format(sheet=sheet_name)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    print(f"[GEN ] partial -> {file_path}")
