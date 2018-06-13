%global  _hardened_build     1
%global  nginx_user          nginx

%bcond_without java
%bcond_without lua
%bcond_without passenger
%bcond_without sregex
# This module does not currently work
%bcond_with x_rid_header
# This also doesn't work
%bcond_with upstream_check

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
%bcond_without systemd
%else
%bcond_with systemd
%endif

%define ngx_sorted_query_string_version  0.3
%define ngx_lua_version             0.10.8
%define ngx_openssl_version         1.0.2j
%define ngx_lua_upstream_sha        e91cf554ef0cd3d5c8e58b11888ddfe652a7497d
%define ngx_lua_upstream_cache_sha  cea46bd2a940c543905583068aa1fb87845ac463
%define ngx_cache_purge_sha         8242f745f408aa4106ba2d0e3ae7867d7de6335f
%define ngx_rtmp_sha                5150993accb5edefa61d71e1c81ad8c02f515428
%define ngx_srcache_sha             af82f755b8a92765fff0b3e70b26bedf4bbacadc
%define ngx_redis2_sha              8cc7304787ae9542db4feb50d9e27beb485caa0f
%define ngx_redis_version           0.3.8
%define ngx_echo_version            0.60
%define ngx_upload_sha              57bbb0db23f113f2a8fa2d09d9193927b891fa75
%define ngx_upload_progress_version 0.9.2
%define ngx_headers_more_version    0.32
%define ngx_devel_kit_sha           e443262071e759c047492be60ec7e2d73c5b57ec
%define ngx_array_var_sha           844ccce047c104b1c47d464292cf01c926e8a6c4
%define ngx_dyups_sha               6fa254dc551d7774a84cc02301ebaf0e59209430
%define ngx_upstream_check_sha      d6341aeeb86911d4798fbceab35015c63178e66f
%define ngx_njs_sha                 f7c74f0dea69846c06f0f6b1ce4294d3a6682663
%define ngx_x_rid_sha               f3f61183d035796b4b78ad710b3a086e3d98dd82
%define ngx_sticky_sha              08a395c66e42
%define ngx_rdns_sha                a32deecaf1fa4be4bd445c2b770283d20bf61da6
%define ngx_pagespeed_version       1.11.33.4
%define ngx_vts_version             0.1.11
%define ngx_replace_filter_sha      2c7f0656c816e347ba43a7909120d434a168044c
%define ngx_clojure_sha             3bd36535686d9df9c774676a7e4405cec34da9a0
%define ngx_clojure_jar_version     0.4.5
%define ngx_clojure_tomcat_version  0.2.3
%define ngx_clojure_jersey_version  0.1.4

%define luajit_inc /usr/include/luajit-2.1
%define luajit_lib /usr/lib64

# gperftools exist only on selected arches
%ifnarch s390 s390x
%global with_gperftools 1
%endif

%global with_aio 1

%if 0%{?fedora} > 22
%global with_mailcap_mimetypes 1
%endif

Name:              nginx
Epoch:             2
Version:           1.12.2
Release:           2%{?dist}

Summary:           A high performance web server and reverse proxy server
Group:             System Environment/Daemons
# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:           BSD
URL:               http://nginx.org/

Source0:           http://nginx.org/download/nginx-%{version}.tar.gz
Source1:           http://nginx.org/download/nginx-%{version}.tar.gz.asc
Source10:          nginx.service
Source11:          nginx.logrotate
Source12:          nginx.conf
Source13:          nginx-upgrade
Source14:          nginx-upgrade.8
Source15:          nginx.init
Source100:         index.html
Source101:         poweredby.png
Source102:         nginx-logo.png
Source103:         404.html
Source104:         50x.html
Source150:         passenger.conf
Source200:         README.dynamic

Source300: https://github.com/openresty/lua-nginx-module/archive/v%{ngx_lua_version}.tar.gz#/lua-nginx-module-%{ngx_lua_version}.tar.gz
Source301: https://github.com/openresty/headers-more-nginx-module/archive/v%{ngx_headers_more_version}.tar.gz#/headers-more-nginx-module-v%{ngx_headers_more_version}.tar.gz
Source302: https://github.com/cloudflare/lua-nginx-cache-module/archive/%{ngx_lua_upstream_cache_sha}.tar.gz#/lua-upstream-cache-nginx-module-%{ngx_lua_upstream_cache_sha}.tar.gz
Source303: https://github.com/simpl/ngx_devel_kit/archive/%{ngx_devel_kit_sha}.tar.gz#/ngx_devel_kit-%{ngx_devel_kit_sha}.tar.gz
Source304: https://github.com/wandenberg/nginx-sorted-querystring-module/archive/%{ngx_sorted_query_string_version}.tar.gz#/nginx-sorted-querystring-module-%{ngx_sorted_query_string_version}.tar.gz
Source305: https://github.com/arut/nginx-rtmp-module/archive/%{ngx_rtmp_sha}.tar.gz#/nginx-rtmp-module-%{ngx_rtmp_sha}.tar.gz
Source306: https://github.com/nginx-modules/ngx_cache_purge/archive/%{ngx_cache_purge_sha}.tar.gz#/ngx_cache_purge-%{ngx_cache_purge_sha}.tar.gz
Source307: https://github.com/nginx-clojure/nginx-clojure/archive/%{ngx_clojure_sha}.tar.gz#/nginx-clojure-%{ngx_clojure_sha}.tar.gz
Source308: https://github.com/openresty/array-var-nginx-module/archive/%{ngx_array_var_sha}.tar.gz#/array-var-nginx-module-%{ngx_array_var_sha}.tar.gz
Source309: https://github.com/openresty/srcache-nginx-module/archive/%{ngx_srcache_sha}.tar.gz#/srcache-nginx-module-%{ngx_srcache_sha}.tar.gz
Source310: https://github.com/openresty/redis2-nginx-module/archive/%{ngx_redis2_sha}.tar.gz#/redis2-nginx-module-%{ngx_redis2_sha}.tar.gz
Source311: https://github.com/yzprofile/ngx_http_dyups_module/archive/%{ngx_dyups_sha}.tar.gz#/ngx_http_dyups_module-%{ngx_dyups_sha}.tar.gz
Source312: https://github.com/openresty/lua-upstream-nginx-module/archive/%{ngx_lua_upstream_sha}.tar.gz#/lua-upstream-nginx-module-%{ngx_lua_upstream_sha}.tar.gz
Source313: https://github.com/openresty/echo-nginx-module/archive/v%{ngx_echo_version}.tar.gz#/echo-nginx-module-v%{ngx_echo_version}.tar.gz
Source314: https://github.com/yaoweibin/nginx_upstream_check_module/archive/%{ngx_upstream_check_sha}.tar.gz#/nginx_upstream_check_module-%{ngx_upstream_check_sha}.tar.gz
Source315: https://github.com/nginx/njs/archive/%{ngx_njs_sha}.tar.gz#/njs-%{ngx_njs_sha}.tar.gz
Source316: https://github.com/fdintino/nginx-upload-module/archive/%{ngx_upload_sha}.tar.gz#/nginx-upload-module-%{ngx_upload_sha}.tar.gz
Source317: https://github.com/masterzen/nginx-upload-progress-module/archive/v%{ngx_upload_progress_version}.tar.gz#/nginx-upload-progress-module-v%{ngx_upload_progress_version}.tar.gz
Source318: https://github.com/kriegsmanj/nginx-x-rid-header/archive/%{ngx_x_rid_sha}.tar.gz#/nginx-x-rid-header-%{ngx_x_rid_sha}.tar.gz
Source319: https://bitbucket.org/nginx-goodies/nginx-sticky-module-ng/get/%{ngx_sticky_sha}.tar.gz#/nginx-goodies-nginx-sticky-module-ng-%{ngx_sticky_sha}.tar.gz
Source320: https://github.com/flant/nginx-http-rdns/archive/%{ngx_rdns_sha}.tar.gz#/nginx-http-rdns-%{ngx_rdns_sha}.tar.gz
Source321: https://github.com/pagespeed/ngx_pagespeed/archive/v%{ngx_pagespeed_version}-beta.tar.gz#/ngx_pagespeed-%{ngx_pagespeed_version}-beta.tar.gz
Source322: https://dl.google.com/dl/page-speed/psol/%{ngx_pagespeed_version}.tar.gz#/psol-%{ngx_pagespeed_version}.tar.gz
Source323: https://github.com/vozlt/nginx-module-vts/archive/v%{ngx_vts_version}.tar.gz#/nginx-module-vts-%{ngx_vts_version}.tar.gz
Source324: https://github.com/openresty/replace-filter-nginx-module/archive/%{ngx_replace_filter_sha}.tar.gz#/replace-filter-nginx-module-%{ngx_replace_filter_sha}.tar.gz
Source330: http://people.freebsd.org/~osa/ngx_http_redis-%{ngx_redis_version}.tar.gz

