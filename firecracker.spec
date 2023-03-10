# This should be left enabled for generating buildreqs correctly.
%bcond_without check

# The RPM macro cargo_target can be defined to specify the Rust target to use
# during the build.  This defaults to musl for security benefits while testing
# in Copr--delete this to default to glibc for inclusion in Fedora.
%if ! %defined cargo_target
%global cargo_target %{_target_cpu}-unknown-linux-musl
%endif

# Assume that musl targets produce static binaries by default, which determines
# if the jailer program is usable.  It should still build successfully with any
# linkage setting, so this conditional allows forcing it to build or not.
%if %{lua:print(rpm.expand("%{cargo_target}"):match("musl") and "1" or "0")}
%bcond_without jailer
%else
%bcond_with jailer
%endif

Name:           firecracker
Version:        1.3.1
Release:        1%{?dist}

Summary:        Secure and fast microVMs for serverless computing
License:        Apache-2.0
URL:            https://firecracker-microvm.github.io/

Source0:        https://github.com/firecracker-microvm/firecracker/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tgz

# Bundle forked versions of existing crates to avoid conflicts with upstreams.
Source1:        https://github.com/firecracker-microvm/kvm-bindings/archive/e8359204b41d5c2e7c5af9ae5c26283b62337740.tar.gz#/kvm-bindings-0.6.0-1.crate
Source2:        https://github.com/firecracker-microvm/micro-http/archive/4b18a043e997da5b5f679e3defc279fec908753e.tar.gz#/micro_http-0.1.0.crate

Patch1:         %{name}-1.3.1-skip-criterion.patch
Patch2:         %{name}-1.3.1-kvm-ioctls.patch

BuildRequires:  rust-packaging
%if %defined cargo_target
BuildRequires:  rust-std-static-%{cargo_target}
%endif

ExclusiveArch:  aarch64 x86_64

%description
Firecracker is an open source virtualization technology that is purpose-built
for creating and managing secure, multi-tenant container and function-based
services that provide serverless operational models.  Firecracker runs
workloads in lightweight virtual machines, called microVMs, which combine the
security and isolation properties provided by hardware virtualization
technology with the speed and flexibility of containers.


%prep
%autosetup -p1

# Extract the bundled forked crates and point their users at the paths.
mkdir forks
tar --transform='s,^[^/]*,kvm-bindings,' -C forks -xzf %{SOURCE1}
tar --transform='s,^[^/]*,micro_http,' -C forks -xzf %{SOURCE2}
sed -i -e 's@^\(kvm-bindings\|micro_http\) = {.*\(, features =.*\| }$\)@\1 = { path = "../../forks/\1"\2@' Cargo.toml src/*/Cargo.toml
sed -i -e 's,../../forks,forks,' Cargo.toml

%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build -- %{!?with_jailer:--exclude=jailer} --workspace %{?cargo_target:--target=%{cargo_target}}

%install
install -pm 0755 -Dt %{buildroot}%{_bindir} target/%{?cargo_target}/release/{firecracker,%{?with_jailer:jailer,}rebase-snap,seccompiler-bin}

# Ship the built-in seccomp JSON as an example that can be edited and compiled.
ln -fn resources/seccomp/%{cargo_target}.json seccomp-filter.json ||
ln -fn resources/seccomp/unimplemented.json seccomp-filter.json

%if %{with check}
%check
# Ignore test failures over host resources like /dev/kvm, but log everything.
%cargo_test -- %{!?with_jailer:--exclude=jailer} --workspace %{?cargo_target:--target=%{cargo_target}} || :
%endif


%files
%{_bindir}/firecracker
%{?with_jailer:%{_bindir}/jailer}
%{_bindir}/rebase-snap
%{_bindir}/seccompiler-bin
%doc seccomp-filter.json
%doc src/api_server/swagger/firecracker.yaml
%doc docs CHANGELOG.md CHARTER.md CODE_OF_CONDUCT.md CONTRIBUTING.md CREDITS.md FAQ.md MAINTAINERS.md README.md SECURITY.md SPECIFICATION.md
%license LICENSE NOTICE THIRD-PARTY


%changelog
* Mon Mar 06 2023 David Michael <fedora.dm0@gmail.com> - 1.3.1-1
- Update to the 1.3.1 release.

* Thu Mar 02 2023 David Michael <fedora.dm0@gmail.com> - 1.3.0-1
- Initial package.
