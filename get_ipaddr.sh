#!/bin/sh
ip addr | grep inet | awk '{print $2}'