Source400: https://openssl.org/source/openssl-%{ngx_openssl_version}.tar.gz
%if %{with java}
Source401: https://clojars.org/repo/nginx-clojure/nginx-tomcat8/%{ngx_clojure_tomcat_version}/nginx-tomcat8-%{ngx_clojure_tomcat_version}.jar
Source402: https://clojars.org/repo/nginx-clojure/nginx-jersey/%{ngx_clojure_jersey_version}/nginx-jersey-%{ngx_clojure_jersey_version}.jar
Source403: https://clojars.org/repo/nginx-clojure/nginx-clojure/%{ngx_clojure_jar_version}/nginx-clojure-%{ngx_clojure_jar_version}.jar
%endif

# removes -Werror in upstream build scripts.  -Werror conflicts with
# -D_FORTIFY_SOURCE=2 causing warnings to turn into errors.
Patch0:            nginx-auto-cc-gcc.patch

Patch101: nginx-upstream-check-changes.patch
Patch102: lua-upstream-cache-nginx-module.dynamic-module.patch
Patch103: nginx-sticky.dynamic-module.patch
Patch117: ngx_http_dyups.dynamic-module.patch
Patch118: ngx_http_dyups.segfault-fix.patch
Patch119: lua-nginx-module.fixes.patch
Patch120: echo-nginx-module.fixes.patch

# https://raw.githubusercontent.com/openresty/openresty/dbccee1418ddb24a2adabd80b0737595b7fd577e/patches/nginx-1.11.2-ssl_cert_cb_yield.patch
Patch201: nginx-1.11.2-ssl_cert_cb_yield.patch
# https://raw.githubusercontent.com/openresty/openresty/dbccee1418ddb24a2adabd80b0737595b7fd577e/patches/nginx-1.11.2-ssl_pending_session.patch
Patch202: nginx-1.11.2-ssl_pending_session.patch

%if 0%{?with_gperftools}
BuildRequires:     gperftools-devel
%endif
BuildRequires:     pcre-devel
BuildRequires:     zlib-devel

Requires:          nginx-filesystem = %{epoch}:%{version}-%{release}

# %if 0%{?rhel} || 0%{?fedora} < 24
# # Introduced at 1:1.10.0-1 to ease upgrade path. To be removed later.
# Requires:          nginx-all-modules = %{epoch}:%{version}-%{release}
# %endif

Requires:          pcre
Requires(pre):     nginx-filesystem
%if 0%{?with_mailcap_mimetypes}
Requires:          nginx-mimetypes
%endif
Provides:          webserver

%if %{with systemd}
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd
%else
Requires(post):    chkconfig
Requires(preun):   chkconfig
Requires(preun):   initscripts
Requires(postun):  initscripts
%endif


%description
Nginx is a web server and a reverse proxy server for HTTP, SMTP, POP3 and
IMAP protocols, with a strong focus on high concurrency, performance and low
memory usage.
%if %{with upstream_check}

Comes bundled with ngx_http_dyups_module and ngx_http_upstream_check_module
%endif

%package all-modules
Group:             System Environment/Daemons
Summary:           A meta package that installs all available Nginx modules
BuildArch:         noarch

Requires:          nginx-mod-http-geoip = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-http-image-filter = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-http-perl = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-http-xslt-filter = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-mail = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-stream = %{epoch}:%{version}-%{release}

%description all-modules
%{summary}.

%package filesystem
Group:             System Environment/Daemons
Summary:           The basic directory layout for the Nginx server
BuildArch:         noarch
Requires(pre):     shadow-utils

%description filesystem
The nginx-filesystem package contains the basic directory layout
for the Nginx server including the correct permissions for the
directories.

%package mod-http-geoip
Group:             System Environment/Daemons
Summary:           Nginx HTTP geoip module
BuildRequires:     GeoIP-devel
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          GeoIP

%description mod-http-geoip
%{summary}.

%package mod-http-image-filter
Group:             System Environment/Daemons
Summary:           Nginx HTTP image filter module
BuildRequires:     gd-devel
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          gd

%description mod-http-image-filter
%{summary}.

%package mod-http-perl
Group:             System Environment/Daemons
Summary:           Nginx HTTP perl module
BuildRequires:     perl-devel
%if 0%{?fedora} >= 24
BuildRequires:     perl-generators
%endif
BuildRequires:     perl(ExtUtils::Embed)
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description mod-http-perl
%{summary}.

%package mod-http-xslt-filter
Group:             System Environment/Daemons
Summary:           Nginx XSLT module
BuildRequires:     libxslt-devel
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-xslt-filter
%{summary}.

%package mod-mail
Group:             System Environment/Daemons
Summary:           Nginx mail modules
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-mail
%{summary}.

%package mod-stream
Group:             System Environment/Daemons
Summary:           Nginx stream modules
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-stream
%{summary}.

