import os
import shutil
import subprocess
import urllib.request

url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
tools_path = os.path.abspath("C:\\platform-tools")
extract_path = os.path.abspath("C:\\")
file_name = "platform-tools.zip"
adb_location = os.path.join(tools_path, "adb.exe")
is_adb_installed = shutil.which("adb")
is_fb_installed = shutil.which("fastboot")


def main(install=None, update=None):
    if install or update:
        print("Downloading latest platform-tools")
        urllib.request.urlretrieve(url, file_name)

        print(f"Extracting platform-tools to {extract_path}")
        shutil.unpack_archive(file_name, extract_path, "zip")

    if install:
        command_arg = f"{os.environ['PATH']};{tools_path}"
        subprocess.run(["setx", "/M", "PATH", command_arg])
        print("Setup complete")


if is_adb_installed and is_fb_installed:
    print(
        f"Platform-tools are already installed at \n{is_adb_installed}\n{is_fb_installed}"
    )
    if is_adb_installed == adb_location:
        print(f"platform-tools are installed at {adb_location}")
        answer = input("Do you want to update them to the latest version(y/n)")
        if answer.lower() == "y":
            main(update=True)
        else:
            print("You have choosen not to update them.\nAborting...")
elif not is_adb_installed:
    print("platform-tools are not installed.")
    print(f"Installing  platform-tools to {adb_location}")
    main(install=True)


# wait for userinput to exit
input("Press any key to exit")
