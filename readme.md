# How to use
## Create AOJ Folder
```
$ aojprepare.py {ProblemID} {Title(optional)}
```

By default, the folder structure is as below.

```
{MMDD}
    ├── {ProblemID}
    │     ├── {ProblemID}.rs
    │     ├── input1.txt
    │     ├── output1.txt
    │     ├── input2.txt
    │     ├── output2.txt
    │         ︙
    │     ├── inputN.txt
    │     └── outputN.txt
    └── {ProblemID}
            ︙
```

You can change the folder or file name rules by editing the `get_folder_name()` and `get_file_name()` in `aojprepare.py`. You can also change the destination folder by editing the `target_dir` variable in `aojprepare.py`.

## Create AtCoder Folder
```
$ atcoderprepare.py {ContestID}|{ContestURL}
```

By default, the folder structure is as below.

```
{ContestID}
  ├── {ProblemID}
  │     ├── {ProblemID}.rs
  │     ├── input1.txt
  │     ├── output1.txt
  │     ├── input2.txt
  │     ├── output2.txt
  │         ︙
  │     ├── inputN.txt
  │     └── outputN.txt
  └── {ProblemID}
        ︙
```

You can change the folder or file name rules by editing the `get_folder_name()` and `get_file_name()` in `atcoderprepare.py`. You can also change the destination folder by editing the `target_dir` variable in `atcoderprepare.py`.

## Setting the Template File

The template file is located in the `src/code_templates/(aoj|atcoder)/` folder, and this is an example of the file.

```rust
/*
{問題ID} - {タイトル}
実行時間制限： {実行時間制限}s
メモリ制限： {メモリ制限}KB
正解率： {正解率}%
From: {提供元}
*/

use std::io::{self, Read};

fn main() {
    println!("");
}
```

You can modify the template file to suit your needs.

## Run the Test

```
$ autotest.py {Folder/FilePath}
```

The above command runs the test and compares the output with the expected output.
If the output is incorrect, the input, expected output, and actual output are displayed.

If the argument is a folder, the test is performed for a file with the same name as the folder in the folder.