%if %{with lua}
%package mod-http-lua
Summary:           Nginx HTTP Lua module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-devel-kit = %{epoch}:%{version}-%{release}
BuildRequires:     luajit-devel

%description mod-http-lua
Embed the Power of Lua into Nginx HTTP servers.

%package mod-http-lua-cache
Summary:           Nginx HTTP Lua upstream cache module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-lua-cache
Nginx module for ngx_lua to provide Lua API to inspect upstream HTTP cache
meta-data.

%package mod-http-lua-upstream
Summary:           Nginx HTTP Lua upstream module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-lua-upstream
Nginx C module to expose Lua API to ngx_lua for Nginx upstreams.
%endif

%package mod-devel-kit
Summary:           Nginx Development Kit module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-devel-kit
An Nginx module that adds additional generic tools that module developers can
use in their own modules.

%package mod-http-array-var
Summary:           Nginx Array Var module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          nginx-mod-devel-kit = %{epoch}:%{version}-%{release}

%description mod-http-array-var
Add support for array variables to Nginx config files.

%package mod-http-headers-more-filter
Summary:           Nginx HTTP Headers More module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-headers-more-filter
Set, add, and clear arbitrary output headers in Nginx http servers.

%package mod-http-sorted-querystring
Summary:           Nginx HTTP sorted querystring module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-sorted-querystring
%{summary}.

%package mod-rtmp
Summary:           Nginx RTMP media streaming module
Group:             System Environment/Daemons
URL:               http://nginx-rtmp.blogspot.com
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-rtmp
%{summary}.

%package mod-http-cache-purge
Summary:           Nginx HTTP cache purge module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-cache-purge
Nginx module which adds ability to purge content from FastCGI, proxy, SCGI,
and uWSGI caches.

%package mod-http-redis
Summary:           Nginx HTTP Redis module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-redis
Nginx module for simple redis caching.

%package mod-http-redis2
Summary:           Nginx HTTP Redis 2.0 module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-redis2
Nginx upstream module for the Redis 2.0 protocol.

%package mod-http-srcache-filter
Group:             System Environment/Daemons
Summary:           Nginx HTTP srcache-filter module
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-srcache-filter
Transparent subrequest-based caching layout for arbitrary nginx locations.

%package mod-http-echo
Summary:           Nginx HTTP echo module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-echo
An Nginx module for bringing the power of "echo", "sleep", "time" and more to
Nginx configs.

%package mod-http-upload
Summary:           Nginx HTTP upload module
Group:             System Environment/Daemons
URL:               http://www.grid.net.ru/nginx/upload.en.html
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-upload
A module for nginx web server for handling file uploads using
multipart/form-data encoding (RFC 1867).

%package mod-http-uploadprogress
Summary:           Nginx HTTP upload progress module
Group:             System Environment/Daemons
URL:               http://wiki.codemongers.com/NginxHttpUploadProgressModule
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-uploadprogress
Nginx module implementing an upload progress system, that monitors RFC1867
POST uploads as they are transmitted to upstream servers.

%if %{with java}
%package mod-http-clojure
Summary:           Nginx HTTP Clojure module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          java-1.8.0-openjdk
Requires:          clojure >= 1.5.1
BuildRequires:     java-1.8.0-openjdk-devel
BuildRequires:     clojure >= 1.5.1

%description mod-http-clojure
Nginx module for embedding Clojure, Java, and Groovy programs.
%endif

%package mod-http-vts
Summary:           Nginx virtual host traffic status module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-vts
%{summary}.

%package mod-pagespeed
Summary:           Nginx PageSpeed module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
%if 0%{rhel} <= 6
BuildRequires: devtoolset-2-gcc-c++ devtoolset-2-binutils
%endif

%description mod-pagespeed
Automatic PageSpeed optimization module for Nginx.

%package mod-http-rdns
Summary:           Nginx HTTP rDNS module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-rdns
%{summary}.

%if !%{with upstream_check}
%package mod-http-dyups
Summary:           Nginx HTTP Dynamic Upstreams module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
# %if %{with lua}
# Requires:          nginx-mod-http-lua
# %endif

%description mod-http-dyups
%{summary}.
%endif

%if %{with sregex}
%package mod-http-replace-filter
Summary:           Nginx HTTP replace filter module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          sregex
BuildRequires:     sregex-devel

%description mod-http-replace-filter
Nginx module providing streaming regular expression replacement in response
bodies.
%endif  # with sregex

%package mod-selective-cache-purge
Summary:           Nginx selective cache purge module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-selective-cache-purge
Nginx module to purge cache by glob patterns.

%package mod-http-sticky
Summary:           Nginx sticky module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-http-sticky
Nginx module to add a sticky cookie to be always forwarded to the same
upstream server.

%if %{with x_rid_header}
%package mod-x-rid-header
Summary:           Nginx X-RID header module
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-x-rid-header
Nginx module that adds a request id header that can be used to correlate
frontend and backend requests.
%endif

%package mod-njs
Summary:           Nginx HTTP and Stream JavaScript modules
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}

%description mod-njs
%{summary}.

%if %{with passenger}
%package mod-passenger
Summary:           Nginx Phusion Passenger support
Group:             System Environment/Daemons
Requires:          nginx = %{epoch}:%{version}-%{release}
Requires:          passenger
BuildRequires:     passenger-devel
BuildRequires:     ruby-devel

%description mod-passenger
%{summary}.

%endif

%prep
%setup -q
%setup -q -D -T -a 300
%setup -q -D -T -a 301
%setup -q -D -T -a 302
%setup -q -D -T -a 303
%setup -q -D -T -a 304
%setup -q -D -T -a 305
%setup -q -D -T -a 306
%setup -q -D -T -a 307
%setup -q -D -T -a 308
%setup -q -D -T -a 309
%setup -q -D -T -a 310
%setup -q -D -T -a 311
%setup -q -D -T -a 312
%setup -q -D -T -a 313
%setup -q -D -T -a 314
%setup -q -D -T -a 315
%setup -q -D -T -a 316
%setup -q -D -T -a 317
%setup -q -D -T -a 318
%setup -q -D -T -a 319
%setup -q -D -T -a 320
%setup -q -D -T -a 321
%setup -q -D -T -a 322
%setup -q -D -T -a 323
%setup -q -D -T -a 324
%setup -q -D -T -a 330
%setup -q -D -T -a 400
%patch0 -p0
%patch101 -d ./nginx_upstream_check_module-%{ngx_upstream_check_sha} -p1
%patch102 -d ./lua-upstream-cache-nginx-module-%{ngx_lua_upstream_cache_sha} -p1
%patch103 -d ./nginx-goodies-nginx-sticky-module-ng-%{ngx_sticky_sha} -p1
%patch117 -d ./ngx_http_dyups_module-%{ngx_dyups_sha} -p1
%patch118 -d ./ngx_http_dyups_module-%{ngx_dyups_sha} -p1
%patch119 -d ./lua-nginx-module-%{ngx_lua_version} -p1
%patch120 -d ./echo-nginx-module-%{ngx_echo_version} -p1
%patch201 -p1
%patch202 -p1
%if %{with upstream_check}
patch -p0 < ./nginx_upstream_check_module-%{ngx_upstream_check_sha}/check_1.11.5+.patch
%endif
mv psol ngx_pagespeed-%{ngx_pagespeed_version}-beta
cp %{SOURCE200} .

