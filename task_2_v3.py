import sys
from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.constants import SATOSHIS_PER_BITCOIN

def main():
    setup('testnet')

    # Command-line arguments input
    if len(sys.argv) != 6:
        print("Usage: python script.py <Private Key 1> <Private Key 2> <Public Key> <P2SH Address> <P2PKH Address>")
        return

    key1 = sys.argv[1]
    key2 = sys.argv[2]
    key3 = sys.argv[3]
    p2sh_address = sys.argv[4] # the address created on the first script
    p2pkh_address = sys.argv[5]

    priv_key1 = PrivateKey(key1)
    priv_key2 = PrivateKey(key2)
    pub_key = PublicKey(key3)

    # Derive public keys from private keys
    derived_pub_key1 = priv_key1.get_public_key()
    derived_pub_key2 = priv_key2.get_public_key()

    # Recreate the redeem script
    script = Script([2, derived_pub_key1.to_hex(), derived_pub_key2.to_hex(), pub_key.to_hex(), 3, 'OP_CHECKMULTISIG'])
    redeem_script = script.to_p2sh_script_pub_key()

    # Transaction detail with the specific UTXO (for the p2sh_address)
    """ Assuming I can get the utxos by doing a get request on the 'https://blockstream.info/testnet/api/address/{address}/utxo'
    for my specific address. Ofc this will not work for me locally """
    utxos = [{'txid': 'd39be75058c0b23f736d84a597f9ef970debbb99640d4c0f7e71bd07fdc7580d', 'vout': 1, 'amount': 3.0}]

    inputs = [TxInput(utxo['txid'], utxo['vout'], script_sig='') for utxo in utxos]
    total_input = sum(int(utxo['amount'] * SATOSHIS_PER_BITCOIN) for utxo in utxos)

    # Estimate fee
    estimated_tx_size = 180 * len(inputs) + 34 * 2 + 10  # 180bytes per input * 34(outputs) * 2 (num of outputs) + 10 (overhead)
    fee_rate = 1  # fee rate is changed by the network, I did not change that in my network
    fee = estimated_tx_size * fee_rate

    # Calculate total output amount after fees
    total_output = total_input - fee

    # Create Transaction Outputs
    outputs = [TxOutput(total_output, P2pkhAddress(p2pkh_address).to_script_pub_key())]

    # Create transaction
    tx = Transaction(inputs, outputs)
    # print("Raw Unsigned Transaction:", tx.serialize())

    # Sign transaction manually
    for i, input in enumerate(inputs):
        sig1 = priv_key1.sign_input(tx, i, redeem_script)
        sig2 = priv_key2.sign_input(tx, i, redeem_script)
        input.script_sig = Script([sig1, sig2, redeem_script.to_hex()])

    # Display results
    print("Raw Signed Transaction:", tx.serialize())
    print("Transaction ID:", tx.get_txid())

if __name__ == "__main__":
    main()
