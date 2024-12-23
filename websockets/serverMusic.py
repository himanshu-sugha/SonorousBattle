from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from web3 import Web3
import asyncio
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Music Battle API")

# Initialize Web3 (replace with your provider URL)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load contract ABI and address (replace with your contract details)
CONTRACT_ABI =abi = [
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "_timeFeedAddress",
          "type": "address"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "winningTrack",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "winner",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "address[]",
          "name": "voters",
          "type": "address[]"
        },
        {
          "indexed": False,
          "internalType": "bool",
          "name": "isTie",
          "type": "bool"
        }
      ],
      "name": "BattleConcluded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "track1",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "string",
          "name": "track2",
          "type": "string"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "creatorTrack1",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "creatorTrack2",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "endTime",
          "type": "uint256"
        }
      ],
      "name": "BattleCreated",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "address",
          "name": "winner",
          "type": "address"
        }
      ],
      "name": "BattleEnded",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        }
      ],
      "name": "FundsTransferredToOwner",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "recipient",
          "type": "address"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        }
      ],
      "name": "RewardPaid",
      "type": "event"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "indexed": False,
          "internalType": "uint256",
          "name": "trackNumber",
          "type": "uint256"
        },
        {
          "indexed": True,
          "internalType": "address",
          "name": "voter",
          "type": "address"
        }
      ],
      "name": "VoteCast",
      "type": "event"
    },
    {
      "inputs": [],
      "name": "MAX_BATTLES",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "MAX_BATTLE_DURATION",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "STARTING_FEES",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "battleCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "userAddress",
          "type": "address"
        }
      ],
      "name": "battleVoters",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "battles",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "id",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "track1",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "track2",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "creatorTrack1",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "creatorTrack2",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "votesTrack1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "votesTrack2",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "endTime",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isActive",
          "type": "bool"
        },
        {
          "internalType": "address",
          "name": "winner",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "battleCreator",
          "type": "address"
        },
        {
          "internalType": "uint256",
          "name": "startingFees",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountGivenByTrack1Voters",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "amountGivenByTrack2Voters",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        }
      ],
      "name": "closeBattle",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        },
        {
          "internalType": "string",
          "name": "",
          "type": "string"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "track1",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "track2",
          "type": "string"
        },
        {
          "internalType": "address",
          "name": "creatorTrack1",
          "type": "address"
        },
        {
          "internalType": "address",
          "name": "creatorTrack2",
          "type": "address"
        }
      ],
      "name": "createBattle",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getBalance",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        }
      ],
      "name": "getBattleDetails",
      "outputs": [
        {
          "internalType": "string",
          "name": "track1",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "track2",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "votesTrack1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "votesTrack2",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "timestamp",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "isActive",
          "type": "bool"
        },
        {
          "internalType": "address",
          "name": "winner",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        }
      ],
      "name": "getBattleVotes",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "track1Votes",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "track2Votes",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getCurrentTime",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "trackNumber",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        }
      ],
      "name": "getSpecificTrackVoters",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "winnerVoters",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        }
      ],
      "name": "getTotalVoters",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "bool",
          "name": "_useOracle",
          "type": "bool"
        }
      ],
      "name": "toggleOracleTime",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "amount",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "addressToSendMoney",
          "type": "address"
        }
      ],
      "name": "transferFundsFromContractToOwner",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "trackNumber",
          "type": "uint256"
        },
        {
          "internalType": "address",
          "name": "userAddress",
          "type": "address"
        }
      ],
      "name": "vote",
      "outputs": [],
      "stateMutability": "payable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        }
      ],
      "name": "votersList",
      "outputs": [
        {
          "internalType": "address[]",
          "name": "_votersList",
          "type": "address[]"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "stateMutability": "payable",
      "type": "receive"
    }
  ]

CONTRACT_ADDRESS = '0x5FbDB2315678afecb367f032d93F642f64180aa3'
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Request/Response Models
class BattleStart(BaseModel):
    track1: str
    track2: str
    creatorTrack1: str
    creatorTrack2: str
    userAddress: str
    paymentAmount: float

    @validator('paymentAmount')
    def validate_payment(cls, v):
        if v <= 0:
            raise ValueError('Payment amount must be greater than 0')
        return v

