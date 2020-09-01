%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)
%global enable_tests 1
Name:                nodejs-tap
Version:             0.7.1
Release:             1
Summary:             A Test Anything Protocol library
License:             MIT
URL:                 https://github.com/isaacs/node-tap
Source0:             https://github.com/tapjs/node-tap/archive/v0.7.1.tar.gz
BuildArch:           noarch
ExclusiveArch:       %{nodejs_arches} noarch
BuildRequires:       nodejs-packaging
%if 0%{?enable_tests}
BuildRequires:       gcc npm(buffer-equal) npm(deep-equal) npm(difflet) npm(glob)
BuildRequires:       npm(inherits) = 1.0.0 npm(mkdirp) npm(nopt) npm(runforcover) npm(slide)
BuildRequires:       npm(yamlish)
%endif
%description
This is a mix-and-match set of utilities that you can use to write test
harnesses and frameworks that communicate with one another using the
Test Anything Protocol.

%prep
%setup -q -n node-tap-%{version}
%nodejs_fixdep deep-equal '^1.0.1'
%nodejs_fixdep glob '^6.0.3'
%nodejs_fixdep inherits 1
%nodejs_fixdep nopt '^3.0.6'
rm -rf node_modules

%build

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/tap
cp -pr bin lib package.json %{buildroot}%{nodejs_sitelib}/tap
mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/tap/bin/tap.js %{buildroot}%{_bindir}/tap
chmod 0755 %{buildroot}%{nodejs_sitelib}/tap/bin/*
%nodejs_symlink_deps

%check
%nodejs_symlink_deps --check
%if 0%{?enable_tests}
%{__nodejs} -e 'require("./")'
rm -f test/debug-test.js
%__nodejs %{buildroot}%{nodejs_sitelib}/tap/bin/tap.js test/*.js
%endif

%files
%{nodejs_sitelib}/tap
%{_bindir}/tap
%doc coverage-example example README.md AUTHORS LICENSE

%changelog
* Fri Aug 21 2020 wangyue <wangyue92@huawei.com> - 0.7.1-1
- package init
