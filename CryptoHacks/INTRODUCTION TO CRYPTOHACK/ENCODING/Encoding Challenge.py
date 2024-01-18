from pwn import *
import json

import base64

##########################################################
import codecs                                           #### ROT-13 Decoder
rot13 = lambda s : codecs.getencoder("rot-13")(s)[0]    ##
############################################################ https://stackoverflow.com/questions/47002483/decode-python-rot13-string

#{"type": "rot13", "encoded": "qvfohefrq_Cbefpurf_gvaqreobkf"}
#{"type": "rot13", "decoded": "disbursed_Porsches_tinderboxs"} # acceptable answer

host = "socket.cryptohack.org"

port = 13377

s = remote(host, port)

for j in range(1,101):
    
    json_string =  s.recvuntil('\n').decode().strip()


    json_string_format = json.loads(json_string)


    current_type = json_string_format["type"] # 
    current_encrypted_text = json_string_format["encoded"]

    #print(current_type)
    #print(current_encrypted_text)
    print(json_string)

    if current_type == "bigint":
        decrypted_text = b''.fromhex(current_encrypted_text.replace('0x','')).decode()

    elif current_type == "rot13":
        decrypted_text = rot13(current_encrypted_text)
        
    elif current_type == "base64":
        decrypted_text = base64.standard_b64decode(current_encrypted_text).decode()

    elif current_type == "hex":
        decrypted_text = b''.fromhex(current_encrypted_text).decode()
        
    elif current_type == "utf-8":
        current_encrypted_text = str(current_encrypted_text).replace("[","").replace("]","").replace(",","")

        current_encrypted_text = current_encrypted_text.split(" ")

        decrypted_text = ""

        for i in current_encrypted_text:
            decrypted_text += chr(int(i))


    answer = '{"type": "' + current_type + '", "decoded": "' + decrypted_text + '"}' 
    s.send((answer+'\n'))

    print(answer)

print(s.recvuntil('\n').decode().strip()) # our 101th response is the flag