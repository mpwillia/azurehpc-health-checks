VERSION="$1"
WORKING_DIR="$2"

AZ_NHC_DIR="azurehpc-health-checks-$VERSION"

pushd $WORKING_DIR/$AZ_NHC_DIR

sudo ./install-nhc.sh