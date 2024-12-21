const hre = require("hardhat");

async function main() {
    // Check if we're on localhost/hardhat network
    const network = await hre.ethers.provider.getNetwork();
    console.log("Deploying to network:", network.name);

    let timeFeedAddress;

    // Set different addresses based on network
    if (network.name === "hardhat" || network.name === "localhost") {
        // For local testing, use zero address
        timeFeedAddress = "0x0000000000000000000000000000000000000000";
        console.log("Using local testing configuration with zero address for time feed");
    } else if (network.name === "sepolia") {
        // For Sepolia testnet (you would need to replace this with actual Sepolia time feed address)
        timeFeedAddress = "YOUR_SEPOLIA_TIME_FEED_ADDRESS";
        console.log("Using Sepolia network configuration");
    } else if (network.name === "mainnet") {
        // For mainnet (you would need to replace this with actual mainnet time feed address)
        timeFeedAddress = "YOUR_MAINNET_TIME_FEED_ADDRESS";
        console.log("Using mainnet configuration");
    } else {
        // Default to zero address for unknown networks
        timeFeedAddress = "0x0000000000000000000000000000000000000000";
        console.log("Unknown network, using zero address for time feed");
    }

    // Deploy contract
    console.log("Deploying MusicBattle contract...");
    const MusicBattle = await hre.ethers.getContractFactory("MusicBattle");
    const musicBattle = await MusicBattle.deploy(timeFeedAddress);
  
    // Wait for the contract to be deployed
    await musicBattle.waitForDeployment();
  
    // Get the address of the deployed contract
    const contractAddress = await musicBattle.target;
  
    // Get deployer's signer
    const [deployer] = await hre.ethers.getSigners();
  
    // Log deployment information
    console.log("\nDeployment Information:");
    console.log("----------------------");
    console.log("Network:", network.name);
    console.log("Time Feed Address:", timeFeedAddress);
    console.log("Deployer's address:", deployer.address);
  
    // Log deployer's balance
    const deployerBalance = await hre.ethers.provider.getBalance(deployer.address);
    console.log("Deployer's balance:", hre.ethers.formatEther(deployerBalance), "ETH");
  
    // Log deployed contract's address
    console.log("Contract deployed at:", contractAddress);
  
    // Log deployed contract's initial balance
    const contractBalance = await hre.ethers.provider.getBalance(contractAddress);
    console.log("Contract's initial balance:", hre.ethers.formatEther(contractBalance), "ETH");

    // Verify contract on Etherscan if not on local network
    if (network.name !== "hardhat" && network.name !== "localhost") {
        console.log("\nVerifying contract on Etherscan...");
        try {
            await hre.run("verify:verify", {
                address: contractAddress,
                constructorArguments: [timeFeedAddress],
            });
            console.log("Contract verified on Etherscan");
        } catch (error) {
            console.log("Error verifying contract:", error.message);
        }
    }
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Deployment error:", error);
        process.exit(1);
    });

// async function main() {
//         // Deploy contract
//         const MusicBattle = await hre.ethers.getContractFactory("MusicBattle");
//         const musicBattle = await MusicBattle.deploy();
      
//         // Wait for the contract to be deployed
//         await musicBattle.waitForDeployment();
      
//         // Get the address of the deployed contract
//         const contractAddress = await musicBattle.target;
      
//         console.log("Contract deployed at:", contractAddress);
//         console.log("deployer address,")
      
//         // Get deployer's signer
//         const [deployer] = await hre.ethers.getSigners();
      
//         // Log deployer's balance before funding
//         // const balanceBefore = await hre.ethers.provider.getBalance(deployer.address);
//         // console.log("Balance Before:", balanceBefore.toString());
//         // console.log("Deployer's balance before funding:", hre.ethers.formatEther(balanceBefore), "ETH");
      
//         // Funding amount
//         // const fundingAmount = "50"; // Desired funding amount in ETH
      
//         // Fund the contract
//         const tx = await deployer.sendTransaction({
//           to: contractAddress,
//         //   value: hre.ethers.parseEther(fundingAmount),
//         });
//         await tx.wait();
      
//         // console.log(`Contract funded with ${fundingAmount} ETH`);
      
//         // Log deployer's balance after funding
//         // const balanceAfter = await hre.ethers.provider.getBalance(deployer.address);
//         // console.log("Balance After:", balanceAfter.toString());
//         // console.log("Deployer's balance after funding:", hre.ethers.formatEther(balanceAfter), "ETH");
      
//         // Log the deployed contract's balance
//         // const contractBalance = await hre.ethers.provider.getBalance(contractAddress);
//         // console.log("Contract's balance:", hre.ethers.formatEther(contractBalance), "ETH");
      
//         // Optional: Calculate the gas used
//         // const gasUsed = balanceBefore.sub(balanceAfter).sub(hre.ethers.parseEther(fundingAmount));
//         // console.log("Gas used for deployment and funding:", hre.ethers.formatEther(gasUsed), "ETH");
//       }
      