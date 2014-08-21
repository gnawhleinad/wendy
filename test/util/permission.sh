#!/bin/bash

sudo chgrp --recursive docker /var/lib/jenkins && sudo chmod --recursive g+w /var/lib/jenkins
