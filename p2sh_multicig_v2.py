import sys
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2shAddress, PublicKey
from bitcoinutils.script import Script

def main():
    setup('regtest')

    if len(sys.argv) != 4:
        print("Usage: python script.py <Public Key 1> <Public Key 2> <Public Key3>")
        return

    key1 = sys.argv[1]
    key2 = sys.argv[2]
    key3 = sys.argv[3]

    pub1 = PublicKey(key1)
    pub2 = PublicKey(key2)
    pub3 = PublicKey(key3)

    script = Script([2, pub1.to_hex(), pub2.to_hex(), pub3.to_hex(), 3, 'OP_CHECKMULTISIG'])

    p2sh_address = P2shAddress.from_script(script)
    print("P2SH Address:", p2sh_address.to_string())

if __name__ == "__main__":
    main()
