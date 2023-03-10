# Generated by rust2rpm 24
%bcond_without check
%global debug_package %{nil}

%global crate linux-loader

Name:           rust-linux-loader
Version:        0.8.1
Release:        %autorelease
Summary:        Linux kernel image loading crate

License:        Apache-2.0 AND BSD-3-Clause
URL:            https://crates.io/crates/linux-loader
Source:         %{crates_source}

Patch1:         %{name}-0.8.1-skip-criterion.patch

BuildRequires:  rust-packaging >= 21

%global _description %{expand:
A Linux kernel image loading crate.}

%description %{_description}

%package        devel
Summary:        %{summary}
BuildArch:      noarch

%description    devel %{_description}

This package contains library source intended for building other packages which
use the "%{crate}" crate.

%files          devel
%license %{crate_instdir}/LICENSE-APACHE
%license %{crate_instdir}/LICENSE-BSD-3-Clause
%doc %{crate_instdir}/CHANGELOG.md
%doc %{crate_instdir}/DESIGN.md
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

%package     -n %{name}+bzimage-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+bzimage-devel %{_description}

This package contains library source intended for building other packages which
use the "bzimage" feature of the "%{crate}" crate.

%files       -n %{name}+bzimage-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+elf-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+elf-devel %{_description}

This package contains library source intended for building other packages which
use the "elf" feature of the "%{crate}" crate.

%files       -n %{name}+elf-devel
%ghost %{crate_instdir}/Cargo.toml

%package     -n %{name}+pe-devel
Summary:        %{summary}
BuildArch:      noarch

%description -n %{name}+pe-devel %{_description}

This package contains library source intended for building other packages which
use the "pe" feature of the "%{crate}" crate.

%files       -n %{name}+pe-devel
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
