# PaperImageExtract

## About

PaperImageExtract is a script that can take Dropbox exported Markdown files and extract the images.

When exporting Markdown from Dropbox the images are still linked to a remote ``https://paper-attachments.dropbox.com`` URL. This script will fetch the images located at this URL, store them locally, and alter the Markdown file to point to the local copies.

## Parameters

- ``--file``: The Markdown file exported from Dropbox.
- ``--output``: The folder to put all files and downloaded images into.

## Demo

As can be seen we have a file ``Untitled.md`` which contains multiple references to remote PNG files stored on Dropbox.

```bash
user@computer:~/DropboxMarkdown$ ls -l
total 28
-rwxr-xr-x 1 user user  4627 Nov 26 00:35 PaperImageExtract.py
-rwxr-xr-x 1 user user 12310 Nov 26 00:35 Untitled.md
drwxr-xr-x 2 user user  4096 Nov 26 00:35 output_folder
user@computer:~/DropboxMarkdown$
user@computer:~/DropboxMarkdown$ cat Untitled.md | grep png
![Test Picture](https://paper-attachments.dropbox.com/s_E4EFB9DAC93D5A33ED9AE14EAD20FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1594068225794_image.png)
![Nice Pict](https://paper-attachments.dropbox.com/s_E4EFB9DAC93D5A23ED9AE14EAD30FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1596235811820_image.png)
![Blah Blah Blah](https://paper-attachments.dropbox.com/s_E4EFB9DAC93D5A24ED9AE14EAD20FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1606368476693_image.png)
user@computer:~/DropboxMarkdown$
```

We run the extraction script.

```bash
user@computer:~/DropboxMarkdown$ ./PaperImageExtract.py --file Untitled.md --output ~/DropboxMarkdown/output_folder/
```

As a result we get the files stored locally and new references to them in the exported Markdown file.

```bash
user@computer:~/DropboxMarkdown$ ls -l ~/DropboxMarkdown/output_folder/img/
total 676
-rw-r--r-- 1 user user  15474 Nov 26 00:35 s_E4EFB9DAC93D5A33ED9AE14EAD20FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1594068225794_image.png
-rw-r--r-- 1 user user   8480 Nov 26 00:35 s_E4EFB9DAC93D5A23ED9AE14EAD30FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1596235811820_image.png
-rw-r--r-- 1 user user 662025 Nov 26 00:35 s_E4EFB9DAC93D5A24ED9AE14EAD20FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1606368476693_image.png
user@computer:~/DropboxMarkdown$ cat ~/DropboxMarkdown/output_folder/Untitled.md | grep png
![Test Picture](./img/s_E4EFB9DAC93D5A33ED9AE14EAD20FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1594068225794_image.png)
![Nice Pict](./img/s_E4EFB9DAC93D5A23ED9AE14EAD30FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1596235811820_image.png)
![Blah Blah Blah](./img/s_E4EFB9DAC93D5A24ED9AE14EAD20FA8B2A8DB4A2242D0DD36C96831867F8E9E4_1606368476693_image.png)
user@computer:~/DropboxMarkdown$
```