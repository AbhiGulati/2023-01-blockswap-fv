using MocksETHReturnsFalse as sETHToken

methods {
    //// Regular methods
    totalETHReceived() returns (uint256) envfree
    calculateETHForFreeFloatingOrCollateralizedHolders() returns (uint256) envfree;
    getUnprocessedETHForAllCollateralizedSlot() returns (uint256) envfree;
    updateAccruedETHPerShares() envfree;
    updatePriorityStakingBlock(uint256);

    // public variables
    owner() returns (address) envfree;
    accumulatedETHPerFreeFloatingShare() returns (uint256) envfree;
    accumulatedETHPerCollateralizedSlotPerKnot() returns (uint256) envfree;
    lastSeenETHPerCollateralizedSlotPerKnot() returns (uint256) envfree;
    lastSeenETHPerFreeFloating() returns (uint256) envfree;
    totalFreeFloatingShares() returns (uint256) envfree;
    totalClaimed() returns (uint256) envfree;
    numberOfRegisteredKnots() returns (uint256) envfree;
    isKnotRegistered(bytes32) returns (bool) envfree;
    priorityStakingEndBlock() returns (uint256) envfree;
    isPriorityStaker(address) returns (bool) envfree;
    // sETHTotalStakeForKnot(bytes32) returns (uint256) envfree;
    // sETHStakedBalanceForKnot() returns () envfree; // new getter needed
    // sETHUserClaimForKnot() returns () envfree; // new getter needed
    // totalETHProcessedPerCollateralizedKnot(bytes32) returns (uint256) envfree; // apparently this is harnessed
    // accruedEarningPerCollateralizedSlotOwnerOfKnot // new getter needed (?)
    // claimedPerCollateralizedSlotOwnerOfKnot // new getter needed (?)
    isNoLongerPartOfSyndicate(bytes32) returns (bool) envfree;
    lastAccumulatedETHPerFreeFloatingShare(bytes32) returns (uint256) envfree;


    // added harness calls
    getSETHStakedBalanceForKnot(bytes32, address) returns (uint256) envfree;
    getIsActiveKnot(bytes32) returns (bool) envfree;


    //// Resolving external calls
	// stakeHouseUniverse
	stakeHouseKnotInfo(bytes32) returns (address,address,address,uint256,uint256,bool) => DISPATCHER(true)
    memberKnotToStakeHouse(bytes32) returns (address) => DISPATCHER(true) // not used directly by Syndicate
    // stakeHouseRegistry
    getMemberInfo(bytes32) returns (address,uint256,uint16,bool) => DISPATCHER(true) // not used directly by Syndicate
    // slotSettlementRegistry
	stakeHouseShareTokens(address) returns (address)  => DISPATCHER(true)
	currentSlashedAmountOfSLOTForKnot(bytes32) returns (uint256)  => DISPATCHER(true)
	numberOfCollateralisedSlotOwnersForKnot(bytes32) returns (uint256)  => DISPATCHER(true)
	getCollateralisedOwnerAtIndex(bytes32, uint256) returns (address) => DISPATCHER(true)
	totalUserCollateralisedSLOTBalanceForKnot(address, address, bytes32) returns (uint256) => DISPATCHER(true)
    getETHBalance(address) returns (uint) envfree;

    // sETH
    sETHToken.balanceOf(address) returns (uint256) envfree
    // ERC20
    name()                                returns (string)  => DISPATCHER(true)
    symbol()                              returns (string)  => DISPATCHER(true)
    decimals()                            returns (string) envfree => DISPATCHER(true)
    totalSupply()                         returns (uint256) => DISPATCHER(true)
    balanceOf(address)                    returns (uint256) => DISPATCHER(true)
    allowance(address,address)            returns (uint)    => DISPATCHER(true)
    approve(address,uint256)              returns (bool)    => DISPATCHER(true)
    transfer(address,uint256)             returns (bool)    => DISPATCHER(true)
    transferFrom(address,address,uint256) returns (bool)    => DISPATCHER(true)

    //// Harnessing
    // harnessed variables
    accruedEarningPerCollateralizedSlotOwnerOfKnot(bytes32,address) returns (uint256) envfree
    totalETHProcessedPerCollateralizedKnot(bytes32) returns (uint256) envfree
    sETHStakedBalanceForKnot(bytes32,address) returns (uint256) envfree
    sETHTotalStakeForKnot(bytes32) returns (uint256) envfree
    // harnessed functions
    deRegisterKnots(bytes32) 
    deRegisterKnots(bytes32,bytes32)
    stake(bytes32,uint256,address)
    stake(bytes32,bytes32,uint256,uint256,address)
    unstake(address,address,bytes32,uint256)
    unstake(address,address,bytes32,bytes32,uint256,uint256)
    claimAsStaker(address,bytes32)
    claimAsStaker(address,bytes32,bytes32)
    claimAsCollateralizedSLOTOwner(address,bytes32)
    claimAsCollateralizedSLOTOwner(address,bytes32,bytes32)
    registerKnotsToSyndicate(bytes32)
    registerKnotsToSyndicate(bytes32,bytes32)
    addPriorityStakers(address)
    addPriorityStakers(address,address)
    batchUpdateCollateralizedSlotOwnersAccruedETH(bytes32)
    batchUpdateCollateralizedSlotOwnersAccruedETH(bytes32,bytes32)
}

/*
 * A successful call to `unstake` in which the caller requests a positive amount
 *  should result in an increase to the recipient's ETH balance.
 */ 
rule unstakingIncreasesSETHAmount() {
    env e;
    address _unclaimedETHRecipient; address _sETHRecipient;
    bytes32 blsKey; uint256 sETHAmount;

    require sETHAmount > 0;
    require _sETHRecipient != currentContract;

    uint _sETHBalance = sETHToken.balanceOf(_sETHRecipient);

    unstake(e, _unclaimedETHRecipient, _sETHRecipient, blsKey, sETHAmount);

    uint sETHBalance_ = sETHToken.balanceOf(_sETHRecipient);

    assert sETHBalance_ > _sETHBalance;
}