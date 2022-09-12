Summary:        File Access Policy Analyzer
Name:           fapolicy-analyzer
Version:        0.6.1
Release:        1%{?dist}
License:        GPLv3+
URL:            https://github.com/ctc-oss/fapolicy-analyzer
Source0:        fapolicy-analyzer.tar.gz
Source1:        crates.tar.gz

BuildRequires: python3-devel
BuildRequires: python3dist(setuptools)
BuildRequires: python3dist(pip)
BuildRequires: python3dist(wheel)
BuildRequires: python3dist(babel)

%if 0%{?rhel}
BuildRequires: rust-toolset
%else
BuildRequires: rust-packaging
BuildRequires: python3dist(setuptools-rust)

# crates
BuildRequires: rust-arrayvec0.5-devel
BuildRequires: rust-atty-devel
BuildRequires: rust-autocfg-devel
BuildRequires: rust-bitflags-devel
BuildRequires: rust-bitvec-devel
BuildRequires: rust-bumpalo-devel
BuildRequires: rust-byteorder-devel
BuildRequires: rust-cc-devel
BuildRequires: rust-cfg-if-devel
BuildRequires: rust-chrono-devel
BuildRequires: rust-clap-devel
BuildRequires: rust-clap_derive-devel
BuildRequires: rust-confy-devel
BuildRequires: rust-crossbeam-channel-devel
BuildRequires: rust-crossbeam-deque-devel
BuildRequires: rust-crossbeam-epoch-devel
BuildRequires: rust-crossbeam-utils-devel
BuildRequires: rust-data-encoding-devel
BuildRequires: rust-dbus-devel
BuildRequires: rust-dirs-sys-devel
BuildRequires: rust-either-devel
BuildRequires: rust-fastrand-devel
BuildRequires: rust-funty-devel
BuildRequires: rust-getrandom-devel
BuildRequires: rust-hashbrown-devel
BuildRequires: rust-heck-devel
BuildRequires: rust-iana-time-zone-devel
BuildRequires: rust-indexmap-devel
BuildRequires: rust-instant-devel
BuildRequires: rust-lazy_static-devel
BuildRequires: rust-lexical-core-devel
BuildRequires: rust-libc-devel
BuildRequires: rust-libdbus-sys-devel
BuildRequires: rust-lock_api-devel
BuildRequires: rust-log-devel
BuildRequires: rust-memchr-devel
BuildRequires: rust-memoffset-devel
BuildRequires: rust-num-integer-devel
BuildRequires: rust-num-traits-devel
BuildRequires: rust-num_cpus-devel
BuildRequires: rust-once_cell-devel
BuildRequires: rust-parking_lot-devel
BuildRequires: rust-parking_lot_core-devel
BuildRequires: rust-pkg-config-devel
BuildRequires: rust-proc-macro-error-devel
BuildRequires: rust-proc-macro-error-attr-devel
BuildRequires: rust-proc-macro-hack-devel
BuildRequires: rust-proc-macro2-devel
BuildRequires: rust-pyo3-devel
BuildRequires: rust-pyo3-build-config-devel
BuildRequires: rust-pyo3-macros-devel
BuildRequires: rust-pyo3-macros-backend-devel
BuildRequires: rust-quote-devel
BuildRequires: rust-radium-devel
BuildRequires: rust-rayon-devel
BuildRequires: rust-rayon-core-devel
BuildRequires: rust-remove_dir_all-devel
BuildRequires: rust-ring-devel
BuildRequires: rust-ryu-devel
BuildRequires: rust-scopeguard-devel
BuildRequires: rust-serde-devel
BuildRequires: rust-serde_derive-devel
BuildRequires: rust-similar-devel
BuildRequires: rust-smallvec-devel
BuildRequires: rust-spin-devel
BuildRequires: rust-static_assertions-devel
BuildRequires: rust-strsim-devel
BuildRequires: rust-syn-devel
BuildRequires: rust-tap-devel
BuildRequires: rust-tempfile-devel
BuildRequires: rust-termcolor-devel
BuildRequires: rust-textwrap-devel
BuildRequires: rust-thiserror-devel
BuildRequires: rust-thiserror-impl-devel
BuildRequires: rust-time0.1-devel
BuildRequires: rust-toml-devel
BuildRequires: rust-unicode-segmentation-devel
BuildRequires: rust-unicode-width-devel
BuildRequires: rust-unicode-xid-devel
BuildRequires: rust-unindent-devel
BuildRequires: rust-untrusted-devel
BuildRequires: rust-vec_map-devel
BuildRequires: rust-version_check-devel
BuildRequires: rust-wyz-devel
BuildRequires: rust-yansi-devel
BuildRequires: rust-paste-devel
BuildRequires: rust-indoc-devel
%endif

Requires: python3
Requires: python3-gobject
Requires: python3-events
Requires: python3-configargparse
Requires: python3-more-itertools
Requires: python3-rx
Requires: python3-importlib-metadata
Requires: gtk3
Requires: dbus-libs
Requires: gtksourceview3

%if 0%{?rhel}
Requires: python3-dataclasses
Requires: python3-importlib-resources
%endif

%global modname fapolicy_analyzer

%description
Tools to assist with the configuration and maintenance of Fapolicyd (File Access Policy Daemon).

%prep
# Problem:  the /usr/share/cargo/registry location is not writable, blocking use of vendored crates
# Solution: link the contents of the /usr/share/cargo/registry into a replacement writable registry
#           extract the contents of the vendored crate tarball to the replacement writable registry
CARGO_REG_DIR=%{_sourcedir}/registry
mkdir -p ${CARGO_REG_DIR}
for d in %{cargo_registry}/*; do ln -sf ${d} ${CARGO_REG_DIR}; done
tar xzf %{_sourcedir}/crates.tar.gz -C ${CARGO_REG_DIR}

%cargo_prep

# remap the registry location in the .cargo/config to the replacement registry
sed -i "s#%{cargo_registry}#${CARGO_REG_DIR}#g" .cargo/config
# unmap any path strings in the so back to the /usr/share/ registry, otherwise rpm check will bark
sed -i "/\[build\]/a rustflags = [\"--remap-path-prefix\", \"${CARGO_REG_DIR}=%{cargo_registry}\"]" .cargo/config

%autosetup -p0 -n %{name}
rm Cargo.lock

%build
echo %{version} > VERSION
%{python3} setup.py compile_catalog -f
%py3_build_wheel

%install
%{py3_install_wheel %{modname}-%{version}*%{_arch}.whl}
install bin/%{name} %{buildroot}%{_sbindir}/%{name} -D

%check

%files -n %{name}
%doc README.md
%license LICENSE
%{python3_sitearch}/%{modname}
%{python3_sitearch}/%{modname}-%{version}*
%attr(755,root,root) %{_sbindir}/fapolicy-analyzer

%changelog
* Fri Sep 09 2022 John Wass <jwass3@gmail.com> 0.6.0-1
- New release
