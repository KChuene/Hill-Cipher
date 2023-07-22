modes = ["decrypt", "encrypt"]
options = ["-key","-f"]

config = {
    "mode":None, 
    "key":None,
    "filename":None
}

def usage():
    print("\n")
    print("HillCipher implementation.\n\n")
    print("usage: \n\tprogram.py <mode> -key <key> [-f <filename>]\n")
    print("modes:")
    print("encrypt\t Execute in encryption mode. Encrypt all input.")
    print("decrypt\t Execute in decryption mode. Decrypt all input.\n\n")
    print("options:")
    print("-key <key>\t The key to use in encryption or decryption mode. (required)")
    print("-f <filename>\t If provided, the program will encrypt or decrypt the "+
          "file specified by <filename>. (optional)")
    exit()

def safe_read_arg_value(arg, argv):
    if argv.index(arg)+1 > len(argv)-1:
        print(f"Unspecified value for {arg}. Insufficient args.")
        usage()
    
    return argv[argv.index(arg)+1]

def validate_args(argv):
    global config

    # 1. Check number of arguments
    if not (len(argv) >= 4 and len(argv) <= 6):
        print(f"No. arguments provided ({len(argv)}). Too few/many provided.")
        usage() 

    # 2. Check validity of mode
    mode = argv[1]
    if not mode in modes:
        print(f"Valid mode expected, but {mode} found.")
        usage()

    config["mode"] = mode
    

    # 3. Ensure key option provided
    if not "-key" in argv:
        print("Key option expected. Not found.")
        usage()

    else:
        key_value = safe_read_arg_value("-key", argv)
        if (key_value in options) or (key_value in modes): # option/mode name not acceptable is as key
            print(f"Unexpected value {key_value} for -key.")
            usage()
        
        config["key"] = key_value
        
    
    # 4. Inspect values of options
    if "-f" in argv:
        filename = safe_read_arg_value("-f", argv)
        if (filename in options) or (filename in modes): # option/mode name not acceptable as filename
            print(f"Unexpected value {filename} for -f.")
            usage()

        config["filename"] = filename

    return config