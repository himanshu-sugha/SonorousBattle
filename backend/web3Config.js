const { Web3 } = require("web3");
const dotenv = require('dotenv');

dotenv.config();


const contractAddress = process.env.CONTRACT_ADDRESS;
const privateKey = process.env.PRIVATE_KEY;

if (!contractAddress || !privateKey) {
    console.error("Missing required environment variables:");
    if (!contractAddress) console.error("- CONTRACT_ADDRESS is not set");
    if (!privateKey) console.error("- PRIVATE_KEY is not set");
    process.exit(1); 
}


const web3 = new Web3("http://127.0.0.1:8545");

// Load contract ABI and address
const contractABI = require("../artifacts/contracts/MusicBattle.sol/MusicBattle.json").abi;

// Create contract instance
const contract = new web3.eth.Contract(contractABI, contractAddress);

module.exports = { web3, contract, privateKey };

