module.exports = {
    contractAddress: "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
    abi: [
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "track1",
          "type": "string"
        },
        {
          "indexed": false,
          "internalType": "string",
          "name": "track2",
          "type": "string"
        }
      ],
      "name": "BattleCreated",
      "type": "event"
    },
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "battleId",
          "type": "uint256"
        },
        {
          "indexed": false,
          "internalType": "uint256",
          "name": "trackNumber",
          "type": "uint256"
        },
        {
          "indexed": false,
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
          "internalType": "uint256",
          "name": "votesTrack1",
          "type": "uint256"
        },
        {
          "internalType": "uint256",
          "name": "votesTrack2",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
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
      "stateMutability": "nonpayable",
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
        }
      ],
      "name": "vote",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    }
  ],
  };
  