FROM centos:latest
MAINTAINER kang@mozilla.com
RUN yum -y update && \
  yum -y install mercurial && \
  yum clean all
COPY hgweb.conf /etc/hgweb.conf
COPY hgweb.cgi /usr/local/bin
# Create test repo
RUN mkdir /data && cd /data && \
  hg clone https://hg.mozilla.org/hgcustom/hg_templates/
CMD hg serve --webdir-conf /etc/hgweb.conf
EXPOSE 8000
