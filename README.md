# aes-wrapper
A convenient wrapper for encrypting and decrypting files with [aescrypt](https://www.aescrypt.com/), useful as a Nautilus plugin.

It's simple to use, just pass the file you wish to encrypt or decrypt as the argument. If the filename ends with `.aes`, the script will automatically assumes the file is an encrypted file, and will prompt you the password to decrypt it.

To use it as a Nautilus plugin, put the script into `$HOME/.local/share/nautilus/scripts/`. You can access the script by right clicking on a file.
