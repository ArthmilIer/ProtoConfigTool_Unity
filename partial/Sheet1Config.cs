using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public partial class Sheet1Config
{
    private Dictionary<uint, Sheet1Item> _byId;

    public void BuildIndex()
    {
        _byId = new Dictionary<uint, Sheet1Item>(Items.Count);
        foreach (var item in Items)
        {
            _byId[item.Id] = item;
        }
    }

    public Sheet1Item Get(uint id)
    {
        _byId.TryGetValue(id, out var val);
        return val;
    }
}
