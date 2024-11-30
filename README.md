# Suspicious Chat

This web application serves as a simple chat platform where logged-in users can add new messages, and admin users have the additional ability to delete messages. The application includes intentional security flaws that are commented out in the source code, providing an opportunity to study and test vulnerabilities based on the OWASP Top 10:2021. Two built-in users are included to facilitate functionality testing.

You can explore the code and the application on GitHub:
https://github.com/gitjuli94/SuspiciousChat


### Installation instructions:

To run the app, ensure that the Django framework is installed. Once set up, you can start the development server using:
```bash
python3 manage.py runserver
```

### Chosen flaws from OWASP Top 10:2021:
1) A01:2021 - Broken Access Control
2) A03:2021 - Injection
3) A05:2021 - Security Misconfiguration
4) A07:2021 - Identification and Authentication Failures
5) A09:2021 - Security Logging and Monitoring Failures

Below, each flaw is described along with its impact, the problematic code, and a suggested fix.

## FLAW 1: A01:2021 - Broken Access Control

### Problem
Non-admin users are able to delete messages due to a missing validation in the delete_chat function. This flaw allows unauthorized users to perform actions that should be restricted to administrators, violating access control policies.

### Fix
Add a verification step to ensure that only users with is_staff privileges (admin users) can delete messages. This can be achieved by adding a conditional check to verify the user's role before allowing access to the delete functionality.

Solutions shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#83

## FLAW 2: A03:2021 - Injection

### Problem
In one of the functions, raw SQL queries are executed using unvalidated user input. Specifically, the use of ChatMessage.objects.raw(...) directly embeds user-provided input into the query. This makes the application vulnerable to SQL injection attacks, enabling attackers to manipulate queries and potentially expose or modify sensitive data.

Problems shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#90

### Fix
The Django ORM ensures that queries are safe from malicious input by handling escaping and parameterization. Replace the raw SQL queries with Django ORM commands, which automatically escape user input to prevent injection attacks.

Solutions shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#91
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#92

## FLAW 3: A05:2021 - Security Misconfiguration

### Problem
The application includes hardcoded credentials, such as the admin account with the username admin and an easily guessable password admin. These credentials are exposed in the source code, making them publicly accessible.

Problems shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#9
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#15

### Fix
- Remove hardcoded credentials from the source code.
- Use environment variables to securely store usernames and passwords.
- Ensure passwords are strong and follow best practices, such as minimum length, inclusion of special characters, and avoiding dictionary words.
- Make the repository private to prevent unauthorized access.

## FLAW 4: A07:2021 - Identification and Authentication Failures

### Problem
Unauthenticated users can access the forum page and post messages. This allows unauthorized individuals to interact with the application, leading to potential misuse.

Problems shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#44
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#54
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#62
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#78

### Fix
Add the @login_required decorator to all functions related to the forum. This ensures that only authenticated users can access these pages or post new messages. Without this decorator, the application fails to enforce proper authentication checks.

## FLAW 5: Security Logging and Monitoring Failures

### Problem
The application does not log login attempts, including failed attempts. This omission allows attackers to brute-force credentials without being detected, as no evidence of their attempts is captured.

### Fix
Implement a logging mechanism for login attempts using a custom Django model, such as FailedLoginAttempt. This model should store the following:

- The username entered.
- The IP address of the requester.
- The timestamp of the attempt.

You can acquire the IP address using a helper function added at the end of views.py. The logging code should be included in the login view to record failed attempts.

Solutions shown on these lines of code:
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/models.py#8
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#36
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#37
https://github.com/gitjuli94/SuspiciousChat/blob/main/src/pages/views.py#99

