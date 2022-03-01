# wai-annotations-voc
wai.annotations module for dealing with Pascal VOC (visual object classes) datasets.

## Plugins
### FROM-YOLO-OD
Reads image object-detection annotations in the Pascal VOC XML-format

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

#### Domain(s):
- **Image Object-Detection Domain**

#### Options:
```
    FROM-VOC-OD:
      Reads image object-detection annotations in the Pascal VOC XML-format

      Domain(s): Image Object-Detection Domain

      usage: from-voc-od [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME] [--seed SEED]

      optional arguments:
        -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
        -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
        -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
        -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
        -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into
        --seed SEED     the seed to use for randomisation
```

### TO-YOLO-OD
Writes image object-detection annotations in the Pascal VOC XML-format

#### Domain(s):
- **Image Object-Detection Domain**

### Options:
```
    TO-VOC-OD:
      Writes image object-detection annotations in the Pascal VOC XML-format

      Domain(s): Image Object-Detection Domain

      usage: to-voc-od [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

      optional arguments:
        --annotations-only
                        skip the writing of data files, outputting only the annotation files
        -o PATH, --output PATH
                        output directory to write annotations to (images are placed in same directory)
        --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
        --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```
