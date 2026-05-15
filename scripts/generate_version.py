import json

v = json.load(open("version/version.json"))["version"]
major, minor = v.split(".")

content = f'''
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=({major},{minor},0,0),
        prodvers=({major},{minor},0,0),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable(
                u'040904B0',
                [
                StringStruct(u'ProductName', u'Company Cleaner'),
                StringStruct(u'FileVersion', u'{v}'),
                StringStruct(u'ProductVersion', u'{v}')
                ]
            )
        ])
    ]
)
'''

open("version.txt", "w").write(content)

print("Generated version.txt:", v)