#!/bin/bash

group="$1"
sudo chgrp --recursive $group /var/lib/jenkins && sudo chmod --recursive g+w /var/lib/jenkins
