const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("MusicBattle Contract", function () {
    let MusicBattle, musicBattle, deployer, addr1, addr2;

    beforeEach(async function () {
        // Deploy contract
        MusicBattle = await ethers.getContractFactory("MusicBattle");
        
        // Modify deployment to work with ethers v6
        musicBattle = await MusicBattle.deploy();
        await musicBattle.waitForDeployment();

        // Get signers
        [deployer, addr1, addr2] = await ethers.getSigners();

        // Send initial funding
        const fundTx = await deployer.sendTransaction({
            to: await musicBattle.getAddress(),
            value: ethers.parseEther("50")
        });
        await fundTx.wait();
    });

    it("Should fund the contract successfully", async function () {
        const balance = await musicBattle.getBalance();
        // Remove decimal places before comparison
        expect(ethers.formatEther(balance).split(".")[0]).to.equal("50");
    });

    it("Should allow funding after deployment", async function () {
        const fundAmount = ethers.parseEther("10");
        await deployer.sendTransaction({ 
            to: await musicBattle.getAddress(), 
            value: fundAmount 
        });

        const balance = await musicBattle.getBalance();
        // Remove decimal places before comparison
        expect(ethers.formatEther(balance).split(".")[0]).to.equal("60");
    });

    it("Should create a battle", async function () {
        const track1 = "Track 1";
        const track2 = "Track 2";
        
        const battleTx = await musicBattle.createBattle(
            track1, 
            track2, 
            addr1.address, 
            addr2.address
        );
        
        const receipt = await battleTx.wait();
        
        // You might want to add more specific assertions
        const battleCount = await musicBattle.battleCount();
        expect(battleCount.toString()).to.equal("1");
    });
});
