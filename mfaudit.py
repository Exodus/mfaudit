#!/usr/bin/env python3
import sys
import argparse
import boto3
import botocore.exceptions

PARSER = argparse.ArgumentParser(
    description='Check which console user does not have MFA')
PARSER.add_argument('profile', help='The AWS Profile to use')
ARGS = PARSER.parse_args()

try:
    boto3.setup_default_session(profile_name=ARGS.profile)
except botocore.exceptions.ProfileNotFound:
    print('AWS Profile not found')
    sys.exit(1)

iam = boto3.resource("iam")
users = [user for user in iam.users.all()]
console_users = []
for idx,user in enumerate(users):
    print("Profile {0} of {1} \r".format(idx, len(users)),end='')
    profile = user.LoginProfile()
    try:
        profile.load()
        console_users.append(user)
    except botocore.exceptions.ClientError as e:
        if 'NoSuchEntity' not in e.response['Error']['Code']:
            print(e.response['Error']['Code'])

abusers = [user for user in console_users if not any(user.mfa_devices.all())]

print('\nThis is the list of users without MFA:')
for abuser in abusers:
    print(abuser.user_name)