# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate versionize

Name:           rust-versionize
Version:        0.1.9
Release:        %autorelease
Summary:        Version tolerant serialization/deserialization framework

License:        Apache-2.0
URL:            https://crates.io/crates/versionize
Source:         %{crates_source}

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
A version tolerant serialization/deserialization framework.}

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
%doc %{crate_instdir}/CONTRIBUTING.md
%doc %{crate_instdir}/README.md
%doc %{crate_instdir}/SECURITY-POLICY.md
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
