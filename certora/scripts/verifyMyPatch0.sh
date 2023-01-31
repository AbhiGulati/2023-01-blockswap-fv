#!/bin/sh

f="certora/tests/participants/bug0.patch"

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
certora/scripts/verifySyndicate.sh "$MSG" claimAsStakerUpdatesAccrued
echo "Reverting $f"
git apply -R $f
