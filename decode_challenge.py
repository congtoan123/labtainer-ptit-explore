import json
import base64
import codecs
from binascii import unhexlify
import sys

def json_recv(input_file):
    try:
        line = input_file.readline()
        if not line:
            return None
        return json.loads(line)
    except json.JSONDecodeError:
        return None

def json_send(output_file, hsh):
    output_file.write(json.dumps(hsh) + '\n')
    output_file.flush()

def list_to_string(s):
    output = ""
    return(output.join(s))


def decode_from_file(input_filename, output_filename):
    flag = ""
    with open(input_filename, "r") as input_file, open(output_filename, "w") as output_file:
        for i in range(101):
            received = json_recv(input_file)
            if received is None:
                print("End of input file reached.")
                break

            if "flag" in received:
                print("\n[*] FLAG: {}".format(received["flag"]))
                break

            print("\n[-] Cycle: {}".format(i))
            print("[-] Received type: {}".format(received["type"]))
            print("[-] Received encoded value: {}".format(received["encoded"]))

            word = received["encoded"]
            encoding = received["type"]
            #write your code down here
            if encoding == "base64":
                decoded = base64.b64decode(word).decode('utf8').replace("'", '"')
            elif encoding == "hex":
                decoded = (unhexlify(word)).decode('utf8').replace("'", '"')
            elif encoding == "rot13":
                decoded = codecs.decode(word, 'rot_13')
            elif encoding == "bigint":
                decoded = unhexlify(word.replace("0x", "")).decode('utf8').replace("'", '"')
            elif encoding == "utf-8":
                decoded = list_to_string([chr(b) for b in word])

            flag += decoded[0]
            # don't write here
            print("[-] Decoded: {}".format(decoded))
            print("[-] Decoded Type: {}".format(type(decoded)))

            to_send = {"decoded": decoded}
            json_send(output_file, to_send)

        print("\n[*] Final FLAG: {}".format(flag))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python decode.py input.json")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = "output.json"
    decode_from_file(input_filename, output_filename)

