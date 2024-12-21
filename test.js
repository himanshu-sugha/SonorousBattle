async function voteTrack(battleId, trackNumber) {
    try {
      // Validate inputs
      if (!battleId || ![1, 2].includes(trackNumber)) {
        throw new Error('Invalid battle ID or track number');
      }
  
      // Verify battle exists
      let battle;
      try{
         battle = await contract.methods.getBattleDetails(battleId).call();
         console.log('battle------',battle)
      }
      catch(err){
        console.log("problem in retrieving battle Id values from getBattleDetails function: error is : ",err)
      }
      // if (!battle || battle.id !== battleId) {
      //   throw new Error("Battle does not exist");
      // }
  
      // Get accounts
      const accounts = await web3.eth.getAccounts();
      const userAddress = accounts[0];
  
      // Prepare vote transaction
      const tx = contract.methods.vote(battleId, trackNumber);
  
      // Estimate gas
      const gas = await tx.estimateGas({ from: userAddress });
  
      // Send transaction
      const receipt = await tx.send({ 
        from: userAddress, 
        gas 
      });
  
      return {
        transactionHash: receipt.transactionHash
      };
    } catch (error) {
      console.error('Vote Track Error:', error);
      throw error;
    }
  }