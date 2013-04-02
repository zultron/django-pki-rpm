%global _gitrel    20130402git562fa1e
%global _dotgitrel %{?_gitrel:.%{_gitrel}}

Name:           django-pki
Version:        0.20.0
Release:        0.1%{?_dotgitrel}%{?dist}
Summary:        A PKI based on Django
Group:          Development/Languages

License:        GPLv2+
URL:            https://github.com/dkerwin/django-pki
# My fork (of a fork of a fork):  https://github.com/zultron/django-pki
Source0:        %{name}-%{version}%{?_dotgitrel}.tar.gz
# Document where static files are located
Patch0:         %{name}-rpm-static-files.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
# for tests
BuildRequires:  Django14
BuildRequires:  python-unittest2
BuildRequires:  python-windmill
BuildRequires:  Django-south

Requires:       python-iterpipes
Requires:       pygraphviz
Requires:       Django14
Requires:       Django-south


%description

This project aims to simplify the installation and management of your
personal CA infrastructure. Features include:

- Create CA chains based on self-signed Root CAs
- CAs can contain other CAs or non-CA certificates
- Automatic CRL generation/update when CA or related certificate is modified
- Creation and export of PEM, PKCS12 and DER encoded versions
- Revoke and renew of certificates

%prep
%setup -q
%patch0 -p1 -z .rpm-static-files


%build
%{__python} setup.py build

# build the docs
pushd docs
# add correct python sitelib
sed -i 's,@PYTHON_SITELIB@,%{python_sitelib},' \
    installation/configuration.rst
SPHINXBUILD=sphinx-build
if test "%{?rhel}" = 6; then
   SPHINXBUILD=sphinx-1.0-build
fi
make SPHINXBUILD=$SPHINXBUILD html
popd


%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

# Fix files that should have been installed as symlinks
for i in delete_detail pki_admin; do
    ln -sf $i.js %{buildroot}%{python_sitelib}/pki/media/pki/js/$i.min.js
done

 
%files
%doc AUTHORS CHANGELOG COPYING LICENSE README.markdown docs/_build/html
%{python_sitelib}/*


%changelog
* Tue Apr  2 2013 John Morris <john@zultron.com> - 0.20.0-0.1.20130402git2d1c037
- initial package

