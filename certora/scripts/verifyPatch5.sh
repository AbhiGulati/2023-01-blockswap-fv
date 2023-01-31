#!/bin/sh

f="certora/tests/certora/bug5.patch"

if [[ "$1" ]]
then
    MSG="$1"
else
    MSG="msg"
fi

echo "Applying $f"
git apply $f;
echo "Running script"
# for script in certora/scripts/*.sh
# do
#     echo "Running $script"
#     sh $script
# done
certora/scripts/verifySyndicate.sh "$MSG" getUnprocessedETHForAllCollateralizedSlot_dependsOnNumberOfKnots
echo "Reverting $f"
git apply -R $f
