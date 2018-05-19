# OggEncoder
A Python **3** script to encode OGG files with oggenc and keeping the file tree

## Usage
This script does not require any additional module

### Command
For a simple use, the command can be launched without option
```
./oggenc.py
```

### Options
| Option                   | Description                                    |
|--------------------------|------------------------------------------------|
| `-s, --source`      | Specify the input directory                         |
| `-d, --destination` | Specify the output directory                        |
| `-q, --quality`     | Specify quality, between -1 (very low) and 10 (very high).<br>Fractional qualities (e.g. 2.75) are permitted.<br>The default quality level is 3. |
| `-e, --extension`   | Speficy the extension of the files to process (default `flac` and `wav`) |
| `-c, --copy`        | Copy the other files from `source` to `destination` |
