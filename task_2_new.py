from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.constants import SATOSHIS_PER_BITCOIN

def main():
    setup('testnet')

    # Input keys and addresses
    priv_key1 = PrivateKey()  # Normally, you would enter or load your specific private key here
    priv_key2 = PrivateKey()  # Same as above
    pub_key = PublicKey('03b32229e4aee58b946a1ececab52e664663be1021780b9f31941caecc95c5ec6b')

    # Derive public keys from private keys
    derived_pub_key1 = priv_key1.get_public_key()
    derived_pub_key2 = priv_key2.get_public_key()

    p2sh_address = '2N1MHfbuQyBux8QPXzDVy3hfb5ZkszczsSS'
    p2pkh_address = 'mjQ2qmVRMcN71MLjsE2ukT3XvVTBGfaDMt'

    # Recreate the redeem script
    script = Script([2, derived_pub_key1.to_hex(), derived_pub_key2.to_hex(), pub_key.to_hex(), 3, 'OP_CHECKMULTISIG'])
    redeem_script = script.to_p2sh_script_pub_key()

    # Transaction detail with the specific UTXO
    utxos = [{'txid': 'd39be75058c0b23f736d84a597f9ef970debbb99640d4c0f7e71bd07fdc7580d', 'vout': 1, 'amount': 3.0}]

    # Calculate transaction fees (fixed for simplicity)
    fee = 0.000221  # Set as per the provided transaction fee
    inputs = [TxInput(utxo['txid'], utxo['vout']) for utxo in utxos]
    total_btc = sum(utxo['amount'] for utxo in utxos) - fee
    total_satoshis = int(total_btc * SATOSHIS_PER_BITCOIN)

    # Create Transaction Outputs
    outputs = [TxOutput(total_satoshis, P2pkhAddress(p2pkh_address).to_script_pub_key())]

    # Create transaction
    tx = Transaction(inputs, outputs)

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
