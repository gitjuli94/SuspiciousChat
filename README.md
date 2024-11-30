# Suspicious Chat

LINK: https://github.com/gitjuli94/SuspiciousChat


installation instructions if needed


### Chosen flaws from OWASP Top 10:2021:
1) A01:2021 - Broken Access Control
2) A03:2021 - Injection
3) A05:2021 - Security Misconfiguration
4) A07:2021 - Identification and Authentication Failures
5) A09:2021 - Security Logging and Monitoring Failures

## FLAW 1: A01:2021 - Broken Access Control

Problem
A non-admin user can delete messages.

Fix
The verification if the user is staff (admin) should be added. Solution is commented out here:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#83

## FLAW 2: A03:2021 - Injection

Problem
In the function, the SQL query is done with raw input instead of the Django ORM (Object-Relational Mapping), which automatically escapes user input to prevent SQL injection. By using ChatMessage.objects.raw(...) with user-provided input directly, the application becomes vulnerable to SQL injection attacks, as attackers can manipulate the input to execute arbitrary SQL commands, potentially exposing or modifying sensitive data.

https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#90

Fix
The issue can be fixed by using the Django ORM commands which prevent injections. The correct commands are in the following lines:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#91
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#92

## FLAW 3: A05:2021 - Security Misconfiguration

Problem
Here we can see predictable credentials, the hard-coded admin account has an easy to guess password (admin). In addition, the hard-coded passwords are visible in the source code, making it publicly available.

https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#9
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#15

Fix
The hardcoded credentials should be removed and the repository should be made private. Also the passwords should be harder to guess.

## FLAW 4: A07:2021 - Identification and Authentication Failures

Problem
Unauthenticated users can access the forum and add new messages.

Problems shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#44
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#54
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#62
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#78

Fix
The @login_required decorator should be added before all the functions related to the forum page. Otherwise unauthenticated users can access the forum.

## FLAW 5: Security Logging and Monitoring Failures

Problem
The log in attempts are not logged, which could lead to an attacker to brute-force credentials without being detected.

Fix
The log in attempts can be logged using a Django model ”FailedLoginAttempt” in models.py file. When a user fails to log in, it stores the username, IP address, and timestamp in the model. The IP address can be acquired using a helper function added in the end of views.py file.

Solution is commented out here:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/models.py#8
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#36
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#37
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#99