class BattleResult(BaseModel):
    battleId: str
    part1: str
    winnerVotersList: List[str]
    resultMessage: str

async def get_winner(battle_id: str) -> BattleResult:
    """Get the winner of a battle."""
    try:
        logger.info(f"Battle no {battle_id} is now closing")
        
        # Call the contract method
        final_result = await contract.functions.closeBattle(battle_id).call()
        logger.info(f"Result: {final_result}")
        
        result = final_result[0]
        result_message = final_result[1]
        
        part1 = "Match Ties, Money will be distributed to both. All voters are winners."
        winner_voters_list = []
        
        if result == 1:
            part1 = "Track 1 is the winner"
            try:
                winner_voters_list = await contract.functions.getSpecificTrackVoters(
                    result, battle_id
                ).call()
            except Exception as e:
                logger.error(f"Error fetching Track 1 voters: {e}")
                
        elif result == 2:
            part1 = "Track 2 is the winner"
            try:
                winner_voters_list = await contract.functions.getSpecificTrackVoters(
                    result, battle_id
                ).call()
            except Exception as e:
                logger.error(f"Error fetching Track 2 voters: {e}")
        else:
            try:
                winner_voters_list = await contract.functions.votersList(battle_id).call()
            except Exception as e:
                logger.error(f"Error fetching tie voters: {e}")
        
        return BattleResult(
            battleId=battle_id,
            part1=part1,
            winnerVotersList=winner_voters_list,
            resultMessage=result_message
        )
        
    except Exception as e:
        logger.error(f"Get Winner Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def start_battle(battle_data: BattleStart):
    """Start a new battle between two tracks."""
    try:
        # Convert payment to Wei
        payment_in_wei = w3.to_wei(battle_data.paymentAmount, 'ether')
        
        # Get user balance before transaction
        balance_before = await w3.eth.get_balance(battle_data.userAddress)
        logger.info(f"User's balance before: {w3.from_wei(balance_before, 'ether')} ETH")
        
        # Prepare transaction
        tx = contract.functions.createBattle(
            battle_data.track1,
            battle_data.track2,
            battle_data.creatorTrack1,
            battle_data.creatorTrack2
        )
        
        # Estimate gas
        gas = await tx.estimate_gas({
            'from': battle_data.userAddress,
            'value': payment_in_wei
        })
        
        # Send transaction
        tx_hash = await tx.transact({
            'from': battle_data.userAddress,
            'gas': gas,
            'value': payment_in_wei
        })
        
        # Wait for transaction receipt
        receipt = await w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Get battle ID from events
        battle_created_event = receipt.events.get('BattleCreated')
        battle_id = battle_created_event['battleId'] if battle_created_event else None
        
        # Schedule winner determination
        if battle_id:
            logger.info(f"Scheduling getWinner for battle ID: {battle_id}")
            asyncio.create_task(
                asyncio.sleep(15)
                .then(lambda: get_winner(battle_id))
            )
        
        # Get final balance
        balance_after = await w3.eth.get_balance(battle_data.userAddress)
        
        return {
            "balanceBefore": w3.from_wei(balance_before, 'ether'),
            "balanceAfter": w3.from_wei(balance_after, 'ether'),
            "battleId": str(battle_id) if battle_id else None,
            "transactionHash": receipt.transactionHash.hex()
        }
        
    except Exception as e:
        logger.error(f"Battle Creation Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# API Routes
@app.post("/startbattle")
async def create_battle(battle_data: BattleStart):
    """Start a new music battle."""
    logger.info("Starting new battle")
    logger.info(f"Request data: {battle_data}")
    
    result = await start_battle(battle_data)
    
    return {
        "message": f"Music Battle between {battle_data.track1} and {battle_data.track2} has started!",
        **result
    }

@app.get("/battle/{battle_id}/winner")
async def get_battle_winner(battle_id: str):
    """Get the winner of a specific battle."""
    return await get_winner(battle_id)

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {"error": str(exc.detail)}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return {"error": "An unexpected error occurred"}