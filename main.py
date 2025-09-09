import os
import shutil
import subprocess
import urllib.request

url = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
tools_path = os.path.abspath("C:\\platform-tools")
extract_path = os.path.abspath("C:\\")

file_name = "platform-tools.zip"
is_adb_installed = shutil.which("adb")
is_fb_installed = shutil.which("fastboot")
installed_tools_path = os.path.dirname(f"{is_adb_installed}")

# get all envs
envs = os.environ["PATH"].split(";")


def prep_tools():
    print("Downloading latest platform-tools")
    urllib.request.urlretrieve(url, file_name)

    print(f"Extracting platform-tools to {extract_path}")
    shutil.unpack_archive(file_name, extract_path, "zip")


def add_path(add=None, remove=None, path=None):
    if add and path:
        command_arg = f"{os.environ['PATH']};{path}"
        subprocess.run(["setx", "/M", "PATH", command_arg])
    if remove and path:
        env_path = envs[:]
        env_path.remove(path)
        env = ";".join(env_path)
        command_arg = f"{env}"
        subprocess.run(["setx", "/M", "PATH", command_arg])


# main function
def main(install=None, update=None):
    if install or update:
        prep_tools()

    if install:
        if tools_path not in envs:
            print("Adding platform-tools to PATH")
            add_path(add=True, path=tools_path)
        else:
            print("platform-tools are already in environment variables")


# execution
if is_adb_installed and is_fb_installed:
    print(f"Platform-tools are already installed at\n{installed_tools_path}")

    if installed_tools_path == tools_path:
        print(f"platform-tools are installed at {tools_path}")
        answer = input("Do you want to update them to the latest version(y/n)")

        if answer.lower() == "y":
            main(update=True)
        else:
            print("You have choosen not to update them.\nAborting...")

    elif not installed_tools_path == tools_path:
        print(f"platform-tools are installed at {installed_tools_path}")
        answer = input(
            f"Do you want to remove this path and install at {tools_path} \nto manage it later with adbwinstall?(y/n)"
        )

        if answer.lower() == "y":
            shutil.rmtree(installed_tools_path)
            envs.remove(installed_tools_path)
            add_path(remove=True, path=installed_tools_path)
            main(install=True)

elif not is_adb_installed:
    print("platform-tools are not installed.")
    print(f"Installing  platform-tools to {tools_path}")
    main(install=True)

# wait for userinput to exit
input("Press any key to exit")
