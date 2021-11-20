from jira import JIRA
from datetime import datetime, timedelta
from slack_sdk import WebClient as slackr

## Purpose: get Jira bug data and return array of pertinent information
class jiraBugs:
    ## datetime
    yesterday_date = (datetime.today() - timedelta(days=1)).date()
    today_date = datetime.now().date()

    ## jira
    options = {'server': 'https://leanix.atlassian.net'}
    da_jira = JIRA(options, basic_auth=('<user>', '<token>'))
    projects = da_jira.projects()

    ## functions
    def get_yesterday_bugs(self):
        # searches jira bugs created yesterday
        # returns array of jira bugs as dict objects
        all_issues = []
        for a_project in self.projects:
            issues_in_proj = self.da_jira.search_issues('project='+str(a_project)+' AND created >= "'+str(self.yesterday_date)+'" AND created <="'+str(self.today_date)+'" AND issuetype="Bug"' )
            for an_issue in issues_in_proj:
                newishew = {}
                da_issue = an_issue.raw
                newishew['id'] = da_issue['id']
                newishew['key'] = da_issue['key']
                newishew['link'] = da_issue['self']
                newishew['project'] = str(a_project)
                newishew['issuetype'] = da_issue['fields']['issuetype']['name']
                newishew['priority'] = da_issue['fields']['priority']['name']
                newishew['status'] = da_issue['fields']['status']['name']
                newishew['created'] = da_issue['fields']['created']
                newishew['summary'] = da_issue['fields']['summary']
                newishew['description'] = da_issue['fields']['description']

                all_issues.append(newishew)
            
        return all_issues

## Purpose: send Jira bugs to slack bug channel
class sendToSlack:
    ## slack
    channel_id = 'C02N5DQUZ4L' # bugs channel
    slack_token = '<slack token>'
    slack_client = slackr(token=slack_token)

    ## functions
    def postMessageToSlack(self, all_messages):
        num_msg = len(all_messages)

        if num_msg == 0:
            print('No bugs for you.')

        elif num_msg == 1:
            self.slack_client.chat_postMessage(
                unfurl_links=True,
                channel=self.channel_id,
                blocks=[
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": 'Jira Key: '+all_messages[0]['key']
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": '[Link to '+all_messages[0]['key']+']('+all_messages[0]['link']+')'
                        }
                    },
                    {
                        "type": "section",
                        "text": 'Summary: '+all_messages[0]['summary']
                    },
                    {
                        "type": "section",
                        "text": 'Description: '+all_messages[0]['description']
                    }
                ]
            )
            
        else:
            for msg in all_messages:
                self.slack_client.chat_postMessage(
                    unfurl_links=True,
                    channel=self.channel_id,
                    blocks=[
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": 'Jira Key: '+msg['key']
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": '[Link to '+msg['key']+']('+msg['key']+')'
                            }
                        },
                        {
                            "type": "section",
                            "text": 'Summary: '+msg['summary']
                        },
                        {
                            "type": "section",
                            "text": 'Description: '+msg['description']
                        }
                    ]    
                )

if __name__ == '__main__':
    jB = jiraBugs() 
    all_jira_bugs_yesterday = jB.get_yesterday_bugs()

    sts = sendToSlack()
    sts.postMessageToSlack(all_jira_bugs_yesterday)