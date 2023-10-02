import subprocess
import platform
import os

system = platform.system()
# Get the current working directory
current_directory = os.getcwd()

def what_os_is():
    if system == "Windows":
        return "win"
    elif system == "Darwin":
        return "mac"
    else:
        return ""

def run_promotheus():
    current_os = what_os_is()
    if current_os == "":
        print("OS Not Found")
        return
    
    try:
        # Run the executable file
        print(f"running {current_os} version of prometheus")
        prometheus_path = ''
        config_file_path = ''
        if(current_os == 'win'):
            prometheus_path = 'prometheus/win/prometheus.exe'
            config_file_path = 'prometheus/win/prometheus.yml'
        else:
            prometheus_path = 'prometheus/mac/bin/prometheus'
            config_file_path = 'prometheus/mac/bin/prometheus.yml'

        executable_path = os.path.join(current_directory, prometheus_path)
        config_param = os.path.join(current_directory, config_file_path)
        subprocess.run([executable_path, '--config.file', config_param])
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    run_promotheus()
