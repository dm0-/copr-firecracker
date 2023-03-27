# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate crc64

Name:           rust-crc64
Version:        1.0.0
Release:        %autorelease
Summary:        CRC64 checksum implementation

License:        BSD-3-Clause
URL:            https://crates.io/crates/crc64
Source:         %{crates_source}
# Manually created patch for downstream crate metadata changes
# * prevent crc64 binary from being built and shipped
Patch:          crc64-fix-metadata.diff

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
CRC64 checksum implementation.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE
%doc %{crate_instdir}/CHANGELOG.md
%doc %{crate_instdir}/README.md
%{crate_instdir}/

%package     -n %{name}+default-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+default-devel %{_description}

This package contains library source intended for building other packages which
use the "default" feature of the "%{crate}" crate.

%files       -n %{name}+default-devel
%ghost %{crate_instdir}/Cargo.toml

%prep
%autosetup -n %{crate}-%{version_no_tilde} -p1
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
%cargo_install

%if %{with check}
%check
%cargo_test
%endif

%changelog
%autochangelog
