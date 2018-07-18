# OggEncoder
A Python **3** script to encode OGG, OPUS and MP3 files with keeping the file tree

## Usage
For each encoder, its corresponding package must be installed:
- **vorbis-toos** for VORBIS codec
- **opus-tools** for OPUS codec
- **lame** for MP3 codec
This script does not require any additional module.

### Command
For a simple use, the command can be launched without option
```
./oggenc.py
```

### Options
| Option                   | Description                                    |
|--------------------------|------------------------------------------------|
| `-i, --input`       | Specify the source directory                        |
| `-o, --output`      | Specify the destination directory                   |
| `-q, --quality`     | Specify quality, between -1 (very low) and 10 (very high).<br>Fractional qualities (e.g. 2.75) are permitted.<br>The default quality level is 3. |
| `-b, --bitrate`     | Specify bitrate value to use instead of quality     |
| `-e, --extension`   | Speficy the extension of the files to process (default `flac` and `wav`) |
| `-s, --source`      | Speficy the extension of the files to process (default flac and wav) |
| `-d, --destination` | Speficy the extension of the destination files (default corresponds to chosen encoder) |
| `-c, --copy`        | Copy the other files from `source` to `destination` |
| `-f, --force`       | Overwrite existing files                            |
  