%if 0%{?rhel} < 8
sed -i -e 's#KillMode=.*#KillMode=process#g' %{SOURCE10}
sed -i -e 's#PROFILE=SYSTEM#HIGH:!aNULL:!MD5#' %{SOURCE12}
%endif


%build
pushd njs-%{ngx_njs_sha}
./configure
make %{?_smp_mflags}
popd

# nginx does not utilize a standard configure script.  It has its own
# and the standard configure options cause the nginx configure script
# to error out.  This is is also the reason for the DESTDIR environment
# variable.
export DESTDIR=%{buildroot}

LUAJIT_INC=%{luajit_inc} LUAJIT_LIB=%{luajit_lib} \
SREGEX_INC=%{_includedir} \
SREGEX_LIB=%{_libdir} \
./configure \
    --prefix=%{_datadir}/nginx \
    --sbin-path=%{_sbindir}/nginx \
    --modules-path=%{_libdir}/nginx/modules \
    --conf-path=%{_sysconfdir}/nginx/nginx.conf \
    --error-log-path=%{_localstatedir}/log/nginx/error.log \
    --http-log-path=%{_localstatedir}/log/nginx/access.log \
    --http-client-body-temp-path=%{_localstatedir}/lib/nginx/tmp/client_body \
    --http-proxy-temp-path=%{_localstatedir}/lib/nginx/tmp/proxy \
    --http-fastcgi-temp-path=%{_localstatedir}/lib/nginx/tmp/fastcgi \
    --http-uwsgi-temp-path=%{_localstatedir}/lib/nginx/tmp/uwsgi \
    --http-scgi-temp-path=%{_localstatedir}/lib/nginx/tmp/scgi \
    --pid-path=/run/nginx.pid \
    --lock-path=/run/lock/subsys/nginx \
    --user=%{nginx_user} \
    --group=%{nginx_user} \
%if 0%{?with_aio}
    --with-file-aio \
%endif
    --with-http_ssl_module \
    --with-openssl=./openssl-%{ngx_openssl_version} \
    --with-http_v2_module \
    --with-http_realip_module \
    --with-http_addition_module \
    --with-http_xslt_module=dynamic \
    --with-http_image_filter_module=dynamic \
    --with-http_geoip_module=dynamic \
    --with-http_sub_module \
    --with-http_dav_module \
    --with-http_flv_module \
    --with-http_mp4_module \
    --with-http_gunzip_module \
    --with-http_gzip_static_module \
    --with-http_random_index_module \
    --with-http_secure_link_module \
    --with-http_degradation_module \
    --with-http_slice_module \
    --with-http_stub_status_module \
    --with-http_perl_module=dynamic \
    --with-mail=dynamic \
    --with-mail_ssl_module \
    --with-pcre \
    --with-pcre-jit \
    --with-stream=dynamic \
    --with-stream_ssl_module \
%if 0%{?with_gperftools}
    --with-google_perftools_module \
%endif
%if %{with passenger}
    --add-dynamic-module=$(passenger-config --nginx-addon-dir) \
%endif
%if %{with lua}
    --add-dynamic-module=./lua-upstream-nginx-module-%{ngx_lua_upstream_sha} \
    --add-dynamic-module=./lua-nginx-module-%{ngx_lua_version} \
    --add-dynamic-module=./lua-upstream-cache-nginx-module-%{ngx_lua_upstream_cache_sha} \
%endif
%if %{with java}
    --add-dynamic-module=./nginx-clojure-%{ngx_clojure_sha}/src/c \
%endif
    --add-dynamic-module=./headers-more-nginx-module-%{ngx_headers_more_version} \
    --add-dynamic-module=./ngx_devel_kit-%{ngx_devel_kit_sha} \
    --add-dynamic-module=./nginx-sorted-querystring-module-%{ngx_sorted_query_string_version} \
    --add-dynamic-module=./nginx-rtmp-module-%{ngx_rtmp_sha} \
    --add-dynamic-module=./ngx_cache_purge-%{ngx_cache_purge_sha} \
    --add-dynamic-module=./array-var-nginx-module-%{ngx_array_var_sha} \
    --add-dynamic-module=./srcache-nginx-module-%{ngx_srcache_sha} \
    --add-dynamic-module=./redis2-nginx-module-%{ngx_redis2_sha} \
    --add-dynamic-module=./ngx_http_redis-%{ngx_redis_version} \
    --add-dynamic-module=./echo-nginx-module-%{ngx_echo_version} \
%if %{with upstream_check}
    --add-module=./ngx_http_dyups_module-%{ngx_dyups_sha} \
    --add-module=./nginx_upstream_check_module-%{ngx_upstream_check_sha} \
%else
    --add-dynamic-module=./ngx_http_dyups_module-%{ngx_dyups_sha} \
%endif
    --add-dynamic-module=./njs-%{ngx_njs_sha}/nginx \
    --add-dynamic-module=./nginx-upload-module-%{ngx_upload_sha} \
    --add-dynamic-module=./nginx-upload-progress-module-%{ngx_upload_progress_version} \
%if %{with x_rid_header}
    --add-dynamic-module=./nginx-x-rid-header-%{ngx_x_rid_sha} \
%endif
    --add-dynamic-module=./nginx-goodies-nginx-sticky-module-ng-%{ngx_sticky_sha} \
    --add-dynamic-module=./nginx-http-rdns-%{ngx_rdns_sha} \
    --add-dynamic-module=./ngx_pagespeed-%{ngx_pagespeed_version}-beta \
    --add-dynamic-module=./nginx-module-vts-%{ngx_vts_version} \
%if %{with sregex}
    --add-dynamic-module=./replace-filter-nginx-module-%{ngx_replace_filter_sha} \
%endif  # with sregex
    --with-debug \
%if 0%{rhel} <= 6
    --with-cc=/opt/rh/devtoolset-2/root/usr/bin/gcc \
%endif
    --with-cc-opt="%{optflags} $(pcre-config --cflags) -fPIC" \
    --with-ld-opt="$RPM_LD_FLAGS -Wl,-E -Wl,-z,now -pie" # so the perl module finds its symbols

sed -i 's|openssl no\-shared|openssl no-shared -fPIC|' objs/Makefile

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALLDIRS=vendor

