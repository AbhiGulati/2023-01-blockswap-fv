using MocksETHReturnsFalse as sETHToken

methods {
    //// Regular methods
    totalETHReceived() returns (uint256) envfree
    calculateETHForFreeFloatingOrCollateralizedHolders() returns (uint256) envfree;
    getUnprocessedETHForAllCollateralizedSlot() returns (uint256) envfree;
    updateAccruedETHPerShares() envfree;

    // public variables
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
    registerKnotsToSyndicate(bytes32) envfree;
    registerKnotsToSyndicate(bytes32,bytes32) envfree;
    addPriorityStakers(address)
    addPriorityStakers(address,address)
    batchUpdateCollateralizedSlotOwnersAccruedETH(bytes32)
    batchUpdateCollateralizedSlotOwnersAccruedETH(bytes32,bytes32)
}

/// We defined additional functions to get around the complexity of defining dynamic arrays in cvl. We filter them in 
/// normal rules and invariants as they serve no purpose.
definition notHarnessCall(method f) returns bool = 
    f.selector != batchUpdateCollateralizedSlotOwnersAccruedETH(bytes32).selector
    && f.selector != batchUpdateCollateralizedSlotOwnersAccruedETH(bytes32,bytes32).selector
    && f.selector != deRegisterKnots(bytes32).selector
    && f.selector != deRegisterKnots(bytes32,bytes32).selector
    && f.selector != stake(bytes32,uint256,address).selector
    && f.selector != stake(bytes32,bytes32,uint256,uint256,address).selector
    && f.selector != unstake(address,address,bytes32,uint256).selector
    && f.selector != unstake(address,address,bytes32,bytes32,uint256,uint256).selector
    && f.selector != claimAsStaker(address,bytes32).selector
    && f.selector != claimAsStaker(address,bytes32,bytes32).selector
    && f.selector != claimAsCollateralizedSLOTOwner(address,bytes32).selector
    && f.selector != claimAsCollateralizedSLOTOwner(address,bytes32,bytes32).selector
    && f.selector != registerKnotsToSyndicate(bytes32).selector
    && f.selector != registerKnotsToSyndicate(bytes32,bytes32).selector
    && f.selector != addPriorityStakers(address).selector
    && f.selector != addPriorityStakers(address,address).selector;


/// Corrollary that can be used as requirement after sETH solvency is proven.
function sETHSolvencyCorrollary(address user1, address user2, bytes32 knot) returns bool {
    return sETHStakedBalanceForKnot(knot,user1) + sETHStakedBalanceForKnot(knot,user2) <= sETHTotalStakeForKnot(knot);
}


/*
 *******************************
 * Verified
 *******************************
 */

/**
 * An unregistered knot can not be deregistered.
 */
rule canNotDegisterUnregisteredKnot(method f) filtered {
    f -> notHarnessCall(f)
} {
    bytes32 knot; env e;
    require !isKnotRegistered(knot);

    deRegisterKnots@withrevert(e, knot);

    assert lastReverted, "deRegisterKnots must revert if knot is not registered";
}


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

/**
 * Total ETH received must not decrease.
 */
rule totalEthReceivedMonotonicallyIncreases(method f) filtered {
    f -> notHarnessCall(f)
}{
    
    uint256 totalEthReceivedBefore = totalETHReceived();

    env e; calldataarg args;
    f(e, args);

    uint256 totalEthReceivedAfter = totalETHReceived();

    assert totalEthReceivedAfter >= totalEthReceivedBefore, "total ether received must not decrease";
}

/**
 * Address 0 must have zero sETH balance.
 */
invariant addressZeroHasNoBalance()
    sETHToken.balanceOf(0) == 0

invariant addressZeroHasNoStakedBalance(bytes32 blsKey)
    getSETHStakedBalanceForKnot(blsKey, 0) == 0


