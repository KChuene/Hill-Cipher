modes = ["decrypt", "encrypt"]
options = ["-key","-f"]

config = {
    "mode":None, 
    "key":None,
}

def usage():
    print("\n")
    print("HillCipher implementation.\n\n")
    print("usage: \n\tprogram.py <mode> -key <key> \n")
    print("modes:")
    print("encrypt\t Execute in encryption mode. Encrypt all input.")
    print("decrypt\t Execute in decryption mode. Decrypt all input.\n\n")
    print("options:")
    print("-key <key>\t The key to use in encryption or decryption mode. (required)")
    exit()

def safe_read_arg_value(arg, argv):
    if argv.index(arg)+1 > len(argv)-1:
        print(f"Unspecified value for '{arg}'. Insufficient args.")
        usage()
    
    return argv[argv.index(arg)+1]

def validate_args(argv):
    global config

    # 1. Check number of arguments
    if (len(argv) < 4):
        print(f"No. arguments provided ({len(argv)}). Too few provided.")
        usage() 

    # 2. Check validity of mode
    mode = argv[1]
    if not mode in modes:
        print(f"Valid mode expected, but '{mode}' found.")
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

    return config