find %{buildroot} -type f -name .packlist -exec rm -f '{}' \;
find %{buildroot} -type f -name perllocal.pod -exec rm -f '{}' \;
find %{buildroot} -type f -empty -exec rm -f '{}' \;
find %{buildroot} -type f -iname '*.so' -exec chmod 0755 '{}' \;

%if %{with systemd}
install -p -D -m 0644 %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
%else
install -p -D -m 0755 %{SOURCE15} %{buildroot}%{_initddir}/%{name}
%endif

install -p -D -m 0644 %{SOURCE11} \
    %{buildroot}%{_sysconfdir}/logrotate.d/nginx

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/nginx/conf.d
install -p -d -m 0755 %{buildroot}%{_sysconfdir}/nginx/default.d

%if %{with passenger}
install -p -m 0644 %{SOURCE150} %{buildroot}%{_sysconfdir}/nginx/conf.d
sed -i "s|PASSENGER_ROOT|%{ruby_vendorlibdir}/phusion_passenger/locations.ini|" \
    %{buildroot}%{_sysconfdir}/nginx/conf.d/passenger.conf
%endif  # with passenger

%if %{with java}
install -p -d -m 0755 %{buildroot}%{_javadir}
install -p -D -m 0755 %{SOURCE401} %{buildroot}%{_javadir}
install -p -D -m 0755 %{SOURCE402} %{buildroot}%{_javadir}
install -p -D -m 0755 %{SOURCE403} %{buildroot}%{_javadir}
%endif

install -p -d -m 0700 %{buildroot}%{_localstatedir}/lib/nginx
install -p -d -m 0700 %{buildroot}%{_localstatedir}/lib/nginx/tmp
install -p -d -m 0700 %{buildroot}%{_localstatedir}/log/nginx

install -p -d -m 0755 %{buildroot}%{_datadir}/nginx/html
install -p -d -m 0755 %{buildroot}%{_datadir}/nginx/modules
install -p -d -m 0755 %{buildroot}%{_libdir}/nginx/modules

install -p -m 0644 %{SOURCE12} \
    %{buildroot}%{_sysconfdir}/nginx
install -p -m 0644 %{SOURCE100} \
    %{buildroot}%{_datadir}/nginx/html
install -p -m 0644 %{SOURCE101} %{SOURCE102} \
    %{buildroot}%{_datadir}/nginx/html
install -p -m 0644 %{SOURCE103} %{SOURCE104} \
    %{buildroot}%{_datadir}/nginx/html

%if 0%{?with_mailcap_mimetypes}
rm -f %{buildroot}%{_sysconfdir}/nginx/mime.types
%endif

install -p -D -m 0644 %{_builddir}/nginx-%{version}/man/nginx.8 \
    %{buildroot}%{_mandir}/man8/nginx.8

install -p -D -m 0755 %{SOURCE13} %{buildroot}%{_bindir}/nginx-upgrade
install -p -D -m 0644 %{SOURCE14} %{buildroot}%{_mandir}/man8/nginx-upgrade.8

for i in ftdetect indent syntax; do
    install -p -D -m644 contrib/vim/${i}/nginx.vim \
        %{buildroot}%{_datadir}/vim/vimfiles/${i}/nginx.vim
done

echo 'load_module "%{_libdir}/nginx/modules/ngx_http_geoip_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-geoip.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_image_filter_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-image-filter.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_perl_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-perl.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_xslt_filter_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-xslt-filter.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_mail_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-mail.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_stream_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-stream.conf

echo 'load_module "%{_libdir}/nginx/modules/ndk_http_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-devel-kit.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_array_var_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-array-var.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_headers_more_filter_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-headers-more-filter.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_sorted_querystring_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-sorted-querystring.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_rtmp_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-rtmp.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_cache_purge_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-cache-purge.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_redis_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-redis.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_redis2_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-redis2.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_srcache_filter_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-srcache-filter.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_echo_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-echo.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_upload_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-upload.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_uploadprogress_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-uploadprogress.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_vhost_traffic_status_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-vts.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_pagespeed.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-pagespeed.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_rdns_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-rdns.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_sticky_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-sticky.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_js_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-njs.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_stream_js_module.so";' \
    >> %{buildroot}%{_datadir}/nginx/modules/mod-njs.conf

%if !%{with upstream_check}
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_dyups_module.so";' \
    >> %{buildroot}%{_datadir}/nginx/modules/mod-http-dyups.conf
%endif

%if %{with x_rid_header}
echo 'load_module "%{_libdir}/nginx/modules/ngx_x_rid_header_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-x-rid-header.conf
%endif  # with x_rid_header

%if %{with lua}
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_lua_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-lua.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_lua_cache_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-lua-cache.conf
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_lua_upstream_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-lua-upstream.conf
%endif  # with lua

%if %{with java}
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_clojure_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-clojure.conf
%endif  # with java

%if %{with passenger}
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_passenger_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-passenger.conf
%endif  # with passenger

%if %{with sregex}
echo 'load_module "%{_libdir}/nginx/modules/ngx_http_replace_filter_module.so";' \
    > %{buildroot}%{_datadir}/nginx/modules/mod-http-replace-filter.conf
%endif  # with sregex


%pre filesystem
getent group %{nginx_user} > /dev/null || groupadd -r %{nginx_user}
getent passwd %{nginx_user} > /dev/null || \
    useradd -r -d %{_localstatedir}/lib/nginx -g %{nginx_user} \
    -s /sbin/nologin -c "Nginx web server" %{nginx_user}
exit 0

%post
%if %{with systemd}
echo "Executing systemd post-install tasks"
%systemd_post nginx.service
%else
echo "Executing System V post-install tasks"
/sbin/chkconfig --add %{name}
%endif

%post mod-http-geoip
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-image-filter
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-perl
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-xslt-filter
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-mail
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-stream
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-devel-kit
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-array-var
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-headers-more-filter
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-sorted-querystring
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-rtmp
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-cache-purge
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-redis
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-redis2
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-srcache-filter
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-echo
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-upload
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-uploadprogress
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-vts
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-pagespeed
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-rdns
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-sticky
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-njs
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%if !%{with upstream_check}
%post mod-http-dyups
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi
%endif

%if %{with x_rid_header}
%post mod-x-rid-header
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi
%endif  # with x_rid_header

%if %{with lua}
%post mod-http-lua
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-lua-cache
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi

%post mod-http-lua-upstream
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi
%endif  # with lua

%if %{with java}
%post mod-http-clojure
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi
%endif  # with java

%if %{with passenger}
%post mod-passenger
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi
%endif  # with passenger

%if %{with sregex}
%post mod-http-replace-filter
if [ $1 -eq 1 ]; then
%if %{with systemd}
    /usr/bin/systemctl reload %{name}.service >/dev/null 2>&1 || :
%else
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
%endif
fi
%endif  # with sregex


