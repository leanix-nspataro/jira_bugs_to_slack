# Jira bugs to Slack #bugs channel

## Requirements
- python 3.x  
- pip 3.x
- slack-sdk (current)
- jira (current)

## Abstract
The purpose of this script is to create visibility into what bugs are being created.  If all engineers are able to easily see which bugs are created, less engineers need to search for if their problem is truly a bug.

## SDKs

This code utilizes the Jira and Slack python SDKs.  The API/SDK documentation for [Jira](https://jira.readthedocs.io/) and [Slack](https://slack.dev/python-slack-sdk/faq.html#python-documents) can help with future development.  

## Current functionality
- get bugs created yesterday in Jira 
- post bugs in the Slack bugs Channel
