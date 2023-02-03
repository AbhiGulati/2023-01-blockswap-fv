using MocksETH as sETHToken

methods {
    //// Regular methods
    totalETHReceived() returns (uint256) envfree
    calculateETHForFreeFloatingOrCollateralizedHolders() returns (uint256) envfree;
    getUnprocessedETHForAllCollateralizedSlot() returns (uint256) envfree;
    updateAccruedETHPerShares() envfree;
    updatePriorityStakingBlock(uint256);
    previewUnclaimedETHAsFreeFloatingStaker(address, bytes32) returns (uint256) envfree;
    getUnprocessedETHForAllFreeFloatingSlot() returns (uint256) envfree;

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
    PRECISION() returns (uint256) envfree;
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
    getSETHUserClaimForKnot(bytes32, address) returns (uint256) envfree;


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
rule canNotDeregisterUnregisteredKnot(method f) filtered {
    f -> notHarnessCall(f)
} {
    bytes32 knot; env e;
    require !isKnotRegistered(knot);

    deRegisterKnots@withrevert(e, knot);

    assert lastReverted, "deRegisterKnots must revert if knot is not registered";
}

/*
 * A successful call to `unstake` in which the caller requests a positive amount
 *  should result in an increase to the recipient's ETH balance.
 * Note: This rule fails when bug1.patch is applied
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

/**
 * Address 0 must have zero staked sETH balance.
 */
invariant addressZeroHasNoStakedBalance(bytes32 blsKey)
    getSETHStakedBalanceForKnot(blsKey, 0) == 0

/*
 * `getUnprocessedETHForAllCollateralizedSlot` should return the collateralized
 *   unprocessed ETH divided by the number of knots
 * Note: This rule fails when bug5.patch is applied
 */ 
rule getUnprocessedETHForAllCollateralizedSlot_dependsOnNumberOfKnots() {
    require numberOfRegisteredKnots() > 0;

    uint diff = calculateETHForFreeFloatingOrCollateralizedHolders() - lastSeenETHPerCollateralizedSlotPerKnot();

    uint actual = getUnprocessedETHForAllCollateralizedSlot();
    uint expected = diff / numberOfRegisteredKnots();

    assert expected == actual;
}

/*
 * When number of knots is > 0 and free floating shares > 0, after calling 
 *  `updateAccruedETHPerShares` the "last seen" values should be same for 
 *  collateralized and free floating.
 */
rule ethForSlotTypesIsEqualAfterUpdateAccrued() {
    require numberOfRegisteredKnots() > 0;
    require totalFreeFloatingShares() > 0;

    updateAccruedETHPerShares();

    assert lastSeenETHPerCollateralizedSlotPerKnot() == lastSeenETHPerFreeFloating();
}

/*
 * Amount of ETH received by staker after calling `claimAsStaker` is the same
 *  regardless of whether `updateAccruedETHPerShares` is called immediately
 *  prior.
 */
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
 * Attempt to register a knot that is already registered will fail
 */ 
rule doubleRegisterWillFail() {
    env e;
    bytes32 blsKey;
    registerKnotsToSyndicate(e, blsKey);

    registerKnotsToSyndicate@withrevert(e, blsKey);

    assert lastReverted;
}

/*
 * Attempt to register an inactive knot that will fail
 */
rule registeringInactiveWillFail() {
    env e;
    bytes32 blsKey;

    require !getIsActiveKnot(blsKey);

    registerKnotsToSyndicate@withrevert(e, blsKey);

    assert lastReverted;
}

/*
 * `registerKnotsToSyndicate` can only be called by owner
 */
rule permissioned_registerKnotsToSyndicate(env e, bytes32 blsKey) {
    registerKnotsToSyndicate(e, blsKey);

    assert e.msg.sender == owner();
}

/*
 * `deRegisterKnots` can only be called by owner
 */
rule permissioned_deRegisterKnots(env e, bytes32 blsKey) {
    deRegisterKnots(e, blsKey);
    assert e.msg.sender == owner();
}

/*
 * `addPriorityStakers` can only be called by owner
 */
rule permissioned_addPriorityStakers(env e, address user) {
    addPriorityStakers(e, user);
    assert e.msg.sender == owner();
}

/*
 * `updatePriorityStakingBlock` can only be called by owner
 */
rule permissioned_updatePriorityStakingBlock(env e, uint256 endBlock) {
    updatePriorityStakingBlock(e, endBlock);
    assert e.msg.sender == owner();
}

/*
 * An address that is not a priority staker cannot have stake before 
 *  `priorityStakingEndBlock` (unless the block has been moved forward)
 */
invariant noWhitelistNoStake(env e, address user, bytes32 blsKey)
    e.block.number < priorityStakingEndBlock() && !isPriorityStaker(user) => getSETHStakedBalanceForKnot(blsKey, user) == 0
    filtered {
        f -> f.selector != initialize(address,uint256,address[],bytes32[]).selector && f.selector != updatePriorityStakingBlock(uint256).selector
    }
    {
        preserved with (env e1) {
            require e1.block.number == e.block.number;
        }
    }


/*
 * Amount of ETH received by staker after calling `claimAsCollateralizedSLOTOwner` 
 * is the same regardless of whether `updateAccruedETHPerShares` is called 
 * immediately prior.
 */
rule claimAsCollateralizedSLOTOwnerUpdatesAccrued() {
    env e;
    address user;
    bytes32 blsKey1;
    bytes32 blsKey2;

    storage init = lastStorage;

    claimAsCollateralizedSLOTOwner(e, user, blsKey1, blsKey2);
    uint userBalance1 = getETHBalance(user);

    updateAccruedETHPerShares() at init;
    claimAsCollateralizedSLOTOwner(e, user, blsKey1, blsKey2);
    uint userBalance2 = getETHBalance(user);

    assert userBalance1 == userBalance2;
}

/*
 * Unstaking only decreases the `totalFreeFloatingShares` iff the KNOT we 
 *  are unstaking from is still active
 */
rule unstakeOnlyDecreasesTotalFreeFloatingSharesIfKnotStillActive() {
    uint totalFreeFloatingSharesBefore = totalFreeFloatingShares();

    env e;
    address _unclaimedETHRecipient; address _sETHRecipient;
    bytes32 blsKey; uint256 sETHAmount;

    require sETHAmount > 0;
    require _sETHRecipient != currentContract;

    unstake(e, _unclaimedETHRecipient, _sETHRecipient, blsKey, sETHAmount);

    uint totalFreeFloatingSharesAfter = totalFreeFloatingShares();

    assert totalFreeFloatingSharesBefore == totalFreeFloatingSharesAfter <=> isNoLongerPartOfSyndicate(blsKey);
}

/*
 *  A KNOT which has not yet been deRegistered will not have a value 
 *   set for lastAccumulatedETHPerFreeFloatingShare
 */ 
invariant notDeregisteredKnotHasNoLastAccumulatedETHPerFreeFloatingShare(bytes32 blsKey)
    !isNoLongerPartOfSyndicate(blsKey) => lastAccumulatedETHPerFreeFloatingShare(blsKey) == 0

/*
 *  The lastAccumulatedETHPerFreeFloatingShare for any KNOT is always less than
 *   the global accumulatedETHPerFreeFloatingShare
 */
invariant accumulatedETHPerFreeFloatingShare_gt_lastAccumulatedETHPerFreeFloatingShare(bytes32 blsKey)
    lastAccumulatedETHPerFreeFloatingShare(blsKey) <= accumulatedETHPerFreeFloatingShare()


/*
 * accumulatedETHPerFreeFloatingShare increases monotonically
 */
rule accumulatedETHPerFreeFloatingShareMonotonicallyIncreases(method f) filtered {
    f -> notHarnessCall(f)
}{
    uint256 _accumulatedETHPerFreeFloatingShare = accumulatedETHPerFreeFloatingShare();

    env e; calldataarg args;
    f(e, args);

    uint256 accumulatedETHPerFreeFloatingShare_ = accumulatedETHPerFreeFloatingShare();

    assert accumulatedETHPerFreeFloatingShare_ >= _accumulatedETHPerFreeFloatingShare, "accumulatedETHPerFreeFloatingShare must not decrease";
}

/*
 * accumulatedETHPerCollateralizedSlotPerKnot increases monotonically
 */
rule accumulatedETHPerCollateralizedSlotPerKnotMonotonicallyIncreases(method f) filtered {
    f -> notHarnessCall(f)
}{
    uint256 _accumulatedETHPerCollateralizedSlotPerKnot = accumulatedETHPerCollateralizedSlotPerKnot();

    env e; calldataarg args;
    f(e, args);

    uint256 accumulatedETHPerCollateralizedSlotPerKnot_ = accumulatedETHPerCollateralizedSlotPerKnot();

    assert accumulatedETHPerCollateralizedSlotPerKnot_ >= _accumulatedETHPerCollateralizedSlotPerKnot, "accumulatedETHPerCollateralizedSlotPerKnot must not decrease";
}

ghost mapping(bytes32 => uint256) sumOfStakesForKnot {
    init_state axiom forall bytes32 blsKey.
        sumOfStakesForKnot[blsKey] == 0;
}

hook Sstore sETHStakedBalanceForKnot[KEY bytes32 a][KEY address b] uint256 new_value (uint256 old_value) STORAGE {
    sumOfStakesForKnot[a] = sumOfStakesForKnot[a] + new_value - old_value;
}

/*
 * Sum of stakes for all stakers in KNOT equals `sETHTotalStakeForKnot`
 */
invariant totalStakeForKnotEqualsSumOfStakesBalances(bytes32 blsKey)
    sumOfStakesForKnot[blsKey] == sETHTotalStakeForKnot(blsKey)

/*
 * Check that user's sETH claim is set according to their new staked balance
 * Note: This rule fails when bug9.patch is applied
 */
rule unstakeUpdatesSETHUserClaimForKnot() {
    env e;
    address _unclaimedETHRecipient; address _sETHRecipient;
    bytes32 blsKey; uint256 sETHAmount;

    requireInvariant totalStakeForKnotEqualsSumOfStakesBalances(blsKey);
    requireInvariant notDeregisteredKnotHasNoLastAccumulatedETHPerFreeFloatingShare(blsKey);

    require totalFreeFloatingShares() > 0;
    require numberOfRegisteredKnots() > 0;
    require !isNoLongerPartOfSyndicate(blsKey);
    require sETHAmount > 0;
    require _sETHRecipient != currentContract;
    require(e.msg.sender != 0);

    unstake(e, _unclaimedETHRecipient, _sETHRecipient, blsKey, sETHAmount);

    assert getSETHUserClaimForKnot(blsKey, e.msg.sender) == accumulatedETHPerFreeFloatingShare() * getSETHStakedBalanceForKnot(blsKey, e.msg.sender) / PRECISION();
    assert previewUnclaimedETHAsFreeFloatingStaker(e.msg.sender, blsKey) == 0;
}

/*
 *******************************
 * Unverified or failing
 *******************************
 */





// invariant numberOfRegisteredKnotsIs0MeansNoRegisteredKnots(bytes32 blsKey)
//     numberOfRegisteredKnots() == 0 => !isKnotRegistered(blsKey) || isNoLongerPartOfSyndicate(blsKey)


/*
ghost mathint number_registered_knots {
    init_state axiom number_registered_knots == 0;
}

ghost mapping(bytes32 => bool) is_NoLongerPartOfSyndicate;

ghost mapping(bytes32 => bool) is_KnotRegistered;

hook Sstore isNoLongerPartOfSyndicate[KEY bytes32 a] bool new_value (bool old_value) STORAGE {
    is_NoLongerPartOfSyndicate[a] = new_value;

    number_registered_knots = (new_value && !old_value && is_KnotRegistered[a])
        ? number_registered_knots - 1
        : (!new_value && old_value && is_KnotRegistered[a]
            ? number_registered_knots + 1
            : number_registered_knots); */
    // if (new_value && !old_value && is_KnotRegistered[a]) {
    //     number_registered_knots = number_registered_knots - 1;
    // } else if (!new_value && old_value && is_KnotRegistered[a]) {
    //     number_registered_knots = number_registered_knots + 1;
    // }
//}
/*
hook Sload bool new_value isNoLongerPartOfSyndicate[KEY bytes32 a] STORAGE {
    is_NoLongerPartOfSyndicate[a] = new_value;
}

hook Sstore isKnotRegistered[KEY bytes32 a] bool new_value (bool old_value) STORAGE {
    is_KnotRegistered[a] = new_value;

    number_registered_knots = (new_value && !old_value && !is_NoLongerPartOfSyndicate[a])
        ? number_registered_knots + 1
        : (!new_value && old_value && !is_NoLongerPartOfSyndicate[a]
            ? number_registered_knots - 1
            : number_registered_knots); */
    // if (new_value && !old_value && !is_NoLongerPartOfSyndicate[a]) {
    //     number_registered_knots = number_registered_knots + 1;
    // } else if (!new_value && old_value && !is_NoLongerPartOfSyndicate[a]) {
    //     number_registered_knots = number_registered_knots - 1;
    // }
//}
/*
hook Sload bool new_value isKnotRegistered[KEY bytes32 a] STORAGE {
    is_KnotRegistered[a] = new_value;
}

invariant numberOfRegisteredKnotsIsNumberOfRegisteredKnots(bytes32 blsKey)
    numberOfRegisteredKnots() == number_registered_knots
*/


// invariant that after something is deregistered it can never receive ETH
// Hm I don't have any way to see the change since before `deRegisterKnots` was
// called vs after.

