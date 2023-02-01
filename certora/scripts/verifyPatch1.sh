#!/bin/sh

f="certora/tests/certora/bug1.patch"

if [[ "$1" ]]
then
    MSG="$1"
else
    MSG="msg"
fi

echo "Applying $f"
git apply $f;
echo "Running script"

certoraRun  certora/harnesses/SyndicateHarness.sol \
    certora/harnesses/MockStakeHouseUniverse.sol \
    certora/harnesses/MockStakeHouseRegistry.sol \
    certora/harnesses/MockSlotSettlementRegistry.sol \
    certora/harnesses/MocksETHReturnsFalse.sol \
    --verify SyndicateHarness:certora/specs/Syndicate-patch1.spec \
    --cloud master \
    --optimistic_loop \
    --optimize 1 \
    --loop_iter 3 \
    --rule unstakingIncreasesSETHAmount \
    --rule_sanity \
    --settings -optimisticFallback=true \
    --packages @blockswaplab=node_modules/@blockswaplab @openzeppelin=node_modules/@openzeppelin \
    --msg "$MSG" \
    $3

echo "Reverting $f"
git apply -R $f
