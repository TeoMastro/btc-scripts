from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey, PublicKey
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.constants import SATOSHIS_PER_BITCOIN

def main():
    setup('testnet')

    # Input keys and addresses
    #priv_key1 = PrivateKey(input("Enter Private Key 1: "))
    priv_key1 = PrivateKey()
    priv_key2 = PrivateKey()
    #priv_key2 = PrivateKey(input("Enter Private Key 2: "))
    #pub_key = PublicKey(input("Enter Public Key: "))
    pub_key = PublicKey('03b32229e4aee58b946a1ececab52e664663be1021780b9f31941caecc95c5ec6b')

    # Derive public keys from private keys
    derived_pub_key1 = priv_key1.get_public_key()
    derived_pub_key2 = priv_key2.get_public_key()

    p2sh_address = '2N1MHfbuQyBux8QPXzDVy3hfb5ZkszczsSS'
    p2pkh_address = 'mjQ2qmVRMcN71MLjsE2ukT3XvVTBGfaDMt'

    # Recreate the redeem script
    script = Script([2, derived_pub_key1.to_hex(), derived_pub_key2.to_hex(), pub_key.to_hex(), 3, 'OP_CHECKMULTISIG'])
    p2sh = P2shAddress.from_script(script)
    redeem_script = script.to_p2sh_script_pub_key()

    # Check UTXOs (This part requires API access or local node query)
    # utxos = fetch_utxos(p2sh_address)
    # Assume we have a UTXO for demonstration:
    utxos = [{'txid': 'a3f258cc7c723bdba2f9606028ad748bac6748aefeec87ee5cde39056bf805b4', 'vout': 0, 'amount': 0.001}]

    # Create Transaction Inputs
    fee = 0.0001  # Set a fixed fee for simplicity
    inputs = [TxInput(utxo['txid'], utxo['vout']) for utxo in utxos]
    total_btc = sum(utxo['amount'] for utxo in utxos) - fee  # sum in BTC
    total_satoshis = int(total_btc * SATOSHIS_PER_BITCOIN)

    # Calculate fees and transaction outputs
    total_amount = sum(utxo['amount'] for utxo in utxos) - fee
    outputs = [TxOutput(total_satoshis, P2pkhAddress(p2pkh_address).to_script_pub_key())]

    # Create transaction
    tx = Transaction(inputs, outputs)

    # Sign transaction manually
    for i, input in enumerate(inputs):
        sig1 = priv_key1.sign_input(tx, i, redeem_script)
        sig2 = priv_key2.sign_input(tx, i, redeem_script)
        # Create the scriptSig that unlocks the previous output
        input.script_sig = Script([sig1, sig2, redeem_script.to_hex()])

    # Display raw unsigned and signed transactions
    print("Raw Unsigned Transaction:", tx.serialize())
    #print("Raw Signed Transaction:", tx.get_signed_transaction())
    print("Transaction ID:", tx.get_txid())

    # Verify and broadcast
    # if tx.is_valid():
    #    broadcast_tx(tx.serialize())

if __name__ == "__main__":
    main()
