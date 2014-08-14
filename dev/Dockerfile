FROM ubuntu:14.04

RUN apt-get update && apt-get install -y wget git openjdk-7-jre-headless
RUN wget -q -O - http://pkg.jenkins-ci.org/debian-stable/jenkins-ci.org.key | apt-key add -
RUN sh -c 'echo deb http://pkg.jenkins-ci.org/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
RUN apt-get update && apt-get install -y jenkins

VOLUME /var/lib/jenkins
ENV JENKINS_HOME /var/lib/jenkins

EXPOSE 8080

ADD run.sh /usr/local/bin/run
RUN chmod +x /usr/local/bin/run

CMD /usr/local/bin/run
