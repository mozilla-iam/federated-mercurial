FROM centos:latest
MAINTAINER kang <kang@insecure.ws>

# Update image & basic dev tools
RUN yum update -y && \
    yum install -y sudo && \
    yum install -y epel-release && \
    yum groupinstall -y 'Development Tools'

# Install access-proxy-specific packages
RUN yum install -y openssl-devel lua-devel yum-utils

# Install OpenResty
RUN yum-config-manager --add-repo https://openresty.org/package/centos/openresty.repo
RUN yum install -y openresty openresty-resty
ENV PATH=$PATH:/usr/local/openresty/luajit/bin/:/usr/local/openresty/nginx/sbin/:/usr/local/openresty/bin/

# Install LUA libs
RUN yum -y install openresty-opm
RUN opm get SkyLothar/lua-resty-jwt

# Credstash
RUN yum install -y python-pip &&  pip install credstash

# Clean
RUN yum groupremove -y 'Development Tools' && yum clean -y all

# Logs and setup
USER root
RUN  ln -sf /dev/stdout /usr/local/openresty/nginx/logs/access.log \
	&& ln -sf /dev/stderr /usr/local/openresty/nginx/logs/error.log
COPY etc/conf.d /usr/local/openresty/nginx/conf/conf.d/
COPY etc/nginx.conf /usr/local/openresty/nginx/conf/

# Ports and Docker stuff
EXPOSE 8080
STOPSIGNAL SIGTERM
ENTRYPOINT ["/usr/bin/openresty", "-g", "daemon off;"]
