# covidresourcesassam
Repo of covid resources in assam. Dynamically updated to website https://covidresourcesassam.firebaseapp.com/ 

This is fight towards COVID 19 , extending any help to people of Assam

[![Deploy to Firebase Hosting on merge](https://github.com/jptalukdar/covidresourcesassam/actions/workflows/firebase-hosting-merge.yml/badge.svg?branch=master)](https://github.com/jptalukdar/covidresourcesassam/actions/workflows/firebase-hosting-merge.yml)

## Live Deployment

Site is live as https://covidresourcesassam.firebaseapp.com/

## Generate Site data

Execute ```python renderer.py``` to generate the site under directory public/

## To add new resources

1. Go to resources/resource-list.yml
1. Updated at the last the data related to the resource
1. Following is an example of resource you can add

Eg Resource

```code
- name: <Name of the resource>
  description: | 
    <description of the resources>
  phone: <phone number if any of the resource>
  type: [website | person | website]
```

## Report
To report , please raise a issue at https://github.com/jptalukdar/covidresourcesassam/issues under label reportIssue

## Submit a new resource
To submit a resource raise a issue at https://github.com/jptalukdar/covidresourcesassam/issues under label submitResource

## Contribute

Fork the repo, Modify your changes , raise a Pull request against ``develop`` branch


## Extending the project to other states

Please clone the repository and maintain the resource list. 
To Auto setup firebase hosting , visit: https://firebase.google.com/docs/hosting/github-integration?authuser=0