%preun
%if %{with systemd}
echo "Executing systemd pre-uninstall tasks"
%systemd_preun nginx.service
%else
echo "Executing System V pre-uninstall tasks"
if [ $1 -eq 0 ] ; then
    /sbin/service %{name} stop >/dev/null 2>&1
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if %{with systemd}
echo "Executing systemd post-uninstall tasks"
%systemd_postun nginx.service
%else
echo "Executing System V post-uninstall tasks"
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif
if [ $1 -ge 1 ]; then
    /usr/bin/nginx-upgrade >/dev/null 2>&1 || :
fi

%files
%license LICENSE
%doc CHANGES README README.dynamic
%{_datadir}/nginx/html/*
%{_bindir}/nginx-upgrade
%{_sbindir}/nginx
%{_datadir}/vim/vimfiles/ftdetect/nginx.vim
%{_datadir}/vim/vimfiles/syntax/nginx.vim
%{_datadir}/vim/vimfiles/indent/nginx.vim
%{_mandir}/man3/nginx.3pm*
%{_mandir}/man8/nginx.8*
%{_mandir}/man8/nginx-upgrade.8*

%if %{with systemd}
%config %{_unitdir}/%{name}.service
%else
%{_initddir}/%{name}
%endif

%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf
%config(noreplace) %{_sysconfdir}/nginx/fastcgi.conf.default
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params
%config(noreplace) %{_sysconfdir}/nginx/fastcgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/koi-utf
%config(noreplace) %{_sysconfdir}/nginx/koi-win
%if ! 0%{?with_mailcap_mimetypes}
%config(noreplace) %{_sysconfdir}/nginx/mime.types
%endif
%config(noreplace) %{_sysconfdir}/nginx/mime.types.default
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf
%config(noreplace) %{_sysconfdir}/nginx/nginx.conf.default
%config(noreplace) %{_sysconfdir}/nginx/scgi_params
%config(noreplace) %{_sysconfdir}/nginx/scgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params
%config(noreplace) %{_sysconfdir}/nginx/uwsgi_params.default
%config(noreplace) %{_sysconfdir}/nginx/win-utf
%config(noreplace) %{_sysconfdir}/logrotate.d/nginx
%attr(700,%{nginx_user},%{nginx_user}) %dir %{_localstatedir}/lib/nginx
%attr(700,%{nginx_user},%{nginx_user}) %dir %{_localstatedir}/lib/nginx/tmp
%attr(700,%{nginx_user},%{nginx_user}) %dir %{_localstatedir}/log/nginx
%dir %{_libdir}/nginx/modules

%files all-modules

%files filesystem
%dir %{_datadir}/nginx
%dir %{_datadir}/nginx/html
%dir %{_sysconfdir}/nginx
%dir %{_sysconfdir}/nginx/conf.d
%dir %{_sysconfdir}/nginx/default.d

%files mod-http-geoip
%{_datadir}/nginx/modules/mod-http-geoip.conf
%{_libdir}/nginx/modules/ngx_http_geoip_module.so

%files mod-http-image-filter
%{_datadir}/nginx/modules/mod-http-image-filter.conf
%{_libdir}/nginx/modules/ngx_http_image_filter_module.so

%files mod-http-perl
%{_datadir}/nginx/modules/mod-http-perl.conf
%{_libdir}/nginx/modules/ngx_http_perl_module.so
%dir %{perl_vendorarch}/auto/nginx
%{perl_vendorarch}/nginx.pm
%{perl_vendorarch}/auto/nginx/nginx.so

%files mod-http-xslt-filter
%{_datadir}/nginx/modules/mod-http-xslt-filter.conf
%{_libdir}/nginx/modules/ngx_http_xslt_filter_module.so

%files mod-mail
%{_datadir}/nginx/modules/mod-mail.conf
%{_libdir}/nginx/modules/ngx_mail_module.so

%files mod-stream
%{_datadir}/nginx/modules/mod-stream.conf
%{_libdir}/nginx/modules/ngx_stream_module.so

%files mod-devel-kit
%{_datadir}/nginx/modules/mod-devel-kit.conf
%{_libdir}/nginx/modules/ndk_http_module.so

%files mod-http-array-var
%{_datadir}/nginx/modules/mod-http-array-var.conf
%{_libdir}/nginx/modules/ngx_http_array_var_module.so

%files mod-http-headers-more-filter
%{_datadir}/nginx/modules/mod-http-headers-more-filter.conf
%{_libdir}/nginx/modules/ngx_http_headers_more_filter_module.so

%files mod-http-sorted-querystring
%{_datadir}/nginx/modules/mod-http-sorted-querystring.conf
%{_libdir}/nginx/modules/ngx_http_sorted_querystring_module.so

%files mod-rtmp
%{_datadir}/nginx/modules/mod-rtmp.conf
%{_libdir}/nginx/modules/ngx_rtmp_module.so

%files mod-http-cache-purge
%{_datadir}/nginx/modules/mod-http-cache-purge.conf
%{_libdir}/nginx/modules/ngx_http_cache_purge_module.so

%files mod-http-redis
%{_datadir}/nginx/modules/mod-http-redis.conf
%{_libdir}/nginx/modules/ngx_http_redis_module.so

%files mod-http-redis2
%{_datadir}/nginx/modules/mod-http-redis2.conf
%{_libdir}/nginx/modules/ngx_http_redis2_module.so

%files mod-http-srcache-filter
%{_datadir}/nginx/modules/mod-http-srcache-filter.conf
%{_libdir}/nginx/modules/ngx_http_srcache_filter_module.so

%files mod-http-echo
%{_datadir}/nginx/modules/mod-http-echo.conf
%{_libdir}/nginx/modules/ngx_http_echo_module.so

%files mod-http-upload
%{_datadir}/nginx/modules/mod-http-upload.conf
%{_libdir}/nginx/modules/ngx_http_upload_module.so

%files mod-http-uploadprogress
%{_datadir}/nginx/modules/mod-http-uploadprogress.conf
%{_libdir}/nginx/modules/ngx_http_uploadprogress_module.so

%files mod-http-vts
%{_datadir}/nginx/modules/mod-http-vts.conf
%{_libdir}/nginx/modules/ngx_http_vhost_traffic_status_module.so

%files mod-pagespeed
%{_datadir}/nginx/modules/mod-pagespeed.conf
%{_libdir}/nginx/modules/ngx_pagespeed.so

%files mod-http-rdns
%{_datadir}/nginx/modules/mod-http-rdns.conf
%{_libdir}/nginx/modules/ngx_http_rdns_module.so

%files mod-http-sticky
%{_datadir}/nginx/modules/mod-http-sticky.conf
%{_libdir}/nginx/modules/ngx_http_sticky_module.so

%files mod-njs
%{_datadir}/nginx/modules/mod-njs.conf
%{_libdir}/nginx/modules/ngx_http_js_module.so
%{_libdir}/nginx/modules/ngx_stream_js_module.so

%if !%{with upstream_check}
%files mod-http-dyups
%{_datadir}/nginx/modules/mod-http-dyups.conf
%{_libdir}/nginx/modules/ngx_http_dyups_module.so
%endif

%if %{with x_rid_header}
%files mod-x-rid-header
%{_datadir}/nginx/modules/mod-x-rid-header.conf
%{_libdir}/nginx/modules/ngx_x_rid_header_module.so
%endif  # with x_rid_header

%if %{with lua}
%files mod-http-lua
%{_datadir}/nginx/modules/mod-http-lua.conf
%{_libdir}/nginx/modules/ngx_http_lua_module.so

%files mod-http-lua-cache
%{_datadir}/nginx/modules/mod-http-lua-cache.conf
%{_libdir}/nginx/modules/ngx_http_lua_cache_module.so

%files mod-http-lua-upstream
%{_datadir}/nginx/modules/mod-http-lua-upstream.conf
%{_libdir}/nginx/modules/ngx_http_lua_upstream_module.so
%endif  # with lua

%if %{with java}
%files mod-http-clojure
%{_datadir}/nginx/modules/mod-http-clojure.conf
%{_libdir}/nginx/modules/ngx_http_clojure_module.so
%{_javadir}/nginx-clojure-%{ngx_clojure_jar_version}.jar
%{_javadir}/nginx-jersey-%{ngx_clojure_jersey_version}.jar
%{_javadir}/nginx-tomcat8-%{ngx_clojure_tomcat_version}.jar
%endif  # with java

%if %{with passenger}
%files mod-passenger
%{_sysconfdir}/nginx/conf.d/passenger.conf
%{_datadir}/nginx/modules/mod-passenger.conf
%{_libdir}/nginx/modules/ngx_http_passenger_module.so
%endif  # with passenger

%if %{with sregex}
%files mod-http-replace-filter
%{_datadir}/nginx/modules/mod-http-replace-filter.conf
%{_libdir}/nginx/modules/ngx_http_replace_filter_module.so
%endif  # with sregex


%changelog
* Tue Feb 21 2018 Frankie Dintino <fdintino@gmail.com> - 2:1.12.2-2
- Update nginx-cache-purge module and nginx-upload-module (the latter
  to support http2)

* Mon Nov 20 2017 Frankie Dintino <fdintino@gmail.com> - 2:1.12.2-1
- Bump epoch so we always trump epel
- Update to 1.12.2

* Mon Sep 25 2017 Frankie Dintino <fdintino@gmail.com> - 1:1.12.1-3
- Update ngx_cache_purge

* Sat Sep 23 2017 Frankie Dintino <fdintino@gmail.com> - 1:1.12.1-2
- Switch to better-maintained fork of ngx_cache_purge, fix segfault
- Update to newer nginx-clojure jars

* Thu Aug 10 2017 Frankie Dintino <fdintino@gmail.com> - 1:1.12.1-1
- Update to upstream release 1.12.1

* Sun Dec 11 2016 Frankie Dintino <fdintino@gmail.com> - 1:1.11.6-4
- Fix typo in lua Requires: of nginx-mod-http-dyups

* Fri Dec 09 2016 Frankie Dintino <fdintino@gmail.com> - 1:1.11.6-1
- update to upstream release 1.11.6
- add a bunch of dynamic modules

* Mon Oct 31 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.2-1
- update to upstream release 1.10.2

* Tue May 31 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.1-1
- update to upstream release 1.10.1

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.10.0-4
- Perl 5.24 rebuild

* Sun May  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.10.0-3
- Enable AIO on aarch64 (rhbz 1258414)

* Wed Apr 27 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.0-2
- only Require nginx-all-modules for EPEL and current Fedora releases

* Wed Apr 27 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.10.0-1
- update to upstream release 1.10.0
- split dynamic modules into subpackages
- spec file cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.1-1
- update to upstream release 1.8.1
- CVE-2016-0747: Insufficient limits of CNAME resolution in resolver
- CVE-2016-0746: Use-after-free during CNAME response processing in resolver
- CVE-2016-0742: Invalid pointer dereference in resolver

* Sun Oct 04 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-14
- consistently use '%%global with_foo' style of logic
- remove PID file before starting nginx (#1268621)

* Fri Sep 25 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:1.8.0-13
- Use nginx-mimetypes from mailcap (#1248736)
- Mark LICENSE as %%license

* Thu Sep 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-12
- also build with gperftools on aarch64 (#1258412)

* Wed Aug 12 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1:1.8.0-11
- nginx.conf: added commented-out SSL configuration directives (#1179232)

* Fri Jul 03 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-10
- switch back to /bin/kill in logrotate script due to SELinux denials

* Tue Jun 16 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-9
- fix path to png in error pages (#1232277)
- optimize png images with optipng

* Sun Jun 14 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-8
- replace /bin/kill with /usr/bin/systemctl kill in logrotate script (#1231543)
- remove After=syslog.target in nginx.service (#1231543)
- replace ExecStop with KillSignal=SIGQUIT in nginx.service (#1231543)

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.8.0-7
- Perl 5.22 rebuild

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-6
- revert previous change

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-5
- move default server to default.conf (#1220094)

* Sun May 10 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-4
- add TimeoutStopSec=5 and KillMode=mixed to nginx.service
- set worker_processes to auto
- add some common options to the http block in nginx.conf
- run nginx-upgrade on package update
- remove some redundant scriptlet commands
- listen on ipv6 for default server (#1217081)

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-3
- improve nginx-upgrade script

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-2
- add --with-pcre-jit

* Wed Apr 22 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.8.0-1
- update to upstream release 1.8.0

* Thu Apr 09 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.7.12-1
- update to upstream release 1.7.12

* Sun Feb 15 2015 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.7.10-1
- update to upstream release 1.7.10
- remove systemd conditionals

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-4
- fix package ownership of directories

* Wed Oct 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-3
- add vim files (#1142849)

* Mon Sep 22 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-2
- create nginx-filesystem subpackage (patch from Remi Collet)
- create /etc/nginx/default.d as a drop-in directory for configuration files
  for the default server block
- clean up nginx.conf

* Wed Sep 17 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.2-1
- update to upstream release 1.6.2
- CVE-2014-3616 nginx: virtual host confusion (#1142573)

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:1.6.1-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.1-2
- add logic for EPEL 7

* Tue Aug 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.1-1
- update to upstream release 1.6.1
- (#1126891) CVE-2014-3556: SMTP STARTTLS plaintext injection flaw

* Wed Jul 02 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 1:1.6.0-3
- Fix FTBFS on aarch64 (#1115559)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.6.0-1
- update to upstream release 1.6.0

* Tue Mar 18 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.7-1
- update to upstream release 1.4.7

* Wed Mar 05 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.6-1
- update to upstream release 1.4.6

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.5-2
- avoid multiple index directives (#1065488)

* Sun Feb 16 2014 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.5-1
- update to upstream release 1.4.5

* Wed Nov 20 2013 Peter Borsa <peter.borsa@gmail.com> - 1:1.4.4-1
- Update to upstream release 1.4.4
- Security fix BZ 1032267

* Sun Nov 03 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.3-1
- update to upstream release 1.4.3

* Fri Aug 09 2013 Jonathan Steffan <jsteffan@fedoraproject.org> - 1:1.4.2-3
- Add in conditionals to build for non-systemd targets

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1:1.4.2-2
- Perl 5.18 rebuild

* Fri Jul 19 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.2-1
- update to upstream release 1.4.2

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1:1.4.1-3
- Perl 5.18 rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 1:1.4.1-2
- rebuild for new GD 2.1.0

* Tue May 07 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.1-1
- update to upstream release 1.4.1 (#960605, #960606):
  CVE-2013-2028 stack-based buffer overflow when handling certain chunked
  transfer encoding requests

* Sun Apr 28 2013 Dan Horák <dan[at]danny.cz> - 1:1.4.0-2
- gperftools exist only on selected arches

* Fri Apr 26 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.4.0-1
- update to upstream release 1.4.0
- enable SPDY module (new in this version)
- enable http gunzip module (new in this version)
- enable google perftools module and add gperftools-devel to BR
- enable debugging (#956845)
- trim changelog

* Tue Apr 02 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.8-1
- update to upstream release 1.2.8

* Fri Feb 22 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.7-2
- make sure nginx directories are not world readable (#913724, #913735)

* Sat Feb 16 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.7-1
- update to upstream release 1.2.7
- add .asc file

* Tue Feb 05 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-6
- use 'kill' instead of 'systemctl' when rotating log files to workaround
  SELinux issue (#889151)

* Wed Jan 23 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-5
- uncomment "include /etc/nginx/conf.d/*.conf by default but leave the
  conf.d directory empty (#903065)

* Wed Jan 23 2013 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-4
- add comment in nginx.conf regarding "include /etc/nginf/conf.d/*.conf"
  (#903065)

* Wed Dec 19 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-3
- use correct file ownership when rotating log files

* Tue Dec 18 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-2
- send correct kill signal and use correct file permissions when rotating
  log files (#888225)
- send correct kill signal in nginx-upgrade

* Tue Dec 11 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.6-1
- update to upstream release 1.2.6

* Sat Nov 17 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.5-1
- update to upstream release 1.2.5

* Sun Oct 28 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.4-1
- update to upstream release 1.2.4
- introduce new systemd-rpm macros (#850228)
- link to official documentation not the community wiki (#870733)
- do not run systemctl try-restart after package upgrade to allow the
  administrator to run nginx-upgrade and avoid downtime
- add nginx man page (#870738)
- add nginx-upgrade man page and remove README.fedora
- remove chkconfig from Requires(post/preun)
- remove initscripts from Requires(preun/postun)
- remove separate configuration files in "/etc/nginx/conf.d" directory
  and revert to upstream default of a centralized nginx.conf file
  (#803635) (#842738)

* Fri Sep 21 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.3-1
- update to upstream release 1.2.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1:1.2.1-2
- Perl 5.16 rebuild

* Sun Jun 10 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.1-1
- update to upstream release 1.2.1

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 1:1.2.0-2
- Perl 5.16 rebuild

* Wed May 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.2.0-1
- update to upstream release 1.2.0

* Wed May 16 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-4
- add nginx-upgrade to replace functionality from the nginx initscript
  that was lost after migration to systemd
- add README.fedora to describe usage of nginx-upgrade
- nginx.logrotate: use built-in systemd kill command in postrotate script
- nginx.service: start after syslog.target and network.target
- nginx.service: remove unnecessary references to config file location
- nginx.service: use /bin/kill instead of "/usr/sbin/nginx -s" following
  advice from nginx-devel
- nginx.service: use private /tmp

* Mon May 14 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-3
- fix incorrect postrotate script in nginx.logrotate

* Thu Apr 19 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-2
- renable auto-cc-gcc patch due to warnings on rawhide

* Sat Apr 14 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.15-1
- update to upstream release 1.0.15
- no need to apply auto-cc-gcc patch
- add %%global _hardened_build 1

* Thu Mar 15 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.14-1
- update to upstream release 1.0.14
- amend some %%changelog formatting

* Tue Mar 06 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.13-1
- update to upstream release 1.0.13
- amend --pid-path and --log-path

* Sun Mar 04 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-5
- change pid path in nginx.conf to match systemd service file

* Sun Mar 04 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-3
- fix %%pre scriptlet

* Mon Feb 20 2012 Jamie Nguyen <jamielinux@fedoraproject.org> - 1:1.0.12-2
- update upstream URL
- replace %%define with %%global
- remove obsolete BuildRoot tag, %%clean section and %%defattr
- remove various unnecessary commands
- add systemd service file and update scriptlets
- add Epoch to accommodate %%triggerun as part of systemd migration

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.12-1
- Update to 1.0.12

* Thu Nov 17 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.10-1
- Bugfix: a segmentation fault might occur in a worker process if resolver got a big DNS response. Thanks to Ben Hawkes.
- Bugfix: in cache key calculation if internal MD5 implementation wasused; the bug had appeared in 1.0.4.
- Bugfix: the module ngx_http_mp4_module sent incorrect "Content-Length" response header line if the "start" argument was used. Thanks to Piotr Sikora.

* Thu Oct 27 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.8-1
- Update to new 1.0.8 stable release

* Fri Aug 26 2011 Keiran "Affix" Smith <fedora@affix.me> - 1.0.5-1
- Update nginx to Latest Stable Release

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-3
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.0.0-2
- Perl 5.14 mass rebuild

* Wed Apr 27 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.0.0-1
- Update to 1.0.0

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.53-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53.5
- Extract out default config into its own file (bug #635776)

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-4
- Revert ownership of log dir

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-3
- Change ownership of /var/log/nginx to be 0700 nginx:nginx
- update init script to use killproc -p
- add reopen_logs command to init script
- update init script to use nginx -q option

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-2
- Fix linking of perl module

* Sun Oct 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.8.53-1
- Update to new stable 0.8.53

* Sat Jul 31 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-2
- add Provides: webserver (bug #619693)

* Sun Jun 20 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.67-1
- Update to new stable 0.7.67
- fix bugzilla #591543

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.7.65-2
- Mass rebuild with perl-5.12.0

* Mon Feb 15 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.65-1
- Update to new stable 0.7.65
- change ownership of logdir to root:root
- add support for ipv6 (bug #561248)
- add random_index_module
- add secure_link_module

* Fri Dec 04 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 0.7.64-1
- Update to new stable 0.7.64
