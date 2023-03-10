# Generated by rust2rpm 24
%bcond_with check
%global debug_package %{nil}

%global crate event-manager

Name:           rust-event-manager
Version:        0.3.0
Release:        %autorelease
Summary:        Abstractions for implementing event based systems

License:        Apache-2.0 OR BSD-3-Clause
URL:            https://crates.io/crates/event-manager
Source:         %{crates_source}

Patch1:         %{name}-0.3.0-skip-criterion.patch

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
Abstractions for implementing event based systems.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-APACHE
%license %{crate_instdir}/LICENSE-BSD-3-CLAUSE
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

%package     -n %{name}+remote_endpoint-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+remote_endpoint-devel %{_description}

This package contains library source intended for building other packages which
use the "remote_endpoint" feature of the "%{crate}" crate.

%files       -n %{name}+remote_endpoint-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+test_utilities-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+test_utilities-devel %{_description}

This package contains library source intended for building other packages which
use the "test_utilities" feature of the "%{crate}" crate.

%files       -n %{name}+test_utilities-devel
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
