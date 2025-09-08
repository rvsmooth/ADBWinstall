import os
import shutil
import subprocess
import urllib.request

url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
tools_path = os.path.abspath("C:\\platform-tools")
extract_path = os.path.abspath("C:\\")
file_name = "platform-tools.zip"


def main():
    print("Downloading latest platform-tools")
    urllib.request.urlretrieve(url, file_name)

    print(f"Extracting platform-tools to {extract_path}")
    shutil.unpack_archive(file_name, extract_path, "zip")

    print("Adding platform-tools to path")
    if shutil.which("adb"):
        print("adb is already added to the path\nskipping adding it to env")
    else:
        command_arg = f"%PATH%;{tools_path}"
        subprocess.run(["setx", "/M", "PATH", command_arg], shell=True)
        print("Setup complete")


# main execution
main()
