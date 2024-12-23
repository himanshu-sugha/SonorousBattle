from flask import Flask, request, jsonify
from web3 import Web3
from flask_validator import Validate, Param
import time
from threading import Timer

app = Flask(__name__)
Validate(app)

# Initialize Web3
web3 = Web3(Web3.HTTPProvider('https://your-ethereum-node-url'))
contract_address = '0xYourContractAddress'
abi = [  # Contract ABI goes here
]
contract = web3.eth.contract(address=contract_address, abi=abi)

def get_balance_in_ether(address):
    return web3.fromWei(web3.eth.get_balance(address), 'ether')

def validate_payment(payment_amount):
    if not payment_amount or payment_amount <= 0:
        raise ValueError('A valid payment amount must be provided.')

def schedule_task(func, delay, *args):
    Timer(delay, func, args).start()

async def get_winner(battle_id):
    try:
        if not battle_id:
            raise ValueError("Battle ID is required")

        print(f"Closing battle {battle_id}...")

        final_result = contract.functions.closeBattle(battle_id).call()

        result = final_result["0"]
        result_message = final_result["1"]

        part1 = "Match Tied. Money will be distributed to both. All voters are winners."
        winner_voters_list = []

        if result == 1:
            part1 = "Track 1 is the winner"
            winner_voters_list = contract.functions.getSpecificTrackVoters(result, battle_id).call()
        elif result == 2:
            part1 = "Track 2 is the winner"
            winner_voters_list = contract.functions.getSpecificTrackVoters(result, battle_id).call()
        else:
            winner_voters_list = contract.functions.votersList(battle_id).call()

        return {
            "part1": part1,
            "winnerVotersList": winner_voters_list,
            "resultMessage": result_message,
        }
    except Exception as e:
        print(f"Error in get_winner: {str(e)}")
        raise

@app.route('/startbattle', methods=['POST'])
@Validate(
    Param('track1', str, required=True),
    Param('track2', str, required=True),
    Param('creatorTrack1', str, required=True),
    Param('creatorTrack2', str, required=True),
    Param('userAddress', str, required=True),
    Param('paymentAmount', float, required=True)
)
def start_battle():
    try:
        data = request.json
        track1 = data['track1']
        track2 = data['track2']
        creator_track1 = data['creatorTrack1']
        creator_track2 = data['creatorTrack2']
        user_address = data['userAddress']
        payment_amount = data['paymentAmount']

        validate_payment(payment_amount)
        payment_in_wei = web3.toWei(payment_amount, 'ether')

        balance_before = web3.eth.get_balance(user_address)
        print(f"User's balance before transaction: {web3.fromWei(balance_before, 'ether')} ETH")

        tx = contract.functions.createBattle(track1, track2, creator_track1, creator_track2)
        gas = tx.estimateGas({
            'from': user_address,
            'value': payment_in_wei
        })

        receipt = tx.transact({
            'from': user_address,
            'gas': gas,
            'value': payment_in_wei
        })

        balance_after = web3.eth.get_balance(user_address)
        print(f"User's balance after transaction: {web3.fromWei(balance_after, 'ether')} ETH")

        battle_id = receipt.logs[0]['data'] if receipt.logs else None

        if battle_id:
            print(f"Scheduling get_winner for battle ID: {battle_id}")
            schedule_task(get_winner, 60, battle_id)

        return jsonify({
            "message": f"Music Battle between {track1} and {track2} has started!",
            "balanceBefore": web3.fromWei(balance_before, 'ether'),
            "balanceAfter": web3.fromWei(balance_after, 'ether'),
            "battleId": battle_id
        })
    except Exception as e:
        print(f"Error in start_battle: {str(e)}")
        return jsonify({"error": "Failed to start battle"}), 500

@app.route('/battle/<int:battle_id>/winner', methods=['GET'])
def battle_winner(battle_id):
    try:
        winner = get_winner(battle_id)
        return jsonify({
            "battleId": battle_id,
            **winner
        })
    except Exception as e:
        print(f"Error in battle_winner: {str(e)}")
        return jsonify({"error": "Failed to retrieve battle winner"}), 500

if __name__ == '__main__':
    app.run(debug=True)
