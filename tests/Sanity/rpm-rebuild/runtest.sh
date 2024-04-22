#!/bin/bash
# vim: dict+=/usr/share/beakerlib/dictionary.vim cpt=.,w,b,u,t,i,k
. /usr/share/beakerlib/beakerlib.sh || exit 1

PACKAGE="$(rpm -qf $(which rustc))"

rlJournalStart
    rlPhaseStartSetup
        rlAssertRpm $PACKAGE || rlDie "rustc not found. Aborting testcase..."
        rlRun "TmpDir=\$(mktemp -d)" 0 "Creating tmp directory"
        rlRun "pushd $TmpDir"

        if [[ "x" == "x${PKG_TO_BUILD}" ]]; then
            rlLogError "No package was configured to build."
            rlDie "The package must be passed over PKG_TO_BUILD environment variable."
        fi

    rlPhaseEnd

    rlPhaseStart FAIL ${PKG_TO_BUILD}FetchSrcAndInstallBuildDeps
        if ! rlCheckRpm $PKG_TO_BUILD; then
            rlRun "yum install -y $PKG_TO_BUILD ${YUM_SWITCHES}"
            rlAssertRpm $PKG_TO_BUILD
        fi
        rlFetchSrcForInstalled $PKG_TO_BUILD
        rlRun SRPM=$(ls -1 *.src.rpm)
        rlRun "rpm -ivh $SRPM"
        rlRun SPECDIR="$(rpm -E '%{_specdir}')"
        # Note about the spec file name: When packaging rust crates, the package
        # is named rust-<crate>, as well as the spec file, but the rpm package
        # (the one we use in dnf to install and query) is named as the crate,
        # (without the "rust-" prefix). We have to take that into account to
        # find the spec:
        # https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/#_package_naming
        rlRun "SPECNAME=$(rpm -ql $SRPM | grep .spec)"

        # Packages built with rust usually contains dynamic dependencies.
        # builddep needs to be run from the srpm, not the spec file, to be able
        # to generate them:
        # https://fedoraproject.org/wiki/Changes/DynamicBuildRequires#rpmbuild
        rlRun "yum-builddep -y ${SRPM} ${YUM_SWITCHES}"
    rlPhaseEnd

    rlPhaseStartTest
        set -o pipefail
        rlRun "rpmbuild -bb ${SPECDIR}/${SPECNAME} |& tee ${SRPM}_rpmbuild.log"
        rlFileSubmit "${SRPM}_rpmbuild.log"
    rlPhaseEnd

    rlPhaseStartCleanup
        rlRun "popd"
        rlRun "rm -r $TmpDir" 0 "Removing tmp directory"
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