rule getUnprocessedETHForAllCollateralizedSlot_dependsOnNumberOfKnots() {
    require numberOfRegisteredKnots() > 0;

    uint diff = calculateETHForFreeFloatingOrCollateralizedHolders() - lastSeenETHPerCollateralizedSlotPerKnot();

    uint actual = getUnprocessedETHForAllCollateralizedSlot();
    uint expected = diff / numberOfRegisteredKnots();

    assert expected == actual;
}

rule ethForSlotTypesIsEqualAfterUpdateAccrued() {
    require numberOfRegisteredKnots() > 0;
    require totalFreeFloatingShares() > 0;

    updateAccruedETHPerShares();

    assert lastSeenETHPerCollateralizedSlotPerKnot() == lastSeenETHPerFreeFloating();
}


rule claimAsStakerUpdatesAccrued() {
    env e;
    address user;
    bytes32 blsKey1;
    bytes32 blsKey2;

    storage init = lastStorage;

    claimAsStaker(e, user, blsKey1, blsKey2);
    uint userBalance1 = getETHBalance(user);

    updateAccruedETHPerShares() at init;
    claimAsStaker(e, user, blsKey1, blsKey2);
    uint userBalance2 = getETHBalance(user);

    assert userBalance1 == userBalance2;
}

/*
 *******************************
 * Unverified or failing
 *******************************
 */

invariant noWhitelistNoStake(env e, address user, bytes32 blsKey)
    e.block.number < priorityStakingEndBlock() && !isPriorityStaker(user) => getSETHStakedBalanceForKnot(blsKey, user) == 0

    {preserved with (env e1) {
        require e1 == e;
    }}


// invariant numberOfRegisteredKnotsIs0MeansNoRegisteredKnots(bytes32 blsKey)
//     numberOfRegisteredKnots() == 0 => !isKnotRegistered(blsKey) || isNoLongerPartOfSyndicate(blsKey)

ghost mathint number_registered_knots {
    init_state axiom number_registered_knots == 0;
}

ghost mapping(bytes32 => bool) is_NoLongerPartOfSyndicate;

ghost mapping(bytes32 => bool) is_KnotRegistered;

hook Sstore isNoLongerPartOfSyndicate[KEY bytes32 a] bool new_value (bool old_value) STORAGE {
    is_NoLongerPartOfSyndicate[a] = new_value;

    if (new_value && !old_value && is_KnotRegistered[a]) {
        number_registered_knots = number_registered_knots - 1;
    } else if (!new_value && old_value && is_KnotRegistered[a]) {
        number_registered_knots = number_registered_knots + 1;
    }
}

hook Sload bool new_value isNoLongerPartOfSyndicate[KEY bytes32 a] STORAGE {
    is_NoLongerPartOfSyndicate[a] = new_value;
}

hook Sstore isKnotRegistered[KEY bytes32 a] bool new_value (bool old_value) STORAGE {
    is_KnotRegistered[a] = new_value;
    if (new_value && !old_value && !is_NoLongerPartOfSyndicate[a]) {
        number_registered_knots = number_registered_knots + 1;
    } else if (!new_value && old_value && !is_NoLongerPartOfSyndicate[a]) {
        number_registered_knots = number_registered_knots - 1;
    }
}

hook Sload bool new_value isKnotRegistered[KEY bytes32 a] STORAGE {
    is_KnotRegistered[a] = new_value;
}

invariant numberOfRegisteredKnotsIsNumberOfRegisteredKnots(bytes32 blsKey)
    numberOfRegisteredKnots() == number_registered_knots



// invariant that after something is deregistered it can never receive ETH
// Hm I don't have any way to see the change since before `deRegisterKnots` was
// called vs after.


rule doubleRegisterWillFail() {
    bytes32 blsKey;
    registerKnotsToSyndicate(blsKey);

    registerKnotsToSyndicate@withrevert(blsKey);

    assert lastReverted;
}

rule registeringInactiveWillFail() {
    bytes32 blsKey;

    require !getIsActiveKnot(blsKey);

    registerKnotsToSyndicate@withrevert(blsKey);

    assert lastReverted;
}