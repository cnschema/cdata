# cdata

"see data", see data, handy snippets for conversion, cleaning and integration.


## json data manipulation
* json (and json stream) file IO, e.g.  items2file(...)
* json data access, e.g. json_get(...)
* json array statistics, e.g. stat(...)

.. code-block:: python
  from cdata.core import any2utf8
  the_input = {"hello": u"世界"}
  the_output = any2utf8(the_input)
  logging.info((the_input, the_output))


## table data manipulation
* json array to/from excel

.. code-block:: python
  import json
  from cdata.table import excel2json,json2excel
  filename = "test.xls"
  items = [{"first":"hello", "last":"world" }]
  json2excel(items, ["first","last"], filename)
  ret = excel2json(filename)
  print json.dumps(ret)

```
JSON data from reading a single sheet excel file
{
    "fields": {
        "00": [
            "name",
            "年龄",
            "notes"
        ]
    },
    "data": {
        "00": [
            {
                "notes": "",
                "年龄": 18.0,
                "name": "张三"
            },
            {
                "notes": "this is li si",
                "年龄": 18.0,
                "name": "李四"
            }
        ]
    }
}
```

## web stuff
* url domain extraction

## misc
* support simple cli function using argparse
