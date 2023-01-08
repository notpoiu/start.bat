import zipfile
import subprocess
import os
import platform
import json

with open('config.json','r') as f:
    config = json.load(f)

def findJars():
    files = os.listdir('.')

    jar_files = [f for f in files if f.endswith('.jar')]
    return jar_files

def check_java():
    try:
        output = subprocess.run(["java", "-version"], capture_output=True, text=True)
        java_version = output.stderr.split("\n")[0]
        return True,java_version.replace('"',"").split(" ")[2]
    except:
        return False

def check_min_version():
    with zipfile.ZipFile(f'{serverJar}', 'r') as jar:
        manifest = jar.read('META-INF/MANIFEST.MF')
    
    lines = manifest.splitlines()

    for line in lines:
    
        line = line.decode()
        if line.startswith('Build-Jdk'):
            
            java_version = line.split(':')[1].strip()
            return java_version

def compareAndFindCompatible(min,current):
    buildVerMin = str(min).split("_")
    buildVerCurrent = str(current).split("_")

    if (buildVerMin[1] < buildVerCurrent[1]) and (buildVerMin[0] == buildVerCurrent[0]):
        return True
    return False

def getOSName():
    if platform.system() == "Darwin":
        return 'Mac OS'
    return platform.system()

if __name__ == "__main__":
    serverJar = findJars()[0]

    didRun,current_java_ver = check_java()
    minimum_java_ver = check_min_version()

    result = compareAndFindCompatible(minimum_java_ver,current_java_ver)

    if result == False:
        print(f"Error with incompatible java version, make sure you have java {minimum_java_ver} or higher")

    if didRun == False:
        print("Error with getting java version on computer...")
        exit(0)

    os.system("title Start.bat but better")

    print(f'''

    ░██████╗████████╗░█████╗░██████╗░████████╗░░░██████╗░░█████╗░████████╗
    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝░░░██╔══██╗██╔══██╗╚══██╔══╝
    ╚█████╗░░░░██║░░░███████║██████╔╝░░░██║░░░░░░██████╦╝███████║░░░██║░░░
    ░╚═══██╗░░░██║░░░██╔══██║██╔══██╗░░░██║░░░░░░██╔══██╗██╔══██║░░░██║░░░
    ██████╔╝░░░██║░░░██║░░██║██║░░██║░░░██║░░░██╗██████╦╝██║░░██║░░░██║░░░
    ╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░
    {f"(but better)".center(70)}

    {f"Java version: {current_java_ver}".center(70)}
    {f"Server jar: {serverJar}".center(70)}
    {"Made by notpoiu".center(70)}


    ''')

    if config['inputRam'] == True:
        raminput = input("How much ram would you like to use for the server? (in gigabytes): ")
        
        with open('config.json','w') as f:
            dictionary = {
                "inputRam": False,
                "Ram": f"{raminput}G",
                "inputPortforwarding": config['inputPortforwarding'],
                "autoPortForward": config['autoPortForward']
            }
            config = json.dump(dictionary,f)
    
    with open('config.json','r') as f:
        config = json.load(f)

    if bool(config['inputPortforwarding']) == True:
        portstartinput = input("Do you want auto port forwarding? y for yes n for no (y/n): ")
        if portstartinput == 'y':
            os.system("start https://dashboard.ngrok.com/login")
            print(f"Make a ngrok account with google or github. next you press on the blue button that says: Download for {getOSName()}")
            os.system("pause")
            print(f"then unzip the ngrok executable and place it in {os.path.dirname(os.path.abspath(__file__))}")
            os.system("pause")
            print("then go back to the dashboard and on the second white box under `Unzip to install`, you will see a box with it saying as the title: `Connect your account`\nUnder the paragraph that talks about ngrok's configuration file, you will see a darker box that contains a command.\ncopy the whole thing, from ngrok to the last character in the key")
            cmdInput = input("Copy pasted command here: ")
            os.system(f"ngrok config add-authtoken {cmdInput.split(' ').pop()}")
            print("Portforwarding successful!")
            with open('config.json','w') as f:
                dictionary = {
                    "inputRam": config['inputRam'],
                    "Ram": config['Ram'],
                    "inputPortforwarding": False,
                    "autoPortForward": True
                }
                config = json.dump(dictionary,f)
        else:
            print("Ok! saving it to your preferences. (NOTE: IF YOU WANT TO CHANGE SETTINGS GO IN CONFIG.JSON TO CHANGE THEM.)")
            with open('config.json','w') as f:
                dictionary = {
                    "inputRam": config['inputRam'],
                    "Ram": config['Ram'],
                    "inputPortforwarding": False,
                    "autoPortForward": False
                }
                config = json.dump(dictionary,f)

    with open('config.json','r') as f:
        config = json.load(f)

    if bool(config['autoPortForward']) == True:
        os.system("cmd /k ngrok tcp 25565")
    
    os.system(f"java -jar -Xms{str(config['Ram'])} -Xmx{str(config['Ram'])} {serverJar} nogui")
    os.system("pause")
    exit(0)