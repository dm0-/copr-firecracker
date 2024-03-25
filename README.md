A couple of Firecracker's security features require it to be statically linked with musl like upstream builds.
Fedora doesn't allow static linking or compiling for Rust's musl target, so the full set of security benefits can't be included in Fedora packages.
This spec file is written to support the `cargo_target` macro for cross-compilation, however, which allows building all security features by specifying the musl target on systems where it is available.
