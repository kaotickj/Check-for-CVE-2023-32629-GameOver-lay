import os
import subprocess
import sys


def is_root_user():
    return os.geteuid() == 0

def is_in_git_repository():
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"])
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        print("Error: Git is not installed or accessible on your system.")
        return False

def check_vulnerable_kernel_versions():
    vulnerable_versions = ["5.10.0-1052", "5.10.0-1053", "5.10.0-1054"]  # Adjust the version numbers
    
    current_kernel_version = os.uname().release
    for version in vulnerable_versions:
        if version in current_kernel_version:
            print("Vulnerable Kernel Version: CVE-2023-2640")
            return
    
    print("No Vulnerable Kernel Versions Found: CVE-2023-2640")

def check_vulnerable_kernel_function():
    vulnerable_function = "ovl_copy_up_meta_inode_data"
    try:
        grep_output = subprocess.check_output(['grep', '-r', vulnerable_function, '/usr/src/linux-*']).decode('utf-8')
        if vulnerable_function in grep_output:
            print("Vulnerable Kernel Function: CVE-2023-32629")
        else:
            print("No Vulnerable Kernel Function Found: CVE-2023-32629")
    except subprocess.CalledProcessError:
        print("Error: An error occurred while running the 'grep' command.")
    except FileNotFoundError:
        print("Error: The 'grep' command or directory '/usr/src/linux-*' was not found.")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")

def is_overlayfs_used():
    overlayfs_mounts = os.popen('mount | grep overlay').read()
    
    if overlayfs_mounts:
        print("OverlayFS is being used on the system.")
    else:
        print("OverlayFS is not being used on the system.")

if __name__ == "__main__":
    if not is_root_user():
        print("Error: This script requires root privileges. Please run using sudo.")
        sys.exit(1)
    
    print("Starting security checks...\n")
    
    if is_in_git_repository():
        print("Your system is in a Git repository.\n")
        check_vulnerable_kernel_versions()
    else:
        print("Your system is not in a Git repository, skipping CVE-2023-2640 check.\n")
    
    check_vulnerable_kernel_function()
    is_overlayfs_used()
    
    print("\nSecurity checks completed.")
