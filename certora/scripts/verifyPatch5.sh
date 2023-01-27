#!/bin/sh

f="certora/tests/certora/bug5.patch"

echo "Applying $f"
git apply $f;
echo "Running script"
# for script in certora/scripts/*.sh
# do
#     echo "Running $script"
#     sh $script
# done
certora/scripts/verifySyndicate.sh msg getUnprocessedETHForAllCollateralizedSlot_dependsOnNumberOfKnots
echo "Reverting $f"
git apply -R $f